#!/bin/bash
# Prolific 自動註冊流程
# 使用 agent-browser 自動化

set -e

echo "========================================"
echo "Prolific 自動註冊流程 v1.0"
echo "========================================"

WORKSPACE="/home/claw/.openclaw/workspace"
URL="https://app.prolific.com/register/participant/join-waitlist/about-yourself"
SCREENSHOT="$WORKSPACE/prolific_page.png"

echo ""
echo "[Step 1] 訪問 Prolific 註冊頁面..."
agent-browser navigate "$URL" --timeout 30000

echo ""
echo "[Step 2] 等待頁面載入..."
sleep 5

echo ""
echo "[Step 3] 獲取頁面快照..."
agent-browser snapshot > "$WORKSPACE/prolific_snapshot.json" 2>&1 || true

echo ""
echo "[Step 4] 分析頁面結構..."
# 嘗試找到註冊按鈕或表單
agent-browser evaluate "document.body.innerHTML" > "$WORKSPACE/prolific_body.html" 2>&1 || true

echo ""
echo "[Step 5] 嘗試點擊 Google SSO（如果存在）..."
# 嘗試找到並點擊 Google 登入按鈕
agent-browser click "button:contains('Google')" 2>&1 || echo "Google SSO 按鈕未找到，可能需要手動操作"

echo ""
echo "[Step 6] 截圖保存..."
agent-browser screenshot "$SCREENSHOT" 2>&1 || echo "截圖功能可能不支援"

echo ""
echo "========================================"
echo "自動化流程完成"
echo "========================================"
echo ""
echo "已生成的檔案："
ls -la "$WORKSPACE"/prolific_* 2>/dev/null || echo "無檔案生成"
echo ""
echo "下一步："
echo "1. 查看 prolific_snapshot.json 了解頁面結構"
echo "2. 如果自動點擊失敗，需手動完成註冊"
echo "3. Prolific 無 CAPTCHA，可在 Windows 瀏覽器完成"
