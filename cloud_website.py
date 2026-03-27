#!/usr/bin/env python3
"""
雲端部署版模擬網站
支援：PythonAnywhere、Render、Railway
"""

from flask import Flask, jsonify
from flask_cors import CORS
import json
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

# 儲存訪問記錄
visit_records = []

@app.route('/')
def home():
    """首頁"""
    html = '''<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🧪 BOT 測試網站（雲端版）</title>
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
        .interval-good { color: #00f5a0; }
        .interval-warning { color: #f90; }
        .interval-bad { color: #f55; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🧪 BOT 測試網站（雲端版）</h1>
        
        <div class="stats-grid" id="statsGrid"></div>
        
        <div style="text-align: center;">
            <button class="refresh-btn" onclick="loadStats()">🔄 重新整理</button>
            <button class="refresh-btn" onclick="clearRecords()">🗑️ 清除記錄</button>
        </div>
        
        <h2 style="margin: 30px 0 15px; color: #00d9f5;">📋 訪問記錄</h2>
        <div style="overflow-x: auto;">
            <table class="visits-table" id="visitsTable"></table>
        </div>
    </div>
    
    <script>
        function loadStats() {
            fetch('/api/stats')
                .then(r => r.json())
                .then(data => {
                    document.getElementById('statsGrid').innerHTML = `
                        <div class="stat-card">
                            <div class="stat-value">${data.total_visits}</div>
                            <div class="stat-label">總訪問次數</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-value">${data.human_like}</div>
                            <div class="stat-label">人性化訪問</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-value">${data.suspicious}</div>
                            <div class="stat-label">可疑訪問</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-value">${data.avg_interval}</div>
                            <div class="stat-label">平均間隔（秒）</div>
                        </div>
                    `;
                });
            
            fetch('/api/visits')
                .then(r => r.json())
                .then(visits => {
                    let html = '<tr><th>#</th><th>時間</th><th>間隔</th><th>狀態</th></tr>';
                    if (visits.length === 0) {
                        html = '<tr><td colspan="4" style="text-align:center;padding:50px;">尚無訪問記錄</td></tr>';
                    } else {
                        visits.slice(-20).reverse().forEach(v => {
                            const cls = v.interval > 60 ? 'interval-good' : v.interval > 10 ? 'interval-warning' : 'interval-bad';
                            const status = v.interval > 60 ? '✅ 人性化' : v.interval > 10 ? '⚠️ 可能' : '❌ BOT';
                            html += `<tr>
                                <td>${v.id}</td>
                                <td>${v.time}</td>
                                <td class="${cls}">${v.interval}s</td>
                                <td>${status}</td>
                            </tr>`;
                        });
                    }
                    document.getElementById('visitsTable').innerHTML = html;
                });
        }
        
        function clearRecords() {
            if (confirm('確定要清除？')) {
                fetch('/clear').then(() => loadStats());
            }
        }
        
        loadStats();
        setInterval(loadStats, 5000);
    </script>
</body>
</html>'''
    return html

@app.route('/api/stats')
def stats():
    """統計 API"""
    total = len(visit_records)
    intervals = [v['interval'] for v in visit_records if v['interval'] > 0]
    
    return jsonify({
        'total_visits': total,
        'human_like': sum(1 for i in intervals if i > 60),
        'suspicious': sum(1 for i in intervals if i < 10),
        'avg_interval': round(sum(intervals) / len(intervals), 2) if intervals else 0
    })

@app.route('/api/visits')
def visits():
    """訪問記錄 API"""
    return jsonify(visit_records)

@app.route('/clear')
def clear():
    """清除記錄"""
    global visit_records
    visit_records = []
    return jsonify({'status': 'cleared'})

@app.route('/track')
def track():
    """追蹤訪問"""
    visit_time = datetime.now()
    
    # 計算間隔
    interval = 0
    if len(visit_records) > 0:
        last = visit_records[-1]['timestamp']
        interval = (visit_time - datetime.fromisoformat(last)).total_seconds()
    
    record = {
        'id': len(visit_records) + 1,
        'timestamp': visit_time.isoformat(),
        'time': visit_time.strftime('%H:%M:%S'),
        'interval': round(interval, 2)
    }
    
    visit_records.append(record)
    return jsonify(record)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8888))
    app.run(host='0.0.0.0', port=port)
