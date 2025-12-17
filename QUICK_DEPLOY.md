# دليل النشر السريع - مشروع POP Materials

## خطوات النشر السريع على VPS Linux

### الطريقة الأولى: النشر التلقائي الكامل (الأسهل)

```bash
# 1. تسجيل الدخول للسيرفر
ssh root@your-server-ip

# 2. استنساخ المشروع
git clone https://github.com/AhmedTUD/pop.git
cd pop

# 3. تشغيل النشر التلقائي الكامل
chmod +x server-deploy.sh
./server-deploy.sh
```

### الطريقة الثانية: النشر اليدوي (للتحكم الكامل)

#### 1. إعداد السيرفر (مرة واحدة فقط)

```bash
# تسجيل الدخول للسيرفر
ssh root@your-server-ip

# استنساخ المشروع
git clone https://github.com/AhmedTUD/pop.git
cd pop

# تشغيل سكريبت الإعداد
chmod +x setup-server.sh
./setup-server.sh
```

#### 2. رفع المشروع

```bash
# إنشاء مجلد المشروع
mkdir -p /opt/pop-materials
cd /opt/pop-materials

# استنساخ المشروع
git clone https://github.com/AhmedTUD/pop.git .
```

### 3. إعداد البيئة

```bash
# نسخ وتعديل ملف البيئة
cp .env.docker .env
nano .env

# تعديل القيم التالية:
SECRET_KEY=your-very-secure-secret-key-here-change-this
DATABASE_URL=  # اتركه فارغاً لاستخدام SQLite
```

### 4. نشر التطبيق

```bash
# تشغيل النشر
chmod +x deploy-production.sh
./deploy-production.sh
```

### 5. إعداد Nginx والدومين

```bash
# نسخ إعداد Nginx
cp nginx.conf /etc/nginx/sites-available/pop-materials

# تعديل الدومين
nano /etc/nginx/sites-available/pop-materials
# غير pop.smart-sense.site إلى الدومين المطلوب

# تفعيل الموقع
ln -s /etc/nginx/sites-available/pop-materials /etc/nginx/sites-enabled/
nginx -t
systemctl reload nginx

# الحصول على شهادة SSL
certbot --nginx -d your-subdomain.smart-sense.site
```

### 6. إعداد المراقبة التلقائية

```bash
# تثبيت المهام التلقائية
chmod +x crontab-setup.sh
./crontab-setup.sh
```

## أوامر سريعة للإدارة

```bash
# عرض حالة التطبيق
docker-compose -f docker-compose.prod.yml ps

# عرض اللوجز
docker-compose -f docker-compose.prod.yml logs -f

# إعادة تشغيل
docker-compose -f docker-compose.prod.yml restart

# إيقاف التطبيق
docker-compose -f docker-compose.prod.yml down

# تحديث التطبيق
git pull  # أو رفع الملفات الجديدة
./deploy-production.sh

# مراقبة النظام
./monitor.sh status
```

## معلومات مهمة

- **المنفذ المحلي**: 5001
- **الدومين**: https://your-subdomain.smart-sense.site
- **مجلد المشروع**: /opt/pop-materials
- **النسخ الاحتياطية**: /opt/backups/pop-materials
- **اللوجز**: /var/log/pop-materials-*.log

## استكشاف الأخطاء

```bash
# فحص حالة Docker
docker ps
docker-compose -f docker-compose.prod.yml logs

# فحص Nginx
nginx -t
systemctl status nginx
tail -f /var/log/nginx/error.log

# فحص شهادة SSL
certbot certificates

# فحص المراقبة
./monitor.sh full
```

## نصائح مهمة

1. **غير SECRET_KEY** في ملف .env قبل النشر
2. **اعمل نسخة احتياطية** قبل أي تحديث
3. **راقب اللوجز** بانتظام
4. **حدث النظام** شهرياً
5. **تحقق من شهادة SSL** قبل انتهائها

## الدعم

إذا واجهت مشاكل:
1. تحقق من اللوجز: `docker-compose logs`
2. تحقق من حالة النظام: `./monitor.sh status`
3. أعد تشغيل التطبيق: `./deploy-production.sh`