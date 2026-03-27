#!/usr/bin/env python3
"""
測試腳本：使用人性化 BOT 訪問模擬網站
"""

from human_like_bot import HumanLikeBot
import time

def main():
    print("=" * 60)
    print("🧪 測試人性化 BOT")
    print("=" * 60)
    print("\n請先在另一個終端啟動模擬網站：")
    print("  python3 mock_website.py")
    print()
    
    input("按 Enter 開始測試...")
    
    bot = HumanLikeBot()
    
    # 測試參數
    url = "http://localhost:8888"
    
    results = bot.run_human_like_campaign(
        url=url,
        total_clicks=5,
        min_interval_minutes=0.1,  # 6 秒（測試用）
        max_interval_minutes=0.5   # 30 秒（測試用）
    )
    
    report = bot.generate_campaign_report(results)
    bot.save_report(report)
    
    print(f"\n🌐 請查看結果: {url}")

if __name__ == "__main__":
    main()