#!/usr/bin/env python3
"""
اختبار تصدير Excel المحسن مع الصور والتنسيق
"""

import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# تحميل متغيرات البيئة
load_dotenv()

def test_excel_export_functions():
    """اختبار دوال تصدير Excel"""
    print("🧪 اختبار دوال تصدير Excel المحسن")
    print("=" * 50)
    
    try:
        from excel_export_enhanced import (
            create_enhanced_excel_with_images,
            create_simple_excel_with_formatting,
            export_enhanced_excel_with_cloudinary
        )
        print("✅ تم استيراد دوال التصدير بنجاح")
    except ImportError as e:
        print(f"❌ خطأ في استيراد دوال التصدير: {e}")
        return False
    
    # بيانات تجريبية
    test_data = [
        (1, 'أحمد محمد', 'EMP001', 'فرع القاهرة', 'CAI001', 'Samsung OLED S95F', 
         'Highlight Zone', 'AI topper,OLED Topper', 'Glare Free', 
         'https://res.cloudinary.com/demo/image/upload/sample.jpg', 
         datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
        (2, 'فاطمة أحمد', 'EMP002', 'فرع الإسكندرية', 'ALX002', 'Samsung Neo QLED QN90', 
         'Fixtures', 'Neo Quantum Processor,Gaming Hub', 'Screen POP', 
         'https://res.cloudinary.com/demo/image/upload/sample2.jpg,https://res.cloudinary.com/demo/image/upload/sample3.jpg', 
         datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
        (3, 'محمد علي', 'EMP003', 'فرع الجيزة', 'GIZ003', 'Samsung QLED Q8F', 
         'Multi Brand Zone', 'QLED Topper,Smart Features', '', 
         '', 
         datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    ]
    
    print(f"\n📊 بيانات الاختبار: {len(test_data)} إدخال")
    
    # اختبار إنشاء Excel بسيط
    print("\n🔍 اختبار Excel البسيط...")
    try:
        filename_simple = f'test_simple_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
        simple_path = create_simple_excel_with_formatting(test_data, filename_simple)
        
        if simple_path and os.path.exists(simple_path):
            file_size = os.path.getsize(simple_path) / 1024  # KB
            print(f"✅ تم إنشاء Excel البسيط: {filename_simple} ({file_size:.1f} KB)")
            
            # حذف الملف التجريبي
            os.remove(simple_path)
        else:
            print("❌ فشل في إنشاء Excel البسيط")
            return False
    except Exception as e:
        print(f"❌ خطأ في Excel البسيط: {e}")
        return False
    
    # اختبار إنشاء Excel مع الصور
    print("\n🖼️ اختبار Excel مع الصور...")
    try:
        filename_enhanced = f'test_enhanced_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
        enhanced_path = create_enhanced_excel_with_images(test_data, filename_enhanced)
        
        if enhanced_path and os.path.exists(enhanced_path):
            file_size = os.path.getsize(enhanced_path) / 1024  # KB
            print(f"✅ تم إنشاء Excel المحسن: {filename_enhanced} ({file_size:.1f} KB)")
            
            # حذف الملف التجريبي
            os.remove(enhanced_path)
        else:
            print("❌ فشل في إنشاء Excel المحسن")
            return False
    except Exception as e:
        print(f"❌ خطأ في Excel المحسن: {e}")
        return False
    
    # اختبار التصدير مع Cloudinary
    print("\n☁️ اختبار التصدير مع Cloudinary...")
    try:
        from cloudinary_config import is_cloudinary_configured
        
        if is_cloudinary_configured():
            print("✅ Cloudinary مُعد بشكل صحيح")
            
            result = export_enhanced_excel_with_cloudinary(test_data)
            
            if result['success']:
                print(f"✅ نجح التصدير: {result['method']}")
                if result['method'] == 'cloudinary':
                    print(f"🔗 رابط التحميل: {result['url']}")
                else:
                    print(f"📁 حجم الملف: {len(result['data']) / 1024:.1f} KB")
            else:
                print(f"❌ فشل التصدير: {result['error']}")
                return False
        else:
            print("⚠️ Cloudinary غير مُعد - سيتم استخدام التخزين المحلي")
            
            result = export_enhanced_excel_with_cloudinary(test_data)
            
            if result['success'] and result['method'] == 'local':
                print(f"✅ نجح التصدير المحلي: {len(result['data']) / 1024:.1f} KB")
            else:
                print(f"❌ فشل التصدير المحلي: {result.get('error', 'خطأ غير معروف')}")
                return False
                
    except Exception as e:
        print(f"❌ خطأ في اختبار Cloudinary: {e}")
        return False
    
    return True

def test_image_processing():
    """اختبار معالجة الصور"""
    print("\n🖼️ اختبار معالجة الصور...")
    
    try:
        from excel_export_enhanced import download_image_from_cloudinary
        
        # اختبار تحميل صورة تجريبية من Cloudinary
        test_url = "https://res.cloudinary.com/demo/image/upload/sample.jpg"
        
        img_buffer = download_image_from_cloudinary(test_url)
        
        if img_buffer:
            size = len(img_buffer.getvalue()) / 1024  # KB
            print(f"✅ تم تحميل وضغط الصورة: {size:.1f} KB")
            return True
        else:
            print("❌ فشل في تحميل الصورة")
            return False
            
    except Exception as e:
        print(f"❌ خطأ في معالجة الصور: {e}")
        return False

def main():
    """الدالة الرئيسية للاختبار"""
    print("🧪 اختبار شامل لتصدير Excel المحسن")
    print("=" * 60)
    
    tests = [
        ("دوال التصدير", test_excel_export_functions),
        ("معالجة الصور", test_image_processing)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n📋 تشغيل اختبار: {test_name}")
        print("-" * 40)
        
        try:
            result = test_func()
            results.append((test_name, result))
            
            if result:
                print(f"✅ {test_name}: نجح")
            else:
                print(f"❌ {test_name}: فشل")
        except Exception as e:
            print(f"❌ {test_name}: خطأ - {e}")
            results.append((test_name, False))
    
    # ملخص النتائج
    print("\n" + "=" * 60)
    print("📊 ملخص نتائج الاختبار")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ نجح" if result else "❌ فشل"
        print(f"   {test_name}: {status}")
    
    print(f"\n🎯 النتيجة الإجمالية: {passed}/{total} اختبار نجح")
    
    if passed == total:
        print("\n🎉 جميع الاختبارات نجحت! تصدير Excel جاهز للاستخدام")
        print("\n📋 الميزات المتاحة:")
        print("   ✅ تصدير Excel مع تنسيق محسن")
        print("   ✅ إضافة الصور من Cloudinary")
        print("   ✅ ألوان وحدود واضحة")
        print("   ✅ ملخص تلقائي للبيانات")
        print("   ✅ رفع إلى Cloudinary (إذا كان مُعد)")
        return True
    else:
        print(f"\n❌ {total - passed} اختبار فشل - يرجى مراجعة الأخطاء أعلاه")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)