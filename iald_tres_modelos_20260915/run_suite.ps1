param([Parameter(Mandatory=$true)][ValidateSet('before','after','final')][string]$Phase)
$ErrorActionPreference = 'Stop'
$ialdOrderWork = 'C:\IALD\Central de Patentes\work\iald_tres_modelos_20260915'
$ialdGuardSource = 'C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\ad4624b2-cfe5-4bdc-b049-f0ab9bdf0aee\scratchpad\sync2\guarda\sitecustomize.py'
$ialdGuardDir = Join-Path $ialdOrderWork 'guard'
if (-not (Test-Path -LiteralPath $ialdGuardDir)) { New-Item -ItemType Directory -Path $ialdGuardDir | Out-Null }
$ialdGuardCopy = Join-Path $ialdGuardDir 'sitecustomize.py'
if (-not (Test-Path -LiteralPath $ialdGuardCopy)) { Copy-Item -LiteralPath $ialdGuardSource -Destination $ialdGuardCopy }
if ((Get-FileHash -LiteralPath $ialdGuardCopy).Hash -ne (Get-FileHash -LiteralPath $ialdGuardSource).Hash) { throw 'Guarda mudou.' }
$env:PYTHONPATH = $ialdGuardDir
$env:PYTHONDONTWRITEBYTECODE = '1'
$env:PYTHONIOENCODING = 'utf-8'
$env:IALD_CREDITO_USO = '0'
$env:GUARDA_LOG = Join-Path $env:TEMP ("iald-models-$Phase-guard.jsonl")
$ialdSuiteLog = Join-Path $ialdOrderWork ("suite_$Phase.log")
if (Test-Path -LiteralPath $ialdSuiteLog) { throw 'Resultado ja existe.' }
& powershell.exe -NoProfile -ExecutionPolicy Bypass -File 'C:\IALD\projetos_pyhton\IALD\tests\rodar_tudo.ps1' *> $ialdSuiteLog
$ialdSuiteExit = $LASTEXITCODE
Get-Content -LiteralPath $ialdSuiteLog | Select-String -Pattern '^XX|RESULTADO:|SUITE\(S\)|TUDO VERDE'
"suite_exit=$ialdSuiteExit"
exit 0
