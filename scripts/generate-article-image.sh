#!/bin/bash
# AI 圖像生成腳本
# 根據文章標題和內容生成吸引人的特色圖片

ARTICLE_TITLE="$1"
ARTICLE_CONTENT="$2"
OUTPUT_DIR="../assets/images/featured"

# 根據文章標題生成圖片提示詞
generate_image_prompt() {
    local title="$1"
    local prompt=""
    
    case "$title" in
        *"健康"*|*"運動"*|*"生活"*)
            prompt="healthy lifestyle wellness vibrant colors modern illustration people exercising nature"
            ;;
        *"AI"*|*"自動化"*|*"科技"*|*"技術"*)
            prompt="futuristic AI technology automation digital transformation neural network blue purple gradient"
            ;;
        *"投資"*|*"理財"*|*"財務"*)
            prompt="financial investment growth charts coins money tree success business professional"
            ;;
        *"效率"*|*"工作"*|*"生產力"*)
            prompt="productivity workflow efficiency modern workspace laptop focus time management"
            ;;
        *)
            prompt="modern professional illustration vibrant colors abstract geometric shapes"
            ;;
    esac
    
    echo "$prompt"
}

echo "🎨 準備生成 AI 圖片..."
echo "   文章標題: $ARTICLE_TITLE"

# 生成提示詞
PROMPT=$(generate_image_prompt "$ARTICLE_TITLE")
echo "   圖片提示詞: $PROMPT"

# 生成檔名（與文章對應）
FILENAME=$(echo "$ARTICLE_TITLE" | tr ' ' '-' | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9-]//g')
echo "   輸出檔名: ${FILENAME}.svg"

echo ""
echo "📌 使用 AI 圖像生成工具:"
echo "   選項 A: Stability AI (需要 API Key)"
echo "   選項 B: DALL-E (需要 OpenAI API Key)"
echo "   選項 C: Midjourney (需要 Discord)"
echo "   選項 D: 本地 SVG 佔位圖（免費）"

echo ""
echo "✅ 腳本完成！請選擇圖像生成方式。"
