#!/usr/bin/env python3
"""批量替换 gallery_data.json 的 caption"""

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

TRAVEL_CAPTIONS = {
    "南宁市": "南宁的夜风，吹不散想你的念头",
    "深圳市": "深圳的灯火，不及你眼里的光",
    "惠州市": "惠州的慢时光，和你刚好匹配",
    "哈尔滨市": "哈尔滨的雪，不如你靠近时的温度",
    "北京市": "北京的秋天，和你一起走才完整",
    "广州市": "广州的烟火气，最想和你一起闻",
    "澳门特别行政区": "澳门的霓虹，都不如你好看",
    "珠海市": "珠海的海风，捎来了想你的讯号",
    "杭州市": "杭州的烟雨，都比不上你低头微笑",
    "南京市": "南京的梧桐，藏不住想你的心事",
}

KEEP_CAPTIONS = {
    "春节",
    "跨年夜",
    "元旦",
    "国庆节",
}

OLD_DATE_PREFIXES = ("202",)

def update_captions():
    with open(GALLERY_JSON, 'r', encoding='utf-8') as f:
        gallery = json.load(f)

    daily_counter = 0
    travel_counter = {city: 0 for city in TRAVEL_CAPTIONS.keys()}
    skipped = 0

    for item in gallery:
        caption = item.get('caption', '')
        category = item.get('category', '')

        if caption in KEEP_CAPTIONS:
            skipped += 1
            continue
        if caption in DAILY_CAPTIONS:
            skipped += 1
            continue
        if caption in TRAVEL_CAPTIONS.values():
            skipped += 1
            continue

        if caption in TRAVEL_CAPTIONS:
            item['caption'] = TRAVEL_CAPTIONS[caption]
            travel_counter[caption] += 1
        elif category == 'daily':
            if caption.startswith(OLD_DATE_PREFIXES) or caption == '家':
                item['caption'] = DAILY_CAPTIONS[daily_counter % len(DAILY_CAPTIONS)]
                daily_counter += 1
            else:
                skipped += 1
        else:
            skipped += 1

    with open(GALLERY_JSON, 'w', encoding='utf-8') as f:
        json.dump(gallery, f, ensure_ascii=False, indent=2)

    print(f"✅ Updated {daily_counter} daily captions")
    print(f"   Travel counts: { {k: v for k, v in travel_counter.items() if v > 0} }")
    print(f"   Skipped: {skipped}")

if __name__ == '__main__':
    update_captions()
