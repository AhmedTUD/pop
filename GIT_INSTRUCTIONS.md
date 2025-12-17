# تعليمات Git للمشروع

## رفع المشروع على GitHub (للمطور)

### 1. إعداد Git محلياً

```bash
# تشغيل سكريبت الإعداد
chmod +x git-setup.sh
./git-setup.sh
```

أو يدوياً:

```bash
# إعداد معلومات Git
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# تهيئة repository
git init
git remote add origin https://github.com/AhmedTUD/pop.git

# إضافة الملفات
git add .
git commit -m "Initial commit: POP Materials Management System"

# رفع على GitHub
git branch -M main
git push -u origin main
```

### 2. النشر على السيرفر

بعد رفع المشروع على GitHub، يمكن نشره على السيرفر:

#### الطريقة السريعة (نشر تلقائي كامل):

```bash
# على السيرفر
ssh root@your-server-ip

# استنساخ ونشر
git clone https://github.com/AhmedTUD/pop.git
cd pop
chmod +x server-deploy.sh
./server-deploy.sh
```

#### الطريقة اليدوية:

```bash
# على السيرفر
ssh root@your-server-ip

# استنساخ المشروع
git clone https://github.com/AhmedTUD/pop.git
cd pop

# إعداد السيرفر
chmod +x setup-server.sh
sudo ./setup-server.sh

# نسخ المشروع لمجلد الإنتاج
sudo mkdir -p /opt/pop-materials
sudo cp -r . /opt/pop-materials/
cd /opt/pop-materials

# إعداد البيئة
cp .env.docker .env
nano .env  # عدل SECRET_KEY والإعدادات

# نشر التطبيق
chmod +x deploy-production.sh
./deploy-production.sh

# إعداد Nginx
sudo cp nginx.conf /etc/nginx/sites-available/pop-materials
sudo nano /etc/nginx/sites-available/pop-materials  # عدل الدومين
sudo ln -s /etc/nginx/sites-available/pop-materials /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx

# الحصول على SSL
sudo certbot --nginx -d your-domain.com

# إعداد المراقبة
chmod +x crontab-setup.sh
sudo ./crontab-setup.sh
```

## تحديث المشروع

### على GitHub (للمطور):

```bash
# إضافة تغييرات جديدة
git add .
git commit -m "وصف التحديث"
git push origin main
```

### على السيرفر:

```bash
# الانتقال لمجلد المشروع
cd /opt/pop-materials

# سحب التحديثات
git pull origin main

# إعادة نشر التطبيق
./deploy-production.sh
```

## فروع Git (Branches)

### إنشاء فرع جديد للتطوير:

```bash
# إنشاء فرع جديد
git checkout -b feature/new-feature

# العمل على التغييرات
# ... تعديل الملفات ...

# حفظ التغييرات
git add .
git commit -m "إضافة ميزة جديدة"

# رفع الفرع
git push origin feature/new-feature
```

### دمج الفرع في الفرع الرئيسي:

```bash
# العودة للفرع الرئيسي
git checkout main

# دمج الفرع الجديد
git merge feature/new-feature

# رفع التحديثات
git push origin main

# حذف الفرع المحلي
git branch -d feature/new-feature

# حذف الفرع من GitHub
git push origin --delete feature/new-feature
```

## أوامر Git مفيدة

```bash
# عرض حالة الملفات
git status

# عرض تاريخ التغييرات
git log --oneline

# عرض الفروق
git diff

# التراجع عن تغييرات غير محفوظة
git checkout -- filename

# التراجع عن آخر commit
git reset --soft HEAD~1

# عرض الفروع
git branch -a

# تنظيف الفروع المحذوفة
git remote prune origin
```

## إعدادات Git المفيدة

```bash
# إعداد محرر النصوص
git config --global core.editor "nano"

# إعداد الألوان
git config --global color.ui auto

# إعداد الاختصارات
git config --global alias.st status
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit

# حفظ كلمة المرور مؤقتاً
git config --global credential.helper cache
```

## استكشاف أخطاء Git

### مشكلة في الـ push:

```bash
# إذا كان هناك تعارض
git pull origin main
# حل التعارضات يدوياً
git add .
git commit -m "حل التعارضات"
git push origin main
```

### نسيان إضافة ملف للـ .gitignore:

```bash
# إزالة الملف من Git مع الاحتفاظ به محلياً
git rm --cached filename

# إضافة الملف للـ .gitignore
echo "filename" >> .gitignore

# حفظ التغييرات
git add .gitignore
git commit -m "إضافة ملف للـ .gitignore"
```

### تغيير آخر commit message:

```bash
git commit --amend -m "الرسالة الجديدة"
```

## نصائح مهمة

1. **اعمل commit بانتظام** مع رسائل واضحة
2. **استخدم فروع منفصلة** للميزات الجديدة
3. **اختبر التغييرات** قبل الـ push
4. **اقرأ .gitignore** للتأكد من عدم رفع ملفات حساسة
5. **اعمل backup** قبل العمليات الكبيرة

## ملفات مهمة في المشروع

- `.gitignore` - الملفات المستبعدة من Git
- `README.md` - وصف المشروع
- `LICENSE` - رخصة المشروع
- `.env.docker` - قالب متغيرات البيئة (لا تحتوي على بيانات حساسة)

**تذكر**: لا ترفع أبداً ملفات تحتوي على:
- كلمات مرور
- مفاتيح API
- قواعد بيانات
- ملفات شخصية