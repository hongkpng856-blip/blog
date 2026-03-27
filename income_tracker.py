#!/usr/bin/env python3
"""
收入追蹤系統 - 追蹤所有賺錢平台的進度
"""

import json
from pathlib import Path
from datetime import datetime

class IncomeTracker:
    def __init__(self):
        self.workspace = Path("/home/claw/.openclaw/workspace")
        self.tracker_file = self.workspace / "income_tracker.json"
        self.target_usd = 5.00
        
        # 載入現有狀態
        self.status = self.load_status()
    
    def load_status(self):
        if self.tracker_file.exists():
            try:
                with open(self.tracker_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {
            "target": self.target_usd,
            "current": 0.0,
            "sources": {},
            "history": []
        }
    
    def save_status(self):
        with open(self.tracker_file, 'w') as f:
            json.dump(self.status, f, indent=2)
    
    def add_income(self, source: str, amount: float, note: str = ""):
        """新增收入記錄"""
        timestamp = datetime.now().isoformat()
        
        if source not in self.status["sources"]:
            self.status["sources"][source] = {"total": 0.0, "records": []}
        
        self.status["sources"][source]["total"] += amount
        self.status["sources"][source]["records"].append({
            "amount": amount,
            "timestamp": timestamp,
            "note": note
        })
        
        self.status["current"] += amount
        self.status["history"].append({
            "source": source,
            "amount": amount,
            "timestamp": timestamp,
            "note": note
        })
        
        self.save_status()
        
        print(f"✅ 已記錄: {source} +${amount:.2f} USD")
        self.show_progress()
    
    def show_progress(self):
        """顯示進度"""
        current = self.status["current"]
        target = self.status["target"]
        gap = max(0, target - current)
        percent = min(100, (current / target) * 100)
        
        print("\n" + "=" * 50)
        print("📊 收入追蹤")
        print("=" * 50)
        print(f"目標: ${target:.2f} USD")
        print(f"目前: ${current:.2f} USD")
        print(f"差距: ${gap:.2f} USD")
        print(f"進度: {percent:.1f}%")
        print("=" * 50)
        
        if self.status["sources"]:
            print("\n📋 收入來源:")
            for source, data in self.status["sources"].items():
                print(f"  • {source}: ${data['total']:.2f} USD")
    
    def generate_report(self):
        """生成報告"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "target": self.status["target"],
            "current": self.status["current"],
            "gap": max(0, self.status["target"] - self.status["current"]),
            "sources": self.status["sources"],
            "status": "達成" if self.status["current"] >= self.status["target"] else "進行中"
        }
        
        return report

if __name__ == "__main__":
    tracker = IncomeTracker()
    tracker.show_progress()
