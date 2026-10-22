from pathlib import Path
import datetime, hashlib, json, os, re, subprocess, sys, time
sys.stdout.reconfigure(encoding='utf-8')
ROOT=Path(__file__).resolve().parents[1]
OLD=ROOT/'revisao/a1_independent_20260914_081736_089694'
OUT=ROOT/'revisao'/('extended_base_independent_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
OUT.mkdir()
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(p,data):
    if not isinstance(data,bytes):data=json.dumps(data,ensure_ascii=False,indent=2).encode('utf-8')
    assert not p.exists(),str(p)
    p.parent.mkdir(parents=True,exist_ok=True)
    tmp=p.with_name(p.name+'.tmp');tmp.write_bytes(data);assert tmp.stat().st_size==len(data);tmp.replace(p)
name='V351ExtendedBaseDualWeight'
source=ROOT/'kernel/TGLExt'/f'{name}.lean'
attempt=ROOT/'attempts/20260914_084253_409522'
run=json.loads((attempt/'run.json').read_text(encoding='utf-8'))
assert run['returncode']==0 and sha(source)==run['source_sha256']==sha(attempt/source.name)
author_bin=Path(run['command'][run['command'].index('-o')+1])
names=['TGLV351.'+n for n in re.findall(r'^#print axioms (\S+)\s*$',source.read_text(encoding='utf-8'),re.M)]
assert len(names)==len(set(names))==14
allowed={'propext','Classical.choice','Quot.sound'}
def parse(text):
    hits=re.findall(r"^'(.+)' (?:depends on axioms: \[([^\]]*)\]|does not depend on any axioms)\s*$",text,re.M)
    d={n:[re.sub(r'\.\{[^{}]*\}$','',x.strip()) for x in a.split(',') if x.strip()] for n,a in hits}
    assert len(hits)==len(d)==14 and set(d)==set(names)
    assert all(set(a)<=allowed for a in d.values())
    return d
author_stdout=(attempt/'stdout.txt').read_text(encoding='utf-8')
assert 'warning:' not in author_stdout and 'error:' not in author_stdout and not (attempt/'stderr.txt').stat().st_size
author_axioms=parse(author_stdout)
ficha=json.loads((ROOT/'REAPROVEITAMENTO_A1_BASE_ESTENDIDA.json').read_text(encoding='utf-8'))
for p in ficha['providers']:assert sha(p['file'])==p['sha256'],p
for p in ficha['searches']:assert sha(p['output'])==p['sha256'],p
for p,h in ficha['inherited_searches'].items():assert sha(p)==h,p
old=json.loads((OLD/'dependencies.json').read_text(encoding='utf-8'))
current=json.loads((ROOT/'DEPENDENCIAS_A1_BASE_ESTENDIDA.json').read_text(encoding='utf-8'))
assert len(old)==375 and len(current)==359
dep_records={d['module']:d for d in old}
for d in current:
    rel=Path(*d['module'].split('.'))
    assert sha(ROOT/'kernel'/rel.with_suffix('.lean'))==d['source_sha256']
    assert sha(ROOT/'build'/rel.with_suffix('.olean'))==sha(d['object_origin'])==d['object_sha256']
    if d['module'] in dep_records:
        assert dep_records[d['module']]['source_sha256']==d['source_sha256'] and dep_records[d['module']]['object_sha256']==d['object_sha256']
    else:dep_records[d['module']]=d
old_comp=json.loads((OLD/'compilation.json').read_text(encoding='utf-8'))
assert old_comp['all_exit_zero'] and old_comp['module_binary_equals_author']
dep_records['TGLExt.V351RegularCoreTraceContract']=dict(module='TGLExt.V351RegularCoreTraceContract',
    source_sha256=old_comp['module']['source_sha256'],object_sha256=old_comp['module']['object_sha256'],
    object_origin=str(OLD/'build/TGLExt/V351RegularCoreTraceContract.olean'))
copied=[]
for n,d in sorted(dep_records.items()):
    rel=Path(*n.split('.'));src=ROOT/'kernel'/rel.with_suffix('.lean')
    prior=OLD/'build'/rel.with_suffix('.olean')
    obj=prior if prior.exists() else Path(d['object_origin'])
    assert sha(src)==d['source_sha256'] and sha(obj)==d['object_sha256']
    assert sha(ROOT/'build'/rel.with_suffix('.olean'))==d['object_sha256']
    dest=OUT/'build'/rel.with_suffix('.olean')
    save(dest,obj.read_bytes());save(OUT/'dependency_sources'/rel.with_suffix('.lean'),src.read_bytes())
    copied.append(dict(d,read_source=str(src),copied_from=str(obj),copied_to=str(dest),own_previously_compiled=n=='TGLExt.V351RegularCoreTraceContract'))
assert len(copied)==377
save(OUT/'dependencies.json',copied)
pins={}
for fn in ['REAPROVEITAMENTO_A1_BASE_ESTENDIDA.md','REAPROVEITAMENTO_A1_BASE_ESTENDIDA.json',
           'DEPENDENCIAS_A1_BASE_ESTENDIDA.json','LACUNAS_A1.md','BASE_E_FONTES.json','um.py']:
    p=ROOT/fn;pins[str(p)]=sha(p)
    if fn!='um.py':save(OUT/'inputs'/fn,p.read_bytes())
for p in ROOT.joinpath('revisao').glob('REVIEW_A1_CONTRATO_*.md'):pins[str(p)]=sha(p)
for p in [ROOT/'revisao/CONSULTA_A1_RESTRICAO_FORMAS_BASE.md',source,ROOT/'kernel/TGLExt/V351RegularCoreTraceContract.lean']:
    pins[str(p)]=sha(p)
for p in attempt.iterdir():
    if p.is_file():save(OUT/'author_final'/p.name,p.read_bytes())
failed=ROOT/'attempts/20260914_084206_268140'
fr=json.loads((failed/'run.json').read_text(encoding='utf-8'));assert fr['returncode']==1
for p in failed.iterdir():
    if p.is_file():save(OUT/'author_rejected'/p.name,p.read_bytes())
packages=[p for p in run['lean_path'] if '/.lake/packages/' in p.replace('\\','/')]
paths=[str(OUT/'build')]+packages
env=os.environ.copy();env['LEAN_PATH']=os.pathsep.join(paths)
compiler=run['command'][0]
src=OUT/'kernel/TGLExt'/source.name;save(src,source.read_bytes())
save(OUT/'preflight.json',dict(time=datetime.datetime.now().astimezone().isoformat(),source_sha256=sha(source),
    author_binary_sha256=sha(author_bin),names=names,pins=pins,compiler=compiler,compiler_sha256=sha(compiler),
    lean_path=paths,author_dependency_manifest_records=359,project_objects_in_own_snapshot=377,
    own_previously_compiled_objects=1,new_inherited_copy=['TGLExt.V350FixedBaseEquivalence'],
    provider_hashes_verified=len(ficha['providers']),new_search_capture_hashes_verified=len(ficha['searches']),
    provenance='375 inherited dependencies frozen during A1 review, reused by hashes; one independently compiled A1 contract; one additional inherited FixedBaseEquivalence binary; external packages readonly, not rebuilt'))
print('BUILD_STARTED '+str(OUT),flush=True)
def compile_one(label,sp,bp):
    bp.parent.mkdir(parents=True,exist_ok=True)
    cmd=[compiler,'--root='+str(OUT/'kernel'),'-o',str(bp),str(sp)]
    start=time.monotonic()
    with (OUT/(label+'.stdout.txt')).open('wb') as o,(OUT/(label+'.stderr.txt')).open('wb') as e:
        p=subprocess.run(cmd,cwd=OUT/'kernel',env=env,stdout=o,stderr=e)
    data=dict(command=cmd,returncode=p.returncode,seconds=time.monotonic()-start,source_sha256=sha(sp),
        stdout_sha256=sha(OUT/(label+'.stdout.txt')),stderr_sha256=sha(OUT/(label+'.stderr.txt')),
        object_sha256=sha(bp) if bp.exists() else None)
    save(OUT/(label+'_run.json'),data)
    txt=(OUT/(label+'.stdout.txt')).read_text(encoding='utf-8')
    assert p.returncode==0 and 'error:' not in txt and 'warning:' not in txt and not (OUT/(label+'.stderr.txt')).stat().st_size, data
    data['axioms']=parse(txt);assert data['axioms']==author_axioms
    save(OUT/(label+'.json'),data)
    print(label.upper()+'_RC0 '+str(data['seconds']),flush=True)
    return data
module=compile_one('module',src,OUT/'build/TGLExt'/f'{name}.olean')
audit=OUT/'kernel/AuditExtendedBase.lean'
text='import TGLExt.'+name+'\nset_option pp.universes true\n'
for n in names:text+='#check '+n+'\n#print axioms '+n+'\n'
save(audit,text.encode('utf-8'))
auditor=compile_one('auditor',audit,OUT/'build/AuditExtendedBase.olean')
unchanged=all(sha(p)==h for p,h in pins.items())
unchanged=unchanged and all(sha(d['read_source'])==d['source_sha256'] and sha(d['copied_from'])==d['object_sha256'] and sha(d['copied_to'])==d['object_sha256'] for d in copied)
equal=module['object_sha256']==sha(author_bin)
assert unchanged and equal
save(OUT/'compilation.json',dict(all_exit_zero=True,exact_targets=True,trio_only=True,
    source_and_dependency_pins_preserved=unchanged,binary_byte_equal_to_author=equal,
    module=module,auditor=auditor,time=datetime.datetime.now().astimezone().isoformat()))
print('FINAL_PASS '+str(OUT),flush=True)
