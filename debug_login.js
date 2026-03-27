/**
 * PrizeRebel 登入調試腳本
 * 分析登入頁面結構
 */
const axios = require('axios');
const cheerio = require('cheerio');
const fs = require('fs');

async function debugLogin() {
    console.log('🔍 分析 PrizeRebel 登入頁面...');
    
    const session = axios.create({
        baseURL: 'https://www.prizerebel.com',
        headers: {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
        },
        withCredentials: true
    });
    
    // 保存 cookies
    const cookies = {};
    
    session.interceptors.response.use((response) => {
        const setCookie = response.headers['set-cookie'];
        if (setCookie) {
            setCookie.forEach(cookie => {
                const parts = cookie.split(';')[0].split('=');
                if (parts.length >= 2) {
                    cookies[parts[0]] = parts[1];
                    console.log(`🍪 Cookie: ${parts[0]} = ${parts[1]}`);
                }
            });
        }
        return response;
    });
    
    try {
        // 步驟 1: 獲取登入頁面
        console.log('\n📄 步驟 1: 獲取登入頁面...');
        const loginPage = await session.get('/login.php');
        console.log(`狀態: ${loginPage.status}`);
        
        // 保存頁面
        fs.writeFileSync('/home/claw/.openclaw/workspace/pr-login-page.html', loginPage.data);
        
        // 步驟 2: 解析表單
        const $ = cheerio.load(loginPage.data);
        
        console.log('\n📝 登入表單分析:');
        
        // 找到所有表單
        $('form').each((i, form) => {
            console.log(`\n表單 ${i + 1}:`);
            console.log(`  Action: ${$(form).attr('action')}`);
            console.log(`  Method: ${$(form).attr('method')}`);
            console.log(`  ID: ${$(form).attr('id')}`);
            
            // 列出所有 input
            $(form).find('input').each((j, input) => {
                const name = $(input).attr('name');
                const type = $(input).attr('type');
                const value = $(input).attr('value');
                const id = $(input).attr('id');
                console.log(`    Input: name="${name}" type="${type}" value="${value || ''}" id="${id || ''}"`);
            });
        });
        
        // 找特定的登入表單
        console.log('\n🎯 尋找登入表單...');
        const loginForm = $('form[action*="login"]').first();
        if (loginForm.length) {
            console.log('找到登入表單!');
            console.log(`Action: ${loginForm.attr('action')}`);
        }
        
        // 檢查是否有 reCAPTCHA
        console.log('\n🔐 安全檢查:');
        if (loginPage.data.includes('recaptcha') || loginPage.data.includes('g-recaptcha')) {
            console.log('⚠️ 發現 reCAPTCHA！');
        }
        if (loginPage.data.includes('cf-') || loginPage.data.includes('cloudflare')) {
            console.log('⚠️ 發現 Cloudflare 保護！');
        }
        if (loginPage.data.includes('csrf') || loginPage.data.includes('token')) {
            console.log('✅ 發現 CSRF Token');
        }
        
        // 提取所有隱藏欄位
        console.log('\n🔒 Hidden fields:');
        $('input[type="hidden"]').each((i, el) => {
            console.log(`  ${$(el).attr('name')} = ${$(el).attr('value')}`);
        });
        
        // 分析完整的登入流程
        console.log('\n📊 分析結果已保存到 pr-login-page.html');
        
    } catch (error) {
        console.error('❌ 錯誤:', error.message);
    }
}

debugLogin().catch(console.error);
