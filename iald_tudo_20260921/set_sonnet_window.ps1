$ErrorActionPreference = 'Stop'
$taskEnvPath = 'C:\IALD\projetos_pyhton\IALD\.env'
$taskBefore = [System.IO.File]::ReadAllBytes($taskEnvPath)
$taskText = [System.Text.Encoding]::UTF8.GetString($taskBefore)
if ([regex]::IsMatch($taskText, '(?m)^IALD_CLAUDE_JANELA=')) { throw 'Explicit window already exists; inspect before changing' }
if (-not [regex]::IsMatch($taskText, '(?m)^IALD_CLAUDE_FATOR_TOKENS=1\.77\s*$')) { throw 'Measured factor changed' }
if (-not [regex]::IsMatch($taskText, '(?m)^IALD_CLAUDE_MODELO="claude-sonnet-5"\s*$')) { throw 'Model changed' }
$taskStamp = Get-Date -Format 'yyyyMMdd_HHmmss_ffff'
$taskAcl = Get-Acl -LiteralPath $taskEnvPath
$taskBackup = $taskEnvPath + '.bak_' + $taskStamp
$taskTemporary = $taskEnvPath + '.tmp_' + $taskStamp
foreach ($taskNewPath in @($taskBackup, $taskTemporary)) {
    $taskStream = [System.IO.File]::Open($taskNewPath, [System.IO.FileMode]::CreateNew)
    $taskStream.Close()
    Set-Acl -LiteralPath $taskNewPath -AclObject $taskAcl
}
[System.IO.File]::WriteAllBytes($taskBackup, $taskBefore)
$taskNewline = if ($taskText.Contains("`r`n")) { "`r`n" } else { "`n" }
$taskAddition = [System.Text.Encoding]::UTF8.GetBytes($taskNewline + 'IALD_CLAUDE_JANELA=560000' + $taskNewline)
$taskAfter = [byte[]]::new($taskBefore.Length + $taskAddition.Length)
[System.Buffer]::BlockCopy($taskBefore, 0, $taskAfter, 0, $taskBefore.Length)
[System.Buffer]::BlockCopy($taskAddition, 0, $taskAfter, $taskBefore.Length, $taskAddition.Length)
[System.IO.File]::WriteAllBytes($taskTemporary, $taskAfter)
if ((Get-FileHash -LiteralPath $taskBackup).Hash -ne (Get-FileHash -LiteralPath $taskEnvPath).Hash) { throw 'Concurrent env change or backup mismatch' }
if ([System.IO.File]::ReadAllBytes($taskTemporary).Length -ne $taskAfter.Length) { throw 'Temporary write failed' }
if ((Get-Acl -LiteralPath $taskTemporary).Sddl -ne $taskAcl.Sddl) { throw 'Temporary ACL mismatch' }
Move-Item -LiteralPath $taskTemporary -Destination $taskEnvPath -Force
if ((Get-Acl -LiteralPath $taskEnvPath).Sddl -ne $taskAcl.Sddl) { throw 'Final ACL mismatch' }
Write-Output '{"changed":"IALD_CLAUDE_JANELA","value":560000,"provider_budget_with_factor":991200,"acl_preserved":true,"server_restarted":false}'
