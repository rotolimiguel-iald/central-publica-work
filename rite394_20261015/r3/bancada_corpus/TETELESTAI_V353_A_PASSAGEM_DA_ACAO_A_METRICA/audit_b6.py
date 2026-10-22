from pathlib import Path
import datetime,hashlib,json,os,re,subprocess
R=Path(__file__).resolve().parent;K=R/'kernel'
BIN=Path(r'C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin')
def pin(p):
    b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def load(p):return json.loads(p.read_text(encoding='utf8'))
def put(p,b):
    assert p.is_relative_to(R) and not p.exists(),p
    q=p.with_name(p.name+'.tmp');q.write_bytes(b);assert q.read_bytes()==b;os.replace(q,p)
attempt=R/'attempts/20260914_170651_058055'
run=load(attempt/'run.json')
assert run['returncode']==0 and run['sources_unchanged_during_build']
for s in run['snapshots']:assert pin(Path(s['path']))['sha256']==s['sha256']
targets=load(R/'ALVOS_B6.json');names=[t['name'] for t in targets]
assert len(names)==len(set(names))==10
env=os.environ.copy();env.pop('LEAN_PATH',None);env.pop('LEAN_SRC_PATH',None)
env['PATH']=str(BIN)+os.pathsep+env['PATH']
A=R/'audit_B6'/datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f');A.mkdir(parents=True)
source=K/'TGLExt/AuditPassageScope.lean';put(A/source.name,source.read_bytes())
cmd=[str(BIN/'lake.exe'),'env','lean',str(source)]
p=subprocess.run(cmd,cwd=K,env=env,capture_output=True)
out=A/'AuditPassageScope.stdout.txt';err=A/'AuditPassageScope.stderr.txt'
put(out,p.stdout);put(err,p.stderr)
commands=[dict(command=cmd,label=source.stem,returncode=p.returncode,source=pin(source),stdout=pin(out),stderr=pin(err))]
put(A/'commands.json',json.dumps(commands,ensure_ascii=False,indent=2).encode('utf8'))
assert p.returncode==0
text=p.stdout.decode('utf8');parsed={}
for name,ax in re.findall(r"'([^']+)' depends on axioms:\s*\[([^]]*)\]",text,re.S):
    parsed[name]=[re.sub(r'\.\{[^}]*\}$','',a.strip()) for a in ax.split(',') if a.strip()]
for name in re.findall(r"'([^']+)' does not depend on any axioms",text):parsed[name]=[]
assert set(parsed)==set(names)
assert all(set(v)<={'propext','Classical.choice','Quot.sound'} for v in parsed.values())
code=source.read_text(encoding='utf8');clean=re.sub(r'/-.*?-/', '',code,flags=re.S);clean=re.sub(r'--[^\n]*','',clean)
assert not re.search(r'\b(sorry|axiom|native_decide|trustCompiler|admit|unsafe|theorem|lemma|def|structure)\b',clean)
proposal=load(R/'PROPOSTA_EXTERNAL_KNOWN_THEOREMS_B6.json')
entries=proposal['external_known_theorems']
assert len(entries)==4 and len({e['name'] for e in entries})==4
for e in entries:
    assert e['imported_into_witness'] is False and e['status']=='KNOWN_EXTERNAL_NOT_KERNEL_FORMALIZED'
    assert all(isinstance(e[k],str) and e[k] for k in ['citation','verified_url','exact_role','source_read_scope'])
    assert e['verified_url'].startswith(('https://arxiv.org/','https://journals.aps.org/'))
assert all(proposal[k] is False for k in ['changes_gate','implements_runtime','chooses_route'])
assert len(proposal['scope'])==11
assert all(e['status'] in {'INPUT','IMPORTED','REAL','OPEN'} and e['provider'] and e['condition'] for e in proposal['scope'])
assert sum(e['status']=='OPEN' for e in proposal['scope'])==2
custody=load(R/'CUSTODIA_V353_FONTES.json')
for f in custody['files']:assert pin(K/f['relative'])['sha256']==f['sha256'],f['relative']
assert pin(R/'um.py')['sha256']==custody['sha256']
d=dict(timestamp=datetime.datetime.now().astimezone().isoformat(),positive_build=pin(attempt/'run.json'),
    sources=[pin(source)],objects=[pin(K/'.lake/build/lib/lean/TGLExt/AuditPassageScope.olean')],
    targets=targets,axioms=parsed,all_trio=True,commands=commands,new_theorems=0,
    existing_theorems=sum(t['kind']=='theorem' for t in targets),existing_structures=sum(t['kind']=='structure' for t in targets),
    proposal=pin(R/'PROPOSTA_EXTERNAL_KNOWN_THEOREMS_B6.json'),documentary_validation=pin(R/'VALIDACAO_DOCUMENTAL_B6.json'),
    four_entries_imported_false=True,schema_checked=True,baseline_files_reverified=len(custody['files']),copied_um_unchanged=True,
    canonical_written=False,empirical_work_performed=False,new_negative_probes=False,
    scope='B6: documentary proposal plus audit of ten existing declarations; no new mathematics, runtime integration or route choice')
put(R/'AUDITORIA_B6.json',json.dumps(d,ensure_ascii=False,indent=2).encode('utf8'))
print(json.dumps(dict(all_trio=True,existing_theorems=d['existing_theorems'],existing_structures=d['existing_structures'],new_theorems=0)))
