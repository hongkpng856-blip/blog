const { chromium } = require('playwright');
const fs = require('fs');

(async () => {
  console.log('🎯 完整問卷填寫流程...');
  const browser = await chromium.launch({ 
    headless: false, 
    slowMo: 1500
  });
  const context = await browser.newContext({
    viewport: { width: 1400, height: 900 }
  });
  const page = await context.newPage();

  try {
    // 登入
    console.log('📧 登入 PrizeRebel...');
    await page.goto('https://www.prizerebel.com/login.php');
    await page.waitForLoadState('networkidle');
    await page.fill('input[name="email"]', 'hongkpng856@gmail.com');
    await page.fill('input[name="password"]', 'mtsd479j');
    await page.click('input[type="submit"]');
    await page.waitForNavigation({ waitUntil: 'networkidle' });
    console.log('✅ 登入成功');

    // 記錄初始積分
    await page.goto('https://www.prizerebel.com/member/dashboard.php');
    await page.waitForLoadState('networkidle');
    await page.screenshot({ path: '/home/claw/.openclaw/workspace/v5-01-start.png' });

    // 進入 offers 頁面
    console.log('📊 進入 offers 頁面...');
    await page.goto('https://www.prizerebel.com/offers.php');
    await page.waitForLoadState('networkidle');
    await page.screenshot({ path: '/home/claw/.openclaw/workspace/v5-02-offers.png' });

    // 點擊 "Complete your profile"
    console.log('🔗 點擊 "Complete your profile"...');
    const profileLink = await page.$('text="Complete your profile"');
    if (profileLink) {
      await profileLink.click();
      await page.waitForTimeout(5000);
      
      // 截圖當前狀態
      await page.screenshot({ path: '/home/claw/.openclaw/workspace/v5-03-popup.png' });

      // 檢查是否有新視窗/彈窗
      const pages = context.pages();
      console.log(`當前有 ${pages.length} 個頁面`);

      if (pages.length > 1) {
        // 切換到新視窗
        const popup = pages[pages.length - 1];
        console.log('發現彈出視窗，切換過去...');
        await popup.waitForLoadState('networkidle');
        await popup.screenshot({ path: '/home/claw/.openclaw/workspace/v5-04-popup-content.png' });

        // 嘗試填寫彈出視窗中的表單
        const radioButtons = await popup.$$('input[type="radio"]');
        console.log(`彈窗中找到 ${radioButtons.length} 個選項`);

        // 隨機選擇一些選項
        for (let i = 0; i < Math.min(3, radioButtons.length); i++) {
          try {
            await radioButtons[i].check();
            await popup.waitForTimeout(500);
          } catch (e) {
            // 忽略錯誤
          }
        }

        // 尋找提交按鈕
        const submitBtn = await popup.$('button[type="submit"], input[type="submit"], .submit, .next');
        if (submitBtn) {
          console.log('找到提交按鈕，點擊...');
          await submitBtn.click();
          await popup.waitForTimeout(3000);
          await popup.screenshot({ path: '/home/claw/.openclaw/workspace/v5-05-after-submit.png' });
        }

        await popup.close();
      }
    }

    // 回到 Dashboard 檢查積分
    console.log('💰 檢查積分變化...');
    await page.goto('https://www.prizerebel.com/member/dashboard.php');
    await page.waitForLoadState('networkidle');
    await page.screenshot({ path: '/home/claw/.openclaw/workspace/v5-06-final.png' });

    // 嘗試 Daily Survey
    console.log('📊 嘗試 Daily Survey...');
    await page.goto('https://www.prizerebel.com/offers.php');
    await page.waitForLoadState('networkidle');

    const dailySurveyLink = await page.$('text="Your Surveys Daily Survey"');
    if (dailySurveyLink) {
      console.log('找到 Daily Survey，點擊...');
      await dailySurveyLink.click();
      await page.waitForTimeout(5000);
      await page.screenshot({ path: '/home/claw/.openclaw/workspace/v5-07-daily-survey.png' });
    }

    // 最終截圖
    await page.goto('https://www.prizerebel.com/member/dashboard.php');
    await page.waitForLoadState('networkidle');
    await page.screenshot({ path: '/home/claw/.openclaw/workspace/v5-final.png', fullPage: true });

    console.log('等待 15 秒...');
    await page.waitForTimeout(15000);

  } catch (error) {
    console.error('❌ 錯誤:', error.message);
    await page.screenshot({ path: '/home/claw/.openclaw/workspace/v5-error.png' });
  } finally {
    await browser.close();
    console.log('🔚 完成！');
  }
})();
