from pathlib import Path
import sys,json,sqlite3,hashlib
W=Path(__file__).resolve().parent;R=Path(r'C:\IALD\projetos_pyhton\IALD');sys.path.insert(0,str(R))
from iald_chat_jobs import WindowsCipher
import iald_app_memory as memory
def capture(which):
 source=W/('LIVE_'+which+'_JOB.json');j=json.loads(source.read_bytes())
 path=R/'.iald_runtime/chat_jobs/jobs.sqlite3'
 with sqlite3.connect(path.as_uri()+'?mode=ro',uri=True) as db:
  db.row_factory=sqlite3.Row;job=dict(db.execute('select id,conversation_id,status,created,updated,seq,error from jobs where id=?',(j['id'],)).fetchone())
  events=list(db.execute('select seq,data from events where job=? order by seq',(j['id'],)))
 assert job['status']=='completed' and not job['error'],job
 cipher=WindowsCipher();fragments=[];warnings=[];tools=[];done=False;provider=[]
 for row in events:
  raw=cipher.open(row['data']).decode('utf-8')
  if raw.strip()=='[DONE]':done=True;continue
  data=json.loads(raw)
  if data.get('iald_aviso') or data.get('error'):warnings.append(data)
  if data.get('iald_status',{}).get('fase')=='ferramenta':tools.append(data['iald_status'].get('tool'))
  for choice in data.get('choices',[]):
   value=(choice.get('delta') or {}).get('content')
   if isinstance(value,str):fragments.append(value)
 text=''.join(fragments);assert text.strip() and done and not warnings
 affected=json.loads((W/'affected_context.json').read_bytes());principal=affected['scope']['principal']
 ident='app_'+hashlib.sha256((principal+':'+job['conversation_id']).encode()).hexdigest()
 store=memory.MemoryStore(memory._SHARED_ROOT);snapshot=store.get(ident,affected['scope'])
 request_id='job_'+memory.digest(principal+':'+job['id'])
 handles=[h for h in snapshot['p']['handles'] if h.get('request_id')==request_id and h.get('kind')=='activity_operation']
 assert handles and all(h['status']=='completed' for h in handles),handles
 result={'status':'PASS','job':job,'duration_seconds':job['updated']-job['created'],'done':done,'warnings':len(warnings),'tools':tools,'characters':len(text),'context_id':ident,'memory_revision':snapshot['revision'],'operation_statuses':[h['status'] for h in handles],'semantic_acceptance_inferred':False}
 with (W/('LIVE_'+which+'_RESULT.json')).open('x',encoding='utf-8') as f:json.dump(result,f,ensure_ascii=False,indent=2)
 with (W/('LIVE_'+which+'_TEXT.txt')).open('x',encoding='utf-8') as f:f.write(text)
 print(json.dumps({'status':'PASS','which':which,'duration_seconds':result['duration_seconds'],'tools':tools,'characters':len(text)},ensure_ascii=False))
if __name__=='__main__':capture(sys.argv[1])
