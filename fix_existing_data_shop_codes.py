#!/usr/bin/env python3
"""
إصلاح البيانات الموجودة - إضافة shop codes
"""

import sqlite3
from datetime import datetime

def fix_existing_shop_codes():
    """إصلاح shop codes للبيانات الموجودة"""
    print("🔧 Fixing existing data - Adding shop codes")
    print("=" * 50)
    
    try:
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        
        # جلب البيانات التي لا تحتوي على shop_code
        c.execute("""SELECT id, employee_name, branch, employee_code 
                    FROM data_entries 
                    WHERE shop_code IS NULL OR shop_code = ''""")
        
        entries_to_fix = c.fetchall()
        
        if not entries_to_fix:
            print("✅ All entries already have shop codes!")
            return True
        
        print(f"📊 Found {len(entries_to_fix)} entries without shop codes")
        
        # إنشاء shop codes تلقائياً بناءً على البيانات الموجودة
        fixed_count = 0
        
        for entry_id, emp_name, branch, emp_code in entries_to_fix:
            # إنشاء shop code بناءً على اسم الفرع
            if branch:
                # تحويل اسم الفرع إلى shop code
                shop_code = generate_shop_code(branch, emp_code)
                
                # تحديث الإدخال
                c.execute("""UPDATE data_entries 
                            SET shop_code = ? 
                            WHERE id = ?""", (shop_code, entry_id))
                
                print(f"  ✅ Fixed entry {entry_id}: {emp_name} | {branch} -> {shop_code}")
                fixed_count += 1
        
        # حفظ التغييرات
        conn.commit()
        
        # إضافة الفروع إلى جدول branches إذا لم تكن موجودة
        print(f"\n🏪 Adding branches to branches table...")
        
        c.execute("""SELECT DISTINCT branch, shop_code, employee_code 
                    FROM data_entries 
                    WHERE shop_code IS NOT NULL AND shop_code != ''""")
        
        unique_branches = c.fetchall()
        
        for branch_name, shop_code, emp_code in unique_branches:
            try:
                c.execute("""INSERT OR IGNORE INTO branches 
                            (branch_name, shop_code, employee_code, created_date) 
                            VALUES (?, ?, ?, ?)""",
                         (branch_name, shop_code, emp_code, 
                          datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
                print(f"  ✅ Added branch: {branch_name} ({shop_code})")
            except:
                pass  # Branch already exists
        
        conn.commit()
        conn.close()
        
        print(f"\n🎉 Successfully fixed {fixed_count} entries!")
        return True
        
    except Exception as e:
        print(f"❌ Error fixing shop codes: {e}")
        return False

def generate_shop_code(branch_name, employee_code):
    """إنشاء shop code من اسم الفرع"""
    # تنظيف اسم الفرع
    clean_branch = branch_name.strip().upper()
    
    # إنشاء كود بناءً على أول 3 أحرف من الفرع + رقم
    if len(clean_branch) >= 3:
        prefix = clean_branch[:3]
    else:
        prefix = clean_branch.ljust(3, 'X')
    
    # إضافة رقم بناءً على كود الموظف أو رقم عشوائي
    try:
        emp_num = ''.join(filter(str.isdigit, employee_code))
        if emp_num:
            suffix = emp_num[-3:].zfill(3)
        else:
            suffix = "001"
    except:
        suffix = "001"
    
    return f"{prefix}{suffix}"

def verify_fix():
    """التحقق من نجاح الإصلاح"""
    print(f"\n🔍 Verifying fix...")
    
    try:
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        
        # إحصائيات بعد الإصلاح
        c.execute("""SELECT COUNT(*) FROM data_entries 
                    WHERE shop_code IS NOT NULL AND shop_code != ''""")
        fixed_count = c.fetchone()[0]
        
        c.execute("SELECT COUNT(*) FROM data_entries")
        total_count = c.fetchone()[0]
        
        print(f"📊 Entries with shop_code: {fixed_count}/{total_count}")
        
        # عرض البيانات المحدثة
        c.execute("""SELECT employee_name, branch, shop_code 
                    FROM data_entries 
                    ORDER BY id DESC LIMIT 5""")
        
        recent = c.fetchall()
        print(f"📋 Recent entries after fix:")
        for i, (name, branch, shop_code) in enumerate(recent, 1):
            print(f"  {i}. {name} | {branch} | {shop_code}")
        
        conn.close()
        
        if fixed_count == total_count:
            print(f"✅ All entries now have shop codes!")
            return True
        else:
            print(f"⚠️ Some entries still missing shop codes")
            return False
            
    except Exception as e:
        print(f"❌ Error verifying fix: {e}")
        return False

def main():
    """الدالة الرئيسية"""
    print("🏪 Shop Code Fix for Existing Data")
    print("=" * 50)
    
    print("This script will:")
    print("1. Find all entries without shop codes")
    print("2. Generate shop codes based on branch names")
    print("3. Update the entries")
    print("4. Add branches to branches table")
    
    proceed = input(f"\n❓ Proceed with fixing shop codes? (y/n): ")
    
    if proceed.lower() in ['y', 'yes']:
        if fix_existing_shop_codes():
            verify_fix()
            
            print(f"\n🎯 Next Steps:")
            print("1. 🔄 Reload your PythonAnywhere web app")
            print("2. 🧹 Clear browser cache (Ctrl+F5)")
            print("3. 🌐 Check admin dashboard - shop codes should now appear!")
            print("4. ✅ Test with new data entry to ensure it works")
        else:
            print(f"\n❌ Fix failed - check error messages above")
    else:
        print(f"\n⏭️ Skipped fixing shop codes")
        print("💡 Alternative: Add new data entries with shop codes")

if __name__ == "__main__":
    main()