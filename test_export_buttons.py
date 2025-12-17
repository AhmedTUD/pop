#!/usr/bin/env python3
"""
اختبار سريع لأزرار التصدير
"""

import sqlite3
from datetime import datetime

def test_export_functions():
    """اختبار دوال التصدير مع بيانات حقيقية"""
    print("🧪 اختبار دوال التصدير مع بيانات حقيقية")
    print("=" * 50)
    
    try:
        # الاتصال بقاعدة البيانات
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        
        # الحصول على البيانات الحقيقية
        c.execute('''SELECT id, employee_name, employee_code, branch, shop_code, model, 
                            display_type, selected_materials, unselected_materials, images, date 
                     FROM data_entries ORDER BY date DESC LIMIT 5''')
        entries = c.fetchall()
        conn.close()
        
        print(f"📊 تم العثور على {len(entries)} إدخال في قاعدة البيانات")
        
        if not entries:
            print("⚠️ لا توجد بيانات في قاعدة البيانات")
            print("💡 أضف بعض البيانات أولاً من خلال التطبيق")
            return False
        
        # عرض عينة من البيانات
        print("\n📋 عينة من البيانات:")
        for i, entry in enumerate(entries[:2], 1):
            print(f"  {i}. {entry[1]} ({entry[2]}) - {entry[5]} - {entry[10]}")
        
        # اختبار التصدير المحسن
        print("\n🖼️ اختبار التصدير المحسن...")
        from excel_export_enhanced import export_enhanced_excel_with_cloudinary
        
        result = export_enhanced_excel_with_cloudinary(entries)
        
        if result['success']:
            if result['method'] == 'cloudinary':
                print(f"✅ تم التصدير إلى Cloudinary: {result['url']}")
            else:
                file_size = len(result['data']) / 1024  # KB
                print(f"✅ تم التصدير محلياً: {result['filename']} ({file_size:.1f} KB)")
            
            print(f"📝 الرسالة: {result['message']}")
            return True
        else:
            print(f"❌ فشل التصدير: {result['error']}")
            return False
            
    except Exception as e:
        print(f"❌ خطأ في الاختبار: {e}")
        return False

def main():
    """الدالة الرئيسية"""
    success = test_export_functions()
    
    if success:
        print("\n🎉 الاختبار نجح!")
        print("\n📋 التوجيهات:")
        print("1. شغل التطبيق: python app.py")
        print("2. اذهب إلى لوحة التحكم")
        print("3. اضغط على 'Export Enhanced Excel' (الزر الأخضر)")
        print("4. يجب أن يتم تحميل ملف Excel محسن مع الصور والتنسيق")
    else:
        print("\n❌ الاختبار فشل!")
        print("تأكد من وجود بيانات في قاعدة البيانات")

if __name__ == "__main__":
    main()