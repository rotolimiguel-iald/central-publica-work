from pathlib import Path
from datetime import datetime
import hashlib, json, os, re, subprocess, sys, time, traceback

R=Path(r'C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012')
OLD=R.parent; SRC=OLD/'kernel'; V=R/'v'; OUT=R/'revisao'
B=OLD.parent/'TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA'
BIN=Path(r'C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin')
STAMP=datetime.now().strftime('%Y%m%d_%H%M%S_%f'); A=OUT/('independent_'+STAMP)
def now():return datetime.now().astimezone().isoformat()
def pin(p):
    b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def load(p):return json.loads(p.read_bytes())
def ck(r):assert pin(Path(r['path']))==r,r
def fresh(p,b):
    assert p.resolve().is_relative_to(OUT.resolve()) or p.resolve().is_relative_to(V.resolve()),p
    assert not p.exists(),p;p.parent.mkdir(parents=True,exist_ok=True)
    t=p.with_name(p.name+'.tmp')
    with t.open('xb') as f:f.write(b)
    assert t.read_bytes()==b;os.replace(t,p)
def save(p,d):fresh(p,(json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode('utf8'))
def uncomment(text):
    out=[];depth=0;i=0
    while i<len(text):
        if text.startswith('/-',i):depth+=1;i+=2
        elif depth and text.startswith('-/',i):depth-=1;i+=2
        elif depth:
            if text[i]=='\n':out.append('\n')
            i+=1
        elif text.startswith('--',i):
            j=text.find('\n',i);i=len(text) if j<0 else j
        else:out.append(text[i]);i+=1
    assert not depth;return ''.join(out)
def main():
    OUT.mkdir(exist_ok=True);A.mkdir();assert not V.exists(),'Do not overwrite a private project'
    recp=B/'RECIBO_B6.json';receipt=load(recp)
    ck(receipt['delivery']);ck(receipt['manifest'])
    fiche=load(R/'REAPROVEITAMENTO_RETORNO_A1B.json');targets=load(R/'ALVOS_RETORNO_A1B.json')
    assert len(targets)==40 and len({t['name'] for t in targets})==40
    assert [sum(t['kind']==k for t in targets) for k in ['theorem','def']]==[36,4]
    modules=['TGLExt.'+m['name'] for m in fiche['modules']];assert len(modules)==7
    prior=B/'revisao_b6/compilation.json';bc=load(prior)
    protected=bc['protected_pins']+[pin(prior),pin(B/'revisao_b6/REVIEW_B6_FINAL.md'),pin(B/'revisao_b6/REVIEW_B6_FINAL.json'),pin(recp),receipt['delivery'],receipt['manifest']]
    for x in bc['inherited_project_objects']:
        protected.extend([x['object'],x['trace']])
    for x in bc['objects']:protected.extend([x['own'],x['trace']])
    for p in sorted(OLD.glob('*.md'))+sorted(OLD.glob('*.json')):protected.append(pin(p))
    for p in sorted((OLD/'revisao').glob('REVIEW*')):
        if p.is_file():protected.append(pin(p))
    protected=list({p['path']:p for p in protected}.values())
    for p in protected:ck(p)
    for m in fiche['modules']:ck(m['original']);ck(m['v353']);assert Path(m['original']['path']).read_bytes()==Path(m['v353']['path']).read_bytes()
    for p in fiche['prior_fiches_and_searches']:ck(p)
    v351=[]
    for p in sorted((SRC/'TGLExt').glob('V351*.lean')):
        q=B/'kernel/TGLExt'/p.name;assert p.read_bytes()==q.read_bytes(),p
        v351.append(dict(original=pin(p),v353=pin(q)))
    assert len(v351)==19
    configs=['lakefile.toml','lake-manifest.json','lean-toolchain']
    for name in configs:
        assert (SRC/name).read_bytes()==(B/'s'/name).read_bytes(),name
        fresh(V/name,(SRC/name).read_bytes())
    sources=[];seen=set()
    def visit(mod):
        if mod in seen:return
        seen.add(mod);p=SRC/(mod.replace('.','/')+'.lean');b=p.read_bytes();code=uncomment(b.decode('utf-8-sig'));imps=[]
        for m in re.finditer(r'^\s*(?:public\s+)?import\s+([^\n]+)',code,re.M):imps+=m.group(1).split()
        for d in imps:
            if d.startswith(('TGL.','TGLExt.')) or d in ['TGL','TGLExt']:visit(d)
        q=V/p.relative_to(SRC);fresh(q,b)
        if mod in modules:
            assert not re.findall(r'\b(?:sorry|axiom|admit|native_decide|trustCompiler|unsafe)\b',code),mod
            names=re.findall(r'^#print axioms\s+(\S+)',code,re.M)
            expected=[t['name'].split('.')[-1] for t in targets if t['module']==mod.split('.')[-1]]
            assert names==expected,(mod,names,expected)
            fresh(A/p.name,b)
        sources.append(dict(module=mod,original=pin(p),copy=pin(q),imports=imps,is_target=mod in modules))
    for m in modules:visit(m)
    own=V/'TGLExt/ReviewA1Orphans.lean'
    txt='\n'.join('import '+m for m in modules)+'\n\nset_option pp.universes true\n\n'+''.join('#check '+t['name']+'\n#print axioms '+t['name']+'\n\n' for t in targets)
    fresh(own,txt.encode('utf8'))
    docs=[]
    for n in ['REAPROVEITAMENTO_RETORNO_A1B.md','REAPROVEITAMENTO_RETORNO_A1B.json','ALVOS_RETORNO_A1B.json']:
        fresh(A/n,(R/n).read_bytes());docs.append(pin(R/n))
    save(A/'source_snapshot.json',dict(timestamp=now(),modules=modules,targets=targets,sources=sources,documents=docs,own_auditor=pin(own),configs=[pin(V/n) for n in configs],original_v351=v351,protected=protected,B6_receipt=pin(recp),cache_parent_compilation=pin(prior),author_project_objects_copied=False))
    save(OUT/'SNAPSHOT_POINTER.json',dict(attempt=str(A),snapshot=pin(A/'source_snapshot.json')))
    print('SOURCES_PINNED',len(sources),'TARGETS',len(targets),'CACHE_COPY_START',str(A),flush=True)
    cache=[];manifest=load(V/'lake-manifest.json')
    for pkg in manifest['packages']:
        name=pkg['name'];source=B/'s/.lake/packages'/name;dest=V/'.lake/packages'/name;records=[]
        print('CACHE_PACKAGE_START',name,flush=True)
        for p in sorted(source.rglob('*')):
            if not p.is_file():continue
            rel=p.relative_to(source);q=dest/rel;b=p.read_bytes();fresh(q,b)
            records.append(dict(relative=str(rel),bytes=len(b),sha256=hashlib.sha256(b).hexdigest()))
        cp=A/('cache_'+name+'_pins.json');save(cp,dict(source=str(source),destination=str(dest),files=records))
        cache.append(dict(name=name,source=str(source),destination=str(dest),revision=pkg.get('rev'),files=len(records),bytes=sum(x['bytes'] for x in records),manifest=pin(cp)))
        print('CACHE_PACKAGE_DONE',name,len(records),flush=True)
    save(A/'cache_provenance.json',dict(timestamp=now(),packages=cache,copy_method='Read bytes, private fresh file, immediate byte comparison; no hardlinks',package_objects_inherited=True,project_objects_inherited=False,package_cache_not_rebuilt=True))
    env=os.environ.copy()
    for key in ['LEAN_PATH','LEAN_SRC_PATH']:env.pop(key,None)
    env['PATH']=str(BIN)+os.pathsep+env.get('PATH','');env['GIT_OPTIONAL_LOCKS']='0'
    n=int(env.get('GIT_CONFIG_COUNT','0'));safe=[]
    for i,pkg in enumerate(manifest['packages'],n):
        p=(V/'.lake/packages'/pkg['name']).resolve();assert p.is_relative_to(V.resolve());safe.append(str(p))
        env[f'GIT_CONFIG_KEY_{i}']='safe.directory';env[f'GIT_CONFIG_VALUE_{i}']=str(p).replace('\\','/')
    env['GIT_CONFIG_COUNT']=str(n+len(safe))
    save(A/'environment_scope.json',dict(process_only_git_safe_directory=safe,global_git_config_modified=False,lean_path_removed=True,driver=pin(Path(__file__)),allowed_write_roots=[str(OUT),str(V)]))
    assert not (V/'.lake/build/lib/lean').exists()
    command=[str(BIN/'lake.exe'),'build',*modules,'TGLExt.ReviewA1Orphans'];start=time.time()
    with (A/'lake_stdout.txt').open('xb') as stdout,(A/'lake_stderr.txt').open('xb') as stderr:
        proc=subprocess.Popen(command,cwd=V,env=env,stdout=stdout,stderr=stderr,creationflags=subprocess.CREATE_NO_WINDOW)
        save(A/'process.json',dict(pid=proc.pid,command=command,cwd=str(V),started=now()))
        print('ORPHANS_LAKE_STARTED',proc.pid,str(A),flush=True);rc=proc.wait()
    run=dict(returncode=rc,elapsed_seconds=time.time()-start,finished=now(),command=command,cwd=str(V),streams=[pin(A/'lake_stdout.txt'),pin(A/'lake_stderr.txt')],toolchain=subprocess.check_output([str(BIN/'lean.exe'),'--version'],env=env).decode().strip(),executables=[pin(BIN/'lean.exe'),pin(BIN/'lake.exe')])
    save(A/'run.json',run);print('ORPHANS_LAKE_EXIT',rc,flush=True)
    for x in protected:ck(x)
    for x in sources:ck(x['original']);ck(x['copy'])
    for x in docs:ck(x)
    save(A/'completion.json',dict(timestamp=now(),status='BUILD_RC0__REVIEW_PENDING' if rc==0 else 'BUILD_FAILED',run=pin(A/'run.json'),snapshot=pin(A/'source_snapshot.json'),protected_originals_unchanged=True))
    return rc
if __name__=='__main__':
    try:sys.exit(main())
    except Exception:
        if A.exists():save(A/'driver_failure.json',dict(timestamp=now(),error=traceback.format_exc()))
        raise
