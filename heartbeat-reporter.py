#!/usr/bin/env python3
import time
import subprocess
import sys

SESSION = "agent:main:telegram:direct:5396608205"
INTERVAL = 300  # 5 minutes

def send_heartbeat():
    try:
        result = subprocess.run(
            ["openclaw", "session", "send", "--session", SESSION, "--message", "🫀 HEARTBEAT - 請匯報目前進度"],
            capture_output=True,
            text=True,
            timeout=30
        )
        timestamp = time.strftime("%H:%M:%S")
        if result.returncode == 0:
            print(f"[{timestamp}] ✅ Heartbeat sent")
        else:
            print(f"[{timestamp}] ❌ Failed: {result.stderr}")
    except Exception as e:
        print(f"[{time.strftime('%H:%M:%S')}] ❌ Error: {e}")

if __name__ == "__main__":
    print("🚀 Heartbeat Reporter 啟動")
    print(f"📅 頻率: 每 {INTERVAL//60} 分鐘")
    print("───")
    while True:
        send_heartbeat()
        time.sleep(INTERVAL)