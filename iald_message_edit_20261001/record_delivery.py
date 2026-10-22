from pathlib import Path
from datetime import datetime, timezone
import hashlib,json,os
W=Path(__file__).resolve().parent
R=Path(r'C:\IALD\projetos_pyhton\IALD')
C=Path(r'C:\IALD\Central de Patentes')
M=Path(r'C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory')
ios=json.loads((W/'ios_release.json').read_bytes())
android=json.loads((W/'android_release.json').read_bytes())
checks=json.loads((W/'tests/test_manifest.json').read_bytes())
assert checks['passed'] and ios['internal']=='Em testes' and ios['external']=='Em testes'
assert android['versionCode']==25 and android['signature_verified']
now=datetime.now(timezone.utc).isoformat()
marker='IALD_MESSAGE_EDIT_CONTRAST_KEYBOARD_BUILD28_20261001'
note=f'''

## 01/10/2026 — Editor de mensagem visível e adaptado ao teclado; iOS 28 / Android 25
<!-- {marker} -->

[INPUT] Corrigir texto invisível ao editar e reenviar mensagem interrompida e a proximidade do teclado, preservando as demais funções do app.

[REAL] Causa reproduzida no cliente anterior: texto de 120 caracteres herdava branco da bolha sobre fundo branco; fonte 15px. Editor agora tem cores explícitas em ambos os temas, preenchimento WebKit, fonte 16px, altura ajustada à conversa, botões de 44px e margens. Durante edição, a rolagem automática não puxa o campo para o fim. Redimensionar preserva seleção e rolagem interna, incluindo o fim de textos longos. Enter quebra linha; Ctrl/Cmd+Enter envia; IME não envia acidentalmente. Cancelar conserva histórico; reenvio revalida geração/conversa/pendência.

[REAL] 25/25 testes offline aprovados; revisão independente corrigiu regressão de cursor no fim antes da entrega. CUA verificou a aplicação completa em fixture local com dados sintéticos e rede bloqueada: 393x852 e 393x460, temas claro/escuro, 30 linhas, cancelamento e reenvio. Nenhuma chamada paga. Teste físico de teclado WKWebView/iPhone ainda não executado. Web instalada com CAS, backups de bytes e troca atômica de dois arquivos; sem reinício do servidor. Sondagem anônima continua redirecionando ao login; não foi declarada verificação autenticada da conta do operador.

[DISPONIBILIDADE — {now}] Web: arquivos atualizados. iOS 4.1(28): compilação Xcode Cloud {ios['cloud_build_id']} concluída, commit {ios['source_commit']}, build ASC {ios['asc_build_id']}; grupos IALD Equipe e IALD Piloto conferidos Em testes. Android 4.1(25): APK/AAB compilados, assinatura e recursos conferidos; APK no canal autenticado {android['url']}. Google Play permanece dependente do cadastro/DUNS, não publicado nesta entrega. Convite existente: https://testflight.apple.com/join/A5XEdy1H. Instalação física da versão nova depende do usuário. Dados de vencimento somente na administração; Apple exibiu {ios['expiry_display']}, sem data/hora exatas, portanto nenhuma data inferida.

[ESCOPO] Sem alteração de backend/JEV, contas, cotas, consentimentos, modelos, memória científica, kernel ou gate. Não habilita push pendente. Evidências e hashes: work/iald_message_edit_20261001/tests/test_manifest.json, visual_verification.json, web_deployment.json, mobile_prepared.json, mobile_audit.json, android_release.json, ios_release.json. Memórias operacionais atualizadas por acréscimo com backup imediato de bytes.
'''
stamp=datetime.now().strftime('%Y%m%d_%H%M%S_%f');records=[]
def replace(p,new):
 old=p.read_bytes();bak=p.with_name(p.name+'.bak_'+stamp)
 with bak.open('xb') as f:f.write(old)
 assert bak.read_bytes()==old
 tmp=p.with_name(p.name+'.tmp_editor_'+str(os.getpid()))
 with tmp.open('xb') as f:f.write(new);f.flush();os.fsync(f.fileno())
 assert tmp.read_bytes()==new and p.read_bytes()==old
 os.replace(tmp,p);assert p.read_bytes()==new
 records.append(dict(path=str(p),backup=str(bak),sha256=hashlib.sha256(new).hexdigest()))
p=R/'iald_deadlines.json';dead=json.loads(p.read_bytes());prior=dead['items'].copy();dead['checked_at']=now
for key,group in [('testflight_internal','IALD Equipe'),('testflight_external','IALD Piloto')]:
 dead['items'][key]=dict(expires_at=None,label='IALD 4.1 (28) — '+group,source='App Store Connect '+now+': Em testes; '+ios['expiry_display']+'; data/hora exatas não exibidas.',build='4.1 (28)',status='Em testes')
for key in prior:
 if not key.startswith('testflight_'):assert prior[key]==dead['items'][key]
replace(p,(json.dumps(dead,ensure_ascii=False,indent=2)+'\n').encode())
paths=[R/'CLAUDE.md',C/'work/iald_openai_motor_20260914/HANDOFF_RUNTIME.md',R/'iald-app/HANDOFF_MOTOR_OPENAI_20260914.md',C/'memory/TGL_ATLAS.md',C/'memory/TGL_INDICE_VIVO.md',M/'MEMORY_2.md',M/'app-iald-mobile.md']
for p in paths:
 old=p.read_bytes()
 if marker.encode() not in old:replace(p,old+note.encode())
(W/'memory_delivery.json').write_bytes(json.dumps(records,ensure_ascii=False,indent=2).encode())
print(json.dumps(dict(updated=len(records),backups_verified=True)))
