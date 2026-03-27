#!/usr/bin/env python3
"""
內容生產管線 + SEO 優化整合
1. 生成文章內容
2. SEO 自動優化（meta description、關鍵字建議、標題結構檢查）
3. 生成 AI 圖片
4. 產出 SEO 報告
"""

import os
import sys
import json
import time
import subprocess
from datetime import datetime
from pathlib import Path

# 匯入 SEO 優化器
try:
    from seo_optimizer import SEOOptimizer
except ImportError:
    # 如果直接執行，使用相對匯入
    import importlib.util
    spec = importlib.util.spec_from_file_location("seo_optimizer", 
        Path(__file__).parent / "seo_optimizer.py")
    seo_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(seo_module)
    SEOOptimizer = seo_module.SEOOptimizer

# 文章模板（加入 SEO 元素）
ARTICLE_TEMPLATES = {
    "技術": {
        "template": """---
layout: post
title: "{title}"
date: {date}
excerpt: "{excerpt}"
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

**延伸閱讀：**
{related_links}
""",
        "prompt_style": "modern technology digital art, clean minimalist design, blue color scheme, futuristic, professional, high quality, 16:9 aspect ratio",
        "keywords": ["程式設計", "Python", "自動化", "教學", "技術"]
    },
    "生活": {
        "template": """---
layout: post
title: "{title}"
date: {date}
excerpt: "{excerpt}"
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

**延伸閱讀：**
{related_links}
""",
        "prompt_style": "warm lifestyle photography, bright natural lighting, cozy atmosphere, soft colors, inspiring, photorealistic, 16:9 aspect ratio",
        "keywords": ["生活技巧", "時間管理", "習慣養成", "心得分享"]
    },
    "健康": {
        "template": """---
layout: post
title: "{title}"
date: {date}
excerpt: "{excerpt}"
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

---

*你開始實踐這些習慣了嗎？歡迎在下方留言分享你的經驗！*

**延伸閱讀：**
{related_links}
""",
        "prompt_style": "fresh wellness photography, natural green tones, healthy lifestyle, peaceful, clean design, photorealistic, 16:9 aspect ratio",
        "keywords": ["健康生活", "運動習慣", "飲食健康", "養生"]
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
        "seo_requirements": {
            "excerpt_min_length": 120,
            "excerpt_max_length": 160,
            "intro_min_length": 80,
            "sections": 3,
            "total_length": 800,
            "tone": "friendly and informative",
            "include_keywords": ARTICLE_TEMPLATES.get(category, {}).get("keywords", [])
        }
    }


def generate_image_pollinations(prompt: str, output_path: str, 
                                width: int = 1280, height: int = 720) -> bool:
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


def generate_meta_description(content: str, max_length: int = 160) -> str:
    """生成 meta description（SEO 用）"""
    import re
    
    # 移除標題和 markdown 標記
    text = re.sub(r'^#+\s+', '', content, flags=re.MULTILINE)
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    text = re.sub(r'[*_`#]', '', text)
    text = text.replace('\n', ' ').strip()
    
    # 截斷到合適長度
    if len(text) <= max_length:
        return text
    
    # 找最後一個完整句子
    truncated = text[:max_length]
    last_period = max(
        truncated.rfind('。'),
        truncated.rfind('！'),
        truncated.rfind('？'),
        truncated.rfind('.')
    )
    
    if last_period > max_length * 0.5:
        return truncated[:last_period + 1]
    
    # 找最後一個完整詞
    last_space = truncated.rfind(' ')
    if last_space > max_length * 0.5:
        return truncated[:last_space] + '...'
    
    return truncated + '...'


def generate_related_links(category: str, current_title: str, all_articles: list) -> str:
    """生成相關文章連結（內部連結優化）"""
    links = []
    
    for article in all_articles:
        if article.get('title') == current_title:
            continue
        if article.get('categories', [])[0] == category:
            # 同分類文章優先
            links.insert(0, f"- [{article['title']}]({{{{ site.baseurl }}}}{article['url']})")
        elif len(links) < 3:
            links.append(f"- [{article['title']}]({{{{ site.baseurl }}}}{article['url']})")
    
    return '\n'.join(links[:3]) if links else "- [更多文章]({{ site.baseurl }}/)"


def run_seo_analysis(posts_dir: str, output_dir: str) -> dict:
    """執行 SEO 分析"""
    print("\n" + "=" * 60)
    print("📊 SEO 分析")
    print("=" * 60)
    
    optimizer = SEOOptimizer(posts_dir)
    results = optimizer.optimize_all_articles()
    
    # 儲存結果
    json_path = os.path.join(output_dir, "seo_analysis.json")
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\n✅ SEO 分析結果: {json_path}")
    
    # 生成報告
    report_path = os.path.join(output_dir, "seo_report.txt")
    optimizer.generate_report(results, report_path)
    
    return {
        "results": results,
        "avg_score": sum(r['seo_score'] for r in results) / len(results) if results else 0,
        "total_words": sum(r['word_count'] for r in results)
    }


def main():
    """主程式"""
    print("=" * 60)
    print("📝 內容生產管線 + SEO 優化")
    print("=" * 60)
    
    # 設定路徑
    repo_dir = Path(__file__).parent.parent
    posts_dir = repo_dir / "_posts"
    images_dir = repo_dir / "assets" / "images" / "featured"
    scripts_dir = repo_dir / "scripts"
    
    print(f"\n📂 Repository: {repo_dir}")
    print(f"📂 Posts: {posts_dir}")
    print(f"📂 Images: {images_dir}")
    
    # 步驟 1: 生成文章提示（含 SEO 要求）
    print("\n" + "=" * 60)
    print("步驟 1: 準備文章生成提示（含 SEO 優化要求）")
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
        print(f"   SEO 關鍵字: {', '.join(prompt_info['seo_requirements']['include_keywords'][:3])}")
        print(f"   字數要求: {prompt_info['seo_requirements']['total_length']}+ 字")
    
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
    
    # 步驟 3: SEO 分析現有文章
    print("\n" + "=" * 60)
    print("步驟 3: SEO 分析現有文章")
    print("=" * 60)
    
    seo_results = run_seo_analysis(str(posts_dir), str(scripts_dir))
    
    print(f"\n📈 SEO 總覽:")
    print(f"   平均分數: {seo_results['avg_score']:.1f}/100")
    print(f"   總字數: {seo_results['total_words']:,}")
    
    # 步驟 4: 輸出管線狀態
    print("\n" + "=" * 60)
    print("步驟 4: 輸出管線狀態")
    print("=" * 60)
    
    pipeline_state = {
        "timestamp": datetime.now().isoformat(),
        "articles": articles_to_create,
        "images": generated_images,
        "seo_summary": {
            "avg_score": seo_results['avg_score'],
            "total_words": seo_results['total_words'],
            "article_count": len(seo_results['results'])
        },
        "next_step": "fill_content"
    }
    
    state_file = scripts_dir / "pipeline_state.json"
    with open(state_file, 'w', encoding='utf-8') as f:
        json.dump(pipeline_state, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 管線狀態已儲存: {state_file}")
    
    # 輸出 SEO 改善建議
    print("\n" + "=" * 60)
    print("📋 SEO 改善建議")
    print("=" * 60)
    
    for result in seo_results['results']:
        if result['seo_score'] < 70:
            print(f"\n⚠️ {result['title']} ({result['seo_score']}/100)")
            for suggestion in result['suggestions']:
                print(f"   {suggestion}")
    
    print("\n" + "=" * 60)
    print("✅ 管線執行完成")
    print("=" * 60)
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
