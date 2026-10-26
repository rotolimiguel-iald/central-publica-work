"""Submit this builder's A/B evidence; preserve independent review authority."""
from pathlib import Path
import hashlib,json
import mission
from bootstrap import cli,save,REF,ACTOR
W=Path(__file__).resolve().parent
V=Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\video_um\delivery_v7')
T=Path(r'C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_022')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
delivery=json.loads((T/'RESULTADO.json').read_bytes())
assert delivery['status']=='BUILT_FOR_MANAGEMENT_REVIEW'
assert delivery['manifest']['sha256']==sha(V/'PUBLIC_DELIVERY_V7.json')
evidence=V/'audit/DELIVERY_AB.json'
for task_id in ['A','B']:
 p=mission.project()
 task=next(t for t in p['projection']['active']+p['projection']['settled'] if t['id']==task_id)
 if task['status']=='review_pending':
  assert task['submitted_by']==ACTOR['id']
  assert any(e['path']==str(evidence) and e['sha256']==sha(evidence) for e in task['evidence'])
  continue
 context={'actor':ACTOR,'expected_revision':p['receipt']['revision'],'projection_sha256':p['projection_sha256'],'task_id':task_id,'lease_id':task['lease']['id']}
 check=mission.call({'operation':'check',**context,'max_chars':100000})
 assert check['ready']
 result=mission.call({'operation':'submit',**context,'event_id':'ordem022-final-submit-'+task_id+'-'+sha(evidence)[:16],'evidence':[{'path':str(evidence),'sha256':sha(evidence)}],'note':'Construção técnica submetida; revisão e publicação pela gerência, sem aceite próprio.'})
 save('SUBMISSION_'+task_id+'_FINAL.json',result)
 print(task_id,result.get('receipt',{}).get('revision'))

final_project=mission.project()
for task in final_project['projection']['active']+final_project['projection']['settled']:
 assert task['status'] in ['review_pending','satisfied'],(task['id'],task['status'])
state=cli(r'C:\IALD\MEMORIA_IALD\session_memory.py',{'operation':'get','reference':str(REF)})['result']
handles=state['p']['handles']
manifest=json.loads((V/'RENDER_MANIFEST.json').read_bytes())
for kind,render in manifest['jobs'].items():
 matches=[p for p in (V/'cinema/render/jobs').glob(kind+'_*.json') if sha(p)==render['job_sha256']]
 assert len(matches)==1,(kind,len(matches))
 job=json.loads(matches[0].read_bytes());assert job['render']['encoded']==job['metadata']['total'] and 'sha256' in job
 handle=next((h for h in handles if h['id']==job['id']),None)
 if handle is None:
  handle={'id':job['id'],'kind':'local_render','task_id':'B'};handles.append(handle)
 handle.update(status='completed',evidence=str(matches[0]),version=manifest['version'],scope='Final corrected construction render')
for h in handles:
 if h.get('kind')=='subagent' and h.get('task_id') in ['C','D','E']:
  h['status']='completed';h['evidence']=str(T/'RESULTADO.json')
result=cli(r'C:\IALD\MEMORIA_IALD\session_memory.py',{'operation':'transition','reference':str(REF),'actor':ACTOR,'expected_revision':state['revision'],'event_id':'ordem022-final-construction-delivery-'+sha(T/'RESULTADO.json')[:16],'changes':{
 'records':[{'id':'v7_final_construction_delivery','kind':'fact','statute':'REAL','text':'Construção V7 entregue para revisão da gerência: filmes224/360s, fontev399, proveniência64checagens, replay61comparações, narraçãoEN/PT e legendas4idiomas; encodes e player final verificados. Negativos de fechamento e legenda preservados com correções. Sem publicação, aceite próprio, nova prova ou clonagem da voz pessoal. Limites e evidências no resultado.','sources':[{'kind':'artifact','ref':str(T/'RESULTADO.json'),'sha256':sha(T/'RESULTADO.json')}]}],
 'flow':{'phase':'construction_submitted_for_management_review','next_action':'Gerência a7 confere critérios, integra por hash e publica conforme ORDEM022. Não repetir TTS ou renders encerrados.','handles':handles}}})
save('TRANSITION_FINAL_DELIVERY.json',result)
print(json.dumps(result,ensure_ascii=False))
