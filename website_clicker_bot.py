#!/usr/bin/env python3
"""
網站點擊 BOT
功能：使用不同 IP 自動點擊網站
"""

import time
import json
from typing import List
from proxy_manager import ProxyManager
from datetime import datetime

class WebsiteClickerBot:
    def __init__(self):
        self.proxy_manager = ProxyManager()
        self.visit_log = []
    
    def click_website(self, url: str, proxy: str = None) -> dict:
        """使用指定 Proxy 點擊網站"""
        import requests
        
        result = {
            "url": url,
            "proxy": proxy,
            "timestamp": datetime.now().isoformat(),
            "success": False,
            "status": None,
            "error": None
        }
        
        proxies = None
        if proxy:
            proxies = {
                "http": f"http://{proxy}",
                "https": f"http://{proxy}"
            }
        
        try:
            # 模擬瀏覽器標頭
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Connection": "keep-alive"
            }
            
            resp = requests.get(url, proxies=proxies, headers=headers, timeout=15)
            result["status"] = resp.status_code
            result["success"] = resp.status_code == 200
            
            if "Access Denied" in resp.text:
                result["error"] = "Blocked by security"
                result["success"] = False
                
        except Exception as e:
            result["error"] = str(e)
        
        return result
    
    def multi_click(self, url: str, clicks: int = 5, delay: float = 2.0) -> List[dict]:
        """使用不同 IP 多次點擊網站"""
        results = []
        
        # 確保有可用 Proxy
        if not self.proxy_manager.working_proxies:
            print("🔄 正在獲取可用 Proxy...")
            self.proxy_manager.refresh(max_valid=clicks)
        
        available = self.proxy_manager.working_proxies[:clicks]
        
        if not available:
            print("❌ 沒有可用的 Proxy")
            return results
        
        print(f"\n🌐 開始使用 {len(available)} 個不同 IP 點擊網站")
        print(f"📍 目標: {url}")
        print("-" * 50)
        
        for i, proxy in enumerate(available):
            print(f"\n[{i+1}/{len(available)}] 使用 Proxy: {proxy}")
            
            result = self.click_website(url, proxy)
            results.append(result)
            
            if result["success"]:
                print(f"✅ 成功（狀態: {result['status']}）")
            else:
                print(f"❌ 失敗: {result['error']}")
            
            if i < len(available) - 1:
                print(f"⏳ 等待 {delay} 秒...")
                time.sleep(delay)
        
        return results
    
    def save_log(self, filename: str = "click_log.json"):
        """儲存點擊記錄"""
        with open(filename, 'w') as f:
            json.dump(self.visit_log, f, indent=2, ensure_ascii=False)
        print(f"\n💾 記錄已儲存到 {filename}")
    
    def generate_report(self, results: List[dict]):
        """生成報告"""
        total = len(results)
        success = sum(1 for r in results if r["success"])
        failed = total - success
        
        print("\n" + "=" * 50)
        print("📊 點擊報告")
        print("=" * 50)
        print(f"總點擊: {total}")
        print(f"成功: {success}")
        print(f"失敗: {failed}")
        print(f"成功率: {(success/total*100):.1f}%" if total > 0 else "N/A")
        
        return {
            "total": total,
            "success": success,
            "failed": failed,
            "success_rate": round(success/total*100, 1) if total > 0 else 0
        }


def main():
    """主程式"""
    print("=" * 60)
    print("🖱️ 網站點擊 BOT")
    print("=" * 60)
    
    bot = WebsiteClickerBot()
    
    # 目標網站
    target_url = input("\n請輸入目標網站 URL: ").strip()
    if not target_url:
        target_url = "https://httpbin.org/ip"
        print(f"使用預設測試網站: {target_url}")
    
    # 點擊次數
    clicks_input = input("請輸入點擊次數 (預設 5): ").strip()
    clicks = int(clicks_input) if clicks_input.isdigit() else 5
    
    # 執行
    results = bot.multi_click(target_url, clicks=clicks, delay=2.0)
    
    # 報告
    bot.generate_report(results)
    
    # 儲存記錄
    bot.visit_log.extend(results)
    bot.save_log()


if __name__ == "__main__":
    main()