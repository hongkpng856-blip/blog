#!/usr/bin/env python3
"""
為文章添加 meta description（SEO 優化）
"""

import os
import re
from pathlib import Path


def generate_description(body: str, title: str, max_length: int = 155) -> str:
    """根據文章內容生成 description"""
    # 移除 markdown 語法
    clean_body = re.sub(r'```[^`]+```', '', body, flags=re.DOTALL)
    clean_body = re.sub(r'`[^`]+`', '', clean_body)
    clean_body = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', clean_body)
    clean_body = re.sub(r'#{1,6}\s*', '', clean_body)
    clean_body = re.sub(r'\*+([^*]+)\*+', r'\1', clean_body)
    clean_body = re.sub(r'\n+', ' ', clean_body)
    clean_body = re.sub(r'\s+', ' ', clean_body).strip()
    
    # 取前幾句作為描述
    sentences = re.split(r'[。！？\.\!\?]', clean_body)
    
    description = ""
    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
        test_desc = description + sentence + "。"
        if len(test_desc) > max_length:
            break
        description = test_desc
    
    # 確保不超過限制
    if len(description) > max_length:
        description = description[:max_length-3] + "..."
    
    # 如果太短，添加標題
    if len(description) < 80:
        description = f"{title} - {description}"
        if len(description) > max_length:
            description = description[:max_length-3] + "..."
    
    return description.strip()


def add_meta_description(filepath: Path) -> bool:
    """為單篇文章添加 meta description"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 解析 front matter
    if not content.startswith('---'):
        return False
    
    parts = content.split('---', 2)
    if len(parts) < 3:
        return False
    
    front_matter_str = parts[1].strip()
    body = parts[2].strip()
    
    # 檢查是否已有 description
    if re.search(r'^description:', front_matter_str, re.MULTILINE):
        print(f"  ⏭️ 已有 description")
        return False
    
    # 提取標題
    title_match = re.search(r'title:\s*["\']?([^"\'\n]+)["\']?', front_matter_str)
    title = title_match.group(1).strip() if title_match else "文章"
    
    # 生成 description
    description = generate_description(body, title)
    
    # 添加到 front matter
    new_front_matter = front_matter_str + f"\ndescription: \"{description}\""
    new_content = f"---\n{new_front_matter}\n---\n{body}\n"
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"  ✅ 已添加: {description[:50]}...")
    return True


def main():
    """主程式"""
    print("=" * 60)
    print("📝 為文章添加 meta description")
    print("=" * 60)
    
    repo_dir = Path(__file__).parent.parent
    posts_dir = repo_dir / "_posts"
    
    updated = 0
    for filepath in sorted(posts_dir.glob("*.md")):
        title_match = None
        with open(filepath, 'r', encoding='utf-8') as f:
            first_lines = f.read(500)
            title_match = re.search(r'title:\s*["\']?([^"\'\n]+)["\']?', first_lines)
        
        title = title_match.group(1).strip() if title_match else filepath.name
        print(f"\n📄 處理: {title}")
        
        if add_meta_description(filepath):
            updated += 1
    
    print(f"\n" + "=" * 60)
    print(f"✅ 完成：更新了 {updated} 篇文章")
    print("=" * 60)


if __name__ == "__main__":
    main()
