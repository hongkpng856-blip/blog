# GitHub Pages 部署指南

## 步驟

### 1. 建立 GitHub 帳號（如果沒有）
- 前往：https://github.com/signup
- 免費註冊

### 2. 建立新 Repository
- 登入後，點擊「New repository」
- Repository 名稱：`mock-website`
- 設為 Public
- 勾選「Add a README file」
- 點擊「Create repository」

### 3. 上傳網站檔案
在 repository 頁面：
1. 點擊「Add file」→「Upload files」
2. 上傳以下檔案：
   - `index.html`（從 mock_website.py 產生）
   - `style.css`（如果有的話）

### 4. 啟用 GitHub Pages
1. 進入 repository → Settings → Pages
2. Source：選擇「Deploy from a branch」
3. Branch：選擇「main」→「/(root)」
4. 點擊「Save」

### 5. 獲得雲端 URL
- GitHub Pages URL：`https://your-username.github.io/mock-website`
- 等待 1-2 分鐘部署完成

## 預計時間：~10 分鐘

## 優點
- 完全免費
- 不需要 ngrok 註冊
- 穩定可靠
- 可以自訂域名（可選）
