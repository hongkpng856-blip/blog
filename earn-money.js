const { chromium } = require('playwright');
const fs = require('fs');

(async () => {
  console.log('🚀 啟動瀏覽器...');
  const browser = await chromium.launch({ headless: false });
  const context = await browser.newContext();
  const page = await context.newPage();

  try {
    // 登入 PrizeRebel
    console.log('📧 登入 PrizeRebel...');
    await page.goto('https://www.prizerebel.com/login.php');
    await page.fill('input[name="email"]', 'hongkpng856@gmail.com');
    await page.fill('input[name="password"]', 'mtsd479j');
    await page.click('input[type="submit"]');
    
    // 等待登入完成
    await page.waitForNavigation({ waitUntil: 'networkidle' });
    console.log('✅ 登入成功！');

    // 截圖保存
    await page.screenshot({ path: '/home/claw/.openclaw/workspace/prizerebel-login.png' });
    console.log('📸 截圖已保存');

    // 進入 Dashboard
    await page.goto('https://www.prizerebel.com/member/dashboard.php');
    await page.waitForLoadState('networkidle');
    
    // 檢查頁面內容
    const content = await page.content();
    console.log('📄 Dashboard 頁面已載入');

    // 嘗試找到並點擊問卷連結
    const surveyLinks = await page.$$('a');
    console.log(`找到 ${surveyLinks.length} 個連結`);

    // 截圖當前狀態
    await page.screenshot({ path: '/home/claw/.openclaw/workspace/prizerebel-dashboard.png', fullPage: true });

    // 查找 "Complete your profile" 連結
    const profileLink = await page.$('text="Complete your profile"');
    if (profileLink) {
      console.log('找到 "Complete your profile" 連結，嘗試點擊...');
      await profileLink.click();
      await page.waitForTimeout(3000);
      await page.screenshot({ path: '/home/claw/.openclaw/workspace/prizerebel-survey.png', fullPage: true });
    }

    // 查找 Video Ads
    const videoLink = await page.$('text="Video"');
    if (videoLink) {
      console.log('找到 Video Ads 連結');
    }

    // 嘗試進入 Earn 頁面
    console.log('進入 Earn 頁面...');
    await page.goto('https://www.prizerebel.com/earn.php');
    await page.waitForLoadState('networkidle');
    await page.screenshot({ path: '/home/claw/.openclaw/workspace/prizerebel-earn.png', fullPage: true });

    // 查找並點擊任何可用的任務
    const earnLinks = await page.$$('a');
    console.log(`Earn 頁面找到 ${earnLinks.length} 個連結`);

    // 檢查頁面文字內容
    const pageText = await page.textContent('body');
    console.log('頁面文字預覽:', pageText.substring(0, 500));

    // 保持瀏覽器開啟一段時間
    console.log('等待 30 秒觀察頁面...');
    await page.waitForTimeout(30000);

  } catch (error) {
    console.error('❌ 錯誤:', error.message);
    await page.screenshot({ path: '/home/claw/.openclaw/workspace/prizerebel-error.png' });
  } finally {
    await browser.close();
    console.log('🔚 瀏覽器已關閉');
  }
})();
