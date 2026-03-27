const https = require('https');

const platforms = [
  { name: 'SproutGigs', url: 'https://sproutgigs.com' },
  { name: 'Picoworkers', url: 'https://picoworkers.com' },
  { name: 'RapidWorkers', url: 'https://rapidworkers.com' }
];

async function checkPlatform(platform) {
  return new Promise((resolve) => {
    const url = new URL(platform.url);
    const req = https.request({
      hostname: url.hostname,
      path: '/',
      method: 'GET',
      timeout: 10000
    }, (res) => {
      resolve({ ...platform, status: res.statusCode, accessible: res.statusCode < 400 });
    });
    req.on('error', (e) => {
      resolve({ ...platform, status: 'ERROR', accessible: false, error: e.message });
    });
    req.on('timeout', () => {
      req.destroy();
      resolve({ ...platform, status: 'TIMEOUT', accessible: false });
    });
    req.end();
  });
}

(async () => {
  console.log('🔍 檢查備選平台可用性...\n');
  for (const p of platforms) {
    const result = await checkPlatform(p);
    console.log(`${result.accessible ? '✅' : '❌'} ${result.name}: ${result.status}`);
  }
  console.log('\n建議：優先嘗試 SproutGigs（前 Picoworkers，較成熟）');
})();
