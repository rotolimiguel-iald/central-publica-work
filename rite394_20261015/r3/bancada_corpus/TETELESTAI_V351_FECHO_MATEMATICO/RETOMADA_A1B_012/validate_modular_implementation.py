from pathlib import Path
import datetime,json,os,subprocess,time,sys
R=Path(__file__).resolve().parent
A=R/'modular_implementation_validation'/datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f');A.mkdir(parents=True)
def put(p,b):
    assert p.is_relative_to(R) and not p.exists(),p
    q=p.with_name(p.name+'.tmp');q.write_bytes(b);assert q.read_bytes()==b;os.replace(q,p)
print(A,flush=True)
print('Waiting for previous sequential validation; no parallel Lake in k.',flush=True)
ready=R/'AUDITORIA_VETORES_FIXOS_MODULARES_A1B.json'
failed=R/'sequential_validation/20260914_183919_757182/failed.json'
while not ready.exists():
    if failed.exists() or any((R/'positive_graph_validation').glob('*/blocked.json')) or any(__import__('json').loads(p.read_text(encoding='utf8')).get('returncode',0) != 0 for p in (R/'positive_graph_validation').glob('*/*.json') if p.name in ('build.json','audit.json')):
        put(A/'blocked.json',json.dumps(dict(reason='Previous author validation failed',path=str(failed))).encode('utf8'))
        sys.exit(2)
    time.sleep(5)
assert json.loads(ready.read_text(encoding='utf8'))['all_axioms_allowed']
before=set((R/'modular_implementation_attempts').glob('*/run.json'))
def step(label,script,args=()):
    print('START',label,flush=True)
    cmd=[r'C:\Python314\python.exe','-X','utf8','-B',str(R/script),*args]
    p=subprocess.run(cmd,cwd=R,capture_output=True)
    put(A/(label+'.stdout.txt'),p.stdout);put(A/(label+'.stderr.txt'),p.stderr)
    put(A/(label+'.json'),json.dumps(dict(command=cmd,returncode=p.returncode)).encode('utf8'))
    print('DONE',label,p.returncode,flush=True)
    if p.returncode:
        print(p.stdout.decode('utf8',errors='replace')[-3500:]);print(p.stderr.decode('utf8',errors='replace')[-3500:]);sys.exit(p.returncode)
step('build','run_modular_implementation_replay.py')
new=set((R/'modular_implementation_attempts').glob('*/run.json'))-before;assert len(new)==1
step('audit','audit_modular_implementation.py',[new.pop().parent.name])
put(A/'complete.json',json.dumps(dict(status='AUTHOR_MODULAR_IMPLEMENTATION_VALIDATED__INDEPENDENT_REVIEW_PENDING')).encode('utf8'))
