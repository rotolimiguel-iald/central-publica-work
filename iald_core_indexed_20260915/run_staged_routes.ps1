$ErrorActionPreference = 'Stop'
$ialdIndexedWork = 'C:\IALD\Central de Patentes\work\iald_core_indexed_20260915'
$ialdIndexedTemp = Join-Path $env:TEMP ('iald-indexed-routes-' + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $ialdIndexedTemp | Out-Null
New-Item -ItemType Directory -Path (Join-Path $ialdIndexedTemp 'app') | Out-Null
Copy-Item -LiteralPath 'C:\IALD\projetos_pyhton\IALD\app\kernel_prompt_loja.js' -Destination (Join-Path $ialdIndexedTemp 'app\kernel_prompt_loja.js')
foreach ($ialdFile in @('iald_web_server.py','iald_memoria_canonica.py','iald_instrucao_mae.py','iald_core_indexado.py','iald_nucleo_fixo.json')) {
    Copy-Item -LiteralPath (Join-Path $ialdIndexedWork $ialdFile) -Destination (Join-Path $ialdIndexedTemp $ialdFile)
}
$env:IALD_TESTE_BASE = $ialdIndexedTemp
$env:PYTHONPATH = 'C:\IALD\Central de Patentes\work\iald_tres_modelos_20260915\guard'
$env:PYTHONDONTWRITEBYTECODE = '1'
$env:PYTHONIOENCODING = 'utf-8'
$env:GUARDA_LOG = Join-Path $env:TEMP 'iald-indexed-staged-guard.jsonl'
$ialdRouteLog = Join-Path $ialdIndexedWork 'free_staged_updated_expectations.log'
if (Test-Path -LiteralPath $ialdRouteLog) { throw 'Test log exists' }
& 'C:\Python314\python.exe' -B -X utf8 'C:\IALD\Central de Patentes\work\iald_core_indexed_20260915\tests\test_gratuito_rotas.py' *> $ialdRouteLog
Get-Content -LiteralPath $ialdRouteLog | Select-String -Pattern 'importando|RESULTADO:|FALHA|Traceback|Error'
if ($LASTEXITCODE -ne 0) { throw 'Staged route test failed' }
