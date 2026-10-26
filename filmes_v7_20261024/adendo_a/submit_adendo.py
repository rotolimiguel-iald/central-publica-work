"""Submit the completed v400 construction without accepting or publishing it."""
from pathlib import Path
import hashlib,json,os,sys,time
W=Path(__file__).resolve().parent
sys.path.insert(0,str(W.parent))
import mission
from bootstrap import cli,REF,ACTOR
V=Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\video_um\delivery_v7')
T=Path(r'C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_022\ADENDO_A')
def sha(p):
 with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def save(p,d):
 b=(json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode()
 if p.exists():
  old=p.read_bytes()
  if old==b:return
  bk=p.with_name(p.name+'.bak_'+str(time.time_ns()));bk.write_bytes(old);assert bk.read_bytes()==old
 tmp=p.with_name(p.name+'.tmp');tmp.write_bytes(b);assert tmp.read_bytes()==b;os.replace(tmp,p)
result=T/'RESULTADO.json';d=json.loads(result.read_bytes())
assert d['status']=='BUILT_FOR_MANAGEMENT_REVIEW' and d['source']=='v400'
assert d['manifest']['sha256']==sha(V/'PUBLIC_DELIVERY_V7.json')
review=W/'INTEGRATION_REVIEW.json'
rv=json.loads(review.read_bytes());assert rv['status']=='PASS_WITH_SCOPE'
for e in d['evidence']:assert sha(Path(e['path']))==e['sha256'],e['path']
p=mission.project();task=next(t for t in p['projection']['active']+p['projection']['settled'] if t['id']=='ADENDO_A')
context={'actor':ACTOR,'expected_revision':p['receipt']['revision'],'projection_sha256':p['projection_sha256'],'task_id':'ADENDO_A','lease_id':task['lease']['id']}
evidence=[{'path':str(f),'sha256':sha(f)} for f in [result,T/'RELATORIO.md',review,V.parent/'PUBLIC_DELIVERY_V7.json']]
if task['status']=='review_pending':
 assert task['submitted_by']==ACTOR['id'] and task['evidence']==evidence
else:
 assert mission.call({'operation':'check',**context,'max_chars':100000})['ready']
 sub=mission.call({'operation':'submit',**context,'event_id':'ordem022-adendo-a-submit-'+sha(result)[:16],'evidence':evidence,'note':'Construção técnica v400 e revisão independente documentadas; integração/publicação/aceite final pela gerência.'})
 save(W/'SUBMISSION_ADENDO_A.json',sub)
state=cli(r'C:\IALD\MEMORIA_IALD\session_memory.py',{'operation':'get','reference':str(REF)})['result']
handles=state['p']['handles'];m=json.loads((V/'RENDER_MANIFEST.json').read_bytes())
for kind,r in m['jobs'].items():
 matches=[p for p in (V/'cinema/render/jobs').glob(kind+'_*.json') if sha(p)==r['job_sha256']]
 assert len(matches)==1
 job=json.loads(matches[0].read_bytes());assert job['render']['encoded']==job['metadata']['total'] and 'sha256' in job
 h=next((h for h in handles if h['id']==job['id']),None)
 if h is None:h={'id':job['id'],'kind':'local_render','task_id':'ADENDO_A'};handles.append(h)
 h.update(status='completed',evidence=str(matches[0]),version='v400',scope='Full rerender authorized by ORDEM022 ADENDO A')
for h in handles:
 if h['id']=='v400-adendo-a-pipeline-20261025':h.update(status='completed',evidence=str(result))
transition=cli(r'C:\IALD\MEMORIA_IALD\session_memory.py',{'operation':'transition','reference':str(REF),'actor':ACTOR,'expected_revision':state['revision'],'event_id':'ordem022-adendo-a-delivery-'+sha(result)[:16],'changes':{
 'records':[{'id':'v400_adendo_a_construction_delivery','kind':'fact','statute':'REAL','text':'ADENDO A concluído tecnicamente: dois filmes e loop renderizados integralmente da fonte v400; comparação exata sem alteração científica; narração EN/PT reutilizada sem TTSnovo; replay, exportações e player conferidos. Voz pessoal permanece em prévias separadas para audição humana. Entrega para revisão/integração da gerência, sem publicação ou mudança do gate.','sources':[{'kind':'artifact','ref':str(result),'sha256':sha(result)}]}],
 'flow':{'phase':'v400_construction_submitted_for_management_review','next_action':'Gerência a7 integra/publica após revisão. Operador avalia as prévias pessoais PT/EN; não incorporar automaticamente nem repetir renders/TTS concluídos.','handles':handles}}})
save(W/'TRANSITION_DELIVERY.json',transition)
route={'tipo':'RESULTADO','rota_id':'site.filmes.v7.ordem022','dominio':'SITE_E_PUBLICACAO','titulo':'Filmes V7 da fonte v400 entregues para integração','resultado':f"v400; comparação científica inalterada; {d['public_files']} arquivos públicos pinados; 64 verificações de proveniência; 61 comparações browser.",'veredito':'BUILT_FOR_MANAGEMENT_REVIEW','estatuto':'REAL','status':'EXAMINADA','olhou_dados':False,'defeito':'Sem benchmark GPU integrada ou audição subjetiva de todas as falas; prévias pessoais aguardam o operador.','nao_refazer':'Reutilizar entrega v400 e caches de áudio verificados. Não repetir render ou TTS encerrados.','proximo_passo':'Gerência a7 revisa, integra por hash e publica.','onde':str(V),'artefatos':[str(result),str(V.parent/'PUBLIC_DELIVERY_V7.json')],'refs':[],'nota':'Construção operacional; não altera ciência ou gate.'}
save(W/'FINAL_ROUTE.json',route)
print(json.dumps({'status':'SUBMITTED_NOT_SELF_ACCEPTED','revision':transition.get('result',{}).get('receipt',{}).get('revision'),'route':str(W/'FINAL_ROUTE.json')},ensure_ascii=False))
