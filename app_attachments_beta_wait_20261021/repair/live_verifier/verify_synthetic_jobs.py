"""Single read-only snapshot of two pinned synthetic jobs. No wait/retry/HTTP."""
from pathlib import Path
from datetime import datetime,timezone
import argparse,ast,ctypes,hashlib,json,os,sqlite3,sys,unicodedata
from ctypes import wintypes
HERE=Path(__file__).resolve().parent
R=Path(r'C:/IALD/projetos_pyhton/IALD')
TERMINAL={'completed','failed','cancelled','interrupted','expired'}
def pin(p):
 raw=Path(p).read_bytes();return {'path':str(p),'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw)}
def connect(p):
 db=sqlite3.connect(Path(p).resolve().as_uri()+'?mode=ro',uri=True,timeout=3);db.execute('PRAGMA query_only=ON');db.row_factory=sqlite3.Row;return db

def cipher_only():
 # ChatJobs construction/import is forbidden: its startup mutates job state.
 source=(R/'iald_chat_jobs.py').read_text(encoding='utf-8');tree=ast.parse(source)
 node=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=='WindowsCipher')
 ns={'os':os,'ctypes':ctypes,'wintypes':wintypes};exec(compile(ast.Module(body=[node],type_ignores=[]),'cipher-class-only','exec'),ns)
 return ns['WindowsCipher']()

def collect(scope):
 ids=[j['id'] for j in scope['jobs']];jobs=[];owners=[];now=datetime.now(timezone.utc);cipher=None
 with connect(R/'.iald_runtime/chat_jobs/jobs.sqlite3') as db:
  # No discovery query and no read of other jobs in this verifier.
  for target in scope['jobs']:
   row=db.execute('SELECT id,owner,status,created,updated,acknowledged,cancel_requested,seq,size,expired FROM jobs WHERE id=?',(target['id'],)).fetchone()
   if row is None:raise RuntimeError('Pinned synthetic job missing')
   if abs(row['created']-target['created'])>.001:raise RuntimeError('Pinned synthetic timestamp changed')
   owners.append(row['owner']);meta={k:row[k] for k in row.keys() if k!='owner'}
   meta['created_local']=datetime.fromtimestamp(row['created']).astimezone().isoformat();meta['updated_local']=datetime.fromtimestamp(row['updated']).astimezone().isoformat();meta['elapsed_job_seconds']=round(row['updated']-row['created'],3)
   observation={'role':target['role'],'job':meta,'terminal':row['status'] in TERMINAL}
   if observation['terminal'] and not row['expired']:
    if cipher is None:cipher=cipher_only()
    model_ids=set();warnings=[];fragments=[];done=False;events=[]
    for event in db.execute('SELECT seq,data FROM events WHERE job=? ORDER BY seq',(target['id'],)):
     encrypted=bytes(event['data']);raw=cipher.open(encrypted);text=raw.decode('utf-8');events.append({'seq':event['seq'],'cipher_sha256':hashlib.sha256(encrypted).hexdigest(),'plain_sha256':hashlib.sha256(raw).hexdigest(),'plain_bytes':len(raw)})
     if text.strip()=='[DONE]':done=True;continue
     value=json.loads(text)
     if isinstance(value.get('iald_modelo'),dict):model_ids.add(str(value['iald_modelo'].get('id','')))
     warning=value.get('iald_aviso')
     if isinstance(warning,dict):
      # Exact known public error only; arbitrary warning text is not exported.
      msg=str(warning.get('texto',''));item={'tipo':warning.get('tipo'),'text_sha256':hashlib.sha256(msg.encode()).hexdigest()}
      if msg=='Entrada/preços não verificáveis; envio bloqueado.':item['known_public_text']=msg
      warnings.append(item)
     for choice in value.get('choices',[]):
      part=(choice.get('delta') or {}).get('content')
      if isinstance(part,str):fragments.append(part)
    answer=''.join(fragments);fold=unicodedata.normalize('NFKC',answer).casefold()
    observation['events']={'pins':events,'done_marker':done,'models':sorted(model_ids),'warnings':warnings,'answer_utf8_bytes':len(answer.encode()),'answer_sha256':hashlib.sha256(answer.encode()).hexdigest(),'expected_terms_presence':{'vermelho':'vermelh' in fold,'azul':'azul' in fold,'ANEXO-73':'anexo-73' in fold},'term_check_scope':'Lexical fixture check only; semantic/UI review remains parent-owned. No response text exported.'}
   else:observation['events_status']='Not decrypted: job not terminal or events expired. No wait/retry.'
   # Direct task_id ownership in monthly wallet, no account-wide scans.
   with connect(R/'.iald_runtime/monthly_wallet/wallet.sqlite3') as wallet:
    task=wallet.execute('SELECT task_id,status,admitted,created_at,finished_at FROM tasks WHERE task_id=?',(target['id'],)).fetchone()
    calls=[dict(x) for x in wallet.execute('SELECT event_id,cap,provider,model,billing_basis,status,created_at,settled_at FROM calls WHERE task_id=? ORDER BY seq',(target['id'],))]
    costs=[dict(x) for x in wallet.execute("SELECT event_id,delta,provider,model,cost_status,effective_at FROM entries WHERE task_id=? AND kind='cost' ORDER BY seq",(target['id'],))]
    observation['wallet']={'link':'Exact task_id=job_id','task':dict(task) if task else None,'calls':calls,'cost_entries':costs,'recorded_debit_nano_usd':-sum(x['delta'] for x in costs) if task else None,'pending_calls':sum(x['status']=='pending' for x in calls),'not_invoice':True,'cost_units':'calls.cap and entries.delta are integer nanoUSD; no account balances/identity exported'}
   # Provider metrics have no job ID: retain narrow attribution explicitly.
   start=datetime.fromtimestamp(row['created'],timezone.utc).isoformat();end=datetime.fromtimestamp(row['updated'] if observation['terminal'] else now.timestamp(),timezone.utc).isoformat()
   with connect(R/'.iald_runtime/app_evaluation/metrics.sqlite3') as metrics:
    fields=['provider','model','utc','status','error_code','elapsed_seconds','first_text_seconds','calls','protocol','modality_counts']
    columns=','.join("json_extract(data,'$."+f+"') AS "+f for f in fields)
    found=[]
    for metric in metrics.execute('SELECT id,'+columns+" FROM turns WHERE json_extract(data,'$.utc') BETWEEN ? AND ? AND json_extract(data,'$.provider')='mimo'",(start,end)):
     d=dict(metric)
     for key in ['calls','protocol','modality_counts']:
      if isinstance(d[key],str):d[key]=json.loads(d[key])
     # Persist whitelisted numerical/protocol metrics only, never arbitrary errors/text.
     if isinstance(d.get('calls'),list):
      allowed={'status','input_bytes_bound','output_reserved_tokens','input_tokens','output_tokens','cached_tokens','cost_estimate_usd','usage'}
      d['calls']=[{k:v for k,v in c.items() if k in allowed and (k!='usage' or v is None)} for c in d['calls'] if isinstance(c,dict)]
     found.append(d)
    observation['provider_metrics']={'link':'TEMPORAL_CORRELATION_ONLY_NOT_DIRECT_JOB_KEY','time_window_utc':[start,end],'candidate_count':len(found),'records':found if len(found)==1 else [],'status':'Unique temporal candidate; not proven exact job linkage' if len(found)==1 else 'Ambiguous/absent; no metric attribution made'}
   jobs.append(observation)
 if len(set(owners))!=1:raise RuntimeError('Synthetic pair owner mismatch; refuse output')
 return {'status':'TERMINAL_PAIR' if all(x['terminal'] for x in jobs) else 'OBSERVED_PENDING_NO_WAIT','observed_at_utc':now.isoformat(),'scope_pin':pin(HERE/'SCOPE.json'),'verifier_pin':pin(__file__),'runtime_source_pins':[pin(R/n) for n in ['iald_chat_jobs.py','iald_app_providers.py','iald_app_spend.py']],'same_job_owner':True,'jobs':jobs,'privacy':'No request payload/private conversations/response text/credentials exported. Only exact pinned synthetic events decrypted after terminal. No other job events opened.','effects':'SQLite mode=ro + PRAGMA query_only; no live imports/ChatJobs instance; no HTTP/provider/retry/waitloop/production writes.','pending_action':'Parent validates DOM and identity. If pending, run once explicitly later with a new output filename; this script never schedules/repeats.'}

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--output',required=True);args=parser.parse_args();out=Path(args.output).resolve()
 if not out.is_relative_to(HERE.resolve()) or out.exists():raise RuntimeError('New receipt must remain in own verifier directory')
 scope=json.loads((HERE/'SCOPE.json').read_text(encoding='utf-8'));result=collect(scope)
 raw=json.dumps(result,ensure_ascii=False,indent=2).encode();tmp=out.with_suffix('.tmp');
 with tmp.open('xb') as f:f.write(raw)
 assert tmp.read_bytes()==raw;tmp.replace(out)
 print(json.dumps({'status':result['status'],'output':str(out),'sha256':hashlib.sha256(raw).hexdigest(),'jobs':[{'id':j['job']['id'],'status':j['job']['status'],'terminal':j['terminal']} for j in result['jobs']]},ensure_ascii=False))
if __name__=='__main__':main()
