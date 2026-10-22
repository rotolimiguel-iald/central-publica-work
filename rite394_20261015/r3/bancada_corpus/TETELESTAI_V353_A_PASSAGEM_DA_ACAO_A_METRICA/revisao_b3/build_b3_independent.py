from pathlib import Path
from datetime import datetime
import hashlib, json, os, re, subprocess, sys, time, traceback

R = Path(r'C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA')
S = R / 's'
OUT = R / 'revisao_b3'
SRC = R / 'kernel'
BIN = Path(r'C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin')
STAMP = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
ATT = OUT / ('independent_' + STAMP)
FINAL = ['TGLExt.SectorFluidClosure', 'TGLExt.SectorFriedmann', 'TGLExt.AuditSector']

def now(): return datetime.now().astimezone().isoformat()
def pin(p):
    b=p.read_bytes()
    return dict(path=str(p), bytes=len(b), sha256=hashlib.sha256(b).hexdigest())
def fresh(p,b):
    p.parent.mkdir(parents=True,exist_ok=True)
    assert p.resolve().is_relative_to(OUT.resolve()) or p.resolve().is_relative_to(S.resolve())
    assert not p.exists(), p
    t=p.with_name(p.name+'.tmp_'+STAMP)
    with t.open('xb') as f: f.write(b); f.flush(); os.fsync(f.fileno())
    assert t.read_bytes()==b
    os.replace(t,p)
def save(p,d): fresh(p,(json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode('utf8'))
def uncomment(text):
    depth=0; out=[]; i=0
    while i<len(text):
        if text.startswith('/-',i): depth+=1; i+=2
        elif depth and text.startswith('-/',i): depth-=1; i+=2
        elif depth:
            if text[i]=='\n':out.append('\n')
            i+=1
        elif text.startswith('--',i):
            j=text.find('\n',i); i=len(text) if j<0 else j
        else: out.append(text[i]); i+=1
    assert depth==0
    return ''.join(out)

def main():
    ATT.mkdir()
    prior=R/'revisao_b2'/'compilation.json'
    b2=json.loads(prior.read_bytes())
    assert b2['status']=='INDEPENDENT_B2_LAKE_RC0' and b2['all_accepted_builds_exit_zero']
    protected_paths=[R/'revisao'/'REVIEW_B1_FINAL.md', R/'revisao'/'REVIEW_B1_FINAL.json',
        R/'r'/'compilation.json', R/'r'/'run.json', R/'MANIFESTO_B1.json',
        R/'revisao_b2'/'REVIEW_B2_FINAL.md', R/'revisao_b2'/'REVIEW_B2_FINAL.json', prior,
        R/'MANIFESTO_B2.json', R/'RECIBO_B2.json']
    protected=[pin(p) for p in protected_paths]
    inherited=[]
    for ob in b2['objects']:
        p=Path(ob['own']['path']); assert pin(p)==ob['own'], p
        assert pin(Path(ob['trace']['path']))==ob['trace']
        inherited.append(dict(object=ob['own'],trace=ob['trace']))
    for p in ['lakefile.toml','lake-manifest.json','lean-toolchain']:
        assert (S/p).read_bytes()==(SRC/p).read_bytes(),p
    au=json.loads((R/'AUDITORIA_B3.json').read_bytes())
    for p in au['sources']+au['objects']+[au['positive_build']]: assert pin(Path(p['path']))==p,p
    targets_meta=json.loads((R/'ALVOS_B3.json').read_bytes())
    assert targets_meta==au['targets']
    target_names=[t['name'] for t in targets_meta]
    assert len(target_names)==len(set(target_names))==22
    assert [sum(t['kind']==k for t in targets_meta) for k in ['theorem','def','structure']]==[14,7,1]
    records=[]; seen=set(); declarations=[]
    def visit(mod):
        if mod in seen:return
        seen.add(mod)
        p=SRC/(mod.replace('.','/')+'.lean'); b=p.read_bytes(); code=uncomment(b.decode('utf-8-sig'))
        imports=[]
        for m in re.finditer(r'^\s*(?:public\s+)?import\s+([^\n]+)',code,re.M):imports.extend(m.group(1).split())
        for dep in imports:
            if dep.startswith(('TGL.','TGLExt.')) or dep in ['TGL','TGLExt']:visit(dep)
        q=S/p.relative_to(SRC); new=not q.exists()
        obj=S/'.lake'/'build'/'lib'/'lean'/(mod.replace('.','/')+'.olean')
        if new:
            assert not obj.exists(),(mod,'Unexpected preexisting object')
            fresh(q,b)
        else:
            assert q.read_bytes()==b,(mod,'Source drift; do not overwrite')
        if mod in FINAL:
            assert new,(mod,'B3 build must start with no prebuilt object')
            fresh(ATT/p.name,b)
            assert not re.findall(r'\b(?:sorry|axiom|admit|native_decide|trustCompiler|unsafe)\b',code),(mod,'Forbidden token')
            if mod!=FINAL[-1]:
                for m in re.finditer(r'^(structure|def|theorem)\s+(\w+)\b',code,re.M):
                    prefix='ChatgptAudit.FLRW.'
                    if mod==FINAL[0] and m.group(1)!='structure':prefix+='SectorFluid.'
                    end=code.find('where' if m.group(1)=='structure' else ':=',m.end())
                    declarations.append(dict(name=prefix+m.group(2),kind=m.group(1),module=mod,line=code[:m.start()].count('\n')+1,statement=code[m.start():end].strip()))
        records.append(dict(module=mod,source=pin(p),copy=pin(q),new_source_copy=new,object_preexisting=obj.exists(),imports=imports))
    visit('TGLExt.AuditSector')
    assert set(target_names)=={d['name'] for d in declarations}
    parsed=re.findall(r'^#print axioms\s+(\S+)',(S/'TGLExt'/'AuditSector.lean').read_text(encoding='utf-8-sig'),re.M)
    assert parsed==target_names
    review='import TGLExt.SectorFriedmann\n\nset_option pp.universes true\n\n'
    for t in target_names:review+=f'#check {t}\n#print axioms {t}\n\n'
    own=S/'TGLExt'/'ReviewSector.lean'; fresh(own,review.encode('utf8'))
    docpins=[]
    for fn in ['REAPROVEITAMENTO_B3.md','REAPROVEITAMENTO_B3.json','AUDITORIA_B3.json','ALVOS_B3.json']:
        p=R/fn; fresh(ATT/fn,p.read_bytes()); docpins.append(pin(p))
    snap=dict(timestamp=now(),status='FROZEN_B3__BUILD_PENDING',sources=records,targets=target_names,
        declarations=declarations,own_auditor=pin(own),documents=docpins,author_objects=au['objects'],
        source_configs=[pin(S/p) for p in ['lakefile.toml','lake-manifest.json','lean-toolchain']],
        inherited_B2_compilation=pin(prior),inherited_project_objects=inherited,protected_before=protected,
        project_objects_copied_from_author=False,mathlib_cache_scope='Inherited pinned private B1/B2 packages, not rebuilt',
        cache_inheritance=b2['cache_inheritance'])
    save(ATT/'snapshot.json',snap)
    save(OUT/'B3_SNAPSHOT_POINTER.json',dict(snapshot=pin(ATT/'snapshot.json'),attempt=str(ATT)))
    print('B3_SNAPSHOT',str(ATT),'NEW_SOURCES',json.dumps([v['module'] for v in records if v['new_source_copy']]),'INHERITED_OBJECTS',len(inherited),flush=True)
    env=os.environ.copy()
    for k in ['LEAN_PATH','LEAN_SRC_PATH']:env.pop(k,None)
    env['PATH']=str(BIN)+os.pathsep+env.get('PATH','')
    env['GIT_OPTIONAL_LOCKS']='0'
    manifest=json.loads((S/'lake-manifest.json').read_bytes()); start=int(env.get('GIT_CONFIG_COUNT','0')); safe=[]
    for i,pkg in enumerate(manifest['packages'],start):
        p=(S/'.lake'/'packages'/pkg['name']).resolve(); assert p.is_relative_to(S.resolve())
        safe.append(str(p)); env[f'GIT_CONFIG_KEY_{i}']='safe.directory'; env[f'GIT_CONFIG_VALUE_{i}']=str(p).replace('\\','/')
    env['GIT_CONFIG_COUNT']=str(start+len(safe))
    save(ATT/'environment_scope.json',dict(safe_directories_process_only=safe,global_git_config_modified=False,
        lean_path_removed=True,script=pin(Path(__file__)),cache_inheritance=b2['cache_inheritance']))
    cmd=[str(BIN/'lake.exe'),'build','TGLExt.TheSameBetaReadsThreeFaces',*FINAL,'TGLExt.ReviewSector']
    started=time.time()
    with (ATT/'lake_stdout.txt').open('xb') as out,(ATT/'lake_stderr.txt').open('xb') as err:
        proc=subprocess.Popen(cmd,cwd=S,env=env,stdout=out,stderr=err,creationflags=subprocess.CREATE_NO_WINDOW)
        save(ATT/'process.json',dict(pid=proc.pid,command=cmd,cwd=str(S),started=now()))
        print('B3_LAKE_STARTED',proc.pid,str(ATT),flush=True)
        rc=proc.wait()
    run=dict(returncode=rc,elapsed_seconds=time.time()-started,finished=now(),command=cmd,cwd=str(S),
        streams=[pin(ATT/'lake_stdout.txt'),pin(ATT/'lake_stderr.txt')],
        toolchain=subprocess.check_output([str(BIN/'lean.exe'),'--version'],env=env).decode().strip(),
        executables=[pin(BIN/'lean.exe'),pin(BIN/'lake.exe')])
    save(ATT/'run.json',run); print('B3_LAKE_EXIT',rc,flush=True)
    checks=[dict(module=d['module'],source_unchanged=pin(Path(d['source']['path']))==d['source'],copy_unchanged=pin(Path(d['copy']['path']))==d['copy']) for d in records]
    assert all(c['source_unchanged'] and c['copy_unchanged'] for c in checks)
    assert all(pin(Path(p['path']))==p for p in protected)
    assert all(pin(Path(p['object']['path']))==p['object'] and pin(Path(p['trace']['path']))==p['trace'] for p in inherited)
    save(ATT/'completion.json',dict(status='BUILD_RC0__SEMANTIC_AND_AXIOM_AUDIT_PENDING' if rc==0 else 'BUILD_FAILED',
        run=pin(ATT/'run.json'),source_checks=checks,inherited_92_objects_unchanged=True,B1_B2_protected_unchanged=True,
        timestamp=now(),snapshot=pin(ATT/'snapshot.json')))
    return rc

if __name__=='__main__':
    try:sys.exit(main())
    except Exception:
        if ATT.exists():save(ATT/'driver_failure.json',dict(timestamp=now(),error=traceback.format_exc()))
        raise
