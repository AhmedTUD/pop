# دليل نشر مشروع POP Materials على Docker

## متطلبات النظام

- Ubuntu/Debian Linux Server
- Docker & Docker Compose
- Nginx (للـ reverse proxy)
- شهادة SSL (Certbot)

## خطوات النشر

### 1. إعداد السيرفر

```bash
# تشغيل سكريبت إعداد السيرفر (كـ root)
sudo bash setup-server.sh
```

### 2. رفع ملفات المشروع

```bash
# إنشاء مجلد المشروع
sudo mkdir -p /opt/pop-materials
cd /opt/pop-materials

# رفع ملفات المشروع (استخدم scp أو git)
# مثال باستخدام git:
git clone your-repository-url .

# أو باستخدام scp من جهازك المحلي:
# scp -r . user@server-ip:/opt/pop-materials/
```

### 3. إعداد متغيرات البيئة

```bash
# نسخ ملف البيئة وتعديله
cp .env.docker .env
nano .env

# تعديل القيم التالية:
SECRET_KEY=your-very-secure-secret-key-here
DATABASE_URL=  # اتركه فارغاً لاستخدام SQLite
```

### 4. تشغيل التطبيق

```bash
# تشغيل سكريبت النشر
chmod +x deploy.sh
./deploy.sh
```

### 5. إعداد Nginx

```bash
# نسخ إعداد Nginx
sudo cp nginx.conf /etc/nginx/sites-available/pop-materials

# تعديل اسم الدومين في الملف
sudo nano /etc/nginx/sites-available/pop-materials
# غير pop.smart-sense.site إلى الساب دومين المطلوب

# تفعيل الموقع
sudo ln -s /etc/nginx/sites-available/pop-materials /etc/nginx/sites-enabled/

# اختبار الإعداد
sudo nginx -t

# إعادة تشغيل Nginx
sudo systemctl reload nginx
```

### 6. الحصول على شهادة SSL

```bash
# الحصول على شهادة SSL مجانية من Let's Encrypt
sudo certbot --nginx -d pop.smart-sense.site

# تجديد الشهادة تلقائياً
sudo crontab -e
# أضف السطر التالي:
# 0 12 * * * /usr/bin/certbot renew --quiet
```

## إدارة التطبيق

### أوامر Docker Compose المفيدة

```bash
# عرض حالة الحاويات
docker-compose ps

# عرض اللوجز
docker-compose logs -f

# إعادة تشغيل التطبيق
docker-compose restart

# إيقاف التطبيق
docker-compose down

# تحديث التطبيق
git pull  # أو رفع الملفات الجديدة
./deploy.sh
```

### مراقبة النظام

```bash
# مراقبة استخدام الموارد
docker stats

# عرض مساحة القرص المستخدمة
docker system df

# تنظيف الملفات غير المستخدمة
docker system prune -a
```

## إعدادات الأمان

### 1. Firewall

```bash
# تفعيل UFW
sudo ufw enable

# السماح بالمنافذ المطلوبة
sudo ufw allow ssh
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# منع الوصول المباشر لمنفذ التطبيق
sudo ufw deny 5001
```

### 2. تحديثات النظام التلقائية

```bash
# تثبيت unattended-upgrades
sudo apt install unattended-upgrades

# تفعيل التحديثات التلقائية
sudo dpkg-reconfigure -plow unattended-upgrades
```

## استكشاف الأخطاء

### مشاكل شائعة وحلولها

1. **التطبيق لا يعمل:**
   ```bash
   docker-compose logs
   ```

2. **مشكلة في قاعدة البيانات:**
   ```bash
   docker-compose exec app python -c "from app import init_db; init_db()"
   ```

3. **مشكلة في الصلاحيات:**
   ```bash
   sudo chown -R 1000:1000 /opt/pop-materials
   ```

4. **مشكلة في Nginx:**
   ```bash
   sudo nginx -t
   sudo systemctl status nginx
   sudo tail -f /var/log/nginx/error.log
   ```

## النسخ الاحتياطي

### نسخ احتياطي لقاعدة البيانات

```bash
# إنشاء نسخة احتياطية
cp database.db backup_$(date +%Y%m%d_%H%M%S).db

# أو باستخدام cron job
echo "0 2 * * * cd /opt/pop-materials && cp database.db backup_\$(date +\%Y\%m\%d_\%H\%M\%S).db" | sudo crontab -
```

### نسخ احتياطي للملفات المرفوعة

```bash
# نسخ احتياطي لمجلد الصور
tar -czf uploads_backup_$(date +%Y%m%d_%H%M%S).tar.gz static/uploads/
```

## المنافذ المستخدمة

- **5001**: منفذ التطبيق الداخلي (Docker)
- **80**: HTTP (Nginx)
- **443**: HTTPS (Nginx)

## معلومات الاتصال

بعد النشر الناجح، سيكون التطبيق متاحاً على:
- **HTTP**: http://pop.smart-sense.site (سيتم إعادة التوجيه إلى HTTPS)
- **HTTPS**: https://pop.smart-sense.site

## ملاحظات مهمة

1. تأكد من تغيير `SECRET_KEY` في ملف `.env`
2. قم بإعداد نسخ احتياطية دورية
3. راقب استخدام الموارد بانتظام
4. حدث النظام والتطبيق بانتظام
5. استخدم شهادات SSL صالحة دائماً