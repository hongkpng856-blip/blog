# 簡易部署方案

## 方案 A：GitHub Pages（推薦）

### 步驟 1：註冊 GitHub（如果沒有帳號）
- 前往：https://github.com/signup

### 步驟 2：建立新 Repository
1. 登入 GitHub
2. 點擊右上角「+」→「New repository」
3. Repository 名稱：`mock-website`
4. 設為 **Public**
5. 勾選「Add a README file」
6. 點擊「Create repository」

### 步驟 3：上傳網站檔案
1. 在 repository 頁面，點擊「Add file」→「Upload files」
2. 上傳 `/home/claw/.openclaw/workspace/mock_site/index.html`
3. 將檔案重命名為 `index.html`（如果需要的話）
4. 點擊「Commit changes」

### 步驟 4：啟用 GitHub Pages
1. 進入 repository → Settings → Pages
2. Source：選擇「Deploy from a branch」
3. Branch：選擇「main」→「/(root)」
4. 點擊「Save」

### 步驟 5：獲得雲端 URL
- URL：`https://your-username.github.io/mock-website`
- 等待 1-2 分鐘部署完成

---

## 方案 B：PythonAnywhere（免費）

### 步驟 1：註冊 PythonAnywhere
- 前往：https://www.pythonanywhere.com/pricing/
- 選擇「Create a free account」

### 步驟 2：建立 Web App
1. 登入後，前往「Web」→「Add a new web app」
2. 選擇「Manual configuration」→「Python 3.9」
3. 設定「Working directory」

### 步驟 3：上傳檔案
1. 前往「Files」
2. 上傳 `mock_site/index.html`

### 步驟 4：設定 Static Files
1. 前往「Web」
2. 在「Static files」區塊，設定：
   - URL: `/` → Directory: `/home/your-username/`
3. 點擊「Reload」

---

## 方案 C：Netlify（免費，最簡單）

### 步驟 1：前往 Netlify
- https://app.netlify.com/drop

### 步驟 2：拖放上傳
1. 直接拖放 `mock_site` 資料夾到網頁上
2. 自動獲得 URL

---

## 預計時間
- GitHub Pages：~10 分鐘
- PythonAnywhere：~15 分鐘
- Netlify：~5 分鐘（最快）

## 推薦
**Netlify** — 最簡單，不需要註冊即可使用
