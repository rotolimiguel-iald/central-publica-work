$ErrorActionPreference = 'Stop'
$taskRoot = 'C:\IALD\Central de Patentes\Chatgpt'
$originalKernel = 'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel'
$toolchainBin = 'C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin'
$libraryPaths = @("$originalKernel\.lake\build\lib\lean")
$libraryPaths += @(Get-ChildItem -LiteralPath "$originalKernel\.lake\packages" -Directory | ForEach-Object { Join-Path $_.FullName '.lake\build\lib\lean' })
$env:LEAN_PATH = $libraryPaths -join ';'
Set-Location -LiteralPath $taskRoot
& "$toolchainBin\lean.exe" '--version'
$proofBefore = (Get-FileHash -LiteralPath 'TomitaClosability.lean' -Algorithm SHA256).Hash
& "$toolchainBin\lean.exe" '-o' 'TomitaClosability.olean' 'TomitaClosability.lean' 2>&1 | Tee-Object -FilePath 'lean_verification.txt'
$compileExit = $LASTEXITCODE
$proofAfter = (Get-FileHash -LiteralPath 'TomitaClosability.lean' -Algorithm SHA256).Hash
if ($proofBefore -ne $proofAfter) { throw 'Source changed during verification' }
$verification = [ordered]@{timestamp=(Get-Date -Format o);exit_code=$compileExit;proof_sha256=$proofAfter;source_stable=$true;mode='Lean direct; existing compiled imports read only; no full dependency rebuild'}
$verification | ConvertTo-Json | Set-Content -LiteralPath 'verificacao_lean.json.tmp' -Encoding utf8
Move-Item -LiteralPath 'verificacao_lean.json.tmp' -Destination 'verificacao_lean.json' -Force
exit $compileExit
