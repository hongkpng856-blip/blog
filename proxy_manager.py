#!/usr/bin/env python3
"""
Proxy 管理器
功能：管理、驗證、自動更新 Proxy 列表
"""

import json
import time
import requests
from pathlib import Path
from datetime import datetime
from typing import List, Optional

class ProxyManager:
    def __init__(self, cache_file: str = "proxy_cache.json"):
        self.cache_file = Path(cache_file)
        self.proxies = []
        self.working_proxies = []
        self.load_cache()
    
    def load_cache(self):
        """載入快取的 Proxy"""
        if self.cache_file.exists():
            with open(self.cache_file, 'r') as f:
                data = json.load(f)
                self.working_proxies = data.get("working_proxies", [])
                print(f"✅ 從快載入 {len(self.working_proxies)} 個可用 Proxy")
    
    def save_cache(self):
        """儲存 Proxy 快取"""
        data = {
            "last_update": datetime.now().isoformat(),
            "working_proxies": self.working_proxies
        }
        with open(self.cache_file, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"💾 已儲存 {len(self.working_proxies)} 個可用 Proxy")
    
    def fetch_from_source(self, source_url: str) -> List[str]:
        """從單一來源獲取 Proxy"""
        try:
            resp = requests.get(source_url, timeout=15)
            if resp.status_code == 200:
                proxies = []
                for line in resp.text.strip().split('\n'):
                    line = line.strip()
                    if ':' in line and len(line) < 30:
                        proxies.append(line)
                return proxies
        except:
            pass
        return []
    
    def fetch_all_sources(self) -> List[str]:
        """從所有來源獲取 Proxy"""
        sources = [
            "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all",
            "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
            "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
            "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/proxy.txt"
        ]
        
        all_proxies = []
        for source in sources:
            print(f"📥 獲取中: {source[:50]}...")
            proxies = self.fetch_from_source(source)
            all_proxies.extend(proxies)
            print(f"  → 獲取 {len(proxies)} 個")
            time.sleep(0.5)
        
        # 去重
        all_proxies = list(set(all_proxies))
        print(f"\n📊 總計: {len(all_proxies)} 個唯一 Proxy")
        return all_proxies
    
    def validate_proxy(self, proxy: str) -> bool:
        """驗證 Proxy 是否可用"""
        test_url = "https://httpbin.org/ip"
        proxies = {
            "http": f"http://{proxy}",
            "https": f"http://{proxy}"
        }
        
        try:
            resp = requests.get(test_url, proxies=proxies, timeout=10)
            return resp.status_code == 200
        except:
            return False
    
    def validate_batch(self, proxies: List[str], max_valid: int = 20) -> List[str]:
        """批量驗證 Proxy"""
        import random
        
        valid = []
        # 隨機抽樣測試
        sample = random.sample(proxies, min(100, len(proxies)))
        
        print(f"\n🔍 測試 {len(sample)} 個 Proxy...")
        
        for i, proxy in enumerate(sample):
            if len(valid) >= max_valid:
                break
            
            if (i + 1) % 10 == 0:
                print(f"  進度: {i+1}/{len(sample)}, 可用: {len(valid)}")
            
            if self.validate_proxy(proxy):
                valid.append(proxy)
        
        print(f"\n✅ 找到 {len(valid)} 個可用 Proxy")
        return valid
    
    def refresh(self, max_valid: int = 20) -> List[str]:
        """刷新 Proxy 列表"""
        print("🔄 正在刷新 Proxy 列表...")
        
        proxies = self.fetch_all_sources()
        if proxies:
            valid = self.validate_batch(proxies, max_valid)
            self.working_proxies = valid
            self.save_cache()
        
        return self.working_proxies
    
    def get_proxy(self, index: int = 0) -> Optional[str]:
        """取得指定索引的 Proxy"""
        if self.working_proxies and 0 <= index < len(self.working_proxies):
            return self.working_proxies[index]
        return None
    
    def get_random_proxy(self) -> Optional[str]:
        """取得隨機 Proxy"""
        import random
        if self.working_proxies:
            return random.choice(self.working_proxies)
        return None


def main():
    """主程式"""
    print("=" * 50)
    print("🔧 Proxy 管理器")
    print("=" * 50)
    
    manager = ProxyManager()
    
    # 如果快取為空或過期，刷新
    if not manager.working_proxies:
        manager.refresh(max_valid=10)
    
    print(f"\n📋 可用 Proxy 列表 ({len(manager.working_proxies)} 個):")
    for i, proxy in enumerate(manager.working_proxies):
        print(f"  {i+1}. {proxy}")


if __name__ == "__main__":
    main()
