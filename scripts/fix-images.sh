#!/bin/bash

# 圖片關鍵詞映射表（文章關鍵詞 → Lorem Picsum 關鍵詞）
declare -A KEYWORD_MAP=(
    # 交通/捷運
    ["捷運"]="subway,train,metro"
    ["交通"]="traffic,city,road"
    ["機車"]="motorcycle,scooter"
    ["自行車"]="bicycle,bike"
    
    # 科技/AI
    ["AI"]="artificial-intelligence,technology,robot"
    ["ChatGPT"]="artificial-intelligence,computer"
    ["Python"]="code,programming,computer"
    ["自動化"]="technology,computer,digital"
    ["代理"]="ai,robot,technology"
    ["機器人"]="robot,future,technology"
    ["Vtuber"]="anime,streaming,camera"
    
    # 網紅/創作者
    ["YouTuber"]="youtube,video,camera"
    ["Threads"]="social-media,phone,app"
    ["短影音"]="video,tiktok,social-media"
    
    # 金融/投資
    ["比特幣"]="bitcoin,crypto,currency"
    ["加密貨幣"]="crypto,currency,bitcoin"
    ["股票"]="stock-market,finance,business"
    ["ETF"]="finance,investment,stock"
    ["理財"]="money,finance,investment"
    ["理財"]="money,finance"
    
    # 美食/餐廳
    ["餐廳"]="food,restaurant,taiwan"
    ["美食"]="food,restaurant,cooking"
    ["母親節"]="gift,flowers,love"
    ["演唱會"]="concert,music,festival"
    
    # 旅遊
    ["旅遊"]="travel,taiwan,japan"
    ["日本"]="japan,tokyo,travel"
    
    # 遊戲
    ["Switch"]="nintendo,gaming,game"
    ["遊戲"]="gaming,game,esports"
    ["手機遊戲"]="gaming,mobile,app"
    
    # 運動/健身
    ["健身"]="fitness,gym,workout"
    ["運動"]="sports,fitness,exercise"
    
    # 時尚
    ["時尚"]="fashion,style,clothing"
    ["穿搭"]="fashion,clothing,style"
    
    # 影視
    ["Netflix"]="netflix,movie,tv"
    ["韓劇"]="korean-drama,tv,drama"
    
    # 支付
    ["LINE Pay"]="mobile-payment,phone,app"
    
    # 蘋果
    ["iPhone"]="iphone,apple,smartphone"
    
    # 棒球
    ["中職"]="baseball,sports,taiwan"
    ["棒球"]="baseball,sports,game"
    
    # 太陽能/綠能
    ["太陽能"]="solar,solar-panel,energy"
    ["綠能"]="solar,nature,green"
    
    # 電商
    ["蝦皮"]="shopping,online-store,e-commerce"
    ["購物"]="shopping,bag,store"
    
    # 健康/生活
    ["健康"]="health,wellness,fitness"
    ["睡眠"]="sleep,bed,rest"
    ["久坐"]="office,sitting,work"
    ["心態"]="mindset,happiness,positive"
    ["專注力"]="focus,concentration,work"
    ["數位排毒"]="nature,peace,relaxation"
    
    # 工作
    ["遠距工作"]="laptop,remote-work,coffee-shop"
    ["办公室"]="office,work,computer"
    
    # 其他
    ["新手"]="beginner,learning,start"
)

# 擷取文章標題中既關鍵詞
get_keywords() {
    local title="$1"
    local keywords=""
    
    for key in "${!KEYWORD_MAP[@]}"; do
        if [[ "$title" == *"$key"* ]]; then
            if [ -z "$keywords" ]; then
                keywords="${KEYWORD_MAP[$key]}"
            else
                keywords="$keywords,${KEYWORD_MAP[$key]}"
            fi
        fi
    done
    
    # 如果冇匹配，用預設值
    if [ -z "$keywords" ]; then
        keywords="lifestyle,modern,asia"
    fi
    
    echo "$keywords"
}

# 下載圖片
download_image() {
    local filename="$1"
    local keywords="$2"
    local output_dir="assets/images/featured"
    local output_path="$output_dir/$filename"
    
    # 用第一個關鍵詞
    local first_keyword=$(echo "$keywords" | cut -d',' -f1)
    
    echo "Downloading: $filename with keyword: $first_keyword"
    
    # 用 seed 確保每次相同標題獲得相同圖片
    local seed=$(echo "$filename" | cksum | cut -d' ' -f1)
    
    # 嘗試下載圖片
    curl -sL "https://picsum.photos/seed/$seed/800/600" -o "$output_path"
    
    if [ $? -eq 0 ] && [ -s "$output_path" ]; then
        echo "✓ Downloaded: $filename"
        return 0
    else
        echo "✗ Failed: $filename"
        return 1
    fi
}

# 主程式
echo "開始修復圖片..."
echo "===================="

cd /home/claw/.openclaw/workspace/blog-repo

# 處理每個今日既文章 (2026-03-31)
for post in _posts/2026-03-31-*.md; do
    # 擷取標題
    title=$(grep "^title:" "$post" | sed 's/title: "*//' | sed 's/"*//')
    
    # 擷取圖片檔名 (原本既)
    old_image=$(grep "^image:" "$post" | sed 's/image: *//')
    
    # 產生新既圖片檔名（將標題轉為檔名格式）
    filename=$(basename "$old_image")
    
    # 獲取關鍵詞
    keywords=$(get_keywords "$title")
    
    echo "Processing: $title"
    echo "  Keywords: $keywords"
    echo "  File: $filename"
    
    # 下載新圖片
    download_image "$filename" "$keywords"
    echo ""
done

echo "===================="
echo "完成！"