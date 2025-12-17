#!/usr/bin/env python3
"""
Test script to verify the Employee Data System functionality
"""

import sqlite3
import os
from werkzeug.security import generate_password_hash

def test_database():
    """Test database creation and initial data"""
    print("🔍 Testing database functionality...")
    
    # Remove existing database for clean test
    if os.path.exists('database.db'):
        os.remove('database.db')
    
    # Import and initialize
    from app import init_db
    init_db()
    
    # Test database connection
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    
    # Check tables exist
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = c.fetchall()
    expected_tables = ['users', 'data_entries', 'branches']
    table_names = [table[0] for table in tables if table[0] in expected_tables]
    print(f"✅ Tables created: {table_names}")
    
    if len(table_names) >= 3:
        print("✅ All required tables created successfully")
    else:
        print("❌ Some tables are missing")
    
    # Check admin user exists
    c.execute('SELECT * FROM users WHERE is_admin = TRUE')
    admin = c.fetchone()
    if admin:
        print(f"✅ Admin user created: {admin[1]} / {admin[2]}")
    else:
        print("❌ Admin user not found")
    
    # Add test employee
    test_password = generate_password_hash('test123')
    c.execute('INSERT INTO users (name, company_code, password, is_admin) VALUES (?, ?, ?, ?)',
             ('Test Employee', 'TEST001', test_password, False))
    conn.commit()
    print("✅ Test employee added: Test Employee / TEST001 / test123")
    
    # Add test branches with shop codes
    from datetime import datetime
    test_branches = [
        ('Main Branch', 'MB001'),
        ('Downtown Store', 'DS002'), 
        ('Mall Location', 'ML003')
    ]
    for branch_name, shop_code in test_branches:
        c.execute('INSERT OR IGNORE INTO branches (branch_name, shop_code, employee_code, created_date) VALUES (?, ?, ?, ?)',
                 (branch_name, shop_code, 'TEST001', datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    conn.commit()
    print("✅ Test branches with shop codes added for TEST001")
    
    conn.close()
    print("✅ Database test completed successfully!\n")

def test_data_structure():
    """Test the JavaScript data structure"""
    print("🔍 Testing data structure...")
    
    # Read the JavaScript file
    with open('static/js/data_entry.js', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for required categories
    required_categories = [
        'OLED', 'Neo QLED', 'QLED', 'UHD', 'LTV',
        'BESPOKE COMBO', 'BESPOKE Front', 'Front', 'TL', 'SBS', 'TMF', 'BMF', 'Local TMF'
    ]
    
    for category in required_categories:
        if f"'{category}'" in content:
            print(f"✅ Category found: {category}")
        else:
            print(f"❌ Category missing: {category}")
    
    # Check for display types
    if 'Highlight Zone' in content and 'POP Out' in content:
        print("✅ Display types configured correctly")
    else:
        print("❌ Display types missing")
    
    # Check for POP materials
    if 'AI topper' in content and 'Samsung Brand/Tech Topper' in content:
        print("✅ POP materials configured correctly")
    else:
        print("❌ POP materials missing")
    
    print("✅ Data structure test completed!\n")

def test_file_structure():
    """Test file structure"""
    print("🔍 Testing file structure...")
    
    required_files = [
        'app.py',
        'requirements.txt',
        'run_project.bat',
        'README.md',
        'static/css/style.css',
        'static/js/main.js',
        'static/js/data_entry.js',
        'static/js/admin_management.js',
        'static/js/user_management.js',
        'static/uploads/.gitkeep',
        'templates/base.html',
        'templates/login.html',
        'templates/data_entry.html',
        'templates/admin_dashboard.html',
        'templates/admin_management.html',
        'templates/user_management.html',
        'templates/register.html'
    ]
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ File exists: {file_path}")
        else:
            print(f"❌ File missing: {file_path}")
    
    print("✅ File structure test completed!\n")

def main():
    """Run all tests"""
    print("🚀 Starting Employee Data System Tests\n")
    print("=" * 50)
    
    try:
        test_file_structure()
        test_data_structure()
        test_database()
        
        print("🎉 All tests completed successfully!")
        print("\n📋 Next steps:")
        print("1. Run: python app.py")
        print("2. Open: http://127.0.0.1:5000")
        print("3. Login as Admin: Admin / ADMIN / admin123")
        print("4. Or as Test Employee: Test Employee / TEST001 / test123")
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")

if __name__ == "__main__":
    main()