#!/usr/bin/env python3
"""
批量為部落格文章生成 AI 圖片
使用 Pollinations AI 免費 API
"""

import os
import sys
import time

# 添加腳本目錄到路徑
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

from generate_ai_image import generate_for_article

# 文章資訊
ARTICLES = [
    {
        "title": "如何在 GitHub Pages 建立個人部落格",
        "category": "技術",
        "summary": "Jekyll 靜態網站生成器教學，從零開始建立部落格，GitHub 免費託管",
        "current_image": "如何在-github-pages-建立個人部落格.svg"
    },
    {
        "title": "提升工作效率的五個實用技巧",
        "category": "生活",
        "summary": "時間管理、番茄工作法、優先處理重要任務、建立專注環境、善用工具",
        "current_image": "提升工作效率的五個實用技巧.svg"
    },
    {
        "title": "AI 自動化如何改變未來工作模式",
        "category": "技術",
        "summary": "人工智慧與自動化技術、人機協作、新興職業、培養不可取代的技能",
        "current_image": "ai-自動化如何改變未來工作模式.svg"
    },
    {
        "title": "建立健康生活的五個簡單習慣",
        "category": "健康",
        "summary": "規律作息、每天運動三十分鐘、均衡飲食、定期休息、保持社交連結",
        "current_image": "建立健康生活的五個簡單習慣.svg"
    }
]

def main():
    """批量生成圖片"""
    # 輸出目錄
    output_dir = os.path.join(os.path.dirname(script_dir), "assets", "images", "featured")
    
    print("=" * 60)
    print("🎨 部落格 AI 圖片批量生成器")
    print(f"📍 輸出目錄: {output_dir}")
    print(f"📊 文章數量: {len(ARTICLES)} 篇")
    print("=" * 60)
    
    success_count = 0
    generated_files = []
    
    for i, article in enumerate(ARTICLES, 1):
        print(f"\n[{i}/{len(ARTICLES)}] 正在處理: {article['title']}")
        print("-" * 60)
        
        # 生成圖片
        success = generate_for_article(
            title=article["title"],
            category=article["category"],
            content_summary=article["summary"],
            output_dir=output_dir
        )
        
        if success:
            success_count += 1
            # 新圖片檔名（PNG 格式）
            safe_title = article["title"].replace(" ", "-").replace("/", "-")
            new_image = f"{safe_title}.png"
            generated_files.append({
                "old": article["current_image"],
                "new": new_image,
                "title": article["title"]
            })
        
        # 避免請求過快
        if i < len(ARTICLES):
            print("⏳ 等待 3 秒...")
            time.sleep(3)
    
    print("\n" + "=" * 60)
    print(f"✅ 完成！成功生成 {success_count}/{len(ARTICLES)} 張圖片")
    print("=" * 60)
    
    # 輸出需要更新的 front matter
    if generated_files:
        print("\n📝 需要更新文章 front matter 的 image 欄位：")
        print("-" * 60)
        for f in generated_files:
            print(f"  {f['title']}")
            print(f"    舊: {f['old']}")
            print(f"    新: {f['new']}")
            print()
    
    return success_count == len(ARTICLES)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
