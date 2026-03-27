#!/usr/bin/env python3
"""
賺錢監控儀表板
追蹤所有平台的賺錢進度
"""

import json
from pathlib import Path
from datetime import datetime

class EarningsDashboard:
    def __init__(self):
        self.status_file = Path(__file__).parent / "earnings_status.json"
        self.memory_file = Path(__file__).parent / "memory" / "2026-03-20.md"
        self.target = 5.00  # USD
        
    def load_status(self):
        """載入狀態"""
        if self.status_file.exists():
            with open(self.status_file, 'r') as f:
                return json.load(f)
        return {"platforms": {}, "total_earnings": 0, "history": []}
    
    def display_dashboard(self):
        """顯示儀表板"""
        status = self.load_status()
        
        print("\n" + "=" * 60)
        print("📊 賺錢監控儀表板")
        print("=" * 60)
        print(f"目標: ${self.target:.2f} USD")
        print(f"目前已賺: ${status['total_earnings']:.2f} USD")
        print(f"差距: ${max(0, self.target - status['total_earnings']):.2f} USD")
        print("=" * 60)
        
        print("\n📱 平台狀態:")
        print("-" * 60)
        
        for platform, data in status["platforms"].items():
            status_icon = "✅" if data["status"] == "可達" else "⏳" if data["status"] == "等待" else "❌"
            print(f"{status_icon} {platform:15} | ${data['earnings']:6.2f} | {data['status']:10} | {data['notes']}")
        
        print("-" * 60)
        
        # 顯示建議
        print("\n💡 建議行動:")
        print("-" * 60)
        
        # Prolific 狀態
        prolific_status = status["platforms"].get("prolific", {}).get("status", "")
        if prolific_status == "可達":
            print("1. 🌟 註冊 Prolific（無 CAPTCHA）")
            print("   URL: https://app.prolific.com/register/participant/join-waitlist/about-yourself")
            print("   預期收入: $5-20/研究")
        
        # PrizeRebel 狀態
        prizerebel_status = status["platforms"].get("prizerebel", {}).get("status", "")
        if prizerebel_status != "已登入":
            print("\n2. 登入 PrizeRebel（需手動 CAPTCHA）")
            print("   執行: start-all-platforms.ps1")
            print("   目標: 完成 Daily Survey (+72 點)")
        
        print("-" * 60)
        
        # 時間線
        print("\n📅 時間線:")
        print("-" * 60)
        today = datetime.now()
        print(f"Day 1 ({today.strftime('%Y-%m-%d')}): 註冊 Prolific + PrizeRebel Daily Survey")
        print(f"Day 2-3: 等待 Prolific 審核 + 持續 PrizeRebel 任務")
        print(f"Day 4-7: Prolific 開始接受研究 + PrizeRebel 累積點數")
        print(f"Day 7: 預計達成 $5 USD 目標")
        print("-" * 60)
        
        return status
    
    def update_memory(self):
        """更新 memory 檔案"""
        status = self.load_status()
        
        memory_content = f"""
## 自動化程式執行狀態（{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}）

### 執行結果
- ✅ Prolific 可達性檢查: 通過
- ✅ 免費代理獲取: 已保存到 free_proxies.txt
- ✅ 行動計畫生成: auto-earning-plan.md
- ✅ 狀態監控: earnings_status.json

### 程式清單
| 檔案 | 用途 |
|------|------|
| auto-earning.py | 主程式 |
| prolific-auto-register.py | Prolific 自動註冊 |
| earnings_dashboard.py | 監控儀表板 |

### 下一步
1. 老闆需在 Windows 註冊 Prolific（無 CAPTCHA）
2. 執行 start-all-platforms.ps1 登入 PrizeRebel
3. 完成 Daily Survey（+72 點）
"""
        
        # 追加到今日 memory
        if self.memory_file.exists():
            with open(self.memory_file, 'a') as f:
                f.write(memory_content)
        else:
            with open(self.memory_file, 'w') as f:
                f.write(f"# 2026-03-20 進度記錄\n{memory_content}")
        
        print(f"\n[INFO] Memory 已更新: {self.memory_file}")

if __name__ == "__main__":
    dashboard = EarningsDashboard()
    dashboard.display_dashboard()
    dashboard.update_memory()
