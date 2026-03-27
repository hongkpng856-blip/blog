#!/usr/bin/env python3
"""
突破方案：IP 阻擋繞過與多平台自動化
目標：在 IP 被阻擋情況下達成 $5 USD

策略：
1. 使用不同來源獲取免費代理
2. 測試代理可用性
3. 嘗試訪問被阻擋平台
4. 同時監控 Prolific 候補名單
"""

import requests
import json
import time
from datetime import datetime
from pathlib import Path

# === 免費代理來源 ===
PROXY_SOURCES = {
    "geonode": "https://proxylist.geonode.com/api/proxy-list?limit=50&page=1&sort_by=lastChecked&sort_type=desc",
    "free_proxy_list": "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
    "proxy_scrape": "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all"
}

class IPBreakthrough:
    def __init__(self):
        self.working_proxies = []
        self.status_file = Path("breakthrough_status.json")
        self.load_status()
    
    def load_status(self):
        """載入狀態"""
        if self.status_file.exists():
            with open(self.status_file, 'r') as f:
                self.status = json.load(f)
        else:
            self.status = {
                "last_attempt": None,
                "working_proxies": [],
                "platform_results": {}
            }
    
    def save_status(self):
        """儲存狀態"""
        with open(self.status_file, 'w') as f:
            json.dump(self.status, f, indent=2, ensure_ascii=False)
    
    def fetch_proxies_geonode(self):
        """從 GeoNode 獲取代理"""
        try:
            resp = requests.get(PROXY_SOURCES["geonode"], timeout=15)
            data = resp.json()
            proxies = []
            for item in data.get("data", []):
                ip = item.get("ip")
                port = item.get("port")
                if ip and port:
                    proxies.append(f"{ip}:{port}")
            return proxies
        except Exception as e:
            print(f"GeoNode 錯誤: {e}")
            return []
    
    def fetch_proxies_github(self):
        """從 GitHub 獲取代理"""
        try:
            resp = requests.get(PROXY_SOURCES["free_proxy_list"], timeout=15)
            return resp.text.strip().split('\n')
        except Exception as e:
            print(f"GitHub 錯誤: {e}")
            return []
    
    def test_proxy(self, proxy, test_url="https://httpbin.org/ip"):
        """測試代理是否可用"""
        proxies = {
            "http": f"http://{proxy}",
            "https": f"http://{proxy}"
        }
        try:
            resp = requests.get(test_url, proxies=proxies, timeout=10)
            if resp.status_code == 200:
                return True
        except:
            pass
        return False
    
    def test_platform_access(self, proxy, platform_url):
        """測試平台是否可通過代理訪問"""
        proxies = {
            "http": f"http://{proxy}",
            "https": f"http://{proxy}"
        }
        try:
            resp = requests.get(platform_url, proxies=proxies, timeout=15)
            if "Access Denied" in resp.text or "Error 16" in resp.text:
                return False, "blocked"
            elif resp.status_code == 200:
                return True, "ok"
        except Exception as e:
            return False, str(e)
        return False, "unknown"
    
    def find_working_proxies(self, limit=10):
        """尋找可用代理"""
        print("🔍 正在獲取代理列表...")
        
        # 從多個來源獲取
        all_proxies = []
        all_proxies.extend(self.fetch_proxies_geonode())
        all_proxies.extend(self.fetch_proxies_github())
        
        print(f"📊 獲取到 {len(all_proxies)} 個代理")
        
        # 測試代理
        working = []
        for i, proxy in enumerate(all_proxies[:50]):  # 只測試前 50 個
            print(f"測試代理 {i+1}/50: {proxy}", end=" ")
            if self.test_proxy(proxy):
                print("✅")
                working.append(proxy)
                if len(working) >= limit:
                    break
            else:
                print("❌")
        
        self.working_proxies = working
        self.status["working_proxies"] = working
        self.save_status()
        
        return working
    
    def attempt_platform_access(self, platform_name, platform_url):
        """嘗試訪問平台"""
        print(f"\n🎯 嘗試訪問 {platform_name}...")
        
        for proxy in self.working_proxies:
            success, result = self.test_platform_access(proxy, platform_url)
            if success:
                print(f"✅ {platform_name} 可通過 {proxy} 訪問")
                self.status["platform_results"][platform_name] = {
                    "proxy": proxy,
                    "status": "accessible",
                    "timestamp": datetime.now().isoformat()
                }
                self.save_status()
                return True, proxy
        
        print(f"❌ {platform_name} 所有代理都被阻擋")
        self.status["platform_results"][platform_name] = {
            "status": "blocked",
            "timestamp": datetime.now().isoformat()
        }
        self.save_status()
        return False, None
    
    def run_breakthrough(self):
        """執行突破嘗試"""
        print("="*60)
        print(f"🚀 IP 阻擋突破方案 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*60)
        
        # 1. 尋找可用代理
        working_proxies = self.find_working_proxies(limit=10)
        
        if not working_proxies:
            print("\n❌ 沒有找到可用代理")
            print("📋 建議：")
            print("  1. 等待 24 小時讓 IP 冷卻")
            print("  2. 使用付費 VPN/代理服務")
            print("  3. 在 Windows 本機操作")
            return False
        
        print(f"\n✅ 找到 {len(working_proxies)} 個可用代理")
        
        # 2. 嘗試訪問平台
        platforms = {
            "qmee": "https://www.qmee.com",
            "prizerebel": "https://www.prizerebel.com",
            "swagbucks": "https://www.swagbucks.com"
        }
        
        for name, url in platforms.items():
            self.attempt_platform_access(name, url)
        
        # 3. 生成報告
        self.generate_report()
        
        return True
    
    def generate_report(self):
        """生成突破報告"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "working_proxies_count": len(self.working_proxies),
            "platform_results": self.status.get("platform_results", {}),
            "next_steps": []
        }
        
        # 根據結果提供建議
        accessible = [p for p, r in self.status.get("platform_results", {}).items() if r.get("status") == "accessible"]
        blocked = [p for p, r in self.status.get("platform_results", {}).items() if r.get("status") == "blocked"]
        
        if accessible:
            report["next_steps"].append(f"可通過代理訪問：{', '.join(accessible)}")
            report["next_steps"].append("建議：使用可用代理進行問卷自動化")
        
        if blocked:
            report["next_steps"].append(f"仍被阻擋：{', '.join(blocked)}")
        
        report["next_steps"].append("持續監控 Prolific 候補名單狀態")
        
        # 儲存報告
        with open("breakthrough_report.json", 'w') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print("\n" + "="*60)
        print("📊 突破報告")
        print("="*60)
        print(f"可用代理：{len(self.working_proxies)} 個")
        print(f"可訪問平台：{len(accessible)} 個")
        print(f"仍被阻擋：{len(blocked)} 個")
        print("\n📋 下一步：")
        for step in report["next_steps"]:
            print(f"  • {step}")
        
        return report


if __name__ == "__main__":
    breakthrough = IPBreakthrough()
    breakthrough.run_breakthrough()
