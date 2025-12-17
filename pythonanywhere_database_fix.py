#!/usr/bin/env python3
"""
إصلاح شامل لقاعدة البيانات على PythonAnywhere
يجب تشغيل هذا الملف على PythonAnywhere لإصلاح جميع المشاكل
"""

import sqlite3
import os
from datetime import datetime

def check_database_exists():
    """التحقق من وجود ملف قاعدة البيانات"""

    print("🔍 التحقق من وجود قاعدة البيانات...")

    if os.path.exists('database.db'):
        size = os.path.getsize('database.db')
        print(f"✅ ملف قاعدة البيانات موجود ({size} bytes)")
        return True
    else:
        print("❌ ملف قاعدة البيانات غير موجود!")
        return False

def check_all_tables():
    """فحص جميع الجداول المطلوبة"""

    print("\n🔍 فحص الجداول المطلوبة...")

    required_tables = {
        'users': ['id', 'name', 'company_code', 'password', 'is_admin', 'created_date'],
        'data_entries': ['id', 'employee_name', 'employee_code', 'branch', 'shop_code', 'model', 'display_type', 'selected_materials', 'unselected_materials', 'images', 'comment', 'date'],
        'branches': ['id', 'branch_name', 'shop_code', 'employee_code', 'created_date'],
        'categories': ['id', 'category_name', 'created_date'],
        'models': ['id', 'model_name', 'category_name', 'created_date'],
        'display_types': ['id', 'display_type_name', 'category_name', 'created_date'],
        'pop_materials_db': ['id', 'material_name', 'model_name', 'category_name', 'created_date'],
        'user_branches': ['id', 'user_id', 'branch_name', 'created_date'],
        'model_images': ['id', 'model_name', 'category_name', 'image_url', 'created_date'],
        'db_init_status': ['id', 'component', 'initialized', 'last_update']
    }

    try:
        conn = sqlite3.connect('database.db')
        c = conn.cursor()

        # فحص الجداول الموجودة
        c.execute("SELECT name FROM sqlite_master WHERE type='table'")
        existing_tables = [row[0] for row in c.fetchall()]

        print(f"📋 الجداول الموجودة ({len(existing_tables)}):")
        for table in existing_tables:
            print(f"   ✅ {table}")

        # فحص الجداول المفقودة
        missing_tables = []
        for table_name in required_tables.keys():
            if table_name not in existing_tables:
                missing_tables.append(table_name)

        if missing_tables:
            print(f"\n❌ الجداول المفقودة ({len(missing_tables)}):")
            for table in missing_tables:
                print(f"   ❌ {table}")
        else:
            print("\n✅ جميع الجداول المطلوبة موجودة")

        # فحص أعمدة كل جدول
        print(f"\n🔍 فحص أعمدة الجداول...")
        for table_name, expected_columns in required_tables.items():
            if table_name in existing_tables:
                c.execute(f"PRAGMA table_info({table_name})")
                actual_columns = [col[1] for col in c.fetchall()]

                missing_columns = [col for col in expected_columns if col not in actual_columns]
                if missing_columns:
                    print(f"   ⚠️ {table_name} - أعمدة مفقودة: {missing_columns}")
                else:
                    print(f"   ✅ {table_name} - جميع الأعمدة موجودة")

        conn.close()
        return len(missing_tables) == 0

    except Exception as e:
        print(f"❌ خطأ في فحص الجداول: {e}")
        return False

def create_missing_tables():
    """إنشاء الجداول المفقودة"""

    print("\n🔧 إنشاء الجداول المفقودة...")

    try:
        conn = sqlite3.connect('database.db')
        c = conn.cursor()

        # إنشاء جدول users
        c.execute('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            company_code TEXT NOT NULL,
            password TEXT NOT NULL,
            is_admin BOOLEAN DEFAULT FALSE,
            created_date TEXT DEFAULT CURRENT_TIMESTAMP
        )''')

        # إنشاء جدول data_entries
        c.execute('''CREATE TABLE IF NOT EXISTS data_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_name TEXT NOT NULL,
            employee_code TEXT NOT NULL,
            branch TEXT NOT NULL,
            shop_code TEXT,
            model TEXT NOT NULL,
            display_type TEXT NOT NULL,
            selected_materials TEXT,
            unselected_materials TEXT,
            images TEXT,
            comment TEXT,
            date TEXT NOT NULL
        )''')

        # إنشاء جدول branches
        c.execute('''CREATE TABLE IF NOT EXISTS branches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            branch_name TEXT NOT NULL,
            shop_code TEXT NOT NULL,
            employee_code TEXT NOT NULL,
            created_date TEXT NOT NULL,
            UNIQUE(branch_name, employee_code),
            UNIQUE(shop_code, employee_code)
        )''')

        # إنشاء جدول categories
        c.execute('''CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_name TEXT NOT NULL UNIQUE,
            created_date TEXT NOT NULL
        )''')

        # إنشاء جدول models
        c.execute('''CREATE TABLE IF NOT EXISTS models (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            model_name TEXT NOT NULL,
            category_name TEXT NOT NULL,
            created_date TEXT NOT NULL,
            UNIQUE(model_name, category_name)
        )''')

        # إنشاء جدول display_types
        c.execute('''CREATE TABLE IF NOT EXISTS display_types (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            display_type_name TEXT NOT NULL,
            category_name TEXT NOT NULL,
            created_date TEXT NOT NULL,
            UNIQUE(display_type_name, category_name)
        )''')

        # إنشاء جدول pop_materials_db
        c.execute('''CREATE TABLE IF NOT EXISTS pop_materials_db (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            material_name TEXT NOT NULL,
            model_name TEXT NOT NULL,
            category_name TEXT NOT NULL,
            created_date TEXT NOT NULL,
            UNIQUE(material_name, model_name)
        )''')

        # إنشاء جدول user_branches
        c.execute('''CREATE TABLE IF NOT EXISTS user_branches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            branch_name TEXT NOT NULL,
            created_date TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
            UNIQUE(user_id, branch_name)
        )''')

        # إنشاء جدول model_images
        c.execute('''CREATE TABLE IF NOT EXISTS model_images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            model_name TEXT NOT NULL,
            category_name TEXT NOT NULL,
            image_url TEXT NOT NULL,
            created_date TEXT NOT NULL,
            UNIQUE(model_name, category_name)
        )''')

        # إنشاء جدول db_init_status
        c.execute('''CREATE TABLE IF NOT EXISTS db_init_status (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            component TEXT NOT NULL UNIQUE,
            initialized BOOLEAN DEFAULT FALSE,
            last_update TEXT NOT NULL
        )''')

        conn.commit()
        conn.close()

        print("✅ تم إنشاء جميع الجداول المطلوبة")
        return True

    except Exception as e:
        print(f"❌ خطأ في إنشاء الجداول: {e}")
        return False

def add_missing_columns():
    """إضافة الأعمدة المفقودة"""

    print("\n🔧 إضافة الأعمدة المفقودة...")

    try:
        conn = sqlite3.connect('database.db')
        c = conn.cursor()

        # إضافة عمود comment إلى data_entries
        try:
            c.execute('ALTER TABLE data_entries ADD COLUMN comment TEXT')
            print("✅ تم إضافة عمود comment إلى data_entries")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e).lower():
                print("✅ عمود comment موجود بالفعل في data_entries")
            else:
                print(f"⚠️ خطأ في إضافة عمود comment: {e}")

        # إضافة عمود created_date إلى users
        try:
            c.execute('ALTER TABLE users ADD COLUMN created_date TEXT DEFAULT CURRENT_TIMESTAMP')
            print("✅ تم إضافة عمود created_date إلى users")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e).lower():
                print("✅ عمود created_date موجود بالفعل في users")
            else:
                print(f"⚠️ خطأ في إضافة عمود created_date: {e}")

        conn.commit()
        conn.close()

        return True

    except Exception as e:
        print(f"❌ خطأ في إضافة الأعمدة: {e}")
        return False

def initialize_default_data():
    """إضافة البيانات الافتراضية"""

    print("\n🔧 إضافة البيانات الافتراضية...")

    try:
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # إضافة الفئات الافتراضية
        categories = ['OLED', 'Neo QLED', 'QLED', 'UHD', 'LTV', 'BESPOKE COMBO',
                     'BESPOKE Front', 'Front', 'TL', 'SBS', 'TMF', 'BMF', 'Local TMF']

        for category in categories:
            c.execute('INSERT OR IGNORE INTO categories (category_name, created_date) VALUES (?, ?)',
                     (category, current_time))

        # إضافة الموديلات الافتراضية
        models_data = [
            ('S95F', 'OLED'), ('S90F', 'OLED'), ('S85F', 'OLED'),
            ('QN90', 'Neo QLED'), ('QN85F', 'Neo QLED'), ('QN80F', 'Neo QLED'), ('QN70F', 'Neo QLED'),
            ('Q8F', 'QLED'), ('Q7F', 'QLED'),
            ('U8000', 'UHD'), ('100"/98"', 'UHD'),
            ('The Frame', 'LTV'),
            ('WD25DB8995', 'BESPOKE COMBO'), ('WD21D6400', 'BESPOKE COMBO'),
            ('WW11B1944DGB', 'BESPOKE Front'),
            ('WW11B1534D', 'Front'), ('WW90CGC', 'Front'), ('WW4040', 'Front'), ('WW4020', 'Front'),
            ('WA19CG6886', 'TL'), ('Local TL', 'TL'),
            ('RS70F', 'SBS'),
            ('Bespoke', 'TMF'), ('TMF Non-Bespoke', 'TMF'), ('TMF', 'TMF'),
            ('(Bespoke, BMF)', 'BMF'), ('(Non-Bespoke, BMF)', 'BMF'),
            ('Local TMF', 'Local TMF')
        ]

        for model, category in models_data:
            c.execute('INSERT OR IGNORE INTO models (model_name, category_name, created_date) VALUES (?, ?, ?)',
                     (model, category, current_time))

        # إضافة أنواع العرض الافتراضية
        display_types_data = [
            ('Highlight Zone', 'OLED'), ('Fixtures', 'OLED'), ('Multi Brand Zone with Space', 'OLED'), ('SIS (Endcap)', 'OLED'),
            ('Highlight Zone', 'Neo QLED'), ('Fixtures', 'Neo QLED'), ('Multi Brand Zone with Space', 'Neo QLED'), ('SIS (Endcap)', 'Neo QLED'),
            ('Highlight Zone', 'QLED'), ('Fixtures', 'QLED'), ('Multi Brand Zone with Space', 'QLED'), ('SIS (Endcap)', 'QLED'),
            ('Highlight Zone', 'UHD'), ('Fixtures', 'UHD'), ('Multi Brand Zone with Space', 'UHD'), ('SIS (Endcap)', 'UHD'),
            ('Highlight Zone', 'LTV'), ('Fixtures', 'LTV'), ('Multi Brand Zone with Space', 'LTV'), ('SIS (Endcap)', 'LTV'),
            ('POP Out', 'BESPOKE COMBO'), ('POP Inner', 'BESPOKE COMBO'), ('POP', 'BESPOKE COMBO'),
            ('POP Out', 'BESPOKE Front'), ('POP Inner', 'BESPOKE Front'), ('POP', 'BESPOKE Front'),
            ('POP Out', 'Front'), ('POP Inner', 'Front'), ('POP', 'Front'),
            ('POP Out', 'TL'), ('POP Inner', 'TL'), ('POP', 'TL'),
            ('POP Out', 'SBS'), ('POP Inner', 'SBS'), ('POP', 'SBS'),
            ('POP Out', 'TMF'), ('POP Inner', 'TMF'), ('POP', 'TMF'),
            ('POP Out', 'BMF'), ('POP Inner', 'BMF'), ('POP', 'BMF'),
            ('POP Out', 'Local TMF'), ('POP Inner', 'Local TMF'), ('POP', 'Local TMF')
        ]

        for display_type, category in display_types_data:
            c.execute('INSERT OR IGNORE INTO display_types (display_type_name, category_name, created_date) VALUES (?, ?, ?)',
                     (display_type, category, current_time))

        # إضافة مواد POP الافتراضية (عينة)
        pop_materials_sample = [
            ('AI topper', 'S95F', 'OLED'),
            ('OLED Topper', 'S95F', 'OLED'),
            ('Glare Free', 'S95F', 'OLED'),
            ('AI topper', 'QN90', 'Neo QLED'),
            ('Lockup Topper', 'QN90', 'Neo QLED'),
            ('Screen POP', 'QN90', 'Neo QLED')
        ]

        for material, model, category in pop_materials_sample:
            c.execute('INSERT OR IGNORE INTO pop_materials_db (material_name, model_name, category_name, created_date) VALUES (?, ?, ?, ?)',
                     (material, model, category, current_time))

        conn.commit()
        conn.close()

        print("✅ تم إضافة البيانات الافتراضية")
        return True

    except Exception as e:
        print(f"❌ خطأ في إضافة البيانات الافتراضية: {e}")
        return False

def test_data_insertion():
    """اختبار إدراج البيانات"""

    print("\n🧪 اختبار إدراج البيانات...")

    try:
        conn = sqlite3.connect('database.db')
        c = conn.cursor()

        # بيانات تجريبية
        test_data = {
            'employee_name': 'Test User PythonAnywhere',
            'employee_code': 'PA_TEST001',
            'branch': 'Test Branch PA',
            'shop_code': 'PA001',
            'model': 'OLED - S95F',
            'display_type': 'Highlight Zone',
            'selected_materials': 'AI topper,OLED Topper',
            'unselected_materials': 'Glare Free',
            'images': '',
            'comment': 'Test comment from PythonAnywhere fix',
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        # محاولة الإدراج
        c.execute('''INSERT INTO data_entries
                    (employee_name, employee_code, branch, shop_code, model, display_type,
                     selected_materials, unselected_materials, images, comment, date)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                 (test_data['employee_name'], test_data['employee_code'],
                  test_data['branch'], test_data['shop_code'], test_data['model'],
                  test_data['display_type'], test_data['selected_materials'],
                  test_data['unselected_materials'], test_data['images'],
                  test_data['comment'], test_data['date']))

        conn.commit()

        # التحقق من الإدراج
        c.execute("SELECT * FROM data_entries WHERE employee_name = ? ORDER BY id DESC LIMIT 1",
                 (test_data['employee_name'],))
        result = c.fetchone()

        if result:
            print("✅ تم إدراج البيانات التجريبية بنجاح")
            print(f"   ID: {result[0]}")
            print(f"   Model: {result[5]}")
            print(f"   Comment: {result[10] if len(result) > 10 else 'N/A'}")

            # حذف البيانات التجريبية
            c.execute("DELETE FROM data_entries WHERE id = ?", (result[0],))
            conn.commit()
            print("🗑️ تم حذف البيانات التجريبية")
        else:
            print("❌ فشل في إدراج البيانات التجريبية")

        conn.close()
        return True

    except Exception as e:
        print(f"❌ خطأ في اختبار الإدراج: {e}")
        return False

def main():
    """الدالة الرئيسية"""

    print("🚀 إصلاح شامل لقاعدة البيانات على PythonAnywhere")
    print("=" * 60)

    # التحقق من وجود قاعدة البيانات
    if not check_database_exists():
        print("❌ لا يمكن المتابعة بدون ملف قاعدة البيانات")
        return False

    # فحص الجداول
    tables_ok = check_all_tables()

    # إنشاء الجداول المفقودة
    if not create_missing_tables():
        return False

    # إضافة الأعمدة المفقودة
    if not add_missing_columns():
        return False

    # إضافة البيانات الافتراضية
    if not initialize_default_data():
        return False

    # اختبار إدراج البيانات
    if not test_data_insertion():
        return False

    # فحص نهائي
    print("\n🔍 فحص نهائي...")
    check_all_tables()

    print("\n" + "=" * 60)
    print("🎉 تم إصلاح قاعدة البيانات بنجاح!")

    print("\n📋 الخطوات التالية:")
    print("1. أعد تشغيل التطبيق على PythonAnywhere")
    print("2. جرب حفظ البيانات مرة أخرى")
    print("3. إذا استمرت المشكلة، تحقق من error logs")

    return True

if __name__ == '__main__':
    main()