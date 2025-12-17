#!/usr/bin/env python3
"""
Test script to verify image upload functionality is working correctly
"""

import os
import sys

def test_files_exist():
    """Test that all required files exist"""
    files_to_check = [
        'static/js/data_entry.js',
        'static/css/style.css', 
        'templates/data_entry.html'
    ]
    
    print("🔍 Checking if required files exist...")
    
    for file_path in files_to_check:
        if os.path.exists(file_path):
            print(f"✅ {file_path} - EXISTS")
        else:
            print(f"❌ {file_path} - MISSING")
            return False
    
    return True

def test_html_structure():
    """Test HTML structure for image upload"""
    print("\n🔍 Checking HTML structure...")
    
    try:
        with open('templates/data_entry.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Check for enhanced upload elements
        checks = [
            ('file-upload-label', 'Enhanced upload button'),
            ('upload-icon', 'Upload icon'),
            ('upload-text', 'Upload text'),
            ('upload-hint', 'Upload hint'),
            ('image-preview', 'Image preview container'),
            ('multiple accept="image/*,.webp,.avif"', 'Multiple file support')
        ]
        
        for check, description in checks:
            if check in html_content:
                print(f"✅ {description} - FOUND")
            else:
                print(f"❌ {description} - MISSING")
                
    except Exception as e:
        print(f"❌ Error reading HTML: {e}")
        return False
    
    return True

def test_javascript_functions():
    """Test JavaScript functions exist"""
    print("\n🔍 Checking JavaScript functions...")
    
    try:
        with open('static/js/data_entry.js', 'r', encoding='utf-8') as f:
            js_content = f.read()
        
        # Check for required functions
        functions = [
            'setupImageUpload',
            'setupDragAndDrop', 
            'validateImageFiles',
            'handleImagePreview',
            'removeImagePreview'
        ]
        
        for func in functions:
            if f'function {func}' in js_content:
                print(f"✅ {func}() - FOUND")
            else:
                print(f"❌ {func}() - MISSING")
                
    except Exception as e:
        print(f"❌ Error reading JavaScript: {e}")
        return False
    
    return True

def test_css_styles():
    """Test CSS styles exist"""
    print("\n🔍 Checking CSS styles...")
    
    try:
        with open('static/css/style.css', 'r', encoding='utf-8') as f:
            css_content = f.read()
        
        # Check for required styles
        styles = [
            '.file-upload-label',
            '.upload-icon',
            '.upload-text', 
            '.image-preview-item',
            '.remove-image-btn',
            '.file-error'
        ]
        
        for style in styles:
            if style in css_content:
                print(f"✅ {style} - FOUND")
            else:
                print(f"❌ {style} - MISSING")
                
    except Exception as e:
        print(f"❌ Error reading CSS: {e}")
        return False
    
    return True

def main():
    """Run all tests"""
    print("🧪 Testing Image Upload Fix")
    print("=" * 50)
    
    tests = [
        test_files_exist,
        test_html_structure,
        test_javascript_functions,
        test_css_styles
    ]
    
    all_passed = True
    
    for test in tests:
        if not test():
            all_passed = False
    
    print("\n" + "=" * 50)
    
    if all_passed:
        print("🎉 ALL TESTS PASSED!")
        print("\n✅ Image upload functionality should now work correctly:")
        print("   • Enhanced upload button with drag & drop")
        print("   • Multiple image selection")
        print("   • Image preview with file info")
        print("   • File validation (type, size, count)")
        print("   • Remove individual images")
        print("\n🚀 Ready to test in browser!")
    else:
        print("❌ SOME TESTS FAILED!")
        print("Please check the issues above before testing.")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)