# تعليمات النشر الكاملة

## 📋 الخطوات المطلوبة

### 1. تحديث المستودع

```bash
# تشغيل سكريبت تحديث المستودع
./update-repository.sh

# أو يدوياً:
git add .
git commit -m "🧹 تنظيف المشروع وإعداد النشر"
git push origin main
```

### 2. إعداد VPS

#### متطلبات السيرفر:
- Ubuntu 20.04+ أو Debian 10+
- 2GB RAM (الحد الأدنى)
- 10GB مساحة تخزين
- صلاحيات root

#### الاتصال بالسيرفر:
```bash
ssh root@your-server-ip
# أو
ssh user@your-server-ip
sudo su -
```

### 3. النشر التلقائي

```bash
# نسخ سكريبت النشر للسيرفر
scp deploy-to-vps.sh root@your-server-ip:/tmp/

# تشغيل السكريبت على السيرفر
ssh root@your-server-ip
chmod +x /tmp/deploy-to-vps.sh
/tmp/deploy-to-vps.sh pop-new.yourdomain.com 5001
```

### 4. النشر اليدوي (خطوة بخطوة)

#### أ. تثبيت المتطلبات:
```bash
# تحديث النظام
apt update && apt upgrade -y

# تثبيت Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# تثبيت Docker Compose
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# تثبيت Nginx
apt install -y nginx

# تثبيت Certbot
apt install -y certbot python3-certbot-nginx
```

#### ب. إعداد المشروع:
```bash
# إنشاء مجلد المشروع
mkdir -p /opt/pop-materials-new
cd /opt/pop-materials-new

# استنساخ المشروع
git clone https://github.com/your-username/your-repo.git .

# إعداد البيئة
cp .env.example .env
nano .env  # عدل SECRET_KEY والإعدادات
```

#### ج. تشغيل Docker:
```bash
# بناء وتشغيل الحاوية
docker-compose -f docker-compose.prod.yml up -d --build

# التحقق من الحالة
docker-compose -f docker-compose.prod.yml ps
```

#### د. إعداد Nginx:
```bash
# نسخ إعداد Nginx
cp nginx-subdomain.conf /etc/nginx/sites-available/pop-materials-new

# تعديل الدومين
nano /etc/nginx/sites-available/pop-materials-new
# غير pop-new.yourdomain.com للدومين الخاص بك

# تفعيل الموقع
ln -s /etc/nginx/sites-available/pop-materials-new /etc/nginx/sites-enabled/

# اختبار وإعادة تحميل
nginx -t
systemctl reload nginx
```

#### هـ. إعداد SSL:
```bash
# الحصول على شهادة SSL
certbot --nginx -d pop-new.yourdomain.com
```

### 5. إعداد DNS

في لوحة تحكم الدومين، أضف:
```
Type: A
Name: pop-new
Value: YOUR_SERVER_IP
TTL: 300
```

### 6. اختبار النشر

```bash
# اختبار محلي
curl -I http://localhost:5001

# اختبار الدومين
curl -I https://pop-new.yourdomain.com
```

## 🔧 إدارة المشروع

### أوامر مفيدة:

```bash
# عرض حالة الحاويات
docker-compose -f /opt/pop-materials-new/docker-compose.prod.yml ps

# عرض اللوجز
docker-compose -f /opt/pop-materials-new/docker-compose.prod.yml logs -f

# إعادة تشغيل
docker-compose -f /opt/pop-materials-new/docker-compose.prod.yml restart

# إيقاف
docker-compose -f /opt/pop-materials-new/docker-compose.prod.yml down

# تحديث المشروع
cd /opt/pop-materials-new
git pull origin main
docker-compose -f docker-compose.prod.yml up -d --build
```

### مراقبة النظام:

```bash
# مراقبة استخدام الموارد
docker stats

# مراقبة مساحة القرص
df -h

# مراقبة اللوجز
tail -f /var/log/nginx/pop-materials-new.access.log
```

## 🔒 الأمان

### تغيير كلمة مرور المدير:
1. سجل دخول بحساب Admin
2. اذهب لإدارة المستخدمين
3. غير كلمة المرور

### تحديث النظام:
```bash
# تحديث النظام بانتظام
apt update && apt upgrade -y

# تحديث Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
```

## 📊 النسخ الاحتياطية

### نسخ احتياطية يدوية:
```bash
# نسخ قاعدة البيانات
cp /opt/pop-materials-new/database.db /opt/backups/database_$(date +%Y%m%d).db

# نسخ الصور
tar -czf /opt/backups/uploads_$(date +%Y%m%d).tar.gz -C /opt/pop-materials-new/static uploads/
```

### نسخ احتياطية تلقائية:
السكريبت التلقائي يقوم بإنشاء نسخ احتياطية يومية في 3:00 صباحاً

## 🚨 استكشاف الأخطاء

### المشاكل الشائعة:

#### 1. الحاوية لا تعمل:
```bash
docker-compose -f /opt/pop-materials-new/docker-compose.prod.yml logs
docker-compose -f /opt/pop-materials-new/docker-compose.prod.yml restart
```

#### 2. خطأ في Nginx:
```bash
nginx -t
systemctl status nginx
tail -f /var/log/nginx/error.log
```

#### 3. مشكلة في SSL:
```bash
certbot renew --dry-run
certbot certificates
```

#### 4. مشكلة في قاعدة البيانات:
```bash
# نسخ احتياطية أولاً
cp /opt/pop-materials-new/database.db /opt/backups/database_backup.db

# إعادة إنشاء قاعدة البيانات
rm /opt/pop-materials-new/database.db
docker-compose -f /opt/pop-materials-new/docker-compose.prod.yml restart
```

## 📞 الدعم

إذا واجهت مشاكل:
1. راجع اللوجز أولاً
2. تحقق من حالة الخدمات
3. راجع هذا الدليل
4. أنشئ Issue في GitHub

## 🎯 النتيجة النهائية

بعد اتباع هذه التعليمات، ستحصل على:
- ✅ مشروع يعمل على https://pop-new.yourdomain.com
- ✅ حاوية Docker على المنفذ 5001
- ✅ شهادة SSL تلقائية
- ✅ نسخ احتياطية تلقائية
- ✅ مراقبة تلقائية
- ✅ نظام آمن ومستقر