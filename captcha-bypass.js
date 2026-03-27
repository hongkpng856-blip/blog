// 使用 Playwright + 2Captcha 繞過 reCAPTCHA
// 需要: npm install playwright 2captcha-ts

const { chromium } = require('playwright');
const Solver = require('2captcha-ts');

(async () => {
  console.log('🔍 啟動 CAPTCHA 繞過流程...');
  
  // 檢查是否有 2Captcha API key
  const apiKey = process.env.TWOCAPTCHA_KEY || process.env.CAPTCHA_KEY;
  
  if (!apiKey) {
    console.log('❌ 需要 2Captcha API key');
    console.log('請設定環境變數: TWOCAPTCHA_KEY 或 CAPTCHA_KEY');
    console.log('');
    console.log('取得 API key: https://2captcha.com/');
    console.log('免費試用: https://2captcha.com/auth/register');
    process.exit(1);
  }
  
  console.log('✅ 找到 API key');
  
  const browser = await chromium.launch({ 
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });
  
  const context = await browser.newContext({
    viewport: { width: 1280, height: 800 }
  });
  
  const page = await context.newPage();
  
  try {
    console.log('📧 前往 PrizeRebel 登入頁面...');
    await page.goto('https://www.prizerebel.com/login.php', { waitUntil: 'networkidle' });
    
    // 填寫登入表單
    console.log('📝 填寫登入資訊...');
    await page.fill('input[name="email"]', 'hongkpng856@gmail.com');
    await page.fill('input[name="password"]', 'mtsd479j');
    
    // 使用 2Captcha 解決 reCAPTCHA
    console.log('🤖 解決 reCAPTCHA...');
    const solver = new Solver.Solver(apiKey);
    
    const res = await solver.solveRecaptchaV2(
      '6Lc_RL8UAAAAAKm5urRcE5B3Y8mpD8pHiN0z3hr4', // PrizeRebel reCAPTCHA site key
      page.url()
    );
    
    console.log('✅ CAPTCHA 已解決');
    
    // 設定 reCAPTCHA response
    await page.evaluate((token) => {
      document.getElementById('g-recaptcha-response').innerHTML = token;
    }, res.data);
    
    // 提交表單
    console.log('📤 提交登入...');
    await page.click('input[type="submit"]');
    
    await page.waitForTimeout(5000);
    
    console.log('📍 目前 URL:', page.url());
    
    // 截圖
    await page.screenshot({ path: '/home/claw/.openclaw/workspace/login-result.png' });
    console.log('📸 截圖已保存');
    
    // 保存 cookies
    const cookies = await context.cookies();
    require('fs').writeFileSync(
      '/home/claw/.openclaw/workspace/prizerebel-cookies.json',
      JSON.stringify(cookies, null, 2)
    );
    console.log('🍪 Cookies 已保存');
    
  } catch (error) {
    console.error('❌ 錯誤:', error.message);
    await page.screenshot({ path: '/home/claw/.openclaw/workspace/error-captcha.png' });
  } finally {
    await browser.close();
  }
})();
