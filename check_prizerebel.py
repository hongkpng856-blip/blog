#!/usr/bin/env python3
"""
PrizeRebel 點數查詢腳本
使用 requests 保持 session 來登入並獲取點數
"""
import requests
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime

class PrizeRebelChecker:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
        })
        
    def login(self, email, password):
        """登入 PrizeRebel"""
        print(f"📧 嘗試登入: {email}")
        
        # 先訪問登入頁面獲取 CSRF token
        login_page = self.session.get('https://www.prizerebel.com/login.php')
        soup = BeautifulSoup(login_page.text, 'html.parser')
        
        # 查找表單中的 hidden fields
        form_data = {}
        form = soup.find('form', {'action': lambda x: x and 'login' in x.lower()})
        if form:
            for inp in form.find_all('input', type='hidden'):
                if inp.get('name') and inp.get('value'):
                    form_data[inp['name']] = inp['value']
        
        # 添加登入資料
        form_data['email'] = email
        form_data['password'] = password
        
        # 執行登入
        login_response = self.session.post(
            'https://www.prizerebel.com/login.php',
            data=form_data,
            allow_redirects=True
        )
        
        print(f"📄 登入回應狀態: {login_response.status_code}")
        print(f"📄 最終 URL: {login_response.url}")
        
        # 檢查是否成功登入
        if 'dashboard' in login_response.url or 'member' in login_response.url:
            print("✅ 登入成功！")
            return True
        else:
            print("❌ 登入失敗")
            # 保存登入頁面內容供分析
            with open('/home/claw/.openclaw/workspace/pr-login-fail.html', 'w') as f:
                f.write(login_response.text)
            return False
    
    def get_points(self):
        """獲取目前點數"""
        print("📊 獲取點數...")
        
        dashboard = self.session.get('https://www.prizerebel.com/member/dashboard.php')
        soup = BeautifulSoup(dashboard.text, 'html.parser')
        
        # 保存 dashboard HTML
        with open('/home/claw/.openclaw/workspace/pr-dashboard.html', 'w') as f:
            f.write(dashboard.text)
        
        # 嘗試多種方式找到點數
        points = None
        
        # 方法 1: 查找包含 "points" 的元素
        for element in soup.find_all(class_=re.compile(r'points', re.I)):
            text = element.get_text(strip=True)
            match = re.search(r'(\d+)', text)
            if match:
                points = match.group(1)
                print(f"💰 找到點數 (class): {points}")
                break
        
        # 方法 2: 查找包含數字的 span
        if not points:
            for span in soup.find_all('span'):
                text = span.get_text(strip=True)
                if re.match(r'^\d+$', text) and int(text) > 10:
                    # 可能是點數
                    points = text
        
        # 方法 3: 正則搜索整個頁面
        if not points:
            # 查找類似 "XXX points" 或 "Points: XXX" 的模式
            patterns = [
                r'(\d+)\s*points?',
                r'points?\s*[:\s]*(\d+)',
                r'balance[^>]*>.*?(\d+)',
                r'credits?\s*[:\s]*(\d+)'
            ]
            for pattern in patterns:
                match = re.search(pattern, dashboard.text, re.I)
                if match:
                    points = match.group(1)
                    print(f"💰 找到點數 (regex): {points}")
                    break
        
        return points
    
    def get_available_surveys(self):
        """獲取可用的問卷"""
        print("📋 獲取可用問卷...")
        
        surveys_page = self.session.get('https://www.prizerebel.com/surveys.php')
        soup = BeautifulSoup(surveys_page.text, 'html.parser')
        
        # 保存問卷頁面
        with open('/home/claw/.openclaw/workspace/pr-surveys.html', 'w') as f:
            f.write(surveys_page.text)
        
        surveys = []
        # 查找問卷列表
        for item in soup.find_all(class_=re.compile(r'survey|offer|task', re.I)):
            title_elem = item.find(['h3', 'h4', 'span', 'div'], class_=re.compile(r'title|name', re.I))
            points_elem = item.find(class_=re.compile(r'points|reward|credit', re.I))
            
            if title_elem:
                survey = {
                    'title': title_elem.get_text(strip=True),
                    'points': points_elem.get_text(strip=True) if points_elem else 'Unknown'
                }
                surveys.append(survey)
        
        return surveys
    
    def get_earn_offers(self):
        """獲取賺取點數的機會"""
        print("🎯 獲取賺取機會...")
        
        earn_page = self.session.get('https://www.prizerebel.com/earn.php')
        soup = BeautifulSoup(earn_page.text, 'html.parser')
        
        # 保存賺取頁面
        with open('/home/claw/.openclaw/workspace/pr-earn.html', 'w') as f:
            f.write(earn_page.text)
        
        offers = []
        # 嘗試解析 offer
        for link in soup.find_all('a', href=re.compile(r'offer|survey')):
            offer_text = link.get_text(strip=True)
            if offer_text and len(offer_text) > 3:
                offers.append({
                    'text': offer_text,
                    'href': link.get('href', '')
                })
        
        return offers[:10]  # 只返回前 10 個


def main():
    print("=" * 50)
    print("🚀 PrizeRebel 點數檢查")
    print("=" * 50)
    
    checker = PrizeRebelChecker()
    
    # 登入
    email = 'hongkpng856@gmail.com'
    password = 'mtsd479j'
    
    if checker.login(email, password):
        # 獲取點數
        points = checker.get_points()
        print(f"\n📊 目前點數: {points or '未知'}")
        
        # 獲取問卷
        surveys = checker.get_available_surveys()
        print(f"\n📋 找到 {len(surveys)} 個問卷")
        
        # 獲取賺取機會
        offers = checker.get_earn_offers()
        print(f"\n🎯 找到 {len(offers)} 個賺取機會")
        
        # 保存狀態報告
        report = {
            'timestamp': datetime.now().isoformat(),
            'email': email,
            'points': points,
            'surveys_count': len(surveys),
            'offers_count': len(offers),
            'surveys': surveys[:5],
            'offers': offers[:5]
        }
        
        with open('/home/claw/.openclaw/workspace/prizerebel-status.json', 'w') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ 狀態報告已保存: prizerebel-status.json")
        print("=" * 50)
        
        return report
    else:
        print("❌ 無法完成檢查")
        return None


if __name__ == '__main__':
    main()
