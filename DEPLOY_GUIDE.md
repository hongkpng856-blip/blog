# 雲端部署指南

## 🚀 快速部署

### 方法 1：ngrok（最快，5 分鐘）

```bash
# 1. 啟動本地網站
python3 mock_website.py

# 2. 新終端，啟動 ngrok
ngrok http 8888

# 3. 取得公開網址
# 例如：https://abc123.ngrok.io
```

---

### 方法 2：PythonAnywhere（免費）

```bash
# 1. 註冊：https://www.pythonanywhere.com

# 2. 上傳檔案：
#    - cloud_website.py
#    - requirements.txt

# 3. 建立 Web App
#    - 選擇 Flask
#    - Python 3.10

# 4. 設定虛擬環境：
pip install flask flask-cors

# 5. 完成！
# 網址：https://你的帳號.pythonanywhere.com
```

---

### 方法 3：Render（免費）

```yaml
# render.yaml
services:
  - type: web
    name: bot-test-website
    env: python
    buildCommand: pip install flask flask-cors
    startCommand: python cloud_website.py
```

```bash
# 1. 連接 GitHub repo
# 2. 選擇 repo
# 3. 自動部署
```

---

### 方法 4：Railway（免費額度）

```bash
# 1. 安裝 CLI
npm install -g @railway/cli

# 2. 登入
railway login

# 3. 初始化
railway init

# 4. 部署
railway up

# 5. 取得網址
railway domain
```

---

## 📋 requirements.txt

```
flask
flask-cors
requests
```

---

## 🔧 環境變數

| 變數 | 說明 | 預設值 |
|------|------|--------|
| PORT | 埠號 | 8888 |

---

## 🎯 推薦順序

1. **測試用**：ngrok（最快）
2. **長期用**：PythonAnywhere（免費穩定）
3. **正式用**：Render/Railway（自動化部署）

---

*最後更新：2026-03-22 07:22 GMT+8*
