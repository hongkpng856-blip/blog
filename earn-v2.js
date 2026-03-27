const { chromium } = require('playwright');
const fs = require('fs');

(async () => {
  console.log('🚀 啟動賺錢自動化...');
  const browser = await chromium.launch({ headless: false, slowMo: 500 });
  const context = await browser.newContext({
    viewport: { width: 1280, height: 800 }
  });
  const page = await context.newPage();

  // 記錄進度
  let progress = {
    startTime: new Date().toISOString(),
    tasks: [],
    points: 0
  };

  try {
    // 登入 PrizeRebel
    console.log('📧 登入 PrizeRebel...');
    await page.goto('https://www.prizerebel.com/login.php', { waitUntil: 'networkidle' });
    await page.fill('input[name="email"]', 'hongkpng856@gmail.com');
    await page.fill('input[name="password"]', 'mtsd479j');
    await page.click('input[type="submit"]');
    await page.waitForNavigation({ waitUntil: 'networkidle' });
    console.log('✅ 登入成功！');
    progress.tasks.push({ action: 'login', status: 'success' });

    // 進入 Dashboard
    await page.goto('https://www.prizerebel.com/member/dashboard.php', { waitUntil: 'networkidle' });
    await page.screenshot({ path: '/home/claw/.openclaw/workspace/progress-01-dashboard.png' });

    // 檢查當前積分
    const pointsElement = await page.$('.points-display, .user-points, [class*="points"]');
    if (pointsElement) {
      const pointsText = await pointsElement.textContent();
      console.log(`💰 當前積分: ${pointsText}`);
      progress.currentPoints = pointsText;
    }

    // 嘗試進入 Earn 頁面
    console.log('📊 進入 Earn 頁面...');
    await page.goto('https://www.prizerebel.com/earn.php', { waitUntil: 'networkidle' });
    await page.screenshot({ path: '/home/claw/.openclaw/workspace/progress-02-earn.png' });

    // 檢查可用任務
    console.log('🔍 檢查可用任務...');
    
    // 嘗試找到任何可點擊的任務連結
    const taskLinks = await page.$$('a[href*="offer"], a[href*="survey"], a[href*="video"]');
    console.log(`找到 ${taskLinks.length} 個可能的任務連結`);

    // 嘗試點擊 Cash Offers
    const cashOffersLink = await page.$('text=Cash Offers');
    if (cashOffersLink) {
      console.log('點擊 Cash Offers...');
      await cashOffersLink.click();
      await page.waitForLoadState('networkidle');
      await page.screenshot({ path: '/home/claw/.openclaw/workspace/progress-03-cash-offers.png' });
      progress.tasks.push({ action: 'click_cash_offers', status: 'success' });
    }

    // 嘗試點擊 Video Ads
    const videoAdsLink = await page.$('text=Video');
    if (videoAdsLink) {
      console.log('點擊 Video Ads...');
      await videoAdsLink.click();
      await page.waitForLoadState('networkidle');
      await page.screenshot({ path: '/home/claw/.openclaw/workspace/progress-04-video-ads.png' });
      progress.tasks.push({ action: 'click_video_ads', status: 'success' });
    }

    // 保存進度報告
    progress.endTime = new Date().toISOString();
    fs.writeFileSync('/home/claw/.openclaw/workspace/earn-progress.json', JSON.stringify(progress, null, 2));
    console.log('📊 進度報告已保存');

    // 等待觀察
    console.log('等待 20 秒...');
    await page.waitForTimeout(20000);

  } catch (error) {
    console.error('❌ 錯誤:', error.message);
    await page.screenshot({ path: '/home/claw/.openclaw/workspace/progress-error.png' });
    progress.error = error.message;
    fs.writeFileSync('/home/claw/.openclaw/workspace/earn-progress.json', JSON.stringify(progress, null, 2));
  } finally {
    await browser.close();
    console.log('🔚 完成！');
  }
})();
