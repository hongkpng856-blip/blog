/**
 * PrizeRebel 點數查詢腳本
 * 使用 axios + cheerio 保持 session 來登入並獲取點數
 */
const axios = require('axios');
const cheerio = require('cheerio');
const fs = require('fs');

class PrizeRebelChecker {
    constructor() {
        this.cookieJar = {};
        this.session = axios.create({
            baseURL: 'https://www.prizerebel.com',
            headers: {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Connection': 'keep-alive',
            },
            withCredentials: true,
            maxRedirects: 5,
            validateStatus: (status) => status < 400
        });
        
        // 攔截回應以保存 cookies
        this.session.interceptors.response.use((response) => {
            const setCookie = response.headers['set-cookie'];
            if (setCookie) {
                setCookie.forEach(cookie => {
                    const parts = cookie.split(';')[0].split('=');
                    if (parts.length >= 2) {
                        this.cookieJar[parts[0]] = parts[1];
                    }
                });
            }
            return response;
        });
        
        // 攔截請求以添加 cookies
        this.session.interceptors.request.use((config) => {
            const cookies = Object.entries(this.cookieJar)
                .map(([k, v]) => `${k}=${v}`)
                .join('; ');
            if (cookies) {
                config.headers.Cookie = cookies;
            }
            return config;
        });
    }
    
    async login(email, password) {
        console.log(`📧 嘗試登入: ${email}`);
        
        try {
            // 步驟 1: 訪問登入頁面
            const loginPage = await this.session.get('/login.php');
            console.log(`📄 登入頁面狀態: ${loginPage.status}`);
            
            // 步驉 2: 解析表單
            const $ = cheerio.load(loginPage.data);
            const formData = {};
            
            $('input[type="hidden"]').each((i, el) => {
                const name = $(el).attr('name');
                const value = $(el).attr('value');
                if (name && value) {
                    formData[name] = value;
                }
            });
            
            // 添加登入資料
            formData.email = email;
            formData.password = password;
            
            console.log('📝 表單資料:', JSON.stringify(formData, null, 2));
            
            // 步驟 3: 執行登入
            const loginResponse = await this.session.post('/login.php', 
                new URLSearchParams(formData).toString(), {
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                        'Referer': 'https://www.prizerebel.com/login.php'
                    },
                    maxRedirects: 10
                }
            );
            
            console.log(`📄 登入回應狀態: ${loginResponse.status}`);
            console.log(`📄 最終 URL: ${loginResponse.request?.res?.responseUrl || loginResponse.config?.url}`);
            
            // 保存登入回應
            fs.writeFileSync('/home/claw/.openclaw/workspace/pr-login-response.html', loginResponse.data);
            
            // 檢查是否成功
            const loginHtml = loginResponse.data;
            if (loginHtml.includes('dashboard') || loginHtml.includes('Logout') || loginHtml.includes('Sign Out')) {
                console.log('✅ 登入成功！');
                return true;
            } else {
                console.log('⚠️ 登入狀態不明，檢查回應...');
                
                // 檢查錯誤訊息
                if (loginHtml.includes('Invalid') || loginHtml.includes('incorrect') || loginHtml.includes('error')) {
                    console.log('❌ 登入失敗：可能帳號密碼錯誤');
                }
                return false;
            }
            
        } catch (error) {
            console.error('❌ 登入錯誤:', error.message);
            return false;
        }
    }
    
    async getPoints() {
        console.log('📊 獲取點數...');
        
        try {
            const dashboard = await this.session.get('/member/dashboard.php');
            const $ = cheerio.load(dashboard.data);
            
            // 保存 dashboard
            fs.writeFileSync('/home/claw/.openclaw/workspace/pr-dashboard.html', dashboard.data);
            
            // 嘗試多種方式找到點數
            let points = null;
            
            // 方法 1: 查找包含 "points" 的 class
            $('[class*="point"]').each((i, el) => {
                const text = $(el).text().trim();
                const match = text.match(/(\d+)/);
                if (match && !points) {
                    points = match[1];
                    console.log(`💰 找到點數 (class): ${points}`);
                }
            });
            
            // 方法 2: 正則搜索
            if (!points) {
                const patterns = [
                    /(\d+)\s*points?/i,
                    /points?\s*[:\s]*(\d+)/i,
                    /balance[^>]*>.*?(\d+)/i,
                    /credits?\s*[:\s]*(\d+)/i,
                    /(\d+)\s*pts/i
                ];
                
                for (const pattern of patterns) {
                    const match = dashboard.data.match(pattern);
                    if (match) {
                        points = match[1];
                        console.log(`💰 找到點數 (regex): ${points}`);
                        break;
                    }
                }
            }
            
            // 方法 3: 查找數字大於 10 的 span
            if (!points) {
                $('span, div').each((i, el) => {
                    const text = $(el).text().trim();
                    if (/^\d+$/.test(text) && parseInt(text) > 10) {
                        points = text;
                        console.log(`💰 找到點數 (span): ${points}`);
                        return false; // break
                    }
                });
            }
            
            return points;
            
        } catch (error) {
            console.error('❌ 獲取點數錯誤:', error.message);
            return null;
        }
    }
    
    async getAvailableSurveys() {
        console.log('📋 獲取可用問卷...');
        
        try {
            const surveysPage = await this.session.get('/surveys.php');
            const $ = cheerio.load(surveysPage.data);
            
            fs.writeFileSync('/home/claw/.openclaw/workspace/pr-surveys.html', surveysPage.data);
            
            const surveys = [];
            // 查找問卷
            $('[class*="survey"], [class*="offer"], [class*="task"]').each((i, el) => {
                const title = $(el).find('h3, h4, .title, .name').first().text().trim();
                const points = $(el).find('[class*="point"], [class*="reward"], [class*="credit"]').text().trim();
                
                if (title) {
                    surveys.push({ title, points: points || 'Unknown' });
                }
            });
            
            console.log(`📋 找到 ${surveys.length} 個問卷`);
            return surveys;
            
        } catch (error) {
            console.error('❌ 獲取問卷錯誤:', error.message);
            return [];
        }
    }
    
    async getEarnOffers() {
        console.log('🎯 獲取賺取機會...');
        
        try {
            const earnPage = await this.session.get('/earn.php');
            const $ = cheerio.load(earnPage.data);
            
            fs.writeFileSync('/home/claw/.openclaw/workspace/pr-earn.html', earnPage.data);
            
            const offers = [];
            $('a[href*="offer"], a[href*="survey"]').each((i, el) => {
                const text = $(el).text().trim();
                const href = $(el).attr('href');
                if (text && text.length > 3 && href) {
                    offers.push({ text, href });
                }
            });
            
            console.log(`🎯 找到 ${offers.length} 個賺取機會`);
            return offers.slice(0, 10);
            
        } catch (error) {
            console.error('❌ 獲取賺取機會錯誤:', error.message);
            return [];
        }
    }
    
    saveReport(report) {
        const jsonPath = '/home/claw/.openclaw/workspace/prizerebel-status.json';
        fs.writeFileSync(jsonPath, JSON.stringify(report, null, 2));
        console.log(`✅ 狀態報告已保存: ${jsonPath}`);
    }
}

async function main() {
    console.log('='.repeat(50));
    console.log('🚀 PrizeRebel 點數檢查');
    console.log('='.repeat(50));
    
    const checker = new PrizeRebelChecker();
    
    // 登入
    const email = 'hongkpng856@gmail.com';
    const password = 'mtsd479j';
    
    const loginSuccess = await checker.login(email, password);
    
    if (loginSuccess) {
        // 獲取點數
        const points = await checker.getPoints();
        console.log(`\n📊 目前點數: ${points || '未知'}`);
        
        // 獲取問卷
        const surveys = await checker.getAvailableSurveys();
        
        // 獲取賺取機會
        const offers = await checker.getEarnOffers();
        
        // 保存報告
        const report = {
            timestamp: new Date().toISOString(),
            email: email,
            points: points,
            surveys_count: surveys.length,
            offers_count: offers.length,
            surveys: surveys.slice(0, 5),
            offers: offers.slice(0, 5),
            login_success: true
        };
        
        checker.saveReport(report);
        
        console.log('='.repeat(50));
        return report;
    } else {
        console.log('❌ 無法完成檢查');
        
        const report = {
            timestamp: new Date().toISOString(),
            email: email,
            login_success: false,
            error: '登入失敗'
        };
        
        checker.saveReport(report);
        return report;
    }
}

main().catch(console.error);
