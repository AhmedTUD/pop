#!/usr/bin/env python3
"""
إعداد المشروع
"""

import os
import subprocess
import sys

def install_requirements():
    """تثبيت المتطلبات"""
    print("📦 تثبيت المتطلبات...")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("✅ تم تثبيت المتطلبات بنجاح")
        return True
    except subprocess.CalledProcessError:
        print("❌ فشل في تثبيت المتطلبات")
        return False

def setup_env():
    """إعداد ملف البيئة"""
    if not os.path.exists('.env'):
        print("⚙️ إنشاء ملف البيئة...")
        try:
            with open('.env.example', 'r') as source:
                content = source.read()
            with open('.env', 'w') as target:
                target.write(content)
            print("✅ تم إنشاء ملف .env")
        except Exception as e:
            print(f"❌ خطأ في إنشاء ملف البيئة: {e}")
            return False
    else:
        print("✅ ملف البيئة موجود بالفعل")
    return True

def main():
    """الإعداد الرئيسي"""
    print("🔧 بدء إعداد مشروع نظام إدارة مواد POP")
    print("=" * 50)
    
    # تثبيت المتطلبات
    if not install_requirements():
        return False
    
    # إعداد ملف البيئة
    if not setup_env():
        return False
    
    print("\n🎉 تم إعداد المشروع بنجاح!")
    print("\n📋 الخطوات التالية:")
    print("1. تشغيل المشروع: python run.py")
    print("2. أو باستخدام Docker: docker-compose up")
    print("3. فتح المتصفح على: http://localhost:5000")
    print("4. تسجيل الدخول بحساب المدير:")
    print("   - اسم المستخدم: Admin")
    print("   - كلمة المرور: admin123")
    
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)