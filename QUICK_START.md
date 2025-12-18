# دليل البدء السريع

## التشغيل المحلي

### الطريقة الأولى: Python مباشرة

```bash
# 1. إعداد المشروع
python setup.py

# 2. تشغيل التطبيق
python run.py
```

### الطريقة الثانية: Docker

```bash
# تشغيل مع Docker
docker-compose up --build
```

## الوصول للتطبيق

- **الرابط**: http://localhost:5000
- **حساب المدير**:
  - اسم المستخدم: `Admin`
  - كلمة المرور: `admin123`

## الملفات المهمة

- `app.py` - التطبيق الرئيسي
- `requirements.txt` - متطلبات Python
- `database.db` - قاعدة البيانات
- `static/` - الملفات الثابتة والصور
- `templates/` - قوالب HTML
- `.env` - إعدادات البيئة

## المشاكل الشائعة

### خطأ في المتطلبات
```bash
pip install -r requirements.txt
```

### خطأ في قاعدة البيانات
```bash
# حذف قاعدة البيانات وإعادة إنشائها
rm database.db
python run.py
```

### خطأ في المنفذ
```bash
# تغيير المنفذ
export PORT=8000
python run.py
```