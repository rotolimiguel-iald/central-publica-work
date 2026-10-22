$ErrorActionPreference = 'Stop'
$ialdAppPath = 'C:\IALD\projetos_pyhton\IALD\iald-app'
$ialdBuildLog = 'C:\IALD\Central de Patentes\work\iald_tres_modelos_20260915\android16_build.log'
$env:JAVA_HOME = 'C:\Program Files\Android\Android Studio1\jbr'
$env:PATH = "$env:JAVA_HOME\bin;C:\Program Files\nodejs;$env:PATH"
Push-Location $ialdAppPath
try {
  & 'C:\Program Files\nodejs\node.exe' scripts/validate-release.mjs
  if ($LASTEXITCODE -ne 0) { throw 'Falha na validacao.' }
  & 'C:\Program Files\nodejs\node.exe' node_modules/@capacitor/cli/bin/capacitor sync android
  if ($LASTEXITCODE -ne 0) { throw 'Falha no sync.' }
  Push-Location (Join-Path $ialdAppPath 'android')
  try {
    & .\gradlew.bat assembleRelease bundleRelease --console=plain *> $ialdBuildLog
    if ($LASTEXITCODE -ne 0) { Get-Content -LiteralPath $ialdBuildLog -Tail 30; throw 'Build falhou.' }
    Get-Content -LiteralPath $ialdBuildLog -Tail 5
  } finally { Pop-Location }
} finally { Pop-Location }
