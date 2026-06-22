#!/usr/bin/env python3
"""Fix missing images by creating placeholders from JSON metadata."""

import json
import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

PROJECT = Path('/data/ourblog')
IMAGES = PROJECT / 'images'
TIMELINE_DIR = IMAGES / 'timeline'
GALLERY_DIR = IMAGES / 'gallery'
COVER_DIR = IMAGES / 'cover'

for d in [TIMELINE_DIR, GALLERY_DIR, COVER_DIR]:
    d.mkdir(parents=True, exist_ok=True)


def make_placeholder(path: Path, text: str = '', size: tuple[int, int] = (800, 600), bg=(253, 248, 243), accent=(212, 165, 165)):
    if path.exists():
        return
    img = Image.new('RGB', size, color=bg)
    draw = ImageDraw.Draw(img)
    w, h = size
    cx, cy = w // 2, h // 2
    r = min(w, h) // 4
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=accent)
    if text:
        try:
            font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 28)
        except Exception:
            font = ImageFont.load_default()
        bbox = draw.textbbox((0, 0), text, font=font)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        draw.text((cx - tw / 2, cy - th / 2), text, fill=(120, 80, 80), font=font)
    img.save(path, 'JPEG', quality=85, optimize=True)


def main():
    tl_json = IMAGES / 'timeline_data.json'
    gal_json = IMAGES / 'gallery_data.json'

    timeline_items = []
    gallery_items = []

    if tl_json.exists():
        try:
            timeline_items = json.loads(tl_json.read_text(encoding='utf-8'))
        except Exception as e:
            print('Failed to read timeline_data.json:', e)

    if gal_json.exists():
        try:
            gallery_items = json.loads(gal_json.read_text(encoding='utf-8'))
        except Exception as e:
            print('Failed to read gallery_data.json:', e)

    created_timeline = 0
    for item in timeline_items:
        for img_rel in item.get('images', []):
            p = IMAGES / img_rel
            if not p.exists():
                make_placeholder(p, item.get('title') or item.get('date'), size=(800, 600))
                created_timeline += 1

    created_gallery = 0
    for item in gallery_items:
        p = IMAGES / item['src']
        if not p.exists():
            ext = p.suffix or '.png'
            if ext.lower() not in {'.jpg', '.jpeg', '.png', '.webp'}:
                p = p.with_suffix('.png')
            make_placeholder(p, item.get('caption', ''), size=(640, 640))
            created_gallery += 1

    for name in ['cover.jpg', 'recent.jpg']:
        make_placeholder(COVER_DIR / name, '', size=(1920, 1080))

    print(f'Created timeline placeholders: {created_timeline}')
    print(f'Created gallery placeholders: {created_gallery}')
    print('Done')


if __name__ == '__main__':
    main()
