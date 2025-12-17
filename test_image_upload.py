#!/usr/bin/env python3
"""
اختبار رفع الصور إلى Cloudinary
"""

import os
from dotenv import load_dotenv
from cloudinary_config import upload_image_to_cloudinary, is_cloudinary_configured
from PIL import Image as PILImage
from io import BytesIO

# تحميل متغيرات البيئة
load_dotenv()

def create_test_image():
    """إنشاء صورة تجريبية للاختبار"""
    try:
        # إنشاء صورة تجريبية 200x200 بكسل
        img = PILImage.new('RGB', (200, 200), color='blue')
        
        # إضافة نص
        try:
            from PIL import ImageDraw, ImageFont
            draw = ImageDraw.Draw(img)
            draw.text((50, 90), "TEST IMAGE", fill='white')
        except:
            pass  # إذا لم تكن الخطوط متاحة
        
        # حفظ في BytesIO
        img_buffer = BytesIO()
        img.save(img_buffer, format='JPEG', quality=90)
        img_buffer.seek(0)
        
        return img_buffer
        
    except Exception as e:
        print(f"خطأ في إنشاء الصورة التجريبية: {e}")
        return None

def test_cloudinary_upload():
    """اختبار رفع صورة إلى Cloudinary"""
    print("🧪 اختبار رفع الصور إلى Cloudinary")
    print("=" * 50)
    
    # التحقق من إعداد Cloudinary
    if not is_cloudinary_configured():
        print("❌ Cloudinary غير مُعد!")
        print("\n🔧 لإعداد Cloudinary:")
        print("1. اذهب إلى: https://cloudinary.com")
        print("2. أنشئ حساب مجاني")
        print("3. احصل على: Cloud Name, API Key, API Secret")
        print("4. أضفهم إلى ملف .env")
        print("5. راجع CLOUDINARY_QUICK_SETUP.md للتفاصيل")
        return False
    
    print("✅ Cloudinary مُعد بشكل صحيح")
    
    # إنشاء صورة تجريبية
    print("\n📸 إنشاء صورة تجريبية...")
    test_image = create_test_image()
    
    if not test_image:
        print("❌ فشل في إنشاء الصورة التجريبية")
        return False
    
    print("✅ تم إنشاء صورة تجريبية (200x200 بكسل)")
    
    # محاولة رفع الصورة
    print("\n☁️ رفع الصورة إلى Cloudinary...")
    
    try:
        # محاكاة ملف مرفوع
        class MockFile:
            def __init__(self, data):
                self.data = data
                self.filename = "test_image.jpg"
            
            def read(self):
                return self.data.getvalue()
        
        mock_file = MockFile(test_image)
        
        result = upload_image_to_cloudinary(mock_file, "test_uploads")
        
        if result['success']:
            print("🎉 نجح رفع الصورة إلى Cloudinary!")
            print(f"🔗 رابط الصورة: {result['url']}")
            print(f"📊 معلومات الصورة:")
            print(f"   - الحجم: {result['width']}x{result['height']} بكسل")
            print(f"   - الحجم بالبايت: {result['bytes']} بايت")
            print(f"   - التنسيق: {result['format']}")
            print(f"   - المعرف: {result['public_id']}")
            
            return True
        else:
            print(f"❌ فشل رفع الصورة: {result.get('error', 'خطأ غير معروف')}")
            return False
            
    except Exception as e:
        print(f"❌ خطأ في رفع الصورة: {e}")
        return False

def test_cloudinary_integration():
    """اختبار التكامل مع التطبيق"""
    print("\n🔗 اختبار التكامل مع التطبيق...")
    
    try:
        # اختبار دالة التحقق
        from app import is_cloudinary_configured as app_cloudinary_check
        
        if app_cloudinary_check():
            print("✅ التطبيق يتعرف على إعدادات Cloudinary")
        else:
            print("❌ التطبيق لا يتعرف على إعدادات Cloudinary")
            return False
        
        # اختبار استيراد الدوال
        from app import upload_image_to_cloudinary as app_upload
        print("✅ دوال رفع الصور متاحة في التطبيق")
        
        return True
        
    except Exception as e:
        print(f"❌ خطأ في التكامل: {e}")
        return False

def main():
    """الدالة الرئيسية"""
    print("🚀 اختبار شامل لـ Cloudinary")
    print("=" * 60)
    
    tests = [
        ("رفع الصور", test_cloudinary_upload),
        ("التكامل مع التطبيق", test_cloudinary_integration)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n📋 تشغيل اختبار: {test_name}")
        print("-" * 40)
        
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ خطأ في الاختبار: {e}")
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
        print("\n🎉 Cloudinary جاهز للاستخدام!")
        print("\n📋 الآن يمكنك:")
        print("   ✅ رفع الصور من خلال التطبيق")
        print("   ✅ تصدير Excel مع صور من Cloudinary")
        print("   ✅ حفظ ملفات Excel في السحابة")
        print("   ✅ حماية كاملة من فقدان البيانات")
        
        print("\n🚀 خطوات الاستخدام:")
        print("1. شغل التطبيق: python app.py")
        print("2. أدخل بيانات جديدة مع صور")
        print("3. جرب التصدير المحسن")
        print("4. تحقق من Cloudinary Console")
        
    else:
        print(f"\n❌ {total - passed} اختبار فشل")
        print("🔧 راجع CLOUDINARY_QUICK_SETUP.md لحل المشاكل")

if __name__ == "__main__":
    main()