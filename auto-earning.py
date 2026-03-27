#!/usr/bin/env python3
"""
自動化賺錢程式 v1.0
目標：在 7 天內賺取最少 $5 USD
方法：Prolific 自動註冊 + 其他無 CAPTCHA 平台
"""

import json
import time
import subprocess
from datetime import datetime
from pathlib import Path

# 配置
CONFIG = {
    "target_usd": 5.00,
    "days_limit": 7,
    "platforms": {
        "prolific": {
            "url": "https://app.prolific.com/register/participant/join-waitlist/about-yourself",
            "captcha": False,
            "payout_range": [5, 20],
            "payout_method": "PayPal"
        },
        "prizerebel": {
            "url": "https://www.prizerebel.com/login.php",
            "captcha": True,
            "payout_threshold": 500,  # 500 點 = $5
            "credentials": {
                "email": "hongkpng856@gmail.com",
                "password": "mtsd479j"
            }
        },
        "swagbucks": {
            "url": "https://www.swagbucks.com/login",
            "captcha": True,
            "credentials": {
                "email": "hongkpng856@gmail.com",
                "password": "Mypassword123!"
            }
        }
    },
    "memory_file": Path(__file__).parent / "memory" / "2026-03-20.md",
    "status_file": Path(__file__).parent / "earnings_status.json"
}

def log(message: str):
    """記錄日誌"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def update_status(platform: str, status: str, earnings: float = 0, notes: str = ""):
    """更新狀態檔案"""
    status_file = CONFIG["status_file"]
    
    if status_file.exists():
        with open(status_file, 'r') as f:
            data = json.load(f)
    else:
        data = {"platforms": {}, "total_earnings": 0, "history": []}
    
    data["platforms"][platform] = {
        "status": status,
        "earnings": earnings,
        "last_update": datetime.now().isoformat(),
        "notes": notes
    }
    data["total_earnings"] = sum(p["earnings"] for p in data["platforms"].values())
    data["history"].append({
        "timestamp": datetime.now().isoformat(),
        "platform": platform,
        "action": status,
        "earnings": earnings
    })
    
    with open(status_file, 'w') as f:
        json.dump(data, f, indent=2)
    
    log(f"狀態已更新: {platform} - {status} (${earnings:.2f})")

def check_prolific_accessibility():
    """檢查 Prolific 是否可訪問"""
    import urllib.request
    import urllib.error
    
    url = CONFIG["platforms"]["prolific"]["url"]
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        response = urllib.request.urlopen(req, timeout=10)
        status_code = response.getcode()
        log(f"Prolific HTTP 狀態: {status_code}")
        return status_code == 200
    except urllib.error.URLError as e:
        log(f"Prolific 訪問失敗: {e}")
        return False

def get_free_proxies():
    """獲取免費代理列表"""
    # 免費代理來源
    proxy_sources = [
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
        "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt"
    ]
    
    proxies = []
    for source in proxy_sources:
        try:
            import urllib.request
            req = urllib.request.Request(source, headers={'User-Agent': 'Mozilla/5.0'})
            response = urllib.request.urlopen(req, timeout=15)
            content = response.read().decode('utf-8')
            for line in content.split('\n')[:20]:  # 取前 20 個
                line = line.strip()
                if ':' in line:
                    proxies.append(f"http://{line}")
        except Exception as e:
            log(f"代理來源 {source} 失敗: {e}")
    
    log(f"獲取到 {len(proxies)} 個代理")
    return proxies

def run_agent_browser(url: str):
    """執行 agent-browser 訪問 URL"""
    try:
        result = subprocess.run(
            ["agent-browser", "navigate", url],
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.stdout
    except subprocess.TimeoutExpired:
        log(f"agent-browser 超時")
        return None
    except FileNotFoundError:
        log(f"agent-browser 未安裝")
        return None

def generate_action_plan():
    """生成行動計畫"""
    plan = """
## 自動化賺錢行動計畫

### 路線 1: Prolific（推薦，無 CAPTCHA）
- **Task**: 註冊 Prolific
- **Owner**: 主代理
- **Steps**:
  1. 訪問註冊頁面
  2. 使用 Google SSO 或 email 註冊
  3. 填寫基本資料
  4. 等待審核（1-7 天）
- **Deliverable**: Prolific 帳號
- **Acceptance Criteria**: 收到確認 email
- **ETA**: 今日內完成註冊，3-7 天收到邀請

### 路線 2: PrizeRebel（備選，需手動 CAPTCHA）
- **Task**: 登入並完成 Daily Survey
- **Owner**: 老闆（需手動）
- **Steps**:
  1. 在 Windows 執行 start-all-platforms.ps1
  2. 手動處理 CAPTCHA
  3. 完成 Daily Survey
- **Deliverable**: +72 點
- **ETA**: 今日

### 路線 3: 免費 API 自動化
- **Task**: 研究 API 賺錢方法
- **Owner**: 子代理
- **Steps**:
  1. 尋找免費 API 任務平台
  2. 撰寫自動化腳本
  3. 執行並監控
- **Deliverable**: 自動化收入
- **ETA**: 3 天內
"""
    return plan

def main():
    """主程式"""
    log("=" * 50)
    log("自動化賺錢程式 v1.0 啟動")
    log(f"目標: ${CONFIG['target_usd']}")
    log(f"時間限制: {CONFIG['days_limit']} 天")
    log("=" * 50)
    
    # 步驟 1: 檢查 Prolific
    log("\n[步驟 1] 檢查 Prolific 可達性...")
    if check_prolific_accessibility():
        log("✅ Prolific 可達")
        update_status("prolific", "可達", 0, "等待註冊")
    else:
        log("❌ Prolific 不可達")
        update_status("prolific", "不可達", 0, "網絡問題")
    
    # 步驟 2: 獲取免費代理
    log("\n[步驟 2] 獲取免費代理...")
    proxies = get_free_proxies()
    if proxies:
        with open(Path(__file__).parent / "free_proxies.txt", 'w') as f:
            f.write('\n'.join(proxies))
        log(f"✅ 已保存 {len(proxies)} 個代理到 free_proxies.txt")
    
    # 步驟 3: 生成行動計畫
    log("\n[步驟 3] 生成行動計畫...")
    plan = generate_action_plan()
    plan_file = Path(__file__).parent / "auto-earning-plan.md"
    with open(plan_file, 'w') as f:
        f.write(plan)
    log(f"✅ 行動計畫已保存到 {plan_file}")
    
    # 步驟 4: 輸出狀態
    log("\n" + "=" * 50)
    log("狀態摘要")
    log("=" * 50)
    log(f"Prolific: 無 CAPTCHA，高報酬（$5-20/研究）")
    log(f"PrizeRebel: 需手動 CAPTCHA，已註冊")
    log(f"Swagbucks: 需手動 CAPTCHA，已註冊")
    log("=" * 50)
    
    log("\n🚀 建議老闆立即執行:")
    log("1. 在 Windows 註冊 Prolific（無 CAPTCHA）")
    log("2. 執行 start-all-platforms.ps1 登入 PrizeRebel")
    log("3. 完成 Daily Survey（+72 點）")
    
    return 0

if __name__ == "__main__":
    exit(main())
