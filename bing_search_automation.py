#!/usr/bin/env python3
"""
Bing 搜索自動化
用於 Microsoft Rewards 積分累積
"""

import urllib.request
import urllib.parse
import time
import random
from datetime import datetime

# 搜索詞列表（30 個，每日搜索）
SEARCH_TERMS = [
    "weather today",
    "news headlines",
    "sports scores",
    "stock market",
    "technology news",
    "health tips",
    "recipe ideas",
    "movie reviews",
    "music charts",
    "travel deals",
    "fitness tips",
    "coding tutorials",
    "science news",
    "art history",
    "world geography",
    "business trends",
    "fashion 2026",
    "pet care",
    "home improvement",
    "car reviews",
    "space exploration",
    "ocean life",
    "mountain hiking",
    "coffee recipes",
    "tea varieties",
    "book recommendations",
    "podcast list",
    "photography tips",
    "garden ideas",
    "DIY projects"
]

def search_bing(term: str, cookies: str = None):
    """搜索 Bing"""
    url = f"https://www.bing.com/search?q={urllib.parse.quote(term)}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    }
    
    if cookies:
        headers['Cookie'] = cookies
    
    try:
        req = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(req, timeout=15)
        return response.getcode() == 200
    except Exception as e:
        print(f"[ERROR] 搜索 '{term}' 失敗: {e}")
        return False

def run_daily_searches(cookies: str = None):
    """執行每日搜索"""
    print(f"\n{'='*50}")
    print("Bing 搜索自動化")
    print(f"時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*50}\n")
    
    success_count = 0
    
    for i, term in enumerate(SEARCH_TERMS, 1):
        print(f"[{i}/30] 搜索: {term}...", end=" ")
        
        if search_bing(term, cookies):
            print("✅")
            success_count += 1
        else:
            print("❌")
        
        # 隨機延遲 5-15 秒（避免被偵測）
        delay = random.randint(5, 15)
        print(f"       等待 {delay} 秒...")
        time.sleep(delay)
    
    print(f"\n{'='*50}")
    print(f"完成: {success_count}/30 搜索成功")
    print(f"{'='*50}")
    
    return success_count

if __name__ == "__main__":
    print("⚠️ 注意：需要 Microsoft Rewards 帳號 cookies 才能累積積分")
    print("請先登入 https://www.bing.com 並獲取 cookies")
    print("")
    
    # 示範運行（無 cookies）
    print("示範運行（不累積積分）...")
    run_daily_searches()
