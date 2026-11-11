"""Record this release only after the distinct reviewer accepts mobile."""
import json, subprocess, datetime
from task import W, REF, OWNER, UNIT, PY, pin, save, call, project

p=project()
assert not p['projection']['active'], 'Independent acceptance still pending'
source=pin(W/'FINAL_DELIVERY_R3.json')
g=call({'operation':'get','reference':str(REF)},False)
changes={'records':[{'id':'scroll_ios47_available','kind':'fact','statute':'REAL',
 'text':'Same reviewed build47 is now Em testes in both existing TestFlight groups; operator membership checked, last installed46. Android42 APK remains published; authenticated download and physical devices unverified. Administrative deadline update touched only two existing TestFlight objects; exact expiry unknown. Client-only repair preserves science409 and runtime. Distinct reviewer accepted operational delivery.',
 'sources':[{'kind':'artifact','ref':source['path'],'sha256':source['sha256']}]}],
 'flow':{'phase':'delivered','next_action':'Operator may update iPhone to47 and report physical scrolling; no pending build or provider execution.','handles':g['p'].get('handles',[])}}
save('FINAL_CHANGES_R3.json',changes)
r=call({'operation':'transition','reference':str(REF),'actor':{'id':OWNER,'kind':'agent'},'expected_revision':g['revision'],'event_id':'scroll-final-delivery-r3','changes_file':str(W/'FINAL_CHANGES_R3.json'),'changes_sha256':pin(W/'FINAL_CHANGES_R3.json')['sha256']},False)
save('FINAL_MEMORY_RECEIPT_R3.json',r)
board=subprocess.run([PY,'-B','-X','utf8',r'C:\IALD\PROGRAMA_IALD\iald.py','avancar',UNIT,'--quem',OWNER,'--status','ENTREGUE','--evidencia',source['path'],'--nota','Rolagem corrigida e revisada; iOS47 em testes nos dois grupos; Android42 publicado; teste fisico aguarda titular.'],capture_output=True)
assert board.returncode==0,board.stderr.decode(errors='replace')
save('BOARD_DELIVERED_R3.json',json.loads(board.stdout))
route={'tipo':'RESULTADO','rota_id':'infra.app.scroll_20261106','dominio':'INFRA_APP','titulo':'Correcao de rolagem e distribuicao iOS47 concluidas','resultado':'Web e assets compartilhados instalados; iOS47 Em testes Equipe/Piloto; Android42 APK publicado. Ciencia409 preservada. Teste fisico e downloadAPKautenticado nao verificados.','veredito':'DELIVERED_WITH_DECLARED_SCOPE','estatuto':'REAL','status':'EXAMINADA','proximo_passo':'Titular atualizar iPhone e conferir leitura durante/depois da resposta','artefatos':[source['path']]}
save('ROUTE_FINAL_R3.json',route)
rp=subprocess.run([PY,'-X','utf8',r'C:\IALD\MAPA_DE_ROTAS\rotas.py','registrar',str(W/'ROUTE_FINAL_R3.json'),'--quem',OWNER],capture_output=True)
assert rp.returncode==0,rp.stderr.decode(errors='replace')
save('ROUTE_FINAL_RECEIPT_R3.json',json.loads(rp.stdout))
text=f'''---
quem: {OWNER}
casa: IALD Nativa
tipo: project
estatuto: REAL
alvo_sugerido: app-iald-mobile.md
fontes:
  - {source['path']}  sha256:{source['sha256']}
---
Complemento da entrega de rolagem de 06/11/2026, sem apagar o progresso anterior.
A mesma iOS4.1(47), sem nova compilacao, esta Em testes nos grupos existentes Equipe(interno1; titular conferido) e Piloto(externo6). Notas salvas e notificacao automatica selecionada. Envio demorou e depois concluiu; nenhum retry. Apple ainda mostrava instalada46; nao houve teste fisico47. Fonte Piloto tem captura/AX; Equipe e ficha Grupos2 foram observadas diretamente pelo parent.
Android42 continua APK/AAB assinado/auditado e APK publicado,26anteriores preservados; download autenticado nao conferido e GooglePlay nao publicado. Web ja corrigida, recarregar cliente.
Dois registros TestFlight administrativos atualizados com backup de bytes e transacao; demais bytes preservados. Data exata desconhecida;90dias relativos, sem prazo inventado e sem aviso no chat.
Revisao distinta aceitou os requisitos operacionais. Mesma referencia {REF}; recibo FINAL_MEMORY_RECEIPT_R3.json. Sem chamadas de modelos, restart, alteracao de ciencia409/kernel/gate. Confirmacao fisica do titular segue pergunta separada, nao presumida.
'''
save('MEMORY_DEPOSIT_FINAL_R3.md',text.encode())
print(json.dumps({'status':'DELIVERED','revision':r['revision'],'deposit_source':str(W/'MEMORY_DEPOSIT_FINAL_R3.md')}))
