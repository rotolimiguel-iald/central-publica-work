param([Parameter(Mandatory=$true)][string]$Module)
$ErrorActionPreference = 'Stop'
if ($Module -notmatch '^[A-Za-z][A-Za-z0-9_]*$') { throw 'Invalid module name' }
$taskRoot = 'C:\IALD\Central de Patentes\Chatgpt'
$originalKernel = 'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel'
$toolchainBin = 'C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin'
$libraryPaths = @($taskRoot, "$originalKernel\.lake\build\lib\lean")
$libraryPaths += @(Get-ChildItem -LiteralPath "$originalKernel\.lake\packages" -Directory | ForEach-Object { Join-Path $_.FullName '.lake\build\lib\lean' })
$env:LEAN_PATH = $libraryPaths -join ';'
Set-Location -LiteralPath $taskRoot
$stamp = Get-Date -Format yyyyMMdd_HHmmss
$source = "$Module.lean"
$log = "$Module.$stamp.log"
$proofBefore = (Get-FileHash -LiteralPath $source -Algorithm SHA256).Hash
& "$toolchainBin\lean.exe" '-o' "$Module.olean" $source 2>&1 | Tee-Object -FilePath $log
$compileExit = $LASTEXITCODE
$proofAfter = (Get-FileHash -LiteralPath $source -Algorithm SHA256).Hash
if ($proofBefore -ne $proofAfter) { throw 'Source changed during verification' }
[ordered]@{timestamp=(Get-Date -Format o);module=$Module;exit_code=$compileExit;proof_sha256=$proofAfter;source_stable=$true;log=$log} | ConvertTo-Json | Set-Content -LiteralPath "$Module.$stamp.json.tmp" -Encoding utf8
Move-Item -LiteralPath "$Module.$stamp.json.tmp" -Destination "$Module.$stamp.json"
exit $compileExit
