#!/usr/bin/env python3
"""
內容生產管線
1. 生成 3 篇文章
2. 為每篇文章生成 AI 圖片
3. 更新到網站
"""

import os
import sys
import json
import time
import subprocess
from datetime import datetime
from pathlib import Path

# 文章模板
ARTICLE_TEMPLATES = {
    "技術": {
        "template": """---
layout: post
title: "{title}"
date: {date}
categories: [技術]
tags: [{tags}]
image: /assets/images/featured/{image_filename}
---

{intro}

## {section1_title}

{section1_content}

## {section2_title}

{section2_content}

## {section3_title}

{section3_content}

## 結語

{conclusion}

---
*你對這個主題有什麼看法？歡迎在下方留言分享！*
""",
        "prompt_style": "modern technology digital art, clean minimalist design, blue color scheme, futuristic, professional, high quality, 16:9 aspect ratio"
    },
    "生活": {
        "template": """---
layout: post
title: "{title}"
date: {date}
categories: [生活]
tags: [{tags}]
image: /assets/images/featured/{image_filename}
---

{intro}

## {section1_title}

{section1_content}

## {section2_title}

{section2_content}

## {section3_title}

{section3_content}

## 結語

{conclusion}

---
*你有什麼心得或建議嗎？歡迎在下方留言分享！*
""",
        "prompt_style": "warm lifestyle photography, bright natural lighting, cozy atmosphere, soft colors, inspiring, photorealistic, 16:9 aspect ratio"
    },
    "健康": {
        "template": """---
layout: post
title: "{title}"
date: {date}
categories: [健康]
tags: [{tags}]
image: /assets/images/featured/{image_filename}
---

{intro}

### 1. {habit1}

{habit1_content}

### 2. {habit2}

{habit2_content}

### 3. {habit3}

{habit3_content}

### 4. {habit4}

{habit4_content}

### 5. {habit5}

{habit5_content}

---

## 結語

{conclusion}

> 「{quote}」
""",
        "prompt_style": "fresh wellness photography, natural green tones, healthy lifestyle, peaceful, clean design, photorealistic, 16:9 aspect ratio"
    }
}

def generate_article_prompt(category: str, topic_hints: list = None) -> dict:
    """生成文章內容提示（給 LLM 用）"""
    
    topic_suggestions = {
        "技術": [
            "Python 程式設計入門指南",
            "如何使用 Git 進行版本控制",
            "資料科學基礎概念解析",
            "網頁開發必學的 CSS 技巧",
            "雲端服務入門：AWS vs GCP vs Azure"
        ],
        "生活": [
            "居家收納的五大技巧",
            "如何培養閱讀習慣",
            "時間管理的實用方法",
            "如何建立良好的早晨習慣",
            "理財規劃的入門指南"
        ],
        "健康": [
            "改善睡眠品質的七個方法",
            "辦公室伸展運動指南",
            "如何建立規律運動習慣",
            "健康飲食的基本原則",
            "心理健康自我照護指南"
        ]
    }
    
    return {
        "category": category,
        "suggested_topics": topic_suggestions.get(category, []),
        "requirements": {
            "intro_min_length": 60,  # 前言至少 60 字
            "sections": 3,
            "total_length": 800,
            "tone": "friendly and informative"
        }
    }

def generate_image_pollinations(prompt: str, output_path: str, width: int = 1280, height: int = 720) -> bool:
    """使用 Pollinations API 生成圖片"""
    import urllib.parse
    import urllib.request
    import random
    
    encoded_prompt = urllib.parse.quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={width}&height={height}&nologo=true&seed={random.randint(1000,99999)}"
    
    print(f"🎨 生成圖片中...")
    print(f"📝 Prompt: {prompt[:80]}...")
    
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0',
            'Accept': 'image/png,image/*'
        })
        
        with urllib.request.urlopen(req, timeout=180) as response:
            image_data = response.read()
            
            if len(image_data) < 1000:
                print(f"❌ 圖片太小 ({len(image_data)} bytes)")
                return False
            
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            with open(output_path, 'wb') as f:
                f.write(image_data)
            
            print(f"✅ 圖片已儲存: {output_path}")
            print(f"📊 檔案大小: {len(image_data) / 1024:.1f} KB")
            return True
            
    except Exception as e:
        print(f"❌ 生成失敗: {e}")
        return False

def create_article_file(title: str, category: str, content: str, posts_dir: str) -> str:
    """建立文章檔案"""
    import re
    
    # 生成檔名
    date_str = datetime.now().strftime("%Y-%m-%d")
    safe_title = re.sub(r'[^\w\s-]', '', title)
    safe_title = re.sub(r'[\s]+', '-', safe_title)
    filename = f"{date_str}-{safe_title}.md"
    filepath = os.path.join(posts_dir, filename)
    
    # 確保目錄存在
    os.makedirs(posts_dir, exist_ok=True)
    
    # 寫入檔案
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ 文章已建立: {filepath}")
    return filename

def main():
    """主程式"""
    print("=" * 60)
    print("📝 內容生產管線")
    print("=" * 60)
    
    # 設定路徑
    repo_dir = Path(__file__).parent.parent
    posts_dir = repo_dir / "_posts"
    images_dir = repo_dir / "assets" / "images" / "featured"
    
    print(f"\n📂 Repository: {repo_dir}")
    print(f"📂 Posts: {posts_dir}")
    print(f"📂 Images: {images_dir}")
    
    # 步驟 1: 生成文章提示
    print("\n" + "=" * 60)
    print("步驟 1: 準備文章生成提示")
    print("=" * 60)
    
    articles_to_create = [
        {"category": "技術", "title": "Python 自動化入門：用程式碼簡化你的生活"},
        {"category": "生活", "title": "極簡主義生活：如何用更少擁有更多"},
        {"category": "健康", "title": "提升免疫力的五個日常習慣"}
    ]
    
    for article in articles_to_create:
        prompt_info = generate_article_prompt(article["category"])
        print(f"\n📌 {article['title']} ({article['category']})")
        print(f"   建議主題: {', '.join(prompt_info['suggested_topics'][:3])}")
    
    # 步驟 2: 生成 AI 圖片
    print("\n" + "=" * 60)
    print("步驟 2: 生成 AI 圖片")
    print("=" * 60)
    
    image_style_map = {
        "技術": "modern technology concept art, programming code, automation, Python logo, futuristic digital art, blue and purple gradient, clean minimalist design, high quality, 16:9 aspect ratio",
        "生活": "minimalist lifestyle, clean white space, simple living, zen atmosphere, natural light, soft colors, inspiring photography, 16:9 aspect ratio",
        "健康": "healthy immune system, fresh fruits and vegetables, wellness, natural green tones, vibrant energy, clean design, photorealistic, 16:9 aspect ratio"
    }
    
    generated_images = []
    for i, article in enumerate(articles_to_create, 1):
        print(f"\n[{i}/3] 生成圖片: {article['title']}")
        print("-" * 40)
        
        prompt = image_style_map[article["category"]]
        safe_title = article["title"].replace(" ", "-").replace("/", "-")
        output_path = str(images_dir / f"{safe_title}.png")
        
        success = generate_image_pollinations(prompt, output_path)
        
        generated_images.append({
            "title": article["title"],
            "category": article["category"],
            "image_path": output_path if success else None,
            "image_filename": f"{safe_title}.png" if success else None
        })
        
        if i < len(articles_to_create):
            print("⏳ 等待 3 秒...")
            time.sleep(3)
    
    # 步驟 3: 輸出文章模板
    print("\n" + "=" * 60)
    print("步驟 3: 文章模板已準備")
    print("=" * 60)
    
    for article in generated_images:
        print(f"\n📝 {article['title']}")
        if article['image_filename']:
            print(f"   🖼️ 圖片: {article['image_filename']}")
        else:
            print(f"   ⚠️ 圖片生成失敗")
    
    print("\n" + "=" * 60)
    print("📋 下一步：使用 LLM 填充文章內容")
    print("=" * 60)
    
    # 輸出 JSON 供 sub-agent 使用
    pipeline_state = {
        "timestamp": datetime.now().isoformat(),
        "articles": articles_to_create,
        "images": generated_images,
        "next_step": "fill_content"
    }
    
    state_file = repo_dir / "scripts" / "pipeline_state.json"
    with open(state_file, 'w', encoding='utf-8') as f:
        json.dump(pipeline_state, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 管線狀態已儲存: {state_file}")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
