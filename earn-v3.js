const { chromium } = require('playwright');
const fs = require('fs');

(async () => {
  console.log('🚀 啟動賺錢自動化 v3...');
  const browser = await chromium.launch({ headless: false, slowMo: 1000 });
  const context = await browser.newContext({
    viewport: { width: 1280, height: 900 }
  });
  const page = await context.newPage();

  let report = {
    startTime: new Date().toISOString(),
    steps: [],
    pointsEarned: 0
  };

  function log(msg) {
    console.log(`[${new Date().toLocaleTimeString()}] ${msg}`);
    report.steps.push({ time: new Date().toISOString(), message: msg });
  }

  try {
    // Step 1: 登入
    log('登入 PrizeRebel...');
    await page.goto('https://www.prizerebel.com/login.php', { waitUntil: 'networkidle' });
    await page.fill('input[name="email"]', 'hongkpng856@gmail.com');
    await page.fill('input[name="password"]', 'mtsd479j');
    await page.click('input[type="submit"]');
    await page.waitForNavigation({ waitUntil: 'networkidle' });
    log('✅ 登入成功');

    // Step 2: 進入 Dashboard
    log('進入 Dashboard...');
    await page.goto('https://www.prizerebel.com/member/dashboard.php', { waitUntil: 'networkidle' });
    await page.screenshot({ path: '/home/claw/.openclaw/workspace/v3-01-dashboard.png' });

    // Step 3: 嘗試找到並點擊 "Complete your profile"
    log('尋找問卷任務...');
    
    // 使用多種選擇器嘗試找到連結
    const selectors = [
      'a:has-text("Complete your profile")',
      'a:has-text("profile")',
      '[href*="profile"]',
      '.task-link',
      '.survey-link'
    ];

    let foundTask = false;
    for (const selector of selectors) {
      try {
        const element = await page.$(selector);
        if (element) {
          log(`找到元素: ${selector}`);
          await element.click();
          await page.waitForLoadState('networkidle');
          await page.waitForTimeout(3000);
          foundTask = true;
          break;
        }
      } catch (e) {
        // 繼續嘗試下一個選擇器
      }
    }

    if (foundTask) {
      log('成功進入任務頁面');
      await page.screenshot({ path: '/home/claw/.openclaw/workspace/v3-02-task-page.png' });

      // 嘗試填寫問卷
      const inputs = await page.$$('input[type="text"], input[type="radio"], select');
      log(`找到 ${inputs.length} 個表單元素`);

      // 截圖當前狀態
      await page.screenshot({ path: '/home/claw/.openclaw/workspace/v3-03-form.png' });
    } else {
      log('未找到任務連結，嘗試其他方法...');

      // 嘗試直接訪問問卷頁面
      log('訪問 offers 頁面...');
      await page.goto('https://www.prizerebel.com/offers.php', { waitUntil: 'networkidle' });
      await page.screenshot({ path: '/home/claw/.openclaw/workspace/v3-04-offers.png' });

      // 檢查頁面內容
      const bodyText = await page.textContent('body');
      log(`頁面內容預覽: ${bodyText.substring(0, 200)}...`);
    }

    // Step 4: 嘗試 Video 區域
    log('檢查 Video 任務...');
    await page.goto('https://www.prizerebel.com/earn.php', { waitUntil: 'networkidle' });
    
    const videoLink = await page.$('a:has-text("Video"), a:has-text("video")');
    if (videoLink) {
      log('找到 Video 連結');
      await videoLink.click();
      await page.waitForLoadState('networkidle');
      await page.screenshot({ path: '/home/claw/.openclaw/workspace/v3-05-videos.png' });
    }

    // 最終截圖
    await page.screenshot({ path: '/home/claw/.openclaw/workspace/v3-final.png', fullPage: true });
    log('完成所有步驟');

    // 等待觀察
    log('等待 15 秒...');
    await page.waitForTimeout(15000);

  } catch (error) {
    log(`❌ 錯誤: ${error.message}`);
    await page.screenshot({ path: '/home/claw/.openclaw/workspace/v3-error.png' });
  } finally {
    // 保存報告
    report.endTime = new Date().toISOString();
    fs.writeFileSync('/home/claw/.openclaw/workspace/earn-report-v3.json', JSON.stringify(report, null, 2));
    
    await browser.close();
    log('🔚 結束');
  }
})();
