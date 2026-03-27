#!/usr/bin/env python3
"""
智慧文章生成器 - SEO 優先的文章生成系統
- 前言不加標題（首頁顯示更乾淨）
- 前言必須吸引人（首頁只顯示前 60 字）
"""

import os
import re
import sys
import argparse
from pathlib import Path
from datetime import datetime

# SEO 模板配置
SEO_CONFIG = {
    "技術": {"min_words": 1000, "min_h2": 4, "structure": ["簡介", "核心概念", "實作步驟", "進階技巧", "常見問題", "結論"]},
    "生活": {"min_words": 800, "min_h2": 3, "structure": ["前言", "核心要點", "實踐方法", "案例分享", "總結"]},
    "健康": {"min_words": 900, "min_h2": 4, "structure": ["為什麼重要", "科學基礎", "具體方法", "執行建議", "注意事項", "總結"]},
    "投資": {"min_words": 1000, "min_h2": 4, "structure": ["背景", "核心概念", "策略分析", "風險評估", "實際建議", "結論"]}
}

POINTS_TEMPLATES = {
    "健康": [
        ("規律作息", "固定的作息時間能幫助身體建立穩定的生理時鐘。"),
        ("均衡飲食", "攝取多樣化的食物，確保營養均衡。"),
        ("適量運動", "每周至少 150 分鐘的中等強度運動。"),
        ("充足睡眠", "成人每天需要 7-9 小時的睡眠。"),
        ("壓力管理", "透過冥想、運動或興趣愛好來紓壓。")
    ],
    "生活": [
        ("建立明確目標", "設定具體、可衡量、可達成的目標。"),
        ("制定執行計畫", "拆解成具體的行動計畫，逐步實現。"),
        ("培養良好習慣", "建立正向習慣，讓成功成為自然。"),
        ("持續追蹤進度", "定期檢視進度，適時調整方向。"),
        ("保持彈性調整", "遇到障礙時能快速調整，不輕易放棄。")
    ],
    "技術": [
        ("理解基礎概念", "先掌握核心原理，再學進階應用。"),
        ("動手實作", "理論搭配實作，加深學習效果。"),
        ("善用工具", "選擇適合的工具，提升開發效率。"),
        ("持續學習", "技術不斷演進，保持學習心態。"),
        ("參與社群", "與同行交流，拓展視野。")
    ],
    "投資": [
        ("風險評估", "了解自己的風險承受度。"),
        ("分散配置", "不要把雞蛋放在同一個籃子裡。"),
        ("長期規劃", "避免短線操作，著眼長期收益。"),
        ("持續學習", "關注市場動態，不斷精進知識。"),
        ("紀律執行", "設定規則後嚴格遵守。")
    ]
}

def generate_five_points(category):
    """生成五個要點"""
    points = POINTS_TEMPLATES.get(category, POINTS_TEMPLATES["生活"])
    content = "以下是五個經過驗證的核心要點：\n\n"
    for i, (title, desc) in enumerate(points, 1):
        content += f"### {i}. {title}\n\n{desc}\n\n"
    return content.strip()

def plan_article(title, category):
    """規劃文章結構"""
    config = SEO_CONFIG.get(category, SEO_CONFIG["生活"])
    structure = config["structure"]
    
    keywords = extract_keywords(title, category)
    
    plan = {
        "title": title,
        "category": category,
        "structure": structure,
        "keywords": keywords,
        "config": config,
        "min_words": config["min_words"],
        "min_h2": config["min_h2"]
    }
    
    print(f"\n📊 文章規劃:")
    print(f"  標題: {title}")
    print(f"  分類: {category}")
    print(f"  結構: {' → '.join(structure)}")
    print(f"  關鍵字: {', '.join(keywords[:5])}")
    print(f"  目標字數: {config['min_words']}+")
    
    return plan

def extract_keywords(title, category):
    """從標題提取關鍵字"""
    words = []
    matches = re.findall(r'[\u4e00-\u9fff]{2,4}(?:生活|工作|健康|投資|技巧|習慣|方法|教學|指南)', title)
    words.extend(matches)
    words.extend(re.findall(r'(?:AI|Python|GitHub|Jekyll|API|SEO)', title))
    
    category_words = {
        "技術": ["教學", "步驟"],
        "生活": ["技巧", "方法"],
        "健康": ["健康", "習慣"],
        "投資": ["投資", "理財"]
    }
    words.extend(category_words.get(category, [])[:2])
    
    return list(set(words))[:10]

def generate_meta_description(title, category):
    """生成 meta description"""
    templates = {
        "技術": f"{title}。本文提供完整教學與實作步驟，幫助您快速掌握核心技術。",
        "生活": f"{title}。分享實用技巧與案例，讓您輕鬆應用於日常生活中。",
        "健康": f"{title}。根據科學研究，提供具體可執行的健康建議。",
        "投資": f"{title}。專業分析與風險評估，協助您做出明智的投資決策。"
    }
    return templates.get(category, f"{title}。深入探討相關主題，提供實用建議。")[:155]

def generate_section(section_title, plan):
    """生成章節內容 - 前言必須吸引人（問題、痛點、數據、承諾）"""
    title = plan["title"]
    category = plan["category"]
    
    # 前言類：使用吸引人的開頭（首頁只顯示前 60 字）
    sections = {
        "簡介": f"你是否也曾想過，為什麼有些人總能輕鬆掌握{title}？其實關鍵不在天賦，而在方法。本文將帶你從零開始，一步步掌握核心技巧，讓你也能快速上手、立刻應用。",
        
        "前言": f"你是否正面臨{title}的困擾？別擔心，你不是一個人。研究顯示，超過 70% 的人在這方面都有類似的問題。好消息是，只要掌握正確的方法，你也能在短時間內看到改變。讓我們一起來看看怎麼做。",
        
        "為什麼重要": f"你知道嗎？忽視{title}可能讓你付出比想像中更大的代價。研究指出，正確理解和執行這件事的人，不僅效率提升了 40%，生活品質也顯著改善。讓我們來看看為什麼這麼重要。",
        
        "背景": f"在探討{title}之前，我們需要先了解相關背景。這個主題涉及多個層面，需要從整體架構來理解。\n\n市場環境的變化、技術的發展，以及個人需求的演變，都影響著這個領域。",
        
        "核心概念": f"在深入探討之前，我們需要先理解幾個核心概念：\n\n### {plan['keywords'][0] if plan['keywords'] else '基礎概念'}\n\n這是{title}的核心基礎，理解後才能掌握後續內容。",
        
        "五個核心要點": generate_five_points(category),
        
        "具體方法": f"以下是執行{title}的具體方法：\n\n### 方法一：從小事開始\n\n不要試圖一次改變太多，從小目標開始更容易成功。\n\n### 方法二：建立規律\n\n固定時間執行，讓行為成為習慣。\n\n### 方法三：追蹤進度\n\n記錄執行狀況，適時調整策略。",
        
        "實作步驟": f"以下是{title}的實作步驟：\n\n### 步驟一：準備階段\n\n確保具備必要的資源和知識。\n\n### 步驟二：基礎建置\n\n建立基礎架構，這是後續工作的根基。\n\n### 步驟三：核心實作\n\n按照規劃逐步執行核心內容。\n\n### 步驟四：測試驗證\n\n完成後進行測試，確保結果符合預期。\n\n### 步驟五：優化改進\n\n根據測試結果進行優化。",
        
        "實踐方法": f"理論需要實踐來驗證。以下是將{title}轉化為行動的方法：\n\n### 從小事開始\n\n不要試圖一次改變太多，循序漸進才是長久之計。\n\n### 建立支持系統\n\n找到志同道合的夥伴，互相支持和鼓勵。\n\n### 定期反思調整\n\n每周檢視進度，調整不適合的做法。",
        
        "策略分析": f"在執行{title}時，需要考慮以下策略：\n\n### 短期策略\n\n快速見效的方法，建立信心和動力。\n\n### 中期策略\n\n穩定發展的規劃，確保持續進步。\n\n### 長期策略\n\n可持續的方案，支持長遠目標。",
        
        "進階技巧": f"掌握基礎後，以下進階技巧能讓您更上層樓：\n\n### 技巧一：自動化\n\n將重複性工作自動化，節省時間和精力。\n\n### 技巧二：整合工具\n\n善用不同工具的整合功能，提升整體效率。\n\n### 技巧三：持續優化\n\n定期檢視並優化流程，保持最佳狀態。",
        
        "案例分享": f"以下是一些成功案例：\n\n### 案例一：小明的轉變\n\n透過持續執行{title}的方法，小明在三個月內看到顯著改變。\n\n### 案例二：團隊的成功\n\n一個小團隊採用這些方法後，整體效率提升了 30%。",
        
        "執行建議": f"以下是{title}的執行建議：\n\n1. **設定明確目標**：知道要達成什麼\n2. **分解成小步驟**：降低執行難度\n3. **建立追蹤機制**：確保持續執行\n4. **適時獎勵自己**：維持動力",
        
        "注意事項": f"在執行{title}時，請注意以下事項：\n\n### 避免過度\n\n循序漸進，不要一次改變太多。\n\n### 保持彈性\n\n遇到困難時，適時調整方法。\n\n### 尋求支持\n\n必要時尋求專業協助。",
        
        "風險評估": f"在進行{title}相關活動時，需要注意以下風險：\n\n### 風險一：市場波動\n\n外部環境變化可能影響結果。\n\n### 風險二：執行偏差\n\n方法不正確可能導致效果不佳。\n\n### 風險三：過度投入\n\n資源分配不當可能造成損失。",
        
        "常見問題": f"以下關於{title}的常見問題：\n\n### Q1：多久能看到效果？\n\n因人而異，通常需要持續執行 2-4 周。\n\n### Q2：需要哪些準備？\n\n基本知識和正確的心態。\n\n### Q3：遇到困難怎麼辦？\n\n尋求社群支持或專業協助。",
        
        "實際建議": f"根據{title}的特點，以下是實際建議：\n\n1. **從小處著手**：降低入門門檻\n2. **持續追蹤**：確保執行到位\n3. **適時調整**：根據結果優化\n4. **長期規劃**：建立可持續的方案",
        
        "科學基礎": f"關於科學基礎的內容將在此呈現。",
        
        "總結": f"{title}是一個值得深入學習的主題。透過本文的介紹，您應該已經掌握了核心概念和實踐方法。\n\n重點回顧：\n\n1. 理解基礎概念是成功的第一步\n2. 實踐比理論更重要\n3. 持續執行才能看到效果\n\n希望本文對您有所幫助，歡迎分享您的經驗和心得！",
        
        "結論": f"總結來說，{title}需要系統性的方法和持續的執行。透過本文提供的框架，您可以更有信心地開始行動。\n\n記住：知識只是起點，行動才能帶來改變。祝您成功！"
    }
    
    return sections.get(section_title, f"關於{section_title}的內容將在此呈現。")

def generate_article(plan):
    """生成完整文章"""
    print(f"\n📝 開始生成文章...")
    
    # Front matter
    date = datetime.now().strftime("%Y-%m-%d")
    front_matter = f"""---
layout: post
title: "{plan['title']}"
date: {date}
categories: {plan['category']}
author: Admin
description: "{generate_meta_description(plan['title'], plan['category'])}"
keywords: "{', '.join(plan['keywords'][:5])}"
image: /assets/images/featured/{plan['title']}.jpg
---"""
    
    # 生成各章節（第一個段落不加標題）
    sections = []
    first_section = plan["structure"][0] if plan["structure"] else None
    
    for section_title in plan["structure"]:
        if section_title == first_section:
            # 前言不加標題，直接輸出內容
            sections.append(generate_section(section_title, plan))
        else:
            sections.append(f"## {section_title}\n\n{generate_section(section_title, plan)}")
        print(f"  ✅ {section_title}")
    
    article = front_matter + "\n\n" + "\n\n".join(sections)
    
    # 統計
    word_count = len(re.findall(r'[\u4e00-\u9fff]', article))
    h2_count = len(re.findall(r'^## ', article, re.MULTILINE))
    
    print(f"\n📊 文章統計:")
    print(f"  字數: {word_count} (目標: {plan['min_words']}+)")
    print(f"  H2 標題: {h2_count} (目標: {plan['min_h2']}+)")
    
    return article

def save_article(article, title, output_dir=None):
    """儲存文章"""
    if output_dir:
        output_path = Path(output_dir)
    else:
        output_path = Path(__file__).parent.parent / "_posts"
    
    output_path.mkdir(parents=True, exist_ok=True)
    
    date = datetime.now().strftime("%Y-%m-%d")
    filename = f"{date}-{title}.md"
    filepath = output_path / filename
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(article)
    
    print(f"\n✅ 文章已儲存: {filepath}")
    return filepath

def main():
    parser = argparse.ArgumentParser(description='智慧文章生成器')
    parser.add_argument('title', help='文章標題')
    parser.add_argument('category', choices=['技術', '生活', '健康', '投資'], help='文章分類')
    parser.add_argument('--output', '-o', help='輸出目錄')
    
    args = parser.parse_args()
    
    plan = plan_article(args.title, args.category)
    article = generate_article(plan)
    save_article(article, args.title, args.output)

if __name__ == "__main__":
    main()
