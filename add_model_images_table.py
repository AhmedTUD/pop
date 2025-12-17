#!/usr/bin/env python3
"""
إضافة جدول model_images لقاعدة البيانات الموجودة
يجب تشغيل هذا الملف على PythonAnywhere لإضافة الجدول المفقود
"""

import sqlite3
import os
from datetime import datetime

def add_model_images_table():
    """إضافة جدول model_images إلى قاعدة البيانات"""

    print("🔧 إضافة جدول model_images...")

    try:
        # الاتصال بقاعدة البيانات
        conn = sqlite3.connect('database.db')
        c = conn.cursor()

        # التحقق من وجود الجدول
        c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='model_images'")
        table_exists = c.fetchone()

        if table_exists:
            print("✅ جدول model_images موجود بالفعل")
            return True

        # إنشاء جدول model_images
        c.execute('''CREATE TABLE IF NOT EXISTS model_images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            model_name TEXT NOT NULL,
            category_name TEXT NOT NULL,
            image_url TEXT NOT NULL,
            created_date TEXT NOT NULL,
            UNIQUE(model_name, category_name)
        )''')

        conn.commit()
        print("✅ تم إنشاء جدول model_images بنجاح")

        # التحقق من إنشاء الجدول
        c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='model_images'")
        if c.fetchone():
            print("✅ تم التأكد من إنشاء الجدول")

            # عرض بنية الجدول
            c.execute("PRAGMA table_info(model_images)")
            columns = c.fetchall()
            print("\n📋 بنية جدول model_images:")
            for col in columns:
                print(f"   - {col[1]} ({col[2]})")

            return True
        else:
            print("❌ فشل في إنشاء الجدول")
            return False

    except Exception as e:
        print(f"❌ خطأ في إضافة الجدول: {e}")
        return False

    finally:
        if conn:
            conn.close()

def check_all_tables():
    """فحص جميع الجداول في قاعدة البيانات"""

    print("\n📊 فحص جميع الجداول...")

    try:
        conn = sqlite3.connect('database.db')
        c = conn.cursor()

        # الحصول على قائمة جميع الجداول
        c.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = c.fetchall()

        print(f"\n📋 الجداول الموجودة ({len(tables)} جدول):")
        for table in tables:
            table_name = table[0]

            # عد الصفوف في كل جدول
            c.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = c.fetchone()[0]

            print(f"   ✅ {table_name}: {count} صف")

        # التحقق من الجداول المطلوبة
        required_tables = [
            'users', 'data_entries', 'branches', 'categories',
            'models', 'display_types', 'pop_materials_db',
            'user_branches', 'model_images', 'db_init_status'
        ]

        existing_tables = [table[0] for table in tables]
        missing_tables = [table for table in required_tables if table not in existing_tables]

        if missing_tables:
            print(f"\n⚠️ الجداول المفقودة: {missing_tables}")
        else:
            print("\n✅ جميع الجداول المطلوبة موجودة")

        return True

    except Exception as e:
        print(f"❌ خطأ في فحص الجداول: {e}")
        return False

    finally:
        if conn:
            conn.close()

def main():
    """الدالة الرئيسية"""

    print("🚀 بدء إضافة جدول model_images")
    print("=" * 50)

    # التحقق من وجود ملف قاعدة البيانات
    if not os.path.exists('database.db'):
        print("❌ ملف قاعدة البيانات غير موجود!")
        print("تأكد من تشغيل هذا الملف في نفس مجلد app.py")
        return False

    # فحص الجداول الحالية
    check_all_tables()

    # إضافة جدول model_images
    success = add_model_images_table()

    if success:
        # فحص الجداول مرة أخرى
        check_all_tables()

        print("\n" + "=" * 50)
        print("🎉 تم إضافة جدول model_images بنجاح!")
        print("\nالآن يمكنك:")
        print("1. إعادة تشغيل التطبيق")
        print("2. الذهاب إلى صفحة Model Images Management")
        print("3. رفع صور الموديلات")

        return True
    else:
        print("\n" + "=" * 50)
        print("❌ فشل في إضافة الجدول")
        return False

if __name__ == '__main__':
    main()