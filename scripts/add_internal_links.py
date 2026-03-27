#!/usr/bin/env python3
"""
為文章添加內部連結（SEO 優化）
"""

import os
import re
from pathlib import Path
from datetime import datetime

def add_internal_links_to_post(filepath: Path, all_posts: list) -> bool:
    """為單篇文章添加內部連結"""
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
    
    # 提取當前文章資訊
    title_match = re.search(r'title:\s*["\']?([^"\'\n]+)["\']?', front_matter_str)
    current_title = title_match.group(1) if title_match else ""
    
    categories_match = re.search(r'categories:\s*\[([^\]]+)\]', front_matter_str)
    current_category = categories_match.group(1).strip() if categories_match else ""
    
    # 檢查是否已有相關文章區塊
    if '延伸閱讀' in body or '相關文章' in body:
        print(f"  ⏭️ 已有相關文章區塊")
        return False
    
    # 找同分類的其他文章
    related_posts = []
    for post in all_posts:
        if post['title'] == current_title:
            continue
        if post['category'] == current_category:
            related_posts.insert(0, post)
        if len(related_posts) >= 3:
            break
    
    # 如果同分類不足，補其他文章
    if len(related_posts) < 3:
        for post in all_posts:
            if post['title'] == current_title:
                continue
            if post not in related_posts:
                related_posts.append(post)
            if len(related_posts) >= 3:
                break
    
    if not related_posts:
        return False
    
    # 生成相關文章連結
    links_lines = ["", "---", "", "*📖 延伸閱讀：*", ""]
    for post in related_posts[:3]:
        links_lines.append(f"- [{post['title']}]({{{{ site.baseurl }}}}{post['url']})")
    
    # 添加到文章末尾
    new_body = body + '\n'.join(links_lines)
    
    # 寫回檔案
    new_content = f"---\n{front_matter_str}\n---\n{new_body}\n"
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return True


def main():
    """主程式"""
    print("=" * 60)
    print("🔗 為文章添加內部連結")
    print("=" * 60)
    
    repo_dir = Path(__file__).parent.parent
    posts_dir = repo_dir / "_posts"
    
    # 收集所有文章資訊
    all_posts = []
    for filepath in sorted(posts_dir.glob("*.md")):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 提取資訊
        title_match = re.search(r'title:\s*["\']?([^"\'\n]+)["\']?', content)
        categories_match = re.search(r'categories:\s*\[([^\]]+)\]', content)
        date_match = re.search(r'date:\s*(\d{4}-\d{2}-\d{2})', content)
        
        if title_match:
            title = title_match.group(1).strip()
            category = categories_match.group(1).strip() if categories_match else ""
            date = date_match.group(1) if date_match else ""
            
            # 生成 URL
            safe_title = re.sub(r'[^\w\s-]', '', title)
            safe_title = re.sub(r'[\s]+', '-', safe_title)
            url = f"/{date.replace('-', '/')}/{safe_title}/"
            
            all_posts.append({
                'filepath': filepath,
                'title': title,
                'category': category,
                'url': url,
                'date': date
            })
    
    print(f"\n📚 找到 {len(all_posts)} 篇文章")
    
    # 為每篇文章添加內部連結
    updated = 0
    for post in all_posts:
        print(f"\n📝 處理: {post['title']}")
        if add_internal_links_to_post(post['filepath'], all_posts):
            updated += 1
            print(f"  ✅ 已添加內部連結")
    
    print(f"\n" + "=" * 60)
    print(f"✅ 完成：更新了 {updated} 篇文章")
    print("=" * 60)


if __name__ == "__main__":
    main()
