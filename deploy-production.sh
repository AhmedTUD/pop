#!/bin/bash

# سكريبت نشر الإنتاج المحسن لمشروع POP Materials
# للاستخدام على VPS Linux في بيئة الإنتاج

set -e  # إيقاف السكريبت عند أي خطأ

PROJECT_NAME="pop-materials"
DOMAIN="pop.smart-sense.site"  # غير هذا إلى الدومين المطلوب
BACKUP_DIR="/opt/backups/$PROJECT_NAME"
LOG_FILE="/var/log/$PROJECT_NAME-deploy.log"

# دالة للطباعة مع الوقت
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a $LOG_FILE
}

# دالة للنسخ الاحتياطي
backup_data() {
    log "📦 إنشاء نسخة احتياطية..."
    
    mkdir -p $BACKUP_DIR
    TIMESTAMP=$(date +%Y%m%d_%H%M%S)
    
    # نسخ احتياطي لقاعدة البيانات
    if [ -f "database.db" ]; then
        cp database.db "$BACKUP_DIR/database_$TIMESTAMP.db"
        log "✅ تم نسخ قاعدة البيانات"
    fi
    
    # نسخ احتياطي للصور
    if [ -d "static/uploads" ]; then
        tar -czf "$BACKUP_DIR/uploads_$TIMESTAMP.tar.gz" static/uploads/
        log "✅ تم نسخ الصور"
    fi
    
    # حذف النسخ القديمة (أكثر من 7 أيام)
    find $BACKUP_DIR -name "*.db" -mtime +7 -delete
    find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete
}

# دالة للتحقق من المتطلبات
check_requirements() {
    log "🔍 التحقق من المتطلبات..."
    
    if ! command -v docker &> /dev/null; then
        log "❌ Docker غير مثبت"
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        log "❌ Docker Compose غير مثبت"
        exit 1
    fi
    
    if [ ! -f ".env" ]; then
        log "❌ ملف .env غير موجود"
        exit 1
    fi
    
    log "✅ جميع المتطلبات متوفرة"
}

# دالة لإعداد الملفات
setup_files() {
    log "📁 إعداد الملفات والمجلدات..."
    
    # إنشاء المجلدات المطلوبة
    mkdir -p static/uploads
    mkdir -p logs
    mkdir -p nginx/sites-enabled
    mkdir -p ssl
    
    # تعيين الصلاحيات
    chmod 755 static/uploads
    chmod 755 logs
    
    log "✅ تم إعداد الملفات"
}

# دالة لبناء ونشر التطبيق
deploy_app() {
    log "🚀 بدء نشر التطبيق..."
    
    # إيقاف الحاويات السابقة
    log "🛑 إيقاف الحاويات السابقة..."
    docker-compose -f docker-compose.prod.yml down --remove-orphans
    
    # بناء الصورة الجديدة
    log "🔨 بناء صورة Docker..."
    docker-compose -f docker-compose.prod.yml build --no-cache --pull
    
    # تشغيل الحاويات
    log "▶️ تشغيل التطبيق..."
    docker-compose -f docker-compose.prod.yml up -d
    
    # انتظار بدء التطبيق
    log "⏳ انتظار بدء التطبيق..."
    sleep 10
    
    # التحقق من حالة الحاويات
    if docker-compose -f docker-compose.prod.yml ps | grep -q "Up"; then
        log "✅ تم تشغيل التطبيق بنجاح"
    else
        log "❌ فشل في تشغيل التطبيق"
        docker-compose -f docker-compose.prod.yml logs
        exit 1
    fi
}

# دالة للتحقق من صحة التطبيق
health_check() {
    log "🏥 فحص صحة التطبيق..."
    
    # انتظار حتى يصبح التطبيق جاهزاً
    for i in {1..30}; do
        if curl -f http://localhost:5001/ &> /dev/null; then
            log "✅ التطبيق يعمل بشكل صحيح"
            return 0
        fi
        log "⏳ انتظار التطبيق... ($i/30)"
        sleep 2
    done
    
    log "❌ فشل في الوصول للتطبيق"
    docker-compose -f docker-compose.prod.yml logs --tail=50
    exit 1
}

# دالة لتنظيف Docker
cleanup_docker() {
    log "🧹 تنظيف Docker..."
    
    # حذف الصور غير المستخدمة
    docker image prune -f
    
    # حذف الحاويات المتوقفة
    docker container prune -f
    
    # حذف الشبكات غير المستخدمة
    docker network prune -f
    
    log "✅ تم تنظيف Docker"
}

# دالة لعرض معلومات النشر
show_info() {
    log "📊 معلومات النشر:"
    echo ""
    echo "🌐 التطبيق متاح على:"
    echo "   - المنفذ المحلي: http://localhost:5001"
    echo "   - الدومين: https://$DOMAIN"
    echo ""
    echo "📋 أوامر مفيدة:"
    echo "   - عرض اللوجز: docker-compose -f docker-compose.prod.yml logs -f"
    echo "   - حالة الحاويات: docker-compose -f docker-compose.prod.yml ps"
    echo "   - إعادة تشغيل: docker-compose -f docker-compose.prod.yml restart"
    echo "   - إيقاف: docker-compose -f docker-compose.prod.yml down"
    echo ""
    echo "📁 مجلدات مهمة:"
    echo "   - قاعدة البيانات: ./database.db"
    echo "   - الصور: ./static/uploads/"
    echo "   - اللوجز: ./logs/"
    echo "   - النسخ الاحتياطية: $BACKUP_DIR"
    echo ""
}

# تشغيل السكريبت الرئيسي
main() {
    log "🚀 بدء نشر مشروع POP Materials - الإنتاج"
    
    check_requirements
    backup_data
    setup_files
    deploy_app
    health_check
    cleanup_docker
    show_info
    
    log "🎉 تم نشر التطبيق بنجاح!"
}

# تشغيل الدالة الرئيسية
main "$@"