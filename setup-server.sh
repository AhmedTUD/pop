#!/bin/bash

# سكريبت إعداد السيرفر الكامل لمشروع POP Materials
# يجب تشغيله بصلاحيات root على Ubuntu/Debian

echo "🚀 بدء إعداد السيرفر لمشروع POP Materials..."

# تحديث النظام
echo "📦 تحديث النظام..."
apt update && apt upgrade -y

# تثبيت Docker
echo "🐳 تثبيت Docker..."
if ! command -v docker &> /dev/null; then
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    usermod -aG docker $USER
    systemctl enable docker
    systemctl start docker
    rm get-docker.sh
    echo "✅ تم تثبيت Docker"
else
    echo "✅ Docker مثبت مسبقاً"
fi

# تثبيت Docker Compose
echo "🔧 تثبيت Docker Compose..."
if ! command -v docker-compose &> /dev/null; then
    curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
    echo "✅ تم تثبيت Docker Compose"
else
    echo "✅ Docker Compose مثبت مسبقاً"
fi

# تثبيت Nginx
echo "🌐 تثبيت Nginx..."
if ! command -v nginx &> /dev/null; then
    apt install nginx -y
    systemctl enable nginx
    systemctl start nginx
    echo "✅ تم تثبيت Nginx"
else
    echo "✅ Nginx مثبت مسبقاً"
fi

# تثبيت Certbot لشهادات SSL
echo "🔒 تثبيت Certbot..."
if ! command -v certbot &> /dev/null; then
    apt install certbot python3-certbot-nginx -y
    echo "✅ تم تثبيت Certbot"
else
    echo "✅ Certbot مثبت مسبقاً"
fi

# إنشاء مجلد المشروع
PROJECT_DIR="/opt/pop-materials"
echo "📁 إنشاء مجلد المشروع في $PROJECT_DIR..."
mkdir -p $PROJECT_DIR
cd $PROJECT_DIR

echo ""
echo "🎉 تم إعداد السيرفر بنجاح!"
echo ""
echo "📋 الخطوات التالية:"
echo "1. ارفع ملفات المشروع إلى $PROJECT_DIR"
echo "2. انسخ ملف .env.docker إلى .env وعدل القيم"
echo "3. شغل الأمر: ./deploy.sh"
echo "4. أعد إعداد Nginx:"
echo "   - انسخ nginx.conf إلى /etc/nginx/sites-available/pop-materials"
echo "   - فعل الموقع: ln -s /etc/nginx/sites-available/pop-materials /etc/nginx/sites-enabled/"
echo "   - اختبر الإعداد: nginx -t"
echo "   - أعد تشغيل Nginx: systemctl reload nginx"
echo "5. احصل على شهادة SSL:"
echo "   certbot --nginx -d pop.smart-sense.site"
echo ""
echo "🌐 بعد الانتهاء، سيكون التطبيق متاحاً على:"
echo "   https://pop.smart-sense.site"