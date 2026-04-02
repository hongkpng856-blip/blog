# Article Writer Agent - 使用說明

## 概述
Article Writer Agent 是一個可被主 Agent 調用的文章生成 Sub-agent。輸入文章主題，輸出符合部落格格式的 Markdown 文章。

## 檔案位置
- 主程式：`/home/claw/.openclaw/workspace/blog-repo/scripts/article_writer.py`
- Shell 腳本：`/home/claw/.openclaw/workspace/blog-repo/scripts/write_article.sh`

---

## 使用方法

### 方法一：直接使用 Python 指令

```bash
# 基本用法
python3 article_writer.py "文章標題"

# 指定分類
python3 article_writer.py "文章標題" --category 技術

# 指定輸出目錄
python3 article_writer.py "文章標題" --output ./my_articles

# 預覽模式（不儲存檔案）
python3 article_writer.py "文章標題" --dry-run
```

### 方法二：使用 Shell 腳本

```bash
# 基本用法
./write_article.sh "文章標題"

# 指定分類
./write_article.sh "文章標題" 分類
```

---

## 參數說明

| 參數 | 說明 | 可選值 |
|------|------|--------|
| `title` | 文章標題（必要） | 任意文字 |
| `--category, -c` | 文章分類 | `技術`, `生活`, `健康`, `投資` |
| `--output, -o` | 輸出目錄 | 預設 `_posts/` |
| `--date, -d` | 發布日期 | `YYYY-MM-DD HH:MM:SS +0800` |
| `--dry-run` | 僅預覽不儲存 | - |

---

## 分類說明

系統會根據標題自動偵測分類，亦可手動指定：

- **技術**：Python、程式設計、AI、軟體開發等
- **生活**：工作效率、生活技巧、自我成長等
- **健康**：睡眠、運動、飲食、養生等
- **投資**：理財、股票、資產配置等

---

## 輸出格式

產出的文章包含：
- ✅ YAML front matter (title, date, categories, author, description, keywords, image)
- ✅ 中文內文 (500-800 字)
- ✅ 多個章節結構
- ✅ 結論與行動建議

---

## 主 Agent 調用範例

### 在 Python 中調用
```python
import subprocess

result = subprocess.run(
    ["python3", "article_writer.py", "如何提升工作效率", "--category", "生活"],
    capture_output=True,
    text=True,
    cwd="/home/claw/.openclaw/workspace/blog-repo/scripts"
)
print(result.stdout)
```

### 在 Shell 中調用
```bash
# 直接產生文章並儲存
python3 /home/claw/.openclaw/workspace/blog-repo/scripts/article_writer.py "你的文章標題"
```

---

## 驗證成果

產生的文章會儲存至 `_posts/` 目錄，檔名格式：
```
YYYY-MM-DD-標題-slug.md
```

例如：`2026-04-02-如何提升工作效率.md`

---

## 限制事項

1. 生成的內容是基於模板的結構化文章，適用於標準格式的文章
2. 如需更創意或客製化的內容，可能需要人工編輯
3. 圖片需要另外透過 Image Creator Agent 生成