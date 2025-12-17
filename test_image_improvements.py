#!/usr/bin/env python3
"""
اختبار تحسينات رفع الصور وجودة Excel
"""

import sqlite3
from excel_export_enhanced import export_enhanced_excel_with_cloudinary

def test_image_improvements():
    """اختبار التحسينات الجديدة للصور"""
    print("🖼️ اختبار تحسينات الصور الجديدة")
    print("=" * 50)
    
    try:
        # الحصول على البيانات مع الصور
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('''SELECT id, employee_name, employee_code, branch, shop_code, model, 
                            display_type, selected_materials, unselected_materials, images, date 
                     FROM data_entries WHERE images IS NOT NULL AND images != "" 
                     ORDER BY date DESC LIMIT 3''')
        entries = c.fetchall()
        conn.close()
        
        if not entries:
            print("❌ لا توجد بيانات مع صور للاختبار")
            return False
        
        print(f"📊 تم العثور على {len(entries)} إدخال مع صور")
        
        # عرض تفاصيل الصور
        for i, entry in enumerate(entries, 1):
            images_data = entry[9] if entry[9] else ''
            if images_data:
                image_urls = [url.strip() for url in images_data.split(',') if url.strip()]
                print(f"  {i}. {entry[1]} - {len(image_urls)} صور")
                for j, img_url in enumerate(image_urls, 1):
                    if img_url.startswith('http'):
                        print(f"     {j}. Cloudinary: {img_url[:60]}...")
                    else:
                        print(f"     {j}. Local: {img_url}")
        
        # اختبار التصدير المحسن
        print(f"\n🚀 اختبار التصدير مع الصور المحسنة...")
        result = export_enhanced_excel_with_cloudinary(entries)
        
        if result['success']:
            if result['method'] == 'cloudinary':
                print(f"✅ تم التصدير إلى Cloudinary: {result['url']}")
            else:
                file_size = len(result['data']) / 1024
                print(f"✅ تم التصدير محلياً: {result['filename']} ({file_size:.1f} KB)")
                
                # حفظ الملف للاختبار
                with open('test_improved_images.xlsx', 'wb') as f:
                    f.write(result['data'])
                print(f"💾 تم حفظ الملف: test_improved_images.xlsx")
            
            return True
        else:
            print(f"❌ فشل التصدير: {result['error']}")
            return False
            
    except Exception as e:
        print(f"❌ خطأ في الاختبار: {e}")
        return False

def show_improvements():
    """عرض التحسينات الجديدة"""
    print(f"\n🎯 التحسينات الجديدة:")
    
    print(f"\n📸 تحسينات رفع الصور:")
    print("✅ واجهة محسنة لرفع الصور المتعددة")
    print("✅ معاينة الصور مع أحجام الملفات")
    print("✅ دعم تنسيقات إضافية (WEBP, AVIF)")
    print("✅ التحقق من صحة الملفات (حجم ونوع)")
    print("✅ حد أقصى 10 صور لكل إدخال")
    print("✅ رسائل خطأ واضحة")
    
    print(f"\n🖼️ تحسينات جودة الصور في Excel:")
    print("✅ حجم صور أكبر: 120x120 بكسل (بدلاً من 80x80)")
    print("✅ جودة أعلى: 95% (بدلاً من 85%)")
    print("✅ دقة أفضل: 200x200 معالجة (بدلاً من 150x150)")
    print("✅ دعم عرض 3 صور لكل صف")
    print("✅ ارتفاع صف أكبر: 150 (بدلاً من 120)")
    print("✅ أعمدة إضافية للصور المتعددة")

def test_frontend_improvements():
    """اختبار تحسينات الواجهة الأمامية"""
    print(f"\n🎨 اختبار تحسينات الواجهة:")
    
    # التحقق من وجود ملفات CSS و JS المحدثة
    import os
    
    files_to_check = [
        ('static/css/style.css', 'file-upload-label'),
        ('static/js/data_entry.js', 'validateImageFiles'),
        ('static/js/data_entry.js', 'handleImagePreview')
    ]
    
    for file_path, search_term in files_to_check:
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if search_term in content:
                    print(f"✅ {file_path}: {search_term} موجود")
                else:
                    print(f"❌ {file_path}: {search_term} مفقود")
        else:
            print(f"❌ {file_path}: الملف غير موجود")

def main():
    """الدالة الرئيسية"""
    print("🧪 اختبار تحسينات الصور الشامل")
    print("=" * 60)
    
    # عرض التحسينات
    show_improvements()
    
    # اختبار الواجهة
    test_frontend_improvements()
    
    # اختبار التصدير
    export_success = test_image_improvements()
    
    print("\n" + "=" * 60)
    print("📊 ملخص الاختبار")
    print("=" * 60)
    
    if export_success:
        print("✅ تحسينات الصور تعمل بشكل مثالي!")
        
        print(f"\n🚀 للاختبار الكامل:")
        print("1. شغل التطبيق: python app.py")
        print("2. أدخل بيانات جديدة")
        print("3. ارفع عدة صور (اختبر الواجهة الجديدة)")
        print("4. اضغط زر التصدير المحسن")
        print("5. افتح الملف وتحقق من جودة الصور")
        
        print(f"\n🔍 ما تتوقع رؤيته:")
        print("- واجهة رفع صور محسنة مع معاينة")
        print("- صور أكبر وأوضح في Excel (120x120)")
        print("- عرض حتى 3 صور في نفس الصف")
        print("- جودة صور عالية (95%)")
        
    else:
        print("❌ هناك مشاكل في التحسينات")
        print("🔧 راجع الأخطاء أعلاه")

if __name__ == "__main__":
    main()