#!/bin/bash

# سكريبت مراقبة مشروع POP Materials
# يمكن تشغيله كـ cron job للمراقبة التلقائية

PROJECT_NAME="pop-materials"
LOG_FILE="/var/log/$PROJECT_NAME-monitor.log"
ALERT_EMAIL="admin@smart-sense.site"  # غير هذا إلى بريدك الإلكتروني

# دالة للطباعة مع الوقت
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a $LOG_FILE
}

# دالة لإرسال تنبيه
send_alert() {
    local message="$1"
    log "🚨 تنبيه: $message"
    
    # إرسال بريد إلكتروني (يتطلب تثبيت mailutils)
    if command -v mail &> /dev/null; then
        echo "$message" | mail -s "تنبيه: $PROJECT_NAME" $ALERT_EMAIL
    fi
    
    # يمكن إضافة تنبيهات أخرى هنا (Slack, Discord, إلخ)
}

# فحص حالة Docker
check_docker() {
    if ! docker-compose -f docker-compose.prod.yml ps | grep -q "Up"; then
        send_alert "التطبيق متوقف أو لا يعمل بشكل صحيح"
        return 1
    fi
    return 0
}

# فحص الوصول للتطبيق
check_app_health() {
    if ! curl -f http://localhost:5001/ &> /dev/null; then
        send_alert "لا يمكن الوصول للتطبيق على المنفذ 5001"
        return 1
    fi
    return 0
}

# فحص مساحة القرص
check_disk_space() {
    local usage=$(df / | awk 'NR==2 {print $5}' | sed 's/%//')
    if [ $usage -gt 85 ]; then
        send_alert "مساحة القرص ممتلئة: ${usage}%"
        return 1
    fi
    return 0
}

# فحص استخدام الذاكرة
check_memory() {
    local usage=$(free | awk 'NR==2{printf "%.0f", $3*100/$2}')
    if [ $usage -gt 90 ]; then
        send_alert "استخدام الذاكرة مرتفع: ${usage}%"
        return 1
    fi
    return 0
}

# فحص حجم قاعدة البيانات
check_database_size() {
    if [ -f "database.db" ]; then
        local size=$(du -m database.db | cut -f1)
        if [ $size -gt 1000 ]; then  # أكثر من 1GB
            send_alert "حجم قاعدة البيانات كبير: ${size}MB"
        fi
    fi
}

# فحص اللوجز للأخطاء
check_logs() {
    local error_count=$(docker-compose -f docker-compose.prod.yml logs --since="1h" | grep -i error | wc -l)
    if [ $error_count -gt 10 ]; then
        send_alert "عدد كبير من الأخطاء في اللوجز: $error_count خطأ في الساعة الماضية"
    fi
}

# تنظيف تلقائي
auto_cleanup() {
    # تنظيف اللوجز القديمة
    find /var/log -name "*$PROJECT_NAME*" -mtime +30 -delete
    
    # تنظيف Docker
    docker system prune -f --volumes &> /dev/null
    
    log "✅ تم التنظيف التلقائي"
}

# إعادة تشغيل التطبيق إذا لزم الأمر
restart_if_needed() {
    if ! check_docker || ! check_app_health; then
        log "🔄 إعادة تشغيل التطبيق..."
        docker-compose -f docker-compose.prod.yml restart
        sleep 30
        
        if check_docker && check_app_health; then
            log "✅ تم إعادة تشغيل التطبيق بنجاح"
        else
            send_alert "فشل في إعادة تشغيل التطبيق"
        fi
    fi
}

# عرض تقرير الحالة
show_status() {
    echo "📊 تقرير حالة $PROJECT_NAME - $(date)"
    echo "=================================="
    
    # حالة Docker
    echo "🐳 حالة Docker:"
    docker-compose -f docker-compose.prod.yml ps
    echo ""
    
    # استخدام الموارد
    echo "💾 استخدام الموارد:"
    echo "القرص: $(df / | awk 'NR==2 {print $5}')"
    echo "الذاكرة: $(free | awk 'NR==2{printf "%.0f%%", $3*100/$2}')"
    echo "المعالج: $(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1)%"
    echo ""
    
    # حجم قاعدة البيانات
    if [ -f "database.db" ]; then
        echo "🗄️ حجم قاعدة البيانات: $(du -h database.db | cut -f1)"
    fi
    
    # عدد الصور
    if [ -d "static/uploads" ]; then
        echo "🖼️ عدد الصور: $(find static/uploads -type f | wc -l)"
        echo "حجم مجلد الصور: $(du -sh static/uploads | cut -f1)"
    fi
    
    echo ""
}

# الدالة الرئيسية
main() {
    case "${1:-monitor}" in
        "monitor")
            log "🔍 بدء المراقبة..."
            check_docker
            check_app_health
            check_disk_space
            check_memory
            check_database_size
            check_logs
            log "✅ انتهت المراقبة"
            ;;
        "restart")
            restart_if_needed
            ;;
        "cleanup")
            auto_cleanup
            ;;
        "status")
            show_status
            ;;
        "full")
            log "🔍 مراقبة شاملة..."
            check_docker
            check_app_health
            check_disk_space
            check_memory
            check_database_size
            check_logs
            restart_if_needed
            auto_cleanup
            show_status
            log "✅ انتهت المراقبة الشاملة"
            ;;
        *)
            echo "الاستخدام: $0 {monitor|restart|cleanup|status|full}"
            echo ""
            echo "الأوامر:"
            echo "  monitor  - مراقبة أساسية"
            echo "  restart  - إعادة تشغيل إذا لزم الأمر"
            echo "  cleanup  - تنظيف تلقائي"
            echo "  status   - عرض تقرير الحالة"
            echo "  full     - مراقبة شاملة مع إعادة تشغيل وتنظيف"
            exit 1
            ;;
    esac
}

# تشغيل الدالة الرئيسية
main "$@"