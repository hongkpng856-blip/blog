# 多 IP 切換 BOT 使用指南

## 📋 檔案清單

| 檔案 | 用途 |
|------|------|
| `multi_ip_bot.py` | 主程式：多 IP 切換 BOT |
| `proxy_manager.py` | Proxy 管理器 |
| `website_clicker_bot.py` | 網站點擊 BOT |
| `run_bot.py` | 一鍵執行腳本 |

---

## 🚀 快速開始

### 方法 1：一鍵執行
```bash
python3 run_bot.py
```

### 方法 2：互動模式
```bash
python3 website_clicker_bot.py
```

### 方法 3：Python 直接執行
```python
from multi_ip_bot import MultiIPBot

bot = MultiIPBot()
bot.find_working_proxies(max_proxies=10)
results = bot.rotate_and_visit("https://example.com", visits=5)
```

---

## 📊 功能說明

### MultiIPBot
- 自動從免費 Proxy 來源獲取 IP
- 驗證 Proxy 可用性
- 使用不同 IP 訪問指定網站
- 記錄訪問結果

### ProxyManager
- 管理 Proxy 快取
- 批量驗證 Proxy
- 自動刷新過期 Proxy

### WebsiteClickerBot
- 使用不同 IP 點擊網站
- 模擬瀏覽器標頭
- 生成點擊報告

---

## ⚙️ 配置選項

```python
# 在 multi_ip_bot.py 中修改以下參數

# Proxy 數量
bot.find_working_proxies(max_proxies=20)

# 訪問次數
bot.rotate_and_visit(url, visits=10)

# 每次訪問間隔（秒）
bot.rotate_and_visit(url, delay=3.0)
```

---

## 📁 輸出檔案

| 檔案 | 內容 |
|------|------|
| `proxy_cache.json` | 可用 Proxy 快取 |
| `visit_results.json` | 訪問結果記錄 |
| `click_log.json` | 點擊記錄 |

---

## ⚠️ 注意事項

1. **免費 Proxy 品質不穩定**：建議多測試幾次
2. **可能被網站阻擋**：部分網站有安全機制
3. **速度較慢**：免費 Proxy 延遲較高
4. **建議延遲**：每次訪問間隔 2-5 秒，避免觸發風控

---

## 🎯 執行結果範例

```
============================================================
🖱️ 網站點擊 BOT
============================================================

請輸入目標網站 URL: https://example.com
請輸入點擊次數 (預設 5): 5

🔄 正在獲取可用 Proxy...
📥 獲取中: https://api.proxyscrape.com...
  → 獲取 1000 個
📊 總計: 1500 個唯一 Proxy
🔍 測試 100 個 Proxy...
✅ 找到 10 個可用 Proxy

🌐 開始使用 5 個不同 IP 點擊網站
📍 目標: https://example.com
--------------------------------------------------

[1/5] 使用 Proxy: 123.456.789.012:8080
✅ 成功（狀態: 200）
⏳ 等待 2.0 秒...

[2/5] 使用 Proxy: 987.654.321.098:3128
✅ 成功（狀態: 200）
...

============================================================
📊 點擊報告
============================================================
總點擊: 5
成功: 5
失敗: 0
成功率: 100.0%

💾 記錄已儲存到 click_log.json
```
