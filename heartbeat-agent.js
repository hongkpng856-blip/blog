#!/usr/bin/env node

const http = require('http');

const MAIN_SESSION_KEY = 'agent:main:telegram:direct:5396608205';
const HEARTBEAT_INTERVAL = 5 * 60 * 1000; // 5 minutes
const OPENCLAW_HOST = 'localhost';
const OPENCLAW_PORT = 42069;

function sendHeartbeat() {
  return new Promise((resolve) => {
    const postData = JSON.stringify({
      sessionKey: MAIN_SESSION_KEY,
      message: '🫀 HEARTBEAT - 請匯報目前進度'
    });

    const options = {
      hostname: OPENCLAW_HOST,
      port: OPENCLAW_PORT,
      path: '/api/sessions/send',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(postData)
      }
    };

    const req = http.request(options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        console.log(`[${new Date().toISOString()}] Heartbeat sent - Status: ${res.statusCode}`);
        resolve(res.statusCode === 200);
      });
    });

    req.on('error', (e) => {
      console.error(`[${new Date().toISOString()}] Error: ${e.message}`);
      resolve(false);
    });

    req.setTimeout(10000, () => {
      console.error(`[${new Date().toISOString()}] Request timeout`);
      req.destroy();
      resolve(false);
    });

    req.write(postData);
    req.end();
  });
}

async function main() {
  console.log('🚀 Heartbeat Agent 啟動');
  console.log(`📅 頻率: 每 ${HEARTBEAT_INTERVAL / 1000 / 60} 分鐘`);
  console.log(`🎯 目標: ${MAIN_SESSION_KEY}`);
  console.log('───');

  // Send immediately on start
  await sendHeartbeat();

  // Then every 5 minutes
  setInterval(async () => {
    await sendHeartbeat();
  }, HEARTBEAT_INTERVAL);
}

main().catch(console.error);