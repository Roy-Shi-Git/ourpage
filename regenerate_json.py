#!/usr/bin/env python3
"""Regenerate JSON data files from actual image files"""

import json
from pathlib import Path

GALLERY_DIR = Path('/data/ourblog/images/gallery')
TIMELINE_DIR = Path('/data/ourblog/images/timeline')
TIMELINE_JSON = Path('/data/ourblog/images/timeline_data.json')
GALLERY_JSON = Path('/data/ourblog/images/gallery_data.json')

def regenerate_data():
    # Get all timeline images
    timeline_files = sorted(TIMELINE_DIR.glob('*.jpg'))
    print(f"Timeline images: {len(timeline_files)}")
    
    # Get all gallery images
    gallery_files = sorted(GALLERY_DIR.glob('*.png'))
    print(f"Gallery images: {len(gallery_files)}")
    
    # Build timeline data from actual files
    timeline_data = {}
    for f in timeline_files:
        # Parse date from filename: 2021-02-12-1.jpg
        parts = f.stem.split('-')
        if len(parts) >= 3:
            date = '-'.join(parts[:3])
            if date not in timeline_data:
                timeline_data[date] = []
            timeline_data[date].append(f'timeline/{f.name}')
    
    # Convert to list format
    events = []
    for date, images in sorted(timeline_data.items()):
        year, month, day = date.split('-')
        events.append({
            'date': date,
            'title': date,
            'description': '值得纪念的一天',
            'images': images,
            'category': 'daily'
        })
    
    # Save timeline data
    with open(TIMELINE_JSON, 'w', encoding='utf-8') as f:
        json.dump(events, f, ensure_ascii=False, indent=2)
    print(f"Saved timeline_data.json with {len(events)} events")
    
    # Build gallery data from actual files
    gallery_data = []
    for f in gallery_files:
        # Parse location from original folder structure
        parts = f.stem.split('_')
        loc = parts[1] if len(parts) > 1 else f.stem[:10]
        
        # Categorize
        loc_lower = loc.lower()
        if any(x in loc_lower for x in ['北京', '上海', '深圳', '广州', '杭州', '哈尔滨', '南宁', '惠州', '澳门', '珠海', '南京', '市']):
            cat = 'travel'
        elif any(x in loc_lower for x in ['春节', '国庆', '元旦', '圣诞', '跨年']):
            cat = 'festival'
        else:
            cat = 'daily'
        
        gallery_data.append({
            'src': f'gallery/{f.name}',
            'caption': loc,
            'category': cat
        })
    
    # Save gallery data
    with open(GALLERY_JSON, 'w', encoding='utf-8') as f:
        json.dump(gallery_data, f, ensure_ascii=False, indent=2)
    print(f"Saved gallery_data.json with {len(gallery_data)} items")

if __name__ == '__main__':
    regenerate_data()
    print("Done!")
