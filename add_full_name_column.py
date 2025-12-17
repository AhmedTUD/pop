#!/usr/bin/env python3
"""
سكريبت لإضافة عمود full_name لقاعدة البيانات
"""

import sqlite3
import os

def add_full_name_column():
    """إضافة عمود full_name لجدول users"""

    # البحث عن ملف قاعدة البيانات
    db_files = ['database.db', 'app.db', 'users.db']
    db_path = None

    for db_file in db_files:
        if os.path.exists(db_file):
            db_path = db_file
            break

    if not db_path:
        print("❌ لم يتم العثور على ملف قاعدة البيانات")
        print("الملفات المتوقعة: database.db, app.db, users.db")
        return False

    print(f"📁 تم العثور على قاعدة البيانات: {db_path}")

    try:
        # الاتصال بقاعدة البيانات
        conn = sqlite3.connect(db_path)
        c = conn.cursor()

        # فحص هيكل الجدول الحالي
        c.execute("PRAGMA table_info(users)")
        columns = c.fetchall()

        print("📋 هيكل جدول users الحالي:")
        for col in columns:
            print(f"   - {col[1]} ({col[2]})")

        # فحص إذا كان العمود موجود
        column_names = [col[1] for col in columns]

        if 'full_name' in column_names:
            print("✅ عمود full_name موجود بالفعل")
            return True

        # إضافة العمود
        print("🔧 جاري إضافة عمود full_name...")
        c.execute('ALTER TABLE users ADD COLUMN full_name TEXT')

        # فحص النتيجة
        c.execute("PRAGMA table_info(users)")
        new_columns = c.fetchall()

        print("📋 هيكل الجدول بعد التحديث:")
        for col in new_columns:
            print(f"   - {col[1]} ({col[2]})")

        conn.commit()
        conn.close()

        print("✅ تم إضافة عمود full_name بنجاح!")
        return True

    except sqlite3.OperationalError as e:
        print(f"❌ خطأ في قاعدة البيانات: {e}")
        return False
    except Exception as e:
        print(f"❌ خطأ عام: {e}")
        return False

if __name__ == "__main__":
    print("🚀 بدء إضافة عمود full_name لقاعدة البيانات...")
    print("=" * 50)

    success = add_full_name_column()

    print("=" * 50)
    if success:
        print("🎉 تم الانتهاء بنجاح!")
        print("يمكنك الآن تشغيل التطبيق بدون مشاكل")
    else:
        print("❌ فشل في إضافة العمود")
        print("تأكد من وجود ملف قاعدة البيانات وأن لديك صلاحيات الكتابة")