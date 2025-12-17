#!/usr/bin/env python3
"""
فحص سريع لـ PythonAnywhere - مشكلة Shop Code
"""

import sqlite3
import os
from datetime import datetime

def quick_check():
    """فحص سريع للمشكلة"""
    print("🔍 PythonAnywhere Quick Check - Shop Code Issue")
    print("=" * 60)
    
    # 1. فحص الملفات المهمة
    print("📁 Critical Files Check:")
    critical_files = {
        'app.py': 'Main application file',
        'templates/admin_dashboard.html': 'Admin dashboard template',
        'static/js/data_entry.js': 'Data entry JavaScript',
        'database.db': 'SQLite database'
    }
    
    files_ok = True
    for file, desc in critical_files.items():
        if os.path.exists(file):
            mtime = os.path.getmtime(file)
            mod_time = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')
            print(f"  ✅ {file} - {desc} (Modified: {mod_time})")
        else:
            print(f"  ❌ {file} - {desc} - MISSING!")
            files_ok = False
    
    # 2. فحص قاعدة البيانات
    print(f"\n🗄️ Database Check:")
    try:
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        
        # فحص بنية الجدول
        c.execute("PRAGMA table_info(data_entries)")
        columns = [col[1] for col in c.fetchall()]
        
        if 'shop_code' in columns:
            print("  ✅ shop_code column exists")
        else:
            print("  ❌ shop_code column MISSING - This is the problem!")
            return False
        
        # فحص البيانات
        c.execute("""SELECT COUNT(*) FROM data_entries 
                    WHERE shop_code IS NOT NULL AND shop_code != ''""")
        valid_entries = c.fetchone()[0]
        
        c.execute("SELECT COUNT(*) FROM data_entries")
        total_entries = c.fetchone()[0]
        
        print(f"  📊 Total entries: {total_entries}")
        print(f"  📊 Entries with shop_code: {valid_entries}")
        
        if total_entries == 0:
            print("  ⚠️ No data entries found - database might be empty")
        
        # عرض آخر 3 إدخالات
        c.execute("""SELECT employee_name, branch, shop_code, date 
                    FROM data_entries 
                    ORDER BY date DESC LIMIT 3""")
        recent = c.fetchall()
        
        print("  📋 Recent entries:")
        for i, entry in enumerate(recent, 1):
            name, branch, shop_code, date = entry
            shop_display = shop_code if shop_code else "NULL/EMPTY"
            print(f"    {i}. {name} | {branch} | {shop_display} | {date}")
        
        conn.close()
        
    except Exception as e:
        print(f"  ❌ Database error: {e}")
        return False
    
    # 3. فحص محتوى الملفات المهمة
    print(f"\n📄 File Content Check:")
    
    # فحص admin_dashboard.html
    try:
        with open('templates/admin_dashboard.html', 'r', encoding='utf-8') as f:
            content = f.read()
            if 'entry[4]' in content and 'Shop Code' in content:
                print("  ✅ admin_dashboard.html has correct shop_code display logic")
            else:
                print("  ❌ admin_dashboard.html missing shop_code display logic")
    except:
        print("  ❌ Cannot read admin_dashboard.html")
    
    # فحص data_entry.js
    try:
        with open('static/js/data_entry.js', 'r', encoding='utf-8') as f:
            content = f.read()
            if 'shop_code' in content and 'selectBranch' in content:
                print("  ✅ data_entry.js has shop_code functionality")
            else:
                print("  ❌ data_entry.js missing shop_code functionality")
    except:
        print("  ❌ Cannot read data_entry.js")
    
    # 4. التوصيات
    print(f"\n💡 Recommendations:")
    
    if not files_ok:
        print("  🔥 URGENT: Upload missing files to PythonAnywhere")
        print("     - Use Files tab to upload missing files")
        print("     - Make sure to upload to correct directories")
    
    if total_entries == 0:
        print("  📊 Database appears empty - upload your local database.db")
    elif valid_entries == 0:
        print("  🏪 No entries have shop_code - check data entry process")
    
    print("  🔄 Always do after uploading files:")
    print("     1. Go to Web tab in PythonAnywhere")
    print("     2. Click 'Reload' button")
    print("     3. Clear browser cache (Ctrl+F5)")
    print("     4. Test in incognito mode")
    
    return True

def create_test_entry():
    """إنشاء إدخال تجريبي للاختبار"""
    print(f"\n➕ Creating test entry with shop_code...")
    
    try:
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        
        test_data = (
            'PythonAnywhere Test User',
            'PA_TEST',
            'PythonAnywhere Test Branch',
            'PA_SHOP_123',
            'Test Model',
            'Test Display',
            'Test Materials',
            'Missing Materials',
            '',
            datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )
        
        c.execute("""INSERT INTO data_entries 
                    (employee_name, employee_code, branch, shop_code, model, display_type, 
                     selected_materials, unselected_materials, images, date)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", test_data)
        
        conn.commit()
        
        # التحقق من الحفظ
        c.execute("""SELECT employee_name, branch, shop_code 
                    FROM data_entries 
                    WHERE employee_code = 'PA_TEST'""")
        result = c.fetchone()
        
        if result:
            print(f"  ✅ Test entry created: {result[0]} | {result[1]} | {result[2]}")
            print("  🌐 Now check your admin dashboard - shop_code should show 'PA_SHOP_123'")
            
            # حذف الإدخال التجريبي
            choice = input("\n🗑️ Delete test entry? (y/n): ")
            if choice.lower() in ['y', 'yes']:
                c.execute("DELETE FROM data_entries WHERE employee_code = 'PA_TEST'")
                conn.commit()
                print("  ✅ Test entry deleted")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"  ❌ Error creating test entry: {e}")
        return False

def main():
    """الدالة الرئيسية"""
    if quick_check():
        print(f"\n" + "="*60)
        create_test = input("🧪 Create test entry to verify shop_code display? (y/n): ")
        if create_test.lower() in ['y', 'yes']:
            create_test_entry()
    
    print(f"\n📋 Summary:")
    print("If shop_code still shows N/A after this check:")
    print("1. 🔄 Reload your PythonAnywhere web app")
    print("2. 🧹 Clear browser cache completely")
    print("3. 🕵️ Test in incognito/private browsing mode")
    print("4. 📊 Check browser developer tools for JavaScript errors")

if __name__ == "__main__":
    main()