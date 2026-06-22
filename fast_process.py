#!/usr/bin/env python3
"""
Fast Image Processing Script
- Processes images from picture_timeline
- Creates timeline and gallery data
"""

import os
import json
import shutil
from pathlib import Path
from PIL import Image

SOURCE_DIR = Path('/data/ourblog/picture_timeline')
TARGET_DIR = Path('/data/ourblog/images')
TIMELINE_DIR = TARGET_DIR / 'timeline'
GALLERY_DIR = TARGET_DIR / 'gallery'
COVER_DIR = TARGET_DIR / 'cover'

# Settings
MAX_SIZE = (1920, 1080)
THUMB_SIZE = (400, 400)

def create_placeholder(width, height, output_path, text=""):
    """Create gradient placeholder"""
    img = Image.new('RGB', (width, height), color=(253, 248, 243))
    draw = ImageDraw.Draw(img)
    # Simple circle
    cx, cy = width // 2, height // 2
    r = min(width, height) // 4
    draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=(212, 165, 165))
    img.save(output_path, 'JPEG', quality=85)

def setup():
    """Create directories"""
    for d in [TIMELINE_DIR, GALLERY_DIR, COVER_DIR]:
        d.mkdir(parents=True, exist_ok=True)
    print("✓ Directories created")

def get_date_info(folder_name):
    """Extract date and location from folder name"""
    import re
    match = re.search(r'(\d{4})年(\d{1,2})月(\d{1,2})日', folder_name)
    if match:
        y, m, d = match.groups()
        date = f"{y}-{m.zfill(2)}-{d.zfill(2)}"
        loc = folder_name.replace(f"{y}年{m}月{d}日", '').strip(' ,-')
        return date, loc
    return None, ""

def categorize(loc):
    """Categorize based on location"""
    loc_lower = loc.lower()
    if any(x in loc_lower for x in ['北京', '上海', '深圳', '广州', '杭州', '哈尔滨', '南宁', '惠州', '澳门', '市']):
        return 'travel'
    if any(x in loc_lower for x in ['春节', '国庆', '元旦', '圣诞', '520', '521']):
        return 'festival'
    return 'daily'

def process():
    """Process all images"""
    print("\n📷 Processing images...")
    
    folders = sorted([f for f in SOURCE_DIR.iterdir() if f.is_dir()], 
                    key=lambda x: get_date_info(x.name)[0] or '9999')
    
    timeline_data = []
    gallery_data = []
    cover_candidates = []
    
    for folder in folders:
        date, loc = get_date_info(folder.name)
        if not date:
            continue
        
        images = sorted([f for f in folder.iterdir() 
                       if f.suffix.lower() in ['.jpg', '.jpeg', '.png', '.webp']])
        
        if not images:
            continue
        
        cat = categorize(loc)
        
        # Cover candidates (early in timeline)
        if len(cover_candidates) < 3:
            cover_candidates.append(images[0])
        
        # Timeline: select up to 3 representative images
        selected = []
        if len(images) >= 3:
            selected = [images[0], images[len(images)//2], images[-1]]
        else:
            selected = images[:3]
        
        tl_images = []
        for i, src in enumerate(selected):
            dst = TIMELINE_DIR / f"{date}-{i+1}.jpg"
            try:
                with Image.open(src) as img:
                    if img.mode == 'RGBA':
                        img = img.convert('RGB')
                    img.thumbnail(MAX_SIZE, Image.Resampling.LANCZOS)
                    img.save(dst, 'JPEG', quality=85, optimize=True)
                    tl_images.append(f"timeline/{dst.name}")
            except Exception as e:
                print(f"  ⚠ Error: {e}")
        
        if tl_images:
            timeline_data.append({
                'date': date,
                'title': loc or date,
                'description': f"{loc}的美好时光" if loc else "值得纪念的一天",
                'images': tl_images,
                'category': cat
            })
        
        # Gallery: all images
        for src in images:
            dst = GALLERY_DIR / f"{date}_{src.name}"
            try:
                with Image.open(src) as img:
                    if img.mode == 'RGBA':
                        img = img.convert('RGB')
                    img.thumbnail(MAX_SIZE, Image.Resampling.LANCZOS)
                    img.save(dst, 'JPEG', quality=80, optimize=True)
                    gallery_data.append({
                        'src': f"gallery/{dst.name}",
                        'caption': loc or date,
                        'category': cat
                    })
            except:
                pass
        
        print(f"✓ {folder.name}: {len(images)} images")
    
    # Create covers
    print("\n🎨 Creating covers...")
    if cover_candidates:
        for i, src in enumerate(cover_candidates[:2]):
            dst = COVER_DIR / ('cover.jpg' if i == 0 else 'recent.jpg')
            try:
                with Image.open(src) as img:
                    if img.mode == 'RGBA':
                        img = img.convert('RGB')
                    img.thumbnail(MAX_SIZE, Image.Resampling.LANCZOS)
                    img.save(dst, 'JPEG', quality=90)
            except:
                create_placeholder(1920, 1080, dst)
    else:
        create_placeholder(1920, 1080, COVER_DIR / 'cover.jpg')
        create_placeholder(1920, 1080, COVER_DIR / 'recent.jpg')
    
    # Save data
    with open(TARGET_DIR / 'timeline_data.json', 'w', encoding='utf-8') as f:
        json.dump(timeline_data, f, ensure_ascii=False, indent=2)
    
    with open(TARGET_DIR / 'gallery_data.json', 'w', encoding='utf-8') as f:
        json.dump(gallery_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Done!")
    print(f"   Timeline events: {len(timeline_data)}")
    print(f"   Gallery images: {len(gallery_data)}")

if __name__ == '__main__':
    setup()
    process()
