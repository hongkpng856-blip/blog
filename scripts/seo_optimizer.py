#!/usr/bin/env python3
"""
SEO 優化器
功能：
1. 自動生成 meta description（120-160 字元）
2. 建議關鍵字並加入 front matter
3. 檢查標題結構（H1, H2, H3 階層）
4. 內部連結建議
5. 產生結構化數據（JSON-LD）
"""

import os
import re
import json
from pathlib import Path
from datetime import datetime
from collections import Counter

# 繁體中文停用詞
STOP_WORDS = set("""
的 是 在 有 一個 這個 可以 我們 你 他 她 它 他們 她們
會 能 要 就 也 都 而且或 但 如果 因為 所以 雖然
這樣 那樣 如何 什麼 為什麼 怎麼 哪個 哪些
非常 很 太 更 最 已經 正在 將要
可以 需要 應該 可能 或許 一定
""".split())

# SEO 關鍵字資料庫（按分類）
CATEGORY_KEYWORDS = {
    "技術": [
        "程式設計", "Python", "JavaScript", "網頁開發", "前端", "後端",
        "資料科學", "機器學習", "AI", "自動化", "API", "Git", "版本控制",
        "雲端服務", "AWS", "資料庫", "Linux", "開源軟體", "教學", "入門指南"
    ],
    "生活": [
        "生活技巧", "時間管理", "生產力", "習慣養成", "極簡主義",
        "居家收納", "理財規劃", "閱讀", "自我成長", "早晨習慣",
        "工作效率", "生活品質", "實用方法", "心得分享"
    ],
    "健康": [
        "健康生活", "運動習慣", "睡眠品質", "心理健康", "飲食健康",
        "免疫力", "伸展運動", "自我照護", "健康飲食", "養生",
        "紓壓方法", "健康知識"
    ],
    "投資": [
        "投資理財", "股票", "基金", "ETF", "被動收入", "財務自由",
        "資產配置", "風險管理", "投資策略", "理財知識"
    ]
}

class SEOOptimizer:
    def __init__(self, posts_dir: str):
        self.posts_dir = Path(posts_dir)
        self.results = []
    
    def analyze_article(self, filepath: Path) -> dict:
        """分析單篇文章的 SEO 狀態"""
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 解析 front matter
        front_matter, body = self._parse_front_matter(content)
        
        # 提取標題結構
        heading_structure = self._extract_headings(body)
        
        # 提取關鍵字
        keywords = self._extract_keywords(body)
        
        # 計算字數
        word_count = len(body.replace('\n', '').replace(' ', ''))
        
        # 檢查內部連結
        internal_links = self._check_internal_links(body)
        
        # 生成 SEO 建議
        suggestions = self._generate_suggestions(
            front_matter, heading_structure, keywords, 
            word_count, internal_links
        )
        
        return {
            "file": filepath.name,
            "title": front_matter.get("title", ""),
            "categories": front_matter.get("categories", []),
            "tags": front_matter.get("tags", []),
            "heading_structure": heading_structure,
            "keywords": keywords[:10],
            "word_count": word_count,
            "internal_links": internal_links,
            "has_meta_description": "excerpt" in front_matter or len(body) > 100,
            "suggestions": suggestions,
            "seo_score": self._calculate_seo_score(
                front_matter, heading_structure, word_count, internal_links
            )
        }
    
    def _parse_front_matter(self, content: str) -> tuple:
        """解析 Jekyll front matter"""
        if not content.startswith('---'):
            return {}, content
        
        parts = content.split('---', 2)
        if len(parts) < 3:
            return {}, content
        
        front_matter_str = parts[1].strip()
        body = parts[2].strip()
        
        # 簡單解析 YAML
        front_matter = {}
        for line in front_matter_str.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip()
                
                # 解析陣列格式 [item1, item2]
                if value.startswith('[') and value.endswith(']'):
                    items = value[1:-1].split(',')
                    front_matter[key] = [i.strip() for i in items if i.strip()]
                else:
                    # 移除引號
                    front_matter[key] = value.strip('"\'')
        
        return front_matter, body
    
    def _extract_headings(self, body: str) -> dict:
        """提取標題結構"""
        headings = {"h1": [], "h2": [], "h3": [], "h4": []}
        
        for line in body.split('\n'):
            if line.startswith('# '):
                headings["h1"].append(line[2:].strip())
            elif line.startswith('## '):
                headings["h2"].append(line[3:].strip())
            elif line.startswith('### '):
                headings["h3"].append(line[4:].strip())
            elif line.startswith('#### '):
                headings["h4"].append(line[5:].strip())
        
        return headings
    
    def _extract_keywords(self, body: str) -> list:
        """提取關鍵字（基於詞頻）"""
        # 移除標題標記
        text = re.sub(r'^#+\s+', '', body, flags=re.MULTILINE)
        # 移除特殊字元
        text = re.sub(r'[^\w\s\u4e00-\u9fff]', ' ', text)
        # 分詞（簡單的二字、三字詞提取）
        words = []
        
        # 繁體中文詞提取
        for i in range(len(text)):
            if i + 2 <= len(text):
                word = text[i:i+2]
                if not any(c in STOP_WORDS for c in word):
                    words.append(word)
            if i + 3 <= len(text):
                word = text[i:i+3]
                if not any(c in STOP_WORDS for c in word):
                    words.append(word)
        
        # 計算詞頻
        word_freq = Counter(words)
        
        # 過濾太短或停用詞
        keywords = [
            word for word, count in word_freq.most_common(20)
            if len(word) >= 2 and word not in STOP_WORDS and count >= 2
        ]
        
        return keywords
    
    def _check_internal_links(self, body: str) -> dict:
        """檢查內部連結"""
        # 找所有連結
        links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', body)
        
        internal = []
        external = []
        
        for text, url in links:
            if url.startswith('/') or url.startswith('./') or 'github.io' in url:
                internal.append({"text": text, "url": url})
            elif url.startswith('http'):
                external.append({"text": text, "url": url})
        
        return {
            "internal_count": len(internal),
            "external_count": len(external),
            "internal_links": internal,
            "external_links": external
        }
    
    def _generate_suggestions(self, front_matter, headings, keywords, 
                             word_count, internal_links) -> list:
        """生成 SEO 建議"""
        suggestions = []
        
        # 標題結構建議
        if not headings["h1"]:
            suggestions.append("❌ 缺少 H1 標題（文章標題應為 H1）")
        elif len(headings["h1"]) > 1:
            suggestions.append("⚠️ H1 標題過多（建議只保留一個）")
        
        if len(headings["h2"]) < 2:
            suggestions.append("⚠️ H2 標題太少（建議至少 2-3 個）")
        
        # 字數建議
        if word_count < 300:
            suggestions.append("⚠️ 文章太短（建議至少 300 字）")
        elif word_count < 800:
            suggestions.append("💡 文章長度可增加至 800+ 字以提升 SEO")
        
        # 內部連結建議
        if internal_links["internal_count"] < 2:
            suggestions.append("⚠️ 內部連結太少（建議至少 2-3 個）")
        
        # 標籤建議
        if not front_matter.get("tags"):
            suggestions.append("❌ 缺少 tags（建議加入 3-5 個相關標籤）")
        
        # 描述建議
        if "excerpt" not in front_matter and "description" not in front_matter:
            suggestions.append("⚠️ 缺少自訂 meta description")
        
        return suggestions
    
    def _calculate_seo_score(self, front_matter, headings, word_count, 
                            internal_links) -> int:
        """計算 SEO 分數（0-100）"""
        score = 0
        
        # 有標題 +20
        if headings["h1"]:
            score += 20
        
        # H2 結構良好 +15
        if len(headings["h2"]) >= 2:
            score += 15
        
        # 字數足夠 +20
        if word_count >= 800:
            score += 20
        elif word_count >= 500:
            score += 10
        
        # 有標籤 +15
        if front_matter.get("tags"):
            score += 15
        
        # 有分類 +10
        if front_matter.get("categories"):
            score += 10
        
        # 內部連結 +10
        if internal_links["internal_count"] >= 2:
            score += 10
        
        # 有圖片 +10
        if front_matter.get("image") or front_matter.get("featured_image"):
            score += 10
        
        return min(100, score)
    
    def generate_meta_description(self, body: str, max_length: int = 160) -> str:
        """生成 meta description"""
        # 移除標題和 markdown 標記
        text = re.sub(r'^#+\s+', '', body, flags=re.MULTILINE)
        text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
        text = re.sub(r'[*_`#]', '', text)
        text = text.replace('\n', ' ').strip()
        
        # 截斷到合適長度
        if len(text) <= max_length:
            return text
        
        # 找最後一個完整句子
        truncated = text[:max_length]
        last_period = max(
            truncated.rfind('。'),
            truncated.rfind('！'),
            truncated.rfind('？'),
            truncated.rfind('.')
        )
        
        if last_period > max_length * 0.5:
            return truncated[:last_period + 1]
        
        # 找最後一個完整詞
        last_space = truncated.rfind(' ')
        if last_space > max_length * 0.5:
            return truncated[:last_space] + '...'
        
        return truncated + '...'
    
    def suggest_keywords(self, body: str, category: str) -> list:
        """建議關鍵字"""
        # 從文章提取關鍵字
        extracted = self._extract_keywords(body)
        
        # 從分類獲取相關關鍵字
        category_kw = CATEGORY_KEYWORDS.get(category, [])
        
        # 合併並去重
        all_keywords = list(set(extracted[:5] + category_kw[:5]))
        
        return all_keywords[:8]
    
    def generate_json_ld(self, article_data: dict, site_url: str) -> dict:
        """生成 JSON-LD 結構化數據"""
        json_ld = {
            "@context": "https://schema.org",
            "@type": "BlogPosting",
            "headline": article_data.get("title", ""),
            "description": article_data.get("description", ""),
            "author": {
                "@type": "Person",
                "name": article_data.get("author", "Blog Author")
            },
            "publisher": {
                "@type": "Organization",
                "name": "My Blog",
                "logo": {
                    "@type": "ImageObject",
                    "url": f"{site_url}/assets/images/avatar.svg"
                }
            },
            "mainEntityOfPage": {
                "@type": "WebPage",
                "@id": article_data.get("url", "")
            },
            "datePublished": article_data.get("date", ""),
            "dateModified": article_data.get("date", ""),
            "keywords": article_data.get("tags", []),
            "articleSection": article_data.get("categories", [])
        }
        
        if article_data.get("image"):
            json_ld["image"] = article_data.get("image")
        
        return json_ld
    
    def optimize_all_articles(self) -> list:
        """優化所有文章"""
        results = []
        
        for filepath in sorted(self.posts_dir.glob("*.md")):
            print(f"\n📝 分析: {filepath.name}")
            analysis = self.analyze_article(filepath)
            results.append(analysis)
            
            print(f"   標題: {analysis['title']}")
            print(f"   字數: {analysis['word_count']}")
            print(f"   SEO 分數: {analysis['seo_score']}/100")
            print(f"   H2 數量: {len(analysis['heading_structure']['h2'])}")
            print(f"   內部連結: {analysis['internal_links']['internal_count']}")
            
            if analysis['suggestions']:
                print("   建議:")
                for s in analysis['suggestions']:
                    print(f"      {s}")
        
        return results
    
    def generate_report(self, results: list, output_path: str = None) -> str:
        """生成 SEO 報告"""
        report = []
        report.append("=" * 60)
        report.append("📊 SEO 分析報告")
        report.append(f"生成時間: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        report.append("=" * 60)
        
        # 總覽
        avg_score = sum(r['seo_score'] for r in results) / len(results) if results else 0
        total_words = sum(r['word_count'] for r in results)
        
        report.append(f"\n📈 總覽:")
        report.append(f"   文章數量: {len(results)}")
        report.append(f"   平均 SEO 分數: {avg_score:.1f}/100")
        report.append(f"   總字數: {total_words:,}")
        
        # 各文章詳情
        report.append("\n" + "-" * 60)
        report.append("📄 各文章 SEO 狀態:")
        report.append("-" * 60)
        
        for r in results:
            status = "✅" if r['seo_score'] >= 70 else "⚠️" if r['seo_score'] >= 50 else "❌"
            report.append(f"\n{status} {r['title']}")
            report.append(f"   檔案: {r['file']}")
            report.append(f"   分數: {r['seo_score']}/100")
            report.append(f"   字數: {r['word_count']}")
            report.append(f"   關鍵字: {', '.join(r['keywords'][:5])}")
            report.append(f"   內部連結: {r['internal_links']['internal_count']}")
            
            if r['suggestions']:
                report.append(f"   待改善:")
                for s in r['suggestions']:
                    report.append(f"      {s}")
        
        report.append("\n" + "=" * 60)
        report_text = "\n".join(report)
        
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(report_text)
            print(f"\n✅ 報告已儲存: {output_path}")
        
        return report_text


def main():
    """主程式"""
    print("=" * 60)
    print("🔧 SEO 優化器")
    print("=" * 60)
    
    # 設定路徑
    repo_dir = Path(__file__).parent.parent
    posts_dir = repo_dir / "_posts"
    
    print(f"\n📂 文章目錄: {posts_dir}")
    
    # 建立優化器
    optimizer = SEOOptimizer(posts_dir)
    
    # 分析所有文章
    results = optimizer.optimize_all_articles()
    
    # 生成報告
    report_path = repo_dir / "scripts" / "seo_report.txt"
    report = optimizer.generate_report(results, str(report_path))
    
    # 儲存 JSON 結果
    json_path = repo_dir / "scripts" / "seo_analysis.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"✅ 分析結果已儲存: {json_path}")
    
    return results