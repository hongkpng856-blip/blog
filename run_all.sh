#!/bin/bash
# 一鍵執行所有自動化賺錢工具
# 使用方法: bash run_all.sh

echo "=========================================="
echo "🤖 自動化賺錢系統 - 一鍵執行"
echo "=========================================="
echo ""

# 切換到工作目錄
cd /home/claw/.openclaw/workspace

echo "[1/5] 檢查平台狀態..."
python3 daily_auto_runner.py
echo ""

echo "[2/5] 檢查收入追蹤..."
python3 income_tracker.py
echo ""

echo "[3/5] 生成最新報告..."
python3 earnings_dashboard.py 2>/dev/null || echo "儀表板跳過"
echo ""

echo "[4/5] 列出可用資產..."
echo "📁 已建立檔案:"
ls -la *.py *.md *.zip *.json 2>/dev/null | head -20
echo ""

echo "[5/5] 顯示執行建議..."
echo ""
echo "=========================================="
echo "📋 執行建議"
echo "=========================================="
echo ""
echo "🌟 方案 1: 出售腳本包（最快）"
echo "   → 上傳 auto_earning_scripts.zip 到 Gumroad"
echo "   → 設定價格 $5 USD"
echo "   → 賣出 1 份即達成目標"
echo ""
echo "⭐ 方案 2: 註冊 Prolific"
echo "   → https://app.prolific.com/register/participant/join-waitlist/about-yourself"
echo "   → 無 CAPTCHA，$5-20/研究"
echo ""
echo "⭐ 方案 3: Microsoft Rewards"
echo "   → 建立 Microsoft 帳號"
echo "   → 執行 python3 bing_search_automation.py"
echo "   → 每日自動搜索累積積分"
echo ""
echo "=========================================="
echo "✅ 執行完成"
echo "=========================================="
