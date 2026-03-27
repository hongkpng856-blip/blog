#!/usr/bin/env python3
"""
部落格文章圖片生成器 - 使用 Unsplash Source API
為部落格文章下載高品質圖片

Unsplash Source API 免費且無需 API key
格式: https://source.unsplash.com/{width}x{height}/?{keywords}
"""

import urllib.request
import urllib.parse
import os
import sys
import time
import random

# Unsplash Source API
UNSPLASH_API = "https://source.unsplash.com"

def download_unsplash_image(keywords: list, output_path: str, width: int = 1280, height: int = 720):
    """
    從 Unsplash 下載符合關鍵字的圖片
    
    Args:
        keywords: 搜尋關鍵字列表
        output_path: 輸出路徑
        width: 圖片寬度
        height: 圖片高度
    """
    # 建構 URL
    query = ",".join(keywords)
    url = f"{UNSPLASH_API}/{width}x{height}/?{query}"
    
    print(f"🖼️ 正在下載 Unsplash 圖片...")
    print(f"📝 Keywords: {query}")
    print(f"📐 Size: {width}x{height}")
    print(f"🔗 URL: {url}")
    
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        with urllib.request.urlopen(req, timeout=60) as response:
            image_data = response.read()
        
        if len(image_data) < 5000:
            print(f"⚠️ 圖片太小 ({len(image_data)} bytes)")
            return False
        
        # 確保目錄存在
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # 儲存圖片
        with open(output_path, 'wb') as f:
            f.write(image_data)
        
        print(f"✅ 圖片已儲存: {output_path}")
        print(f"📊 檔案大小: {len(image_data) / 1024:.1f} KB")
        return True
        
    except Exception as e:
        print(f"❌ 下載失敗: {e}")
        return False

def generate_for_article(title: str, category: str, output_dir: str):
    """
    為文章下載特色圖片
    
    Args:
        title: 文章標題
        category: 文章分類
        output_dir: 輸出目錄
    """
    
    # 根據分類選擇關鍵字
    keyword_map = {
        "技術": ["technology", "coding", "computer", "programming", "laptop", "developer"],
        "生活": ["lifestyle", "work", "office", "productivity", "desk", "creative"],
        "健康": ["health", "wellness", "fitness", "yoga", "nature", "healthy"],
        "投資": ["business", "finance", "money", "investment", "stock", "economy"]
    }
    
    keywords = keyword_map.get(category, ["blog", "article", "writing"])
    
    # 輸出檔名
    safe_title = title.replace(" ", "-").replace("/", "-")
    output_path = os.path.join(output_dir, f"{safe_title}.jpg")
    
    return download_unsplash_image(keywords, output_path)

def main():
    """主程式"""
    if len(sys.argv) < 4:
        print("使用方式: python3 generate_image_unsplash.py <標題> <分類> <輸出目錄>")
        print("範例: python3 generate_image_unsplash.py '如何在 GitHub Pages 建立個人部落格' '技術' './assets/images/featured/'")
        sys.exit(1)
    
    title = sys.argv[1]
    category = sys.argv[2]
    output_dir = sys.argv[3]
    
    success = generate_for_article(title, category, output_dir)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
