#!/usr/bin/env python3
"""
簡易 BOT - 訪問雲端網站並模擬點擊
"""
import time
import random
import urllib.request
import urllib.error

def visit_website(url, clicks=5):
    """訪問網站並模擬點擊"""
    print(f"🌐 BOT 啟動 - 目標: {url}")
    print(f"📊 預計點擊次數: {clicks}")
    print("-" * 50)
    
    success_count = 0
    
    for i in range(clicks):
        try:
            # 模擬人類延遲
            delay = random.uniform(2, 5)
            print(f"⏳ 點擊 {i+1}/{clicks} - 等待 {delay:.1f} 秒...")
            time.sleep(delay)
            
            # 訪問網站
            req = urllib.request.Request(
                url,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
            )
            response = urllib.request.urlopen(req, timeout=30)
            html = response.read().decode('utf-8')
            
            # 檢查內容
            if 'mock-website' in html or 'Click' in html or 'BOT' in html:
                print(f"✅ 點擊 {i+1}/{clicks} - 成功！")
                success_count += 1
            else:
                print(f"⚠️ 點擊 {i+1}/{clicks} - 內容異常")
                
        except urllib.error.HTTPError as e:
            print(f"❌ 點擊 {i+1}/{clicks} - HTTP 錯誤: {e.code}")
        except urllib.error.URLError as e:
            print(f"❌ 點擊 {i+1}/{clicks} - URL 錯誤: {e.reason}")
        except Exception as e:
            print(f"❌ 點擊 {i+1}/{clicks} - 錯誤: {str(e)}")
    
    print("-" * 50)
    print(f"📊 結果: {success_count}/{clicks} 成功")
    print(f"🎯 成功率: {success_count/clicks*100:.1f}%")
    
    return success_count

if __name__ == "__main__":
    import sys
    
    # 預設 URL
    url = "https://hongkpng856-blip.github.io/mock-website/"
    
    # 檢查命令列參數
    if len(sys.argv) > 1:
        url = sys.argv[1]
    
    # 執行 BOT
    visit_website(url, clicks=5)
