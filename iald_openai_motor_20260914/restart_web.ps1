$ErrorActionPreference = 'Stop'
$taskRoot = 'C:\IALD\Central de Patentes\work\iald_openai_motor_20260914'
$serverRoot = 'C:\IALD\projetos_pyhton\IALD'
$receiptFile = Get-ChildItem -LiteralPath $taskRoot -Filter 'installation_*.json' | Sort-Object LastWriteTime -Descending | Select-Object -First 1
if (-not $receiptFile) { throw 'Installation receipt missing' }
$receipt = Get-Content -LiteralPath $receiptFile.FullName -Raw | ConvertFrom-Json
foreach ($property in $receipt.files.PSObject.Properties) {
    $actual = (Get-FileHash -LiteralPath (Join-Path $serverRoot $property.Name) -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($actual -ne $property.Value) { throw ('Concurrent edit before restart: ' + $property.Name) }
}
$expectedWebPid = 44296
$webProcess = Get-CimInstance Win32_Process -Filter "ProcessId=$expectedWebPid"
if (-not $webProcess -or $webProcess.ExecutablePath -ne 'C:\Python314\python.exe' -or $webProcess.CommandLine -notmatch 'iald_web_server.py' -or $webProcess.CreationDate.ToString('yyyy-MM-ddTHH:mm:ss') -ne '2026-09-13T18:41:17') { throw 'Web process identity differs' }
$listener = @(Get-NetTCPConnection -State Listen -LocalPort 8082)
if ($listener.Count -ne 1 -or $listener[0].OwningProcess -ne $expectedWebPid) { throw 'Unexpected listener on 8082' }
$nativeBefore = @(Get-NetTCPConnection -State Listen -LocalPort 8081)[0].OwningProcess
$logDir = Join-Path $serverRoot '.iald_runtime\logs'
New-Item -ItemType Directory -Path $logDir -Force | Out-Null
$taskAccount = (& whoami).Trim()
& icacls $logDir /inheritance:r /grant:r "${taskAccount}:(OI)(CI)F" 'SYSTEM:(OI)(CI)F' | Out-Null
if ($LASTEXITCODE -ne 0) { throw 'Could not protect log directory' }
$stamp = Get-Date -Format 'yyyyMMdd_HHmmss'
Stop-Process -Id $expectedWebPid
Wait-Process -Id $expectedWebPid -ErrorAction SilentlyContinue -Timeout 15
$started = Start-Process -FilePath 'C:\Python314\python.exe' -ArgumentList @('-u', 'iald_web_server.py') -WorkingDirectory $serverRoot -WindowStyle Hidden -RedirectStandardOutput (Join-Path $logDir "web_$stamp.stdout.log") -RedirectStandardError (Join-Path $logDir "web_$stamp.stderr.log") -PassThru
$result = [ordered]@{started_at=(Get-Date).ToString('o'); old_pid=$expectedWebPid; new_pid=$started.Id; native_pid_before=$nativeBefore; installation=$receiptFile.Name; log_directory=$logDir; status='STARTED_AWAITING_HEALTH'}
$result | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $taskRoot "restart_$stamp.json") -Encoding UTF8
$result | ConvertTo-Json -Compress
