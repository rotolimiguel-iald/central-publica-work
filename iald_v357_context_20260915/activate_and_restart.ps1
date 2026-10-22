$ErrorActionPreference='Stop'
$ialdReviewDir='C:\IALD\Central de Patentes\work\iald_v357_context_20260915'
$ialdWebListeners=@(Get-NetTCPConnection -LocalPort 8082 -State Listen)
$ialdWebPid=@($ialdWebListeners.OwningProcess | Select-Object -Unique)
if ($ialdWebPid.Count -ne 1) { throw 'Web listener ambiguous' }
$ialdWebProcess=Get-CimInstance Win32_Process -Filter "ProcessId=$($ialdWebPid[0])"
if ($ialdWebProcess.ParentProcessId -ne 47020 -or $ialdWebProcess.Name -notmatch '^python') { throw 'Unexpected web supervisor' }
$ialdLlamaBefore=@(Get-NetTCPConnection -LocalPort 8081 -State Listen | Select-Object -ExpandProperty OwningProcess -Unique)
if ($ialdLlamaBefore.Count -ne 1 -or $ialdLlamaBefore[0] -ne 34128) { throw 'Native process changed; do not restart' }
& 'C:\Python314\python.exe' -X utf8 (Join-Path $ialdReviewDir 'activate.py')
if ($LASTEXITCODE -ne 0) { throw 'Activation preflight failed; process not stopped' }
Stop-Process -Id $ialdWebPid[0] -ErrorAction Stop
$ialdNewWebPid=$null
$ialdLocalStatus=$null
for ($ialdAttempt=0; $ialdAttempt -lt 40; $ialdAttempt++) {
    Start-Sleep -Milliseconds 500
    try {
        $ialdNewWebPid=@(Get-NetTCPConnection -LocalPort 8082 -State Listen -ErrorAction Stop | Select-Object -ExpandProperty OwningProcess -Unique)
        if ($ialdNewWebPid.Count -eq 1 -and $ialdNewWebPid[0] -ne $ialdWebPid[0]) {
            $ialdLocalHealth=Invoke-WebRequest -UseBasicParsing -Uri 'http://localhost:8082/health' -TimeoutSec 2
            $ialdLocalStatus=[int]$ialdLocalHealth.StatusCode
            if ($ialdLocalStatus -eq 200) { break }
        }
    } catch { }
}
if ($ialdLocalStatus -ne 200) { throw 'New web process not healthy; inspect before retrying' }
$ialdPublicHealth=Invoke-WebRequest -UseBasicParsing -Uri 'https://demo.iald.ia.br/health' -TimeoutSec 15
if ([int]$ialdPublicHealth.StatusCode -ne 200) { throw 'Public health failed' }
$ialdLlamaAfter=@(Get-NetTCPConnection -LocalPort 8081 -State Listen | Select-Object -ExpandProperty OwningProcess -Unique)
if ($ialdLlamaAfter[0] -ne $ialdLlamaBefore[0]) { throw 'Native process changed' }
$ialdReceipt=[pscustomobject]@{at=(Get-Date -Format o);status='ACTIVE_HEALTHY';old_web_pid=$ialdWebPid[0];new_web_pid=$ialdNewWebPid[0];supervisor_pid=47020;native_pid=$ialdLlamaAfter[0];local_health=$ialdLocalStatus;public_health=[int]$ialdPublicHealth.StatusCode}
$ialdReceiptPath=Join-Path $ialdReviewDir 'runtime_live.json'
if (Test-Path -LiteralPath $ialdReceiptPath) { throw 'Receipt already exists' }
$ialdReceiptJson=$ialdReceipt | ConvertTo-Json
[IO.File]::WriteAllText($ialdReceiptPath+'.tmp',$ialdReceiptJson,[Text.UTF8Encoding]::new($false))
Move-Item -LiteralPath ($ialdReceiptPath+'.tmp') -Destination $ialdReceiptPath
$ialdReceiptJson
