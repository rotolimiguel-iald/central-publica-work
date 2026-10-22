$ErrorActionPreference = 'Stop'
$ialdBetaWork = 'C:\IALD\Central de Patentes\work\iald_group_beta_20260915'
$env:IALD_TESTE_BASE = $ialdBetaWork
$env:PYTHONPATH = 'C:\IALD\Central de Patentes\work\iald_tres_modelos_20260915\guard'
$env:PYTHONDONTWRITEBYTECODE = '1'
$env:PYTHONIOENCODING = 'utf-8'
$env:GUARDA_LOG = Join-Path $env:TEMP 'iald-beta-route-guard.jsonl'
foreach ($ialdTestName in @('test_gratuito_rotas.py','test_motor_rotas.py')) {
    $ialdTestLog = Join-Path $ialdBetaWork ($ialdTestName + '.log')
    if (Test-Path -LiteralPath $ialdTestLog) { throw 'Test log exists' }
    & 'C:\Python314\python.exe' -B -X utf8 (Join-Path $ialdBetaWork ('tests\' + $ialdTestName)) *> $ialdTestLog
    Get-Content -LiteralPath $ialdTestLog | Select-String -Pattern 'RESULTADO:|FALHA|Traceback|Error|GUARD'
}
