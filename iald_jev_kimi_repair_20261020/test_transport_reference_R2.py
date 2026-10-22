"""Actual isolated MemoryStore/ActivityRuntime + future transport references. No network."""
import os,sys,json,sqlite3,hashlib,types,traceback
from pathlib import Path
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent;STAGE=W/'admission_staging_R2';ISO=W/'i2';ISO.mkdir(exist_ok=False)
R=Path(r'C:\IALD\projetos_pyhton\IALD');sys.path[:0]=[str(STAGE),str(R)]
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
from iald_memory import guard
from iald_memory.activity import KEY
checks={};cases={}
def fresh(name):
 root=ISO/name;m._SHARED_ROOT=root
 b=m.begin(R,'synthetic-sidecar','transport_'+name,[{'role':'user','content':'Teste local de transporte sem provedor.'}],request_id='local_'+name)
 return b
def operation(b,key):return b._lifecycle.start('local_transport',key=key)
def response(op):return ops.Response(types.SimpleNamespace(status_code=200,headers={'Content-Type':'text/event-stream'}),op,expect_sse=True)
def capture(fn):
 try:return {'ok':True,'value':fn()}
 except Exception as e:return {'ok':False,'exception':type(e).__name__,'message':str(e),'code':getattr(e,'code',None),'traceback':traceback.format_exc()}
def refs(b):
 out=[]
 for r in b.snapshot()['q']['records']:
  data=r.get('meta',{}).get(KEY,{})
  if data.get('kind')=='result':
   val=data['data']['result'];rec=val.get('response') if isinstance(val,dict) else None
   if isinstance(rec,dict) and rec.get('protocol')==ops.WIRE_REF_PROTOCOL:out.append(rec)
  try:v=json.loads(r['text'])
  except ValueError:continue
  if isinstance(v,dict) and isinstance(v.get('transport'),dict):out.append(v['transport'])
 return out
wire='data: {"content":"Luz: á é 𐀀"}\r\n\r\ndata: [DONE]\r\n\r\n'.encode()
for name,chunks,expected,success,lines in [
 ('complete',[wire],wire,True,False),
 ('split',[wire[i:i+1] for i in range(len(wire))],wire,True,False),
 ('truncated',[wire.split(b'data: [DONE]')[0]],wire.split(b'data: [DONE]')[0],False,False),
 ('invalid_utf8',[b'data: {"content":"\xc3'],b'data: {"content":"\xc3',False,False),
 ('terminal_no_newline',[b'data: [DONE]'],b'data: [DONE]',True,False),
 ('lines',[b'data: {"text":"ok"}',b'',b'data: [DONE]',b''],b'data: {"text":"ok"}\n\ndata: [DONE]\n',True,True),
 ('trailing_usage',[wire,b'data: {"usage":{"total_tokens":1}}\n\n'],wire+b'data: {"usage":{"total_tokens":1}}\n\n',True,False),
]:
 b=fresh(name);op=operation(b,'1');wrapped=response(op)
 result=capture(lambda:list(wrapped._iterate(iter(chunks),lines=lines)))
 recs=refs(b);assert recs,(name,result)
 receipt=recs[-1];restored=ops.read_wire(b,receipt)
 checks[name+'_exact_bytes']=restored==expected
 checks[name+'_status']=receipt['status']==('RECEIVED' if success else 'UNCERTAIN')
 checks[name+'_done_state']=op.done is success
 checks[name+'_result']=result['ok'] is success
 state=b.snapshot()
 checks[name+'_no_inline_wire']=all('wire_utf8' not in r['text'] and 'wire_base64' not in r['text'] and 'received_text' not in r['text'] for r in state['q']['records'])
 cases[name]={'receipt':receipt,'exception':None if result['ok'] else result,'q_records':len(state['q']['records'])}
 # Public iterator still yields exactly the caller's bytes/line objects.
 if success:checks[name+'_outward_chunks_unchanged']=result['value']==chunks
# Use the original preserved wire as a fixture, without decoding/copying live DB.
with sqlite3.connect((W/'isolated'/'baseline'/'memory.sqlite3').as_uri()+'?mode=ro',uri=True) as db:
 st=json.loads(db.execute('select state_json from context_state').fetchone()[0])
 values=[]
 for r in st['q']['records']:
  try:v=json.loads(r['text'])
  except ValueError:continue
  if isinstance(v,dict) and len(v.get('received_text',''))>100000:values.append(v['received_text'])
 raw=values[0].encode('utf-8')
b=fresh('large_wire');before=b.snapshot();counts=[]
for k in range(3):
 op=operation(b,str(k));wrapped=response(op)
 list(wrapped._iterate(iter([raw]),lines=False))
 receipt=refs(b)[-1];checks['large_wire_'+str(k)+'_full_bytes']=ops.read_wire(b,receipt)==raw
 counts.append(len(json.dumps(b.snapshot()['q'],ensure_ascii=False).encode()))
after=b.snapshot();growth=counts[-1]-len(json.dumps(before['q'],ensure_ascii=False).encode())
checks['bounded_three_large_transports']=growth<60000
checks['one_wire_artifact_deduplicated']=len({r['ref']['path'] for r in refs(b)})==1
checks['legacy_snapshot_untouched']=len(st['q']['records'])==29
cases['large_wire']={'wire_bytes':len(raw),'q_growth_three_calls_bytes':growth,'q_sizes':counts,'ref':receipt}
# Actual artifact adulteration, with byte backup, must prevent false completion.
b=fresh('tamper');op=operation(b,'1');receipt=ops.archive_wire(b,wire,'test exact bytes','RECEIVED')
path=Path(receipt['ref']['path']);original=path.read_bytes();backup=path.with_suffix('.json.bak_test');backup.write_bytes(original);path.write_bytes(original+b' ')
bad=capture(lambda:op.complete({'http_status':200,'response':receipt},terminal=False))
checks['tampered_ref_false_ack_denied']=not bad['ok'] and bad['message']=='Transport artifact hash mismatch'
checks['tampered_ref_not_done']=not op.done
checks['tampered_ref_no_result']=not refs(b)
path.write_bytes(original)
wrong=dict(receipt,bytes=receipt['bytes']+1);bad_size=capture(lambda:ops.read_wire(b,wrong))
checks['false_size_denied']=not bad_size['ok'] and bad_size['message']=='Transport wire hash/size mismatch'
other=fresh('wrong_scope');wrong_scope=capture(lambda:ops.read_wire(other,receipt))
checks['foreign_scope_ref_denied']=not wrong_scope['ok']
# The reader still verifies scope even for a file moved into the current root.
copy=other.activity.artifacts/path.name;copy.parent.mkdir(exist_ok=True);copy.write_bytes(original)
scoped=dict(receipt,ref=dict(receipt['ref'],path=str(copy)))
wrong_scope2=capture(lambda:ops.read_wire(other,scoped))
checks['copied_foreign_scope_ref_denied']=not wrong_scope2['ok'] and wrong_scope2['message']=='Transport artifact scope mismatch'
cases['tamper']={'false_ack':bad,'false_size':bad_size,'foreign_scope':wrong_scope2}
# Wire reception never accepts the activity or final semantic answer.
checks['semantic_acceptance_not_inferred']=all(r.get('meta',{}).get(KEY,{}).get('kind')!='accepted' for r in after['q']['records'])
assert all(checks.values()),{k:v for k,v in checks.items() if not v}
report={'status':'PASS','checks':checks,'checks_passed':len(checks),'cases':cases,'provider_calls':0,'installed':False,'artifact_contract':'Scoped immutable UTF8 wire (or explicitly invalid UTF8 base64), full SHA256 and exact bytes; compact q receipt; verified read before acknowledging custody.','limits':['iter_lines preserves returned line values joined by LF, not unavailable original HTTP delimiters.','Complete SSE custody occurs on source exhaustion after a terminal frame; interrupted consumers remain UNCERTAIN.','observe_stream semantic text unchanged; original records never rewritten.']}
with (W/'transport_reference_tests_R2.json').open('x',encoding='utf-8') as f:json.dump(report,f,ensure_ascii=False,indent=2)
print(json.dumps({'status':'PASS','checks':len(checks),'large_wire_bytes':len(raw),'q_growth_three_calls_bytes':growth}))
