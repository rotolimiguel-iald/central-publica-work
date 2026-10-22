from pathlib import Path
import concurrent.futures as futures
import datetime, hashlib, json, os, re, subprocess, sys, time, uuid

ROOT=Path(__file__).resolve().parent
AUTHOR=ROOT.parent/'TETELESTAI_V351_FECHO_MATEMATICO'/'A2_012'
BASE=AUTHOR.parent/'RETOMADA_A1B_012'/'k'
SRC=ROOT/'src'
OUT=ROOT/'build'
CACHE=ROOT/'accepted_cache'
BIN=Path(r'C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin')
NAMES=['V354FiniteTraceSupport','V354SpectralThreshold','V354RegularMatrixCorner',
       'V354FiniteEqualSplit','V354NormalizedSplit','V354RegularSupport','V354PositiveTraceReader','V354TraceReaderWall']
MODULES=['TGL.CoreSupport']+['TGLExt.'+n for n in NAMES]
ALLOWED={'propext','Classical.choice','Quot.sound'}
sys.stdout.reconfigure(encoding='utf-8')

def stamp(): return datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%d_%H%M%S_%f')
def info(p):
    p=Path(p); b=p.read_bytes()
    return dict(path=str(p.resolve()),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
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
    assert tmp.stat().st_size==len(b)
    os.replace(tmp,p); assert p.read_bytes()==b
def record(p,d): write(p,json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def code_only(s):
    # Remove comments, including nested blocks, and quoted strings.
    out=[]; i=0; depth=0; quote=False
    while i<len(s):
        c=s[i]; pair=s[i:i+2]
        if depth:
            if pair=='/-': depth+=1; out.extend('  '); i+=2; continue
            if pair=='-/': depth-=1; out.extend('  '); i+=2; continue
            out.append('\n' if c=='\n' else ' '); i+=1; continue
        if quote:
            if c=='\\': out.extend('  '); i+=2; continue
            if c=='"': quote=False
            out.append('\n' if c=='\n' else ' '); i+=1; continue
        if pair=='/-': depth=1; out.extend('  '); i+=2; continue
        if pair=='--':
            end=s.find('\n',i); end=len(s) if end<0 else end
            out.extend(' '*(end-i)); i=end; continue
        if c=='"': quote=True; out.append(' '); i+=1; continue
        out.append(c); i+=1
    assert not depth and not quote
    return ''.join(out)
def imports(p): return re.findall(r'^\s*(?:public\s+)?import\s+([\w.]+)',code_only(p.read_text(encoding='utf-8-sig')),re.M)
def modpath(m): return Path(*m.split('.')).with_suffix('.lean')

def prepare():
    assert not SRC.exists(), 'Require fresh review root'
    snapshots=[]; new_graph={}; deps={}; objects=[]
    for m in MODULES:
        p=AUTHOR/'src'/modpath(m); q=SRC/modpath(m)
        write(q,p.read_bytes()); snapshots.append(dict(module=m,source=info(p),copy=info(q)))
        new_graph[m]=[n for n in imports(q) if n in MODULES]
    assert (SRC/'TGL'/'CoreSupport.lean').read_bytes()==(BASE/'TGL'/'CoreSupport.lean').read_bytes()
    def dependency(m):
        if m in MODULES or m in deps or not m.startswith(('TGL.','TGLExt.')): return
        p=BASE/modpath(m)
        deps[m]=dict(source=info(p),imports=imports(p))
        rel=Path(*m.split('.'))
        base=BASE/'.lake'/'build'/'lib'/'lean'/rel
        primary=base.with_suffix('.olean')
        assert primary.is_file(), f'Missing accepted dependency: {primary}'
        for suffix in ['.olean','.olean.private','.olean.server','.ilean','.ir']:
            src=base.with_suffix(suffix)
            if src.is_file():
                dst=(CACHE/rel).with_suffix(suffix)
                assert not dst.exists(); dst.parent.mkdir(parents=True,exist_ok=True)
                os.link(src,dst)
                a=info(src); b=info(dst)
                assert a['sha256']==b['sha256'] and os.path.samefile(src,dst)
                objects.append(dict(source=a,hardlink=b))
        for n in deps[m]['imports']: dependency(n)
    for m in MODULES:
        for n in imports(SRC/modpath(m)): dependency(n)
    for rel in ['REAPROVEITAMENTO_A2.md','REAPROVEITAMENTO_A2.json','PROVENIENCIA_CORE_SUPPORT.json','REQUISITOS_ADENDO_001.json']:
        p=AUTHOR/rel; q=ROOT/'inputs'/rel
        write(q,p.read_bytes()); snapshots.append(dict(source=info(p),copy=info(q)))
    for name in ['ORDEM_011_fecho_matematico_da_realizacao_concreta.md','ORDEM_012_RECIBO_E_ADENDO_001_quarta_face_e_sequencia.md']:
        p=ROOT.parent/'TUNEL'/'PARA_CHATGPT'/name; q=ROOT/'inputs'/name
        write(q,p.read_bytes()); snapshots.append(dict(source=info(p),copy=info(q)))
    for rel in ['TGL/ContinuousCornerAbstract.lean','TGL/ModularRealization.lean',
        'TGLExt/V351RegularCoreTraceContract.lean','TGLExt/V351RegularCoreTraceConstruction.lean']:
        p=BASE/rel; q=ROOT/'inputs'/'accepted_sources'/rel
        write(q,p.read_bytes()); snapshots.append(dict(source=info(p),copy=info(q)))
    names=[]; scans=[]
    for m in MODULES:
        p=SRC/modpath(m); code=code_only(p.read_text(encoding='utf-8-sig'))
        ns=re.findall(r'^namespace\s+(\S+)',code,re.M)
        assert len(ns)==1,(m,ns)
        public=re.findall(r'^(?:noncomputable\s+)?(?:def|theorem|lemma|abbrev|structure)\s+(\w+)',code,re.M)
        names += [ns[0]+'.'+n for n in public]
        scans.append(dict(source=info(p),public_names=[ns[0]+'.'+n for n in public],
            forbidden=re.findall(r'\b(?:sorry|admit|native_decide|trustCompiler|unsafe|implemented_by|extern)\b|^\s*axiom\b',code,re.M),
            classical_occurrences=[i for i,l in enumerate(code.splitlines(),1) if re.search(r'Classical|\bclassical\b',l)],
            dimensional_occurrences=[dict(line=i,text=l.strip()) for i,l in enumerate(code.splitlines(),1) if re.search(r'FiniteDimensional|FiniteRank|Fintype|Finite ',l)],
            heartbeats=re.findall(r'set_option maxHeartbeats\s+(\d+)',code)))
    assert len(names)==len(set(names))
    audit='import TGLExt.V354PositiveTraceReader\nset_option pp.universes true\n'
    audit+='\n'.join('#check '+n+'\n#print axioms '+n for n in names)+'\n'
    audit+='\n#print TGLV350.Regular.regularNormalizedFaces\n#print TGLV350.Regular.regularContinuousCorner\n'
    write(SRC/'AuditAllPublic.lean',audit)
    record(ROOT/'INPUTS.json',dict(snapshots=snapshots,new_graph=new_graph,accepted_dependencies=deps,
        accepted_objects=objects,expected_public_names=names,
        core_support_baseline=info(BASE/'TGL'/'CoreSupport.lean'),
        excluded_unfrozen=['TGLExt.V354TraceReaderWall'],policy='A1 accepted caches read only; no accepted object overwritten or rebuilt'))
    record(ROOT/'SOURCE_SCAN.json',dict(files=scans,all_clean=all(not x['forbidden'] for x in scans)))
    (ROOT/'tmp').mkdir(exist_ok=True)
    print('New modules',len(MODULES),'public names',len(names),'accepted source modules',len(deps),'hardlinks',len(objects),flush=True)

def env():
    e=os.environ.copy(); e.pop('LEAN_SRC_PATH',None)
    paths=[OUT,CACHE]+sorted(p/'.lake/build/lib/lean' for p in (BASE/'.lake/packages').iterdir() if (p/'.lake/build/lib/lean').is_dir())
    e['LEAN_PATH']=os.pathsep.join(map(str,paths))
    e['TEMP']=e['TMP']=str(ROOT/'tmp'); e['PATH']=str(BIN)+os.pathsep+e['PATH']
    return e

def run(src,folder,output=None):
    src=Path(src); cmd=[str(BIN/'lean.exe'),'-R',str(SRC)]
    if output:
        output=Path(output); assert output.resolve().is_relative_to(OUT)
        assert not output.exists(), 'Never overwrite compiled or borrowed object'
        output.parent.mkdir(parents=True,exist_ok=True); cmd+=['-o',str(output)]
    cmd+=[str(src)]
    before=info(src); write(folder/src.name,src.read_bytes()); start=stamp(); t=time.monotonic()
    p=subprocess.run(cmd,cwd=ROOT,env=env(),capture_output=True)
    write(folder/'stdout.txt',p.stdout); write(folder/'stderr.txt',p.stderr)
    r=dict(command=cmd,cwd=str(ROOT),source=before,source_unchanged=info(src)==before,
        started_utc=start,finished_utc=stamp(),seconds=time.monotonic()-t,returncode=p.returncode,
        stdout=info(folder/'stdout.txt'),stderr=info(folder/'stderr.txt'))
    if output: r['object']=info(output) if output.exists() else None
    record(folder/'RESULT.json',r)
    return r,(p.stdout+p.stderr).decode('utf-8',errors='replace')

def build():
    data=json.loads((ROOT/'INPUTS.json').read_text(encoding='utf-8')); graph=data['new_graph']
    done=set(); rows={}
    record(ROOT/'TOOLCHAIN.json',dict(lean=info(BIN/'lean.exe'),version=subprocess.check_output([str(BIN/'lean.exe'),'--version']).decode().strip(),
        search_paths=env()['LEAN_PATH'].split(os.pathsep),temporary=str(ROOT/'tmp'),
        source_builds=MODULES,accepted_A1_rebuilt=False))
    while len(done)<len(graph):
        ready=[m for m,d in graph.items() if m not in done and set(d)<=done]
        assert ready
        def job(m):
            r,out=run(SRC/modpath(m),ROOT/'build_logs'/m,(OUT/Path(*m.split('.'))).with_suffix('.olean'))
            print(m,r['returncode'],round(r['seconds'],2),flush=True)
            if r['returncode']: print(out[-7000:],flush=True)
            return m,r
        with futures.ThreadPoolExecutor(max_workers=2) as pool: finished=list(pool.map(job,ready))
        rows.update(finished); record(ROOT/'BUILD_PROGRESS.json',rows)
        if any(r['returncode']!=0 or not r['object'] for m,r in finished): raise RuntimeError('Build failed; not proof')
        done.update(ready)
    audit,out=run(SRC/'AuditAllPublic.lean',ROOT/'build_logs'/'AuditAllPublic',OUT/'AuditAllPublic.olean')
    print('AuditAllPublic',audit['returncode'],flush=True)
    if audit['returncode']: print(out[-7000:],flush=True)
    record(ROOT/'BUILD.json',dict(modules=rows,count=len(rows),audit=audit,
        all_pass=all(r['returncode']==0 and r['source_unchanged'] for r in rows.values()) and audit['returncode']==0))
    assert audit['returncode']==0

if __name__=='__main__': {'prepare':prepare,'build':build}[sys.argv[1]]()
