$ErrorActionPreference = 'Stop'
$taskRoot = 'C:\IALD\Central de Patentes\Chatgpt'
$originalKernel = 'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel'
$toolchainBin = 'C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin'
$libraryPaths = @($taskRoot, "$originalKernel\.lake\build\lib\lean")
$libraryPaths += @(Get-ChildItem -LiteralPath "$originalKernel\.lake\packages" -Directory | ForEach-Object { Join-Path $_.FullName '.lake\build\lib\lean' })
$env:LEAN_PATH = $libraryPaths -join ';'
Set-Location -LiteralPath $taskRoot
$proofBefore = (Get-FileHash -LiteralPath 'ClosedModulatorCandidate.lean' -Algorithm SHA256).Hash
& "$toolchainBin\lean.exe" '-o' 'ClosedModulatorCandidate.olean' 'ClosedModulatorCandidate.lean' 2>&1 | Tee-Object -FilePath 'modulator_verification.txt'
$compileExit = $LASTEXITCODE
$proofAfter = (Get-FileHash -LiteralPath 'ClosedModulatorCandidate.lean' -Algorithm SHA256).Hash
if ($proofBefore -ne $proofAfter) { throw 'Source changed during verification' }
[ordered]@{timestamp=(Get-Date -Format o);exit_code=$compileExit;proof_sha256=$proofAfter;source_stable=$true} | ConvertTo-Json | Set-Content -LiteralPath 'verificacao_modulador.json.tmp' -Encoding utf8
Move-Item -LiteralPath 'verificacao_modulador.json.tmp' -Destination 'verificacao_modulador.json' -Force
exit $compileExit
