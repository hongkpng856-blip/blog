#!/bin/bash
# Article Writer - 主 Agent 調用腳本
# 用法: ./write_article.sh "文章標題" [分類]
# 
# 範例:
#   ./write_article.sh "如何提升工作效率"
#   ./write_article.sh "Python 教學" 技術

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="$SCRIPT_DIR/article_writer.py"

TITLE="${1:-}"
CATEGORY="${2:-}"

if [ -z "$TITLE" ]; then
    echo "用法: $0 \"文章標題\" [分類]"
    echo "分類可選: 技術, 生活, 健康, 投資 (預設自動偵測)"
    exit 1
fi

if [ -n "$CATEGORY" ]; then
    python3 "$PYTHON_SCRIPT" "$TITLE" --category "$CATEGORY"
else
    python3 "$PYTHON_SCRIPT" "$TITLE"
fi