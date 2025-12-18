#!/usr/bin/env python3
"""
ملف تشغيل المشروع المبسط
"""

import os
import sys
from app import app, init_db

def main():
    """تشغيل التطبيق"""
    print("🚀 بدء تشغيل نظام إدارة مواد POP - Samsung")
    
    # تهيئة قاعدة البيانات
    print("📊 تهيئة قاعدة البيانات...")
    init_db()
    print("✅ تم تهيئة قاعدة البيانات بنجاح")
    
    # الحصول على المنفذ من متغيرات البيئة أو استخدام 5000 كافتراضي
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    print(f"🌐 التطبيق يعمل على: http://localhost:{port}")
    print("👤 حساب المدير الافتراضي:")
    print("   اسم المستخدم: Admin")
    print("   كلمة المرور: admin123")
    print("\n🛑 اضغط Ctrl+C لإيقاف التطبيق")
    
    try:
        app.run(host='0.0.0.0', port=port, debug=debug)
    except KeyboardInterrupt:
        print("\n👋 تم إيقاف التطبيق بنجاح")
        sys.exit(0)

if __name__ == '__main__':
    main()