#!/usr/bin/env python3
"""
多 IP 切換 BOT
功能：使用不同 IP 訪問網站，自動切換 Proxy
"""

import requests
import time
import random
from typing import List, Optional
import json
from datetime import datetime

class MultiIPBot:
    def __init__(self):
        self.current_proxy = None
        self.proxy_list = []
        self.working_proxies = []
        self.session = requests.Session()
        
    def load_free_proxies(self) -> List[str]:
        """從多個免費 Proxy 來源獲取列表"""
        proxies = []
        
        # 免費 Proxy 來源（這些是常見的免費 Proxy API）
        proxy_sources = [
            "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all",
            "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
            "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt"
        ]
        
        for source in proxy_sources:
            try:
                print(f"📥 正在從 {source} 獲取 Proxy 列表...")
                resp = requests.get(source, timeout=15)
                if resp.status_code == 200:
                    lines = resp.text.strip().split('\n')
                    for line in lines:
                        line = line.strip()
                        if ':' in line:
                            proxies.append(line)
                    print(f"✅ 獲取 {len(lines)} 個 Proxy")
            except Exception as e:
                print(f"⚠️ 無法從 {source} 獲取: {e}")
        
        # 去重
        proxies = list(set(proxies))
        print(f"\n📊 總共獲取 {len(proxies)} 個唯一 Proxy")
        
        return proxies
    
    def test_proxy(self, proxy: str, test_url: str = "https://httpbin.org/ip") -> bool:
        """測試單個 Proxy 是否可用"""
        proxies = {
            "http": f"http://{proxy}",
            "https": f"http://{proxy}"
        }
        
        try:
            start_time = time.time()
            resp = requests.get(test_url, proxies=proxies, timeout=10)
            elapsed = time.time() - start_time
            
            if resp.status_code == 200:
                print(f"✅ {proxy} - 可用（延遲: {elapsed:.2f}s）")
                return True
        except:
            pass
        
        return False
    
    def find_working_proxies(self, max_proxies: int = 10) -> List[str]:
        """找出可用的 Proxy"""
        print(f"\n🔍 正在測試 Proxy 可用性...")
        
        self.proxy_list = self.load_free_proxies()
        working = []
        
        # 隨機選擇測試（避免測試太多）
        test_count = min(50, len(self.proxy_list))
        test_proxies = random.sample(self.proxy_list, test_count)
        
        for i, proxy in enumerate(test_proxies):
            print(f"[{i+1}/{test_count}] 測試 {proxy}...", end=" ")
            if self.test_proxy(proxy):
                working.append(proxy)
                if len(working) >= max_proxies:
                    break
        
        print(f"\n✅ 找到 {len(working)} 個可用 Proxy")
        self.working_proxies = working
        return working
    
    def visit_website(self, url: str, proxy: Optional[str] = None) -> dict:
        """使用指定 Proxy 訪問網站"""
        result = {
            "url": url,
            "proxy": proxy,
            "success": False,
            "status_code": None,
            "response_time": None,
            "error": None,
            "timestamp": datetime.now().isoformat()
        }
        
        proxies = None
        if proxy:
            proxies = {
                "http": f"http://{proxy}",
                "https": f"http://{proxy}"
            }
        
        try:
            start_time = time.time()
            resp = self.session.get(url, proxies=proxies, timeout=15)
            elapsed = time.time() - start_time
            
            result["status_code"] = resp.status_code
            result["response_time"] = round(elapsed, 2)
            
            # 檢查是否被阻擋
            if "Access Denied" in resp.text or "Error 16" in resp.text:
                result["error"] = "Blocked by security service"
            else:
                result["success"] = True
                
        except Exception as e:
            result["error"] = str(e)
        
        return result
    
    def rotate_and_visit(self, url: str, visits: int = 5, delay: float = 2.0) -> List[dict]:
        """輪換 IP 並多次訪問網站"""
        results = []
        
        if not self.working_proxies:
            self.find_working_proxies()
        
        if not self.working_proxies:
            print("❌ 沒有可用的 Proxy")
            return results
        
        print(f"\n🌐 開始使用 {min(visits, len(self.working_proxies))} 個不同 IP 訪問 {url}")
        
        for i in range(min(visits, len(self.working_proxies))):
            proxy = self.working_proxies[i]
            print(f"\n[{i+1}/{visits}] 使用 Proxy: {proxy}")
            
            result = self.visit_website(url, proxy)
            results.append(result)
            
            if result["success"]:
                print(f"✅ 訪問成功（狀態: {result['status_code']}, 延遲: {result['response_time']}s）")
            else:
                print(f"❌ 訪問失敗: {result['error']}")
            
            if i < visits - 1:
                print(f"⏳ 等待 {delay} 秒...")
                time.sleep(delay)
        
        return results
    
    def save_results(self, results: List[dict], filename: str = "visit_results.json"):
        """儲存訪問結果"""
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"\n💾 結果已儲存到 {filename}")


def main():
    """主程式"""
    print("=" * 60)
    print("🌐 多 IP 切換 BOT")
    print("=" * 60)
    
    bot = MultiIPBot()
    
    # 找可用 Proxy
    bot.find_working_proxies(max_proxies=10)
    
    if not bot.working_proxies:
        print("\n❌ 沒有找到可用的 Proxy，請稍後再試")
        return
    
    # 測試網站
    test_url = "https://httpbin.org/ip"
    print(f"\n🧪 測試網站: {test_url}")
    
    # 使用不同 IP 訪問
    results = bot.rotate_and_visit(test_url, visits=3, delay=1.0)
    
    # 儲存結果
    bot.save_results(results)
    
    # 統計
    success_count = sum(1 for r in results if r["success"])
    print(f"\n📊 統計:")
    print(f"  總訪問: {len(results)}")
    print(f"  成功: {success_count}")
    print(f"  失敗: {len(results) - success_count}")


if __name__ == "__main__":
    main()
