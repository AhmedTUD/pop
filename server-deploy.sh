#!/bin/bash

# سكريبت النشر الكامل على السيرفر
# يجب تشغيله على السيرفر بعد clone المشروع

set -e

PROJECT_DIR="/opt/pop-materials"
DOMAIN="pop.smart-sense.site"  # غير هذا حسب الحاجة
LOG_FILE="/var/log/pop-deploy.log"

# دالة للطباعة مع الوقت
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a $LOG_FILE
}

echo "🚀 بدء النشر الكامل لمشروع POP Materials على السيرفر"
echo "=================================================="

# التحقق من أننا في المجلد الصحيح
if [ ! -f "app.py" ]; then
    echo "❌ يجب تشغيل هذا السكريبت من داخل مجلد المشروع"
    exit 1
fi

# إنشاء مجلد المشروع ونسخ الملفات
log "📁 إعداد مجلد المشروع..."
sudo mkdir -p $PROJECT_DIR
sudo cp -r . $PROJECT_DIR/
cd $PROJECT_DIR

# تعيين الصلاحيات
sudo chown -R $USER:$USER $PROJECT_DIR
chmod +x *.sh

# إعداد ملف البيئة
log "⚙️ إعداد ملف البيئة..."
if [ ! -f ".env" ]; then
    cp .env.docker .env
    echo ""
    echo "📝 يرجى تعديل ملف .env بالقيم الصحيحة:"
    echo "   - SECRET_KEY: مفتاح تشفير قوي"
    echo "   - DATABASE_URL: رابط قاعدة البيانات (اتركه فارغاً لـ SQLite)"
    echo ""
    read -p "اضغط Enter بعد تعديل ملف .env..." -r
    nano .env
fi

# تشغيل إعداد السيرفر إذا لم يكن معداً
log "🔧 التحقق من إعداد السيرفر..."
if ! command -v docker &> /dev/null; then
    log "🐳 تثبيت Docker والمتطلبات..."
    sudo ./setup-server.sh
else
    log "✅ Docker مثبت مسبقاً"
fi

# نشر التطبيق
log "🚀 نشر التطبيق..."
./deploy-production.sh

# إعداد Nginx
log "🌐 إعداد Nginx..."
sudo cp nginx.conf /etc/nginx/sites-available/pop-materials

# تعديل الدومين في ملف Nginx
log "📝 تعديل إعدادات Nginx..."
sudo sed -i "s/pop\.smart-sense\.site/$DOMAIN/g" /etc/nginx/sites-available/pop-materials

# تفعيل الموقع
sudo ln -sf /etc/nginx/sites-available/pop-materials /etc/nginx/sites-enabled/

# اختبار إعداد Nginx
if sudo nginx -t; then
    log "✅ إعداد Nginx صحيح"
    sudo systemctl reload nginx
else
    log "❌ خطأ في إعداد Nginx"
    exit 1
fi

# إعداد SSL
log "🔒 إعداد شهادة SSL..."
if command -v certbot &> /dev/null; then
    echo ""
    echo "🔐 الحصول على شهادة SSL..."
    echo "سيتم طلب شهادة SSL للدومين: $DOMAIN"
    read -p "هل تريد المتابعة؟ (y/n): " -r
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        sudo certbot --nginx -d $DOMAIN --non-interactive --agree-tos --email admin@smart-sense.site || {
            log "⚠️ فشل في الحصول على شهادة SSL - يمكن إعدادها لاحقاً"
        }
    fi
else
    log "⚠️ Certbot غير مثبت - تخطي إعداد SSL"
fi

# إعداد المراقبة التلقائية
log "📊 إعداد المراقبة التلقائية..."
sudo ./crontab-setup.sh

# إعداد Firewall
log "🛡️ إعداد Firewall..."
if command -v ufw &> /dev/null; then
    sudo ufw --force enable
    sudo ufw allow ssh
    sudo ufw allow 80/tcp
    sudo ufw allow 443/tcp
    sudo ufw deny 5001  # منع الوصول المباشر للتطبيق
    log "✅ تم إعداد Firewall"
fi

# التحقق النهائي
log "🏥 فحص صحة النظام..."
sleep 10

if curl -f http://localhost:5001/ &> /dev/null; then
    log "✅ التطبيق يعمل محلياً"
else
    log "❌ مشكلة في التطبيق المحلي"
fi

if curl -f http://$DOMAIN/ &> /dev/null; then
    log "✅ التطبيق يعمل عبر الدومين"
else
    log "⚠️ تحقق من إعدادات DNS للدومين"
fi

# عرض معلومات النشر
echo ""
echo "🎉 تم النشر بنجاح!"
echo "==================="
echo ""
echo "🌐 معلومات الوصول:"
echo "   - الدومين: https://$DOMAIN"
echo "   - المنفذ المحلي: http://localhost:5001"
echo ""
echo "👤 حساب المدير الافتراضي:"
echo "   - اسم المستخدم: Admin"
echo "   - كلمة المرور: admin123"
echo ""
echo "📁 مجلدات مهمة:"
echo "   - المشروع: $PROJECT_DIR"
echo "   - النسخ الاحتياطية: /opt/backups/pop-materials"
echo "   - اللوجز: /var/log/pop-*.log"
echo ""
echo "🔧 أوامر إدارية مفيدة:"
echo "   - حالة التطبيق: docker-compose -f docker-compose.prod.yml ps"
echo "   - عرض اللوجز: docker-compose -f docker-compose.prod.yml logs -f"
echo "   - إعادة تشغيل: docker-compose -f docker-compose.prod.yml restart"
echo "   - مراقبة النظام: ./monitor.sh status"
echo "   - تحديث التطبيق: git pull && ./deploy-production.sh"
echo ""
echo "📊 المراقبة التلقائية:"
echo "   - فحص كل 5 دقائق"
echo "   - نسخ احتياطية يومية"
echo "   - تجديد SSL تلقائي"
echo ""

log "🎯 النشر مكتمل بنجاح!"