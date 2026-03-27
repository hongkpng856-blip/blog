#!/usr/bin/env python3
"""
模擬網站 — 用於測試人性化點擊 BOT
功能：
1. 記錄每次訪問
2. 檢測 BOT 行為
3. 即時顯示結果
4. 提供視覺化介面
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import time
from datetime import datetime
from collections import defaultdict
import threading
import os

# 儲存訪問記錄
visit_records = []
bot_detection_stats = {
    "total_visits": 0,
    "suspicious_visits": 0,
    "human_like_visits": 0,
    "avg_interval": 0,
    "intervals": []
}

class MockWebsiteHandler(BaseHTTPRequestHandler):
    """模擬網站處理器"""
    
    def log_message(self, format, *args):
        """禁用預設日誌"""
        pass
    
    def do_GET(self):
        """處理 GET 請求"""
        
        # 記錄訪問時間
        visit_time = datetime.now()
        timestamp = visit_time.timestamp()
        
        # 解析請求
        headers = dict(self.headers)
        user_agent = headers.get('User-Agent', 'Unknown')
        
        # 記錄到全局
        visit_record = {
            "id": len(visit_records) + 1,
            "timestamp": visit_time.isoformat(),
            "path": self.path,
            "user_agent": user_agent,
            "headers": {
                "Accept": headers.get('Accept', ''),
                "Accept-Language": headers.get('Accept-Language', ''),
                "Accept-Encoding": headers.get('Accept-Encoding', ''),
                "Sec-Fetch-Site": headers.get('Sec-Fetch-Site', ''),
            }
        }
        
        # 計算間隔
        if len(visit_records) > 0:
            last_visit = visit_records[-1]["timestamp"]
            last_timestamp = datetime.fromisoformat(last_visit).timestamp()
            interval = timestamp - last_timestamp
            visit_record["interval_seconds"] = round(interval, 2)
            visit_record["interval_minutes"] = round(interval / 60, 2)
            bot_detection_stats["intervals"].append(interval)
        else:
            visit_record["interval_seconds"] = 0
            visit_record["interval_minutes"] = 0
        
        visit_records.append(visit_record)
        bot_detection_stats["total_visits"] = len(visit_records)
        
        # 根據路徑返回不同內容
        if self.path == '/':
            self.send_homepage()
        elif self.path == '/stats':
            self.send_stats()
        elif self.path == '/api/visits':
            self.send_api_visits()
        elif self.path == '/api/detection':
            self.send_api_detection()
        elif self.path == '/clear':
            self.clear_records()
        else:
            self.send_404()
    
    def send_homepage(self):
        """發送首頁"""
        html = '''<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🧪 BOT 測試網站</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', sans-serif; 
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            color: #eee;
            min-height: 100vh;
            padding: 20px;
        }
        .container { max-width: 1200px; margin: 0 auto; }
        h1 { 
            text-align: center; 
            margin-bottom: 30px;
            font-size: 2.5em;
            background: linear-gradient(90deg, #00f5a0, #00d9f5);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .stats-grid { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .stat-card {
            background: rgba(255,255,255,0.1);
            padding: 20px;
            border-radius: 15px;
            text-align: center;
        }
        .stat-value {
            font-size: 2.5em;
            font-weight: bold;
            color: #00f5a0;
        }
        .stat-label {
            color: #888;
            margin-top: 5px;
        }
        .detection-box {
            background: rgba(255,255,255,0.05);
            padding: 20px;
            border-radius: 15px;
            margin-bottom: 30px;
        }
        .detection-title {
            font-size: 1.5em;
            margin-bottom: 15px;
            color: #00d9f5;
        }
        .progress-bar {
            height: 30px;
            background: #333;
            border-radius: 15px;
            overflow: hidden;
            margin: 10px 0;
        }
        .progress-fill {
            height: 100%;
            transition: width 0.5s;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
        }
        .human-like { background: linear-gradient(90deg, #00f5a0, #00d9f5); }
        .suspicious { background: linear-gradient(90deg, #f55, #f90); }
        .visits-table {
            width: 100%;
            border-collapse: collapse;
            background: rgba(255,255,255,0.05);
            border-radius: 15px;
            overflow: hidden;
        }
        .visits-table th, .visits-table td {
            padding: 15px;
            text-align: left;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }
        .visits-table th {
            background: rgba(0,245,160,0.2);
        }
        .visits-table tr:hover {
            background: rgba(255,255,255,0.1);
        }
        .interval-good { color: #00f5a0; }
        .interval-warning { color: #f90; }
        .interval-bad { color: #f55; }
        .refresh-btn {
            background: linear-gradient(90deg, #00f5a0, #00d9f5);
            border: none;
            padding: 15px 30px;
            border-radius: 25px;
            color: #1a1a2e;
            font-size: 1.1em;
            font-weight: bold;
            cursor: pointer;
            margin: 20px 5px;
        }
        .refresh-btn:hover { opacity: 0.9; }
        .clear-btn {
            background: linear-gradient(90deg, #f55, #f90);
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🧪 BOT 測試網站</h1>
        
        <div class="stats-grid" id="statsGrid">
            <!-- 動態載入 -->
        </div>
        
        <div class="detection-box">
            <div class="detection-title">🔍 BOT 檢測結果</div>
            <div id="detectionResult">
                <!-- 動態載入 -->
            </div>
        </div>
        
        <div style="text-align: center;">
            <button class="refresh-btn" onclick="loadStats()">🔄 重新整理</button>
            <button class="refresh-btn clear-btn" onclick="clearRecords()">🗑️ 清除記錄</button>
        </div>
        
        <h2 style="margin: 30px 0 15px; color: #00d9f5;">📋 訪問記錄</h2>
        <div style="overflow-x: auto;">
            <table class="visits-table" id="visitsTable">
                <!-- 動態載入 -->
            </table>
        </div>
    </div>
    
    <script>
        function loadStats() {
            fetch('/api/detection')
                .then(r => r.json())
                .then(data => {
                    updateStats(data);
                    updateDetection(data);
                });
            
            fetch('/api/visits')
                .then(r => r.json())
                .then(data => {
                    updateVisitsTable(data);
                });
        }
        
        function updateStats(data) {
            const grid = document.getElementById('statsGrid');
            grid.innerHTML = `
                <div class="stat-card">
                    <div class="stat-value">${data.total_visits}</div>
                    <div class="stat-label">總訪問次數</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">${data.human_like_visits}</div>
                    <div class="stat-label">人性化訪問</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">${data.suspicious_visits}</div>
                    <div class="stat-label">可疑訪問</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">${data.avg_interval_minutes}</div>
                    <div class="stat-label">平均間隔（分鐘）</div>
                </div>
            `;
        }
        
        function updateDetection(data) {
            const result = document.getElementById('detectionResult');
            const humanPercent = data.total_visits > 0 
                ? (data.human_like_visits / data.total_visits * 100).toFixed(1)
                : 0;
            const botPercent = data.total_visits > 0 
                ? (data.suspicious_visits / data.total_visits * 100).toFixed(1)
                : 0;
            
            result.innerHTML = `
                <p style="margin-bottom: 10px;">人性化行為比例：</p>
                <div class="progress-bar">
                    <div class="progress-fill human-like" style="width: ${humanPercent}%">
                        ${humanPercent}%
                    </div>
                </div>
                
                <p style="margin: 20px 0 10px;">可疑 BOT 行為比例：</p>
                <div class="progress-bar">
                    <div class="progress-fill suspicious" style="width: ${botPercent}%">
                        ${botPercent}%
                    </div>
                </div>
                
                <div style="margin-top: 20px; padding: 15px; background: rgba(0,0,0,0.3); border-radius: 10px;">
                    <strong>📊 分析：</strong>
                    <span id="analysis">${data.analysis}</span>
                </div>
            `;
        }
        
        function updateVisitsTable(visits) {
            const table = document.getElementById('visitsTable');
            if (visits.length === 0) {
                table.innerHTML = '<tr><td colspan="5" style="text-align:center;padding:50px;">尚無訪問記錄</td></tr>';
                return;
            }
            
            let html = `
                <tr>
                    <th>#</th>
                    <th>時間</th>
                    <th>間隔</th>
                    <th>User-Agent</th>
                    <th>狀態</th>
                </tr>
            `;
            
            visits.slice(-20).reverse().forEach(v => {
                const intervalClass = v.interval_seconds > 60 ? 'interval-good' 
                    : v.interval_seconds > 10 ? 'interval-warning' 
                    : 'interval-bad';
                
                const statusIcon = v.interval_seconds > 60 ? '✅ 人性化'
                    : v.interval_seconds > 10 ? '⚠️ 可能'
                    : '❌ BOT';
                
                html += `
                    <tr>
                        <td>${v.id}</td>
                        <td>${new Date(v.timestamp).toLocaleTimeString()}</td>
                        <td class="${intervalClass}">${v.interval_minutes.toFixed(2)} 分</td>
                        <td style="font-size:0.8em">${v.user_agent.substring(0,50)}...</td>
                        <td>${statusIcon}</td>
                    </tr>
                `;
            });
            
            table.innerHTML = html;
        }
        
        function clearRecords() {
            if (confirm('確定要清除所有記錄？')) {
                fetch('/clear')
                    .then(() => loadStats());
            }
        }
        
        // 初始載入
        loadStats();
        
        // 每 5 秒自動更新
        setInterval(loadStats, 5000);
    </script>
</body>
</html>'''
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode())
    
    def send_stats(self):
        """發送統計頁"""
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(bot_detection_stats, indent=2).encode())
    
    def send_api_visits(self):
        """API：返回訪問記錄"""
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(visit_records, indent=2).encode())
    
    def send_api_detection(self):
        """API：返回檢測結果"""
        # 計算統計
        intervals = bot_detection_stats["intervals"]
        
        # 分析間隔
        if len(intervals) > 1:
            avg_interval = sum(intervals) / len(intervals)
            bot_detection_stats["avg_interval"] = round(avg_interval, 2)
            bot_detection_stats["avg_interval_minutes"] = round(avg_interval / 60, 2)
            
            # 檢測 BOT 行為（間隔 < 10 秒）
            suspicious = sum(1 for i in intervals if i < 10)
            human_like = sum(1 for i in intervals if i > 60)
            
            bot_detection_stats["suspicious_visits"] = suspicious
            bot_detection_stats["human_like_visits"] = human_like
        
        # 生成分析報告
        total = bot_detection_stats["total_visits"]
        if total == 0:
            analysis = "尚無數據"
        elif total < 5:
            analysis = "數據不足，請繼續測試"
        else:
            human_rate = bot_detection_stats["human_like_visits"] / total * 100
            if human_rate > 80:
                analysis = "🟢 非常像真實人類！BOT 難以被檢測"
            elif human_rate > 50:
                analysis = "🟡 部分像人類，部分可疑"
            else:
                analysis = "🔴 高度可疑，容易被檢測為 BOT"
        
        result = {
            "total_visits": bot_detection_stats["total_visits"],
            "suspicious_visits": bot_detection_stats["suspicious_visits"],
            "human_like_visits": bot_detection_stats["human_like_visits"],
            "avg_interval_seconds": bot_detection_stats.get("avg_interval", 0),
            "avg_interval_minutes": bot_detection_stats.get("avg_interval_minutes", 0),
            "analysis": analysis
        }
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(result, indent=2).encode())
    
    def clear_records(self):
        """清除記錄"""
        global visit_records, bot_detection_stats
        visit_records = []
        bot_detection_stats = {
            "total_visits": 0,
            "suspicious_visits": 0,
            "human_like_visits": 0,
            "avg_interval": 0,
            "intervals": []
        }
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'<script>window.location="/";</script>')
    
    def send_404(self):
        """發送 404"""
        self.send_response(404)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'<h1>404 Not Found</h1>')


def run_server(port=8888):
    """啟動模擬網站"""
    server = HTTPServer(('0.0.0.0', port), MockWebsiteHandler)
    print("=" * 60)
    print("🌐 模擬網站已啟動")
    print("=" * 60)
    print(f"\n📍 網址: http://localhost:{port}")
    print(f"📍 外部: http://<你的IP>:{port}")
    print("\n📋 功能:")
    print("  - 記錄每次訪問")
    print("  - 檢測 BOT 行為")
    print("  - 即時顯示結果")
    print("\n🛑 按 Ctrl+C 停止")
    print("-" * 60)
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\n👋 網站已停止")
        server.shutdown()


if __name__ == "__main__":
    run_server()
