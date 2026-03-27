# 賺錢平台一鍵啟動腳本（Windows PowerShell）
# 用途：同時開啟 Prolific + PrizeRebel + Swagbucks

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  賺錢平台一鍵啟動器 v1.0" -ForegroundColor Cyan
Write-Host "  目標：最少賺取 $5 USD" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 平台列表
$platforms = @(
    @{Name="Prolific"; Url="https://app.prolific.com/register/participant/join-waitlist/about-yourself"; Note="🌟 無 CAPTCHA，高報酬"},
    @{Name="PrizeRebel"; Url="https://www.prizerebel.com/login.php"; Note="已註冊，需處理 CAPTCHA"},
    @{Name="Swagbucks"; Url="https://www.swagbucks.com/login"; Note="已註冊，需處理 CAPTCHA"}
)

Write-Host "將開啟以下平台：" -ForegroundColor Yellow
foreach ($p in $platforms) {
    Write-Host "  - $($p.Name): $($p.Note)" -ForegroundColor White
}
Write-Host ""

Write-Host "按任意鍵開啟所有平台..." -ForegroundColor Green
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

# 開啟平台
foreach ($p in $platforms) {
    Write-Host "開啟 $($p.Name)..." -ForegroundColor Cyan
    Start-Process $p.Url
    Start-Sleep -Milliseconds 500
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  所有平台已開啟！" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "登入資訊：" -ForegroundColor Yellow
Write-Host "  Email: hongkpng856@gmail.com" -ForegroundColor White
Write-Host "  PrizeRebel 密碼: mtsd479j" -ForegroundColor White
Write-Host "  Swagbucks 密碼: Mypassword123!" -ForegroundColor White
Write-Host ""

Write-Host "今日任務：" -ForegroundColor Yellow
Write-Host "  1. Prolific: 完成註冊 + 填寫基本資料" -ForegroundColor White
Write-Host "  2. PrizeRebel: 登入 + 完成 Daily Survey (+72 點)" -ForegroundColor White
Write-Host "  3. Swagbucks: 登入 + 完成每日任務" -ForegroundColor White
Write-Host ""

Write-Host "完成後請回報：" -ForegroundColor Green
Write-Host "  - Prolific 註冊狀態"
Write-Host "  - PrizeRebel 當前點數"
Write-Host "  - Swagbucks 當前 SB 點數"
Write-Host ""
