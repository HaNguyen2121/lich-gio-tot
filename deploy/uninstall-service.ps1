# Go dich vu nen tren Windows. Sau khi go van chay thu cong: python -m giotot
#   powershell -ExecutionPolicy Bypass -File deploy\uninstall-service.ps1

$ErrorActionPreference = "SilentlyContinue"

Stop-ScheduledTask -TaskName "GioTotDichLy"
Unregister-ScheduledTask -TaskName "GioTotDichLy" -Confirm:$false

# Tat tien trinh con nghe cong 5057 (neu con)
Get-NetTCPConnection -LocalPort 5057 -State Listen | ForEach-Object {
    Stop-Process -Id $_.OwningProcess -Force
}

Write-Host "Da go dich vu nen. Chay thu cong khi can: python -m giotot"
