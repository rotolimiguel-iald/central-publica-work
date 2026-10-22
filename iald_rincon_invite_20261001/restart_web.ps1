$ErrorActionPreference = 'Stop'
$taskRoot = 'C:\IALD\Central de Patentes\work\iald_rincon_invite_20261001'
& 'C:\Python314\python.exe' -B -X utf8 "$taskRoot\provision.py" quiet
if ($LASTEXITCODE -ne 0) { throw 'Servidor ocupado' }
$taskListener = Get-NetTCPConnection -LocalPort 8082 -State Listen | Select-Object -First 1
$taskProcess = Get-CimInstance Win32_Process -Filter "ProcessId=$($taskListener.OwningProcess)"
$taskParent = Get-CimInstance Win32_Process -Filter "ProcessId=$($taskProcess.ParentProcessId)"
if ($taskProcess.ProcessId -ne 139424 -or $taskProcess.CommandLine -notlike '*\IALD\iald_web_server.py 8082*' -or $taskParent.ProcessId -ne 41020 -or $taskParent.CommandLine -notlike '*\IALD\start_iald_web.ps1*') { throw 'Identidade do processo mudou' }
Stop-Process -Id $taskProcess.ProcessId
$taskReady = $false
for ($i=0; $i -lt 20; $i++) {
 Start-Sleep -Seconds 2
 try {
  $taskHealth = Invoke-WebRequest -Uri 'http://127.0.0.1:8082/health' -TimeoutSec 2 -UseBasicParsing
  if ($taskHealth.StatusCode -eq 200) { $taskReady = $true; break }
 } catch {}
}
if (-not $taskReady) { throw 'Health indisponivel; verificar supervisor' }
$taskNew = Get-NetTCPConnection -LocalPort 8082 -State Listen | Select-Object -First 1
if ($taskNew.OwningProcess -eq $taskProcess.ProcessId) { throw 'Processo antigo ainda ativo' }
@{old_pid=$taskProcess.ProcessId;new_pid=$taskNew.OwningProcess;health=200;supervisor=$taskParent.ProcessId;at=(Get-Date).ToString('o')} | ConvertTo-Json | Set-Content -LiteralPath "$taskRoot\restart.json" -Encoding utf8
Get-Content -LiteralPath "$taskRoot\restart.json"
