from pathlib import Path
import datetime, hashlib, json, os, re, subprocess, sys, time
sys.stdout.reconfigure(encoding='utf-8')
R=Path(__file__).resolve().parents[1]
OLD=R/'revisao/extended_base_independent_20260914_084553_472856'
OUT=R/'revisao'/('scalar_semifiniteness_independent_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
OUT.mkdir()
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(p,data):
    if not isinstance(data,bytes):data=json.dumps(data,ensure_ascii=False,indent=2).encode('utf-8')
    assert not p.exists(),str(p)
    p.parent.mkdir(parents=True,exist_ok=True)
    tmp=p.with_name(p.name+'.tmp');tmp.write_bytes(data);assert tmp.stat().st_size==len(data);tmp.replace(p)
name='V351ScalarWeightSemifiniteness'
source=R/'kernel/TGLExt'/f'{name}.lean'
attempt=R/'attempts/20260914_084729_714501'
run=json.loads((attempt/'run.json').read_text(encoding='utf-8'))
assert run['returncode']==0 and sha(source)==run['source_sha256']==sha(attempt/source.name)
author_bin=Path(run['command'][run['command'].index('-o')+1])
names=['TGLV351.'+n for n in re.findall(r'^#print axioms (\S+)\s*$',source.read_text(encoding='utf-8'),re.M)]
assert len(names)==len(set(names))==2
allowed={'propext','Classical.choice','Quot.sound'}
def parse(s):
    h=re.findall(r"^'(.+)' (?:depends on axioms: \[([^\]]*)\]|does not depend on any axioms)\s*$",s,re.M)
    d={n:[re.sub(r'\.\{[^{}]*\}$','',a.strip()) for a in ax.split(',') if a.strip()] for n,ax in h}
    assert len(h)==len(d)==2 and set(d)==set(names) and all(set(a)<=allowed for a in d.values())
    return d
author_out=(attempt/'stdout.txt').read_text(encoding='utf-8')
assert 'error:' not in author_out and 'warning:' not in author_out and not (attempt/'stderr.txt').stat().st_size
author_axioms=parse(author_out)
ficha=json.loads((R/'REAPROVEITAMENTO_A1_SEMIFINITUDE.json').read_text(encoding='utf-8'))
for f in ficha['providers']:assert sha(f['file'])==f['sha256']
old=json.loads((OLD/'dependencies.json').read_text(encoding='utf-8'))
current=json.loads((R/'DEPENDENCIAS_A1_SEMIFINITUDE.json').read_text(encoding='utf-8'))
assert len(old)==377 and len(current)==378
records={d['module']:d for d in old}
new=[]
for d in current:
    rel=Path(*d['module'].split('.'))
    assert sha(R/'kernel'/rel.with_suffix('.lean'))==d['source_sha256']
    assert sha(R/'build'/rel.with_suffix('.olean'))==sha(d['object_origin'])==d['object_sha256']
    if d['module'] in records:
        assert records[d['module']]['source_sha256']==d['source_sha256'] and records[d['module']]['object_sha256']==d['object_sha256']
    else:records[d['module']]=d;new.append(d['module'])
old_comp=json.loads((OLD/'compilation.json').read_text(encoding='utf-8'))
assert old_comp['all_exit_zero'] and old_comp['binary_byte_equal_to_author']
records['TGLExt.V351ExtendedBaseDualWeight']=dict(module='TGLExt.V351ExtendedBaseDualWeight',
    source_sha256=old_comp['module']['source_sha256'],object_sha256=old_comp['module']['object_sha256'],
    object_origin=str(OLD/'build/TGLExt/V351ExtendedBaseDualWeight.olean'))
copied=[]
for n,d in sorted(records.items()):
    rel=Path(*n.split('.'));src=R/'kernel'/rel.with_suffix('.lean');prior=OLD/'build'/rel.with_suffix('.olean')
    obj=prior if prior.exists() else Path(d['object_origin'])
    assert sha(src)==d['source_sha256'] and sha(obj)==d['object_sha256']
    assert sha(R/'build'/rel.with_suffix('.olean'))==d['object_sha256']
    dest=OUT/'build'/rel.with_suffix('.olean')
    save(dest,obj.read_bytes());save(OUT/'dependency_sources'/rel.with_suffix('.lean'),src.read_bytes())
    copied.append(dict(module=n,source=str(src),source_sha256=d['source_sha256'],object_sha256=d['object_sha256'],copied_from=str(obj),copied_to=str(dest)))
assert len(copied)==382 and len(new)==4
save(OUT/'dependencies.json',copied)
pins={}
for fn in ['REAPROVEITAMENTO_A1_SEMIFINITUDE.md','REAPROVEITAMENTO_A1_SEMIFINITUDE.json','DEPENDENCIAS_A1_SEMIFINITUDE.json','um.py']:
    p=R/fn;pins[str(p)]=sha(p)
    if fn!='um.py':save(OUT/'inputs'/fn,p.read_bytes())
for p in [source,R/'revisao/REVIEW_A1_BASE_ESTENDIDA_FINAL.md',R/'revisao/REVIEW_A1_CONTRATO_FINAL.md',R/'revisao/CONSULTA_A1_RESTRICAO_FORMAS_BASE.md']:
    pins[str(p)]=sha(p)
for p in attempt.iterdir():
    if p.is_file():save(OUT/'author_final'/p.name,p.read_bytes())
packages=[p for p in run['lean_path'] if '/.lake/packages/' in p.replace('\\','/')]
paths=[str(OUT/'build')]+packages
env=os.environ.copy();env['LEAN_PATH']=os.pathsep.join(paths)
compiler=run['command'][0]
src=OUT/'kernel/TGLExt'/source.name;save(src,source.read_bytes())
save(OUT/'preflight.json',dict(source_sha256=sha(source),author_binary_sha256=sha(author_bin),names=names,pins=pins,
    compiler=compiler,compiler_sha256=sha(compiler),lean_path=paths,author_dependency_records=378,
    own_project_snapshot_objects=382,new_inherited_objects=new,
    provenance='Reused prior frozen 377 objects plus independently compiled ExtendedBaseDualWeight, and four additional inherited objects pinned against source/origin; no dependency rebuild. Two V351 parents were previously independently compiled; all 380 older project objects are inherited binaries.',
    provider_records_verified=len(ficha['providers'])))
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
    assert p.returncode==0 and 'error:' not in txt and 'warning:' not in txt and not (OUT/(label+'.stderr.txt')).stat().st_size,data
    data['axioms']=parse(txt);assert data['axioms']==author_axioms
    save(OUT/(label+'.json'),data);print(label.upper()+'_RC0',flush=True)
    return data
module=compile_one('module',src,OUT/'build/TGLExt'/f'{name}.olean')
audit=OUT/'kernel/AuditScalarSemifiniteness.lean'
text='import TGLExt.'+name+'\nset_option pp.universes true\n'
for n in names:text+='#check '+n+'\n#print axioms '+n+'\n'
save(audit,text.encode('utf-8'))
auditor=compile_one('auditor',audit,OUT/'build/AuditScalarSemifiniteness.olean')
unchanged=all(sha(p)==h for p,h in pins.items()) and all(sha(d['source'])==d['source_sha256'] and sha(d['copied_from'])==d['object_sha256'] and sha(d['copied_to'])==d['object_sha256'] for d in copied)
equal=module['object_sha256']==sha(author_bin)
assert unchanged and equal
assert sha(R/'um.py')==json.loads((R/'BASE_E_FONTES.json').read_text(encoding='utf-8'))['program_sha256']
save(OUT/'compilation.json',dict(all_exit_zero=True,exact_targets=True,trio_only=True,
    source_dependency_and_review_pins_preserved=unchanged,binary_byte_equal_to_author=equal,
    module=module,auditor=auditor,time=datetime.datetime.now().astimezone().isoformat()))
print('FINAL_PASS '+str(OUT),flush=True)
