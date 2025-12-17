#!/usr/bin/env python3
"""
إنشاء أيقونات PWA بأحجام مختلفة
"""

import os
from PIL import Image, ImageDraw, ImageFont
import math

def create_gradient_background(size, color1=(102, 126, 234), color2=(118, 75, 162)):
    """إنشاء خلفية متدرجة"""
    image = Image.new('RGBA', (size, size), (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)
    
    # رسم دائرة متدرجة
    center = size // 2
    radius = size // 2 - 10
    
    for i in range(radius):
        # حساب اللون المتدرج
        ratio = i / radius
        r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
        g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
        b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
        
        # رسم دائرة
        draw.ellipse([center - radius + i, center - radius + i, 
                     center + radius - i, center + radius - i], 
                    fill=(r, g, b, 255))
    
    return image

def create_icon(size):
    """إنشاء أيقونة بحجم محدد"""
    # إنشاء الخلفية
    image = create_gradient_background(size)
    draw = ImageDraw.Draw(image)
    
    center = size // 2
    
    # حساب أحجام العناصر بناءً على حجم الأيقونة
    font_size_rm = max(size // 12, 12)
    font_size_team = max(size // 20, 8)
    checkbox_size = max(size // 15, 8)
    line_height = max(size // 25, 4)
    
    try:
        # محاولة استخدام خط عربي
        font_rm = ImageFont.truetype("arial.ttf", font_size_rm)
        font_team = ImageFont.truetype("arial.ttf", font_size_team)
    except:
        # استخدام الخط الافتراضي
        font_rm = ImageFont.load_default()
        font_team = ImageFont.load_default()
    
    # رسم نص RM في الأعلى
    rm_text = "RM"
    bbox = draw.textbbox((0, 0), rm_text, font=font_rm)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    draw.text((center - text_width//2, size//6), rm_text, 
              fill=(255, 255, 255, 255), font=font_rm)
    
    # رسم قوائم التحقق في المنتصف
    start_y = center - checkbox_size * 2
    
    for i in range(3):
        y = start_y + i * (checkbox_size + line_height + 5)
        x_checkbox = center - checkbox_size * 3
        
        # رسم مربع الاختيار
        draw.rectangle([x_checkbox, y, x_checkbox + checkbox_size, y + checkbox_size], 
                      outline=(255, 255, 255, 255), width=2)
        
        # رسم علامة الصح للعنصرين الأولين
        if i < 2:
            check_size = checkbox_size // 3
            draw.line([x_checkbox + check_size, y + checkbox_size//2,
                      x_checkbox + checkbox_size//2, y + checkbox_size - check_size,
                      x_checkbox + checkbox_size - check_size//2, y + check_size], 
                     fill=(255, 255, 255, 255), width=2)
        
        # رسم خط النص
        line_x = x_checkbox + checkbox_size + 10
        line_width = checkbox_size * 4 - (10 if i == 1 else 0)
        draw.rectangle([line_x, y + checkbox_size//2 - line_height//2,
                       line_x + line_width, y + checkbox_size//2 + line_height//2], 
                      fill=(255, 255, 255, 255))
    
    # رسم نص TEAM في الأسفل
    team_text = "TEAM"
    bbox = draw.textbbox((0, 0), team_text, font=font_team)
    text_width = bbox[2] - bbox[0]
    draw.text((center - text_width//2, size - size//6), team_text, 
              fill=(255, 255, 255, 255), font=font_team)
    
    return image

def main():
    """إنشاء جميع الأيقونات المطلوبة"""
    # إنشاء مجلد الأيقونات إذا لم يكن موجوداً
    icons_dir = "static/icons"
    os.makedirs(icons_dir, exist_ok=True)
    
    # أحجام الأيقونات المطلوبة
    sizes = [16, 32, 72, 96, 128, 144, 152, 180, 192, 384, 512]
    
    print("🎨 إنشاء أيقونات PWA...")
    
    for size in sizes:
        print(f"📱 إنشاء أيقونة {size}x{size}...")
        icon = create_icon(size)
        
        # حفظ الأيقونة
        filename = f"icon-{size}x{size}.png"
        filepath = os.path.join(icons_dir, filename)
        icon.save(filepath, "PNG")
        print(f"✅ تم حفظ {filename}")
    
    # إنشاء favicon
    print("🌟 إنشاء favicon...")
    favicon = create_icon(32)
    favicon.save(os.path.join(icons_dir, "favicon.ico"), "ICO")
    
    print("🎉 تم إنشاء جميع الأيقونات بنجاح!")
    print(f"📁 الأيقونات محفوظة في: {icons_dir}")

if __name__ == "__main__":
    main()