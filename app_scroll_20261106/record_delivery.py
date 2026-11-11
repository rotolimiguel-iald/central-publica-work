"""Record verified progress, leaving TestFlight distribution explicitly pending."""
import json,datetime,subprocess,os
from pathlib import Path
from task import W,REF,OWNER,UNIT,PY,pin,save,call,act
M=W/'mobile/release'
final=json.loads((M/'IOS_ARCHIVE_FINAL.json').read_bytes())
assert final['status']=='completed'
installed=json.loads((W/'INSTALLED.json').read_bytes())
assert all(pin(r['target'])['sha256']==r['new'] for r in installed['files'])
plan=json.loads((W/'INSTALL_PLAN.json').read_bytes())
assert all(pin(r['path'])['sha256']==r['sha256'] for r in plan['preserve'])
receipts=['INSTALLED.json','INSTALL_PLAN.json','TEST_SCROLL.json','TEST_FULL_CLIENT.json','review/REVIEW_R1.json','review/DEPLOY_REVIEW_R1.json','review/PRIVATE_REGRESSION.json','review/PUSH_BYTES_REVIEW.json','HTTP_AFTER_INSTALL.json','mobile/release/AUDIT.json','mobile/release/APK_PUBLICATION.json','mobile/release/ANONYMOUS_DOWNLOAD.json','mobile/release/COMMIT.json','mobile/release/PUSH.json','mobile/release/IOS_ARCHIVE_FINAL.json']
delivery={'status':'STATIC_REPAIR_INSTALLED_NATIVE_BUILD_FINISHED_DISTRIBUTION_PENDING','unit':UNIT,'reference':str(REF),
 'changes':['User upward gestures pause following immediately; geometry alone no longer forces bottom','Background identity checks no longer rebuild an unchanged conversation','Same-view redraw preserves scroll; delayed frame cannot override newer gesture or view','Public/private rendering share scroll policy; editing and selection remain protected'],
 'installed_files':len(installed['files']),'preserved_files':len(plan['preserve']),'restart':False,'provider_calls':0,
 'availability':{'web':'Installed; reload page to load new client. Full client tested in isolated synthetic browser, no authenticated production chat test.',
  'android':'4.1(42) APK/AAB signed/audited; APK published on existing authenticated route; 26 older APKs preserved. Local anonymous request302/login; public403, layer undetermined. Authenticated download and physical install unverified.',
  'ios':'4.1(47) source pushed; Xcode Cloud archive '+str(final['conclusion'])+'. TestFlight processing/groups not inspected; Apple login pending.',
  'google_play':'Not published in this delivery','physical_devices':'Not inspected'},
 'commit':final['head_sha'],'apple_check':final['id'],'apple_build_url':final['details_url'],
 'pending':['Complete Apple login; inspect same archive/TestFlight build, save test notes and distribute to Equipe/Piloto as applicable','Confirm iPhone physical scrolling after upgrade; optional authenticated APK download check'],
 'sources':[pin(W/r) for r in receipts]}
save('DELIVERY_PENDING_APPLE.json',delivery)
source=pin(W/'DELIVERY_PENDING_APPLE.json')
g=call({'operation':'get','reference':str(REF)},False);handles=list(g['p'].get('handles',[]))
handles.append({'id':'ios47_archive','status':'completed' if final['conclusion']=='success' else 'failed','evidence':pin(M/'IOS_ARCHIVE_FINAL.json')})
changes={'records':[{'id':'scroll_native_delivery_pending_apple','kind':'fact','statute':'REAL','text':'Static repair reviewed and installed; Android42 signed/published; same iOS47 Cloud archive finished. Apple sign-in and actual TestFlight group distribution remain pending. No physical device test, provider generation or science change.','sources':[{'kind':'artifact','ref':source['path'],'sha256':source['sha256']}]}], 'flow':{'phase':'awaiting_apple_login','next_action':'Resume exact reference; inspect existing iOS47 archive and both TestFlight groups after user sign-in; do not build or push again.','handles':handles}}
save('DELIVERY_CHANGES.json',changes)
r=call({'operation':'transition','reference':str(REF),'actor':{'id':OWNER,'kind':'agent'},'expected_revision':g['revision'],'event_id':'scroll-delivery-pending-apple','changes_file':str(W/'DELIVERY_CHANGES.json'),'changes_sha256':pin(W/'DELIVERY_CHANGES.json')['sha256']},False);save('DELIVERY_RECEIPT.json',r)
save('MOBILE_PENDING.json',act('block',task_id='mobile',event_id='scroll-mobile-apple-login',reason='Apple session expired; explicit login request remains pending. Native archive inspected through exact commit check only; no group claim.',sources=[source]))
board=subprocess.run([PY,'-B','-X','utf8',r'C:\IALD\PROGRAMA_IALD\iald.py','avancar',UNIT,'--quem',OWNER,'--status','AGUARDA_OPERADOR','--evidencia',source['path'],'--nota','Web corrigida e Android42 publicado; iOS47 arquivo concluido, falta entrada Apple/distribuicao.'],capture_output=True)
assert board.returncode==0,board.stderr.decode(errors='replace')
save('BOARD_PENDING.json',json.loads(board.stdout))
route={'tipo':'RESULTADO','rota_id':'infra.app.scroll_20261106','dominio':'INFRA_APP','titulo':'Correção de rolagem instalada; iOS aguarda distribuição','resultado':'10destinos revisados instalados,1797pinos preservados; regressão pública/privada e interface completa passaram; Android42 publicado; archive47 '+str(final['conclusion']),'veredito':'STATIC_PASS_DISTRIBUTION_PENDING','estatuto':'REAL','status':'EXAMINADA','proximo_passo':'Entrada Apple e distribuição da mesma build47; nenhum rebuild','artefatos':[source['path']]}
save('ROUTE_DELIVERY.json',route)
rp=subprocess.run([PY,'-X','utf8',r'C:\IALD\MAPA_DE_ROTAS\rotas.py','registrar',str(W/'ROUTE_DELIVERY.json'),'--quem',OWNER],capture_output=True);assert rp.returncode==0
save('ROUTE_DELIVERY_RECEIPT.json',json.loads(rp.stdout))
text=f'''---
quem: {OWNER}
casa: IALD Nativa
tipo: project
estatuto: REAL
alvo_sugerido: app-iald-mobile.md
fontes:
  - {source['path']}  sha256:{source['sha256']}
---
Correção operacional de rolagem: acompanhamento automático respeita gesto para ler acima, recuperação de identidade não redesenha conversa inalterada, RAF atrasado não sobrepõe gesto/troca de sessão. Ramo privado usa a mesma política visual. Testes sintéticos de navegador público/privado, autenticação e interface completa aprovados; não são teste físico.
Dez destinos estáticos/versões instalados com revisão independente e backups de bytes; 1797pinos de ciência/runtime preservados, sem restart ou chamadas de modelos. v409 permanece.
Android4.1(42): APK/AABassinados/auditados; APK publicado,26anteriores preservados; download autenticado não conferido. GooglePlay não publicado.
iOS4.1(47): commit {final['head_sha']}; mesmo archive {final['id']} concluiu {final['conclusion']}. TestFlight/grupos Equipe/Piloto AINDA NÃO CONFERIDOS: sessãoAppleexpirada, pergunta ao titular pendente. Não declarar47disponível nem iniciar outrobuild.
Retomar referência {REF}; mobilebloqueadoaguardandologin, unidadeAGUARDA_OPERADOR. Ciência/kernel/gate intactos.
Lição: não vincular recuperação periódica a abrirConversa/scrollHeight; modo seguir exige intenção. Git *.gradle text eol=lf produz diff aparente contra blobCRLFcustodiado; reconciliação revisada exigiu igualdade de bytes working/plan/commit e ausência de diff semântico. Pinosoriginais preservados; não repetirpush.
'''
save('MEMORY_DEPOSIT.md',text.encode())
print(json.dumps({'delivery':str(W/'DELIVERY_PENDING_APPLE.json'),'memory_candidate':str(W/'MEMORY_DEPOSIT.md'),'revision':r['revision']}))
