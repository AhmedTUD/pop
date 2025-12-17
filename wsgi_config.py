#!/usr/bin/python3.10

import sys
import os

# Add your project directory to sys.path
project_home = '/home/yourusername/employee_system'  # غير yourusername إلى اسم المستخدم الخاص بك
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

# Set environment variables
os.environ['FLASK_APP'] = 'app.py'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

# Import your Flask app
from app import app as application

if __name__ == "__main__":
    application.run()