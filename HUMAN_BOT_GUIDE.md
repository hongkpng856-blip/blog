# 人性化點擊 BOT 使用指南

## 📋 新功能說明

### 🎯 主要功能
1. **隨機化點擊間距** — 模擬真實人類行為
2. **可調整時間範圍** — 例如隨機 1-30 分鐘
3. **模擬人類行為** — 閱讀、思考、滾動
4. **避免被檢測** — 使用多種分佈混合

---

## 🚀 快速開始

### 方法 1：一鍵執行
```bash
python3 run_human_bot.py
```

### 方法 2：互動模式
```bash
python3 human_like_bot.py
```

### 方法 3：Python 直接執行
```python
from human_like_bot import HumanLikeBot

bot = HumanLikeBot()

# 執行活動
results = bot.run_human_like_campaign(
    url="https://example.com",
    total_clicks=10,
    min_interval_minutes=5,   # 最小間隔 5 分鐘
    max_interval_minutes=30   # 最大間隔 30 分鐘
)
```

---

## ⚙️ 參數說明

| 參數 | 說明 | 預設值 |
|------|------|--------|
| `url` | 目標網站 | httpbin.org/ip |
| `total_clicks` | 總點擊次數 | 5 |
| `min_interval_minutes` | 最小間隔（分鐘） | 1 |
| `max_interval_minutes` | 最大間隔（分鐘） | 30 |
| `proxies` | Proxy 列表（可選） | None |

---

## 🎭 模擬的人類行為

### 1. 頁面載入等待
- 隨機 1-4 秒

### 2. 初始瀏覽
- 隨機 3-10 秒

### 3. 頁面滾動
- 隨機 3-10 次
- 每次間隔 0.5-3 秒
- 30% 機率會停下來看

### 4. 內容閱讀
- 根據內容長度計算閱讀時間
- 閱讀速度：200-400 字/分鐘
- 加入分心、重複閱讀因素

### 5. 思考時間
- 隨機 2-15 秒
- 40% 機率會思考

---

## 📊 輸出範例

```
============================================================
👤 人性化點擊 BOT 啟動
============================================================

📍 目標網站: https://example.com
🔢 總點擊次數: 10
⏱️ 間隔時間: 5-30 分鐘（隨機）
------------------------------------------------------------

[1/10] 第 1 次點擊
  ⏰ 開始時間: 06:30:00
  🌐 使用 Proxy: 123.456.789.012:8080
  📖 模擬閱讀：500 字，預計 45.2 秒
  📜 模擬滾動：5 次
  ✅ 成功
  📊 會話時間: 62.3 秒
  📊 行為數量: 5

  ⏳ 等待 12.5 分鐘後進行下一次點擊...
  📅 預計下次時間: 06:42:30
```

---

## 🎯 使用場景

### 場景 1：長期活動（推薦）
```python
# 每天 10 次，間隔 30-60 分鐘
bot.run_human_like_campaign(
    url="https://target.com",
    total_clicks=10,
    min_interval_minutes=30,
    max_interval_minutes=60
)
```

### 場景 2：測試模式
```python
# 快速測試，間隔 1-5 分鐘
bot.run_human_like_campaign(
    url="https://target.com",
    total_clicks=5,
    min_interval_minutes=1,
    max_interval_minutes=5
)
```

### 場景 3：極度模擬
```python
# 最接近真人，間隔 1-2 小時
bot.run_human_like_campaign(
    url="https://target.com",
    total_clicks=20,
    min_interval_minutes=60,
    max_interval_minutes=120
)
```

---

## ⚠️ 注意事項

1. **時間越隨機越難被檢測**
2. **建議間隔至少 5 分鐘以上**
3. **避免在固定時間執行**
4. **可搭配 Proxy 列表使用**

---

## 📁 檔案清單

| 檔案 | 用途 |
|------|------|
| `human_like_bot.py` | 人性化點擊主程式 |
| `run_human_bot.py` | 一鍵執行腳本 |
| `HUMAN_BOT_GUIDE.md` | 使用指南 |

---

*最後更新：2026-03-22 06:30 GMT+8*