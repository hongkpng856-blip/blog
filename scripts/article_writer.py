#!/usr/bin/env python3
"""
Article Writer Agent - 文章生成 Sub-agent
==========================================
可被主 Agent 調用，輸入文章主題，輸出完整的 Markdown 文章檔案

使用方法:
    python article_writer.py "文章標題" --category 分類 [--output 目錄]

範例:
    python article_writer.py "如何提升工作效率" --category 生活
    python article_writer.py "Python 入門教學" --category 技術 --output ./output
"""
import os
import re
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime

# 根據分類自動推薦 featured image
IMAGE_SUGGESTIONS = {
    "技術": "tech-coding",
    "生活": "lifestyle-productivity", 
    "健康": "health-wellness",
    "投資": "finance-investment"
}

def detect_category(title):
    """從標題自動偵測分類"""
    title_lower = title.lower()
    if any(kw in title_lower for kw in ['python', '程式', '教學', 'code', 'api', 'git', '自動化', 'ai', '軟體', '技術']):
        return "技術"
    elif any(kw in title_lower for kw in ['投資', '理財', '股票', '比特幣', '基金', '資產']):
        return "投資"
    elif any(kw in title_lower for kw in ['健康', '睡眠', '運動', '飲食', '減肥', '養生']):
        return "健康"
    else:
        return "生活"

def generate_front_matter(title, category, date_str=None):
    """生成 YAML front matter"""
    date = date_str or datetime.now().strftime("%Y-%m-%d %H:%M:%S +0800")
    image_suggestion = IMAGE_SUGGESTIONS.get(category, "featured-default")
    
    # 清理標題中的特殊字符用於 filename
    safe_title = re.sub(r'[^\w\u4e00-\u9fff]', '-', title)
    safe_title = re.sub(r'-+', '-', safe_title).strip('-')
    
    front_matter = f"""---
layout: post
title: "{title}"
date: {date}
categories: {category}
author: Admin
description: "{title}。本文提供完整教學與實用建議，幫助您快速掌握核心概念並應用於日常生活中。"
keywords: "{category}, {title}, 教學, 指南"
image: /assets/images/{image_suggestion}.jpg
---"""
    return front_matter, safe_title

def generate_content(title, category):
    """生成文章主體內容 - 目標 500-800 字"""
    
    # 根據分類選擇不同的開頭模板
    intro_templates = {
        "技術": f"""在這個快速變化的時代，{title}已成為現代人必備的技能之一。無論你是剛踏入這個領域的新手，還是希望提升既有能力的進階學習者，本文都將帶你深入了解核心概念，並提供具體的實作方法。透過系統化的學習路徑，你能在短時間內掌握精髓，應用於工作或個人專案中。""",
        
        "生活": f"""你是否也對{title}感到困惑？在現代繁忙的生活中，我們常常忽略了一些重要的事情。別擔心，這篇文章將分享實用且可執行的方法，幫助你改善現狀、提升生活品質。這些建議經過許多人驗證，不需要大幅改變現有生活方式，就能看到明顯的效果。讓我們一起來探索如何讓生活變得更好吧。""",
        
        "健康": f"""良好的習慣是健康的基石，而{title}正是其中一個值得重視的領域。研究顯示，持續實踐正確的健康觀念，不僅能讓你的身體更強健，還能提升心理狀態和整體生活滿意度。更重要的是，這些方法不需要昂貴的設備或特殊的環境，每個人都可以從今天開始執行。讓我們一起來了解如何邁向更健康的生活吧。""",
        
        "投資": f"""理財是每個人都應該學習的重要課題，而{title}正是理財規劃中的關鍵一環。在這個充滿不確定性的時代，了解基本的投資原則變得尤為重要。無論你是想要開始投資的新手，還是希望優化現有投資組合的朋友，本文都將提供實用的建議和策略，幫助你做出更明智的財務決策。"""
    }
    
    intro = intro_templates.get(category, intro_templates["生活"])
    
    # 章節內容生成 - 擴展以達到 500-800 字
    sections = {
        "技術": [
            ("為什麼要學？", f"""在開始之前，讓我們先理解為什麼{title}如此重要。隨著科技發展，這些技能的需求與日俱增，不僅能提升工作效率，還能打開新的職業發展機會。

此外，{title}還能幫助你解決日常問題，提升邏輯思維能力。"""),

            ("核心概念與基礎", f"""要掌握{title}，首先需要理解幾個核心概念：

### 基礎原理
了解基本原理是學習的第一步。當你清楚知道每個環節的運作方式後，面對問題時就能更快找到解決方案。

### 常見應用場景
掌握這些概念後，你可以應用在多種場景中。

### 工具選擇
選擇適合的工具能大幅提升效率。"""),

            ("實作步驟", f"""以下是{title}的實作步驟，讓你能按部就班學習：

### 步驟一：環境準備
確保你的開發環境正確設定。安裝必要的軟體和依賴，這是順利學習的前提。

### 步驟二：基礎建置
從簡單的功能開始，逐步擴展。不要急於一次完成所有功能，先確保基礎運作正常。

### 步驟三：進階應用
熟悉基本操作後，嘗試進階功能。這時你可以挑戰更複雜的專案，鞏固所學。

### 步驟四：優化與除錯
持續優化程式碼，處理可能出現的問題。好的程式碼需要不斷打磨，這是成為高手的必經之路。"""),

            ("常見問題與解答", f"""在使用過程中，你可能會遇到以下問題：

### Q1：初學者該從哪裡開始？
從最小可行性產品開始，逐步迭代。不要害怕犯錯，每次錯誤都是學習的機會。

### Q2：遇到錯誤怎麼辦？
先仔細閱讀錯誤訊息，它們通常會指出問題所在。查閱官方文檔或尋求社群幫助也很有效。

### Q3：如何持續進步？
定期練習是關鍵。可以自己動手做小專案，實際應用所學知識。"""),

            ("結論", f"""透過本文的介紹，你應該對{title}有了更深入的了解。記住，持續練習和不斷學習是掌握任何技能的關鍵。剛開始可能會感到困難，但只要堅持下去，一定能看到進步。

建議你可以從今天就開始動手做一個小專案，在實作中學習是最有效的方式。祝你在學習的道路上順利前進！""")
        ],
        "生活": [
            ("為什麼這很重要？", f"""{title}對我們的日常生活有著深遠的影響。研究顯示，正確的方法能顯著提升生活品質和工作效率。很多人嘗試改變卻失敗，往往是因為方法不對或者目標設定過於模糊。

在開始之前，你需要先了解為什麼這件事值得投入時間和精力。當你真正理解其重要性時，動機會更強烈，執行起來也會更有決心。"""),

            ("具體實踐方法", f"""以下是實踐{title}的具體方法：

### 方法一：從小處著手
不要試圖一次改變太多，從可達成的小目標開始。成功的經驗會激勵你繼續前進，形成正向循環。

### 方法二：建立規律
將新行為變成日常習慣的一部分。重複執行21天以上，通常就能形成新的習慣。

### 方法三：創造支持環境
讓身邊的環境有利於新習慣的維持。例如想要健身的人，可以把運動服放在床邊，出門時就能看到。

### 方法四：持續追蹤與調整
記錄進展，適時調整策略。每週檢視自己的表現，找出需要改進的地方。"""),

            ("執行建議", f"""1. 設定明確的目標：具體、可測量的目標更容易達成
2. 分解成可執行的步驟：大目標拆成小步驟，降低心理負擔
3. 給自己適當的獎勵：達成里程碑時獎勵自己，保持動力
4. 保持耐心和恆心：改變需要時間，不要期望立即看到結果
5. 找到 accountability partner：找人互相監督，增加執行力"""),

            ("常見陷阱與避免方法", f"""在執行過程中，常見的陷阱包括：

### 過度完美主義
不要等到準備完美才開始，先完成再說。完成的都比完美的重要。

### 三分鐘熱度
一開始熱情滿滿，但很快就放棄。解決方法是建立支持系統和追蹤機制。

### 過度疲勞
不要一次改變太多，循序漸進才能持久。"""),

            ("總結", f"""{title}不是一蹴可幾的事，需要時間和持續的努力。但只要用對方法，每個人都能成功。希望這些建議能對你有所幫助，讓你的人生更加充實。記住，開始永遠不會太晚，今天就是開始的最佳時機！""")
        ],
        "健康": [
            ("科學背景", f"""關於{title}，科學研究提供了重要的見解。近年來，越來越多的研究證實了這些方法對健康的正面影響。良好的習慣不僅影響身體健康，也會影響心理狀態和整體生活品質。

研究顯示，持續實踐健康習慣的人，在壽命、生活滿意度、工作表現等各個面向都比其他人更好。這些發現讓我們更確定{title}的價值。"""),

            ("具體執行方法", f"""以下是實踐{title}的具體方法：

### 方法一：制定可行計畫
將大目標拆解成小步驟，更容易執行。例如，不要說「我要減肥」，而是「每天晚餐少吃半碗飯」。

### 方法二：建立支持系統
找到志同道合的夥伴互相支持。一個人走得快，但一群人走得遠。

### 方法三：傾聽身體信號
注意身體的反應，適時調整。每個人的身體狀況不同，要根據自己的情況彈性調整。

### 方法四：循序漸進
不要急於求成，慢慢來反而比較快。身体需要時間適應新的習慣。"""),

            ("執行時的注意事項", f"""執行時請注意以下事項：

### 避免過度
循序漸進，不要一次改變太多。過度的改變容易導致反彈，讓你更容易放棄。

### 保持彈性
遇到困難時，適時調整方法。計畫不可能完美，隨時保持彈性很重要。

### 尋求專業協助
必要時諮詢專業人士。如果遇到健康問題，記得尋求醫生或營養師的建議。

### 傾聽身體信號
身體會告訴你什麼時候需要休息，什麼時候可以更進一步。"""),

            ("長期維持的關鍵", f"""要長期維持健康習慣，關鍵在於：

首先，將新習慣與現有生活整合。不要創造額外的工作，而是讓新行為成為日常的一部分。

其次，設立合理的期望。改變不會在一夜之間發生，需要時間和耐心。

第三，慶祝小的成功。每次達成目標，給自己一點獎勵，這會強化正向行為。"""),

            ("結論", f"""健康的建立需要時間和耐心，但這絕對是值得的投資。透過本文介紹的方法，希望你能逐步建立起更好的習慣，享受健康帶來的美好生活。

記住，健康是所有美好事物的基礎。當你擁有健康，就有更多的能量和熱情去追求其他的目標。從今天開始，為自己的健康負責吧！""")
        ],
        "投資": [
            ("為什麼理財很重要？", f"""在開始投資之前，了解基礎概念非常重要。{title}是理財規劃中的關鍵環節，正確的理解能幫助你做出更好的財務決策。

很多人認為投資是有錢人的專利，但其實每個人都可以開始理財。關鍵在於及早開始，並持續學習。越早開始，你的資金就有越多時間透過複利增長。"""),

            ("基本概念與原則", f"""投資有其基本的原則和概念，了解這些是成功的基礎：

### 風險與報酬
高報酬通常伴隨高風險。了解自己的風險承受度，選擇適合自己的投資標的。

### 複利的力量
愛因斯坦曾說複利是世界第八大奇蹟。透過時間的力量，小額的投資也能累積成可觀的資產。

### 分散投資
不要把所有雞蛋放在同一個籃子裡。分散投資可以降低單一標的下跌的衝擊。"""),

            ("實用策略建議", f"""以下是關於{title}的策略建議：

### 短期策略
關注流動性和風險管理。短期投資需要更謹慎的風險控制。

### 中長期策略
注重複利效應和長期增長。時間是投資者最好的朋友。

### 定期投資
無論市場好壞，定期投入固定金額。這種「定時定額」的方法可以平均成本。

### 資產配置
根據年齡和風險承受度，決定股票、債券、現金等資產的比例。"""),

            ("風險管理與注意事項", f"""投資有其風險，請注意以下事項：

### 市場波動
市場有漲跌，做好心理準備。不要因為短期波動而驚慌失措。

### 分散投資
不要把所有資金放在同一個標的上。多元化是降低風險的有效方法。

### 持續學習
市場環境變化快，要持續進修。了解最新的市場趨勢和投資工具。

### 避免跟風
不要盲目跟隨他人的投資決定。每個人的情況不同，需要因時制宜。

### 設定停損
事先設定止損點，避免過度損失。"""),

            ("結論與行動建議", f"""總結來說，{title}需要謹慎規劃和持續學習。希望本文能幫助你建立正確的理財觀念，做出明智的投資決策。

建議從今天開始，先建立緊急儲蓄帳戶，然後再逐步開始投資。記住，理財是一場馬拉松，不是短跑。保持耐心，持續學習，你一定能達到財務自由的目標！""")
        ]
    }
    
    # 建構文章內容
    content_parts = [intro]
    
    category_sections = sections.get(category, sections["生活"])
    for section_title, section_content in category_sections:
        content_parts.append(f"## {section_title}\n\n{section_content}")
    
    return "\n\n".join(content_parts)

def count_chinese_chars(text):
    """計算中文字數"""
    return len(re.findall(r'[\u4e00-\u9fff]', text))

def generate_article(title, category=None, date_str=None):
    """生成完整文章"""
    # 自動偵測分類
    if not category:
        category = detect_category(title)
    
    # 生成 front matter
    front_matter, safe_title = generate_front_matter(title, category, date_str)
    
    # 生成內容
    content = generate_content(title, category)
    
    # 組合完整文章
    article = f"{front_matter}\n\n{content}"
    
    # 統計
    char_count = count_chinese_chars(content)
    
    return article, safe_title, char_count

def save_article(article, safe_title, output_dir=None):
    """儲存文章"""
    if output_dir:
        output_path = Path(output_dir)
    else:
        output_path = Path(__file__).parent.parent / "_posts"
    
    output_path.mkdir(parents=True, exist_ok=True)
    
    date = datetime.now().strftime("%Y-%m-%d")
    filename = f"{date}-{safe_title}.md"
    filepath = output_path / filename
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(article)
    
    return filepath

def main():
    parser = argparse.ArgumentParser(
        description='Article Writer Agent - 智慧文章生成器',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
範例:
  python article_writer.py "如何提升工作效率"
  python article_writer.py "Python 入門教學" --category 技術
  python article_writer.py "健康生活的五個習慣" --category 健康 --output ./articles
        """
    )
    parser.add_argument('title', help='文章標題')
    parser.add_argument('--category', '-c', 
                       choices=['技術', '生活', '健康', '投資'],
                       help='文章分類 (預設自動偵測)')
    parser.add_argument('--output', '-o', help='輸出目錄 (預設 _posts)')
    parser.add_argument('--date', '-d', help='日期 (格式: YYYY-MM-DD HH:MM:SS +0800)')
    parser.add_argument('--dry-run', action='store_true', 
                       help='僅顯示文章內容，不儲存檔案')
    
    args = parser.parse_args()
    
    # 生成文章
    article, safe_title, char_count = generate_article(args.title, args.category, args.date)
    
    # 輸出結果
    print(f"\n{'='*50}")
    print(f"📝 Article Writer Agent")
    print(f"{'='*50}")
    print(f"標題: {args.title}")
    print(f"分類: {args.category or detect_category(args.title)}")
    print(f"字數: {char_count} 字")
    print(f"{'='*50}\n")
    
    if args.dry_run:
        print(article)
    else:
        filepath = save_article(article, safe_title, args.output)
        print(f"\n✅ 文章已儲存: {filepath}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main() or 0)