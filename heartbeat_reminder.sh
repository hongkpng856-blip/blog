#!/usr/bin/env bash
# heartbeat_reminder.sh - 每 5 分鐘寫入提醒訊息，供 Agent 自行檢查

REMINDER_FILE="/home/claw/.openclaw/workspace/reminder_5min.txt"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
echo "${TIMESTAMP} - 請回報 5 分鐘更新" >> "${REMINDER_FILE}"
