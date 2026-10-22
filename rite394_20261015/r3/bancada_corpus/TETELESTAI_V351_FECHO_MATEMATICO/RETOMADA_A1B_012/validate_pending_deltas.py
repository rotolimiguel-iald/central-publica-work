from pathlib import Path
import datetime,hashlib,json,os,subprocess,time,sys
R=Path(__file__).resolve().parent
PY=Path(r'C:\Python314\python.exe')
def pin(p):
    b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def put(p,b):
    assert p.is_relative_to(R) and not p.exists(),p
    p.parent.mkdir(parents=True,exist_ok=True)
    q=p.with_name(p.name+'.tmp');q.write_bytes(b);assert q.read_bytes()==b;os.replace(q,p)
A=R/'sequential_validation'/datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
A.mkdir(parents=True);rows=[]
put(A/'runner.py',Path(__file__).read_bytes())
print(A,flush=True)
base=R/'attempts/20260914_173309_164705/run.json'
print('Waiting for existing cold Lake run; no duplicate build.',flush=True)
while not base.exists():time.sleep(5)
assert json.loads(base.read_text(encoding='utf8'))['returncode']==0
def step(label,script,args=()):
    cmd=[str(PY),'-X','utf8','-B',str(R/script),*args]
    print('START',label,flush=True)
    p=subprocess.run(cmd,cwd=R,capture_output=True)
    out=A/(label+'.stdout.txt');err=A/(label+'.stderr.txt')
    put(out,p.stdout);put(err,p.stderr)
    row=dict(label=label,returncode=p.returncode,command=cmd,script=pin(R/script),stdout=pin(out),stderr=pin(err))
    rows.append(row);put(A/(label+'.json'),json.dumps(row,ensure_ascii=False,indent=2).encode('utf8'))
    print('DONE',label,p.returncode,flush=True)
    if p.returncode:
        print(p.stdout.decode('utf8',errors='replace')[-3500:])
        print(p.stderr.decode('utf8',errors='replace')[-3500:])
        put(A/'failed.json',json.dumps(dict(stages=rows),ensure_ascii=False,indent=2).encode('utf8'))
        sys.exit(p.returncode)
step('orphans_audit','audit_orphans.py')
for name,folder,runner,auditor in [
    ('core','core_attempts','run_core_replay.py','audit_core.py'),
    ('absorption','absorption_attempts','run_absorption_replay.py','audit_absorption.py'),
    ('fourier','fourier_translation_attempts','run_fourier_translation_replay.py','audit_fourier_translation.py')]:
    before=set((R/folder).glob('*/run.json')) if (R/folder).exists() else set()
    step(name+'_build',runner)
    new=set((R/folder).glob('*/run.json'))-before
    assert len(new)==1,new
    attempt=new.pop()
    step(name+'_audit',auditor,[attempt.parent.name])
put(A/'complete.json',json.dumps(dict(timestamp=datetime.datetime.now().astimezone().isoformat(),status='AUTHOR_STANDALONE_DELTAS_ACCEPTED__REVIEW_AND_TRACE_PENDING',base=pin(base),stages=rows),ensure_ascii=False,indent=2).encode('utf8'))
print('ALL AUTHOR BUILDS/AUDITS COMPLETED; independent reviews remain separate.',flush=True)
