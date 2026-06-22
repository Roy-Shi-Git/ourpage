#!/usr/bin/env python3
"""
Image Processing Script for Anniversary Website
- Copies and organizes images from picture_timeline folder
- Creates optimized versions for web
- Generates timeline and gallery directories
"""

import os
import shutil
import json
from pathlib import Path
from datetime import datetime
from PIL import Image

# Configuration
SOURCE_DIR = Path('/data/ourblog/picture_timeline')
TARGET_DIR = Path('/data/ourblog/images')
TIMELINE_DIR = TARGET_DIR / 'timeline'
GALLERY_DIR = TARGET_DIR / 'gallery'
COVER_DIR = TARGET_DIR / 'cover'

# Max dimensions for web optimization
MAX_WIDTH = 1920
MAX_HEIGHT = 1080
THUMBNAIL_SIZE = (400, 400)

def setup_directories():
    """Create necessary directory structure"""
    for dir_path in [TARGET_DIR, TIMELINE_DIR, GALLERY_DIR, COVER_DIR]:
        dir_path.mkdir(parents=True, exist_ok=True)
    print(f"✓ 目录结构已创建")

def parse_folder_name(folder_name):
    """Parse folder name to extract date and location"""
    # Common patterns:
    # - "2021年3月14日"
    # - "北京市, 2025年10月18日"
    # - "春节, 2021年2月12日"
    
    import re
    
    # Try to extract date
    date_pattern = r'(\d{4})年(\d{1,2})月(\d{1,2})日'
    match = re.search(date_pattern, folder_name)
    
    if match:
        year, month, day = match.groups()
        date_str = f"{year}-{month.zfill(2)}-{day.zfill(2)}"
        
        # Try to extract location
        location = folder_name.replace(f"{year}年{month}月{day}日", '').strip()
        if location.startswith(','):
            location = location[1:].strip()
        if location.startswith('-'):
            location = location[1:].strip()
        
        return {
            'date': date_str,
            'location': location if location else None,
            'category': categorize_folder(folder_name)
        }
    
    return None

def categorize_folder(folder_name):
    """Determine category based on folder name"""
    folder_lower = folder_name.lower()
    
    if any(kw in folder_lower for kw in ['北京', '上海', '深圳', '广州', '杭州', '哈尔滨', '南宁', '惠州', '澳门', '旅游', '旅行']):
        return 'travel'
    elif any(kw in folder_lower for kw in ['春节', '国庆', '元旦', '新年', '圣诞', '情人节', '520', '521']):
        return 'festival'
    elif any(kw in folder_lower for kw in ['美食', '吃', '餐厅']):
        return 'food'
    elif any(kw in folder_lower for kw in ['搞怪', '搞笑', '表情']):
        return 'fun'
    else:
        return 'daily'

def optimize_image(image_path, output_path, max_size=(MAX_WIDTH, MAX_HEIGHT)):
    """Optimize image for web display"""
    try:
        with Image.open(image_path) as img:
            # Convert to RGB if necessary
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')
            
            # Resize if larger than max dimensions
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            # Save as JPEG with optimization
            img.save(output_path, 'JPEG', quality=85, optimize=True)
            return True
    except Exception as e:
        print(f"  ⚠ 优化失败: {e}")
        return False

def process_images():
    """Process all images from picture_timeline"""
    print("\n📷 开始处理图片...")
    
    # Get all subdirectories (each represents a date/event)
    folders = sorted([f for f in SOURCE_DIR.iterdir() if f.is_dir()])
    
    # Sort by date
    folders.sort(key=lambda x: parse_folder_name(x.name)['date'] if parse_folder_name(x.name) else '9999-12-31')
    
    timeline_data = []
    gallery_items = []
    
    # Select first 3 images for cover photos
    cover_candidates = []
    
    for folder in folders:
        info = parse_folder_name(folder.name)
        if not info:
            continue
        
        # Get all images in this folder
        images = sorted([
            f for f in folder.iterdir() 
            if f.suffix.lower() in ['.jpg', '.jpeg', '.png', '.webp', '.gif']
        ])
        
        if not images:
            continue
        
        print(f"\n📁 {folder.name}")
        print(f"   日期: {info['date']}, 分类: {info['category']}")
        
        # Select representative images
        selected_images = []
        
        # For timeline: select first and last image, or up to 3
        if len(images) >= 3:
            selected_images = [images[0], images[len(images)//2], images[-1]]
        elif len(images) == 2:
            selected_images = images
        else:
            selected_images = images
        
        # Add to cover candidates if early in timeline
        if len(cover_candidates) < 5:
            cover_candidates.append(images[0])
        
        # Process selected images for timeline
        folder_timeline_images = []
        for i, img_path in enumerate(selected_images):
            # Generate filename based on date and index
            filename = f"{info['date']}-{i+1}{img_path.suffix.lower()}"
            if img_path.suffix.lower() in ['.jpg', '.jpeg']:
                filename = filename.replace('.jpeg', '.jpg').replace('.JPEG', '.jpg')
                filename = filename.replace(img_path.suffix, '.jpg')
            output_path = TIMELINE_DIR / filename
            
            if optimize_image(img_path, output_path):
                print(f"   ✓ 封面图: {filename}")
                folder_timeline_images.append(f"timeline/{filename}")
        
        # Add to gallery: all images
        for img_path in images:
            filename = f"{info['date']}-{img_path.name}"
            output_path = GALLERY_DIR / filename
            
            # Create thumbnail version
            thumb_filename = f"thumb_{filename}"
            thumb_path = GALLERY_DIR / thumb_filename
            
            if optimize_image(img_path, output_path):
                # Create thumbnail
                try:
                    with Image.open(img_path) as img:
                        if img.mode in ('RGBA', 'P'):
                            img = img.convert('RGB')
                        img.thumbnail(THUMBNAIL_SIZE, Image.Resampling.LANCZOS)
                        img.save(thumb_path, 'JPEG', quality=80, optimize=True)
                except:
                    pass
                
                gallery_items.append({
                    'src': f"gallery/{filename}",
                    'caption': f"{info['location'] or ''} {info['date']}",
                    'category': info['category']
                })
        
        # Add to timeline data if we have images
        if folder_timeline_images:
            timeline_data.append({
                'date': info['date'],
                'folder': folder.name,
                'images': folder_timeline_images
            })
    
    # Copy cover images
    print("\n🎨 设置封面图片...")
    cover_index = 0
    for i, img_path in enumerate(cover_candidates[:2]):
        filename = 'cover.jpg' if i == 0 else 'recent.jpg'
        output_path = COVER_DIR / filename
        try:
            optimize_image(img_path, output_path, (1920, 1080))
            print(f"   ✓ {filename}")
            cover_index += 1
        except Exception as e:
            print(f"   ⚠ 封面设置失败: {e}")
    
    # Generate timeline JSON for JavaScript
    generate_timeline_js(timeline_data)
    
    # Generate gallery JSON
    generate_gallery_js(gallery_items)
    
    print(f"\n✅ 图片处理完成!")
    print(f"   时间线图片: {len(timeline_data)} 个节点")
    print(f"   相册图片: {len(gallery_items)} 张")
    
    return timeline_data, gallery_items

def generate_timeline_js(timeline_data):
    """Generate timeline data for JavaScript"""
    # Create a structured timeline based on actual images
    events = []
    
    # Group by date and create meaningful descriptions
    for item in timeline_data:
        date = datetime.strptime(item['date'], '%Y-%m-%d')
        formatted_date = f"{date.year}年{date.month}月{date.day}日"
        
        event = {
            'date': item['date'],
            'title': item['folder'].split(',')[0] if ',' in item['folder'] else item['folder'],
            'description': f"{item['folder']}",
            'images': item['images'],
            'category': categorize_folder(item['folder'])
        }
        events.append(event)
    
    # Write to a JSON file that can be included
    with open(TARGET_DIR / 'timeline_data.json', 'w', encoding='utf-8') as f:
        json.dump(events, f, ensure_ascii=False, indent=2)
    
    print(f"   ✓ 生成时间线数据: timeline_data.json")

def generate_gallery_js(gallery_items):
    """Generate gallery data for JavaScript"""
    with open(TARGET_DIR / 'gallery_data.json', 'w', encoding='utf-8') as f:
        json.dump(gallery_items, f, ensure_ascii=False, indent=2)
    
    print(f"   ✓ 生成相册数据: gallery_data.json")

def create_placeholder_cover():
    """Create a placeholder cover if no images available"""
    # Create a simple gradient placeholder
    from PIL import ImageDraw
    
    img = Image.new('RGB', (1920, 1080), color=(253, 248, 243))
    draw = ImageDraw.Draw(img)
    
    # Add some decorative elements
    draw.ellipse([860, 480, 1060, 680], fill=(212, 165, 165))
    
    img.save(COVER_DIR / 'cover.jpg', 'JPEG', quality=90)
    img.save(COVER_DIR / 'recent.jpg', 'JPEG', quality=90)
    print(f"   ✓ 已创建默认封面占位图")

def main():
    print("=" * 50)
    print("📸 纪念日网站图片处理工具")
    print("=" * 50)
    
    # Setup directories
    setup_directories()
    
    # Process images
    timeline_data, gallery_items = process_images()
    
    # Create placeholder covers if needed
    if not list(COVER_DIR.glob('*.jpg')):
        create_placeholder_cover()
    
    print("\n" + "=" * 50)
    print("🎉 处理完成!")
    print("=" * 50)
    print("\n下一步:")
    print("1. 查看 images/timeline_data.json 和 images/gallery_data.json")
    print("2. 根据需要编辑 js/main.js 中的时间线内容")
    print("3. 添加背景音乐到 media/bgm.mp3")
    print("4. 运行本地服务器查看效果")

if __name__ == '__main__':
    main()
