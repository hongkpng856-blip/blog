#!/bin/bash

# Blog 文章 AI 圖片生成腳本
# 使用 Pollinations AI 生成特色圖片

POSTS_DIR="/home/claw/.openclaw/workspace/blog-repo/_posts"
IMAGES_DIR="/home/claw/.openclaw/workspace/blog-repo/assets/images"

# 確保圖片目錄存在
mkdir -p "$IMAGES_DIR"

# 根據標題生成 AI 提示詞既函數
generate_prompt() {
    local title="$1"
    
    # 提取標題關鍵字並生成合適既提示詞
    case "$title" in
        *"GitHub"*)
            echo "modern flat design laptop with GitHub logo, coding environment, minimalist tech blog illustration, soft gradient background"
            ;;
        *"工作效率"*)
            echo "productive workspace with calendar, coffee, laptop, organized desk, efficiency concept, soft warm lighting"
            ;;
        *"AI 自動化"*)
            echo "futuristic AI automation, robot arm working with computers, digital transformation, cyber technology illustration"
            ;;
        *"健康生活"*)
            echo "healthy lifestyle, fresh fruits, yoga mat, wellness concept, natural light, peaceful morning"
            ;;
        *"免疫力"*)
            echo "immune system boost, vitamin C, healthy food, natural immunity, fresh fruits and vegetables, clean aesthetic"
            ;;
        *"極簡主義"*)
            echo "minimalist living room, clean empty space, simple furniture, decluttered home, zen aesthetic"
            ;;
        *"Python"*)
            echo "Python programming code on screen, developer working, tech coding illustration, dark theme terminal"
            ;;
        *"專注力"*)
            echo "focus and concentration, person working at desk, laser focus concept, minimal distractions, productivity"
            ;;
        *"AI Agent"*)
            echo "AI artificial intelligence agent, robot assistant, smart technology, futuristic AI illustration"
            ;;
        *"人形機器人"*)
            echo "humanoid robot at home, domestic robot assistant, futuristic household, sci-fi technology illustration"
            ;;
        *"睡眠"*)
            echo "good sleep, comfortable bed, peaceful night, restful sleep, moon and stars, cozy bedroom"
            ;;
        *"數位生活"*)
            echo "digital lifestyle, smart devices, technology in daily life, modern convenience, connected world"
            ;;
        *"理財"*|*"股票"*|*"ETF"*)
            echo "financial planning, investment chart, growing wealth, stocks and graphs, money concept, professional finance"
            ;;
        *"比特幣"*|*"加密貨幣"*)
            echo "bitcoin cryptocurrency, digital coins, blockchain technology, crypto trading, futuristic finance"
            ;;
        *"遠距工作"*)
            echo "remote work, person working from home, laptop coffee, flexible work lifestyle, modern telecommuting"
            ;;
        *"Vtuber"*)
            echo "virtual YouTuber, anime avatar, VTuber character, digital streaming, virtual entertainment"
            ;;
        *"台北捷運"*)
            echo "Taipei MRT train, metro subway, Taiwan transportation, modern public transit"
            ;;
        *"YouTuber"*)
            echo "YouTube creator, video filming, content creator, social media star, modern influencer"
            ;;
        *"太陽能"*)
            echo "solar panels, renewable energy, green power, solar farm, sustainable energy future"
            ;;
        *"母親節"*)
            echo "Mother's Day gift, flowers and love, family appreciation, warm Mother's Day celebration"
            ;;
        *"演唱會"*)
            echo "concert venue, live music performance, energetic concert crowd, music festival atmosphere"
            ;;
        *"短影音"*)
            echo "short video content, TikTok Reels, viral video concept, mobile social media, modern content creation"
            ;;
        *"蝦皮"*|*"購物"*)
            echo "online shopping, e-commerce shopping cart, mobile shopping, retail therapy, convenient shopping"
            ;;
        *"運動"*|*"健身"*)
            echo "fitness workout, gym exercise, healthy lifestyle, training at gym, sport and exercise"
            ;;
        *"餐廳"*)
            echo "delicious food restaurant, Taiwanese cuisine, gourmet dining, tasty meal presentation"
            ;;
        *"AI 代理"*)
            echo "AI assistant virtual helper, smart AI agent, artificial intelligence service, chatbot technology"
            ;;
        *"AI 寫作"*)
            echo "AI writing assistant, creative writing with AI, content generation, artificial intelligence writing"
            ;;
        *"ChatGPT"*)
            echo "ChatGPT AI chatbot, conversational AI, smart AI assistant, next generation chatbot"
            ;;
        *"LINE Pay"*)
            echo "mobile payment, LINE Pay QR code, digital wallet, contactless payment, cashless transaction"
            ;;
        *"Netflix"*)
            echo "Netflix streaming, watching TV shows, binge watching, entertainment at home, streaming service"
            ;;
        *"Switch 2"*)
            echo "Nintendo Switch 2 gaming console, video game controller, gaming entertainment, play station"
            ;;
        *"Threads"*)
            echo "Threads social media, Meta platform, social networking, online community, digital communication"
            ;;
        *"iPhone"*)
            echo "iPhone smartphone, Apple phone, latest smartphone, mobile technology, sleek device"
            ;;
        *"中職"*)
            echo "Taiwan baseball CPBL, baseball stadium, baseball game, Taiwanese baseball league, sport competition"
            ;;
        *"办公室"*)
            echo "office worker sitting, desk job health, workplace wellness, ergonomic office chair, sedentary lifestyle"
            ;;
        *"心態"*)
            echo "positive mindset, personal growth, motivation, success mindset, achievement and goals"
            ;;
        *"手機遊戲"*)
            echo "mobile gaming, smartphone games, playing mobile games, casual gaming, fun gaming session"
            ;;
        *"數位排毒"*)
            echo "digital detox, unplugged from technology, nature and technology balance, mental wellness, disconnect"
            ;;
        *"日本"*|*"旅遊"*)
            echo "Japan travel, Japanese temple, Mt Fuji, tourism in Japan, travel adventure, beautiful Japan"
            ;;
        *"機車"*)
            echo "motorcycle modification, scooter customization, motorcycle rider, Taiwan motorbike culture"
            ;;
        *"短影音行銷"*)
            echo "short video marketing, viral content, social media marketing, video advertising, digital promotion"
            ;;
        *"自由工作者"*)
            echo "freelancer working remotely, digital nomad, independent worker, flexible career lifestyle"
            ;;
        *"韓劇"*)
            echo "Korean drama, K-drama watching, Korean entertainment, binge watching K-drama, popular drama"
            ;;
        *"高股息"*)
            echo "dividend investing, passive income, ETF investment, portfolio growth, financial freedom"
            ;;
        *)
            echo "modern blog article illustration, clean design, professional content, minimal aesthetic"
            ;;
    esac
}

# 處理每篇文章
process_post() {
    local post_file="$1"
    local filename=$(basename "$post_file" .md)
    
    # 提取日期和標題slug
    local date_slug=$(echo "$filename" | cut -d'-' -f1-3)
    
    # 提取標題（從 frontmatter）
    local title=$(sed -n '2s/title: "\(.*\)"/\1/p' "$post_file")
    
    if [ -z "$title" ]; then
        title=$(sed -n '2s/title: \(.*\)/\1/p' "$post_file")
    fi
    
    # 清理標題中的特殊字符
    local clean_title=$(echo "$title" | sed 's/[^\w\s-]//g' | tr ' ' '-')
    local image_name="${date_slug}-${clean_title}.jpg"
    
    # 根據標題生成 AI 提示詞
    local prompt=$(generate_prompt "$title")
    local encoded_prompt=$(python3 -c "import urllib.parse; print(urllib.parse.quote('''$prompt'''))")
    
    # 下載圖片
    local image_url="https://image.pollinations.ai/prompt/${encoded_prompt}?nologo=true&width=1200&height=630"
    local output_path="${IMAGES_DIR}/${image_name}"
    
    echo "Processing: $title"
    echo "  -> Image: $image_name"
    echo "  -> Prompt: $prompt"
    
    # 下載圖片（使用 curl）
    if curl -sL --max-time 60 "$image_url" -o "$output_path"; then
        echo "  -> Downloaded successfully!"
        
        # 更新 markdown 文件的 image 路径
        local image_path_in_markdown="/assets/images/${image_name}"
        
        # 使用 sed 更新 frontmatter 中的 image 字段
        if grep -q "^image:" "$post_file"; then
            sed -i "s|^image:.*|image: $image_path_in_markdown|" "$post_file"
        else
            # 如果沒有 image 字段，在 description 後面添加
            sed -i "/^description:/a\\image: $image_path_in_markdown" "$post_file"
        fi
        echo "  -> Updated markdown frontmatter"
    else
        echo "  -> FAILED to download!"
    fi
    
    echo ""
}

# 遍歷所有 markdown 文件
cd "$POSTS_DIR"
for post in *.md; do
    if [ -f "$post" ]; then
        process_post "$post"
        # 避免請求過快，稍作延遲
        sleep 2
    fi
done

echo "=== 完成 ==="
echo "所有圖片已生成並更新 markdown 文件"