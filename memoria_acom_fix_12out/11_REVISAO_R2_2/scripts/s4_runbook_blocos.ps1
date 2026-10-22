# Revisor c1 R2.2: extrai os blocos powershell do RUNBOOK_OPERADOR.md, parseia (sem executar) e confere caminhos citados.
$rb = 'C:\IALD\Central de Patentes\work\memoria_acom_fix_12out\9_R2_2\RUNBOOK_OPERADOR.md'
$txt = [IO.File]::ReadAllText($rb, [Text.Encoding]::UTF8)
$ms = [regex]::Matches($txt, '(?ms)^\s*```powershell\r?\n(.*?)^\s*```')
"blocos powershell: $($ms.Count)"
$i = 0
foreach ($m in $ms) {
    $i++
    $code = $m.Groups[1].Value
    $errs = $null; $toks = $null
    [void][System.Management.Automation.Language.Parser]::ParseInput($code, [ref]$toks, [ref]$errs)
    $first = ($code -split "`n")[0].Trim()
    if (-not $first) { $first = ($code -split "`n")[1].Trim() }
    "bloco ${i}: erros de sintaxe = $($errs.Count) | $($first.Substring(0, [Math]::Min(100, $first.Length)))"
    foreach ($e in $errs) { "   ERRO: $($e.Message) @ linha $($e.Extent.StartLineNumber)" }
}
# caminhos entre aspas citados no runbook (apenas os que nao tem <...>)
$caminhos = [regex]::Matches($txt, '"([A-Z]:\\[^"<>]+)"') | ForEach-Object { $_.Groups[1].Value } | Sort-Object -Unique
foreach ($c in $caminhos) { "{0,-6} {1}" -f (Test-Path -LiteralPath $c), $c }
$outros = [regex]::Matches($txt, '(?<![\w"])(C:\\IALD\\MEMORIA_IALD\\[\w\.]+\.py)') | ForEach-Object { $_.Groups[1].Value } | Sort-Object -Unique
"-- instalados em producao (so existencia; o mover so passa a existir apos a implantacao):"
foreach ($c in $outros) { "{0,-6} {1}" -f (Test-Path -LiteralPath $c), $c }
"-- scripts do app (so existencia)"
foreach ($n in 'stop_iald_web.ps1', 'start_iald_web.ps1') { "{0,-6} {1}" -f (Test-Path -LiteralPath ('C:\IALD\projetos_pyhton\IALD\' + $n)), $n }
"-- tarefa agendada (so leitura do estado)"
Get-ScheduledTask -TaskName 'IALD Web Server' -ErrorAction SilentlyContinue | Select-Object TaskName, State | Format-List | Out-String
"-- python"
(Get-Command python).Source
python --version
