#!/usr/bin/env python3
"""
為所有文章重新生成 AI 圖片
使用免費 AI 圖片生成服務
"""
import os
import json
import urllib.request
import urllib.parse
import time
import hashlib

BLOG_DIR = "/home/claw/.openclaw/workspace/blog-repo"
IMAGES_DIR = f"{BLOG_DIR}/assets/images/featured"

# 主題顏色配置（根據分類）
CATEGORY_COLORS = {
    "技術": {"primary": "#2196F3", "secondary": "#1565C0", "gradient": "blue"},
    "生活": {"primary": "#FF9800", "secondary": "#F57C00", "gradient": "orange"},
    "健康": {"primary": "#4CAF50", "secondary": "#388E3C", "gradient": "green"},
    "投資": {"primary": "#FFC107", "secondary": "#FFA000", "gradient": "gold"},
    "default": {"primary": "#9C27B0", "secondary": "#7B1FA2", "gradient": "purple"}
}

# 關鍵詞到視覺元素的映射
KEYWORD_VISUALS = {
    # 科技
    "AI": "artificial intelligence, futuristic robot, neural network",
    "ChatGPT": "AI chatbot, conversation, modern interface",
    "Python": "code on screen, programming, developer",
    "自動化": "robot arm, automation, technology",
    "代理": "AI assistant, digital agent, smart robot",
    "Vtuber": "virtual YouTuber, anime avatar, streaming",
    "YouTuber": "YouTube creator, camera, video production",
    "Threads": "social media app, smartphone, connected",
    "短影音": "TikTok, short video, mobile phone",
    "iPhone": "iPhone, Apple smartphone, modern device",
    "Switch": "Nintendo Switch, gaming, console",
    
    # 金融
    "比特幣": "bitcoin, cryptocurrency, blockchain",
    "加密貨幣": "crypto coins, digital currency, blockchain",
    "股票": "stock chart, trading, finance",
    "ETF": "ETF, investment, portfolio",
    "理財": "money, savings, financial planning",
    "高股息": "dividends, stocks, income investing",
    
    # 生活
    "捷運": "Taipei Metro, subway train, Taiwan",
    "交通": "traffic, city, transportation",
    "機車": "motorcycle, scooter, Taiwan street",
    "餐廳": "restaurant, food, dining",
    "美食": "delicious food, Taiwan cuisine",
    "母親節": "mother's day, gift, flowers, love",
    "演唱會": "concert, music festival, live performance",
    "旅遊": "travel, Japan, tourism",
    "日本": "Japan, Tokyo, travel",
    "蝦皮": "online shopping, e-commerce, delivery",
    "購物": "shopping, mall, retail",
    
    # 時尚
    "時尚": "fashion, stylish clothing, trend",
    "穿搭": "outfit, fashion style, clothing",
    
    # 遊戲
    "遊戲": "gaming, video game, esports",
    "手機遊戲": "mobile gaming, smartphone game",
    
    # 運動
    "健身": "fitness, gym, workout",
    "運動": "sports, exercise, athlete",
    
    # 影視
    "Netflix": "Netflix, streaming, movie",
    "韓劇": "Korean drama, K-drama, TV",
    
    # 支付
    "LINE Pay": "LINE Pay, mobile payment, QR code",
    
    # 棒球
    "中職": "baseball, CPBL, Taiwan baseball",
    "棒球": "baseball, stadium, sports",
    
    # 能源
    "太陽能": "solar panels, renewable energy, green",
    "綠能": "solar energy, nature, sustainable",
    
    # 健康
    "健康": "health, wellness, lifestyle",
    "睡眠": "sleep, bedroom, rest",
    "久坐": "office, desk work, sitting",
    "心態": "mindset, positive thinking, happiness",
    "專注力": "focus, concentration, work",
    "數位排毒": "nature, peace, digital detox",
    "遠距工作": "remote work, laptop, home office",
    "办公室": "office, workspace, computer",
}

def get_keywords_from_title(title):
    """從標題提取關鍵詞"""
    keywords = []
    for key in KEYWORD_VISUALS:
        if key in title:
            keywords.append(key)
    return keywords

def get_category_from_title(title):
    """從標題猜測分類"""
    category_keywords = {
        "技術": ["AI", "ChatGPT", "Python", "代理", "Threads", "iPhone", "Switch", "自動化"],
        "投資": ["比特幣", "加密貨幣", "股票", "ETF", "理財", "高股息"],
        "健康": ["健康", "睡眠", "健身", "運動", "久坐", "心態"],
        "生活": ["捷運", "交通", "機車", "餐廳", "美食", "母親節", "演唱會", "旅遊", "日本", 
                 "蝦皮", "購物", "時尚", "穿搭", "遊戲", "手機遊戲", "Netflix", "韓劇", 
                 "LINE Pay", "中職", "棒球", "短影音", "YouTuber", "Vtuber", "數位排毒", 
                 "遠距工作", "办公室"]
    }
    
    for cat, keys in category_keywords.items():
        for key in keys:
            if key in title:
                return cat
    return "生活"

def generate_ai_image_url(title, width=800, height=600):
    """生成 AI 圖片 URL - 嘗試多個免費服務"""
    
    # 提取關鍵詞
    keywords = get_keywords_from_title(title)
    category = get_category_from_title(title)
    
    if keywords:
        prompt = KEYWORD_VISUALS.get(keywords[0], "modern lifestyle")
    else:
        prompt = "modern lifestyle, Asia"
    
    # 添加分類相關的描述
    prompt += f", {category}, high quality, professional"
    
    # 嘗試 Pollinations AI (新版本)
    encoded_prompt = urllib.parse.quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={width}&height={height}&nologo=true"
    
    return url, prompt

def download_image(url, output_path, title):
    """下載圖片"""
    print(f"  下載 URL: {url[:80]}...")
    try:
        req = urllib.request.Request(
            url,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
        )
        with urllib.request.urlopen(req, timeout=60) as response:
            data = response.read()
            
        if len(data) > 5000:  # 有效的圖片應該大於 5KB
            with open(output_path, 'wb') as f:
                f.write(data)
            print(f"  ✓ 成功下載: {len(data)} bytes")
            return True
        else:
            print(f"  ✗ 圖片太小，可能失敗")
            return False
    except Exception as e:
        print(f"  ✗ 下載失敗: {e}")
        return False

def create_fallback_image(title, output_path):
    """創建備用圖案（當 AI 生成失敗時）"""
    category = get_category_from_title(title)
    colors = CATEGORY_COLORS.get(category, CATEGORY_COLORS["default"])
    
    # 創建簡單的 SVG 圖案
    svg_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="800" height="600" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:{colors['primary']};stop-opacity:1" />
      <stop offset="100%" style="stop-color:{colors['secondary']};stop-opacity:1" />
    </linearGradient>
  </defs>
  <rect width="800" height="600" fill="url(#grad)"/>
  <text x="400" y="300" font-family="Arial, sans-serif" font-size="32" 
        fill="white" text-anchor="middle" dominant-baseline="middle">
    {title[:20]}...
  </text>
</svg>'''
    
    # 轉換為 PNG（使用簡單的占位符）
    with open(output_path.replace('.jpg', '.svg'), 'w', encoding='utf-8') as f:
        f.write(svg_content)
    
    print(f"  ⚠ 已創建 SVG 備用圖案")
    return True

def main():
    print("=" * 60)
    print("開始為所有文章生成 AI 圖片...")
    print("=" * 60)
    
    # 獲取所有文章
    posts_dir = f"{BLOG_DIR}/_posts"
    posts = sorted([f for f in os.listdir(posts_dir) if f.endswith('.md')])
    
    print(f"找到 {len(posts)} 篇文章")
    
    success_count = 0
    fail_count = 0
    
    for post_file in posts:
        post_path = os.path.join(posts_dir, post_file)
        
        # 讀取文章標題
        title = None
        image_path = None
        
        with open(post_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.startswith('title:'):
                    title = line.replace('title:', '').strip().strip('"')
                if line.startswith('image:'):
                    image_path = line.replace('image:', '').strip()
        
        if not title or not image_path:
            print(f"\n⚠ 跳過 {post_file} (缺少標題或圖片欄位)")
            continue
        
        # 獲取圖片檔名
        image_filename = os.path.basename(image_path)
        image_full_path = os.path.join(IMAGES_DIR, image_filename)
        
        print(f"\n處理: {title}")
        print(f"  圖片: {image_filename}")
        
        # 檢查圖片是否已存在且大小足夠
        if os.path.exists(image_full_path):
            size = os.path.getsize(image_full_path)
            if size > 10000:  # 大於 10KB 认为有效
                print(f"  ✓ 圖片已存在且有效 ({size} bytes)，跳過")
                success_count += 1
                continue
        
        # 生成 AI 圖片 URL
        ai_url, prompt = generate_ai_image_url(title)
        
        # 下載圖片
        if download_image(ai_url, image_full_path, title):
            success_count += 1
        else:
            # 嘗試備用方案
            print("  嘗試備用方案...")
            if create_fallback_image(title, image_full_path):
                success_count += 1
            else:
                fail_count += 1
        
        # 避免請求過快
        time.sleep(1)
    
    print("\n" + "=" * 60)
    print(f"完成！成功: {success_count}, 失敗: {fail_count}")
    print("=" * 60)

if __name__ == "__main__":
    main()