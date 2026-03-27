#!/usr/bin/env python3
"""
人性化點擊 BOT
功能：
1. 隨機化點擊間距（模擬真實人類行為）
2. 可調整時間範圍（例如隨機 1-30 分鐘）
3. 模擬人類閱讀、思考、滾動等行為
4. 避免被檢測為 BOT
"""

import random
import time
import json
import requests
from datetime import datetime, timedelta
from typing import List, Optional, Tuple
import math

class HumanLikeBot:
    """模擬真實人類點擊行為的 BOT"""
    
    def __init__(self):
        self.session = requests.Session()
        self.visit_log = []
        
        # 模擬人類行為的參數
        self.behavior_config = {
            # 閱讀速度（每分鐘字數）
            "reading_speed": (200, 400),
            # 頁面瀏覽時間（秒）
            "page_view_time": (10, 60),
            # 思考時間（秒）
            "thinking_time": (2, 15),
            # 滾動次數
            "scroll_count": (3, 10),
            # 滾動間隔（秒）
            "scroll_interval": (0.5, 3),
        }
    
    def human_delay(self, min_seconds: float, max_seconds: float) -> float:
        """
        生成人性化延遲時間
        使用多種分佈混合，避免被檢測
        """
        # 方法 1：均勻分佈
        uniform_val = random.uniform(min_seconds, max_seconds)
        
        # 方法 2：正態分佈（偏向中間值）
        mean = (min_seconds + max_seconds) / 2
        std = (max_seconds - min_seconds) / 4
        normal_val = random.gauss(mean, std)
        normal_val = max(min_seconds, min(max_seconds, normal_val))
        
        # 方法 3：指數分佈（偏向較短時間）
        lambda_val = 1 / (min_seconds + (max_seconds - min_seconds) * 0.3)
        exp_val = random.expovariate(lambda_val)
        exp_val = max(min_seconds, min(max_seconds, exp_val))
        
        # 隨機選擇一種分佈
        choice = random.random()
        if choice < 0.4:
            return uniform_val
        elif choice < 0.7:
            return normal_val
        else:
            return exp_val
    
    def human_delay_minutes(self, min_minutes: float, max_minutes: float) -> float:
        """生成人性化延遲時間（分鐘）"""
        return self.human_delay(min_minutes * 60, max_minutes * 60)
    
    def simulate_reading(self, content_length: int = 500) -> float:
        """
        模擬人類閱讀行為
        返回預計閱讀時間（秒）
        """
        # 計算閱讀時間
        reading_speed = random.randint(*self.behavior_config["reading_speed"])
        base_time = content_length / reading_speed * 60
        
        # 加入隨機變化（人會分心、重複閱讀）
        distraction_factor = random.uniform(0.8, 1.5)
        actual_time = base_time * distraction_factor
        
        # 加入思考時間
        thinking_time = self.human_delay(*self.behavior_config["thinking_time"])
        
        total_time = actual_time + thinking_time
        
        print(f"  📖 模擬閱讀：{content_length} 字，預計 {total_time:.1f} 秒")
        return total_time
    
    def simulate_scrolling(self) -> float:
        """
        模擬人類滾動行為
        返回總滾動時間（秒）
        """
        scroll_count = random.randint(*self.behavior_config["scroll_count"])
        total_time = 0
        
        print(f"  📜 模擬滾動：{scroll_count} 次")
        
        for i in range(scroll_count):
            # 滾動間隔
            scroll_time = self.human_delay(*self.behavior_config["scroll_interval"])
            total_time += scroll_time
            
            # 模擬在頁面上停留（可能會看某個部分）
            if random.random() < 0.3:  # 30% 機率會停下來看
                pause_time = self.human_delay(1, 5)
                total_time += pause_time
        
        return total_time
    
    def simulate_human_session(self) -> dict:
        """
        模擬一個完整的人類瀏覽會話
        返回會話統計
        """
        session_start = datetime.now()
        
        # 隨機決定行為
        actions = []
        total_time = 0
        
        # 1. 頁面載入等待
        load_time = self.human_delay(1, 4)
        total_time += load_time
        actions.append(f"頁面載入 ({load_time:.1f}s)")
        
        # 2. 初始瀏覽
        initial_view = self.human_delay(3, 10)
        total_time += initial_view
        actions.append(f"初始瀏覽 ({initial_view:.1f}s)")
        
        # 3. 滾動
        if random.random() < 0.7:  # 70% 機率會滾動
            scroll_time = self.simulate_scrolling()
            total_time += scroll_time
            actions.append(f"頁面滾動 ({scroll_time:.1f}s)")
        
        # 4. 閱讀
        if random.random() < 0.5:  # 50% 機率會仔細閱讀
            content_length = random.randint(200, 1000)
            read_time = self.simulate_reading(content_length)
            total_time += read_time
            actions.append(f"閱讀內容 ({read_time:.1f}s)")
        
        # 5. 思考
        if random.random() < 0.4:  # 40% 機率會思考
            think_time = self.human_delay(2, 15)
            total_time += think_time
            actions.append(f"思考 ({think_time:.1f}s)")
        
        return {
            "start_time": session_start.isoformat(),
            "total_time": round(total_time, 2),
            "actions": actions,
            "action_count": len(actions)
        }
    
    def visit_with_human_behavior(self, url: str, proxy: str = None) -> dict:
        """使用人性化行為訪問網站"""
        result = {
            "url": url,
            "proxy": proxy,
            "timestamp": datetime.now().isoformat(),
            "success": False,
            "session": None,
            "error": None
        }
        
        proxies = None
        if proxy:
            proxies = {
                "http": f"http://{proxy}",
                "https": f"http://{proxy}"
            }
        
        # 模擬瀏覽器標頭（每次都略有不同）
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        ]
        
        headers = {
            "User-Agent": random.choice(user_agents),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": random.choice(["en-US,en;q=0.9", "zh-TW,zh;q=0.9,en-US;q=0.8", "en-GB,en;q=0.9"]),
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": random.choice(["none", "same-origin", "cross-site"]),
            "Sec-Fetch-User": "?1",
            "Cache-Control": random.choice(["max-age=0", "no-cache"]),
        }
        
        try:
            # 模擬人類會話
            session = self.simulate_human_session()
            result["session"] = session
            
            # 實際請求
            resp = self.session.get(url, proxies=proxies, headers=headers, timeout=30)
            result["status_code"] = resp.status_code
            result["success"] = resp.status_code == 200
            
            if "Access Denied" in resp.text or "Error 16" in resp.text:
                result["error"] = "Blocked by security"
                result["success"] = False
                
        except Exception as e:
            result["error"] = str(e)
        
        return result
    
    def run_human_like_campaign(
        self, 
        url: str, 
        total_clicks: int = 10,
        min_interval_minutes: float = 5,
        max_interval_minutes: float = 30,
        proxies: List[str] = None
    ) -> List[dict]:
        """
        執行人性化點擊活動
        
        參數：
        - url: 目標網站
        - total_clicks: 總點擊次數
        - min_interval_minutes: 最小間隔（分鐘）
        - max_interval_minutes: 最大間隔（分鐘）
        - proxies: Proxy 列表（可選）
        """
        results = []
        
        print("=" * 60)
        print("👤 人性化點擊 BOT 啟動")
        print("=" * 60)
        print(f"\n📍 目標網站: {url}")
        print(f"🔢 總點擊次數: {total_clicks}")
        print(f"⏱️ 間隔時間: {min_interval_minutes}-{max_interval_minutes} 分鐘（隨機）")
        print("-" * 60)
        
        for i in range(total_clicks):
            print(f"\n[{i+1}/{total_clicks}] 第 {i+1} 次點擊")
            print(f"  ⏰ 開始時間: {datetime.now().strftime('%H:%M:%S')}")
            
            # 選擇 Proxy
            proxy = None
            if proxies and len(proxies) > 0:
                proxy = proxies[i % len(proxies)]
                print(f"  🌐 使用 Proxy: {proxy}")
            
            # 執行訪問
            result = self.visit_with_human_behavior(url, proxy)
            results.append(result)
            
            if result["success"]:
                print(f"  ✅ 成功")
                if result.get("session"):
                    print(f"  📊 會話時間: {result['session']['total_time']:.1f} 秒")
                    print(f"  📊 行為數量: {result['session']['action_count']}")
            else:
                print(f"  ❌ 失敗: {result.get('error', 'Unknown')}")
            
            # 如果不是最後一次，等待隨機間隔
            if i < total_clicks - 1:
                wait_time = self.human_delay_minutes(min_interval_minutes, max_interval_minutes)
                wait_minutes = wait_time / 60
                
                print(f"\n  ⏳ 等待 {wait_minutes:.1f} 分鐘後進行下一次點擊...")
                print(f"  📅 預計下次時間: {(datetime.now() + timedelta(seconds=wait_time)).strftime('%H:%M:%S')}")
                
                # 實際等待
                time.sleep(wait_time)
        
        return results
    
    def generate_campaign_report(self, results: List[dict]) -> dict:
        """生成活動報告"""
        total = len(results)
        success = sum(1 for r in results if r.get("success"))
        failed = total - success
        
        # 計算總時間
        total_session_time = sum(
            r.get("session", {}).get("total_time", 0) 
            for r in results if r.get("session")
        )
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total_clicks": total,
                "successful": success,
                "failed": failed,
                "success_rate": round(success / total * 100, 1) if total > 0 else 0,
                "total_session_time_seconds": round(total_session_time, 2),
                "total_session_time_minutes": round(total_session_time / 60, 2)
            },
            "results": results
        }
        
        print("\n" + "=" * 60)
        print("📊 活動報告")
        print("=" * 60)
        print(f"總點擊: {total}")
        print(f"成功: {success}")
        print(f"失敗: {failed}")
        print(f"成功率: {report['summary']['success_rate']}%")
        print(f"總會話時間: {report['summary']['total_session_time_minutes']:.1f} 分鐘")
        
        return report
    
    def save_report(self, report: dict, filename: str = "human_campaign_report.json"):
        """儲存報告"""
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        print(f"\n💾 報告已儲存到 {filename}")


def main():
    """主程式"""
    print("=" * 60)
    print("👤 人性化點擊 BOT")
    print("=" * 60)
    
    bot = HumanLikeBot()
    
    # 互動輸入
    print("\n請輸入參數：")
    
    url = input("目標網站 URL（預設 httpbin.org/ip）: ").strip()
    if not url:
        url = "https://httpbin.org/ip"
    
    clicks_input = input("總點擊次數（預設 5）: ").strip()
    clicks = int(clicks_input) if clicks_input.isdigit() else 5
    
    min_interval_input = input("最小間隔分鐘（預設 1）: ").strip()
    min_interval = float(min_interval_input) if min_interval_input else 1
    
    max_interval_input = input("最大間隔分鐘（預設 30）: ").strip()
    max_interval = float(max_interval_input) if max_interval_input else 30
    
    print(f"\n📊 參數確認：")
    print(f"  目標: {url}")
    print(f"  點擊次數: {clicks}")
    print(f"  間隔時間: {min_interval}-{max_interval} 分鐘")
    
    confirm = input("\n確認開始？(y/n): ").strip().lower()
    if confirm != 'y':
        print("已取消")
        return
    
    # 執行活動
    results = bot.run_human_like_campaign(
        url=url,
        total_clicks=clicks,
        min_interval_minutes=min_interval,
        max_interval_minutes=max_interval
    )
    
    # 生成報告
    report = bot.generate_campaign_report(results)
    bot.save_report(report)


if __name__ == "__main__":
    main()
