#!/bin/bash
# GitHub 自動部署腳本
# 使用方法：./github_deploy.sh

echo "🚀 開始部署到 GitHub Pages..."

# 步驟 1：認證 GitHub
echo ""
echo "📌 步驟 1：GitHub 認證"
echo "請選擇認證方式："
echo "  1) 使用 Personal Access Token（推薦）"
echo "  2) 互動式登入"
echo ""
read -p "請輸入選項 (1 或 2): " auth_choice

if [ "$auth_choice" = "1" ]; then
    echo ""
    read -p "請輸入你的 GitHub Personal Access Token: " token
    echo "$token" | gh auth login --with-token
elif [ "$auth_choice" = "2" ]; then
    gh auth login
else
    echo "❌ 無效選項"
    exit 1
fi

# 步驟 2：建立 Repository
echo ""
echo "📌 步驟 2：建立 Repository"
read -p "請輸入 GitHub 用戶名: " username
read -p "請輸入 Repository 名稱 (預設: mock-website): " repo_name
repo_name=${repo_name:-mock-website}

# 建立 repository
gh repo create "$repo_name" --public --clone

# 步驟 3：上傳檔案
echo ""
echo "📌 步驟 3：上傳網站檔案"
cd "$repo_name"
cp /home/claw/.openclaw/workspace/mock_site/index.html .
git add index.html
git commit -m "Add mock website"
git push origin main

# 步驟 4：啟用 GitHub Pages
echo ""
echo "📌 步驟 4：啟用 GitHub Pages"
gh api -X PUT repos/"$username"/"$repo_name"/pages -f source='{"branch":"main","path":"/"}'

echo ""
echo "✅ 部署完成！"
echo "🌐 網站 URL: https://$username.github.io/$repo_name"
echo ""
echo "請等待 1-2 分鐘讓 GitHub Pages 完成部署。"
