# استخدام Python 3.11 كصورة أساسية
FROM python:3.11-slim

# تعيين متغير البيئة لمنع إنشاء ملفات .pyc
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# تعيين مجلد العمل
WORKDIR /app

# تثبيت متطلبات النظام
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# نسخ ملف المتطلبات وتثبيتها بالترتيب الصحيح لحل مشكلة numpy/pandas
COPY requirements.txt .

# تحديث pip وتثبيت الأدوات الأساسية
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# تثبيت numpy أولاً
RUN pip install --no-cache-dir numpy==1.26.2

# تثبيت pandas بعد numpy
RUN pip install --no-cache-dir pandas==2.1.4

# تثبيت باقي المكتبات
RUN pip install --no-cache-dir Flask==3.0.0 Werkzeug==3.0.1 openpyxl==3.1.2 Pillow==10.1.0 python-dotenv==1.0.0 gunicorn==21.2.0 requests==2.31.0

# نسخ ملفات المشروع
COPY . .

# إنشاء مجلد uploads إذا لم يكن موجوداً
RUN mkdir -p static/uploads

# تعيين الصلاحيات
RUN chmod +x app.py

# كشف المنفذ
EXPOSE 5000

# تشغيل التطبيق
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "120", "app:app"]