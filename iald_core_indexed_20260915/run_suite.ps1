$ErrorActionPreference = 'Stop'
$ialdIndexedWork = 'C:\IALD\Central de Patentes\work\iald_core_indexed_20260915'
$env:PYTHONPATH = 'C:\IALD\Central de Patentes\work\iald_tres_modelos_20260915\guard'
$env:PYTHONDONTWRITEBYTECODE = '1'
$env:PYTHONIOENCODING = 'utf-8'
$env:IALD_CREDITO_USO = '0'
$env:GUARDA_LOG = Join-Path $env:TEMP 'iald-indexed-regression-guard.jsonl'
$ialdIndexedLog = Join-Path $ialdIndexedWork 'suite.log'
if (Test-Path -LiteralPath $ialdIndexedLog) { throw 'Result already exists' }
& powershell.exe -NoProfile -ExecutionPolicy Bypass -File 'C:\IALD\projetos_pyhton\IALD\tests\rodar_tudo.ps1' *> $ialdIndexedLog
Get-Content -LiteralPath $ialdIndexedLog | Select-String -Pattern '^XX|RESULTADO:|SUITE\(S\)|TUDO VERDE'
