#!/usr/bin/env python3
"""
تحديث بنية قاعدة البيانات لتشمل جميع الجداول الجديدة
"""

import sqlite3
import os
from datetime import datetime

def update_database_structure():
    """تحديث بنية قاعدة البيانات"""
    
    print("🔧 تحديث بنية قاعدة البيانات...")
    
    try:
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        
        # 1. إضافة جدول model_images
        print("📋 إضافة جدول model_images...")
        c.execute('''CREATE TABLE IF NOT EXISTS model_images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            model_name TEXT NOT NULL,
            category_name TEXT NOT NULL,
            image_url TEXT NOT NULL,
            created_date TEXT NOT NULL,
            UNIQUE(model_name, category_name)
        )''')
        
        # 2. التأكد من وجود عمود comment في data_entries
        print("📋 التحقق من عمود comment...")
        try:
            c.execute('ALTER TABLE data_entries ADD COLUMN comment TEXT')
            print("✅ تم إضافة عمود comment")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e).lower():
                print("✅ عمود comment موجود بالفعل")
            else:
                print(f"⚠️ خطأ في إضافة عمود comment: {e}")
        
        # 3. التأكد من وجود جدول user_branches
        print("📋 التحقق من جدول user_branches...")
        c.execute('''CREATE TABLE IF NOT EXISTS user_branches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            branch_name TEXT NOT NULL,
            created_date TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
            UNIQUE(user_id, branch_name)
        )''')
        
        # 4. التأكد من وجود جدول db_init_status
        print("📋 التحقق من جدول db_init_status...")
        c.execute('''CREATE TABLE IF NOT EXISTS db_init_status (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            component TEXT NOT NULL UNIQUE,
            initialized BOOLEAN DEFAULT FALSE,
            last_update TEXT NOT NULL
        )''')
        
        # 5. التأكد من وجود عمود created_date في users
        print("📋 التحقق من عمود created_date في users...")
        try:
            c.execute('ALTER TABLE users ADD COLUMN created_date TEXT DEFAULT CURRENT_TIMESTAMP')
            print("✅ تم إضافة عمود created_date")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e).lower():
                print("✅ عمود created_date موجود بالفعل")
            else:
                print(f"⚠️ خطأ في إضافة عمود created_date: {e}")
        
        conn.commit()
        print("✅ تم تحديث بنية قاعدة البيانات بنجاح")
        
        return True
        
    except Exception as e:
        print(f"❌ خطأ في تحديث قاعدة البيانات: {e}")
        return False
        
    finally:
        if conn:
            conn.close()

def verify_database_structure():
    """التحقق من بنية قاعدة البيانات"""
    
    print("\n🔍 التحقق من بنية قاعدة البيانات...")
    
    try:
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        
        # فحص الجداول المطلوبة
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
        
        all_good = True
        
        for table_name, expected_columns in required_tables.items():
            # التحقق من وجود الجدول
            c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
            if not c.fetchone():
                print(f"❌ الجدول {table_name} غير موجود")
                all_good = False
                continue
            
            # التحقق من الأعمدة
            c.execute(f"PRAGMA table_info({table_name})")
            actual_columns = [col[1] for col in c.fetchall()]
            
            missing_columns = [col for col in expected_columns if col not in actual_columns]
            if missing_columns:
                print(f"⚠️ الجدول {table_name} - أعمدة مفقودة: {missing_columns}")
                all_good = False
            else:
                print(f"✅ الجدول {table_name} - جميع الأعمدة موجودة")
        
        if all_good:
            print("\n🎉 بنية قاعدة البيانات صحيحة ومكتملة!")
        else:
            print("\n⚠️ هناك مشاكل في بنية قاعدة البيانات")
        
        return all_good
        
    except Exception as e:
        print(f"❌ خطأ في فحص قاعدة البيانات: {e}")
        return False
        
    finally:
        if conn:
            conn.close()

def main():
    """الدالة الرئيسية"""
    
    print("🚀 تحديث بنية قاعدة البيانات")
    print("=" * 50)
    
    # التحقق من وجود ملف قاعدة البيانات
    if not os.path.exists('database.db'):
        print("❌ ملف قاعدة البيانات غير موجود!")
        print("تأكد من تشغيل هذا الملف في نفس مجلد app.py")
        return False
    
    # تحديث بنية قاعدة البيانات
    if update_database_structure():
        # التحقق من البنية
        verify_database_structure()
        
        print("\n" + "=" * 50)
        print("🎉 تم تحديث قاعدة البيانات بنجاح!")
        print("\nيمكنك الآن:")
        print("1. إعادة تشغيل التطبيق")
        print("2. استخدام جميع الميزات الجديدة")
        print("3. رفع صور الموديلات")
        
        return True
    else:
        print("\n❌ فشل في تحديث قاعدة البيانات")
        return False

if __name__ == '__main__':
    main()