# IALD para iOS e Android

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
