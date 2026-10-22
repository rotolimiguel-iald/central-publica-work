$ErrorActionPreference = 'Stop'
$ialdWork = 'C:\IALD\Central de Patentes\work\iald_hypotheses_20260915'
$ialdWebIds = @(Get-NetTCPConnection -LocalPort 8082 -State Listen | Select-Object -ExpandProperty OwningProcess -Unique)
if ($ialdWebIds.Count -ne 1) { throw 'Web process ambiguous' }
$ialdWebProcess = Get-CimInstance Win32_Process -Filter "ProcessId=$($ialdWebIds[0])"
if ($ialdWebProcess.ParentProcessId -ne 47020 -or $ialdWebProcess.Name -notmatch '^python') { throw 'Unexpected supervisor' }
$ialdNativeIds = @(Get-NetTCPConnection -LocalPort 8081 -State Listen | Select-Object -ExpandProperty OwningProcess -Unique)
if ($ialdNativeIds.Count -ne 1 -or $ialdNativeIds[0] -ne 34128) { throw 'Native process changed' }
$ialdOldWeb = $ialdWebIds[0]
& 'C:\Python314\python.exe' -B -X utf8 (Join-Path $ialdWork 'activate.py')
if ($LASTEXITCODE -ne 0) { throw 'Activation failed; web not stopped' }
Stop-Process -Id $ialdOldWeb -ErrorAction Stop
$ialdDispatch = [pscustomobject]@{at=(Get-Date -Format o);old_web_pid=$ialdOldWeb;supervisor_pid=47020;native_pid=$ialdNativeIds[0];status='WEB_CHILD_STOPPED_ONCE_WAITING_SUPERVISOR'}
$ialdTarget = Join-Path $ialdWork 'restart_dispatch.json'
if (Test-Path -LiteralPath $ialdTarget) { throw 'Restart receipt exists' }
$ialdData = $ialdDispatch | ConvertTo-Json
[IO.File]::WriteAllText($ialdTarget+'.tmp',$ialdData,[Text.UTF8Encoding]::new($false))
Move-Item -LiteralPath ($ialdTarget+'.tmp') -Destination $ialdTarget
$ialdData
