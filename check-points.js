const { chromium } = require('playwright');

(async () => {
  console.log('🔍 檢查 PrizeRebel 點數...');
  
  const browser = await chromium.launch({ 
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });
  
  const context = await browser.newContext({
    viewport: { width: 1280, height: 800 }
  });
  
  const page = await context.newPage();
  
  try {
    // 登入
    console.log('📧 登入中...');
    await page.goto('https://www.prizerebel.com/login.php', { waitUntil: 'networkidle' });
    
    // 填寫登入表單
    await page.fill('input[name="email"]', 'hongkpng856@gmail.com');
    await page.fill('input[name="password"]', 'mtsd479j');
    await page.click('input[type="submit"]');
    
    // 等待登入完成
    await page.waitForTimeout(3000);
    
    // 進入 Dashboard
    console.log('📊 進入 Dashboard...');
    await page.goto('https://www.prizerebel.com/member/dashboard.php', { waitUntil: 'networkidle' });
    
    // 截圖
    await page.screenshot({ path: '/home/claw/.openclaw/workspace/dashboard-check.png', fullPage: true });
    
    // 獲取頁面內容
    const content = await page.content();
    
    // 尋找點數
    const pointsMatch = content.match(/(\d+)\s*points?/i);
    if (pointsMatch) {
      console.log(`💰 目前點數: ${pointsMatch[1]}`);
    }
    
    // 提取更多資訊
    const url = page.url();
    console.log(`📍 目前 URL: ${url}`);
    
    // 獲取頁面標題
    const title = await page.title();
    console.log(`📄 頁面標題: ${title}`);
    
    // 檢查是否在登入頁面（表示登入失敗）
    if (url.includes('login') || title.toLowerCase().includes('login')) {
      console.log('⚠️ 可能在登入頁面，需要檢查截圖');
    }
    
    // 保存頁面 HTML
    require('fs').writeFileSync('/home/claw/.openclaw/workspace/dashboard.html', content);
    console.log('✅ 頁面 HTML 已保存');
    
  } catch (error) {
    console.error('❌ 錯誤:', error.message);
    await page.screenshot({ path: '/home/claw/.openclaw/workspace/error-dashboard.png' });
  } finally {
    await browser.close();
    console.log('🔚 完成');
  }
})();
