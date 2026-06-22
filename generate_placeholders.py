#!/usr/bin/env python3
"""
Generate placeholder images and timeline/gallery data
"""

import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# Setup paths
TARGET_DIR = Path('/data/ourblog/images')
COVER_DIR = TARGET_DIR / 'cover'
TIMELINE_DIR = TARGET_DIR / 'timeline'

def create_placeholder_image(width, height, text, output_path, colors=('#F5EDE6', '#D4A5A5')):
    """Create a simple gradient placeholder image"""
    img = Image.new('RGB', (width, height), color=colors[0])
    draw = ImageDraw.Draw(img)
    
    # Add gradient effect
    for i in range(height):
        alpha = int(255 * (i / height) * 0.3)
        r = int(int(colors[1][1:3], 16) + (255 - int(colors[1][1:3], 16)) * (i / height))
        g = int(int(colors[1][3:5], 16) + (255 - int(colors[1][3:5], 16)) * (i / height))
        b = int(int(colors[1][5:7], 16) + (255 - int(colors[1][5:7], 16)) * (i / height))
        draw.line([(0, i), (width, i)], fill=(r, g, b))
    
    # Add decorative circle
    center_x, center_y = width // 2, height // 2
    radius = min(width, height) // 4
    draw.ellipse(
        [center_x - radius, center_y - radius, center_x + radius, center_y + radius],
        fill=colors[1]
    )
    
    img.save(output_path, 'JPEG', quality=90)
    print(f"Created: {output_path}")

def generate_timeline_data():
    """Generate timeline data from processed images"""
    # Get all timeline images grouped by date
    timeline_images = {}
    
    for img_path in TIMELINE_DIR.glob('*.jpg'):
        # Parse date from filename (format: YYYY-MM-DD-N.jpg)
        parts = img_path.stem.split('-')
        if len(parts) >= 3:
            date = '-'.join(parts[:3])
            if date not in timeline_images:
                timeline_images[date] = []
            timeline_images[date].append(f"timeline/{img_path.name}")
    
    # Sort by date
    sorted_dates = sorted(timeline_images.keys())
    
    # Create timeline events
    events = []
    for date in sorted_dates:
        images = timeline_images[date]
        year, month, day = date.split('-')
        formatted_date = f"{year}年{int(month)}月{int(day)}日"
        
        # Parse location from folder name if available
        location = ""
        category = "daily"
        
        event = {
            'date': date,
            'title': f"{formatted_date}",
            'description': f"这一天值得纪念。",
            'images': images,
            'category': category
        }
        events.append(event)
    
    # Save to JSON
    with open(TARGET_DIR / 'timeline_data.json', 'w', encoding='utf-8') as f:
        json.dump(events, f, ensure_ascii=False, indent=2)
    
    print(f"Generated timeline_data.json with {len(events)} events")
    return events

def generate_gallery_data():
    """Generate gallery data from all images"""
    gallery_items = []
    
    # Timeline images
    for img_path in TIMELINE_DIR.glob('*.jpg'):
        gallery_items.append({
            'src': f"timeline/{img_path.name}",
            'caption': img_path.stem,
            'category': 'daily'
        })
    
    # Sort by filename
    gallery_items.sort(key=lambda x: x['src'])
    
    # Save to JSON
    with open(TARGET_DIR / 'gallery_data.json', 'w', encoding='utf-8') as f:
        json.dump(gallery_items, f, ensure_ascii=False, indent=2)
    
    print(f"Generated gallery_data.json with {len(gallery_items)} items")
    return gallery_items

def main():
    print("Creating placeholder assets...")
    
    # Create cover images
    create_placeholder_image(1920, 1080, "封面", COVER_DIR / 'cover.jpg')
    create_placeholder_image(1920, 1080, "近照", COVER_DIR / 'recent.jpg')
    
    # Generate data files
    generate_timeline_data()
    generate_gallery_data()
    
    print("\nDone!")

if __name__ == '__main__':
    main()
