#!/usr/bin/env python3
"""
AI 圖片生成器 - 使用多種免費 API
為部落格文章生成真正的 AI 圖片

支援的 API:
1. Hugging Face Inference API (免費)
2. Pollinations (免費，無需 key)
"""

import json
import urllib.parse
import urllib.request
import os
import sys
import time
import random

def generate_image_hf(prompt: str, output_path: str, model: str = "stable-diffusion-v1-5"):
    """
    使用 Hugging Face 免費 Inference API 生成圖片
    
    免費模型: stable-diffusion-v1-5, stable-diffusion-xl-base-1.0
    """
    API_URL = f"https://api-inference.huggingface.co/models/stabilityai/{model}"
    
    print(f"🎨 使用 Hugging Face API 生成圖片...")
    print(f"📝 Prompt: {prompt[:100]}...")
    print(f"🤖 Model: {model}")
    
    try:
        # 建立請求
        data = json.dumps({"inputs": prompt}).encode('utf-8')
        req = urllib.request.Request(
            API_URL,
            data=data,
            headers={
                'Content-Type': 'application/json',
                'User-Agent': 'Mozilla/5.0'
            },
            method='POST'
        )
        
        # 發送請求
        with urllib.request.urlopen(req, timeout=120) as response:
            image_data = response.read()
        
        if len(image_data) < 1000:
            print(f"⚠️ 圖片太小 ({len(image_data)} bytes)，可能是錯誤回應")
            return False
        
        # 確保目錄存在
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # 儲存圖片
        with open(output_path, 'wb') as f:
            f.write(image_data)
        
        print(f"✅ 圖片已儲存: {output_path}")
        print(f"📊 檔案大小: {len(image_data) / 1024:.1f} KB")
        return True
        
    except urllib.error.HTTPError as e:
        print(f"❌ HTTP Error {e.code}: {e.reason}")
        if e.code == 503:
            print("⚠️ 模型正在載入中，請稍後再試")
        return False
    except Exception as e:
        print(f"❌ 生成失敗: {e}")
        return False

def generate_image_pollinations(prompt: str, output_path: str, width: int = 1280, height: int = 720):
    """
    使用 Pollinations API 生成圖片
    
    直接 URL: https://image.pollinations.ai/prompt/{prompt}?width=1280&height=720&nologo=true
    """
    encoded_prompt = urllib.parse.quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={width}&height={height}&nologo=true&seed={random.randint(1000,99999)}"
    
    print(f"🎨 使用 Pollinations API 生成圖片...")
    print(f"📝 Prompt: {prompt[:100]}...")
    print(f"🔗 URL: {url[:150]}...")
    
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'image/png,image/*'
        })
        
        with urllib.request.urlopen(req, timeout=180) as response:
            image_data = response.read()
        
        # 檢查是否為 JSON 錯誤
        if image_data[:1] == b'{' or image_data[:1] == b'{':
            print(f"⚠️ API 返回錯誤: {image_data.decode('utf-8', errors='ignore')[:200]}")
            return False
        
        if len(image_data) < 1000:
            print(f"❌ 圖片太小 ({len(image_data)} bytes)")
            return False
        
        # 確保目錄存在
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # 儲存圖片
        with open(output_path, 'wb') as f:
            f.write(image_data)
        
        print(f"✅ 圖片已儲存: {output_path}")
        print(f"📊 檔案大小: {len(image_data) / 1024:.1f} KB")
        return True
        
    except urllib.error.HTTPError as e:
        print(f"❌ HTTP Error {e.code}: {e.reason}")
        return False
    except Exception as e:
        print(f"❌ 生成失敗: {e}")
        return False

def generate_image(prompt: str, output_path: str, method: str = "auto"):
    """
    使用免費 API 生成圖片
    
    Args:
        prompt: 圖片描述提示詞
        output_path: 輸出圖片路徑
        method: 使用的方法 (auto, hf, pollinations)
    """
    if method == "auto":
        # 先嘗試 Pollinations，再嘗試 HF
        if generate_image_pollinations(prompt, output_path):
            return True
        print("⏳ Pollinations 失敗，嘗試 Hugging Face...")
        time.sleep(2)
        if generate_image_hf(prompt, output_path):
            return True
        return False
    elif method == "pollinations":
        return generate_image_pollinations(prompt, output_path)
    elif method == "hf":
        return generate_image_hf(prompt, output_path)
    else:
        return generate_image_pollinations(prompt, output_path)

def generate_for_article(title: str, category: str, content_summary: str, output_dir: str, method: str = "auto"):
    """
    為文章生成特色圖片
    
    Args:
        title: 文章標題
        category: 文章分類
        content_summary: 內容摘要
        output_dir: 輸出目錄
        method: 使用的方法 (auto, hf, pollinations)
    """
    
    # 根據分類選擇風格
    style_map = {
        "技術": "modern technology digital art, clean minimalist design, blue color scheme, futuristic, professional, high quality, 16:9 aspect ratio",
        "生活": "warm lifestyle photography, bright natural lighting, cozy atmosphere, soft colors, inspiring, photorealistic, 16:9 aspect ratio",
        "健康": "fresh wellness photography, natural green tones, healthy lifestyle, peaceful, clean design, photorealistic, 16:9 aspect ratio",
        "投資": "professional business finance, gold and dark blue colors, elegant, trustworthy, modern, high quality, 16:9 aspect ratio"
    }
    
    category_style = style_map.get(category, "professional, clean, modern, high quality, 16:9 aspect ratio")
    
    # 建構提示詞（英文效果更好）
    prompt = f"""Create a beautiful featured image for a blog article.
Title: {title}
Theme: {content_summary}
Style: {category_style}
Requirements: High quality, visually appealing, suitable for blog featured image, 16:9 aspect ratio, no text overlay, professional look"""
    
    # 輸出檔名（處理中文）
    safe_title = title.replace(" ", "-").replace("/", "-")
    output_path = os.path.join(output_dir, f"{safe_title}.png")
    
    return generate_image(prompt, output_path, method=method)

def main():
    """主程式"""
    if len(sys.argv) < 4:
        print("使用方式: python3 generate_ai_image.py <標題> <分類> <輸出目錄> [內容摘要]")
        print("範例: python3 generate_ai_image.py '如何在 GitHub Pages 建立個人部落格' '技術' './assets/images/featured/' 'Jekyll 部落格教學'")
        print("\n選項:")
        print("  --method <auto|hf|pollinations>  選擇生成方法（預設 auto）")
        sys.exit(1)
    
    title = sys.argv[1]
    category = sys.argv[2]
    output_dir = sys.argv[3]
    content_summary = sys.argv[4] if len(sys.argv) > 4 else f"關於{title}的深度探討"
    method = sys.argv[6] if "--method" in sys.argv else "auto"
    
    success = generate_for_article(title, category, content_summary, output_dir, method=method)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
