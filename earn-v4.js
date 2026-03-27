const { chromium } = require('playwright');
const fs = require('fs');

(async () => {
  console.log('🎯 嘗試完成 PrizeRebel 問卷...');
  const browser = await chromium.launch({ 
    headless: false, 
    slowMo: 2000,  // 放慢操作以便觀察
    args: ['--start-maximized']
  });
  const context = await browser.newContext({
    viewport: { width: 1400, height: 900 }
  });
  const page = await context.newPage();

  try {
    // 登入
    console.log('📧 登入...');
    await page.goto('https://www.prizerebel.com/login.php');
    await page.waitForLoadState('networkidle');
    await page.fill('input[name="email"]', 'hongkpng856@gmail.com');
    await page.fill('input[name="password"]', 'mtsd479j');
    await page.click('input[type="submit"]');
    await page.waitForNavigation({ waitUntil: 'networkidle' });
    console.log('✅ 登入成功');

    // 進入 offers 頁面
    console.log('📊 進入 offers 頁面...');
    await page.goto('https://www.prizerebel.com/offers.php');
    await page.waitForLoadState('networkidle');
    await page.screenshot({ path: '/home/claw/.openclaw/workspace/v4-01-offers.png' });

    // 等待頁面完全載入
    await page.waitForTimeout(3000);

    // 嘗試找到 "Complete your profile" 連結
    console.log('🔍 尋找問卷連結...');
    
    // 方法 1: 使用 text 選擇器
    const profileLink = await page.$('text="Complete your profile"');
    if (profileLink) {
      console.log('找到 "Complete your profile" 連結');
      
      // 獲取連結的 href
      const href = await profileLink.getAttribute('href');
      console.log(`連結目標: ${href}`);
      
      // 點擊連結
      await profileLink.click();
      await page.waitForTimeout(5000);
      await page.screenshot({ path: '/home/claw/.openclaw/workspace/v4-02-after-click.png' });
      
      // 檢查是否跳轉到新頁面
      console.log(`當前 URL: ${page.url()}`);
    }

    // 方法 2: 直接訪問可能的問卷 URL
    console.log('嘗試直接訪問問卷 URL...');
    await page.goto('https://www.prizerebel.com/survey.php');
    await page.waitForLoadState('networkidle');
    await page.screenshot({ path: '/home/claw/.openclaw/workspace/v4-03-survey.png' });

    // 方法 3: 嘗試 profile 頁面
    await page.goto('https://www.prizerebel.com/member/profile.php');
    await page.waitForLoadState('networkidle');
    await page.screenshot({ path: '/home/claw/.openclaw/workspace/v4-04-profile.png' });

    // 等待觀察
    console.log('等待 20 秒以便手動觀察...');
    await page.waitForTimeout(20000);

  } catch (error) {
    console.error('❌ 錯誤:', error.message);
    await page.screenshot({ path: '/home/claw/.openclaw/workspace/v4-error.png' });
  } finally {
    await browser.close();
    console.log('🔚 結束');
  }
})();
