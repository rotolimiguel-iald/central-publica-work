$ErrorActionPreference = 'Stop'
$taskWork = $PSScriptRoot
$taskRoot = 'C:\IALD\projetos_pyhton\IALD'
$taskReceipt = Join-Path $taskWork 'APP_RESTART.json'
if (Test-Path -LiteralPath $taskReceipt) { throw 'Existing restart receipt: inspect instead of repeating.' }
$taskDeployment = Get-Content -LiteralPath (Join-Path $taskWork 'APP_DEPLOYMENT.json') -Raw | ConvertFrom-Json
if ($taskDeployment.status -ne 'INSTALLED_RESTART_REQUIRED') { throw 'Installation is not ready.' }
Push-Location -LiteralPath 'C:\IALD\Central de Patentes\work\iald_monthly_wallet_20261007'
try {
    & 'C:\Python314\python.exe' -B -X utf8 -c 'from transaction import quiet; quiet()'
    if ($LASTEXITCODE -ne 0) { throw 'Active work or unreadable ledger; no restart.' }
} finally { Pop-Location }
$taskWebPath = Join-Path $taskRoot 'iald_web_server.py'
$taskSupervisorPath = Join-Path $taskRoot 'start_iald_web.ps1'
$taskWeb = @(Get-CimInstance Win32_Process -Filter "name = 'python.exe'" | Where-Object {
    $_.CommandLine -match [regex]::Escape($taskWebPath)
})
if ($taskWeb.Count -ne 1) { throw 'Expected exactly one web process.' }
$taskParent = Get-CimInstance Win32_Process -Filter "ProcessId = $($taskWeb[0].ParentProcessId)"
if ($taskParent.CommandLine -notmatch [regex]::Escape($taskSupervisorPath)) { throw 'Supervisor identity mismatch.' }
$taskListen = @(Get-NetTCPConnection -LocalPort 8082 -State Listen)
if ($taskListen.Count -ne 1 -or $taskListen[0].OwningProcess -ne $taskWeb[0].ProcessId) { throw 'Listener identity mismatch.' }
$taskRecord = [ordered]@{
    status = 'STOP_REQUESTED'
    utc = [DateTime]::UtcNow.ToString('o')
    old_web_pid = $taskWeb[0].ProcessId
    supervisor_pid = $taskParent.ProcessId
    new_web_pid = $null
    restart_scope = 'Only web child; existing supervisor remains running'
}
function Save-TaskReceipt {
    if (Test-Path -LiteralPath $taskReceipt) {
        $taskBackup = $taskReceipt + '.bak_' + [DateTime]::UtcNow.ToString('yyyyMMdd_HHmmss_fffffff')
        [IO.File]::WriteAllBytes($taskBackup, [IO.File]::ReadAllBytes($taskReceipt))
    }
    $taskTemp = $taskReceipt + '.tmp'
    $taskBytes = [Text.UTF8Encoding]::new($false).GetBytes(($taskRecord | ConvertTo-Json -Depth 6))
    [IO.File]::WriteAllBytes($taskTemp, $taskBytes)
    if ((Get-Item -LiteralPath $taskTemp).Length -ne $taskBytes.Length) { throw 'Receipt size mismatch.' }
    Move-Item -LiteralPath $taskTemp -Destination $taskReceipt -Force
}
Save-TaskReceipt
Stop-Process -Id $taskWeb[0].ProcessId -ErrorAction Stop
Start-Sleep -Seconds 6
for ($taskAttempt = 0; $taskAttempt -lt 12; $taskAttempt++) {
    $taskNew = @(Get-CimInstance Win32_Process -Filter "name = 'python.exe'" | Where-Object {
        $_.ParentProcessId -eq $taskParent.ProcessId -and
        $_.CommandLine -match [regex]::Escape($taskWebPath) -and
        $_.ProcessId -ne $taskWeb[0].ProcessId
    })
    if ($taskNew.Count -eq 1) {
        try {
            $taskResponse = Invoke-WebRequest -Uri 'http://127.0.0.1:8082/login' -TimeoutSec 2 -UseBasicParsing
            $taskReadyListen = @(Get-NetTCPConnection -LocalPort 8082 -State Listen)
            $taskReadyProcess = Get-CimInstance Win32_Process -Filter "ProcessId = $($taskNew[0].ProcessId)"
            if ($taskResponse.StatusCode -eq 200 -and $taskReadyListen.Count -eq 1 -and
                $taskReadyListen[0].OwningProcess -eq $taskNew[0].ProcessId -and
                $taskReadyProcess.ParentProcessId -eq $taskParent.ProcessId -and
                $taskReadyProcess.CommandLine -match [regex]::Escape($taskWebPath)) {
                $taskRecord.status = 'PASS'
                $taskRecord.new_web_pid = $taskNew[0].ProcessId
                $taskRecord.utc = [DateTime]::UtcNow.ToString('o')
                Save-TaskReceipt
                $taskRecord | ConvertTo-Json
                exit 0
            }
        } catch { }
    }
    Start-Sleep -Seconds 2
}
$taskRecord.status = 'RESTART_NOT_VERIFIED'
Save-TaskReceipt
throw 'Web restart not verified; inspect supervisor without stopping other services.'
