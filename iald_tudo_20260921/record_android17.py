"""Record verified Android compilation and remaining release gates."""
import record_haiku_preparation as record
record.MARKER = 'IALD_ANDROID17_BUILT_IOS18_PREPARED_20260922'
record.NOTE = '''[REAL] Instalados npm exatos Filesystem8.1.3(MIT), Share8.0.2(MIT), Printer8.1.4(MPL-2.0). Backups verificados de package/lock/plist. Backup indevido dewww movido para _backups_build18_20260922_104326 antes do sync. PrivacyInfo ganhou FileTimestamp C617.1 preservando UserDefaults CA92.1. npm run sync passou validação11referências e sincronização Android/iOS. FileProvider e cache-path conferidos. iOS CURRENT_PROJECT_VERSION18; Android versionCode17; marketing4.1. Nenhum commit/push.

[REAL] Primeira compilação falhou por Java8. Refeita com JBR21.0.9 de C:\\Program Files\\Android\\Android Studio1\\jbr somente no processo, sem mudar Java global. assembleRelease+bundleRelease: BUILD SUCCESSFUL,2m26s,454tarefas. verify_android17.py conferiu certificado igual ao APK16, plugins e assets APK/AAB iguais awww, sem backups/env/jks nos assets. aapt2 confirmou br.ia.IALD/versionCode17. APK4952423bytes; AAB4804748bytes. Hashes/certificado no recibo android17_*.json em work/iald_build18_20260921. APK copiado e conferido em C:\\IALD\\projetos_pyhton\\IALD\\downloads\\IALD-4.1-17.apk. Chave existente, nenhuma credencial criada.

[MATRIZ] Android17 compilado localmente; download autenticado e exportação física pendentes; GooglePlay não enviado. HEAD sem sessão recebeu200 text/html, nãoAPK: NÃO prova download; rota exige sessão/cadastro e isso foi preservado. iOS18 tem fontes/plugins/plist preparados; falta regenerar Package.resolved no workflow ios-dependencies, compilar XcodeCloud e atualizar Equipe/Piloto. Nenhuma nova build TestFlight enviada. Web/servidor não reiniciados nem alterados nesta etapa. Não declarar exportação resolvida sem testes físicos iPhone/iPad/Android.

[OPEN] Haiku candidato corrigido204859tokens ainda excede janela; fontes Lean nucleares restauradas. Sonnet testes pagos/cache pendentes. fetch_tgl.pointer aguarda autorização específica após rejeição automática; não executado. Objetivo integral inacabado.
'''
if __name__ == '__main__':
    record.main()
