#!/bin/bash
# 文章 + AI 圖像生成管線
# 用法: ./article-with-image-pipeline.sh "文章標題" "分類" "標籤（逗號分隔）"

TITLE="$1"
CATEGORY="$2"
TAGS="$3"
DATE=$(date +%Y-%m-%d)
FILENAME="${DATE}-$(echo "$TITLE" | tr ' ' '-' | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9-]//g').md"

echo "📝 準備生成文章..."
echo "   標題: $TITLE"
echo "   分類: $CATEGORY"
echo "   標籤: $TAGS"
echo "   檔名: $FILENAME"

# 1. 生成文章（呼叫文章生成器）
echo ""
echo "📌 步驟 1/2: 生成文章內容"
# 這裡會由 AI agent 執行文章生成

# 2. 生成 AI 圖像
echo ""
echo "📌 步驟 2/2: 生成特色圖片"
# 這裡會由 AI 圖像 agent 執行圖片生成

echo ""
echo "✅ 管線完成！"
