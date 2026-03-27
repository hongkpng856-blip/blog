#!/usr/bin/env python3
"""
Agent Browser 自動化賺錢控制器
使用 Agent Browser 完成無 CAPTCHA 平台的註冊和任務
"""

import subprocess
import json
import time
from pathlib import Path
from datetime import datetime

class AgentBrowserController:
    def __init__(self):
        self.workspace = Path("/home/claw/.openclaw/workspace")
        self.log_file = self.workspace / "agent_browser_log.json"
        self.status_file = self.workspace / "earnings_status.json"
        
    def run_command(self, cmd: str, timeout: int = 30) -> dict:
        """執行 agent-browser 命令"""
        result = {"command": cmd, "timestamp": datetime.now().isoformat()}
        try:
            proc = subprocess.run(
                f"agent-browser {cmd}",
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=str(self.workspace)
            )
            result["success"] = proc.returncode == 0
            result["stdout"] = proc.stdout[:2000] if proc.stdout else ""
            result["stderr"] = proc.stderr[:500] if proc.stderr else ""
            result["returncode"] = proc.returncode
        except subprocess.TimeoutExpired:
            result["success"] = False
            result["error"] = "Timeout"
        except Exception as e:
            result["success"] = False
            result["error"] = str(e)
        
        self._log(result)
        return result
    
    def _log(self, data: dict):
        """記錄日誌"""
        logs = []
        if self.log_file.exists():
            try:
                with open(self.log_file, 'r') as f:
                    logs = json.load(f)
            except:
                logs = []
        
        logs.append(data)
        
        with open(self.log_file, 'w') as f:
            json.dump(logs[-100:], f, indent=2)  # 只保留最近 100 條
    
    def navigate(self, url: str) -> dict:
        """導航到 URL"""
        print(f"[NAVIGATE] {url}")
        return self.run_command(f'navigate "{url}"', timeout=60)
    
    def snapshot(self) -> dict:
        """獲取頁面快照"""
        print("[SNAPSHOT] Getting page snapshot...")
        return self.run_command("snapshot", timeout=30)
    
    def click(self, selector: str) -> dict:
        """點擊元素"""
        print(f"[CLICK] {selector}")
        return self.run_command(f'click "{selector}"', timeout=15)
    
    def type_text(self, selector: str, text: str) -> dict:
        """輸入文字"""
        print(f"[TYPE] {selector} <- {text[:20]}...")
        return self.run_command(f'type "{selector}" "{text}"', timeout=15)
    
    def evaluate(self, script: str) -> dict:
        """執行 JavaScript"""
        print(f"[EVAL] {script[:50]}...")
        return self.run_command(f'evaluate "{script}"', timeout=15)
    
    def register_prolific(self) -> dict:
        """嘗試註冊 Prolific"""
        print("\n" + "="*50)
        print("開始 Prolific 註冊流程")
        print("="*50)
        
        results = {"steps": [], "success": False}
        
        # Step 1: 導航到註冊頁面
        result = self.navigate("https://app.prolific.com/register/participant/join-waitlist/about-yourself")
        results["steps"].append({"step": "navigate", "result": result})
        
        if not result.get("success"):
            results["error"] = "無法導航到 Prolific"
            return results
        
        time.sleep(3)
        
        # Step 2: 獲取快照分析頁面
        result = self.snapshot()
        results["steps"].append({"step": "snapshot", "result": result})
        
        # Step 3: 嘗試找到並點擊 Google SSO
        selectors = [
            'button:contains("Google")',
            'button:contains("Sign up with Google")',
            '[data-testid="google-button"]',
            '.google-signin-button',
            'button[aria-label*="Google"]'
        ]
        
        clicked = False
        for selector in selectors:
            result = self.click(selector)
            if result.get("success"):
                clicked = True
                results["steps"].append({"step": "click_google_sso", "selector": selector, "result": result})
                break
        
        if not clicked:
            results["steps"].append({"step": "click_google_sso", "result": "所有選擇器都失敗"})
        
        results["success"] = clicked
        results["message"] = "點擊成功，請檢查是否有新視窗或重定向" if clicked else "需要手動操作"
        
        return results
    
    def check_prizerebel(self) -> dict:
        """檢查 PrizeRebel 狀態"""
        print("\n" + "="*50)
        print("檢查 PrizeRebel 狀態")
        print("="*50)
        
        results = {"steps": []}
        
        # 嘗試訪問登入頁面
        result = self.navigate("https://www.prizerebel.com/login.php")
        results["steps"].append({"step": "navigate_login", "result": result})
        
        time.sleep(2)
        
        # 獲取快照
        result = self.snapshot()
        results["steps"].append({"step": "snapshot", "result": result})
        
        # 檢查是否有 CAPTCHA
        result = self.evaluate("document.body.innerHTML.includes('g-recaptcha') || document.body.innerHTML.includes('captcha')")
        results["steps"].append({"step": "check_captcha", "result": result})
        
        results["has_captcha"] = "true" in str(result.get("stdout", "")).lower()
        
        return results
    
    def run_full_automation(self):
        """執行完整自動化流程"""
        print("\n" + "="*60)
        print("🤖 Agent Browser 自動化賺錢控制器")
        print("="*60)
        print(f"時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*60)
        
        all_results = {
            "timestamp": datetime.now().isoformat(),
            "prolific": None,
            "prizerebel": None
        }
        
        # 執行 Prolific 註冊
        print("\n[1/2] Prolific 註冊流程...")
        all_results["prolific"] = self.register_prolific()
        
        # 檢查 PrizeRebel
        print("\n[2/2] PrizeRebel 狀態檢查...")
        all_results["prizerebel"] = self.check_prizerebel()
        
        # 保存結果
        results_file = self.workspace / "automation_results.json"
        with open(results_file, 'w') as f:
            json.dump(all_results, f, indent=2)
        
        print("\n" + "="*60)
        print("📊 執行結果摘要")
        print("="*60)
        
        print(f"\nProlific:")
        if all_results["prolific"].get("success"):
            print("  ✅ 自動點擊成功")
        else:
            print("  ⏳ 需要手動操作")
        
        print(f"\nPrizeRebel:")
        if all_results["prizerebel"].get("has_captcha"):
            print("  ⚠️ 需要 CAPTCHA（需手動處理）")
        else:
            print("  ❓ 無法確定")
        
        print(f"\n結果已保存: {results_file}")
        
        return all_results

if __name__ == "__main__":
    controller = AgentBrowserController()
    results = controller.run_full_automation()
