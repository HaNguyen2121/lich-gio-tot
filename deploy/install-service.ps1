# Cai dich vu nen tren Windows (Task Scheduler): app tu chay khi dang nhap,
# luon san o http://127.0.0.1:<port>. Tu do duong dan Python + thu muc project.
#
#   powershell -ExecutionPolicy Bypass -File deploy\install-service.ps1 [port]
#   (mac dinh port 5057)

$ErrorActionPreference = "Stop"

$ProjectDir = (Resolve-Path "$PSScriptRoot\..").Path
if ($args.Count -ge 1) { $Port = $args[0] } else { $Port = "5057" }

# Tim pythonw.exe (chay khong hien cua so console)
$PyExe = $null
$cmd = Get-Command pythonw.exe -ErrorAction SilentlyContinue
if ($cmd) { $PyExe = $cmd.Source }
if (-not $PyExe) {
    $p = Get-Command python.exe -ErrorAction SilentlyContinue
    if ($p) {
        $cand = Join-Path (Split-Path $p.Source) "pythonw.exe"
        if (Test-Path $cand) { $PyExe = $cand } else { $PyExe = $p.Source }
    }
}
if (-not $PyExe) {
    Write-Error "Khong tim thay Python. Cai Python 3 tu https://python.org (nho tick 'Add Python to PATH')."
    exit 1
}

# Bien dich san bytecode de lan khoi dong dau khong tranh ghi .pyc
& $PyExe -m compileall -q "$ProjectDir\giotot" 2>$null

$Action = New-ScheduledTaskAction -Execute $PyExe `
    -Argument "-m giotot --no-open --port $Port" -WorkingDirectory $ProjectDir
$Trigger = New-ScheduledTaskTrigger -AtLogOn
$Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries -RestartCount 999 `
    -RestartInterval (New-TimeSpan -Minutes 1) `
    -ExecutionTimeLimit (New-TimeSpan -Seconds 0)

Register-ScheduledTask -TaskName "GioTotDichLy" -Action $Action -Trigger $Trigger `
    -Settings $Settings -Description "Gio tot theo Dich ly Viet Nam" -Force | Out-Null
Start-ScheduledTask -TaskName "GioTotDichLy"
Start-Sleep -Seconds 2

Write-Host ""
Write-Host "Da cai dich vu nen (Task Scheduler)."
Write-Host "  Mo app:  http://127.0.0.1:$Port   (nen bookmark lai)"
Write-Host "  Python:  $PyExe"
Write-Host "  Project: $ProjectDir"
Write-Host "  Go:      powershell -ExecutionPolicy Bypass -File deploy\uninstall-service.ps1"
