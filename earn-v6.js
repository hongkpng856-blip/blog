const { chromium } = require('playwright');

(async () => {
  console.log('🎯 PrizeRebel 問卷自動填寫 v6...');
  const browser = await chromium.launch({ 
    headless: false, 
    slowMo: 800
  });
  const context = await browser.newContext({
    viewport: { width: 1400, height: 900 }
  });
  const page = await context.newPage();

  let pointsEarned = 0;

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

    // 進入 offers
    await page.goto('https://www.prizerebel.com/offers.php');
    await page.waitForLoadState('networkidle');

    // 點擊 "Complete your profile"
    console.log('🔗 點擊問卷...');
    await page.click('text="Complete your profile"');
    await page.waitForTimeout(5000);

    // 檢查新視窗
    const pages = context.pages();
    console.log(`頁面數量: ${pages.length}`);

    if (pages.length > 1) {
      const surveyPage = pages[pages.length - 1];
      console.log('切換到問卷頁面...');
      await surveyPage.waitForLoadState('networkidle');
      await surveyPage.screenshot({ path: '/home/claw/.openclaw/workspace/v6-01-survey-start.png' });

      // 嘗試填寫問卷
      console.log('📝 開始填寫問卷...');
      
      let step = 0;
      let maxSteps = 20; // 最多嘗試 20 個步驟
      
      while (step < maxSteps) {
        step++;
        console.log(`步驟 ${step}...`);
        
        await surveyPage.waitForTimeout(2000);
        
        // 嘗試找到並選擇 radio buttons
        const radios = await surveyPage.$$('input[type="radio"]:not(:checked)');
        if (radios.length > 0) {
          // 選擇第一個未選中的 radio
          await radios[0].click();
          console.log(`選擇了一個 radio 選項`);
        }
        
        // 嘗試找到並選擇 checkboxes
        const checkboxes = await surveyPage.$$('input[type="checkbox"]:not(:checked)');
        if (checkboxes.length > 0) {
          await checkboxes[0].click();
          console.log(`選擇了一個 checkbox`);
        }
        
        // 嘗試找到並填寫 text inputs
        const textInputs = await surveyPage.$$('input[type="text"]:not([value]), textarea');
        for (const input of textInputs) {
          try {
            const placeholder = await input.getAttribute('placeholder');
            if (placeholder) {
              // 根據 placeholder 填寫適當內容
              if (placeholder.toLowerCase().includes('age') || placeholder.toLowerCase().includes('年齡')) {
                await input.fill('25');
              } else if (placeholder.toLowerCase().includes('zip') || placeholder.toLowerCase().includes('郵遞區號')) {
                await input.fill('10001');
              } else if (placeholder.toLowerCase().includes('name') || placeholder.toLowerCase().includes('名')) {
                await input.fill('Test');
              } else {
                await input.fill('Yes');
              }
            }
          } catch (e) {
            // 忽略錯誤
          }
        }
        
        // 嘗試找到並點擊 select dropdowns
        const selects = await surveyPage.$$('select');
        for (const select of selects) {
          try {
            await select.selectOption({ index: 1 }); // 選擇第一個選項
          } catch (e) {
            // 忽略錯誤
          }
        }
        
        // 截圖當前狀態
        await surveyPage.screenshot({ path: `/home/claw/.openclaw/workspace/v6-step-${step.toString().padStart(2, '0')}.png` });
        
        // 嘗試點擊下一步/提交按鈕
        const nextButtons = await surveyPage.$$('button:has-text("Next"), button:has-text("Submit"), button:has-text("Continue"), input[type="submit"], .next-btn, .submit-btn');
        if (nextButtons.length > 0) {
          await nextButtons[0].click();
          console.log('點擊下一步按鈕');
        }
        
        // 檢查是否完成
        const currentUrl = surveyPage.url();
        if (currentUrl.includes('complete') || currentUrl.includes('thank') || currentUrl.includes('done')) {
          console.log('✅ 問卷可能已完成！');
          await surveyPage.screenshot({ path: '/home/claw/.openclaw/workspace/v6-complete.png' });
          pointsEarned += 15;
          break;
        }
      }

      await surveyPage.close();
    }

    // 回到 PrizeRebel 檢查積分
    console.log('💰 檢查積分...');
    await page.goto('https://www.prizerebel.com/member/dashboard.php');
    await page.waitForLoadState('networkidle');
    await page.screenshot({ path: '/home/claw/.openclaw/workspace/v6-final-dashboard.png' });

    // 輸出結果
    console.log(`\n========== 結果 ==========`);
    console.log(`預估賺取積分: ${pointsEarned}`);
    console.log('========================\n');

    console.log('等待 10 秒...');
    await page.waitForTimeout(10000);

  } catch (error) {
    console.error('❌ 錯誤:', error.message);
    await page.screenshot({ path: '/home/claw/.openclaw/workspace/v6-error.png' });
  } finally {
    await browser.close();
    console.log('🔚 結束');
  }
})();
