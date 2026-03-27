#!/usr/bin/env python3
"""
每日自動執行腳本
每天自動檢查並執行可行的賺錢任務
"""

import json
import subprocess
import urllib.request
from pathlib import Path
from datetime import datetime

class DailyAutoRunner:
    def __init__(self):
        self.workspace = Path("/home/claw/.openclaw/workspace")
        self.status_file = self.workspace / "daily_status.json"
        self.target_usd = 5.00
        
    def log(self, msg):
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{ts}] {msg}")
        
    def check_platform_status(self):
        """檢查各平台狀態"""
        platforms = {
            "prolific": {"url": "https://app.prolific.com", "captcha": False},
            "prizerebel": {"url": "https://www.prizerebel.com", "captcha": True},
            "swagbucks": {"url": "https://www.swagbucks.com", "captcha": True},
            "microsoft_rewards": {"url": "https://rewards.microsoft.com", "captcha": False}
        }
        
        results = {}
        for name, info in platforms.items():
            try:
                req = urllib.request.Request(info["url"], headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                })
                resp = urllib.request.urlopen(req, timeout=10)
                results[name] = {"accessible": resp.getcode() == 200, "captcha": info["captcha"]}
            except Exception as e:
                results[name] = {"accessible": False, "error": str(e)[:50], "captcha": info["captcha"]}
        
        return results
    
    def get_current_earnings(self):
        """獲取目前收入"""
        status_file = self.workspace / "earnings_status.json"
        if status_file.exists():
            try:
                with open(status_file, 'r') as f:
                    data = json.load(f)
                    return data.get("total_earnings", 0)
            except:
                pass
        return 0.0
    
    def generate_daily_report(self):
        """生成每日報告"""
        self.log("=" * 60)
        self.log("📊 每日自動執行報告")
        self.log("=" * 60)
        
        # 檢查平台
        self.log("\n[1] 檢查平台狀態...")
        platforms = self.check_platform_status()
        
        accessible = []
        need_captcha = []
        
        for name, info in platforms.items():
            if info.get("accessible"):
                if info.get("captcha"):
                    need_captcha.append(name)
                else:
                    accessible.append(name)
        
        self.log(f"\n✅ 可用（無 CAPTCHA）: {', '.join(accessible) if accessible else '無'}")
        self.log(f"⚠️ 可用（需 CAPTCHA）: {', '.join(need_captcha) if need_captcha else '無'}")
        
        # 目前收入
        self.log("\n[2] 目前收入狀態...")
        current = self.get_current_earnings()
        self.log(f"已賺取: ${current:.2f} USD")
        self.log(f"目標: ${self.target_usd:.2f} USD")
        self.log(f"差距: ${max(0, self.target_usd - current):.2f} USD")
        
        # 可執行行動
        self.log("\n[3] 今日可執行行動...")
        
        actions = []
        
        if "prolific" in accessible:
            actions.append({
                "priority": 1,
                "name": "註冊 Prolific",
                "url": "https://app.prolific.com/register/participant/join-waitlist/about-yourself",
                "expected": "$5-20/研究",
                "captcha": False
            })
        
        if "microsoft_rewards" in accessible:
            actions.append({
                "priority": 2,
                "name": "Microsoft Rewards 搜索",
                "url": "https://www.bing.com",
                "expected": "$5/月",
                "captcha": False
            })
        
        # 腳本出售
        actions.append({
            "priority": 0,
            "name": "出售腳本包",
            "url": "Gumroad",
            "expected": "$5/份",
            "captcha": False
        })
        
        for i, action in enumerate(sorted(actions, key=lambda x: x["priority"]), 1):
            self.log(f"  {i}. {action['name']} → {action['expected']}")
            if action["url"] != "Gumroad":
                self.log(f"     URL: {action['url']}")
        
        self.log("\n" + "=" * 60)
        self.log("執行完成")
        self.log("=" * 60)
        
        # 保存報告
        report = {
            "timestamp": datetime.now().isoformat(),
            "platforms": platforms,
            "current_earnings": current,
            "target": self.target_usd,
            "gap": max(0, self.target_usd - current),
            "actions": actions
        }
        
        with open(self.status_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        self.log(f"\n報告已保存: {self.status_file}")
        
        return report

if __name__ == "__main__":
    runner = DailyAutoRunner()
    runner.generate_daily_report()
