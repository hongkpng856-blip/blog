/**
 * 免費資源網 - 主要 JavaScript
 */

document.addEventListener('DOMContentLoaded', function() {
    // ==========================================
    // 手機版選單切換
    // ==========================================
    const mobileMenuBtn = document.getElementById('mobileMenuBtn');
    const navMenu = document.getElementById('navMenu');

    if (mobileMenuBtn && navMenu) {
        mobileMenuBtn.addEventListener('click', function() {
            navMenu.classList.toggle('active');
            // 切換圖示
            const icon = this.querySelector('i');
            if (navMenu.classList.contains('active')) {
                icon.classList.remove('fa-bars');
                icon.classList.add('fa-times');
            } else {
                icon.classList.remove('fa-times');
                icon.classList.add('fa-bars');
            }
        });

        // 點擊選單連結後關閉選單
        navMenu.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                navMenu.classList.remove('active');
                const icon = mobileMenuBtn.querySelector('i');
                icon.classList.remove('fa-times');
                icon.classList.add('fa-bars');
            });
        });

        // 點擊頁面其他地方關閉選單
        document.addEventListener('click', function(e) {
            if (!navMenu.contains(e.target) && !mobileMenuBtn.contains(e.target)) {
                navMenu.classList.remove('active');
                const icon = mobileMenuBtn.querySelector('i');
                icon.classList.remove('fa-times');
                icon.classList.add('fa-bars');
            }
        });
    }

    // ==========================================
    // 回到頂部按鈕
    // ==========================================
    const backToTopBtn = document.getElementById('backToTop');

    if (backToTopBtn) {
        // 監聽滾動事件
        window.addEventListener('scroll', function() {
            if (window.scrollY > 300) {
                backToTopBtn.classList.add('show');
            } else {
                backToTopBtn.classList.remove('show');
            }
        });

        // 點擊回到頂部
        backToTopBtn.addEventListener('click', function() {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }

    // ==========================================
    // 搜尋框功能
    // ==========================================
    const searchBox = document.querySelector('.search-box');
    if (searchBox) {
        searchBox.addEventListener('submit', function(e) {
            e.preventDefault();
            const input = this.querySelector('input');
            const query = input.value.trim();
            if (query) {
                // 這裡可以實作搜尋功能
                alert('搜尋功能尚未實作\n搜尋關鍵字: ' + query);
            }
        });
    }

    // ==========================================
    // 電子報訂閱功能
    // ==========================================
    const newsletterForm = document.querySelector('.newsletter-form');
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const input = this.querySelector('input[type="email"]');
            const email = input.value.trim();
            if (email && validateEmail(email)) {
                // 這裡可以實作訂閱功能
                alert('感謝訂閱！\nEmail: ' + email);
                input.value = '';
            } else {
                alert('請輸入有效的 Email 地址');
            }
        });
    }

    // ==========================================
    // 圖片懶加載效果
    // ==========================================
    const lazyImages = document.querySelectorAll('img[loading="lazy"]');
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.classList.add('loaded');
                    observer.unobserve(img);
                }
            });
        });

        lazyImages.forEach(img => {
            imageObserver.observe(img);
        });
    }

    // ==========================================
    // 文章卡片點擊效果
    // ==========================================
    const postCards = document.querySelectorAll('.post-card');
    postCards.forEach(card => {
        card.addEventListener('click', function(e) {
            // 如果點擊的是連結，讓連結自己處理
            if (e.target.tagName === 'A') return;

            // 否則點擊整個卡片跳轉到文章
            const link = this.querySelector('h3 a');
            if (link) {
                window.location.href = link.href;
            }
        });

        // 添加游標樣式
        card.style.cursor = 'pointer';
    });

    // ==========================================
    // 滾動時 Header 效果
    // ==========================================
    const header = document.querySelector('.header');
    let lastScrollY = window.scrollY;

    window.addEventListener('scroll', function() {
        const currentScrollY = window.scrollY;

        if (currentScrollY > lastScrollY && currentScrollY > 100) {
            // 向下滾動 - 隱藏 header
            header.style.transform = 'translateY(-100%)';
        } else {
            // 向上滾動 - 顯示 header
            header.style.transform = 'translateY(0)';
        }

        lastScrollY = currentScrollY;
    });

    // ==========================================
    // 分類標籤篩選 (可選功能)
    // ==========================================
    const categoryLinks = document.querySelectorAll('.category-list a, .tag-cloud .tag');
    categoryLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const category = this.textContent.trim();
            // 這裡可以實作分類篩選功能
            alert('分類篩選功能尚未實作\n選擇分類: ' + category);
        });
    });

    // ==========================================
    // 閱讀進度條 (可選功能)
    // ==========================================
    function createProgressBar() {
        const progressBar = document.createElement('div');
        progressBar.className = 'reading-progress';
        progressBar.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            height: 3px;
            background: linear-gradient(90deg, #2563eb, #10b981);
            z-index: 9999;
            transition: width 0.1s ease;
            width: 0%;
        `;
        document.body.appendChild(progressBar);

        window.addEventListener('scroll', function() {
            const scrollTop = window.scrollY;
            const docHeight = document.documentElement.scrollHeight - window.innerHeight;
            const scrollPercent = (scrollTop / docHeight) * 100;
            progressBar.style.width = scrollPercent + '%';
        });
    }

    // 只在文章頁面啟用閱讀進度條
    if (document.querySelector('.post-detail')) {
        createProgressBar();
    }

    // ==========================================
    // 輔助函數
    // ==========================================
    function validateEmail(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    }

    // ==========================================
    // 廣告載入提示 (開發用)
    // ==========================================
    const adSlots = document.querySelectorAll('.ad-slot');
    adSlots.forEach(slot => {
        // 開發模式下顯示廣告位置
        if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
            slot.style.backgroundColor = '#f0f9ff';
            slot.style.borderColor = '#3b82f6';
        }
    });

    // ==========================================
    // Console 訊息
    // ==========================================
    console.log('%c免費資源網', 'font-size: 24px; font-weight: bold; color: #2563eb;');
    console.log('歡迎來到免費資源網！');
    console.log('如有問題請聯繫: contact@example.com');
});

// ==========================================
// 頁面載入完成後執行
// ==========================================
window.addEventListener('load', function() {
    // 隱藏載入動畫（如果有的話）
    const loader = document.querySelector('.page-loader');
    if (loader) {
        loader.style.opacity = '0';
        setTimeout(() => loader.style.display = 'none', 300);
    }
});
