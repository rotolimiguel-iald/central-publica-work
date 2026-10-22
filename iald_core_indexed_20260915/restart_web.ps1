$ErrorActionPreference = 'Stop'
$ialdActivationWork = 'C:\IALD\Central de Patentes\work\iald_core_indexed_20260915'
$ialdGate = Get-Content -LiteralPath (Join-Path $ialdActivationWork 'suite_gate.json') -Raw | ConvertFrom-Json
if (-not $ialdGate.passed -or $ialdGate.new_failures -ne 0) { throw 'Regression gate not passed' }
if (Test-Path -LiteralPath (Join-Path $ialdActivationWork 'restart_dispatch.json')) { throw 'Restart already dispatched' }
$ialdWebIds = @(Get-NetTCPConnection -LocalPort 8082 -State Listen | Select-Object -ExpandProperty OwningProcess -Unique)
if ($ialdWebIds.Count -ne 1) { throw 'Web process ambiguous' }
$ialdWebProcess = Get-CimInstance Win32_Process -Filter "ProcessId=$($ialdWebIds[0])"
if ($ialdWebProcess.ParentProcessId -ne 47020 -or $ialdWebProcess.Name -notmatch '^python' -or $ialdWebProcess.CommandLine -notmatch 'iald_web_server.py') { throw 'Unexpected supervisor or process' }
$ialdNativeIds = @(Get-NetTCPConnection -LocalPort 8081 -State Listen | Select-Object -ExpandProperty OwningProcess -Unique)
if ($ialdNativeIds.Count -ne 1 -or $ialdNativeIds[0] -ne 34128) { throw 'Native process changed' }
$ialdOldWeb = $ialdWebIds[0]
Stop-Process -Id $ialdOldWeb -ErrorAction Stop
$ialdReceipt = [pscustomobject]@{at=(Get-Date -Format o);old_web_pid=$ialdOldWeb;supervisor_pid=47020;native_pid=$ialdNativeIds[0];status='WEB_CHILD_STOPPED_ONCE_WAITING_SUPERVISOR'}
$ialdTarget = Join-Path $ialdActivationWork 'restart_dispatch.json'
$ialdData = $ialdReceipt | ConvertTo-Json
[IO.File]::WriteAllText($ialdTarget+'.tmp',$ialdData,[Text.UTF8Encoding]::new($false))
Move-Item -LiteralPath ($ialdTarget+'.tmp') -Destination $ialdTarget
$ialdData
