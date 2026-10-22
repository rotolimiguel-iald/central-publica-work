$ErrorActionPreference='Stop'
$taskRoot='C:\IALD\projetos_pyhton\IALD'
$taskWork='C:\IALD\Central de Patentes\work\iald_jev_default_20261001'
$listener=Get-NetTCPConnection -LocalPort 8082 -State Listen
$child=Get-CimInstance Win32_Process -Filter "ProcessId=$($listener[0].OwningProcess)"
$parent=Get-CimInstance Win32_Process -Filter "ProcessId=$($child.ParentProcessId)"
if ($child.ProcessId -ne 65868 -or $parent.ProcessId -ne 41020) { throw 'Process identity changed; inspect before restarting' }
if ($child.CommandLine -notlike '*C:\IALD\projetos_pyhton\IALD\iald_web_server.py 8082*') { throw 'Unexpected web process' }
if ($parent.CommandLine -notlike '*C:\IALD\projetos_pyhton\IALD\start_iald_web.ps1*' -or $parent.CommandLine -like '*NoSupervise*') { throw 'Supervised restart not guaranteed' }
& 'C:\Python314\python.exe' -B -X utf8 "$taskWork\deploy.py" quiet
if ($LASTEXITCODE -ne 0) { throw 'Active work or incomplete status; no process stopped' }
$before=Invoke-WebRequest -Uri 'http://127.0.0.1:8082/health' -UseBasicParsing -TimeoutSec 8
if ($before.StatusCode -ne 200) { throw 'Initial health check failed' }
Stop-Process -Id $child.ProcessId
$healthy=$false
for ($attempt=0;$attempt -lt 20;$attempt++) {
    Start-Sleep -Seconds 2
    try {
        $reply=Invoke-WebRequest -Uri 'http://127.0.0.1:8082/health' -UseBasicParsing -TimeoutSec 2
        if ($reply.StatusCode -eq 200) {$healthy=$true;break}
    } catch {}
}
if (-not $healthy) {
    $stillParent=Get-Process -Id $parent.ProcessId -ErrorAction SilentlyContinue
    $stillListener=Get-NetTCPConnection -LocalPort 8082 -State Listen -ErrorAction SilentlyContinue
    if (-not $stillParent -and -not $stillListener) {
        Start-Process -FilePath 'powershell.exe' -ArgumentList @('-NoProfile','-ExecutionPolicy','Bypass','-File',"$taskRoot\start_iald_web.ps1") -WindowStyle Hidden
    }
    throw 'Supervised startup still pending; verify health before reporting ready'
}
$after=Get-NetTCPConnection -LocalPort 8082 -State Listen
$record=@{old_pid=$child.ProcessId;new_pid=$after[0].OwningProcess;supervisor=$parent.ProcessId;health=200;timestamp=(Get-Date).ToString('o')}
$record | ConvertTo-Json | Set-Content -LiteralPath "$taskWork\restart.json" -Encoding UTF8
$record | ConvertTo-Json
