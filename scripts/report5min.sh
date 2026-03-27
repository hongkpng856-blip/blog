#!/usr/bin/env bash
# 5 分鐘回報子代理腳本
# 取得當前會話的 session key（在此環境中直接寫死）
SESSION_KEY="agent:main:telegram:direct:5396608205"

while true; do
  # 產生回報內容（可自行根據 Memory 擴充）
  TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
  REPORT="🕒 ${TIMESTAMP}\n✅ 5 分鐘自動回報已觸發。"
  # 送回原始會話
  openclaw message send --channel telegram --to telegram:5396608205 --message "$REPORT"
  # 等待 300 秒（5 分鐘）
  sleep 300
done
