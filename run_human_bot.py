#!/usr/bin/env python3
"""
一鍵執行人性化點擊 BOT
"""

from human_like_bot import HumanLikeBot

def main():
    print("=" * 60)
    print("👤 人性化點擊 BOT - 一鍵執行")
    print("=" * 60)
    
    bot = HumanLikeBot()
    
    # 預設參數
    url = "https://hongkpng856-blip.github.io/ip-tracker/"
    clicks = 3
    min_interval = 0.5  # 30 秒（測試用）
    max_interval = 2    # 2 分鐘（測試用）
    
    print(f"\n📍 目標網站: {url}")
    print(f"🔢 點擊次數: {clicks}")
    print(f"⏱️ 間隔時間: {min_interval}-{max_interval} 分鐘（隨機）")
    print("-" * 60)
    
    # 執行
    results = bot.run_human_like_campaign(
        url=url,
        total_clicks=clicks,
        min_interval_minutes=min_interval,
        max_interval_minutes=max_interval
    )
    
    # 報告
    report = bot.generate_campaign_report(results)
    bot.save_report(report)


if __name__ == "__main__":
    main()
