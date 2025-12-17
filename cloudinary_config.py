import os
import tempfile
from werkzeug.utils import secure_filename
import pandas as pd
from datetime import datetime

def upload_image_to_cloudinary(file, folder="employee_data_images"):
    """
    رفع صورة محلياً (Cloudinary معطل)
    """
    return {
        'success': False,
        'error': 'Cloudinary disabled for PythonAnywhere'
    }

def upload_excel_to_cloudinary(file_path, filename, folder="employee_data_exports"):
    """
    رفع Excel محلياً (Cloudinary معطل)
    """
    return {
        'success': False,
        'error': 'Cloudinary disabled for PythonAnywhere'
    }

def delete_file_from_cloudinary(public_id, resource_type="image"):
    """
    حذف ملف من Cloudinary (معطل)
    """
    return False

def get_cloudinary_images_list(folder="employee_data_images", max_results=100):
    """
    الحصول على قائمة الصور (معطل)
    """
    return []

def create_temp_excel_file(data, filename):
    """
    إنشاء ملف Excel مؤقت
    """
    try:
        temp_dir = tempfile.gettempdir()
        temp_path = os.path.join(temp_dir, filename)
        
        if isinstance(data, dict):
            with pd.ExcelWriter(temp_path, engine='openpyxl') as writer:
                for sheet_name, df in data.items():
                    df.to_excel(writer, sheet_name=sheet_name, index=False)
        else:
            data.to_excel(temp_path, index=False)
        
        return temp_path
        
    except Exception as e:
        print(f"خطأ في إنشاء ملف Excel مؤقت: {e}")
        return None

def cleanup_temp_file(file_path):
    """
    حذف الملف المؤقت
    """
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
    except Exception as e:
        print(f"خطأ في حذف الملف المؤقت: {e}")
    return False

def is_cloudinary_configured():
    """
    التحقق من إعداد Cloudinary - معطل لـ PythonAnywhere
    """
    return False
