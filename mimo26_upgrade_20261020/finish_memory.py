import json,hashlib
from pathlib import Path
import task
W=Path(__file__).resolve().parent
assert json.loads((W/'FINAL_REVIEW.json').read_bytes())['status']=='PASS'
projection=task.project()
assert not projection['projection']['active']
latest=json.loads((W/'memory_final/LATEST_PREPARED.json').read_bytes())
applied=list(Path(latest['latest_plan']).parent.glob('APPLIED_*.json'))
assert len(applied)==1
receipt=json.loads(applied[0].read_bytes());assert receipt['status']=='APPLIED_VERIFIED'
current=task.call({'operation':'get','reference':str(task.REF)},False)
handles=current['p']['handles']
observed=json.loads((W/'AGENT_TERMINAL_OBSERVATION.json').read_bytes())['status']
expected={'mimo26-media-agent':'01a15aa9-fb97-79b2-9391-db6af761eea1','mimo26-mobile-agent':'01a15604-76c6-7110-9a73-2dc692d95018','mimo26-review-agent':'01a15607-da9a-76e2-a12f-7ce9a5ab4a54','mimo26-routing-agent':'01a15aaa-d85e-7d01-bf9b-89747fc482d3'}
for h in handles:
 if h['id'] not in expected:continue
 assert h.get('external_id')==expected[h['id']]
 terminal=observed.get(h['external_id'])
 assert isinstance(terminal,dict) and terminal.get('completed'),h['id']
 h['status']='completed'
 h['terminal_observation_ref']=str(W/'AGENT_TERMINAL_OBSERVATION.json')
sources=[]
for p in [W/'FINAL_REVIEW.json',W/'DEPLOY_ACCEPT_REVIEWER.json',W/'live_validation.json',applied[0]]:
 sources.append({'kind':'artifact','ref':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
changes={'records':[{'id':'mimo26-final-delivery-verified','kind':'fact','statute':'REAL','text':'Aceites MiMo2/JEV3 recebidos e aplicados; revisão independente aceitou implantação. Ciência v394 preservada. Imagem e vídeo corretos; primeiro áudio falhou, preservado; ensaio após orientação identificou tom corretamente, sem causalidade isolada. Quatro chamadas MiMo/JEV estimadas USD0.0706696812, não fatura. iOS34 Em testes nos dois grupos; Android29 download autenticado/hash aprovado, sem GooglePlay ou instalação física verificada. Oito memórias atualizadas por append com backups.','sources':sources}], 'flow':{'phase':'completed','next_action':'Operador atualizar TestFlight para4.1(34); observar novos anexos dentro dos limites locais. Nenhum pedido incerto deve ser repetido.','handles':handles}}
r=task.call({'operation':'transition','reference':str(task.REF),'actor':{'id':task.OWNER,'kind':'agent'},'expected_revision':current['receipt']['revision'],'event_id':'mimo26-final-delivery-verified','changes':changes},False)
task.new('COMPLETION_MEMORY.json',r)
verify=task.call({'operation':'verify','reference':str(task.REF)},False);task.new('FINAL_MEMORY_VERIFY.json',verify)
p=task.project();task.new('FINAL_MISSION_STATE.json',p)
assert p['projection']['tetelestai']
print(json.dumps({'status':'COMPLETED','revision':p['receipt']['revision'],'tetelestai':True,'memory_surfaces':len(receipt['surfaces'])}))
