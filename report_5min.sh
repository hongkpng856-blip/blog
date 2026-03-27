#!/usr/bin/env bash
# report_5min.sh - 每 5 分鐘產生系統與業務簡報，並透過 Telegram Bot 推送

# ==== 設定 ==== 
# 替換下面的 YOUR_TELEGRAM_BOT_TOKEN 與 YOUR_CHAT_ID 為實際值
BOT_TOKEN="YOUR_TELEGRAM_BOT_TOKEN"
CHAT_ID="YOUR_CHAT_ID"

# 收集資訊 (可自行擴充) 
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
CPU_LOAD=$(uptime | awk -F'load average:' '{print $2}' | cut -d',' -f1 | xargs)
MEM_USAGE=$(free -m | awk '/Mem:/ {printf "%.1f%%", $3/$2*100}')
DISK_USAGE=$(df -h / | awk 'NR==2 {print $5}')
# 假設有收入/任務指標，這裡以檔案方式示範 (自行替換)
INCOME=$(cat /tmp/daily_income.txt 2>/dev/null || echo "0")
TASK_PENDING=$(cat /tmp/pending_tasks.txt 2>/dev/null || echo "0")

# 組合訊息
MESSAGE="📊 每 5 分鐘報告\n時間: $TIMESTAMP\nCPU Load: $CPU_LOAD\n記憶體使用率: $MEM_USAGE\n磁碟使用率: $DISK_USAGE\n今日收入: $INCOME\n待處理任務: $TASK_PENDING"

# 發送至 Telegram
curl -s -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendMessage" \
    -d chat_id=${CHAT_ID} \
    -d text="${MESSAGE}" \
    -d parse_mode=Markdown > /dev/null

# 若 curl 失敗，寫入錯誤日誌
if [ $? -ne 0 ]; then
    echo "${TIMESTAMP} - Telegram 發送失敗" >> /home/claw/.openclaw/workspace/log/report_error.log
fi
