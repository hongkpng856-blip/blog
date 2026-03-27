const { chromium } = require('playwright');
const fs = require('fs');

(async () => {
  console.log('🚀 啟動 PrizeRebel 點數檢查...');
  
  const browser = await chromium.launch({
    headless: false,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });
  
  const context = await browser.newContext({
    viewport: { width: 1280, height: 900 }
  });
  
  const page = await context.newPage();
  
  try {
    // 步驟 1: 登入 PrizeRebel
    console.log('📧 步驟 1: 登入 PrizeRebel...');
    await page.goto('https://www.prizerebel.com/login.php', { waitUntil: 'networkidle' });
    
    // 等待並填寫登入表單
    await page.waitForSelector('input[name="email"]', { timeout: 10000 });
    await page.fill('input[name="email"]', 'hongkpng856@gmail.com');
    await page.fill('input[name="password"]', 'mtsd479j');
    
    // 點擊登入
    await page.click('input[type="submit"]');
    
    // 等待導航完成
    await page.waitForNavigation({ waitUntil: 'networkidle', timeout: 30000 });
    console.log('✅ 登入成功！');
    
    // 步驟 2: 查看 Dashboard
    console.log('📊 步驟 2: 查看 Dashboard...');
    await page.goto('https://www.prizerebel.com/member/dashboard.php', { waitUntil: 'networkidle' });
    
    // 截圖保存
    await page.screenshot({ path: '/home/claw/.openclaw/workspace/pr-dashboard-current.png', fullPage: true });
    
    // 嘗試多種選擇器獲取點數
    let points = '未知';
    const selectors = [
      '.points-display',
      '.user-points',
      '[class*="points"]',
      '.balance',
      '.credit',
      'span.points',
      'div.points',
      '.header-points',
      '.sidebar-points'
    ];
    
    for (const selector of selectors) {
      try {
        const element = await page.$(selector);
        if (element) {
          const text = await element.textContent();
          if (text && text.match(/\d+/)) {
            points = text.trim();
            console.log(`💰 找到點數 (${selector}): ${points}`);
            break;
          }
        }
      } catch (e) {}
    }
    
    // 如果還是找不到，嘗試從整個頁面內容中提取
    if (points === '未知') {
      const pageContent = await page.content();
      const pointsMatch = pageContent.match(/(\d+)\s*(?:points?|pts?)/i);
      if (pointsMatch) {
        points = pointsMatch[1];
        console.log(`💰 從頁面提取點數: ${points}`);
      }
    }
    
    console.log(`📊 目前點數: ${points}`);
    
    // 步驟 3: 查看 Earn 頁面的可用任務
    console.log('🎯 步驟 3: 查看 Earn 頁面...');
    await page.goto('https://www.prizerebel.com/earn.php', { waitUntil: 'networkidle' });
    await page.screenshot({ path: '/home/claw/.openclaw/workspace/pr-earn-current.png', fullPage: true });
    
    // 步驟 4: 查看 Daily Survey
    console.log('📋 步驟 4: 查看 Daily Survey...');
    await page.goto('https://www.prizerebel.com/surveys.php', { waitUntil: 'networkidle' });
    await page.screenshot({ path: '/home/claw/.openclaw/workspace/pr-surveys-current.png', fullPage: true });
    
    // 寫入狀態報告
    const report = {
      timestamp: new Date().toISOString(),
      points: points,
      screenshots: [
        'pr-dashboard-current.png',
        'pr-earn-current.png',
        'pr-surveys-current.png'
      ]
    };
    
    fs.writeFileSync('/home/claw/.openclaw/workspace/prizerebel-status.json', JSON.stringify(report, null, 2));
    console.log('✅ 狀態報告已保存');
    
    // 保持瀏覽器開啟 10 秒
    console.log('⏳ 等待 10 秒...');
    await page.waitForTimeout(10000);
    
  } catch (error) {
    console.error('❌ 錯誤:', error.message);
    await page.screenshot({ path: '/home/claw/.openclaw/workspace/pr-error.png' });
  } finally {
    await browser.close();
    console.log('🔚 完成');
  }
})();
