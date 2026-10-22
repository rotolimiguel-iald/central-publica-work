from pathlib import Path
import datetime, hashlib, json, os, re, subprocess, sys, time, uuid

ROOT=Path(__file__).resolve().parent
PRIOR=ROOT.parent.parent
AUTHOR=PRIOR.parent/'A2_TRACE_COMPLETION_012'
BASE=PRIOR.parent/'TETELESTAI_V351_FECHO_MATEMATICO'/'RETOMADA_A1B_012'/'k'
BIN=Path(r'C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin')
SRC=ROOT/'src'; OUT=ROOT/'build'
MODULES=['V354TraceShiftEquivalence','V354CyclicTraceCompletion','V354BoundedPolar',
    'V354SelfAdjointPowerKernel','V354PolarIntertwining','V354PositiveTraceTransport','V354PositiveShiftCompatibility']
ALLOWED={'propext','Classical.choice','Quot.sound'}
sys.stdout.reconfigure(encoding='utf-8')

def stamp(): return datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%d_%H%M%S_%f')
def info(p):
    p=Path(p); b=p.read_bytes()
    return dict(path=str(p.resolve()),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def current(r): return info(r['path'])==r
def write(p,b):
    p=Path(p); assert p.resolve().is_relative_to(ROOT)
    if isinstance(b,str): b=b.encode('utf-8')
    p.parent.mkdir(parents=True,exist_ok=True)
    if p.exists():
        old=p.read_bytes(); backup=p.with_name(p.name+'.bak_'+stamp())
        with backup.open('xb') as f: f.write(old)
        assert backup.read_bytes()==old
    tmp=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex)
    with tmp.open('xb') as f: f.write(b); f.flush(); os.fsync(f.fileno())
    assert tmp.stat().st_size==len(b); os.replace(tmp,p); assert p.read_bytes()==b
def record(p,d): write(p,json.dumps(d,ensure_ascii=False,indent=2)+'\n')

def code_only(text):
    result=[]; i=0; depth=0; string=False
    while i<len(text):
        if depth:
            if text[i:i+2]=='/-': depth+=1; i+=2
            elif text[i:i+2]=='-/': depth-=1; i+=2
            else:
                if text[i]=='\n': result.append('\n')
                i+=1
        elif string:
            if text[i]=='\\': i+=2
            elif text[i]=='"': string=False; i+=1
            else: i+=1
        elif text[i:i+2]=='/-': depth=1; result.append(' '); i+=2
        elif text[i:i+2]=='--':
            j=text.find('\n',i); i=len(text) if j<0 else j
        elif text[i]=='"': string=True; result.append(' '); i+=1
        else: result.append(text[i]); i+=1
    assert depth==0 and not string
    return ''.join(result)

def prepare():
    assert not SRC.exists() and not OUT.exists()
    prior_manifest=read(PRIOR/'MANIFESTO_A2.json'); prior_seal=read(PRIOR/'SELO_A2.json')
    prior_items=prior_manifest['files']+prior_manifest['new_objects']+prior_seal['files']
    assert all(current(x) for x in prior_items)
    snapshots=[]; names=[]; graph={}; scan=[]
    for m in MODULES:
        p=AUTHOR/'src'/'TGLExt'/(m+'.lean'); q=SRC/'TGLExt'/p.name
        before=info(p); code=p.read_text(encoding='utf-8'); write(q,p.read_bytes()); assert current(before)
        clean=code_only(code)
        public=re.findall(r'^(?:noncomputable\s+)?(?:def|theorem|lemma|abbrev|structure)\s+(\w+)',clean,re.M)
        qualified=[]
        for n in public:
            ns='TGLV354.' if m=='V354BoundedPolar' else 'TGLV354.TraceCompletion.'
            if m=='V354TraceShiftEquivalence' and n!='ShiftRelated': ns+='ShiftRelated.'
            qualified.append(ns+n)
        names+=qualified
        forbidden=re.findall(r'\b(?:sorry|admit|native_decide|trustCompiler|unsafe|implemented_by|extern)\b|^\s*axiom\b',clean,re.M)
        assert not forbidden
        graph['TGLExt.'+m]=[n for n in re.findall(r'^import\s+(\S+)',code,re.M) if n.startswith('TGLExt.V354')]
        snapshots.append(dict(module='TGLExt.'+m,source=before,copy=info(q)))
        scan.append(dict(source=info(q),public_names=qualified,forbidden=forbidden,
            private_names=re.findall(r'^private\s+(?:def|theorem|lemma)\s+(\w+)',clean,re.M)))
    assert len(names)==len(set(names))
    assert all(dep in graph for deps in graph.values() for dep in deps)
    prov=read(AUTHOR/'PROVENIENCIA_POLAR.json')
    original=Path(prov['source']); copied=Path(prov['copy'])
    assert original.read_bytes()==copied.read_bytes()==(SRC/'TGLExt/V354BoundedPolar.lean').read_bytes()
    assert info(original)['bytes']==prov['bytes'] and info(original)['sha256']==prov['sha256']
    provenance=dict(claims=prov,original=info(original),author_copy=info(copied),independent_copy=info(SRC/'TGLExt/V354BoundedPolar.lean'))
    write(ROOT/'inputs/PROVENIENCIA_POLAR.json',(AUTHOR/'PROVENIENCIA_POLAR.json').read_bytes())
    links=[]
    for r in read(PRIOR/'INPUTS.json')['accepted_objects']:
        assert current(r['source']) and current(r['hardlink'])
        p=Path(r['hardlink']['path']); q=OUT/p.relative_to(PRIOR/'accepted_cache')
        assert not q.exists(); q.parent.mkdir(parents=True,exist_ok=True); os.link(p,q)
        links.append(dict(source=r['source'],borrowed=r['hardlink'],review=info(q)))
    for m in MODULES: assert not (OUT/'TGLExt'/(m+'.olean')).exists()
    (ROOT/'tmp').mkdir(exist_ok=True)
    write(SRC/'AuditCompatibility.lean','import TGLExt.V354PositiveShiftCompatibility\nset_option pp.universes true\n'+
        '\n'.join('#check '+n+'\n#print axioms '+n for n in names)+'\n'+
        '#print TGLV354.TraceCompletion.positiveShift_trace_compatible\n#print TGLV354.TraceCompletion.cyclicTraceCandidate_positive\n')
    record(ROOT/'INPUTS.json',dict(snapshots=snapshots,public_names=names,count=len(names),graph=graph,source_scan=scan,
        shared_polar=provenance,cache_links=links,prior_receipt=info(PRIOR/'RECIBO_REVISAO_A2.md'),prior_seal=info(PRIOR/'SELO_A2.json'),
        historical_math_review_seal=info(ROOT.parent/'SELO_DOCUMENTAL.json'),
        scope='Seven stable analytical modules only; final ContinuousCoreData assembly pending separate delivery'))
    print('Prepared',len(MODULES),'modules;',len(names),'public names;',len(links),'accepted read-only cache objects',flush=True)

def env():
    e=os.environ.copy(); e.pop('LEAN_SRC_PATH',None)
    paths=[OUT]+sorted(p/'.lake/build/lib/lean' for p in (BASE/'.lake/packages').iterdir() if (p/'.lake/build/lib/lean').is_dir())
    e['LEAN_PATH']=os.pathsep.join(map(str,paths)); e['PATH']=str(BIN)+os.pathsep+e['PATH']; e['TEMP']=e['TMP']=str(ROOT/'tmp')
    return e

def run(p,folder,out=None):
    folder.mkdir(parents=True,exist_ok=True)
    cmd=[str(BIN/'lean.exe'),'-R',str(SRC)]
    if out:
        assert out.resolve().is_relative_to(OUT) and not out.exists(); out.parent.mkdir(parents=True,exist_ok=True)
        cmd+=['-o',str(out)]
    cmd+=[str(p)]; before=info(p); write(folder/p.name,p.read_bytes()); started=stamp(); t=time.monotonic()
    r=subprocess.run(cmd,cwd=ROOT,env=env(),capture_output=True)
    write(folder/'stdout.txt',r.stdout); write(folder/'stderr.txt',r.stderr)
    row=dict(command=cmd,cwd=str(ROOT),started_utc=started,finished_utc=stamp(),seconds=time.monotonic()-t,
        source=before,source_unchanged=current(before),returncode=r.returncode,
        stdout=info(folder/'stdout.txt'),stderr=info(folder/'stderr.txt'))
    if out: row['object']=info(out) if out.exists() else None
    record(folder/'RESULT.json',row)
    return row,(r.stdout+r.stderr).decode('utf-8',errors='replace')

def build():
    d=read(ROOT/'INPUTS.json'); done=set(); results={}
    record(ROOT/'TOOLCHAIN.json',dict(lean=info(BIN/'lean.exe'),version=subprocess.check_output([str(BIN/'lean.exe'),'--version']).decode().strip(),
        lean_path=env()['LEAN_PATH'].split(os.pathsep),cache_policy='A1/Mathlib cached, not rebuilt; seven reviewed V354 built from private snapshots without their prior objects'))
    while len(done)<len(d['graph']):
        ready=[m for m,deps in d['graph'].items() if m not in done and set(deps)<=done]; assert ready
        for m in ready:
            p=SRC/Path(*m.split('.')).with_suffix('.lean')
            r,output=run(p,ROOT/'build_logs'/m,OUT/Path(*m.split('.')).with_suffix('.olean'))
            results[m]=r; record(ROOT/'BUILD_PROGRESS.json',results); print(m,r['returncode'],round(r['seconds'],2),flush=True)
            if r['returncode'] or not r['object']: print(output[-6000:],flush=True); raise RuntimeError('Build failed; not proof')
            done.add(m)
    audit,output=run(SRC/'AuditCompatibility.lean',ROOT/'build_logs/AuditCompatibility',OUT/'AuditCompatibility.olean')
    record(ROOT/'BUILD.json',dict(modules=results,audit=audit))
    print('Independent all-name audit',audit['returncode'],flush=True)
    if audit['returncode']: print(output[-6000:]); raise RuntimeError('Audit failed')

if __name__=='__main__': {'prepare':prepare,'build':build}[sys.argv[1]]()
