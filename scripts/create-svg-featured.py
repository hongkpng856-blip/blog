#!/usr/bin/env python3
"""
AI 圖像生成器 - SVG 特色圖片生成
根據文章內容自動生成吸引人的 SVG 圖片

使用方式:
    python3 create-svg-featured.py "文章標題" "文章分類"
"""

import sys
import os
from datetime import datetime

# 圖片配色方案
COLOR_SCHEMES = {
    "技術": {
        "primary": "#1a237e",      # 深藍
        "secondary": "#3949ab",    # 中藍
        "accent": "#00bcd4",       # 青色
        "gradient": ["#1a237e", "#3949ab", "#00bcd4"]
    },
    "健康": {
        "primary": "#2e7d32",      # 綠色
        "secondary": "#43a047",    # 中綠
        "accent": "#8bc34a",       # 淺綠
        "gradient": ["#2e7d32", "#43a047", "#8bc34a"]
    },
    "生活": {
        "primary": "#f57c00",      # 橙色
        "secondary": "#ff9800",    # 中橙
        "accent": "#ffc107",       # 金色
        "gradient": ["#f57c00", "#ff9800", "#ffc107"]
    },
    "投資": {
        "primary": "#1565c0",      # 藍色
        "secondary": "#1976d2",    # 中藍
        "accent": "#4caf50",       # 綠色（成長）
        "gradient": ["#1565c0", "#1976d2", "#4caf50"]
    },
    "default": {
        "primary": "#1a237e",
        "secondary": "#3949ab",
        "accent": "#00bcd4",
        "gradient": ["#1a237e", "#3949ab", "#00bcd4"]
    }
}

# 圖示模板
ICON_TEMPLATES = {
    "技術": """<circle cx="100" cy="100" r="60" fill="{primary}" opacity="0.8"/>
<circle cx="100" cy="100" r="40" fill="{secondary}" opacity="0.6"/>
<circle cx="100" cy="100" r="20" fill="{accent}"/>
<line x1="100" y1="40" x2="100" y2="160" stroke="{accent}" stroke-width="2" opacity="0.5"/>
<line x1="40" y1="100" x2="160" y2="100" stroke="{accent}" stroke-width="2" opacity="0.5"/>""",
    
    "健康": """<circle cx="100" cy="100" r="50" fill="{primary}" opacity="0.8"/>
<path d="M80 100 L90 110 L120 80" stroke="white" stroke-width="6" fill="none" stroke-linecap="round"/>
<circle cx="100" cy="50" r="15" fill="{accent}"/>
<rect x="95" y="50" width="10" height="30" fill="{accent}"/>""",
    
    "生活": """<circle cx="100" cy="100" r="50" fill="{primary}" opacity="0.8"/>
<circle cx="80" cy="80" r="15" fill="{accent}"/>
<circle cx="120" cy="80" r="15" fill="{accent}"/>
<path d="M70 110 Q100 130 130 110" stroke="white" stroke-width="4" fill="none"/>
<circle cx="100" cy="100" r="8" fill="{secondary}"/>""",
    
    "投資": """<path d="M40 140 L80 100 L100 120 L140 60 L160 80" stroke="{accent}" stroke-width="4" fill="none"/>
<circle cx="40" cy="140" r="8" fill="{primary}"/>
<circle cx="80" cy="100" r="8" fill="{primary}"/>
<circle cx="100" cy="120" r="8" fill="{primary}"/>
<circle cx="140" cy="60" r="8" fill="{accent}"/>
<circle cx="160" cy="80" r="8" fill="{accent}"/>
<rect x="30" y="150" width="140" height="20" fill="{primary}" opacity="0.3" rx="5"/>""",
    
    "default": """<circle cx="100" cy="100" r="50" fill="{primary}" opacity="0.8"/>
<circle cx="100" cy="100" r="30" fill="{secondary}" opacity="0.6"/>
<circle cx="100" cy="100" r="15" fill="{accent}"/>"""
}

def generate_svg(title: str, category: str, output_dir: str = None) -> str:
    """生成 SVG 圖片"""
    
    # 取得配色
    colors = COLOR_SCHEMES.get(category, COLOR_SCHEMES["default"])
    
    # 取得圖示
    icon = ICON_TEMPLATES.get(category, ICON_TEMPLATES["default"])
    
    # 替換顏色
    icon = icon.format(
        primary=colors["primary"],
        secondary=colors["secondary"],
        accent=colors["accent"]
    )
    
    # 生成檔名
    filename = title.lower().replace(" ", "-").replace("，", "-")
    filename = "".join(c for c in filename if c.isalnum() or c == "-")
    filename = f"{filename}.svg"
    
    # SVG 內容
    svg_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="800" height="400" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
  <!-- 背景 -->
  <defs>
    <linearGradient id="bg-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:{colors["gradient"][0]};stop-opacity:1" />
      <stop offset="50%" style="stop-color:{colors["gradient"][1]};stop-opacity:1" />
      <stop offset="100%" style="stop-color:{colors["gradient"][2]};stop-opacity:1" />
    </linearGradient>
    <filter id="shadow">
      <feDropShadow dx="2" dy="2" stdDeviation="3" flood-opacity="0.3"/>
    </filter>
  </defs>
  
  <rect width="200" height="200" fill="url(#bg-gradient)"/>
  
  <!-- 裝飾元素 -->
  <circle cx="30" cy="30" r="40" fill="white" opacity="0.1"/>
  <circle cx="170" cy="170" r="50" fill="white" opacity="0.1"/>
  <circle cx="170" cy="30" r="30" fill="white" opacity="0.05"/>
  
  <!-- 主要圖示 -->
  <g filter="url(#shadow)">
    {icon}
  </g>
  
  <!-- 標題文字 -->
  <text x="100" y="185" text-anchor="middle" font-family="Arial, sans-serif" font-size="12" fill="white" font-weight="bold">
    {title[:20]}{"..." if len(title) > 20 else ""}
  </text>
</svg>'''
    
    # 輸出路徑
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, filename)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(svg_content)
        return output_path
    
    return svg_content


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("使用方式: python3 create-svg-featured.py \"文章標題\" \"文章分類\" [輸出目錄]")
        print("範例: python3 create-svg-featured.py \"健康生活的秘訣\" \"健康\" ../assets/images/featured/")
        sys.exit(1)
    
    title = sys.argv[1]
    category = sys.argv[2]
    output_dir = sys.argv[3] if len(sys.argv) > 3 else None
    
    result = generate_svg(title, category, output_dir)
    
    if output_dir:
        print(f"✅ SVG 圖片已生成: {result}")
    else:
        print(result)
