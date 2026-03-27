#!/usr/bin/env python3
"""
訪客追蹤網站 - 自動記錄所有訪客 IP
功能：
1. 頁面載入時自動記錄 IP（無需點擊）
2. 顯示訪客自己的 IP
3. 記錄時間戳、User-Agent、Referer
4. 提供記錄查詢介面
"""

import http.server
import socketserver
import json
import sqlite3
from datetime import datetime
from urllib.parse import urlparse, parse_qs

# 資料庫路徑
DB_PATH = '/home/claw/.openclaw/workspace/visitor_logs.db'
PORT = 8890

# HTML 模板 - 自動記錄版
INDEX_HTML = '''<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>訪客追蹤網站</title>
    <style>
        * { box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 1000px;
            margin: 0 auto;
            padding: 20px;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            min-height: 100vh;
            color: #fff;
        }
        h1 { text-align: center; margin-bottom: 10px; }
        .subtitle { text-align: center; color: #888; margin-bottom: 30px; }
        
        .your-ip {
            background: linear-gradient(135deg, #00d2ff 0%, #3a7bd5 100%);
            padding: 30px;
            border-radius: 16px;
            text-align: center;
            margin-bottom: 20px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        }
        .your-ip h2 { margin: 0 0 10px 0; font-size: 18px; }
        .your-ip .ip { font-size: 36px; font-weight: bold; }
        .your-ip .time { font-size: 14px; opacity: 0.8; margin-top: 10px; }
        
        .status {
            text-align: center;
            padding: 15px;
            border-radius: 12px;
            margin-bottom: 20px;
        }
        .status.success { background: rgba(46, 204, 113, 0.2); color: #2ecc71; }
        .status.loading { background: rgba(52, 152, 219, 0.2); color: #3498db; }
        
        .summary {
            display: flex;
            gap: 15px;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }
        .summary-card {
            flex: 1;
            min-width: 150px;
            background: rgba(255,255,255,0.1);
            padding: 20px;
            border-radius: 12px;
            text-align: center;
        }
        .summary-card h4 { margin: 0 0 5px 0; color: #888; font-size: 14px; }
        .summary-card .number { font-size: 32px; font-weight: bold; color: #00d2ff; }
        
        .records {
            background: rgba(255,255,255,0.05);
            border-radius: 16px;
            padding: 20px;
        }
        .records h3 { margin-top: 0; }
        
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }
        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }
        th { background: rgba(0,210,255,0.2); color: #00d2ff; }
        tr:hover { background: rgba(255,255,255,0.05); }
        .ip-badge {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 13px;
        }
        .time-badge { color: #888; font-size: 13px; }
        .ua-text { font-size: 11px; color: #666; max-width: 200px; overflow: hidden; text-overflow: ellipsis; }
        
        .refresh-btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 14px;
            margin-top: 10px;
        }
        .refresh-btn:hover { opacity: 0.9; }
        
        .auto-badge {
            display: inline-block;
            background: #2ecc71;
            color: white;
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 12px;
            margin-left: 10px;
        }
    </style>
</head>
<body>
    <h1>🌐 訪客追蹤網站 <span class="auto-badge">自動記錄</span></h1>
    <p class="subtitle">每次訪問自動記錄 IP，無需任何操作</p>
    
    <div class="your-ip">
        <h2>📍 你的 IP 地址</h2>
        <div class="ip" id="yourIP">載入中...</div>
        <div class="time" id="visitTime"></div>
    </div>
    
    <div class="status loading" id="status">
        🔄 正在自動記錄您的訪問...
    </div>
    
    <div class="summary">
        <div class="summary-card">
            <h4>總訪問次數</h4>
            <div class="number" id="totalVisits">-</div>
        </div>
        <div class="summary-card">
            <h4>獨立 IP 數量</h4>
            <div class="number" id="uniqueIPs">-</div>
        </div>
        <div class="summary-card">
            <h4>最後訪問時間</h4>
            <div class="number" id="lastVisit" style="font-size: 16px;">-</div>
        </div>
    </div>
    
    <div class="records">
        <h3>📊 訪問記錄（最近 50 筆）</h3>
        <button class="refresh-btn" onclick="loadRecords()">🔄 刷新記錄</button>
        <table id="recordsTable">
            <thead>
                <tr>
                    <th>#</th>
                    <th>IP 地址</th>
                    <th>訪問時間</th>
                    <th>瀏覽器</th>
                </tr>
            </thead>
            <tbody></tbody>
        </table>
    </div>
    
    <script>
        // 頁面載入時自動記錄訪客
        function autoRecordVisit() {
            fetch('/api/visit', { method: 'POST' })
                .then(r => r.json())
                .then(data => {
                    document.getElementById('yourIP').textContent = data.ip;
                    document.getElementById('visitTime').textContent = '訪問時間: ' + data.timestamp;
                    document.getElementById('status').className = 'status success';
                    document.getElementById('status').textContent = '✅ 已自動記錄您的訪問！';
                    
                    // 更新統計
                    document.getElementById('totalVisits').textContent = data.total_visits;
                    loadRecords();
                    loadSummary();
                })
                .catch(err => {
                    document.getElementById('status').className = 'status';
                    document.getElementById('status').style.background = 'rgba(231,76,60,0.2)';
                    document.getElementById('status').textContent = '❌ 記錄失敗: ' + err.message;
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
                            <td class="ua-text">${r.user_agent}</td>
                        </tr>
                    `).join('');
                });
        }
        
        function loadSummary() {
            fetch('/api/summary')
                .then(r => r.json())
                .then(data => {
                    document.getElementById('totalVisits').textContent = data.total_visits;
                    document.getElementById('uniqueIPs').textContent = data.unique_ips;
                    document.getElementById('lastVisit').textContent = data.last_visit || '無記錄';
                });
        }
        
        // 🎯 頁面載入時自動執行
        autoRecordVisit();
    </script>
</body>
</html>
'''

def init_db():
    """初始化資料庫"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS visits (
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

class VisitorTrackerHandler(http.server.BaseHTTPRequestHandler):
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
            c.execute('SELECT * FROM visits ORDER BY id DESC LIMIT 50')
            rows = c.fetchall()
            conn.close()
            
            records = []
            for row in rows:
                ua = row['user_agent'] or ''
                records.append({
                    'id': row['id'],
                    'ip': row['ip'],
                    'time': row['timestamp'],
                    'user_agent': ua[:40] + '...' if len(ua) > 40 else ua
                })
            
            self.send_json({'records': records})
            
        elif parsed_path.path == '/api/summary':
            # 獲取統計
            conn = get_db()
            c = conn.cursor()
            c.execute('SELECT COUNT(*) FROM visits')
            total_visits = c.fetchone()[0]
            c.execute('SELECT COUNT(DISTINCT ip) FROM visits')
            unique_ips = c.fetchone()[0]
            c.execute('SELECT timestamp FROM visits ORDER BY id DESC LIMIT 1')
            row = c.fetchone()
            last_visit = row[0] if row else None
            conn.close()
            
            self.send_json({
                'total_visits': total_visits,
                'unique_ips': unique_ips,
                'last_visit': last_visit
            })
            
        elif parsed_path.path.startswith('/api/ip/'):
            # 查詢特定 IP
            ip_address = parsed_path.path[8:]
            conn = get_db()
            c = conn.cursor()
            c.execute('SELECT * FROM visits WHERE ip = ? ORDER BY id DESC', (ip_address,))
            rows = c.fetchall()
            conn.close()
            
            records = [{'id': r['id'], 'ip': r['ip'], 'time': r['timestamp'], 'user_agent': r['user_agent']} for r in rows]
            self.send_json({'ip': ip_address, 'count': len(records), 'records': records})
        else:
            self.send_error(404, 'Not Found')
    
    def do_POST(self):
        """處理 POST 請求"""
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/api/visit':
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
                'INSERT INTO visits (ip, timestamp, user_agent, referer) VALUES (?, ?, ?, ?)',
                (ip, timestamp, user_agent, referer)
            )
            conn.commit()
            c.execute('SELECT COUNT(*) FROM visits')
            total_visits = c.fetchone()[0]
            conn.close()
            
            self.send_json({
                'success': True,
                'ip': ip,
                'timestamp': timestamp,
                'total_visits': total_visits
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
║ 🌐 訪客追蹤網站已啟動（自動記錄版）                        ║
╠════════════════════════════════════════════════════════════╣
║ 📍 本地訪問：http://localhost:{PORT}                        ║
║ 🌍 外部訪問：http://<你的IP>:{PORT}                        ║
║                                                            ║
║ ✨ 特點：頁面載入時自動記錄 IP，無需點擊                   ║
║                                                            ║
║ 📊 API 端點：                                              ║
║    GET  /              首頁                                ║
║    POST /api/visit     自動記錄訪客                        ║
║    GET  /api/records   獲取最近 50 筆記錄                  ║
║    GET  /api/summary   獲取統計摘要                        ║
║    GET  /api/ip/<ip>   查詢特定 IP 的所有記錄              ║
║                                                            ║
║ 🛑 按 Ctrl+C 停止伺服器                                    ║
╚════════════════════════════════════════════════════════════╝
''')
    with socketserver.TCPServer(("", PORT), VisitorTrackerHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n👋 伺服器已停止")

if __name__ == '__main__':
    main()
