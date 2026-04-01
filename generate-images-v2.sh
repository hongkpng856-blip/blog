#!/bin/bash

# Blog 文章 AI 圖片生成腳本 v2
# 使用 Pollinations AI 生成特色圖片

POSTS_DIR="/home/claw/.openclaw/workspace/blog-repo/_posts"
IMAGES_DIR="/home/claw/.openclaw/workspace/blog-repo/assets/images"

# 確保圖片目錄存在
mkdir -p "$IMAGES_DIR"

# 根據標題生成 AI 提示詞既函數
generate_prompt() {
    local title="$1"
    
    # 提取標題關鍵字並生成合適既提示詞
    if [[ "$title" == *"GitHub"* ]]; then
        echo "modern flat design laptop with GitHub logo, coding environment, minimalist tech blog illustration, soft gradient background"
    elif [[ "$title" == *"工作效率"* ]] || [[ "$title" == *"productivity"* ]]; then
        echo "productive workspace with calendar, coffee, laptop, organized desk, efficiency concept, soft warm lighting"
    elif [[ "$title" == *"AI 自動化"* ]] || [[ "$title" == *"automation"* ]]; then
        echo "futuristic AI automation, robot arm working with computers, digital transformation, cyber technology illustration"
    elif [[ "$title" == *"健康生活"* ]] || [[ "$title" == *"healthy"* ]]; then
        echo "healthy lifestyle, fresh fruits, yoga mat, wellness concept, natural light, peaceful morning"
    elif [[ "$title" == *"免疫力"* ]] || [[ "$title" == *"immune"* ]]; then
        echo "immune system boost, vitamin C, healthy food, natural immunity, fresh fruits and vegetables, clean aesthetic"
    elif [[ "$title" == *"極簡主義"* ]] || [[ "$title" == *"minimalist"* ]]; then
        echo "minimalist living room, clean empty space, simple furniture, decluttered home, zen aesthetic"
    elif [[ "$title" == *"Python"* ]] || [[ "$title" == *"python"* ]]; then
        echo "Python programming code on screen, developer working, tech coding illustration, dark theme terminal"
    elif [[ "$title" == *"專注力"* ]] || [[ "$title" == *"focus"* ]]; then
        echo "focus and concentration, person working at desk, laser focus concept, minimal distractions, productivity"
    elif [[ "$title" == *"AI Agent"* ]] || [[ "$title" == *"agent"* ]]; then
        echo "AI artificial intelligence agent, robot assistant, smart technology, futuristic AI illustration"
    elif [[ "$title" == *"人形機器人"* ]]; then
        echo "humanoid robot at home, domestic robot assistant, futuristic household, sci-fi technology illustration"
    elif [[ "$title" == *"睡眠"* ]]; then
        echo "good sleep, comfortable bed, peaceful night, restful sleep, moon and stars, cozy bedroom"
    elif [[ "$title" == *"數位生活"* ]]; then
        echo "digital lifestyle, smart devices, technology in daily life, modern convenience, connected world"
    elif [[ "$title" == *"理財"* ]] || [[ "$title" == *"理財觀念"* ]] || [[ "$title" == *"理財攻略"* ]]; then
        echo "financial planning, investment chart, growing wealth, stocks and graphs, money concept, professional finance"
    elif [[ "$title" == *"比特幣"* ]] || [[ "$title" == *"加密貨幣"* ]]; then
        echo "bitcoin cryptocurrency, digital coins, blockchain technology, crypto trading, futuristic finance"
    elif [[ "$title" == *"遠距工作"* ]]; then
        echo "remote work, person working from home, laptop coffee, flexible work lifestyle, modern telecommuting"
    elif [[ "$title" == *"Vtuber"* ]]; then
        echo "virtual YouTuber, anime avatar, VTuber character, digital streaming, virtual entertainment"
    elif [[ "$title" == *"台北捷運"* ]]; then
        echo "Taipei MRT train, metro subway, Taiwan transportation, modern public transit"
    elif [[ "$title" == *"YouTuber"* ]]; then
        echo "YouTube creator, video filming, content creator, social media star, modern influencer"
    elif [[ "$title" == *"太陽能"* ]]; then
        echo "solar panels, renewable energy, green power, solar farm, sustainable energy future"
    elif [[ "$title" == *"母親節"* ]]; then
        echo "Mother's Day gift, flowers and love, family appreciation, warm Mother's Day celebration"
    elif [[ "$title" == *"演唱會"* ]]; then
        echo "concert venue, live music performance, energetic concert crowd, music festival atmosphere"
    elif [[ "$title" == *"短影音"* ]]; then
        echo "short video content, TikTok Reels, viral video concept, mobile social media, modern content creation"
    elif [[ "$title" == *"蝦皮"* ]] || [[ "$title" == *"購物"* ]]; then
        echo "online shopping, e-commerce shopping cart, mobile shopping, retail therapy, convenient shopping"
    elif [[ "$title" == *"運動"* ]] || [[ "$title" == *"健身"* ]]; then
        echo "fitness workout, gym exercise, healthy lifestyle, training at gym, sport and exercise"
    elif [[ "$title" == *"餐廳"* ]]; then
        echo "delicious food restaurant, Taiwanese cuisine, gourmet dining, tasty meal presentation"
    elif [[ "$title" == *"AI 代理"* ]]; then
        echo "AI assistant virtual helper, smart AI agent, artificial intelligence service, chatbot technology"
    elif [[ "$title" == *"AI 寫作"* ]]; then
        echo "AI writing assistant, creative writing with AI, content generation, artificial intelligence writing"
    elif [[ "$title" == *"ChatGPT"* ]]; then
        echo "ChatGPT AI chatbot, conversational AI, smart AI assistant, next generation chatbot"
    elif [[ "$title" == *"LINE Pay"* ]]; then
        echo "mobile payment, LINE Pay QR code, digital wallet, contactless payment, cashless transaction"
    elif [[ "$title" == *"Netflix"* ]]; then
        echo "Netflix streaming, watching TV shows, binge watching, entertainment at home, streaming service"
    elif [[ "$title" == *"Switch"* ]]; then
        echo "Nintendo Switch gaming console, video game controller, gaming entertainment, play station"
    elif [[ "$title" == *"Threads"* ]]; then
        echo "Threads social media, Meta platform, social networking, online community, digital communication"
    elif [[ "$title" == *"iPhone"* ]]; then
        echo "iPhone smartphone, Apple phone, latest smartphone, mobile technology, sleek device"
    elif [[ "$title" == *"中職"* ]] || [[ "$title" == *"棒球"* ]]; then
        echo "Taiwan baseball CPBL, baseball stadium, baseball game, Taiwanese baseball league, sport competition"
    elif [[ "$title" == *"办公室"* ]] || [[ "$title" == *"久坐"* ]]; then
        echo "office worker sitting, desk job health, workplace wellness, ergonomic office chair, sedentary lifestyle"
    elif [[ "$title" == *"心態"* ]]; then
        echo "positive mindset, personal growth, motivation, success mindset, achievement and goals"
    elif [[ "$title" == *"手機遊戲"* ]]; then
        echo "mobile gaming, smartphone games, playing mobile games, casual gaming, fun gaming session"
    elif [[ "$title" == *"數位排毒"* ]]; then
        echo "digital detox, unplugged from technology, nature and technology balance, mental wellness, disconnect"
    elif [[ "$title" == *"日本"* ]] || [[ "$title" == *"旅遊"* ]]; then
        echo "Japan travel, Japanese temple, Mt Fuji, tourism in Japan, travel adventure, beautiful Japan"
    elif [[ "$title" == *"機車"* ]]; then
        echo "motorcycle modification, scooter customization, motorcycle rider, Taiwan motorbike culture"
    elif [[ "$title" == *"短影音行銷"* ]]; then
        echo "short video marketing, viral content, social media marketing, video advertising, digital promotion"
    elif [[ "$title" == *"自由工作者"* ]]; then
        echo "freelancer working remotely, digital nomad, independent worker, flexible career lifestyle"
    elif [[ "$title" == *"韓劇"* ]]; then
        echo "Korean drama, K-drama watching, Korean entertainment, binge watching K-drama, popular drama"
    elif [[ "$title" == *"高股息"* ]]; then
        echo "dividend investing, passive income, ETF investment, portfolio growth, financial freedom"
    elif [[ "$title" == *"時尚"* ]]; then
        echo "fashion style, trendy clothing, stylish outfit, fashion model, modern fashion design"
    else
        echo "modern blog article illustration, clean design, professional content, minimal aesthetic"
    fi
}

# 生成 slug 既函數
generate_slug() {
    local title="$1"
    # 移除 .md 擴展名（如果有的話）
    title="${title%.md}"
    # 移除日期部分
    title=$(echo "$title" | sed 's/^[0-9-]*-//')
    # 將特殊字符替換為連字符
    echo "$title" | sed 's/ /-/g' | sed 's/　/-/g' | sed 's/[^\w-]//g' | tr '[:upper:]' '[:lower:]'
}

# 處理每篇文章
process_post() {
    local post_file="$1"
    local filename=$(basename "$post_file" .md)
    
    # 提取日期（YYYY-MM-DD）
    local date_slug=$(echo "$filename" | grep -oE '^[0-9]{4}-[0-9]{2}-[0-9]{2}')
    
    # 從文件名提取標題slug
    local title_slug=$(generate_slug "$filename")
    
    # 從 frontmatter 讀取標題
    local title=$(sed -n 's/^title: *"\(.*\)"/\1/p; s/^title: *'\''\(.*\)'\''/\1/p' "$post_file" | head -1)
    
    if [ -z "$title" ]; then
        title="$filename"
    fi
    
    local image_name="${date_slug}-${title_slug}.jpg"
    local output_path="${IMAGES_DIR}/${image_name}"
    
    # 如果圖片已存在，跳過
    if [ -f "$output_path" ]; then
        # 但仍更新 frontmatter
        local image_path_in_markdown="/assets/images/${image_name}"
        if ! grep -q "image:.*$image_name" "$post_file"; then
            if grep -q "^image:" "$post_file"; then
                sed -i "s|^image:.*|image: $image_path_in_markdown|" "$post_file"
            else
                sed -i "/^---/a\\image: $image_path_in_markdown" "$post_file"
            fi
        fi
        echo "Skipped (exists): $title"
        return
    fi
    
    # 根據標題生成 AI 提示詞
    local prompt=$(generate_prompt "$title")
    local encoded_prompt=$(python3 -c "import urllib.parse; print(urllib.parse.quote('''$prompt'''))")
    
    # 下載圖片
    local image_url="https://image.pollinations.ai/prompt/${encoded_prompt}?nologo=true&width=1200&height=630"
    
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

# 清除舊既測試圖片
rm -f ${IMAGES_DIR}/2026-03-*.jpg

# 遍歷所有 markdown 文件
cd "$POSTS_DIR"
count=0
for post in *.md; do
    if [ -f "$post" ]; then
        process_post "$post"
        count=$((count + 1))
        # 避免請求過快
        sleep 1.5
    fi
done

echo "=== 完成 ==="
echo "共處理 $count 篇文章"