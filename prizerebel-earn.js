const { chromium } = require('playwright');
const fs = require('fs');

(async () => {
  console.log('🚀 啟動 PrizeRebel 賺錢腳本...');
  
  const browser = await chromium.launch({ 
    headless: false,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });
  
  const context = await browser.newContext({
    viewport: { width: 1280, height: 800 }
  });
  
  const page = await context.newPage();

  try {
    // 步驟 1: 登入 PrizeRebel
    console.log('📧 步驟 1: 登入 PrizeRebel...');
    await page.goto('https://www.prizerebel.com/login.php', { waitUntil: 'networkidle' });
    
    await page.fill('input[name="email"]', 'hongkpng856@gmail.com');
    await page.fill('input[name="password"]', 'mtsd479j');
    await page.click('input[type="submit"]');
    
    await page.waitForNavigation({ waitUntil: 'networkidle' });
    console.log('✅ 登入成功！');
    
    await page.screenshot({ path: '/home/claw/.openclaw/workspace/step1-login.png' });

    // 步驟 2: 查看 Dashboard
    console.log('📊 步驟 2: 查看 Dashboard...');
    await page.goto('https://www.prizerebel.com/member/dashboard.php', { waitUntil: 'networkidle' });
    
    // 獲取目前積分
    const pointsElement = await page.$('.points-display, .user-points, [class*="points"]');
    let currentPoints = '未知';
    if (pointsElement) {
      currentPoints = await pointsElement.textContent();
    }
    console.log(`💰 目前積分: ${currentPoints}`);
    
    await page.screenshot({ path: '/home/claw/.openclaw/workspace/step2-dashboard.png', fullPage: true });

    // 步驟 3: 進入 Earn 頁面
    console.log('🎯 步驟 3: 進入 Earn 頁面...');
    await page.goto('https://www.prizerebel.com/earn.php', { waitUntil: 'networkidle' });
    await page.screenshot({ path: '/home/claw/.openclaw/workspace/step3-earn.png', fullPage: true });

    // 步驟 4: 查看 Video Ads
    console.log('📺 步驟 4: 查看 Video Ads...');
    await page.goto('https://www.prizerebel.com/videos.php', { waitUntil: 'networkidle' });
    await page.screenshot({ path: '/home/claw/.openclaw/workspace/step4-videos.png', fullPage: true });
    
    // 查找影片連結
    const videoLinks = await page.$$('a');
    console.log(`找到 ${videoLinks.length} 個連結`);
    
    // 嘗試獲取頁面內容
    const pageContent = await page.content();
    console.log('頁面 HTML 長度:', pageContent.length);

    // 步驟 5: 查看 Cash Offers
    console.log('💎 步驟 5: 查看 Cash Offers...');
    await page.goto('https://www.prizerebel.com/offers.php', { waitUntil: 'networkidle' });
    await page.screenshot({ path: '/home/claw/.openclaw/workspace/step5-offers.png', fullPage: true });

    // 步驟 6: 查看 Offer Walls
    console.log('🏢 步驟 6: 查看 Offer Walls...');
    await page.goto('https://www.prizerebel.com/offerwalls.php', { waitUntil: 'networkidle' });
    await page.screenshot({ path: '/home/claw/.openclaw/workspace/step6-offerwalls.png', fullPage: true });

    // 寫入進度報告
    const report = {
      timestamp: new Date().toISOString(),
      status: 'completed',
      steps: [
        { step: 1, name: 'login', status: 'success' },
        { step: 2, name: 'dashboard', status: 'success' },
        { step: 3, name: 'earn', status: 'success' },
        { step: 4, name: 'videos', status: 'success' },
        { step: 5, name: 'offers', status: 'success' },
        { step: 6, name: 'offerwalls', status: 'success' }
      ],
      screenshots: [
        'step1-login.png',
        'step2-dashboard.png',
        'step3-earn.png',
        'step4-videos.png',
        'step5-offers.png',
        'step6-offerwalls.png'
      ]
    };
    
    fs.writeFileSync('/home/claw/.openclaw/workspace/earn-progress.json', JSON.stringify(report, null, 2));
    console.log('✅ 進度報告已保存');

    // 保持瀏規器開啟 30 秒
    console.log('⏳ 等待 30 秒以便觀察...');
    await page.waitForTimeout(30000);

  } catch (error) {
    console.error('❌ 錯誤:', error.message);
    await page.screenshot({ path: '/home/claw/.openclaw/workspace/error-screenshot.png' });
    
    const errorReport = {
      timestamp: new Date().toISOString(),
      status: 'error',
      error: error.message
    };
    fs.writeFileSync('/home/claw/.openclaw/workspace/earn-progress.json', JSON.stringify(errorReport, null, 2));
  } finally {
    await browser.close();
    console.log('🔚 瀏規器已關閉');
  }
})();
