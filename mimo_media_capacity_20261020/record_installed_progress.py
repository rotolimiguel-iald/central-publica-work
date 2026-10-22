"""Record installed facts and the observed UI regression without claiming delivery."""
import hashlib,json
from task import W,REF,OWNER,call,new
current=call({'operation':'get','reference':str(REF)},False)
flow=dict(current['p'])
flow.update(phase='installed_ui_followup',next_action='Revisar e instalar correção de bootstrap da mídia legada; depois testes reais e distribuição.')
sources=[]
for name in ('deployment.json','restart.json','INSTALLED_VERIFICATION.json','review_backend/LIVE_BOOTSTRAP_HOLD_R1.json'):
    p=W/name;sources.append(dict(kind='artifact',ref=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
result=call(dict(operation='transition',reference=str(REF),actor=dict(id=OWNER,kind='agent'),
    expected_revision=current['receipt']['revision'],event_id='media-capacity-installed-ui-followup-r1',
    changes=dict(records=[dict(id='media-capacity-install-and-ui-followup-r1',kind='fact',statute='REAL',
        text='18 arquivos instalados e reinício web HTTP200 conferidos; ciência v394 preservada. Teste UI revelou falha de bootstrap/migração de mídia antiga, registrada ao lado e em correção. Nenhuma nova chamada de modelo ou distribuição mobile nesta etapa.',sources=sources)],flow=flow)),False)
new('INSTALLED_PROGRESS_MEMORY.json',result)
print(json.dumps(dict(revision=result['revision'],phase='installed_ui_followup')))
