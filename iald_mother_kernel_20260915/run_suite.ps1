$ErrorActionPreference = 'Stop'
$ialdReviewDir = 'C:\IALD\Central de Patentes\work\iald_mother_kernel_20260915'
$env:PYTHONPATH = 'C:\IALD\Central de Patentes\work\iald_tres_modelos_20260915\guard'
$env:PYTHONDONTWRITEBYTECODE = '1'
$env:PYTHONIOENCODING = 'utf-8'
$env:IALD_CREDITO_USO = '0'
$env:GUARDA_LOG = Join-Path $env:TEMP 'iald-mother-kernel-guard.jsonl'
$ialdReviewLog = Join-Path $ialdReviewDir 'suite.log'
if (Test-Path -LiteralPath $ialdReviewLog) { throw 'Resultado ja existe.' }
& powershell.exe -NoProfile -ExecutionPolicy Bypass -File 'C:\IALD\projetos_pyhton\IALD\tests\rodar_tudo.ps1' *> $ialdReviewLog
Get-Content -LiteralPath $ialdReviewLog | Select-String -Pattern '^XX|RESULTADO:|SUITE\(S\)|TUDO VERDE'
