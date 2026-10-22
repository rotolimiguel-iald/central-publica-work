from pathlib import Path
from datetime import datetime
import json
import plistlib
import shutil

ROOT = Path(r'C:\IALD\projetos_pyhton\IALD\iald-app')
STAMP = datetime.now().strftime('%Y%m%d_%H%M%S')

def write(relative, content):
    path = ROOT / relative
    data = content.encode('utf-8') if isinstance(content, str) else content
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        old = path.read_bytes()
        if old == data:
            return
        backup = ROOT / ('_backups_' + STAMP) / relative
        backup.parent.mkdir(parents=True, exist_ok=True)
        backup.write_bytes(old)
        assert backup.read_bytes() == old
    temp = path.with_name(path.name + '.tmp_release')
    temp.write_bytes(data)
    assert temp.stat().st_size == len(data) and data
    temp.replace(path)
    assert path.read_bytes() == data
    print(relative)

write('.gitignore', '''# Local credentials, operator notes and previous submissions
.env
.env.*
!.env.example
*.jks
*.keystore
*.p12
*.p8
*.mobileprovision
keystore.properties
HANDOFF*.md
GUIA_DISTRIBUICAO_APPSTORE.md
IOS_entregas_marco_2026/
_backups_*/
*.bak_*
*.tmp_release
node_modules/
.idea/
.DS_Store
Thumbs.db
android/local.properties
android/.gradle/
android/build/
android/app/build/
android/captures/
ios/App/build/
ios/App/Pods/
ios/App/DerivedData/
build/
*.apk
*.aab
*.ipa
*.xcarchive
*.xcresult
Screenshot/
*.zip
App Store Connect.pdf
Simulator Screenshot*.png
*.log
# Legacy root splash; www/index.html is the embedded entry point.
/index.html
''')
write('.gitattributes', '* text=auto\n*.sh text eol=lf\n*.gradle text eol=lf\n*.swift text eol=lf\n*.png binary\n*.jar binary\n')
pkg = json.loads((ROOT / 'package.json').read_text(encoding='utf-8-sig'))
pkg['version'] = '4.1.0'
pkg['engines'] = {'node': '>=22'}
for name in ['core', 'cli', 'ios', 'android']:
    pkg['dependencies']['@capacitor/' + name] = '8.5.2'
for name in ['splash-screen', 'status-bar']:
    pkg['dependencies']['@capacitor/' + name] = '8.0.1'
pkg['dependencies']['@capacitor-community/apple-sign-in'] = '7.1.0'
pkg['scripts'].update({'validate': 'node scripts/validate-release.mjs',
                       'sync': 'npm run validate && cap sync',
                       'sync:ios': 'npm run validate && cap sync ios',
                       'sync:android': 'npm run validate && cap sync android'})
write('package.json', json.dumps(pkg, ensure_ascii=False, indent=2) + '\n')
config = json.loads((ROOT / 'capacitor.config.json').read_text(encoding='utf-8-sig'))
config['ios']['scheme'] = 'App'
# External sites must not inherit the native bridge.
config['server'].pop('allowNavigation', None)
write('capacitor.config.json', json.dumps(config, ensure_ascii=False, indent=2) + '\n')
gradle = (ROOT / 'android/app/build.gradle').read_text(encoding='utf-8-sig')
gradle = gradle.replace('versionCode 1\n', 'versionCode 11\n').replace('versionName "1.0"', 'versionName "4.1"')
gradle = gradle.replace("android {", '''def signingValues = new Properties()
def signingFile = rootProject.file('keystore.properties')
if (signingFile.exists()) {
    signingFile.withInputStream { signingValues.load(it) }
}
def signingValue = { name -> System.getenv('IALD_ANDROID_' + name) ?: signingValues.getProperty(name) }
def releaseRequested = gradle.startParameter.taskNames.any { it.toLowerCase().contains('release') }
if (releaseRequested && ['STORE_FILE', 'STORE_PASSWORD', 'KEY_ALIAS', 'KEY_PASSWORD'].any { !signingValue(it) }) {
    throw new GradleException('Missing Android upload signing configuration. See README.md.')
}

android {''', 1)
gradle = gradle.replace('    buildTypes {', '''    signingConfigs {
        release {
            if (signingValue('STORE_FILE')) {
                storeFile file(signingValue('STORE_FILE'))
                storePassword signingValue('STORE_PASSWORD')
                keyAlias signingValue('KEY_ALIAS')
                keyPassword signingValue('KEY_PASSWORD')
            }
        }
    }
    buildTypes {''', 1)
gradle = gradle.replace('        release {\n            minifyEnabled', '        release {\n            signingConfig signingConfigs.release\n            minifyEnabled', 1)
write('android/app/build.gradle', gradle)
manifest = (ROOT / 'android/app/src/main/AndroidManifest.xml').read_text(encoding='utf-8')
write('android/app/src/main/AndroidManifest.xml', manifest.replace('android:allowBackup="true"', 'android:allowBackup="false"'))
pl = plistlib.loads((ROOT / 'ios/App/App/Info.plist').read_bytes())
pl.pop('UIRequiredDeviceCapabilities', None)
pl['CFBundleDevelopmentRegion'] = 'pt_BR'
write('ios/App/App/Info.plist', plistlib.dumps(pl, sort_keys=False))
write('ios/App/App.xcodeproj/xcshareddata/xcschemes/App.xcscheme', '''<?xml version="1.0" encoding="UTF-8"?>
<Scheme LastUpgradeVersion="2600" version="1.3">
  <BuildAction parallelizeBuildables="YES" buildImplicitDependencies="YES">
    <BuildActionEntries>
      <BuildActionEntry buildForTesting="YES" buildForRunning="YES" buildForProfiling="YES" buildForArchiving="YES" buildForAnalyzing="YES">
        <BuildableReference BuildableIdentifier="primary" BlueprintIdentifier="504EC3031FED79650016851F" BuildableName="App.app" BlueprintName="App" ReferencedContainer="container:App.xcodeproj"/>
      </BuildActionEntry>
    </BuildActionEntries>
  </BuildAction>
  <TestAction buildConfiguration="Debug" selectedDebuggerIdentifier="Xcode.DebuggerFoundation.Debugger.LLDB" selectedLauncherIdentifier="Xcode.IDEFoundation.Launcher.LLDB" shouldUseLaunchSchemeArgsEnv="YES"/>
  <LaunchAction buildConfiguration="Debug" selectedDebuggerIdentifier="Xcode.DebuggerFoundation.Debugger.LLDB" selectedLauncherIdentifier="Xcode.IDEFoundation.Launcher.LLDB" launchStyle="0" useCustomWorkingDirectory="NO" ignoresPersistentStateOnLaunch="NO" debugDocumentVersioning="YES" allowLocationSimulation="YES">
    <BuildableProductRunnable runnableDebuggingMode="0">
      <BuildableReference BuildableIdentifier="primary" BlueprintIdentifier="504EC3031FED79650016851F" BuildableName="App.app" BlueprintName="App" ReferencedContainer="container:App.xcodeproj"/>
    </BuildableProductRunnable>
  </LaunchAction>
  <ProfileAction buildConfiguration="Release" shouldUseLaunchSchemeArgsEnv="YES" savedToolIdentifier="" useCustomWorkingDirectory="NO" debugDocumentVersioning="YES">
    <BuildableProductRunnable runnableDebuggingMode="0">
      <BuildableReference BuildableIdentifier="primary" BlueprintIdentifier="504EC3031FED79650016851F" BuildableName="App.app" BlueprintName="App" ReferencedContainer="container:App.xcodeproj"/>
    </BuildableProductRunnable>
  </ProfileAction>
  <AnalyzeAction buildConfiguration="Debug"/>
  <ArchiveAction buildConfiguration="Release" revealArchiveInOrganizer="YES"/>
</Scheme>
''')
write('ios/App/ci_scripts/ci_post_clone.sh', '''#!/bin/sh
set -eu
cd "${CI_PRIMARY_REPOSITORY_PATH:-$(cd "$(dirname "$0")/../../.." && pwd)}"
if ! command -v node >/dev/null 2>&1; then
  brew install node@24
  export PATH="$(brew --prefix node@24)/bin:$PATH"
fi
node --version
npm ci --no-audit --no-fund
npm run sync:ios
''')
write('scripts/validate-release.mjs', r'''import { readFileSync, existsSync, readdirSync } from 'node:fs';
import { resolve, join } from 'node:path';
import { fileURLToPath } from 'node:url';
const root = resolve(fileURLToPath(new URL('..', import.meta.url)));
const config = JSON.parse(readFileSync(join(root, 'capacitor.config.json'), 'utf8'));
function check(ok, message) { if (!ok) throw new Error(message); }
check(config.appId === 'br.ia.IALD', 'Unexpected bundle identifier');
check(!config.server?.url, 'Release must use embedded assets');
for (const name of ['index.html', 'iald.js', 'iald.css', 'kernel_prompt.js', 'kernel_prompt_loja.js', 'icon.png']) {
  check(existsSync(join(root, config.webDir, name)), `Missing embedded asset: ${name}`);
}
const blocked = [/Licenciamento:/i, /Sovereign/i, /Efficiency 1\.2/i, /ROI R\$/i,
  /-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----/, /\bAIza[0-9A-Za-z_-]{30,}/,
  /\bgh[pousr]_[0-9A-Za-z]{20,}/];
function scan(dir) {
  for (const item of readdirSync(dir, { withFileTypes: true })) {
    const path = join(dir, item.name);
    if (item.isDirectory()) scan(path);
    else if (/\.(js|html|css|json)$/.test(item.name)) {
      const text = readFileSync(path, 'utf8');
      check(!blocked.some(pattern => pattern.test(text)), `Restricted content in ${path}`);
    }
  }
}
scan(join(root, config.webDir));
console.log('Release validation passed: embedded assets, app ID and content guard.');
''')
write('.github/workflows/ios-build.yml', '''name: Validate iOS archive
on:
  workflow_dispatch:
permissions:
  contents: read
jobs:
  archive:
    runs-on: macos-26
    timeout-minutes: 20
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '24'
          cache: npm
      - run: npm ci --no-audit --no-fund
      - run: npm run sync:ios
      - name: Compile unsigned iOS archive
        run: |
          set -o pipefail
          xcodebuild -version
          xcodebuild -project ios/App/App.xcodeproj -scheme App -configuration Release -destination 'generic/platform=iOS' -archivePath build/IALD.xcarchive -resultBundlePath build/IALD.xcresult CODE_SIGNING_ALLOWED=NO archive 2>&1 | tee build-ios.log
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: ios-build-log
          path: build-ios.log
          retention-days: 7
''')
write('README.md', '''# IALD para iOS e Android

Projeto Capacitor, pacote `br.ia.IALD`, versão 4.1 (11). O app conversa com o servidor HTTPS da IALD.

## Compilar

Node 22 ou posterior, JDK 21 / Android SDK 36 para Android, macOS e Xcode compatível com Capacitor 8 para iOS.

```sh
npm ci
npm run sync
```

A interface compartilhada é mantida na pasta irmã `app/` da máquina de desenvolvimento. Execute `sincronizar_app.ps1` ali antes de versionar mudanças. O repositório contém um instantâneo validado em `www/`, suficiente para compilar em uma máquina limpa. As dependências Swift locais estão em `node_modules`: `npm ci` é obrigatório mesmo com os recursos web versionados.

## Apple

Abra `ios/App/App.xcodeproj`, esquema compartilhado `App`, Team `48DLBH89QY`, assinatura automática. O script `ios/App/ci_scripts/ci_post_clone.sh` prepara as dependências no Xcode Cloud. Configure uma ação Archive e distribuição para TestFlight interno. O onboarding inicial do Xcode Cloud pode exigir Xcode em um Mac; verifique o estado da conta no App Store Connect.

O workflow manual `Validate iOS archive` compila sem assinatura no GitHub Actions. Essa verificação não produz um IPA instalável nem envia ao TestFlight. A assinatura e o envio exigem as credenciais de distribuição da Apple ou Xcode Cloud configurado.

## Android

Use uma chave de upload guardada fora deste repositório. Configure as variáveis `IALD_ANDROID_STORE_FILE`, `IALD_ANDROID_STORE_PASSWORD`, `IALD_ANDROID_KEY_ALIAS`, `IALD_ANDROID_KEY_PASSWORD`; alternativamente use `android/keystore.properties` local (ignorado). Nunca envie senhas ou chaves ao Git.

```sh
cd android
./gradlew :app:bundleRelease :app:assembleRelease
```

O AAB assinado sai em `android/app/build/outputs/bundle/release/app-release.aab`. Envie primeiro ao teste interno do Google Play. O APK assinado é para instalação direta; após aderir ao Play App Signing, a assinatura da loja pode diferir da chave de upload.

Com Play App Signing, uma chave de upload perdida pode ser redefinida pelo Google. Preserve o keystore e seu backup para evitar interrupções.

## Antes da revisão

Verificar entrada Apple no iPhone e iPad, entrada Android, streaming, saída/expiração de sessão, política de privacidade, exclusão de conta e declarações de dados. TGL Coin é um experimento de créditos fictícios sem valor comercial; confirmar que não compra, transfere ou desbloqueia recursos na distribuição das lojas. Não enviar respostas de revisão que afirmem testes ainda não executados.
''')
