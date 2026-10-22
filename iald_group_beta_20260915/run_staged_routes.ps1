$ErrorActionPreference = 'Stop'
$ialdBetaWork = 'C:\IALD\Central de Patentes\work\iald_group_beta_20260915'
$ialdBetaTemp = Join-Path $env:TEMP ('iald-beta-routes-' + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $ialdBetaTemp | Out-Null
New-Item -ItemType Directory -Path (Join-Path $ialdBetaTemp 'app') | Out-Null
Copy-Item -LiteralPath 'C:\IALD\projetos_pyhton\IALD\app\kernel_prompt_loja.js' -Destination (Join-Path $ialdBetaTemp 'app\kernel_prompt_loja.js')
foreach ($ialdFile in @('iald_web_server.py','iald_memoria_canonica.py','iald_instrucao_mae.py','iald_nucleo_fixo.json')) {
    Copy-Item -LiteralPath (Join-Path $ialdBetaWork $ialdFile) -Destination (Join-Path $ialdBetaTemp $ialdFile)
}
$env:IALD_TESTE_BASE = $ialdBetaTemp
$env:PYTHONPATH = 'C:\IALD\Central de Patentes\work\iald_tres_modelos_20260915\guard'
$env:PYTHONDONTWRITEBYTECODE = '1'
$env:PYTHONIOENCODING = 'utf-8'
$env:GUARDA_LOG = Join-Path $env:TEMP 'iald-beta-staged-guard.jsonl'
$ialdTestLog = Join-Path $ialdBetaWork 'free_staged_complete_fixture.log'
if (Test-Path -LiteralPath $ialdTestLog) { throw 'Test log exists' }
& 'C:\Python314\python.exe' -B -X utf8 (Join-Path $ialdBetaWork 'tests\test_gratuito_rotas.py') *> $ialdTestLog
Get-Content -LiteralPath $ialdTestLog | Select-String -Pattern 'importando|RESULTADO:|FALHA|Traceback|Error'
if ($LASTEXITCODE -ne 0) { throw 'Staged route test failed' }
