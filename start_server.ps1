# CareTaker Server Startup Script
Write-Host "Starting CareTaker Agent Swarm..." -ForegroundColor Cyan
$env:FLASK_APP = "caretaker.app"
$env:FLASK_ENV = "development"

# Check if port 5001 is in use and kill it if necessary (optional, but helpful)
$port = 5001
$tcpConnection = Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue
if ($tcpConnection) {
    Write-Host "Port $port is in use. Attempting to free it..." -ForegroundColor Yellow
    Stop-Process -Id $tcpConnection.OwningProcess -Force -ErrorAction SilentlyContinue
    Start-Sleep -Seconds 1
}

python -m caretaker.app
