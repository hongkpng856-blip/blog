#!/usr/bin/env python3
import os, re, subprocess, json, sys

POSTS_DIR = os.path.join(os.path.dirname(__file__), '..', '_posts')
BASE_URL = 'https://hongkpng856-blip.github.io/blog'
REPORT_PATH = os.path.join(os.path.dirname(__file__), 'debug_report.txt')

def get_article_url(filepath):
    # filename like 2026-04-03-女性理財規劃.md
    name = os.path.basename(filepath)
    m = re.match(r'(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})-(?P<slug>.+)\.md', name)
    if not m:
        return None
    return f"{BASE_URL}/{m.group('year')}/{m.group('month')}/{m.group('day')}/{m.group('slug')}/"

def get_image_url(filepath):
    with open(filepath, 'r', encoding='utf8') as f:
        for line in f:
            if line.strip().startswith('image:'):
                # line like: image: /assets/images/featured/女性理財規劃.png
                path = line.split(':',1)[1].strip()
                # ensure leading slash
                if not path.startswith('/'):
                    path = '/' + path
                return BASE_URL + path
    return None

def check_url(url):
    try:
        result = subprocess.run(['curl','-s','-o','/dev/null','-w','%{http_code}',url], capture_output=True, text=True, timeout=30)
        return result.stdout.strip()
    except Exception as e:
        return f'error:{e}'

def main():
    failures = []
    for root, _, files in os.walk(POSTS_DIR):
        for f in files:
            if not f.endswith('.md'):
                continue
            fp = os.path.join(root, f)
            article_url = get_article_url(fp)
            image_url = get_image_url(fp)
            if article_url:
                code = check_url(article_url)
                if code != '200':
                    failures.append({'type':'article','file':fp,'url':article_url,'code':code})
            if image_url:
                code = check_url(image_url)
                if code != '200':
                    failures.append({'type':'image','file':fp,'url':image_url,'code':code})
    # write report
    with open(REPORT_PATH,'w',encoding='utf8') as out:
        if not failures:
            out.write('All articles and images returned HTTP 200.\n')
        else:
            out.write(f"Found {len(failures)} issues:\n")
            for f in failures:
                out.write(json.dumps(f, ensure_ascii=False)+'\n')
    print(f"Debug report written to {REPORT_PATH}")
    if failures:
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == '__main__':
    main()
