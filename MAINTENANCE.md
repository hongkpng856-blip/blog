# 部落格維護計劃

## 每週更新計劃

### 週一：內容規劃
- [ ] 構思本週文章主題
- [ ] 收集相關資料和參考連結
- [ ] 準備文章所需的圖片

### 週三：文章撰寫
- [ ] 撰寫新文章草稿
- [ ] 選擇合適的特色圖片
- [ ] 設定 SEO 相關標籤

### 週五：發布與維護
- [ ] 發布新文章
- [ ] 檢查所有圖片是否正常顯示
- [ ] 回覆讀者留言
- [ ] 更新舊文章內容（如有需要）

### 每月第一週：全面檢查
- [ ] 檢查所有頁面連結是否正常
- [ ] 檢查響應式設計是否正常
- [ ] 更新「關於我」頁面
- [ ] 備份整個部落格

---

## 備份策略

### 方法 1：Git 版本控制（自動）
每次 push 到 GitHub 都會自動建立版本備份。

### 方法 2：本地備份
```bash
# 在 blog-repo 目錄執行
./scripts/backup.sh
```

### 方法 3：下載 ZIP 備份
從 GitHub 下載最新版本的 ZIP 檔案。

---

## 圖片維護優先清單

1. **頭像圖片** (`avatar.svg`)
   - 確保在首頁、側邊欄、關於頁面正確顯示
   - 建議尺寸：200x200 像素

2. **特色圖片** (`tech.svg`, `investment.svg`, `health.svg`)
   - 確保每篇文章都有對應的特色圖片
   - 建議尺寸：800x400 像素

3. **預設圖片** (`default-post.svg`)
   - 文章沒有指定圖片時使用
   - 建議尺寸：800x400 像素

---

## 檔案結構說明

```
blog/
├── _posts/           # 文章目錄
│   └── YYYY-MM-DD-title.md
├── _layouts/         # 頁面模板
│   ├── default.html
│   ├── post.html
│   └── page.html
├── _includes/        # 可重用組件
│   ├── head.html
│   ├── navbar.html
│   ├── sidebar.html
│   ├── social-share.html
│   └── social-follow.html
├── assets/           # 靜態資源
│   ├── images/       # 圖片
│   │   ├── avatar.svg
│   │   ├── posts/
│   │   └── featured/
│   └── css/          # 樣式
├── backup/           # 備份目錄
├── scripts/          # 維護腳本
├── _config.yml       # Jekyll 配置
├── sitemap.xml       # SEO 網站地圖
├── robots.txt        # 搜索引擎指引
└── search.json       # 搜索資料
```

---

*建立日期：2026-03-25*