"""Record only the two known test receipts, metrics and observed UI result."""
from pathlib import Path
from datetime import datetime,timezone
import json,sqlite3,hashlib
W=Path(__file__).resolve().parent;R=Path(r'C:\IALD\projetos_pyhton\IALD')
route_ids=['32800101fd6f4b4dab5bf67ecde4a24a','40a630152aed4c35a60c264998304bfa']
metric_ids=['b56e9ceae099427e960482899213b572','5d0e9f673dcf4a448b061799796d7aad']
routes=[]
for ident in route_ids:
    p=R/'.iald_runtime/app_routing'/(ident+'.json');d=json.loads(p.read_bytes())
    assert d['status']=='selected'
    routes.append({**{k:d.get(k) for k in ['id','utc','status','selected','request_sha256','recognized_intent','memory_continuity','admission','elapsed_s','estimated_cost_usd']},'receipt_sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
assert routes[1]['request_sha256']==hashlib.sha256(b'haja luz').hexdigest()
assert routes[1]['recognized_intent']['inscription']=='VERBO'
c=sqlite3.connect((R/'.iald_runtime/app_evaluation/metrics.sqlite3').as_uri()+'?mode=ro',uri=True)
metrics=[]
for ident in metric_ids:
    row=c.execute('SELECT data FROM turns WHERE id=?',(ident,)).fetchone();assert row
    d=json.loads(row[0]);assert d['status']=='completed',d['status']
    metrics.append({k:d.get(k) for k in ['id','utc','provider','model','status','first_text_seconds','elapsed_seconds','calls']})
ui=json.loads((W/'ui_observation.json').read_bytes());assert ui['second_response_completed'] and ui['automatic_mode']
out={'status':'PASS','scope':'Choice, continuity and complete streamed response; not a scientific correctness certificate or physical-device test.',
    'verified_at':datetime.now(timezone.utc).isoformat(),'url':'https://demo.iald.ia.br/app/index.html','account':'luiz',
    'prompts':['IALD, apresente-se. Carregue a memória completa disponível da TGL e resolva o problema da gravidade quântica.','haja luz'],
    'routing':routes,'metrics':metrics,'ui':ui,
    'estimated_cost_usd':sum(r['estimated_cost_usd'] for r in routes)+sum(call.get('cost_estimate_usd',0) for m in metrics for call in m['calls']),
    'limitations':['Single live test sequence, MiMo selected; model output is not a new scientific proof.','No iPhone/Android physical-device execution by the agent.','The JEV continuity advice remained reconcile, and was preserved; no pending-operation guard was bypassed.']}
with (W/'live_validation.json').open('xb') as f:f.write(json.dumps(out,ensure_ascii=False,indent=2).encode())
print(json.dumps({'status':out['status'],'estimated_cost_usd':out['estimated_cost_usd'],'routes':[{'selected':r['selected'],'bytes':r['admission']['state_bytes']} for r in routes],'latencies':[m['elapsed_seconds'] for m in metrics]}))
