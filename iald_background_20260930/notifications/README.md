# Sidecar de notificações — entrega em staging

[REAL] Auditoria independente do núcleo de jobs, feita sobre `C:\IALD\projetos_pyhton\IALD\iald-app`, com implementação nesta pasta e integração autorizada em `../client`. Produção, `iald_chat_jobs.py`, autenticação e servidor principal não foram editados. A cópia final do módulo push está também em `../server/iald_chat_push.py`. Nenhuma instalação, emissão de chave, chamada APNs/FCM ou chamada paga foi feita. A revisão externa deste sidecar e testes físicos ainda estão pendentes; os próprios testes não constituem aprovação independente do código que os acompanha.

Arquivos de integração: `iald_chat_push.py`, `client/native-notifications.mjs`, `client/registration.mjs`, [CONTRACT.md](CONTRACT.md) e [CONFIGURATION.md](CONFIGURATION.md). O pai faz wiring do servidor, cofre DPAPI e auth/session. A UI foi integrada após a cessão de `../client` por Ampere: `notification_settings.js` e `native_notifications_integration.js` são incorporados por `build_client.py`. Único asset público: `app/iald.js`. O controle nativo permanece desabilitado enquanto `/api/native-push/status` devolver ios/android false; nenhum prompt ou registro de token ocorre nesse estado.

| Patch separado | Conteúdo / gate |
|---|---|
| `01-dependency.patch` | Proposta `@capacitor/push-notifications` 8.1.2, core/ios/android continuam 8.5.2. **Não aplicado nem instalado.** |
| `02-capacitor-config.patch` | Apresentação de alerta em primeiro plano. Aplicar junto à integração autorizada do plugin. |
| `03-ios-after-approval.patch` | Callbacks APNs, capability do projeto, entitlement por Debug/Release. **Aguardar autorização Apple/perfis.** |
| `04-android-opt-in.patch` | Ícone, canal, permissão, auto-init desligado e guarda nativa. Sem Firebase, build padrão mantém push desabilitado. |

`proposed/` contém cópias para revisão; `patch-manifest.json` fixa hashes lidos das fontes e derivados. `build_patches.py` somente lê o app e gera arquivos dentro do staging; recusa sobrescrever um baseline existente. Os patches não substituem `package-lock.json`. [INPUT — coordenação] O pai verificou a versão 8.1.2 no npm e gerou `../native-dependencies/package-lock.json` com `--package-lock-only`, sem scripts. Após autorização da etapa nativa, usar o lock preparado e executar `cap sync` para regenerar SPM/Gradle. Nenhuma instalação ou sync foi executado por este sidecar. Versão consultada também no [package oficial](https://github.com/ionic-team/capacitor-plugins/blob/main/push-notifications/package.json).

[REAL — fontes locais] O app auditado declara Capacitor 8.5.2; não possui plugin push. Bundle/application ID `br.ia.IALD`; namespace Java `br.ia.iald.app` preservado. iOS 4.1/build 25, Android 4.1/versionCode 22. AppDelegate encaminha OAuth/scene ao Capacitor; patch preserva esses caminhos. Entitlements existentes só incluem Sign in with Apple. MainActivity era básica. Gradle tinha integração Google Services 4.4.4 opcional, sem configuração Firebase presente. A varredura de nomes/metadados do app encontrou `android/keystore.properties`, sem ler conteúdo; não encontrou `.p8`, `.p12`, configuração Google Services ou conta de serviço FCM no escopo auditado. Não se infere ausência no CI/cofres externos.

[REAL — release] `ci_post_clone.sh` usa `npm ci` + `sync:ios`; workflows GitHub fazem resolução Swift e archive iOS sem assinatura. Schemes App e IALD apontam ao mesmo target; a diferença de nomes não é um bloqueio medido. Archive sem assinatura não valida APNs/provisionamento. Não foram executados pipelines, compilação Android/Xcode ou consultas a distribuição nesta entrega.

[INPUT — coordenação] App ID Apple estava com push desabilitado. O pai chegou à confirmação, bloqueada por revisão automática por invalidar perfis; autorização específica pendente. Nenhuma tentativa de contornar. Pai informou projeto Google criado (`iald-app-notificacoes`, número 288651677723), mas ativação Firebase bloqueada na confirmação de IAM/vínculo de faturamento, pendente de autorização específica. Estes estados de console são relatos da coordenação, não medições desta auditoria. Não criar projeto substituto.

| Plataforma | Estado desta entrega | Bloqueio para push real |
|---|---|---|
| Web | `../client/iald.js` pronto em staging, sem Web Push | Publicação pelo pai; nada implantado aqui |
| iOS interno | Patch pronto, não compilado/distribuído | Autorização capability, perfil assinado, chave APNs e runtime, nova build e teste físico |
| iOS externo | Igual; nenhum grupo TestFlight alterado | Além dos anteriores, distribuição externa e review quando aplicáveis |
| Android | Patch condicionado, desabilitado por padrão | Finalizar Firebase, obter `google-services.json`, autorizar sender FCM, build habilitada e aparelho com Google Play services |

O alerta nativo visível é apropriado porque o sistema pode suspendê-lo depois de sair. A geração deve permanecer no backend. A [API oficial Capacitor](https://capacitorjs.com/docs/apis/push-notifications) integra APNs no iOS e FCM no Android; não implementa silent push iOS. No Android, notification+data permite alerta pelo sistema e entrega dos IDs ao tocar, conforme [recebimento FCM](https://firebase.google.com/docs/cloud-messaging/android/receive-messages). [FCM Android](https://firebase.google.com/docs/cloud-messaging/android/get-started) documenta opt-in/auto-init; o patch não migra para APIs novas de Firebase Installation ID, preservando a integração token do plugin 8 auditado.

O backend usa [APNs com JWT ES256/HTTP2](https://developer.apple.com/library/archive/documentation/NetworkingInternet/Conceptual/RemoteNotificationsPG/CommunicatingwithAPNs.html) e [FCM HTTP v1](https://firebase.google.com/docs/cloud-messaging/send/v1-api), por dependências/adaptadores ainda a conferir no runtime de produção. Nenhum envio de teste foi feito. Não há promessa de aviso se permissões, Focus, rede, force-stop ou restrições do sistema o impedirem.

Testes locais, sem dependências novas:

```powershell
& 'C:\Program Files\nodejs\node.exe' --test 'C:\IALD\Central de Patentes\work\iald_background_20260930\notifications\tests\notifications.test.mjs'
& 'C:\Python314\python.exe' -X utf8 -B -m unittest discover -s 'C:\IALD\Central de Patentes\work\iald_background_20260930\notifications\tests' -p 'test_*.py' -v
```

DPAPI exige execução sob usuário Windows com perfil disponível. No isolamento desta sessão a chamada sintética retornou código Windows 2; fora do isolamento o round-trip passou. Tests de rotas usam uma fachada Flask (framework real ausente neste Python), e testes de assinatura/transporte usam fakes. O relatório final `validation.json` registra os resultados, sem confundi-los com compilação/entrega no dispositivo.

Gate físico posterior: opt-in/recusa; Home/tela bloqueada; app encerrado e toque a frio; múltiplos jobs; perda de rede; token rotacionado; troca de conta/logout; permissões retiradas; configurações ausentes; resposta acessível na retomada sem push. Conferir entitlements do **binário assinado**, APNs production no TestFlight e canal/ícone/Android 13+. Auditar ambos os grupos iOS e o canal Android aplicável antes de anunciar disponibilidade.


[REAL — fechamento local 30/09/2026] 49/49 testes Node do cliente integrado, 16/16 testes Node do sidecar, 32/32 testes Python do backend/patches e 6/6 regressões adversariais do núcleo. `node --check` passou no asset gerado. HTTP 410 agora é terminal expired: persiste aviso antes de eliminar o pendente, sem ACK impossível nem nova geração. Logout nativo aguarda POST `/api/native-push/revoke-session` autenticado; falha mantém o bearer e pede nova tentativa. O módulo final em `../server` foi conferido byte a byte. Não houve chamada remota, deploy ou compilação nativa. Evidências e hashes em `validation.json`; instruções finais em `HANDOFF.txt`.

[INPUT — fechamento do pai] Android debug isolado em `../mobile-review`, com patches nativos e push 8.1.2, passou 245 tasks. Compilação relatada pelo pai, sem envio push ou distribuição demonstrados nesta auditoria.
