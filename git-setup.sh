#!/bin/bash

# سكريبت إعداد ورفع المشروع على Git

echo "🚀 إعداد المشروع لرفعه على Git..."

# التحقق من وجود Git
if ! command -v git &> /dev/null; then
    echo "❌ Git غير مثبت. يرجى تثبيت Git أولاً"
    exit 1
fi

# إعداد Git إذا لم يكن معداً
echo "📝 إعداد معلومات Git..."
read -p "أدخل اسمك: " git_name
read -p "أدخل بريدك الإلكتروني: " git_email

git config --global user.name "$git_name"
git config --global user.email "$git_email"

# تهيئة Git repository
echo "🔧 تهيئة Git repository..."
git init

# إضافة remote origin
echo "🌐 إضافة remote repository..."
git remote add origin https://github.com/AhmedTUD/pop.git

# إضافة جميع الملفات
echo "📁 إضافة الملفات..."
git add .

# إنشاء أول commit
echo "💾 إنشاء أول commit..."
git commit -m "Initial commit: POP Materials Management System

- إضافة نظام إدارة مواد POP كامل
- دعم Docker و Docker Compose
- إعداد Nginx للـ reverse proxy
- نظام مراقبة ونسخ احتياطية تلقائية
- واجهة إدارية متقدمة
- دعم رفع الصور وتصدير Excel
- إعدادات أمان متقدمة
- دليل نشر شامل"

# رفع على GitHub
echo "⬆️ رفع المشروع على GitHub..."
git branch -M main
git push -u origin main

echo ""
echo "🎉 تم رفع المشروع بنجاح على GitHub!"
echo "🌐 رابط المشروع: https://github.com/AhmedTUD/pop"
echo ""
echo "📋 الخطوات التالية:"
echo "1. تأكد من أن المشروع ظهر على GitHub"
echo "2. انتقل للسيرفر وشغل أوامر الـ clone والنشر"
echo ""
echo "🖥️ أوامر النشر على السيرفر:"
echo "git clone https://github.com/AhmedTUD/pop.git"
echo "cd pop"
echo "chmod +x setup-server.sh && sudo ./setup-server.sh"
echo "cp .env.docker .env && nano .env"
echo "chmod +x deploy-production.sh && ./deploy-production.sh"