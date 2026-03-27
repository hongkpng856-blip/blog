# PrizeRebel 登入輔助腳本（Windows PowerShell）
# 用途：在 Windows 上開啟瀏覽器，手動處理 CAPTCHA，然後導出 cookies

Write-Host "=== PrizeRebel 登入輔助 ===" -ForegroundColor Cyan
Write-Host ""

# 檢查 Chrome 是否存在
$chromePath = "C:\Program Files\Google\Chrome\Application\chrome.exe"
if (-not (Test-Path $chromePath)) {
    $chromePath = "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
}

if (Test-Path $chromePath) {
    Write-Host "[OK] 找到 Chrome: $chromePath" -ForegroundColor Green
} else {
    Write-Host "[WARN] 未找到 Chrome，將使用預設瀏覽器" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "步驟 1: 開啟 PrizeRebel 登入頁面..." -ForegroundColor Cyan
Start-Process "https://www.prizerebel.com/login.php"

Write-Host ""
Write-Host "請在瀏覽器中完成以下步驟：" -ForegroundColor Yellow
Write-Host "  1. 輸入 Email: hongkpng856@gmail.com"
Write-Host "  2. 輸入 Password: mtsd479j"
Write-Host "  3. 完成 CAPTCHA 驗證"
Write-Host "  4. 點擊登入"
Write-Host "  5. 登入成功後，按任意鍵繼續..."
Write-Host ""

$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

Write-Host ""
Write-Host "步驟 2: 請手動記錄以下資訊：" -ForegroundColor Cyan
Write-Host "  - 點數餘額（右上角）"
Write-Host "  - 是否有 Daily Survey 可做"
Write-Host "  - 截圖保存到桌面"
Write-Host ""

Write-Host "完成後請將截圖傳送給 Agent，以便記錄進度。" -ForegroundColor Green
Write-Host ""
Write-Host "=== 提示 ===" -ForegroundColor Cyan
Write-Host "若要自動化，可安裝 Chrome 擴充功能 'EditThisCookie'"
Write-Host "登入後用擴充功能導出 cookies JSON"
Write-Host ""
