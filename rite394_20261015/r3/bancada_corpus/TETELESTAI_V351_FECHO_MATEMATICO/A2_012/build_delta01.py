from pathlib import Path
import subprocess,sys,json,hashlib,datetime,os,re
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'delta01_build'
OUT.mkdir(exist_ok=False)
plan=json.loads((ROOT/'AUDIT_NAMES_DELTA01.json').read_text(encoding='utf8'))
mods=[Path(s['path']).stem for s in plan['sources']]+['AuditA2RegularSupport']
def pin(p):
    b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def put(p,obj):
    assert not p.exists()
    b=json.dumps(obj,ensure_ascii=False,indent=2).encode('utf8')
    t=p.with_suffix(p.suffix+'.tmp');t.write_bytes(b);assert t.read_bytes()==b;os.replace(t,p)
rows=[]
for m in mods:
    run=subprocess.run([sys.executable,'-X','utf8','-B',str(ROOT/'dev_lean.py'),m],
        cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    log=OUT/(m+'.txt');log.write_bytes(run.stdout)
    attempt=Path(run.stdout.decode('utf8').splitlines()[0])
    assert attempt.is_relative_to(ROOT/'attempts')
    receipt=json.loads((attempt/'RESULT.json').read_text(encoding='utf8'))
    row=dict(module=m,returncode=run.returncode,receipt=pin(attempt/'RESULT.json'),log=pin(log))
    put(OUT/(m+'.json'),row);rows.append(row)
    print(json.dumps(dict(module=m,returncode=run.returncode)),flush=True)
    if run.returncode!=0 or not receipt['source_unchanged']:
        put(OUT/'FAILED.json',dict(rows=rows));sys.exit(1)

audit=json.loads(Path(rows[-1]['receipt']['path']).read_text(encoding='utf8'))
text=Path(audit['stdout']['path']).read_text(encoding='utf8')
entries=re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]",text)
assert [n for n,_ in entries]==plan['names']
allowed={'propext','Classical.choice','Quot.sound'}
assert all({x.strip() for x in a.split(',') if x.strip()}<=allowed for _,a in entries)
for s in plan['sources']: assert {k:s[k] for k in ('path','bytes','sha256')}==pin(Path(s['path']))
put(OUT/'RESULT.json',dict(timestamp=datetime.datetime.now().astimezone().isoformat(),
    all_compiled=True,public_names=len(entries),all_axioms_allowed=True,rows=rows,
    sources=[pin(Path(s['path'])) for s in plan['sources']],
    previous_controls='Historical controls retained: deletion of unused corollaries changes no surviving statement or proof body; independent delta review determines additional checks.',
    independent_review=False,gate_changed=False))
print(json.dumps(dict(result=pin(OUT/'RESULT.json'),public_names=len(entries)),ensure_ascii=False),flush=True)
