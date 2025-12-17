#!/usr/bin/env python3
"""
اختبار سريع لإعدادات Cloudinary
"""

import os
from dotenv import load_dotenv
from cloudinary_config import is_cloudinary_configured, configure_cloudinary
import cloudinary.api

# تحميل متغيرات البيئة
load_dotenv()

def test_cloudinary_connection():
    """اختبار الاتصال بـ Cloudinary"""
    print("🔍 اختبار اتصال Cloudinary...")
    
    # التحقق من وجود المتغيرات
    if not is_cloudinary_configured():
        print("❌ متغيرات Cloudinary غير مُعدة")
        print("📋 المتغيرات المطلوبة:")
        print("   - CLOUDINARY_CLOUD_NAME")
        print("   - CLOUDINARY_API_KEY")
        print("   - CLOUDINARY_API_SECRET")
        print("\n💡 راجع ملف .env.example لمعرفة كيفية الإعداد")
        return False
    
    try:
        # إعداد Cloudinary
        configure_cloudinary()
        
        # اختبار الاتصال
        result = cloudinary.api.ping()
        
        if result.get('status') == 'ok':
            print("✅ الاتصال بـ Cloudinary ناجح!")
            
            # عرض معلومات الحساب
            try:
                usage = cloudinary.api.usage()
                print(f"📊 معلومات الحساب:")
                print(f"   - المساحة المستخدمة: {usage.get('storage', {}).get('usage', 0) / 1024 / 1024:.2f} MB")
                print(f"   - عدد الملفات: {usage.get('resources', 0)}")
                print(f"   - النقل الشهري: {usage.get('bandwidth', {}).get('usage', 0) / 1024 / 1024:.2f} MB")
            except:
                print("📊 معلومات الحساب غير متاحة (هذا طبيعي للحسابات الجديدة)")
            
            return True
        else:
            print("❌ فشل الاتصال بـ Cloudinary")
            return False
            
    except Exception as e:
        print(f"❌ خطأ في الاتصال: {e}")
        print("\n🔧 تحقق من:")
        print("   1. صحة بيانات Cloudinary")
        print("   2. الاتصال بالإنترنت")
        print("   3. إعدادات الحساب")
        return False

def test_environment_variables():
    """اختبار متغيرات البيئة"""
    print("\n🔍 اختبار متغيرات البيئة...")
    
    env_vars = {
        'CLOUDINARY_CLOUD_NAME': os.getenv('CLOUDINARY_CLOUD_NAME'),
        'CLOUDINARY_API_KEY': os.getenv('CLOUDINARY_API_KEY'),
        'CLOUDINARY_API_SECRET': os.getenv('CLOUDINARY_API_SECRET')
    }
    
    all_set = True
    for var_name, var_value in env_vars.items():
        if var_value:
            # إخفاء جزء من القيمة للأمان
            if 'SECRET' in var_name:
                display_value = var_value[:4] + '*' * (len(var_value) - 8) + var_value[-4:]
            else:
                display_value = var_value
            print(f"✅ {var_name}: {display_value}")
        else:
            print(f"❌ {var_name}: غير مُعد")
            all_set = False
    
    return all_set

def main():
    """الدالة الرئيسية للاختبار"""
    print("🧪 اختبار إعدادات Cloudinary")
    print("=" * 40)
    
    # اختبار متغيرات البيئة
    env_ok = test_environment_variables()
    
    if not env_ok:
        print("\n❌ يجب إعداد متغيرات البيئة أولاً")
        print("📖 راجع CLOUDINARY_SETUP_GUIDE.md للمساعدة")
        return False
    
    # اختبار الاتصال
    connection_ok = test_cloudinary_connection()
    
    print("\n" + "=" * 40)
    
    if connection_ok:
        print("🎉 Cloudinary جاهز للاستخدام!")
        print("\n📋 يمكنك الآن:")
        print("   ✅ رفع الصور")
        print("   ✅ تصدير ملفات Excel")
        print("   ✅ النشر على Render")
        return True
    else:
        print("❌ Cloudinary غير جاهز")
        print("\n🔧 راجع CLOUDINARY_SETUP_GUIDE.md لحل المشاكل")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)