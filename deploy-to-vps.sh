#!/bin/bash

# سكريبت نشر مشروع POP Materials على VPS
# الاستخدام: ./deploy-to-vps.sh [domain] [port]

set -e  # إيقاف السكريبت عند أي خطأ

# الألوان للرسائل
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# المتغيرات الافتراضية
DEFAULT_DOMAIN="pop-new.yourdomain.com"
DEFAULT_PORT="5001"
PROJECT_NAME="pop-materials-new"
PROJECT_DIR="/opt/$PROJECT_NAME"

# قراءة المعاملات
DOMAIN=${1:-$DEFAULT_DOMAIN}
PORT=${2:-$DEFAULT_PORT}

echo -e "${BLUE}🚀 بدء نشر مشروع POP Materials${NC}"
echo -e "${BLUE}📋 الإعدادات:${NC}"
echo -e "   الدومين: $DOMAIN"
echo -e "   المنفذ: $PORT"
echo -e "   مجلد المشروع: $PROJECT_DIR"
echo ""

# التحقق من صلاحيات الجذر
if [[ $EUID -ne 0 ]]; then
   echo -e "${RED}❌ هذا السكريبت يحتاج صلاحيات الجذر (sudo)${NC}"
   exit 1
fi

# دالة للتحقق من وجود الأمر
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# التحقق من المتطلبات
echo -e "${YELLOW}🔍 التحقق من المتطلبات...${NC}"

if ! command_exists docker; then
    echo -e "${RED}❌ Docker غير مثبت${NC}"
    echo "تثبيت Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    systemctl enable docker
    systemctl start docker
    echo -e "${GREEN}✅ تم تثبيت Docker${NC}"
fi

if ! command_exists docker-compose; then
    echo -e "${RED}❌ Docker Compose غير مثبت${NC}"
    echo "تثبيت Docker Compose..."
    curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
    echo -e "${GREEN}✅ تم تثبيت Docker Compose${NC}"
fi

if ! command_exists nginx; then
    echo -e "${RED}❌ Nginx غير مثبت${NC}"
    echo "تثبيت Nginx..."
    apt update
    apt install -y nginx
    systemctl enable nginx
    systemctl start nginx
    echo -e "${GREEN}✅ تم تثبيت Nginx${NC}"
fi

if ! command_exists certbot; then
    echo -e "${RED}❌ Certbot غير مثبت${NC}"
    echo "تثبيت Certbot..."
    apt install -y certbot python3-certbot-nginx
    echo -e "${GREEN}✅ تم تثبيت Certbot${NC}"
fi

# إنشاء مجلد المشروع
echo -e "${YELLOW}📁 إعداد مجلد المشروع...${NC}"
mkdir -p $PROJECT_DIR
cd $PROJECT_DIR

# استنساخ أو تحديث المشروع
if [ -d ".git" ]; then
    echo -e "${YELLOW}🔄 تحديث المشروع الموجود...${NC}"
    git pull origin main
else
    echo -e "${YELLOW}📥 استنساخ المشروع...${NC}"
    # تحتاج لتغيير هذا الرابط لمستودعك
    read -p "أدخل رابط المستودع: " REPO_URL
    git clone $REPO_URL .
fi

# إعداد ملف البيئة
echo -e "${YELLOW}⚙️ إعداد متغيرات البيئة...${NC}"
if [ ! -f ".env" ]; then
    cp .env.example .env
    
    # إنشاء مفتاح سري عشوائي
    SECRET_KEY=$(openssl rand -hex 32)
    sed -i "s/your-secret-key-change-this/$SECRET_KEY/g" .env
    
    echo -e "${GREEN}✅ تم إنشاء ملف .env${NC}"
else
    echo -e "${GREEN}✅ ملف .env موجود${NC}"
fi

# تحديث المنفذ في docker-compose
echo -e "${YELLOW}🐳 إعداد Docker Compose...${NC}"
if [ -f "docker-compose.prod.yml" ]; then
    sed -i "s/5001:5000/$PORT:5000/g" docker-compose.prod.yml
    echo -e "${GREEN}✅ تم تحديث المنفذ في Docker Compose${NC}"
fi

# بناء وتشغيل الحاوية
echo -e "${YELLOW}🔨 بناء وتشغيل الحاوية...${NC}"
docker-compose -f docker-compose.prod.yml down 2>/dev/null || true
docker-compose -f docker-compose.prod.yml up -d --build

# انتظار تشغيل الحاوية
echo -e "${YELLOW}⏳ انتظار تشغيل التطبيق...${NC}"
sleep 10

# التحقق من حالة الحاوية
if docker-compose -f docker-compose.prod.yml ps | grep -q "Up"; then
    echo -e "${GREEN}✅ الحاوية تعمل بنجاح${NC}"
else
    echo -e "${RED}❌ فشل في تشغيل الحاوية${NC}"
    docker-compose -f docker-compose.prod.yml logs
    exit 1
fi

# إعداد Nginx
echo -e "${YELLOW}🌐 إعداد Nginx...${NC}"

# إنشاء ملف إعداد Nginx
cat > /etc/nginx/sites-available/$PROJECT_NAME << EOF
server {
    listen 80;
    server_name $DOMAIN;

    location / {
        proxy_pass http://localhost:$PORT;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_cache_bypass \$http_upgrade;
        
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    location /static/ {
        proxy_pass http://localhost:$PORT/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    client_max_body_size 16M;
}
EOF

# تفعيل الموقع
ln -sf /etc/nginx/sites-available/$PROJECT_NAME /etc/nginx/sites-enabled/

# اختبار إعداد Nginx
if nginx -t; then
    echo -e "${GREEN}✅ إعداد Nginx صحيح${NC}"
    systemctl reload nginx
else
    echo -e "${RED}❌ خطأ في إعداد Nginx${NC}"
    exit 1
fi

# إعداد SSL
echo -e "${YELLOW}🔒 إعداد شهادة SSL...${NC}"
read -p "هل تريد إعداد شهادة SSL للدومين $DOMAIN؟ (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    certbot --nginx -d $DOMAIN --non-interactive --agree-tos --email admin@$DOMAIN
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ تم إعداد SSL بنجاح${NC}"
    else
        echo -e "${YELLOW}⚠️ فشل في إعداد SSL - يمكنك إعداده لاحقاً${NC}"
    fi
fi

# إعداد النسخ الاحتياطية
echo -e "${YELLOW}💾 إعداد النسخ الاحتياطية...${NC}"
mkdir -p /opt/backups/$PROJECT_NAME

cat > /opt/backups/backup-$PROJECT_NAME.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/opt/backups/PROJECT_NAME_PLACEHOLDER"
PROJECT_DIR="/opt/PROJECT_NAME_PLACEHOLDER"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# نسخ قاعدة البيانات
cp $PROJECT_DIR/database.db $BACKUP_DIR/database_$DATE.db

# نسخ الصور
tar -czf $BACKUP_DIR/uploads_$DATE.tar.gz -C $PROJECT_DIR/static uploads/ 2>/dev/null || true

# حذف النسخ القديمة (أكثر من 30 يوم)
find $BACKUP_DIR -name "*.db" -mtime +30 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +30 -delete

echo "$(date): تم إنشاء نسخة احتياطية"
EOF

# استبدال المتغيرات في سكريبت النسخ الاحتياطي
sed -i "s/PROJECT_NAME_PLACEHOLDER/$PROJECT_NAME/g" /opt/backups/backup-$PROJECT_NAME.sh
chmod +x /opt/backups/backup-$PROJECT_NAME.sh

# إضافة للـ crontab
(crontab -l 2>/dev/null; echo "0 3 * * * /opt/backups/backup-$PROJECT_NAME.sh >> /var/log/backup-$PROJECT_NAME.log 2>&1") | crontab -

echo -e "${GREEN}✅ تم إعداد النسخ الاحتياطية${NC}"

# إنشاء سكريبت مراقبة
echo -e "${YELLOW}👁️ إعداد المراقبة...${NC}"
cat > /opt/monitor-$PROJECT_NAME.sh << EOF
#!/bin/bash
CONTAINER_NAME="$PROJECT_NAME"
DOMAIN="$DOMAIN"
PROJECT_DIR="$PROJECT_DIR"

# التحقق من حالة الحاوية
if ! docker ps | grep -q \$CONTAINER_NAME; then
    echo "\$(date): ⚠️ الحاوية متوقفة - إعادة تشغيل..."
    cd \$PROJECT_DIR
    docker-compose -f docker-compose.prod.yml up -d
fi

# التحقق من الاستجابة
if ! curl -f -s http://localhost:$PORT > /dev/null; then
    echo "\$(date): ⚠️ التطبيق لا يستجيب - إعادة تشغيل..."
    cd \$PROJECT_DIR
    docker-compose -f docker-compose.prod.yml restart
fi
EOF

chmod +x /opt/monitor-$PROJECT_NAME.sh

# إضافة المراقبة للـ crontab (كل 5 دقائق)
(crontab -l 2>/dev/null; echo "*/5 * * * * /opt/monitor-$PROJECT_NAME.sh >> /var/log/monitor-$PROJECT_NAME.log 2>&1") | crontab -

echo -e "${GREEN}✅ تم إعداد المراقبة${NC}"

# اختبار نهائي
echo -e "${YELLOW}🧪 اختبار النشر...${NC}"
sleep 5

if curl -f -s http://localhost:$PORT > /dev/null; then
    echo -e "${GREEN}✅ التطبيق يعمل على المنفذ $PORT${NC}"
else
    echo -e "${RED}❌ التطبيق لا يستجيب على المنفذ $PORT${NC}"
fi

# عرض النتائج النهائية
echo ""
echo -e "${GREEN}🎉 تم النشر بنجاح!${NC}"
echo -e "${BLUE}📋 معلومات النشر:${NC}"
echo -e "   🌐 الدومين: https://$DOMAIN"
echo -e "   🔌 المنفذ المحلي: $PORT"
echo -e "   📁 مجلد المشروع: $PROJECT_DIR"
echo -e "   🐳 اسم الحاوية: $PROJECT_NAME"
echo -e "   👤 حساب المدير: Admin / admin123"
echo ""
echo -e "${YELLOW}📝 الأوامر المفيدة:${NC}"
echo -e "   عرض اللوجز: docker-compose -f $PROJECT_DIR/docker-compose.prod.yml logs -f"
echo -e "   إعادة تشغيل: docker-compose -f $PROJECT_DIR/docker-compose.prod.yml restart"
echo -e "   إيقاف: docker-compose -f $PROJECT_DIR/docker-compose.prod.yml down"
echo -e "   النسخ الاحتياطية: /opt/backups/backup-$PROJECT_NAME.sh"
echo ""
echo -e "${GREEN}✨ النشر مكتمل!${NC}"