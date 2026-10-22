"""Persist the release commit, dependency evidence and exact Cloud run to resume."""
import record_haiku_preparation as record

record.MARKER = 'IALD_IOS18_DEPENDENCIES_RESOLVED_CLOUD_STARTED_20260922'
record.NOTE = '''[REAL] audit_mobile_publish.py conferiu 15 arquivos de cliente, índice Git vazio antes de staging, conjunto exato de mudanças, padrões de credenciais e igualdade de assets www/iOS. npm run validate passou11referências. Commit local acd1c2f enviado à referência temporária codex/ios-dependencies-build18 do repositório privado rotolimiguel-iald/iald-app. Nenhum arquivo de servidor, .env, chave ou acervo privado incluído.

[REAL] Workflow ios-dependencies executado no GitHub, run35738305958, terminou SUCCESS em22/09/2026 14:10:13UTC. Artifact ios-swift-package-lock baixado em work/iald_build18_20260921/swift_lock_run_35738305958/Package.resolved. Pins lidos: capacitor-swift-pm8.5.2 e ion-ios-filesystem1.1.4. Lock incorporado com backup de bytes e verificação, sem inventar revision. Commit e87d3b5 enviado à branch autorizada codex/mobile-release. O estado GitHub do commit registra contexto IALD | IALD PENDING, URL da execução: https://appstoreconnect.apple.com/teams/7e576f08-1ae7-4b38-ac9f-cfdb952c2cac/apps/6760655636/ci/builds/9e2530cb-e3f9-4643-a633-0a3e8e9c6b67 . Isso comprova execução registrada, NÃO sucesso ou disponibilidade TestFlight.

[OPEN — Apple] A aba1 apresentou inicialmente dados antigos da4.1(17), depois redirecionou para /login ao consultar detalhe. Portanto não tratar o primeiro estado como verificação atual autenticada. Login expirado: aba App Store Connect ficou visível, solicitada entrada pelo iPhone via pergunta assíncrona. Clique automatizado do botão falhou alvo indisponível; operador pode clicar diretamente. Não foi fornecida senha/código. Retomar execução Cloud específica acima após login; não disparar build duplicada enquanto status não terminal. Atualizar IALD Equipe e IALD Piloto após sucesso/processamento, conferir participação operador, O que testar e datas exatas.

[MATRIZ] Web inalterado e não reiniciado nesta etapa. Android17 APK/AAB compilados conforme recibo anterior; testes físicos/download autenticado/GooglePlay pendentes. iOS18 fonte+lock enviados e Cloud pending; interno/externo ainda não atualizados. Haiku: rascunho com proteção de campos corrigida, orçamento Anthropic atual não medido, não implantado. Sonnet/cache e confirmação visual Central pendentes. Objetivo integral permanece ativo e incompleto.
'''

if __name__ == '__main__':
    record.main()
