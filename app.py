from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash, send_file
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import sqlite3
import os
from datetime import datetime, timezone, timedelta
import pandas as pd
from io import BytesIO
from dotenv import load_dotenv
try:
    import psycopg2
    from urllib.parse import urlparse
    PSYCOPG2_AVAILABLE = True
except ImportError:
    PSYCOPG2_AVAILABLE = False
    print("⚠️ psycopg2 not available - PostgreSQL support disabled")

from excel_export_enhanced import (
    create_enhanced_excel_with_images,
    create_simple_excel_with_formatting
)

# دوال بديلة لحفظ الصور محلياً
def save_image_locally(file, subfolder=""):
    """حفظ صورة محلياً في مجلد static/uploads"""
    try:
        if not file or not file.filename:
            return None
        
        # إنشاء اسم ملف فريد
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{secure_filename(file.filename)}"
        
        # إنشاء المجلد إذا لم يكن موجوداً
        upload_dir = os.path.join('static', 'uploads')
        if subfolder:
            upload_dir = os.path.join(upload_dir, subfolder)
        
        os.makedirs(upload_dir, exist_ok=True)
        
        # حفظ الملف
        file_path = os.path.join(upload_dir, filename)
        file.save(file_path)
        
        return filename
        
    except Exception as e:
        print(f"خطأ في حفظ الصورة: {e}")
        return None

def create_temp_excel_file(data, filename):
    """إنشاء ملف Excel مؤقت"""
    try:
        temp_path = create_simple_excel_with_formatting(data, filename)
        return temp_path
    except Exception as e:
        print(f"خطأ في إنشاء ملف Excel: {e}")
        return None

def cleanup_temp_file(file_path):
    """حذف ملف مؤقت"""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
    except Exception as e:
        print(f"خطأ في حذف الملف المؤقت: {e}")
    return False
import requests

# Load environment variables
load_dotenv()

# إعداد المنطقة الزمنية المحلية - مصر (القاهرة)
# يتعامل تلقائياً مع التوقيت الشتوي والصيفي
try:
    from zoneinfo import ZoneInfo
    LOCAL_TIMEZONE = ZoneInfo("Africa/Cairo")
except ImportError:
    # Fallback for older Python versions
    try:
        import pytz
        LOCAL_TIMEZONE = pytz.timezone("Africa/Cairo")
    except ImportError:
        # Final fallback - Egypt winter time (UTC+2)
        LOCAL_TIMEZONE = timezone(timedelta(hours=2))
        print("⚠️ Warning: Using fixed UTC+2. Install zoneinfo or pytz for automatic DST handling.")

def get_local_time():
    """الحصول على الوقت المحلي الحالي (القاهرة) مع التعامل التلقائي مع التوقيت الشتوي/الصيفي"""
    return datetime.now(LOCAL_TIMEZONE)

def get_local_time_string():
    """الحصول على الوقت المحلي كنص منسق (القاهرة)"""
    return get_local_time().strftime('%Y-%m-%d %H:%M:%S')

def get_display_name(user_record):
    """Get display name with fallback logic"""
    if isinstance(user_record, (list, tuple)) and len(user_record) > 6:
        full_name = user_record[6] if user_record[6] else None
        username = user_record[1]
    else:
        # Handle cases where full_name might not be available
        full_name = None
        username = user_record[1] if isinstance(user_record, (list, tuple)) else str(user_record)
    
    return full_name if full_name and full_name.strip() else username

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-change-this')
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Database configuration
DATABASE_URL = os.getenv('DATABASE_URL')
IS_PRODUCTION = DATABASE_URL is not None

def get_db_connection():
    """Get database connection based on environment"""
    if IS_PRODUCTION and DATABASE_URL and PSYCOPG2_AVAILABLE:
        # Production: PostgreSQL
        url = urlparse(DATABASE_URL)
        conn = psycopg2.connect(
            host=url.hostname,
            port=url.port,
            database=url.path[1:],
            user=url.username,
            password=url.password,
            sslmode='require'
        )
        return conn, 'postgresql'
    else:
        # Development: SQLite
        conn = sqlite3.connect('database.db')
        return conn, 'sqlite'

def execute_query(query, params=None, fetch_one=False, fetch_all=False):
    """Execute query with proper database handling"""
    conn, db_type = get_db_connection()
    
    try:
        cursor = conn.cursor()
        
        if db_type == 'postgresql':
            # Convert SQLite placeholders to PostgreSQL
            if params:
                pg_query = query.replace('?', '%s')
                cursor.execute(pg_query, params)
            else:
                cursor.execute(query)
        else:
            # SQLite
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
        
        result = None
        if fetch_one:
            result = cursor.fetchone()
        elif fetch_all:
            result = cursor.fetchall()
        else:
            result = cursor.rowcount
            
        conn.commit()
        return result
        
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def init_db():
    """Initialize database with persistent data preservation"""
    conn, db_type = get_db_connection()
    c = conn.cursor()
    
    # Users table
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        company_code TEXT NOT NULL,
        password TEXT NOT NULL,
        is_admin BOOLEAN DEFAULT FALSE,
        created_date TEXT DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Add created_date column if it doesn't exist (for existing databases)
    try:
        c.execute('ALTER TABLE users ADD COLUMN created_date TEXT')
    except sqlite3.OperationalError:
        pass  # Column already exists
    
    # Add full_name column if it doesn't exist (for existing databases)
    try:
        c.execute('ALTER TABLE users ADD COLUMN full_name TEXT')
    except sqlite3.OperationalError:
        pass  # Column already exists
    
    # Data entries table
    c.execute('''CREATE TABLE IF NOT EXISTS data_entries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_name TEXT NOT NULL,
        employee_code TEXT NOT NULL,
        branch TEXT NOT NULL,
        shop_code TEXT,
        model TEXT NOT NULL,
        display_type TEXT NOT NULL,
        selected_materials TEXT,
        unselected_materials TEXT,
        images TEXT,
        comment TEXT,
        date TEXT NOT NULL
    )''')
    
    # Add comment column if it doesn't exist (for existing databases)
    try:
        c.execute('ALTER TABLE data_entries ADD COLUMN comment TEXT')
    except sqlite3.OperationalError:
        pass  # Column already exists
    
    # Branches table for autocomplete
    c.execute('''CREATE TABLE IF NOT EXISTS branches (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        branch_name TEXT NOT NULL,
        shop_code TEXT NOT NULL,
        employee_code TEXT NOT NULL,
        created_date TEXT NOT NULL,
        UNIQUE(branch_name, employee_code),
        UNIQUE(shop_code, employee_code)
    )''')
    
    # Categories management table
    c.execute('''CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category_name TEXT NOT NULL UNIQUE,
        created_date TEXT NOT NULL
    )''')
    
    # Models management table
    c.execute('''CREATE TABLE IF NOT EXISTS models (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        model_name TEXT NOT NULL,
        category_name TEXT NOT NULL,
        created_date TEXT NOT NULL,
        UNIQUE(model_name, category_name)
    )''')
    
    # Display types management table
    c.execute('''CREATE TABLE IF NOT EXISTS display_types (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        display_type_name TEXT NOT NULL,
        category_name TEXT NOT NULL,
        created_date TEXT NOT NULL,
        UNIQUE(display_type_name, category_name)
    )''')
    
    # POP materials management table
    c.execute('''CREATE TABLE IF NOT EXISTS pop_materials_db (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        material_name TEXT NOT NULL,
        model_name TEXT NOT NULL,
        category_name TEXT NOT NULL,
        created_date TEXT NOT NULL,
        UNIQUE(material_name, model_name)
    )''')
    
    # User branches management table
    c.execute('''CREATE TABLE IF NOT EXISTS user_branches (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        branch_name TEXT NOT NULL,
        created_date TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
        UNIQUE(user_id, branch_name)
    )''')
    
    # Model images table for guide images
    c.execute('''CREATE TABLE IF NOT EXISTS model_images (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        model_name TEXT NOT NULL,
        category_name TEXT NOT NULL,
        image_url TEXT NOT NULL,
        created_date TEXT NOT NULL,
        UNIQUE(model_name, category_name)
    )''')
    
    # Database initialization status table
    c.execute('''CREATE TABLE IF NOT EXISTS db_init_status (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        component TEXT NOT NULL UNIQUE,
        initialized BOOLEAN DEFAULT FALSE,
        last_update TEXT NOT NULL
    )''')
    
    # Check if this is the first run or if we need to initialize data
    initialize_system_data(c)
    
    conn.commit()
    conn.close()

def initialize_system_data(cursor):
    """Initialize system data only if not already done"""
    current_time = get_local_time_string()
    
    # Check if admin user exists
    cursor.execute('SELECT COUNT(*) FROM users WHERE is_admin = TRUE')
    admin_count = cursor.fetchone()[0]
    
    if admin_count == 0:
        print("🔧 Creating admin user...")
        admin_password = generate_password_hash('admin123')
        cursor.execute('INSERT INTO users (name, company_code, password, is_admin) VALUES (?, ?, ?, ?)',
                     ('Admin', 'ADMIN', admin_password, True))
        
        # Mark admin as initialized
        cursor.execute('INSERT OR REPLACE INTO db_init_status (component, initialized, last_update) VALUES (?, ?, ?)',
                     ('admin_user', True, current_time))
        print("✅ Admin user created")
    
    # Check if default categories are initialized
    cursor.execute('SELECT initialized FROM db_init_status WHERE component = ?', ('default_categories',))
    categories_init = cursor.fetchone()
    
    if not categories_init or not categories_init[0]:
        print("🔧 Initializing default categories...")
        initialize_default_categories(cursor)
        cursor.execute('INSERT OR REPLACE INTO db_init_status (component, initialized, last_update) VALUES (?, ?, ?)',
                     ('default_categories', True, current_time))
        print("✅ Default categories initialized")
    
    # Check if default models are initialized
    cursor.execute('SELECT initialized FROM db_init_status WHERE component = ?', ('default_models',))
    models_init = cursor.fetchone()
    
    if not models_init or not models_init[0]:
        print("🔧 Initializing default models...")
        initialize_default_models(cursor)
        cursor.execute('INSERT OR REPLACE INTO db_init_status (component, initialized, last_update) VALUES (?, ?, ?)',
                     ('default_models', True, current_time))
        print("✅ Default models initialized")
    
    # Check if default display types are initialized
    cursor.execute('SELECT initialized FROM db_init_status WHERE component = ?', ('default_display_types',))
    display_types_init = cursor.fetchone()
    
    if not display_types_init or not display_types_init[0]:
        print("🔧 Initializing default display types...")
        initialize_default_display_types(cursor)
        cursor.execute('INSERT OR REPLACE INTO db_init_status (component, initialized, last_update) VALUES (?, ?, ?)',
                     ('default_display_types', True, current_time))
        print("✅ Default display types initialized")
    
    # Check if default POP materials are initialized
    cursor.execute('SELECT initialized FROM db_init_status WHERE component = ?', ('default_pop_materials',))
    pop_materials_init = cursor.fetchone()
    
    if not pop_materials_init or not pop_materials_init[0]:
        print("🔧 Initializing default POP materials...")
        initialize_default_pop_materials(cursor)
        cursor.execute('INSERT OR REPLACE INTO db_init_status (component, initialized, last_update) VALUES (?, ?, ?)',
                     ('default_pop_materials', True, current_time))
        print("✅ Default POP materials initialized")

def initialize_default_categories(cursor):
    """Initialize default categories"""
    current_time = get_local_time_string()
    
    categories = ['OLED', 'Neo QLED', 'QLED', 'UHD', 'LTV', 'BESPOKE COMBO', 
                 'BESPOKE Front', 'Front', 'TL', 'SBS', 'TMF', 'BMF', 'Local TMF']
    
    for category in categories:
        cursor.execute('INSERT OR IGNORE INTO categories (category_name, created_date) VALUES (?, ?)',
                      (category, current_time))

def initialize_default_models(cursor):
    """Initialize default models"""
    current_time = get_local_time_string()
    
    models_data = {
        'OLED': ['S95F', 'S90F', 'S85F'],
        'Neo QLED': ['QN90', 'QN85F', 'QN80F', 'QN70F'],
        'QLED': ['Q8F', 'Q7F'],
        'UHD': ['U8000', '100"/98"'],
        'LTV': ['The Frame'],
        'BESPOKE COMBO': ['WD25DB8995', 'WD21D6400'],
        'BESPOKE Front': ['WW11B1944DGB'],
        'Front': ['WW11B1534D', 'WW90CGC', 'WW4040', 'WW4020'],
        'TL': ['WA19CG6886', 'Local TL'],
        'SBS': ['RS70F'],
        'TMF': ['Bespoke', 'TMF Non-Bespoke', 'TMF'],
        'BMF': ['(Bespoke, BMF)', '(Non-Bespoke, BMF)'],
        'Local TMF': ['Local TMF']
    }
    
    for category, models in models_data.items():
        for model in models:
            cursor.execute('INSERT OR IGNORE INTO models (model_name, category_name, created_date) VALUES (?, ?, ?)',
                          (model, category, current_time))

def initialize_default_display_types(cursor):
    """Initialize default display types"""
    current_time = get_local_time_string()
    
    display_types_data = {
        'OLED': ['Highlight Zone', 'Fixtures', 'Multi Brand Zone with Space', 'SIS (Endcap)'],
        'Neo QLED': ['Highlight Zone', 'Fixtures', 'Multi Brand Zone with Space', 'SIS (Endcap)'],
        'QLED': ['Highlight Zone', 'Fixtures', 'Multi Brand Zone with Space', 'SIS (Endcap)'],
        'UHD': ['Highlight Zone', 'Fixtures', 'Multi Brand Zone with Space', 'SIS (Endcap)'],
        'LTV': ['Highlight Zone', 'Fixtures', 'Multi Brand Zone with Space', 'SIS (Endcap)'],
        'BESPOKE COMBO': ['POP Out', 'POP Inner', 'POP'],
        'BESPOKE Front': ['POP Out', 'POP Inner', 'POP'],
        'Front': ['POP Out', 'POP Inner', 'POP'],
        'TL': ['POP Out', 'POP Inner', 'POP'],
        'SBS': ['POP Out', 'POP Inner', 'POP'],
        'TMF': ['POP Out', 'POP Inner', 'POP'],
        'BMF': ['POP Out', 'POP Inner', 'POP'],
        'Local TMF': ['POP Out', 'POP Inner', 'POP']
    }
    
    for category, display_types in display_types_data.items():
        for display_type in display_types:
            cursor.execute('INSERT OR IGNORE INTO display_types (display_type_name, category_name, created_date) VALUES (?, ?, ?)',
                          (display_type, category, current_time))

def initialize_default_pop_materials(cursor):
    """Initialize default POP materials by model"""
    current_time = get_local_time_string()
    
    # Get existing models
    cursor.execute('SELECT model_name, category_name FROM models')
    models = cursor.fetchall()
    
    # Default materials by model
    model_materials = {
        # OLED Models
        'S95F': ['S95F Premium Topper', 'S95F Gaming Features', 'S95F Design POP', 'Anti-Glare Technology', 'AI topper'],
        'S90F': ['S90F Smart Features', 'S90F Connectivity POP', 'S90F Performance Card', 'AI topper'],
        'S85F': ['S85F Essential Features', 'S85F Value POP', 'S85F Specs Display', 'AI topper'],
        
        # Neo QLED Models
        'QN90': ['QN90 Neo Quantum', 'QN90 Gaming Hub', 'QN90 Premium Features', 'Neo Quantum Processor 4K', 'AI topper'],
        'QN85F': ['QN85F Neo Features', 'QN85F Smart Hub', 'QN85F Performance POP', 'AI topper'],
        'QN80F': ['QN80F Neo Display', 'QN80F Features Card', 'QN80F Value POP', 'AI topper'],
        'QN70F': ['QN70F Essential Neo', 'QN70F Basic Features', 'QN70F Entry POP', 'AI topper'],
        
        # Add more models as needed...
    }
    
    for model_name, category_name in models:
        # Get materials for this model or use default
        materials = model_materials.get(model_name, [f'{model_name} Standard POP', f'{model_name} Features', 'AI topper'])
        
        for material in materials:
            cursor.execute('INSERT OR IGNORE INTO pop_materials_db (material_name, model_name, category_name, created_date) VALUES (?, ?, ?, ?)',
                          (material, model_name, category_name, current_time))



@app.route('/')
def index():
    return render_template('login.html')

@app.route('/manifest.json')
def manifest():
    return send_file('static/manifest.json', mimetype='application/json')

@app.route('/sw.js')
def service_worker():
    return send_file('static/sw.js', mimetype='application/javascript')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    remember_me = 'remember_me' in request.form
    
    conn, db_type = get_db_connection()
    c = conn.cursor()
    
    # Try to get user with full_name, fallback if column doesn't exist
    try:
        c.execute('SELECT id, name, company_code, password, is_admin, full_name FROM users WHERE name = ?', (username,))
        user = c.fetchone()
        full_name_index = 5
    except sqlite3.OperationalError:
        # full_name column doesn't exist yet, use basic query
        c.execute('SELECT id, name, company_code, password, is_admin FROM users WHERE name = ?', (username,))
        user = c.fetchone()
        full_name_index = None
    
    conn.close()
    
    if user and check_password_hash(user[3], password):
        session['user_id'] = user[0]
        session['user_name'] = user[1]
        session['company_code'] = user[2]  # كود الموظف سيبقى في الجلسة للاستخدام في التقارير
        session['is_admin'] = user[4]
        session['full_name'] = user[full_name_index] if full_name_index and len(user) > full_name_index else None
        session.permanent = remember_me
        
        if user[4]:  # is_admin
            return redirect(url_for('admin_dashboard'))
        else:
            return redirect(url_for('data_entry'))
    else:
        flash('Invalid login credentials')
        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/data_entry')
def data_entry():
    if 'user_id' not in session or session.get('is_admin'):
        return redirect(url_for('index'))
    return render_template('data_entry.html')

@app.route('/get_dynamic_data/<data_type>')
def get_dynamic_data(data_type):
    """Get dynamic data from database for frontend"""
    try:
        conn, db_type = get_db_connection()
        c = conn.cursor()
        
        if data_type == 'categories':
            c.execute('SELECT category_name FROM categories ORDER BY category_name')
            data = [row[0] for row in c.fetchall()]
        
        elif data_type == 'models':
            category = request.args.get('category', '')
            if category:
                c.execute('SELECT model_name FROM models WHERE category_name = ? ORDER BY model_name', (category,))
            else:
                c.execute('SELECT model_name, category_name FROM models ORDER BY category_name, model_name')
            data = c.fetchall()
        
        elif data_type == 'display_types':
            category = request.args.get('category', '')
            if category:
                c.execute('SELECT display_type_name FROM display_types WHERE category_name = ? ORDER BY display_type_name', (category,))
                data = [row[0] for row in c.fetchall()]
            else:
                data = []
        
        elif data_type == 'pop_materials':
            model = request.args.get('model', '')
            if model:
                c.execute('SELECT material_name FROM pop_materials_db WHERE model_name = ? ORDER BY material_name', (model,))
                data = [row[0] for row in c.fetchall()]
            else:
                data = []
        
        conn.close()
        return jsonify({'success': True, 'data': data})
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/get_branches', methods=['GET'])
def get_branches():
    if 'user_id' not in session or session.get('is_admin'):
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    try:
        user_id = session['user_id']
        search_term = request.args.get('search', '').strip()
        
        conn, db_type = get_db_connection()
        c = conn.cursor()
        
        if search_term:
            # Search in user's assigned branches only
            c.execute('''SELECT ub.branch_name, b.shop_code 
                        FROM user_branches ub
                        LEFT JOIN branches b ON ub.branch_name = b.branch_name AND b.employee_code = ?
                        WHERE ub.user_id = ? AND ub.branch_name LIKE ?
                        ORDER BY ub.branch_name''', 
                     (session['company_code'], user_id, f'%{search_term}%'))
        else:
            # Get all user's assigned branches
            c.execute('''SELECT ub.branch_name, b.shop_code 
                        FROM user_branches ub
                        LEFT JOIN branches b ON ub.branch_name = b.branch_name AND b.employee_code = ?
                        WHERE ub.user_id = ?
                        ORDER BY ub.branch_name''', 
                     (session['company_code'], user_id))
        
        branches = [{'name': row[0], 'code': row[1] if row[1] else 'N/A'} for row in c.fetchall()]
        conn.close()
        
        return jsonify({'success': True, 'branches': branches})
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/get_branch_by_code', methods=['GET'])
def get_branch_by_code():
    if 'user_id' not in session or session.get('is_admin'):
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    try:
        employee_code = session['company_code']
        shop_code = request.args.get('code', '').strip()
        
        if not shop_code:
            return jsonify({'success': False, 'message': 'Shop code is required'})
        
        conn, db_type = get_db_connection()
        c = conn.cursor()
        
        c.execute('''SELECT branch_name, shop_code FROM branches 
                    WHERE employee_code = ? AND shop_code = ?''', 
                 (employee_code, shop_code))
        
        result = c.fetchone()
        conn.close()
        
        if result:
            return jsonify({'success': True, 'branch': {'name': result[0], 'code': result[1]}})
        else:
            return jsonify({'success': False, 'message': 'Branch not found'})
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/submit_data', methods=['POST'])
def submit_data():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Unauthorized - Please login'}), 401
    
    # Allow both regular users and admins to submit data
    if session.get('is_admin'):
        print("⚠️ Admin user submitting data - this is allowed for testing")
    
    try:
        # Get form data
        employee_name = session.get('full_name') if session.get('full_name') and session.get('full_name').strip() else session['user_name']
        employee_code = session['company_code']
        
        print(f"🔍 Processing data submission for {employee_name} ({employee_code})")
        
        # Log all form data for debugging
        print("📋 All form data received:")
        for key, value in request.form.items():
            print(f"   {key}: {value}")
        
        # Process multiple model entries
        entries_saved = 0
        model_index = 0
        
        while f'branch_{model_index}' in request.form:
            try:
                branch = request.form.get(f'branch_{model_index}')
                shop_code = request.form.get(f'shop_code_{model_index}')
                category = request.form.get(f'category_{model_index}')
                model = request.form.get(f'model_{model_index}')
                display_type = request.form.get(f'display_type_{model_index}')
                comment = request.form.get(f'comment_{model_index}', '')
                
                print(f"🔍 Processing model {model_index}:")
                print(f"   Branch: '{branch}'")
                print(f"   Shop Code: '{shop_code}'")
                print(f"   Category: '{category}'")
                print(f"   Model: '{model}'")
                print(f"   Display Type: '{display_type}'")
                print(f"   Comment: '{comment}'")
                
                # Validate required fields
                missing_fields = []
                if not branch: missing_fields.append('branch')
                if not shop_code: missing_fields.append('shop_code')
                if not category: missing_fields.append('category')
                if not model: missing_fields.append('model')
                if not display_type: missing_fields.append('display_type')
                
                if missing_fields:
                    print(f"❌ Missing required fields for model {model_index}: {missing_fields}")
                    model_index += 1
                    continue
                
                # Save branch if it's new
                if branch and shop_code:
                    conn, db_type = get_db_connection()
                    c = conn.cursor()
                    try:
                        c.execute('''INSERT OR IGNORE INTO branches 
                                    (branch_name, shop_code, employee_code, created_date) 
                                    VALUES (?, ?, ?, ?)''',
                                 (branch, shop_code, employee_code, get_local_time_string()))
                        conn.commit()
                    except:
                        pass  # Branch already exists, ignore
                    conn.close()
                
                # Get selected POP materials
                selected_materials = request.form.getlist(f'pop_materials_{model_index}')
            
                # Define all possible materials by category
                pop_materials_by_category = {
                'OLED': [
                    'AI topper', 'Oled Topper', 'Glare Free', 'New Topper', '165 HZ Side POP',
                    'Category POP', 'Samsung OLED Topper', '165 HZ & joy stick indicator',
                    'AI Topper Gaming', 'Side POP', 'Specs Card', 'OLED Topper', 'Why Oled side POP'
                ],
                'Neo QLED': [
                    'AI topper', 'Lockup Topper', 'Screen POP', 'New Topper', 'Glare Free', 'Specs Card'
                ],
                'QLED': [
                    'AI topper', 'Samsung QLED Topper', 'Screen POP', 'New Topper', 'Specs Card', 'QLED Topper'
                ],
                'UHD': [
                    'UHD topper', 'Samsung UHD topper', 'Screen POP', 'New Topper', 'Specs Card',
                    'AI topper', 'Samsung Lockup Topper', 'Inch Logo side POP'
                ],
                'LTV': [
                    'Side POP', 'Matte Display', 'Category POP', 'Frame Bezel'
                ],
                'BESPOKE COMBO': [
                    'PODs (Door)', 'POD (Top)', 'POD (Front)', '3 PODs (Top)', 'AI Home POP',
                    'AI Home', 'AI control panel', 'Capacity (Kg)', 'Capacity Dryer', 'Filter',
                    'Ecobuble POP', 'Ecco Buble', 'AI Ecco Buble', '20 Years Warranty',
                    'New Arrival', 'Samsung Brand/Tech Topper'
                ],
                'BESPOKE Front': [
                    'PODs (Door)', 'POD (Top)', 'POD (Front)', '3 PODs (Top)', 'AI Home POP',
                    'AI Home', 'AI control panel', 'Capacity (Kg)', 'Capacity Dryer', 'Filter',
                    'Ecobuble POP', 'Ecco Buble', 'AI Ecco Buble', '20 Years Warranty',
                    'New Arrival', 'Samsung Brand/Tech Topper'
                ],
                'Front': [
                    'PODs (Door)', 'POD (Top)', 'POD (Front)', '3 PODs (Top)', 'AI Home POP',
                    'AI Home', 'AI control panel', 'Capacity (Kg)', 'Capacity Dryer', 'Filter',
                    'Ecobuble POP', 'Ecco Buble', 'AI Ecco Buble', '20 Years Warranty',
                    'New Arrival', 'Samsung Brand/Tech Topper'
                ],
                'TL': [
                    'PODs (Door)', 'POD (Top)', 'POD (Front)', '3 PODs (Top)', 'AI Home POP',
                    'AI Home', 'AI control panel', 'Capacity (Kg)', 'Capacity Dryer', 'Filter',
                    'Ecobuble POP', 'Ecco Buble', 'AI Ecco Buble', '20 Years Warranty',
                    'New Arrival', 'Samsung Brand/Tech Topper'
                ],
                'SBS': [
                    'Samsung Brand/Tech Topper', 'Main POD', '20 Years Warranty', 'Twin Cooling Plus™',
                    'Smart Conversion™', 'Digital Inverter™', 'SpaceMax™', 'Tempered Glass',
                    'Power Freeze', 'Big Vegetable Box', 'Organize Big Bin'
                ],
                'TMF': [
                    'Samsung Brand/Tech Topper', '20 Years Warranty', 'Key features POP', 'Side POP',
                    'Global No.1', 'Freshness POP', 'Bacteria Safe Ionizer POP', 'Gallon Guard POP',
                    'Big Vegetables Box POP', 'Adjustable Pin & Organize POP', 'Optimal Fresh',
                    'Tempered Glass', 'Gallon Guard', 'Veg Box', 'Internal Display', 'Multi Tray',
                    'Foldable Shelf', 'Active Fresh Filter'
                ],
                'BMF': [
                    'Samsung Brand/Tech Topper', '20 Years Warranty', 'Key features POP', 'Side POP',
                    'Global No.1', 'Led Lighting POP', 'Full Open Box POP', 'Big Guard POP',
                    'Adjustable Pin', 'Saves Energy POP', 'Gentle Lighting', 'Multi Tray',
                    'All-Around Cooling', '2 Step Foldable Shelf', 'Big Fresh Box'
                ],
                'Local TMF': [
                    'Samsung Brand/Tech Topper', 'Key features POP', 'Side POP', 'Big Vegetables Box POP'
                ]
                }
                
                # Get all materials for the selected model from database
                conn_materials, db_type_materials = get_db_connection()
                c_materials = conn_materials.cursor()
                c_materials.execute('SELECT material_name FROM pop_materials_db WHERE model_name = ?', (model,))
                model_materials = [row[0] for row in c_materials.fetchall()]
                conn_materials.close()
                
                # Calculate unselected materials based on model-specific materials
                unselected_materials = [mat for mat in model_materials if mat not in selected_materials]
            
                # Handle image uploads
                uploaded_images = []
                if f'images_{model_index}' in request.files:
                    files = request.files.getlist(f'images_{model_index}')
                    for file in files:
                        if file and file.filename:
                            # حفظ محلي فقط
                            filename = secure_filename(file.filename)
                            timestamp = get_local_time().strftime('%Y%m%d_%H%M%S_')
                            filename = timestamp + filename
                            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                            try:
                                file.save(file_path)
                                uploaded_images.append(filename)
                            except Exception as e:
                                flash(f'خطأ في حفظ الصورة: {str(e)}', 'error')
                
                # Save to database
                conn, db_type = get_db_connection()
                c = conn.cursor()
                c.execute('''INSERT INTO data_entries 
                            (employee_name, employee_code, branch, shop_code, model, display_type, 
                             selected_materials, unselected_materials, images, comment, date)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                         (employee_name, employee_code, branch, shop_code, f"{category} - {model}", 
                          display_type, ','.join(selected_materials), 
                          ','.join(unselected_materials), ','.join(uploaded_images), comment,
                          get_local_time_string()))
                
                conn.commit()
                conn.close()
                
                print(f"✅ Successfully saved model {model_index}: {category} - {model}")
                entries_saved += 1
                
            except Exception as model_error:
                print(f"❌ Error saving model {model_index}: {str(model_error)}")
                # Continue with next model instead of failing completely
                
            model_index += 1
        
        if entries_saved > 0:
            return jsonify({
                'success': True, 
                'message': f'{entries_saved} model entries saved successfully!'
            })
        else:
            return jsonify({
                'success': False, 
                'message': 'No valid model entries found to save. Please check your form data.'
            }), 400
        
    except Exception as e:
        print(f"❌ Critical error in submit_data: {str(e)}")
        return jsonify({'success': False, 'message': f'Server error: {str(e)}'}), 500

@app.route('/admin_dashboard')
def admin_dashboard():
    if 'user_id' not in session or not session.get('is_admin'):
        return redirect(url_for('index'))
    
    # Get filter parameters
    employee_filter = request.args.get('employee', '')
    branch_filter = request.args.get('branch', '')
    model_filter = request.args.get('model', '')
    date_from = request.args.get('date_from', '')
    date_to = request.args.get('date_to', '')
    
    # Build query
    query = 'SELECT * FROM data_entries WHERE 1=1'
    params = []
    
    if employee_filter:
        query += ' AND employee_name LIKE ?'
        params.append(f'%{employee_filter}%')
    
    if branch_filter:
        query += ' AND branch LIKE ?'
        params.append(f'%{branch_filter}%')
    
    if model_filter:
        query += ' AND model LIKE ?'
        params.append(f'%{model_filter}%')
    
    if date_from:
        query += ' AND date >= ?'
        params.append(date_from)
    
    if date_to:
        query += ' AND date <= ?'
        params.append(date_to + ' 23:59:59')
    
    query += ' ORDER BY date DESC'
    
    # Execute query
    conn, db_type = get_db_connection()
    c = conn.cursor()
    c.execute(query, params)
    data_entries = c.fetchall()
    
    # Get unique values for filters
    c.execute('SELECT DISTINCT employee_name FROM data_entries ORDER BY employee_name')
    employees = [row[0] for row in c.fetchall()]
    
    c.execute('SELECT DISTINCT branch FROM data_entries ORDER BY branch')
    branches = [row[0] for row in c.fetchall()]
    
    c.execute('SELECT DISTINCT model FROM data_entries ORDER BY model')
    models = [row[0] for row in c.fetchall()]
    
    conn.close()
    
    return render_template('admin_dashboard.html', 
                         data_entries=data_entries,
                         employees=employees,
                         branches=branches,
                         models=models,
                         filters={
                             'employee': employee_filter,
                             'branch': branch_filter,
                             'model': model_filter,
                             'date_from': date_from,
                             'date_to': date_to
                         })

@app.route('/export_excel')
def export_excel():
    """تصدير Excel محسن مع الصور والتنسيق"""
    if 'user_id' not in session or not session.get('is_admin'):
        return redirect(url_for('index'))
    
    try:
        # الحصول على معاملات الفلترة من الطلب
        employee_filter = request.args.get('employee', '')
        branch_filter = request.args.get('branch', '')
        model_filter = request.args.get('model', '')
        date_from = request.args.get('date_from', '')
        date_to = request.args.get('date_to', '')
        
        # بناء الاستعلام مع الفلاتر (نفس منطق admin_dashboard)
        query = '''SELECT id, employee_name, employee_code, branch, shop_code, model, 
                          display_type, selected_materials, unselected_materials, images, date, comment 
                   FROM data_entries WHERE 1=1'''
        params = []
        
        if employee_filter:
            query += ' AND employee_name LIKE ?'
            params.append(f'%{employee_filter}%')
        
        if branch_filter:
            query += ' AND branch LIKE ?'
            params.append(f'%{branch_filter}%')
        
        if model_filter:
            query += ' AND model LIKE ?'
            params.append(f'%{model_filter}%')
        
        if date_from:
            query += ' AND date >= ?'
            params.append(date_from)
        
        if date_to:
            query += ' AND date <= ?'
            params.append(date_to + ' 23:59:59')
        
        query += ' ORDER BY date DESC'
        
        # تنفيذ الاستعلام
        conn, db_type = get_db_connection()
        c = conn.cursor()
        c.execute(query, params)
        entries = c.fetchall()
        conn.close()
        
        if not entries:
            flash('لا توجد بيانات للتصدير مع الفلاتر المحددة')
            return redirect(url_for('admin_dashboard'))
        
        # إضافة رسالة توضيحية عن عدد السجلات
        flash(f'جاري تصدير {len(entries)} سجل مع الفلاتر المطبقة')
        
        # تصدير محسن مع الصور (محلي فقط)
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'pop_materials_report_enhanced_{timestamp}.xlsx'
            
            temp_path = create_enhanced_excel_with_images(entries, filename)
            
            if temp_path and os.path.exists(temp_path):
                # قراءة الملف وإرساله
                with open(temp_path, 'rb') as f:
                    file_data = f.read()
                
                # حذف الملف المؤقت
                cleanup_temp_file(temp_path)
                
                flash('تم إنشاء التقرير المحسن بنجاح!')
                return send_file(
                    BytesIO(file_data),
                    mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                    as_attachment=True,
                    download_name=filename
                )
            else:
                flash('خطأ في إنشاء التقرير المحسن')
                return redirect(url_for('export_excel_simple'))
                
        except Exception as e:
            flash(f'خطأ في التصدير المحسن: {str(e)}')
            return redirect(url_for('export_excel_simple'))
            
    except Exception as e:
        flash(f'خطأ في تصدير البيانات: {str(e)}')
        return redirect(url_for('admin_dashboard'))

@app.route('/export_excel_simple')
def export_excel_simple():
    """تصدير Excel بسيط مع تنسيق محسن (بدون صور)"""
    if 'user_id' not in session or not session.get('is_admin'):
        return redirect(url_for('index'))
    
    try:
        # الحصول على معاملات الفلترة من الطلب
        employee_filter = request.args.get('employee', '')
        branch_filter = request.args.get('branch', '')
        model_filter = request.args.get('model', '')
        date_from = request.args.get('date_from', '')
        date_to = request.args.get('date_to', '')
        
        # بناء الاستعلام مع الفلاتر (نفس منطق admin_dashboard)
        query = '''SELECT id, employee_name, employee_code, branch, shop_code, model, 
                          display_type, selected_materials, unselected_materials, images, date, comment 
                   FROM data_entries WHERE 1=1'''
        params = []
        
        if employee_filter:
            query += ' AND employee_name LIKE ?'
            params.append(f'%{employee_filter}%')
        
        if branch_filter:
            query += ' AND branch LIKE ?'
            params.append(f'%{branch_filter}%')
        
        if model_filter:
            query += ' AND model LIKE ?'
            params.append(f'%{model_filter}%')
        
        if date_from:
            query += ' AND date >= ?'
            params.append(date_from)
        
        if date_to:
            query += ' AND date <= ?'
            params.append(date_to + ' 23:59:59')
        
        query += ' ORDER BY date DESC'
        
        # تنفيذ الاستعلام
        conn, db_type = get_db_connection()
        c = conn.cursor()
        c.execute(query, params)
        entries = c.fetchall()
        conn.close()
        
        if not entries:
            flash('لا توجد بيانات للتصدير مع الفلاتر المحددة')
            return redirect(url_for('admin_dashboard'))
        
        # إضافة رسالة توضيحية عن عدد السجلات
        flash(f'جاري تصدير {len(entries)} سجل (بسيط) مع الفلاتر المطبقة')
        
        # إنشاء اسم الملف
        timestamp = get_local_time().strftime('%Y%m%d_%H%M%S')
        filename = f'pop_materials_simple_{timestamp}.xlsx'
        
        # إنشاء ملف Excel مع تنسيق
        temp_path = create_simple_excel_with_formatting(entries, filename)
        
        if not temp_path:
            flash('خطأ في إنشاء ملف Excel')
            return redirect(url_for('admin_dashboard'))
        
        # إرسال الملف مباشرة (محلي فقط)
        with open(temp_path, 'rb') as f:
            file_data = f.read()
        
        cleanup_temp_file(temp_path)
        
        flash('تم إنشاء التقرير بنجاح')
        return send_file(
            BytesIO(file_data),
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=filename
        )
    
    except Exception as e:
        flash(f'خطأ في تصدير البيانات: {str(e)}')
        return redirect(url_for('admin_dashboard'))

# تم دمج وظائف التصدير في excel_export_enhanced.py

@app.route('/download_image/<filename>')
def download_image(filename):
    if 'user_id' not in session or not session.get('is_admin'):
        return redirect(url_for('index'))
    
    try:
        return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename), 
                        as_attachment=True)
    except Exception as e:
        flash(f'Error downloading image: {str(e)}')
        return redirect(url_for('admin_dashboard'))

@app.route('/admin_management')
def admin_management():
    if 'user_id' not in session or not session.get('is_admin'):
        return redirect(url_for('index'))
    return render_template('admin_management.html')

@app.route('/get_management_data/<data_type>')
def get_management_data(data_type):
    if 'user_id' not in session or not session.get('is_admin'):
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    try:
        conn, db_type = get_db_connection()
        c = conn.cursor()
        
        if data_type == 'categories':
            c.execute('SELECT * FROM categories ORDER BY category_name')
            data = [{'id': row[0], 'name': row[1], 'created_date': row[2]} for row in c.fetchall()]
        
        elif data_type == 'models':
            category = request.args.get('category', '')
            if category:
                c.execute('SELECT * FROM models WHERE category_name = ? ORDER BY model_name', (category,))
            else:
                c.execute('SELECT * FROM models ORDER BY category_name, model_name')
            data = [{'id': row[0], 'name': row[1], 'category': row[2], 'created_date': row[3]} for row in c.fetchall()]
        
        elif data_type == 'display_types':
            category = request.args.get('category', '')
            if category:
                c.execute('SELECT * FROM display_types WHERE category_name = ? ORDER BY display_type_name', (category,))
            else:
                c.execute('SELECT * FROM display_types ORDER BY category_name, display_type_name')
            data = [{'id': row[0], 'name': row[1], 'category': row[2], 'created_date': row[3]} for row in c.fetchall()]
        
        elif data_type == 'pop_materials':
            model = request.args.get('model', '')
            category = request.args.get('category', '')
            if model:
                c.execute('SELECT * FROM pop_materials_db WHERE model_name = ? ORDER BY material_name', (model,))
                data = [{'id': row[0], 'name': row[1], 'model': row[2], 'category': row[3], 'created_date': row[4]} for row in c.fetchall()]
            elif category:
                c.execute('SELECT * FROM pop_materials_db WHERE category_name = ? ORDER BY model_name, material_name', (category,))
                data = [{'id': row[0], 'name': row[1], 'model': row[2], 'category': row[3], 'created_date': row[4]} for row in c.fetchall()]
            else:
                c.execute('SELECT * FROM pop_materials_db ORDER BY category_name, model_name, material_name')
                data = [{'id': row[0], 'name': row[1], 'model': row[2], 'category': row[3], 'created_date': row[4]} for row in c.fetchall()]
        
        else:
            return jsonify({'success': False, 'message': 'Invalid data type'}), 400
        
        conn.close()
        return jsonify({'success': True, 'data': data})
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/manage_data', methods=['POST'])
def manage_data():
    if 'user_id' not in session or not session.get('is_admin'):
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    try:
        data = request.get_json()
        action = data.get('action')
        data_type = data.get('type')
        
        conn, db_type = get_db_connection()
        c = conn.cursor()
        
        if action == 'add':
            return handle_add_data(c, conn, data_type, data)
        elif action == 'edit':
            return handle_edit_data(c, conn, data_type, data)
        elif action == 'delete':
            return handle_delete_data(c, conn, data_type, data)
        else:
            return jsonify({'success': False, 'message': 'Invalid action'}), 400
            
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

def handle_add_data(cursor, conn, data_type, data):
    current_time = get_local_time_string()
    
    if data_type == 'categories':
        cursor.execute('INSERT INTO categories (category_name, created_date) VALUES (?, ?)',
                      (data['name'], current_time))
    
    elif data_type == 'models':
        cursor.execute('INSERT INTO models (model_name, category_name, created_date) VALUES (?, ?, ?)',
                      (data['name'], data['category'], current_time))
    
    elif data_type == 'display_types':
        cursor.execute('INSERT INTO display_types (display_type_name, category_name, created_date) VALUES (?, ?, ?)',
                      (data['name'], data['category'], current_time))
    
    elif data_type == 'pop_materials':
        cursor.execute('INSERT OR IGNORE INTO pop_materials_db (material_name, model_name, category_name, created_date) VALUES (?, ?, ?, ?)',
                      (data['name'], data['model'], data['category'], current_time))
    
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': f'{data_type.title()} added successfully'})

def handle_edit_data(cursor, conn, data_type, data):
    if data_type == 'categories':
        # Get old category name for cascading updates
        cursor.execute('SELECT category_name FROM categories WHERE id = ?', (data['id'],))
        old_category = cursor.fetchone()
        old_category_name = old_category[0] if old_category else None
        
        # Update category
        cursor.execute('UPDATE categories SET category_name = ? WHERE id = ?',
                      (data['name'], data['id']))
        
        # Cascading update: Update all related tables
        if old_category_name and old_category_name != data['name']:
            cursor.execute('UPDATE models SET category_name = ? WHERE category_name = ?',
                          (data['name'], old_category_name))
            cursor.execute('UPDATE display_types SET category_name = ? WHERE category_name = ?',
                          (data['name'], old_category_name))
            cursor.execute('UPDATE pop_materials_db SET category_name = ? WHERE category_name = ?',
                          (data['name'], old_category_name))
            cursor.execute('UPDATE data_entries SET model = REPLACE(model, ?, ?) WHERE model LIKE ?',
                          (old_category_name, data['name'], f"{old_category_name} - %"))
    
    elif data_type == 'models':
        # Get old model name for cascading updates
        cursor.execute('SELECT model_name FROM models WHERE id = ?', (data['id'],))
        old_model = cursor.fetchone()
        old_model_name = old_model[0] if old_model else None
        
        # Update model
        cursor.execute('UPDATE models SET model_name = ?, category_name = ? WHERE id = ?',
                      (data['name'], data['category'], data['id']))
        
        # Cascading update: Update all POP materials and data entries with this model
        if old_model_name and old_model_name != data['name']:
            cursor.execute('UPDATE pop_materials_db SET model_name = ?, category_name = ? WHERE model_name = ?',
                          (data['name'], data['category'], old_model_name))
            cursor.execute('UPDATE data_entries SET model = ? WHERE model = ?',
                          (f"{data['category']} - {data['name']}", f"{data['category']} - {old_model_name}"))
    
    elif data_type == 'display_types':
        # Get old display type name for cascading updates
        cursor.execute('SELECT display_type_name FROM display_types WHERE id = ?', (data['id'],))
        old_display_type = cursor.fetchone()
        old_display_type_name = old_display_type[0] if old_display_type else None
        
        # Update display type
        cursor.execute('UPDATE display_types SET display_type_name = ?, category_name = ? WHERE id = ?',
                      (data['name'], data['category'], data['id']))
        
        # Cascading update: Update all data entries with this display type
        if old_display_type_name and old_display_type_name != data['name']:
            cursor.execute('UPDATE data_entries SET display_type = ? WHERE display_type = ?',
                          (data['name'], old_display_type_name))
    
    elif data_type == 'pop_materials':
        cursor.execute('UPDATE pop_materials_db SET material_name = ?, model_name = ?, category_name = ? WHERE id = ?',
                      (data['name'], data['model'], data['category'], data['id']))
    
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': f'{data_type.title()} updated successfully with cascading changes'})

def handle_delete_data(cursor, conn, data_type, data):
    if data_type == 'categories':
        # Get category name before deletion for cascading deletes
        cursor.execute('SELECT category_name FROM categories WHERE id = ?', (data['id'],))
        category_result = cursor.fetchone()
        category_name = category_result[0] if category_result else None
        
        # Delete category
        cursor.execute('DELETE FROM categories WHERE id = ?', (data['id'],))
        
        # Cascading delete: Remove all related data
        if category_name:
            cursor.execute('DELETE FROM models WHERE category_name = ?', (category_name,))
            cursor.execute('DELETE FROM display_types WHERE category_name = ?', (category_name,))
            cursor.execute('DELETE FROM pop_materials_db WHERE category_name = ?', (category_name,))
    
    elif data_type == 'models':
        # Get model name before deletion for cascading deletes
        cursor.execute('SELECT model_name FROM models WHERE id = ?', (data['id'],))
        model_result = cursor.fetchone()
        model_name = model_result[0] if model_result else None
        
        # Delete model
        cursor.execute('DELETE FROM models WHERE id = ?', (data['id'],))
        
        # Cascading delete: Remove all POP materials for this model
        if model_name:
            cursor.execute('DELETE FROM pop_materials_db WHERE model_name = ?', (model_name,))
    
    elif data_type == 'display_types':
        cursor.execute('DELETE FROM display_types WHERE id = ?', (data['id'],))
    
    elif data_type == 'pop_materials':
        cursor.execute('DELETE FROM pop_materials_db WHERE id = ?', (data['id'],))
    
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': f'{data_type.title()} deleted successfully with related data'})

@app.route('/delete_entry/<int:entry_id>', methods=['DELETE'])
def delete_entry(entry_id):
    if 'user_id' not in session or not session.get('is_admin'):
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    try:
        conn, db_type = get_db_connection()
        c = conn.cursor()
        
        # Get entry details before deletion for cleanup
        c.execute('SELECT images FROM data_entries WHERE id = ?', (entry_id,))
        result = c.fetchone()
        
        if result and result[0]:
            # Delete associated images
            images = result[0].split(',')
            for image in images:
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], image)
                if os.path.exists(image_path):
                    os.remove(image_path)
        
        # Delete the entry
        c.execute('DELETE FROM data_entries WHERE id = ?', (entry_id,))
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': 'Entry deleted successfully'})
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/user_management')
def user_management():
    if 'user_id' not in session or not session.get('is_admin'):
        return redirect(url_for('index'))
    
    conn, db_type = get_db_connection()
    c = conn.cursor()
    
    # Get users with their branches count from user_branches table
    try:
        # Try to get users with full_name column
        c.execute('''SELECT u.id, u.name, u.company_code, u.password, u.is_admin, u.full_name,
                            (SELECT COUNT(*) FROM user_branches ub WHERE ub.user_id = u.id) as branch_count,
                            (SELECT GROUP_CONCAT(ub.branch_name, ', ') FROM user_branches ub WHERE ub.user_id = u.id LIMIT 5) as sample_branches
                     FROM users u 
                     ORDER BY u.is_admin DESC, u.name''')
        users = c.fetchall()
    except sqlite3.OperationalError:
        # full_name column doesn't exist yet, use basic query
        c.execute('''SELECT u.id, u.name, u.company_code, u.password, u.is_admin, NULL as full_name,
                            (SELECT COUNT(*) FROM user_branches ub WHERE ub.user_id = u.id) as branch_count,
                            (SELECT GROUP_CONCAT(ub.branch_name, ', ') FROM user_branches ub WHERE ub.user_id = u.id LIMIT 5) as sample_branches
                     FROM users u 
                     ORDER BY u.is_admin DESC, u.name''')
        users = c.fetchall()
    
    conn.close()
    
    return render_template('user_management.html', users=users)

@app.route('/manage_user', methods=['POST'])
def manage_user():
    if 'user_id' not in session or not session.get('is_admin'):
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    try:
        data = request.get_json()
        action = data.get('action')
        
        conn, db_type = get_db_connection()
        c = conn.cursor()
        
        if action == 'add':
            name = data.get('name')
            full_name = data.get('full_name', '').strip() or None
            company_code = data.get('company_code')
            password = data.get('password')
            is_admin = data.get('is_admin', False)
            
            # Check if user already exists
            c.execute('SELECT * FROM users WHERE name = ? OR company_code = ?', (name, company_code))
            if c.fetchone():
                return jsonify({'success': False, 'message': 'User with this name or company code already exists'})
            
            hashed_password = generate_password_hash(password)
            c.execute('INSERT INTO users (name, company_code, password, is_admin, full_name) VALUES (?, ?, ?, ?, ?)',
                     (name, company_code, hashed_password, is_admin, full_name))
            
        elif action == 'edit':
            user_id = data.get('id')
            name = data.get('name')
            full_name = data.get('full_name', '').strip() or None
            company_code = data.get('company_code')
            password = data.get('password')
            is_admin = data.get('is_admin', False)
            
            # Check if another user has the same name or company code
            c.execute('SELECT * FROM users WHERE (name = ? OR company_code = ?) AND id != ?', 
                     (name, company_code, user_id))
            if c.fetchone():
                return jsonify({'success': False, 'message': 'Another user with this name or company code already exists'})
            
            if password:
                # Update with new password
                hashed_password = generate_password_hash(password)
                c.execute('UPDATE users SET name = ?, company_code = ?, password = ?, is_admin = ?, full_name = ? WHERE id = ?',
                         (name, company_code, hashed_password, is_admin, full_name, user_id))
            else:
                # Update without changing password
                c.execute('UPDATE users SET name = ?, company_code = ?, is_admin = ?, full_name = ? WHERE id = ?',
                         (name, company_code, is_admin, full_name, user_id))
            
        elif action == 'delete':
            user_id = data.get('id')
            
            # Prevent deleting the current admin user
            if user_id == session['user_id']:
                return jsonify({'success': False, 'message': 'Cannot delete your own account'})
            
            # Check if this is the last admin
            c.execute('SELECT COUNT(*) FROM users WHERE is_admin = TRUE')
            admin_count = c.fetchone()[0]
            
            c.execute('SELECT is_admin FROM users WHERE id = ?', (user_id,))
            user_to_delete = c.fetchone()
            
            if user_to_delete and user_to_delete[0] and admin_count <= 1:
                return jsonify({'success': False, 'message': 'Cannot delete the last admin user'})
            
            # Delete user's branches and data entries
            c.execute('SELECT company_code FROM users WHERE id = ?', (user_id,))
            user_data = c.fetchone()
            if user_data:
                company_code = user_data[0]
                c.execute('DELETE FROM branches WHERE employee_code = ?', (company_code,))
                
                # Get and delete images from data entries
                c.execute('SELECT images FROM data_entries WHERE employee_code = ?', (company_code,))
                entries = c.fetchall()
                for entry in entries:
                    if entry[0]:
                        images = entry[0].split(',')
                        for image in images:
                            image_path = os.path.join(app.config['UPLOAD_FOLDER'], image)
                            if os.path.exists(image_path):
                                os.remove(image_path)
                
                c.execute('DELETE FROM data_entries WHERE employee_code = ?', (company_code,))
            
            c.execute('DELETE FROM users WHERE id = ?', (user_id,))
        
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': f'User {action}ed successfully'})
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/change_admin_password', methods=['POST'])
def change_admin_password():
    if 'user_id' not in session or not session.get('is_admin'):
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    try:
        data = request.get_json()
        current_password = data.get('current_password')
        new_password = data.get('new_password')
        
        conn, db_type = get_db_connection()
        c = conn.cursor()
        c.execute('SELECT password FROM users WHERE id = ?', (session['user_id'],))
        user = c.fetchone()
        
        if not user or not check_password_hash(user[0], current_password):
            return jsonify({'success': False, 'message': 'Current password is incorrect'})
        
        hashed_password = generate_password_hash(new_password)
        c.execute('UPDATE users SET password = ? WHERE id = ?', (hashed_password, session['user_id']))
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': 'Password changed successfully'})
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' not in session or not session.get('is_admin'):
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        name = request.form['name']
        full_name = request.form.get('full_name', '').strip() or None
        company_code = request.form['company_code']
        password = request.form['password']
        branch_names = request.form.getlist('branch_names[]')
        branch_codes = request.form.getlist('branch_codes[]')
        
        # Check if user already exists
        conn, db_type = get_db_connection()
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE name = ? OR company_code = ?', (name, company_code))
        existing_user = c.fetchone()
        
        if existing_user:
            flash('User with this name or company code already exists')
        else:
            # Create user
            hashed_password = generate_password_hash(password)
            c.execute('INSERT INTO users (name, company_code, password, is_admin, full_name) VALUES (?, ?, ?, ?, ?)',
                     (name, company_code, hashed_password, False, full_name))
            
            # Get the new user ID
            user_id = c.lastrowid
            
            # Add branches for this user
            current_time = get_local_time_string()
            for branch_name, branch_code in zip(branch_names, branch_codes):
                if branch_name.strip() and branch_code.strip():
                    # Add to user_branches table
                    c.execute('INSERT INTO user_branches (user_id, branch_name, created_date) VALUES (?, ?, ?)',
                             (user_id, branch_name.strip(), current_time))
                    
                    # Also add to branches table for this employee
                    c.execute('INSERT OR IGNORE INTO branches (branch_name, shop_code, employee_code, created_date) VALUES (?, ?, ?, ?)',
                             (branch_name.strip(), branch_code.strip(), company_code, current_time))
            
            conn.commit()
            flash(f'User registered successfully with {len([b for b in branch_names if b.strip()])} branches')
        
        conn.close()
        return redirect(url_for('user_management'))
    
    return render_template('register.html')

@app.route('/get_user_branches/<int:user_id>')
def get_user_branches(user_id):
    """Get branches for a specific user"""
    if 'user_id' not in session or not session.get('is_admin'):
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    try:
        conn, db_type = get_db_connection()
        c = conn.cursor()
        
        # Get user's company code first
        c.execute('SELECT company_code FROM users WHERE id = ?', (user_id,))
        user_result = c.fetchone()
        if not user_result:
            return jsonify({'success': False, 'message': 'User not found'}), 404
        
        company_code = user_result[0]
        
        # Get user branches with shop codes - improved matching
        c.execute('''SELECT ub.id, ub.branch_name, 
                           COALESCE(b.shop_code, 'N/A') as shop_code
                    FROM user_branches ub
                    LEFT JOIN branches b ON LOWER(TRIM(ub.branch_name)) = LOWER(TRIM(b.branch_name)) 
                    AND b.employee_code = ?
                    WHERE ub.user_id = ?
                    ORDER BY ub.branch_name''', (company_code, user_id))
        
        branches = []
        for row in c.fetchall():
            branches.append({
                'id': row[0],
                'branch_name': row[1],
                'shop_code': row[2]
            })
        
        conn.close()
        return jsonify({'success': True, 'branches': branches})
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/manage_user_branches', methods=['POST'])
def manage_user_branches():
    """Manage user branches (add/remove)"""
    if 'user_id' not in session or not session.get('is_admin'):
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    try:
        data = request.get_json()
        action = data.get('action')
        user_id = data.get('user_id')
        
        if not user_id:
            return jsonify({'success': False, 'message': 'User ID is required'}), 400
        
        conn, db_type = get_db_connection()
        c = conn.cursor()
        
        # Get user's company code
        c.execute('SELECT company_code FROM users WHERE id = ?', (user_id,))
        user_result = c.fetchone()
        if not user_result:
            return jsonify({'success': False, 'message': 'User not found'}), 404
        
        company_code = user_result[0]
        current_time = get_local_time_string()
        
        if action == 'add_branch':
            branch_name = data.get('branch_name', '').strip()
            branch_code = data.get('branch_code', '').strip()
            
            print(f"DEBUG: Adding branch - User ID: {user_id}, Branch: {branch_name}, Code: {branch_code}")
            
            if not branch_name or not branch_code:
                print(f"DEBUG: Missing data - Branch name: '{branch_name}', Branch code: '{branch_code}'")
                return jsonify({'success': False, 'message': 'Branch name and code are required'}), 400
            
            # Check if branch already exists for this user
            c.execute('SELECT id FROM user_branches WHERE user_id = ? AND LOWER(TRIM(branch_name)) = LOWER(TRIM(?))', 
                     (user_id, branch_name))
            existing_branch = c.fetchone()
            if existing_branch:
                print(f"DEBUG: Branch already exists - ID: {existing_branch[0]}")
                return jsonify({'success': False, 'message': 'Branch already exists for this user'}), 400
            
            # Add to user_branches
            c.execute('INSERT INTO user_branches (user_id, branch_name, created_date) VALUES (?, ?, ?)',
                     (user_id, branch_name, current_time))
            
            # Check if shop_code already exists for this employee
            c.execute('SELECT id, branch_name FROM branches WHERE shop_code = ? AND employee_code = ?',
                     (branch_code, company_code))
            existing_code = c.fetchone()
            
            if existing_code and existing_code[1] != branch_name:
                return jsonify({'success': False, 'message': f'Shop code "{branch_code}" is already used for branch "{existing_code[1]}"'}), 400
            
            # Update or insert into branches table - use REPLACE to ensure consistency
            c.execute('DELETE FROM branches WHERE branch_name = ? AND employee_code = ?',
                     (branch_name, company_code))
            c.execute('INSERT INTO branches (branch_name, shop_code, employee_code, created_date) VALUES (?, ?, ?, ?)',
                     (branch_name, branch_code, company_code, current_time))
            
            conn.commit()
            print(f"DEBUG: Branch added successfully - {branch_name} with code {branch_code}")
            conn.close()
            return jsonify({'success': True, 'message': 'Branch added successfully'})
        
        elif action == 'remove_branch':
            branch_id = data.get('branch_id')
            
            if not branch_id:
                return jsonify({'success': False, 'message': 'Branch ID is required'}), 400
            
            # Get branch name before deleting
            c.execute('SELECT branch_name FROM user_branches WHERE id = ? AND user_id = ?', (branch_id, user_id))
            branch_result = c.fetchone()
            
            if not branch_result:
                return jsonify({'success': False, 'message': 'Branch not found'}), 404
            
            branch_name = branch_result[0]
            
            # Remove from user_branches
            c.execute('DELETE FROM user_branches WHERE id = ? AND user_id = ?', (branch_id, user_id))
            
            # Remove from branches table if no other user uses it
            c.execute('DELETE FROM branches WHERE branch_name = ? AND employee_code = ?', (branch_name, company_code))
            
            conn.commit()
            conn.close()
            return jsonify({'success': True, 'message': 'Branch removed successfully'})
        
        elif action == 'add_multiple_branches':
            branches = data.get('branches', [])
            
            if not branches:
                return jsonify({'success': False, 'message': 'No branches provided'}), 400
            
            added_count = 0
            for branch in branches:
                branch_name = branch.get('name', '').strip()
                branch_code = branch.get('code', '').strip()
                
                if branch_name and branch_code:
                    # Check if branch already exists for this user
                    c.execute('SELECT id FROM user_branches WHERE user_id = ? AND LOWER(TRIM(branch_name)) = LOWER(TRIM(?))', 
                             (user_id, branch_name))
                    if not c.fetchone():
                        # Check if shop_code already exists for this employee
                        c.execute('SELECT id, branch_name FROM branches WHERE shop_code = ? AND employee_code = ?',
                                 (branch_code, company_code))
                        existing_code = c.fetchone()
                        
                        if not existing_code or existing_code[1] == branch_name:
                            # Add to user_branches
                            c.execute('INSERT INTO user_branches (user_id, branch_name, created_date) VALUES (?, ?, ?)',
                                     (user_id, branch_name, current_time))
                            
                            # Update or insert into branches table - ensure consistency
                            c.execute('DELETE FROM branches WHERE branch_name = ? AND employee_code = ?',
                                     (branch_name, company_code))
                            c.execute('INSERT INTO branches (branch_name, shop_code, employee_code, created_date) VALUES (?, ?, ?, ?)',
                                     (branch_name, branch_code, company_code, current_time))
                            added_count += 1
            
            conn.commit()
            conn.close()
            
            if added_count == 0:
                return jsonify({'success': False, 'message': 'No new branches were added (all already exist)'}), 400
            else:
                return jsonify({'success': True, 'message': f'{added_count} branches added successfully'})
        
        else:
            print(f"DEBUG: Invalid action received: {action}")
            return jsonify({'success': False, 'message': 'Invalid action'}), 400
        
    except Exception as e:
        print(f"DEBUG: Exception in manage_user_branches: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'message': str(e)}), 500

# Model Images Management Routes
@app.route('/upload_model_image', methods=['POST'])
def upload_model_image():
    """Upload guide image for a model"""
    if 'user_id' not in session or not session.get('is_admin'):
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    try:
        model_name = request.form.get('model_name')
        category_name = request.form.get('category_name')
        
        if not model_name or not category_name:
            return jsonify({'success': False, 'message': 'Model name and category are required'}), 400
        
        if 'image' not in request.files:
            return jsonify({'success': False, 'message': 'No image file provided'}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'success': False, 'message': 'No image file selected'}), 400
        
        # Validate file type
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
        if not ('.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in allowed_extensions):
            return jsonify({'success': False, 'message': 'Invalid file type. Only images are allowed.'}), 400
        
        # Save locally only
        filename = secure_filename(f"{category_name}_{model_name}_{file.filename}")
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        try:
            file.save(filepath)
            image_url = f"/static/uploads/{filename}"
        except Exception as e:
            return jsonify({'success': False, 'message': f'Failed to save image: {str(e)}'}), 500
        
        # Save to database
        conn, db_type = get_db_connection()
        c = conn.cursor()
        current_time = get_local_time_string()
        
        c.execute('''INSERT OR REPLACE INTO model_images 
                    (model_name, category_name, image_url, created_date) 
                    VALUES (?, ?, ?, ?)''',
                 (model_name, category_name, image_url, current_time))
        
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': 'Model image uploaded successfully', 'image_url': image_url})
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/get_model_image/<category>/<model>')
def get_model_image(category, model):
    """Get guide image URL for a specific model"""
    try:
        conn, db_type = get_db_connection()
        c = conn.cursor()
        
        # Check if model_images table exists
        if db_type == 'sqlite':
            c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='model_images'")
            if not c.fetchone():
                conn.close()
                return jsonify({'success': False, 'message': 'Model images feature not available - database needs update'})
        
        c.execute('SELECT image_url FROM model_images WHERE model_name = ? AND category_name = ?',
                 (model, category))
        result = c.fetchone()
        conn.close()
        
        if result:
            return jsonify({'success': True, 'image_url': result[0]})
        else:
            return jsonify({'success': False, 'message': 'No image found for this model'})
            
    except Exception as e:
        error_msg = str(e)
        if 'no such table: model_images' in error_msg:
            return jsonify({'success': False, 'message': 'Model images feature not available - please update database'})
        return jsonify({'success': False, 'message': f'Database error: {error_msg}'}), 500

@app.route('/delete_model_image', methods=['POST'])
def delete_model_image():
    """Delete guide image for a model"""
    if 'user_id' not in session or not session.get('is_admin'):
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    try:
        data = request.get_json()
        model_name = data.get('model_name')
        category_name = data.get('category_name')
        
        if not model_name or not category_name:
            return jsonify({'success': False, 'message': 'Model name and category are required'}), 400
        
        conn, db_type = get_db_connection()
        c = conn.cursor()
        
        # Get image URL before deleting
        c.execute('SELECT image_url FROM model_images WHERE model_name = ? AND category_name = ?',
                 (model_name, category_name))
        result = c.fetchone()
        
        if result:
            image_url = result[0]
            
            # Delete from database
            c.execute('DELETE FROM model_images WHERE model_name = ? AND category_name = ?',
                     (model_name, category_name))
            conn.commit()
            
            # Delete local file
            if image_url.startswith('/static/uploads/'):
                try:
                    local_path = image_url.replace('/static/uploads/', '')
                    full_path = os.path.join(app.config['UPLOAD_FOLDER'], local_path)
                    if os.path.exists(full_path):
                        os.remove(full_path)
                except Exception as e:
                    print(f"Warning: Could not delete local file: {e}")
        
        conn.close()
        return jsonify({'success': True, 'message': 'Model image deleted successfully'})
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/model_images_management')
def model_images_management():
    """Model images management page"""
    if 'user_id' not in session or not session.get('is_admin'):
        return redirect(url_for('login'))
    
    try:
        conn, db_type = get_db_connection()
        c = conn.cursor()
        
        # Check if model_images table exists
        if db_type == 'sqlite':
            c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='model_images'")
            if not c.fetchone():
                conn.close()
                flash('Model images feature is not available. Database needs to be updated.', 'warning')
                return redirect(url_for('admin_dashboard'))
        
        # Get all categories
        c.execute('SELECT DISTINCT category_name FROM categories ORDER BY category_name')
        categories = [row[0] for row in c.fetchall()]
        
        # Get all models with their images
        c.execute('''SELECT m.category_name, m.model_name, mi.image_url, mi.created_date
                    FROM models m
                    LEFT JOIN model_images mi ON m.model_name = mi.model_name AND m.category_name = mi.category_name
                    ORDER BY m.category_name, m.model_name''')
        
        models_data = []
        for row in c.fetchall():
            models_data.append({
                'category': row[0],
                'model': row[1],
                'image_url': row[2],
                'created_date': row[3]
            })
        
        conn.close()
        
        return render_template('model_images_management.html', 
                             categories=categories, 
                             models_data=models_data)
        
    except Exception as e:
        error_msg = str(e)
        if 'no such table: model_images' in error_msg:
            flash('Model images feature is not available. Please update the database.', 'warning')
        else:
            flash(f'Error loading model images: {error_msg}', 'error')
        return redirect(url_for('admin_dashboard'))

# تم إزالة دوال إدارة الفروع المعقدة - النظام الآن مبسط

@app.route('/api/export_excel')
def api_export_excel():
    """API endpoint for enhanced Excel export with AJAX support"""
    if 'user_id' not in session or not session.get('is_admin'):
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    try:
        # Get filter parameters from request
        employee_filter = request.args.get('employee', '')
        branch_filter = request.args.get('branch', '')
        model_filter = request.args.get('model', '')
        date_from = request.args.get('date_from', '')
        date_to = request.args.get('date_to', '')
        
        # Build query with filters (same logic as admin_dashboard)
        query = '''SELECT id, employee_name, employee_code, branch, shop_code, model, 
                          display_type, selected_materials, unselected_materials, images, date, comment 
                   FROM data_entries WHERE 1=1'''
        params = []
        
        if employee_filter:
            query += ' AND employee_name LIKE ?'
            params.append(f'%{employee_filter}%')
        
        if branch_filter:
            query += ' AND branch LIKE ?'
            params.append(f'%{branch_filter}%')
        
        if model_filter:
            query += ' AND model LIKE ?'
            params.append(f'%{model_filter}%')
        
        if date_from:
            query += ' AND date >= ?'
            params.append(date_from)
        
        if date_to:
            query += ' AND date <= ?'
            params.append(date_to + ' 23:59:59')
        
        query += ' ORDER BY date DESC'
        
        # Execute query
        conn, db_type = get_db_connection()
        c = conn.cursor()
        c.execute(query, params)
        entries = c.fetchall()
        conn.close()
        
        if not entries:
            return jsonify({
                'success': False, 
                'message': 'لا توجد بيانات للتصدير مع الفلاتر المحددة'
            }), 400
        
        # Enhanced export with images (local only)
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'pop_materials_report_enhanced_{timestamp}.xlsx'
            
            temp_path = create_enhanced_excel_with_images(entries, filename)
            
            if temp_path and os.path.exists(temp_path):
                # Read file and send it
                with open(temp_path, 'rb') as f:
                    file_data = f.read()
                
                # Clean up temp file
                cleanup_temp_file(temp_path)
                
                return send_file(
                    BytesIO(file_data),
                    mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                    as_attachment=True,
                    download_name=filename
                )
            else:
                return jsonify({
                    'success': False,
                    'message': 'خطأ في إنشاء التقرير المحسن'
                }), 500
                
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'خطأ في التصدير المحسن: {str(e)}'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'خطأ في تصدير البيانات: {str(e)}'
        }), 500

@app.route('/api/export_excel_simple')
def api_export_excel_simple():
    """API endpoint for simple Excel export with AJAX support"""
    if 'user_id' not in session or not session.get('is_admin'):
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    try:
        # Get filter parameters from request
        employee_filter = request.args.get('employee', '')
        branch_filter = request.args.get('branch', '')
        model_filter = request.args.get('model', '')
        date_from = request.args.get('date_from', '')
        date_to = request.args.get('date_to', '')
        
        # Build query with filters (same logic as admin_dashboard)
        query = '''SELECT id, employee_name, employee_code, branch, shop_code, model, 
                          display_type, selected_materials, unselected_materials, images, date, comment 
                   FROM data_entries WHERE 1=1'''
        params = []
        
        if employee_filter:
            query += ' AND employee_name LIKE ?'
            params.append(f'%{employee_filter}%')
        
        if branch_filter:
            query += ' AND branch LIKE ?'
            params.append(f'%{branch_filter}%')
        
        if model_filter:
            query += ' AND model LIKE ?'
            params.append(f'%{model_filter}%')
        
        if date_from:
            query += ' AND date >= ?'
            params.append(date_from)
        
        if date_to:
            query += ' AND date <= ?'
            params.append(date_to + ' 23:59:59')
        
        query += ' ORDER BY date DESC'
        
        # Execute query
        conn, db_type = get_db_connection()
        c = conn.cursor()
        c.execute(query, params)
        entries = c.fetchall()
        conn.close()
        
        if not entries:
            return jsonify({
                'success': False,
                'message': 'لا توجد بيانات للتصدير مع الفلاتر المحددة'
            }), 400
        
        # Create filename
        timestamp = get_local_time().strftime('%Y%m%d_%H%M%S')
        filename = f'pop_materials_simple_{timestamp}.xlsx'
        
        # Create Excel file with formatting
        temp_path = create_simple_excel_with_formatting(entries, filename)
        
        if not temp_path:
            return jsonify({
                'success': False,
                'message': 'خطأ في إنشاء ملف Excel'
            }), 500
        
        # Send file directly (local only)
        with open(temp_path, 'rb') as f:
            file_data = f.read()
        
        cleanup_temp_file(temp_path)
        
        return send_file(
            BytesIO(file_data),
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=filename
        )
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'خطأ في تصدير البيانات: {str(e)}'
        }), 500

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=not IS_PRODUCTION)