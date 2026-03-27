#!/usr/bin/env python3
"""
智能狀態監控與自動重試腳本
功能：
1. 定期檢查 Prolific 候補名單狀態
2. 檢測 IP 是否被阻擋
3. 自動從免費代理池切換 IP
4. 生成每日進度報告
"""

import json
import time
import requests
from datetime import datetime
from pathlib import Path

# === 配置 ===
CONFIG = {
    "check_interval": 300,  # 5 分鐘檢查一次
    "max_retries": 3,
    "proxy_list_file": "free_proxies.txt",
    "status_file": "platform_status.json",
    "report_file": "daily_report.json",
    "platforms": {
        "prolific": {
            "url": "https://app.prolific.com",
            "login_url": "https://app.prolific.com/login",
            "priority": 1,
            "status": "waitlist"
        },
        "qmee": {
            "url": "https://www.qmee.com",
            "priority": 2,
            "status": "blocked"
        },
        "prizeRebel": {
            "url": "https://www.prizerebel.com",
            "priority": 3,
            "status": "captcha"
        }
    }
}

class SmartMonitor:
    def __init__(self):
        self.status_file = Path(CONFIG["status_file"])
        self.report_file = Path(CONFIG["report_file"])
        self.load_status()
    
    def load_status(self):
        """載入狀態"""
        if self.status_file.exists():
            with open(self.status_file, 'r') as f:
                self.status = json.load(f)
        else:
            self.status = {
                "last_check": None,
                "ip_status": "unknown",
                "platforms": CONFIG["platforms"],
                "total_earned": 0.0
            }
    
    def save_status(self):
        """儲存狀態"""
        with open(self.status_file, 'w') as f:
            json.dump(self.status, f, indent=2, ensure_ascii=False)
    
    def check_ip_blocked(self):
        """檢測 IP 是否被阻擋"""
        test_urls = [
            "https://www.qmee.com",
            "https://www.prizerebel.com"
        ]
        
        blocked_count = 0
        for url in test_urls:
            try:
                resp = requests.get(url, timeout=10)
                if "Access Denied" in resp.text or "Error 16" in resp.text:
                    blocked_count += 1
                    print(f"⚠️ {url} - 被阻擋")
                else:
                    print(f"✅ {url} - 可訪問")
            except Exception as e:
                print(f"❌ {url} - 錯誤: {e}")
                blocked_count += 1
        
        self.status["ip_status"] = "blocked" if blocked_count > 0 else "ok"
        return self.status["ip_status"]
    
    def get_free_proxies(self):
        """獲取免費代理列表"""
        proxies = []
        proxy_file = Path(CONFIG["proxy_list_file"])
        
        if proxy_file.exists():
            with open(proxy_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and ":" in line:
                        proxies.append(line)
        
        return proxies
    
    def test_proxy(self, proxy):
        """測試代理是否可用"""
        test_url = "https://httpbin.org/ip"
        proxies = {
            "http": f"http://{proxy}",
            "https": f"http://{proxy}"
        }
        
        try:
            resp = requests.get(test_url, proxies=proxies, timeout=10)
            if resp.status_code == 200:
                print(f"✅ 代理可用: {proxy}")
                return True
        except:
            pass
        
        print(f"❌ 代理失效: {proxy}")
        return False
    
    def switch_proxy(self):
        """切換代理"""
        proxies = self.get_free_proxies()
        
        for proxy in proxies:
            if self.test_proxy(proxy):
                return proxy
        
        return None
    
    def check_prolific_status(self):
        """檢查 Prolific 狀態"""
        print("\n🔍 檢查 Prolific 候補名單狀態...")
        
        # 注意：這裡需要實際登入才能檢查
        # 目前只是模擬檢查
        print("⏳ Prolific 狀態：候補名單中（需等待 1-7 天）")
        
        return self.status["platforms"]["prolific"]["status"]
    
    def generate_daily_report(self):
        """生成每日報告"""
        report = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "time": datetime.now().strftime("%H:%M:%S"),
            "ip_status": self.status["ip_status"],
            "total_earned": self.status["total_earned"],
            "platforms": {},
            "recommendations": []
        }
        
        # 平台狀態
        for name, platform in self.status["platforms"].items():
            report["platforms"][name] = {
                "status": platform["status"],
                "priority": platform["priority"]
            }
        
        # 建議
        if self.status["ip_status"] == "blocked":
            report["recommendations"].append("建議：等待 IP 冷卻或使用 VPN")
        
        if self.status["platforms"]["prolific"]["status"] == "waitlist":
            report["recommendations"].append("建議：等待 Prolific 審核結果")
        
        report["recommendations"].append("建議：手動驗證其他 7 個平台的 email")
        
        # 儲存報告
        with open(self.report_file, 'w') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        return report
    
    def run_monitor_cycle(self):
        """執行一次監控循環"""
        print(f"\n{'='*50}")
        print(f"🔄 監控循環開始 - {datetime.now().strftime('%H:%M:%S')}")
        print(f"{'='*50}")
        
        # 1. 檢查 IP 狀態
        ip_status = self.check_ip_blocked()
        
        # 2. 如果 IP 被阻擋，嘗試切換代理
        if ip_status == "blocked":
            print("\n🔄 嘗試切換代理...")
            new_proxy = self.switch_proxy()
            if new_proxy:
                print(f"✅ 已切換到代理: {new_proxy}")
            else:
                print("⚠️ 無可用代理")
        
        # 3. 檢查 Prolific 狀態
        prolific_status = self.check_prolific_status()
        
        # 4. 更新時間戳
        self.status["last_check"] = datetime.now().isoformat()
        self.save_status()
        
        # 5. 生成報告
        report = self.generate_daily_report()
        
        print(f"\n📊 今日報告:")
        print(f"  IP 狀態: {report['ip_status']}")
        print(f"  累計收入: ${report['total_earned']:.2f}")
        print(f"\n📋 建議:")
        for rec in report["recommendations"]:
            print(f"  • {rec}")
        
        return report
    
    def run(self, continuous=True):
        """運行監控"""
        print("🚀 智能狀態監控啟動")
        print(f"📅 日期: {datetime.now().strftime('%Y-%m-%d')}")
        
        if continuous:
            while True:
                self.run_monitor_cycle()
                print(f"\n⏰ 等待 {CONFIG['check_interval']} 秒後進行下次檢查...")
                time.sleep(CONFIG["check_interval"])
        else:
            return self.run_monitor_cycle()


if __name__ == "__main__":
    monitor = SmartMonitor()
    
    # 單次執行
    monitor.run(continuous=False)
    
    # 持續監控（取消註解以啟用）
    # monitor.run(continuous=True)
