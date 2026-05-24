Write-Host "====================================================" -ForegroundColor Cyan
Write-Host "🚀 Starting Automated Native CI Test Pipeline Suite" -ForegroundColor Cyan
Write-Host "====================================================" -ForegroundColor Cyan

# Activate environment if not already activated
if (Test-Path ".\env\Scripts\Activate.ps1") {
    Write-Host "📦 Ensuring Virtual Environment is Active..." -ForegroundColor Yellow
    & .\env\Scripts\Activate.ps1
}

Write-Host "🧪 Running Pytest validations..." -ForegroundColor Yellow
pytest test_app.py
$lastCode = $LASTEXITCODE

Write-Host "====================================================" -ForegroundColor Cyan
if ($lastCode -eq 0) {
    Write-Host "✅ SUCCESS: All tests passed flawlessly! Exit code: 0" -ForegroundColor Green
    exit 0
} else {
    Write-Host "❌ FAILURE: Test suite regression found. Exit code: 1" -ForegroundColor Red
    exit 1
}