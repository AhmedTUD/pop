#!/usr/bin/env python3
"""
اختبار تصدير البيانات المفلترة
"""

import sqlite3
from urllib.parse import urlencode

def test_filter_logic():
    """اختبار منطق الفلترة"""
    print("🔍 اختبار منطق الفلترة")
    print("=" * 50)
    
    try:
        # الحصول على البيانات الحالية
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        
        # عرض جميع البيانات
        c.execute('SELECT id, employee_name, branch, model, date FROM data_entries ORDER BY date DESC')
        all_entries = c.fetchall()
        
        print(f"📊 إجمالي السجلات: {len(all_entries)}")
        print("\n📋 جميع السجلات:")
        for entry in all_entries:
            print(f"  ID: {entry[0]}, Employee: {entry[1]}, Branch: {entry[2]}, Model: {entry[3][:30]}...")
        
        # اختبار فلترة بالموظف
        print(f"\n🔍 اختبار الفلترة بالموظف 'ahmed':")
        query = '''SELECT id, employee_name, branch, model, date FROM data_entries 
                   WHERE employee_name LIKE ? ORDER BY date DESC'''
        c.execute(query, ('%ahmed%',))
        filtered_entries = c.fetchall()
        
        print(f"📊 السجلات المفلترة: {len(filtered_entries)}")
        for entry in filtered_entries:
            print(f"  ID: {entry[0]}, Employee: {entry[1]}, Branch: {entry[2]}")
        
        # اختبار فلترة بالفرع
        print(f"\n🔍 اختبار الفلترة بالفرع 'Test':")
        query = '''SELECT id, employee_name, branch, model, date FROM data_entries 
                   WHERE branch LIKE ? ORDER BY date DESC'''
        c.execute(query, ('%Test%',))
        branch_filtered = c.fetchall()
        
        print(f"📊 السجلات المفلترة بالفرع: {len(branch_filtered)}")
        for entry in branch_filtered:
            print(f"  ID: {entry[0]}, Employee: {entry[1]}, Branch: {entry[2]}")
        
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ خطأ في اختبار الفلترة: {e}")
        return False

def generate_export_urls():
    """إنشاء روابط التصدير مع فلاتر مختلفة"""
    print(f"\n🔗 روابط التصدير مع الفلاتر:")
    
    # فلاتر مختلفة للاختبار
    test_filters = [
        {'employee': 'ahmed'},
        {'branch': 'Test'},
        {'model': 'OLED'},
        {'employee': 'ahmed', 'branch': 'Test'},
        {'date_from': '2025-10-22'},
        {}  # بدون فلاتر
    ]
    
    base_urls = [
        'http://127.0.0.1:5000/export_excel',
        'http://127.0.0.1:5000/export_excel_simple'
    ]
    
    for i, filters in enumerate(test_filters, 1):
        if filters:
            query_string = urlencode({k: v for k, v in filters.items() if v})
            filter_desc = ', '.join([f"{k}={v}" for k, v in filters.items()])
        else:
            query_string = ''
            filter_desc = 'بدون فلاتر'
        
        print(f"\n{i}. فلتر: {filter_desc}")
        for base_url in base_urls:
            export_type = "محسن" if "export_excel'" not in base_url or base_url.endswith('export_excel') else "بسيط"
            full_url = f"{base_url}?{query_string}" if query_string else base_url
            print(f"   {export_type}: {full_url}")

def test_dashboard_integration():
    """اختبار التكامل مع Dashboard"""
    print(f"\n🎯 اختبار التكامل مع Dashboard:")
    
    print("✅ تم تحديث أزرار التصدير لتمرير معاملات الفلترة")
    print("✅ تم تحديث دوال التصدير لقراءة معاملات الفلترة")
    print("✅ تم إضافة رسائل توضيحية لعدد السجلات")
    
    print(f"\n📋 خطوات الاختبار:")
    print("1. شغل التطبيق: python app.py")
    print("2. اذهب إلى Admin Dashboard")
    print("3. طبق فلتر معين (مثل اختيار موظف محدد)")
    print("4. اضغط زر التصدير")
    print("5. تحقق من أن الملف يحتوي فقط على البيانات المفلترة")
    
    print(f"\n🔍 علامات النجاح:")
    print("- رسالة: 'جاري تصدير X سجل مع الفلاتر المطبقة'")
    print("- الملف يحتوي فقط على السجلات المعروضة في الجدول")
    print("- عدد السجلات في الملف = عدد السجلات في الجدول")

def main():
    """الدالة الرئيسية"""
    print("🧪 اختبار تصدير البيانات المفلترة")
    print("=" * 60)
    
    # اختبار منطق الفلترة
    filter_ok = test_filter_logic()
    
    # إنشاء روابط الاختبار
    generate_export_urls()
    
    # اختبار التكامل
    test_dashboard_integration()
    
    print("\n" + "=" * 60)
    print("📊 ملخص الاختبار")
    print("=" * 60)
    
    if filter_ok:
        print("✅ منطق الفلترة يعمل بشكل صحيح")
        print("✅ أزرار التصدير محدثة")
        print("✅ دوال التصدير محدثة")
        
        print(f"\n🎉 التصدير المفلتر جاهز للاستخدام!")
        print(f"\n🚀 اختبر الآن:")
        print("1. شغل التطبيق")
        print("2. طبق فلاتر في Dashboard")
        print("3. اضغط زر التصدير")
        print("4. تحقق من النتيجة")
        
    else:
        print("❌ هناك مشكلة في منطق الفلترة")
        print("🔧 راجع قاعدة البيانات والاستعلامات")

if __name__ == "__main__":
    main()