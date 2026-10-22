$ErrorActionPreference = 'Stop'
$taskRoot = $PSScriptRoot
if ($taskRoot -ne 'C:\IALD\Central de Patentes\Chatgpt') { throw 'Unexpected workbench' }
$modules = @('TowerExpectation','ExpectationProjection','ExpectationBounded','ExpectationBimodule','ExpectationPositive','ExpectationSlice','ExpectationContractGap','LevelExpectationFamily')
foreach ($module in $modules) {
    $binary = Join-Path $taskRoot ($module + '.olean')
    if (Test-Path -LiteralPath $binary) {
        $backup = $binary + '.bak_' + (Get-Date -Format yyyyMMdd_HHmmss_ffff)
        Copy-Item -LiteralPath $binary -Destination $backup
        if ((Get-FileHash -LiteralPath $binary).Hash -ne (Get-FileHash -LiteralPath $backup).Hash) { throw 'Backup mismatch' }
    }
    & (Join-Path $taskRoot 'verify_stage.ps1') -Module $module
    if ($LASTEXITCODE -ne 0) { throw "Lean failed: $module" }
}
& 'C:\Python314\python.exe' -B (Join-Path $taskRoot 'check_scale_obstruction.py')
if ($LASTEXITCODE -ne 0) { throw 'Exact scale check failed' }
