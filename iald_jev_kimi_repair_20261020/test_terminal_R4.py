"""Real local lifecycle + consumer break regression; no provider or live writes."""
import os,sys,json,hashlib,types,traceback
from pathlib import Path
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent;R=Path(r'C:\IALD\projetos_pyhton\IALD');native='--native' in sys.argv
ISO=W/('n4' if native else 'q4');ISO.mkdir(exist_ok=False)
sys.path[:0]=([] if native else [str(W/'admission_R4_stage')])+[str(R)]
os.environ['IALD_MEMORY_SNAPSHOT_ARCHIVE_DIR']=str(ISO/'archive')
def audit(event,args):
 if event in ('socket.connect','socket.getaddrinfo','subprocess.Popen'):raise RuntimeError('OFFLINE_DENIED:'+event)
 if event=='open':
  p,mode,flags=args
  if isinstance(p,(str,bytes)) and ((mode and any(c in mode for c in 'wax+')) or flags & (os.O_WRONLY|os.O_RDWR|os.O_CREAT)):
   if not Path(p).resolve().is_relative_to(W):raise RuntimeError('LIVE_WRITE_DENIED')
sys.addaudithook(audit)
import iald_app_memory as m
import iald_activity_operations as ops
from iald_memory.activity import KEY
checks={};cases={}
def fresh(name):
 m._SHARED_ROOT=ISO/name
 return m.begin(R,'synthetic-r4','r4_'+name,[{'role':'user','content':'Teste local sem provedor, preservar candidato para revisão.'}],request_id='r4_'+name)
class Source:
 def __init__(self,parts):self.parts=parts;self.status_code=200;self.headers={'Content-Type':'text/event-stream'}
 def iter_lines(self):yield from self.parts
 def iter_content(self):yield from self.parts
 def close(self):pass
def make(b,parts,label):
 op=b._lifecycle.start(label)
 return op,ops.Response(Source(parts),op,expect_sse=True)
def refs(b):
 out=[]
 for r in b.snapshot()['q']['records']:
  a=r.get('meta',{}).get(KEY,{})
  if a.get('kind')=='result':
   v=a['data']['result'];rec=v.get('response') if isinstance(v,dict) else None
   if isinstance(rec,dict) and rec.get('protocol')==ops.WIRE_REF_PROTOCOL:out.append(('result',rec))
  try:v=json.loads(r['text'])
  except ValueError:continue
  if isinstance(v,dict) and isinstance(v.get('transport'),dict):out.append(('checkpoint',v['transport']))
 return out
def capture(fn):
 try:return {'ok':True,'value':fn()}
 except Exception as e:return {'ok':False,'type':type(e).__name__,'message':str(e),'code':getattr(e,'code',None),'traceback':traceback.format_exc()}
done=b'data: [DONE]';stop=b'data: {"type":"message_stop"}';content=b'data: {"choices":[{"delta":{"content":"Luz"}}]}'
# Exact _api pattern: break on terminal, then context manager closes the response.
for name,terminal in [('break',done),('anthropic',stop)]:
 b=fresh(name);op,r=make(b,[content,b'',terminal,b'',b'UNREAD_TRAILING'],name)
 seen=[];at_terminal=False
 with r:
  for line in r.iter_lines():
   seen.append(line)
   if line==terminal:
    at_terminal=op.done
    break
 recs=refs(b);restored=ops.read_wire(b,recs[-1][1]) if recs else b''
 cases[name]={'done_before_terminal_reaches_consumer':at_terminal,'done_after_close':op.done,'wire_bytes':len(restored),'ref_status':recs[-1][1]['status'] if recs else None}
 checks[name+'_custody_before_yield']=at_terminal
 checks[name+'_exact_observed_wire']=restored==b'\n'.join([content,b'',terminal])
 checks[name+'_received_not_uncertain']=bool(recs) and recs[-1][1]['status']=='RECEIVED'
 if native:continue
if native:
 assert not checks['break_custody_before_yield'] and not checks['anthropic_custody_before_yield']
else:
 # Same chunk contains terminator and tail: all of this chunk was already received.
 first=content+b'\n\n'+done+b'\n\nTAIL_SAME_CHUNK'
 b=fresh('chunkbreak');op,r=make(b,[first,b'UNREAD_NEXT_CHUNK'],'p')
 it=r.iter_content();seen=next(it);checks['chunk_terminal_custody_before_yield']=op.done
 it.close();r.close();recs=refs(b)
 checks['chunk_terminal_tail_exact']=ops.read_wire(b,recs[-1][1])==first and seen==first
 # Continued drain: supplemental full wire is referenced, never second complete.
 b=fresh('drain');op,r=make(b,[first,b'\nTAIL_NEXT_CHUNK'],'p');parts=list(r.iter_content());recs=refs(b)
 checks['drained_wire_exact']=ops.read_wire(b,recs[-1][1])==b''.join(parts)
 checks['drained_one_result']=sum(kind=='result' for kind,_ in recs)==1
 checks['drained_tail_checkpoint']=any(kind=='checkpoint' for kind,_ in recs)
 checks['drained_completed']=op.done
 # Iterator closure before terminal remains uncertain; no speculative source read.
 b=fresh('prestop');op,r=make(b,[content,b'',done],'p');it=r.iter_lines();assert next(it)==content;it.close();r.close();recs=refs(b)
 checks['preterminal_uncertain']=not op.done and recs[-1][1]['status']=='UNCERTAIN'
 checks['preterminal_exact_prefix']=ops.read_wire(b,recs[-1][1])==content
 # Bare EOF/partial terminator must never become an acknowledgement.
 b=fresh('partial');op,r=make(b,[b'data: [DON'],'p');result=capture(lambda:list(r.iter_content()));recs=refs(b)
 checks['partial_terminal_refused']=not result['ok'] and not op.done
 checks['partial_terminal_uncertain']=recs[-1][1]['status']=='UNCERTAIN'
 # Pin mismatch is detected before the terminator can escape to the consumer.
 b=fresh('badpin');op,r=make(b,[done],'p');original_archive=ops.archive_wire;backups={}
 def corrupt(binding,raw,representation,status):
  receipt=original_archive(binding,raw,representation,status)
  if status=='RECEIVED':
   path=Path(receipt['ref']['path']);old=path.read_bytes();backup=path.with_suffix('.json.bak_test');backup.write_bytes(old);backups[path]=old;path.write_bytes(old+b' ')
  return receipt
 ops.archive_wire=corrupt
 failed=capture(lambda:next(r.iter_lines()))
 ops.archive_wire=original_archive
 for path,old in backups.items():path.write_bytes(old)
 checks['bad_pin_blocks_terminal_delivery']=not failed['ok'] and not op.done
 checks['bad_pin_no_completed_result']=not any(kind=='result' for kind,_ in refs(b))
 cases['badpin']=failed
 # Two provider tool rounds, a local sandbox result, final provider response,
 # and the complete observe_stream wrapper: all real local custody APIs.
 b=fresh('tools');providers=[]
 def flow():
  for i in range(2):
   op,r=make(b,[b'data: {"choices":[{"delta":{"tool_calls":[{"id":"local"}]}}]}',b'',done],'provider')
   providers.append(op)
   with r:
    for line in r.iter_lines():
     if line==done:break
   with ops.operation(b,'sandbox',key=str(i)) as sandbox:
    sandbox.complete({'synthetic':True,'stdout':str((i+1)*2),'remote':False})
  op,r=make(b,[content,b'',done],'provider');providers.append(op)
  with r:
   for line in r.iter_lines():
    if line==done:break
    if line.startswith(b'data:'):yield line.decode()+'\n\n'
  yield 'data: [DONE]\n\n'
 result=capture(lambda:list(m.observe_stream(flow(),b)))
 snap=b.snapshot();provider_ids={p.id for p in providers};handles=snap['p']['handles']
 checks['two_round_full_observe_stream']=result['ok'] and result['value'][-1]=='data: [DONE]\n\n'
 checks['all_provider_ops_completed']=len(providers)==3 and all(p.done for p in providers)
 checks['root_response_done']=b._lifecycle.response.done
 checks['all_operations_completed']=all(h['status']=='completed' for h in handles if h.get('kind')=='activity_operation')
 checks['semantic_answer_full']=any(r['text']=='Luz' and r['statute']=='DECLARADO' for r in snap['q']['records'])
 checks['review_pending_not_accepted']=any(t['status']=='review_pending' for t in b.activity.controller.project(max_chars=100000)['projection']['active'])
 cases['tools']={'result':result,'provider_count':len(providers),'response_done':b._lifecycle.response.done}
 assert all(checks.values()),{k:v for k,v in checks.items() if not v}
report={'status':'NATIVE_REGRESSION_REPRODUCED' if native else 'PASS','checks':checks,'cases':cases,'provider_calls':0,'runtime_installation':False,'scope':'Only production iald_activity_operations.py changed in staging; actual installed app/shared runtime used in isolated fresh contexts.'}
path=W/('terminal_R4_native.json' if native else 'terminal_R4_tests.json')
with path.open('x',encoding='utf-8') as f:json.dump(report,f,ensure_ascii=False,indent=2)
print(json.dumps({'status':report['status'],'checks':len(checks),'module':ops.__file__}))
