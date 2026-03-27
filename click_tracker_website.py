#!/usr/bin/env python3
"""
點擊追蹤網站 - 使用 Python 內建 http.server（無需 Flask）
功能：
1. 記錄每個點擊的 IP 地址
2. 儲存點擊時間戳
3. 提供記錄查詢介面
"""

import http.server
import socketserver
import json
import os
import sqlite3
from datetime import datetime
from urllib.parse import urlparse, parse_qs

# 資料庫路徑
DB_PATH = '/home/claw/.openclaw/workspace/click_logs.db'
PORT = 8889

# HTML 模板
INDEX_HTML = '''<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>點擊追蹤網站</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 1000px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }
        h1 { color: #333; text-align: center; }
        .click-area {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 40px;
            margin: 20px 0;
            border-radius: 12px;
            cursor: pointer;
            text-align: center;
            color: white;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            transition: transform 0.2s;
        }
        .click-area:hover { transform: scale(1.02); }
        .click-area h2 { margin: 0; font-size: 28px; }
        #counter { font-size: 48px; font-weight: bold; }
        .stats {
            background: white;
            padding: 20px;
            border-radius: 12px;
            margin-top: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .stats h3 { color: #333; margin-top: 0; }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }
        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        th { background: #667eea; color: white; }
        tr:hover { background: #f9f9f9; }
        .ip-badge {
            background: #667eea;
            color: white;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 14px;
        }
        .time-badge { color: #666; font-size: 14px; }
        .summary {
            display: flex;
            gap: 20px;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }
        .summary-card {
            flex: 1;
            min-width: 150px;
            background: white;
            padding: 20px;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .summary-card h4 { margin: 0; color: #666; }
        .summary-card .number { font-size: 36px; font-weight: bold; color: #667eea; }
        .refresh-btn {
            background: #667eea;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 16px;
            margin-top: 10px;
        }
        .refresh-btn:hover { background: #5a6fd6; }
    </style>
</head>
<body>
    <h1>🌐 點擊追蹤網站</h1>
    
    <div class="click-area" onclick="recordClick()">
        <h2>👆 點擊這裡記錄</h2>
        <p>總點擊次數：<span id="counter">載入中...</span></p>
    </div>
    
    <div class="summary">
        <div class="summary-card">
            <h4>總點擊次數</h4>
            <div class="number" id="totalClicks">-</div>
        </div>
        <div class="summary-card">
            <h4>獨立 IP 數量</h4>
            <div class="number" id="uniqueIPs">-</div>
        </div>
        <div class="summary-card">
            <h4>最後點擊時間</h4>
            <div class="number" id="lastClick" style="font-size: 18px;">-</div>
        </div>
    </div>
    
    <div class="stats">
        <h3>📊 點擊記錄（最近 50 筆）</h3>
        <button class="refresh-btn" onclick="loadRecords()">🔄 刷新記錄</button>
        <table id="recordsTable">
            <thead>
                <tr>
                    <th>#</th>
                    <th>IP 地址</th>
                    <th>時間</th>
                    <th>User-Agent</th>
                </tr>
            </thead>
            <tbody></tbody>
        </table>
    </div>
    
    <script>
        function recordClick() {
            fetch('/api/click', { method: 'POST' })
                .then(r => r.json())
                .then(data => {
                    document.getElementById('counter').textContent = data.total_clicks;
                    loadRecords();
                    loadSummary();
                });
        }
        
        function loadRecords() {
            fetch('/api/records')
                .then(r => r.json())
                .then(data => {
                    const tbody = document.querySelector('#recordsTable tbody');
                    tbody.innerHTML = data.records.map((r, i) => `
                        <tr>
                            <td>${i + 1}</td>
                            <td><span class="ip-badge">${r.ip}</span></td>
                            <td><span class="time-badge">${r.time}</span></td>
                            <td style="font-size:12px;max-width:200px;overflow:hidden;text-overflow:ellipsis;">${r.user_agent}</td>
                        </tr>
                    `).join('');
                });
        }
        
        function loadSummary() {
            fetch('/api/summary')
                .then(r => r.json())
                .then(data => {
                    document.getElementById('totalClicks').textContent = data.total_clicks;
                    document.getElementById('uniqueIPs').textContent = data.unique_ips;
                    document.getElementById('lastClick').textContent = data.last_click || '無記錄';
                    document.getElementById('counter').textContent = data.total_clicks;
                });
        }
        
        // 初始載入
        loadRecords();
        loadSummary();
    </script>
</body>
</html>
'''

def init_db():
    """初始化資料庫"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS clicks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            user_agent TEXT,
            referer TEXT
        )
    ''')
    conn.commit()
    conn.close()

def get_db():
    """獲取資料庫連接"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

class ClickTrackerHandler(http.server.BaseHTTPRequestHandler):
    
    def do_GET(self):
        """處理 GET 請求"""
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/':
            # 首頁
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(INDEX_HTML.encode('utf-8'))
            
        elif parsed_path.path == '/api/records':
            # 獲取記錄
            conn = get_db()
            c = conn.cursor()
            c.execute('SELECT * FROM clicks ORDER BY id DESC LIMIT 50')
            rows = c.fetchall()
            conn.close()
            
            records = []
            for row in rows:
                ua = row['user_agent'] or ''
                records.append({
                    'id': row['id'],
                    'ip': row['ip'],
                    'time': row['timestamp'],
                    'user_agent': ua[:50] + '...' if len(ua) > 50 else ua
                })
            
            self.send_json({'records': records})
            
        elif parsed_path.path == '/api/summary':
            # 獲取統計
            conn = get_db()
            c = conn.cursor()
            
            c.execute('SELECT COUNT(*) FROM clicks')
            total_clicks = c.fetchone()[0]
            
            c.execute('SELECT COUNT(DISTINCT ip) FROM clicks')
            unique_ips = c.fetchone()[0]
            
            c.execute('SELECT timestamp FROM clicks ORDER BY id DESC LIMIT 1')
            row = c.fetchone()
            last_click = row[0] if row else None
            
            conn.close()
            
            self.send_json({
                'total_clicks': total_clicks,
                'unique_ips': unique_ips,
                'last_click': last_click
            })
            
        elif parsed_path.path.startswith('/api/ip/'):
            # 查詢特定 IP
            ip_address = parsed_path.path[8:]
            conn = get_db()
            c = conn.cursor()
            c.execute('SELECT * FROM clicks WHERE ip = ? ORDER BY id DESC', (ip_address,))
            rows = c.fetchall()
            conn.close()
            
            records = [{'id': r['id'], 'ip': r['ip'], 'time': r['timestamp'], 'user_agent': r['user_agent']} for r in rows]
            
            self.send_json({'ip': ip_address, 'count': len(records), 'records': records})
            
        else:
            self.send_error(404, 'Not Found')
    
    def do_POST(self):
        """處理 POST 請求"""
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/api/click':
            # 獲取真實 IP
            ip = self.headers.get('X-Forwarded-For', self.client_address[0])
            if ',' in str(ip):
                ip = ip.split(',')[0].strip()
            
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            user_agent = self.headers.get('User-Agent', 'Unknown')
            referer = self.headers.get('Referer', '')
            
            # 儲存到資料庫
            conn = get_db()
            c = conn.cursor()
            c.execute(
                'INSERT INTO clicks (ip, timestamp, user_agent, referer) VALUES (?, ?, ?, ?)',
                (ip, timestamp, user_agent, referer)
            )
            conn.commit()
            
            c.execute('SELECT COUNT(*) FROM clicks')
            total_clicks = c.fetchone()[0]
            conn.close()
            
            self.send_json({
                'success': True,
                'ip': ip,
                'timestamp': timestamp,
                'total_clicks': total_clicks
            })
        else:
            self.send_error(404, 'Not Found')
    
    def send_json(self, data):
        """發送 JSON 回應"""
        self.send_response(200)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))
    
    def log_message(self, format, *args):
        """自定義日誌格式"""
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {args[0]}")

def main():
    init_db()
    print(f'''
╔════════════════════════════════════════════════════════════╗
║        🌐 點擊追蹤網站已啟動                              ║
╠════════════════════════════════════════════════════════════╣
║  📍 本地訪問：http://localhost:{PORT}                       ║
║  🌍 外部訪問：http://<你的IP>:{PORT}                        ║
║                                                            ║
║  📊 API 端點：                                             ║
║     GET  /              首頁（含記錄查詢介面）             ║
║     POST /api/click     記錄點擊                           ║
║     GET  /api/records   獲取最近 50 筆記錄                 ║
║     GET  /api/summary   獲取統計摘要                       ║
║     GET  /api/ip/<ip>   查詢特定 IP 的所有記錄             ║
║                                                            ║
║  🛑 按 Ctrl+C 停止伺服器                                  ║
╚════════════════════════════════════════════════════════════╝
''')
    
    with socketserver.TCPServer(("", PORT), ClickTrackerHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n👋 伺服器已停止")

if __name__ == '__main__':
    main()
