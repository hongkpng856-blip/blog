#!/usr/bin/env python3
"""修復文章中的 image 路徑：將冒號改為連字符"""

import os
import re

POSTS_DIR = "_posts"

def get_actual_files():
    """獲取實際存在的圖片檔案名"""
    featured_dir = "assets/images/featured"
    files = os.listdir(featured_dir)
    # 建立映射：正規化名稱 -> 實際檔名
    normalized_map = {}
    for f in files:
        if f.endswith(('.jpg', '.jpeg', '.png', '.gif', '.svg')):
            # 移除副檔名
            name = os.path.splitext(f)[0]
            # 將所有非字母數字替換為連字符
            normalized = re.sub(r'[^a-zA-Z0-9\u4e00-\u9fff]', '-', name)
            normalized = re.sub(r'-+', '-', normalized).strip('-').lower()
            normalized_map[normalized] = f
    return normalized_map

def normalize_filename(filename):
    """將檔名正規化以便匹配"""
    name = os.path.splitext(filename)[0]
    normalized = re.sub(r'[^a-zA-Z0-9\u4e00-\u9fff]', '-', name)
    normalized = re.sub(r'-+', '-', normalized).strip('-').lower()
    return normalized

def find_matching_file(image_name, normalized_map):
    """找到實際存在的檔案"""
    normalized = normalize_filename(image_name)
    
    # 直接匹配
    if normalized in normalized_map:
        return normalized_map[normalized]
    
    # 嘗試部分匹配
    for key, value in normalized_map.items():
        if normalized in key or key in normalized:
            return value
    
    return None

def fix_posts():
    """修復所有文章中的 image 路徑"""
    normalized_map = get_actual_files()
    print(f"找到 {len(normalized_map)} 個圖片檔案")
    
    fixed_count = 0
    posts = [f for f in os.listdir(POSTS_DIR) if f.endswith('.md')]
    
    for post in posts:
        post_path = os.path.join(POSTS_DIR, post)
        with open(post_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 找 image 欄位
        match = re.search(r'^image:\s*(.+)$', content, re.MULTILINE)
        if not match:
            continue
        
        old_image = match.group(1).strip().strip('"').strip("'")
        image_name = os.path.basename(old_image)
        
        # 找匹配的實際檔案
        new_filename = find_matching_file(image_name, normalized_map)
        
        if new_filename and new_filename != image_name:
            new_image = f"/assets/images/featured/{new_filename}"
            new_content = content.replace(old_image, new_image)
            
            with open(post_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print(f"✅ {post}")
            print(f"   {image_name}")
            print(f"   → {new_filename}")
            fixed_count += 1
        elif not new_filename:
            print(f"⚠️ 找不到對應檔案: {image_name}")
    
    print(f"\n總共修復 {fixed_count} 篇文章")

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    fix_posts()