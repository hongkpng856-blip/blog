#!/usr/bin/env python3
"""
Prolific 自動註冊嘗試
使用 Playwright 自動化瀏覽器（無頭模式）
"""

import subprocess
import sys
import json
from pathlib import Path
from datetime import datetime

def check_playwright():
    """檢查 Playwright 是否已安裝"""
    try:
        import playwright
        return True
    except ImportError:
        return False

def install_playwright():
    """安裝 Playwright"""
    print("[INFO] 正在安裝 Playwright...")
    subprocess.run([sys.executable, "-m", "pip", "install", "playwright"], check=True)
    subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], check=True)
    print("[INFO] Playwright 安裝完成")

def register_prolific_headless():
    """使用 Playwright 嘗試註冊 Prolific（無頭模式）"""
    try:
        from playwright.sync_api import sync_playwright
        
        print("[INFO] 啟動 Playwright 無頭瀏覽器...")
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            )
            page = context.new_page()
            
            print("[INFO] 訪問 Prolific 註冊頁面...")
            page.goto("https://app.prolific.com/register/participant/join-waitlist/about-yourself", timeout=60000)
            
            # 等待頁面載入
            page.wait_for_timeout(5000)
            
            # 截圖
            screenshot_path = Path(__file__).parent / "prolific_screenshot.png"
            page.screenshot(path=str(screenshot_path))
            print(f"[INFO] 截圖已保存: {screenshot_path}")
            
            # 獲取頁面內容
            content = page.content()
            html_path = Path(__file__).parent / "prolific_page.html"
            with open(html_path, 'w') as f:
                f.write(content)
            print(f"[INFO] 頁面 HTML 已保存: {html_path}")
            
            # 檢查是否有 Google SSO 按鈕
            google_button = page.query_selector('button:has-text("Google"), [data-testid="google-button"], .google-button')
            if google_button:
                print("[SUCCESS] 發現 Google SSO 按鈕！")
            
            browser.close()
            return True
            
    except Exception as e:
        print(f"[ERROR] {e}")
        return False

def main():
    print("=" * 50)
    print("Prolific 自動註冊嘗試")
    print("=" * 50)
    
    # 檢查並安裝 Playwright
    if not check_playwright():
        print("[WARN] Playwright 未安裝")
        try:
            install_playwright()
        except Exception as e:
            print(f"[ERROR] 無法安裝 Playwright: {e}")
            print("[INFO] 將使用 curl 作為備選方案...")
            return use_curl_fallback()
    
    # 嘗試無頭註冊
    return register_prolific_headless()

def use_curl_fallback():
    """使用 curl 作為備選方案"""
    import urllib.request
    import urllib.error
    
    url = "https://app.prolific.com/register/participant/join-waitlist/about-yourself"
    
    print(f"[INFO] 使用 curl 訪問 {url}...")
    
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
        })
        response = urllib.request.urlopen(req, timeout=30)
        content = response.read().decode('utf-8')
        
        # 保存響應
        html_path = Path(__file__).parent / "prolific_curl_response.html"
        with open(html_path, 'w') as f:
            f.write(content)
        print(f"[INFO] 響應已保存: {html_path}")
        
        # 分析響應
        if "Prolific" in content:
            print("[SUCCESS] 成功獲取 Prolific 頁面")
            return True
        else:
            print("[WARN] 響應內容異常")
            return False
            
    except urllib.error.URLError as e:
        print(f"[ERROR] 請求失敗: {e}")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n[DONE] Prolific 頁面已成功訪問")
        print("[NEXT] 需要老闆在 Windows 上手動完成註冊（無 CAPTCHA）")
    else:
        print("\n[FAIL] 自動訪問失敗")
        print("[NEXT] 請老闆手動訪問 Prolific 註冊頁面")
