#!/bin/bash
# 啟動點擊追蹤網站

echo "🌐 啟動點擊追蹤網站..."
cd /home/claw/.openclaw/workspace

# 檢查 Flask 是否已安裝
if ! python3 -c "import flask" 2>/dev/null; then
    echo "📦 安裝 Flask..."
    pip3 install flask
fi

# 啟動網站
python3 click_tracker_website.py
