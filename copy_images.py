#!/usr/bin/env python3
"""
Simple image copy script - no processing, just copy
"""

import os
import json
import shutil
from pathlib import Path
from datetime import datetime
import re

SOURCE_DIR = Path('/data/ourblog/picture_timeline')
TARGET_DIR = Path('/data/ourblog/images')
TIMELINE_DIR = TARGET_DIR / 'timeline'
GALLERY_DIR = TARGET_DIR / 'gallery'
COVER_DIR = TARGET_DIR / 'cover'

def get_date_info(folder_name):
    """Extract date from folder name"""
    match = re.search(r'(\d{4})年(\d{1,2})月(\d{1,2})日', folder_name)
    if match:
        y, m, d = match.groups()
        return f"{y}-{m.zfill(2)}-{d.zfill(2)}", folder_name.replace(f"{y}年{m}月{d}日", '').strip(' ,-')
    return None, ""

def categorize(loc):
    loc_lower = loc.lower()
    if any(x in loc_lower for x in ['北京', '上海', '深圳', '广州', '杭州', '哈尔滨', '南宁', '惠州', '澳门', '市', '国庆', '元旦']):
        return 'travel' if '节' not in loc_lower else 'festival'
    if any(x in loc_lower for x in ['春节', '圣诞', '520', '521', '国庆', '元旦']):
        return 'festival'
    return 'daily'

def main():
    print("Copying images...")
    
    # Create dirs
    for d in [TIMELINE_DIR, GALLERY_DIR, COVER_DIR]:
        d.mkdir(parents=True, exist_ok=True)
    
    folders = sorted([f for f in SOURCE_DIR.iterdir() if f.is_dir()], 
                    key=lambda x: get_date_info(x.name)[0] or '9999')
    
    timeline_data = []
    gallery_data = []
    cover_candidates = []
    tl_count = 0
    gal_count = 0
    
    for folder in folders:
        date, loc = get_date_info(folder.name)
        if not date:
            continue
        
        images = sorted([f for f in folder.iterdir() 
                       if f.suffix.lower() in ['.jpg', '.jpeg', '.png', '.webp']])
        
        if not images:
            continue
        
        cat = categorize(loc)
        
        # Cover candidates
        if len(cover_candidates) < 3:
            cover_candidates.append(images[0])
        
        # Timeline: select up to 3
        selected = images[:3] if len(images) < 3 else [images[0], images[len(images)//2], images[-1]]
        
        tl_images = []
        for i, src in enumerate(selected):
            dst = TIMELINE_DIR / f"{date}-{i+1}{src.suffix}"
            shutil.copy2(src, dst)
            tl_images.append(f"timeline/{dst.name}")
            tl_count += 1
        
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
            shutil.copy2(src, dst)
            gallery_data.append({
                'src': f"gallery/{dst.name}",
                'caption': loc or date,
                'category': cat
            })
            gal_count += 1
        
        print(f"✓ {folder.name}")
    
    # Copy covers
    print("\nCopying covers...")
    for i, src in enumerate(cover_candidates[:2]):
        dst = COVER_DIR / ('cover.jpg' if i == 0 else 'recent.jpg')
        shutil.copy2(src, dst)
    
    # Save data
    with open(TARGET_DIR / 'timeline_data.json', 'w', encoding='utf-8') as f:
        json.dump(timeline_data, f, ensure_ascii=False, indent=2)
    
    with open(TARGET_DIR / 'gallery_data.json', 'w', encoding='utf-8') as f:
        json.dump(gallery_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Done!")
    print(f"   Timeline: {tl_count} images, {len(timeline_data)} events")
    print(f"   Gallery: {gal_count} images")

if __name__ == '__main__':
    main()
