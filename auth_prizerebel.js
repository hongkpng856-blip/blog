/**
 * PrizeRebel 正確登入腳本
 * 分析登入頁面並執行登入
 */
const axios = require('axios');
const cheerio = require('cheerio');
const fs = require('fs');

class PrizeRebelAuth {
    constructor() {
        this.cookies = {};
        this.session = axios.create({
            baseURL: 'https://www.prizerebel.com',
            headers: {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
            },
            withCredentials: true,
            maxRedirects: 0, // 不自動重定向
            validateStatus: (status) => status < 400 || status === 302 || status === 301
        });
        
        // 攔截回應
        this.session.interceptors.response.use((response) => {
            // 保存 cookies
            const setCookie = response.headers['set-cookie'];
            if (setCookie) {
                setCookie.forEach(cookie => {
                    const parts = cookie.split(';')[0].split('=');
                    if (parts.length >= 2) {
                        this.cookies[parts[0]] = parts[1];
                    }
                });
            }
            return response;
        }, (error) => {
            if (error.response && (error.response.status === 302 || error.response.status === 301)) {
                // 處理重定向
                const setCookie = error.response.headers['set-cookie'];
                if (setCookie) {
                    setCookie.forEach(cookie => {
                        const parts = cookie.split(';')[0].split('=');
                        if (parts.length >= 2) {
                            this.cookies[parts[0]] = parts[1];
                        }
                    });
                }
                return error.response;
            }
            throw error;
        });
        
        // 攔截請求
        this.session.interceptors.request.use((config) => {
            const cookieStr = Object.entries(this.cookies)
                .map(([k, v]) => `${k}=${v}`)
                .join('; ');
            if (cookieStr) {
                config.headers.Cookie = cookieStr;
            }
            return config;
        });
    }
    
    async login(email, password) {
        console.log(`🔐 嘗試登入 PrizeRebel...`);
        console.log(`📧 Email: ${email}`);
        
        try {
            // 步驟 1: 訪問首頁獲取初始 cookies
            console.log('\n📄 步驟 1: 訪問首頁...');
            const homePage = await this.session.get('/');
            console.log(`狀態: ${homePage.status}`);
            console.log(`Cookies: ${JSON.stringify(this.cookies, null, 2)}`);
            
            // 步驟 2: 構建登入請求
            // PrizeRebel 的登入是通過 POST 到 /index.php
            console.log('\n📝 步驟 2: 執行登入...');
            
            const loginData = new URLSearchParams();
            loginData.append('email', email);
            loginData.append('password', password);
            loginData.append('action', 'login');
            
            const loginResponse = await this.session.post('/index.php', loginData.toString(), {
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Referer': 'https://www.prizerebel.com/',
                    'Origin': 'https://www.prizerebel.com'
                }
            });
            
            console.log(`登入回應狀態: ${loginResponse.status}`);
            console.log(`登入回應 URL: ${loginResponse.headers.location || 'N/A'}`);
            
            // 保存登入回應
            if (loginResponse.data) {
                fs.writeFileSync('/home/claw/.openclaw/workspace/pr-login-response.html', loginResponse.data);
            }
            
            // 檢查重定向位置
            const location = loginResponse.headers.location;
            if (location) {
                console.log(`重定向到: ${location}`);
                
                // 如果重定向到 dashboard，表示登入成功
                if (location.includes('dashboard') || location.includes('member')) {
                    console.log('✅ 登入成功！');
                    
                    // 跟隨重定向
                    const dashboardResponse = await this.session.get(location, {
                        baseURL: ''
                    });
                    
                    fs.writeFileSync('/home/claw/.openclaw/workspace/pr-dashboard.html', dashboardResponse.data);
                    console.log(`Dashboard 狀態: ${dashboardResponse.status}`);
                    
                    return true;
                }
            }
            
            // 檢查回應內容
            if (loginResponse.data) {
                if (loginResponse.data.includes('Invalid') || loginResponse.data.includes('error')) {
                    console.log('❌ 登入失敗：可能帳號密碼錯誤');
                } else if (loginResponse.data.includes('dashboard') || loginResponse.data.includes('Logout')) {
                    console.log('✅ 登入成功！');
                    return true;
                }
            }
            
            // 嘗試直接訪問 dashboard
            console.log('\n📊 嘗試直接訪問 Dashboard...');
            const dashboard = await this.session.get('/member/dashboard.php');
            console.log(`Dashboard 狀態: ${dashboard.status}`);
            
            fs.writeFileSync('/home/claw/.openclaw/workspace/pr-dashboard.html', dashboard.data);
            
            // 檢查是否成功登入
            if (dashboard.data.includes('Logout') || dashboard.data.includes('Sign Out')) {
                console.log('✅ 登入成功！');
                return true;
            } else if (dashboard.data.includes('login') && dashboard.data.includes('password')) {
                console.log('❌ 未登入，被重定向到登入頁面');
                return false;
            }
            
            return true;
            
        } catch (error) {
            console.error('❌ 錯誤:', error.message);
            return false;
        }
    }
    
    async getPoints() {
        console.log('\n💰 獲取點數...');
        
        try {
            const dashboard = await this.session.get('/member/dashboard.php');
            const $ = cheerio.load(dashboard.data);
            
            // 嘗試多種選擇器
            let points = null;
            
            // 查找包含 "points" 的元素
            const pageText = dashboard.data;
            
            // 正則匹配
            const patterns = [
                /(\d+)\s*points?/i,
                /points?\s*[:\s]*(\d+)/i,
                /balance[^>]*?>[^<]*(\d+)/i,
                /Your\s+Points[^>]*?>[^<]*(\d+)/i
            ];
            
            for (const pattern of patterns) {
                const match = pageText.match(pattern);
                if (match) {
                    points = match[1];
                    console.log(`💰 找到點數: ${points}`);
                    break;
                }
            }
            
            // 如果沒找到，嘗試從數字開頭的 span 查找
            if (!points) {
                $('span, div, p').each((i, el) => {
                    const text = $(el).text().trim();
                    if (/^\d+$/.test(text) && parseInt(text) > 10) {
                        points = text;
                        return false;
                    }
                });
            }
            
            return points;
            
        } catch (error) {
            console.error('❌ 獲取點數錯誤:', error.message);
            return null;
        }
    }
    
    async getDashboardInfo() {
        console.log('\n📊 獲取 Dashboard 資訊...');
        
        try {
            const dashboard = await this.session.get('/member/dashboard.php');
            const $ = cheerio.load(dashboard.data);
            
            // 提取用戶名
            let username = 'Unknown';
            $('.username, .user-name, [class*="user"]').each((i, el) => {
                const text = $(el).text().trim();
                if (text && text.length < 50) {
                    username = text;
                }
            });
            
            // 提取點數
            let points = 'Unknown';
            $('[class*="point"]').each((i, el) => {
                const text = $(el).text().trim();
                const match = text.match(/(\d+)/);
                if (match) {
                    points = match[1];
                }
            });
            
            // 提取等級
            let level = 'Unknown';
            $('[class*="level"], [class*="rank"]').each((i, el) => {
                const text = $(el).text().trim();
                if (text) {
                    level = text;
                }
            });
            
            return { username, points, level };
            
        } catch (error) {
            console.error('❌ 獲取 Dashboard 錯誤:', error.message);
            return null;
        }
    }
    
    saveReport(report) {
        const path = '/home/claw/.openclaw/workspace/prizerebel-status.json';
        fs.writeFileSync(path, JSON.stringify(report, null, 2));
        console.log(`\n✅ 報告已保存: ${path}`);
    }
}

async function main() {
    console.log('='.repeat(60));
    console.log('🚀 PrizeRebel 登入與點數查詢');
    console.log('='.repeat(60));
    
    const auth = new PrizeRebelAuth();
    
    // 帳號資訊
    const email = 'hongkpng856@gmail.com';
    const password = 'mtsd479j';
    
    // 執行登入
    const loginSuccess = await auth.login(email, password);
    
    if (loginSuccess) {
        // 獲取 Dashboard 資訊
        const dashboardInfo = await auth.getDashboardInfo();
        
        if (dashboardInfo) {
            console.log('\n📊 Dashboard 資訊:');
            console.log(`  用戶名: ${dashboardInfo.username}`);
            console.log(`  點數: ${dashboardInfo.points}`);
            console.log(`  等級: ${dashboardInfo.level}`);
        }
        
        // 獲取點數
        const points = await auth.getPoints();
        
        // 保存報告
        const report = {
            timestamp: new Date().toISOString(),
            email: email,
            login_success: true,
            points: points,
            dashboard: dashboardInfo
        };
        
        auth.saveReport(report);
        
        console.log('\n' + '='.repeat(60));
        console.log('📊 最終報告:');
        console.log(`  登入狀態: ✅ 成功`);
        console.log(`  目前點數: ${points || 'Unknown'}`);
        console.log('='.repeat(60));
        
        return report;
    } else {
        console.log('\n❌ 登入失敗');
        
        const report = {
            timestamp: new Date().toISOString(),
            email: email,
            login_success: false
        };
        
        auth.saveReport(report);
        return report;
    }
}

main().catch(console.error);
