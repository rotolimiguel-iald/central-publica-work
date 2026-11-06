"""Record exact candidate pins and a synthetic-only subprocess test transcript."""
from pathlib import Path
import datetime,subprocess,hashlib,json,sys
ROOT=Path(__file__).resolve().parents[1]
label=sys.argv[1] if len(sys.argv)>1 else datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
if not label.replace('_','').isalnum():raise ValueError('bad artifact label')
paths=[ROOT/'candidate'/n for n in ('um_bancada.py','bancada/canonical.py','bancada/gw.py','bancada/gw_stack.py')]+[ROOT/'tests_core'/'test_core_synthetic.py']
def pins():return [{'path':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size} for p in paths]
before=pins();start=datetime.datetime.now(datetime.timezone.utc)
cmd=[sys.executable,'-B','-X','utf8',str(ROOT/'tests_core'/'test_core_synthetic.py')]
r=subprocess.run(cmd,capture_output=True,text=True,encoding='utf-8');end=datetime.datetime.now(datetime.timezone.utc);after=pins()
log=ROOT/'tests_core'/('CORE_TEST_'+label+'.log')
with log.open('x',encoding='utf-8',newline='\n') as f:f.write('COMMAND: '+repr(cmd)+'\nSTART: '+start.isoformat()+'\nEND: '+end.isoformat()+'\nSECONDS: '+str((end-start).total_seconds())+'\nEXIT: '+str(r.returncode)+'\n'+r.stdout+r.stderr)
receipt={'unit':'F0.3.B2','scope':'CANONICAL_HTTP_GW_SYNTHETIC_ONLY','command':cmd,'start':start.isoformat(),'end':end.isoformat(),'seconds':(end-start).total_seconds(),'exit':r.returncode,'source_bytes_stable_during_run':before==after,'before':before,'after':after,'log_sha256':hashlib.sha256(log.read_bytes()).hexdigest(),'original_motor_instantiated':False,'observed_test_run':False,'installed_bench_written':False}
p=ROOT/'tests_core'/('CORE_RECEIPT_'+label+'.json')
with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(receipt,f,ensure_ascii=False,indent=2);f.write('\n')
print(r.stdout+r.stderr);print(json.dumps({'receipt':str(p),'receipt_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'exit':r.returncode,'stable':before==after}))
sys.exit(r.returncode if before==after else 9)
