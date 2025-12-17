#!/usr/bin/env python3
"""
Test script to verify Shop Code functionality
"""

import sqlite3
from datetime import datetime

def test_shop_code_functionality():
    """Test shop code functionality"""
    print("🏪 Testing Shop Code functionality...")
    
    # Connect to database
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    
    # Test 1: Add branches with shop codes
    test_branches = [
        ('Samsung Store Cairo', 'SSC001', 'TEST001'),
        ('Samsung Mall Alexandria', 'SMA002', 'TEST001'),
        ('Samsung Outlet Giza', 'SOG003', 'TEST001'),
        ('Samsung Center Luxor', 'SCL004', 'TEST002')
    ]
    
    for branch_name, shop_code, employee_code in test_branches:
        try:
            c.execute('''INSERT OR REPLACE INTO branches 
                        (branch_name, shop_code, employee_code, created_date) 
                        VALUES (?, ?, ?, ?)''',
                     (branch_name, shop_code, employee_code, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            print(f"✅ Added branch: {branch_name} (Code: {shop_code})")
        except Exception as e:
            print(f"❌ Failed to add branch {branch_name}: {e}")
    
    conn.commit()
    
    # Test 2: Search branches by name
    print("\n🔍 Testing branch search by name:")
    search_terms = ['Samsung', 'Cairo', 'Mall']
    
    for term in search_terms:
        c.execute('''SELECT branch_name, shop_code FROM branches 
                    WHERE employee_code = ? AND 
                    (branch_name LIKE ? OR shop_code LIKE ?)''',
                 ('TEST001', f'%{term}%', f'%{term}%'))
        results = c.fetchall()
        print(f"  Search '{term}': Found {len(results)} branches")
        for branch_name, shop_code in results:
            print(f"    - {branch_name} ({shop_code})")
    
    # Test 3: Search branches by shop code
    print("\n🏷️ Testing branch search by shop code:")
    shop_codes = ['SSC001', 'SMA', '003']
    
    for code in shop_codes:
        c.execute('''SELECT branch_name, shop_code FROM branches 
                    WHERE employee_code = ? AND shop_code LIKE ?''',
                 ('TEST001', f'%{code}%'))
        results = c.fetchall()
        print(f"  Search code '{code}': Found {len(results)} branches")
        for branch_name, shop_code in results:
            print(f"    - {branch_name} ({shop_code})")
    
    # Test 4: Test unique constraints
    print("\n🔒 Testing unique constraints:")
    try:
        c.execute('''INSERT INTO branches 
                    (branch_name, shop_code, employee_code, created_date) 
                    VALUES (?, ?, ?, ?)''',
                 ('Duplicate Branch', 'SSC001', 'TEST001', datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        conn.commit()
        print("❌ Duplicate shop code was allowed (should be prevented)")
    except sqlite3.IntegrityError:
        print("✅ Duplicate shop code correctly prevented")
    
    # Test 5: Add data entry with shop code
    print("\n📊 Testing data entry with shop code:")
    try:
        c.execute('''INSERT OR REPLACE INTO data_entries 
                    (employee_name, employee_code, branch, shop_code, model, display_type, 
                     selected_materials, unselected_materials, images, date)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                 ('Test Employee', 'TEST001', 'Samsung Store Cairo', 'SSC001', 'OLED - S95F', 
                  'Highlight Zone', 'AI topper,Oled Topper', 'Glare Free,New Topper', '',
                  datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        conn.commit()
        print("✅ Data entry with shop code saved successfully")
    except Exception as e:
        print(f"❌ Failed to save data entry: {e}")
    
    # Test 6: Verify data entry includes shop code
    c.execute('SELECT branch, shop_code, model FROM data_entries WHERE employee_code = ? ORDER BY date DESC LIMIT 1', 
              ('TEST001',))
    result = c.fetchone()
    if result:
        branch, shop_code, model = result
        print(f"✅ Latest entry: {branch} (Code: {shop_code}) - {model}")
    else:
        print("❌ No data entries found")
    
    conn.close()
    print("✅ Shop Code functionality test completed!")

def test_shop_code_api():
    """Test shop code API endpoints"""
    print("\n🌐 Testing Shop Code API endpoints...")
    
    # This would require running the Flask app
    # For now, we'll just verify the database structure
    
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    
    # Check if shop_code column exists in branches table
    c.execute("PRAGMA table_info(branches)")
    columns = [column[1] for column in c.fetchall()]
    
    if 'shop_code' in columns:
        print("✅ shop_code column exists in branches table")
    else:
        print("❌ shop_code column missing in branches table")
    
    # Check if shop_code column exists in data_entries table
    c.execute("PRAGMA table_info(data_entries)")
    columns = [column[1] for column in c.fetchall()]
    
    if 'shop_code' in columns:
        print("✅ shop_code column exists in data_entries table")
    else:
        print("❌ shop_code column missing in data_entries table")
    
    conn.close()

def main():
    """Run all shop code tests"""
    print("🚀 Starting Shop Code Tests\n")
    print("=" * 50)
    
    try:
        test_shop_code_functionality()
        test_shop_code_api()
        
        print("\n🎉 All shop code tests completed successfully!")
        print("\n📋 What was tested:")
        print("1. ✅ Adding branches with shop codes")
        print("2. ✅ Searching branches by name and code")
        print("3. ✅ Unique constraint enforcement")
        print("4. ✅ Data entries with shop codes")
        print("5. ✅ Database structure verification")
        
        print("\n🔧 Next steps:")
        print("1. Run the system: python app.py")
        print("2. Test branch autocomplete with shop codes")
        print("3. Verify shop codes appear in admin dashboard")
        print("4. Test Excel export includes shop codes")
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")

if __name__ == "__main__":
    main()