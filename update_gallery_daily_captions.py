#!/usr/bin/env python3
"""补替换 gallery_data.json 里剩余的 daily caption"""

import json
from pathlib import Path

GALLERY_JSON = Path('/data/ourblog/images/gallery_data.json')

DAILY_CAPTIONS = [
    "今天的风很温柔，就像你在我身边",
    "有你在的日常，才是最好的时光",
    "不用特别去哪，有你就够了",
    "今天也是，被你偏爱的一天",
    "普通的星期二，因为有你而特别",
    "和你一起浪费的时间，才算数",
    "生活平淡，但有你发光的瞬间",
    "今天天气很好，适合想你",
]

KEEP_CAPTIONS = {
    "春节",
    "跨年夜",
    "元旦",
    "国庆节",
}

def is_old_daily_caption(caption: str) -> bool:
    if caption in KEEP_CAPTIONS:
        return False
    if caption in DAILY_CAPTIONS:
        return False
    if caption.startswith('和你在'):
        return False
    return True

def update_daily_captions():
    with open(GALLERY_JSON, 'r', encoding='utf-8') as f:
        gallery = json.load(f)

    updated = 0
    daily_counter = 0

    for item in gallery:
        if item.get('category') != 'daily':
            continue
        caption = item.get('caption', '')
        if not is_old_daily_caption(caption):
            continue
        item['caption'] = DAILY_CAPTIONS[daily_counter % len(DAILY_CAPTIONS)]
        daily_counter += 1
        updated += 1

    with open(GALLERY_JSON, 'w', encoding='utf-8') as f:
        json.dump(gallery, f, ensure_ascii=False, indent=2)

    print(f"✅ Updated {updated} daily captions")

if __name__ == '__main__':
    update_daily_captions()
