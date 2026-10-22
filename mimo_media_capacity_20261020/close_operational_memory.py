"""Close local agents only after official tool results; retain external uncertainty."""
import json,hashlib
from task import W,REF,OWNER,call,new,project
c=call({'operation':'get','reference':str(REF)},False)
t=W/'AGENT_TERMINAL_TOOL_RESULTS_RFINAL.json'
s=json.loads(t.read_bytes())['result']['status']
flow=dict(c['p']);handles=[dict(h) for h in flow.get('handles',[])]
for h in handles:
    state=s.get(h.get('external_id'))
    if isinstance(state,dict) and 'completed' in state:
        h.update(status='completed',terminal_source=str(t))
flow.update(handles=handles,phase='engineering_delivered_with_provider_limits',next_action='Novo teste pago opcional aguarda resposta humana na unidade específica. Áudio maior falhou em percepção; vídeo incerto não será repetido.')
paths=[W/'delivery.json',W/'DEPLOY_ACCEPTED_RFINAL.json',t,W/'memory_stage/FINAL_R4/APPLIED.json']
record=dict(id='media-capacity-engineering-accepted-rfinal',kind='fact',statute='REAL',text='Entrega de engenharia e distribuição aceita por revisor real distinto na revisão11. Oito superfícies de memória verificadas após aplicação. Percepção geral não demonstrada; vídeo incerto preservado sem retry e teste extra0.50USD continua pendente de resposta humana.',sources=[dict(kind='artifact',ref=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in paths])
r=call(dict(operation='transition',reference=str(REF),actor=dict(id=OWNER,kind='agent'),expected_revision=c['receipt']['revision'],event_id='media-capacity-local-closeout-rfinal',changes=dict(records=[record],flow=flow)),False)
new('FINAL_OPERATIONAL_MEMORY.json',r)
p=project();new('FINAL_MISSION_PROJECT.json',p)
print(json.dumps(dict(revision=p['receipt']['revision'],tetelestai=p['projection']['tetelestai'],unresolved_handles=p['projection']['unresolved_handles'],scope='Engineering only; provider limitations and pending human decision retained')))
