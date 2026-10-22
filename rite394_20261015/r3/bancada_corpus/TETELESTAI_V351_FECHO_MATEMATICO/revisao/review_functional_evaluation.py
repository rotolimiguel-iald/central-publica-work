from pathlib import Path
import datetime, hashlib, json, os, re, subprocess, time

ROOT=Path(__file__).resolve().parents[1]
PREV=ROOT/'revisao/base_moreau_independent_20260914_090556_274602'
OUT=ROOT/'revisao'/('functional_evaluation_independent_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
OUT.mkdir()
NAME='V351BaseFunctionalEvaluation'
SOURCE=ROOT/'kernel/TGLExt'/f'{NAME}.lean'
ATTEMPT=ROOT/'attempts/20260914_092635_416376'
ALLOWED={'propext','Classical.choice','Quot.sound'}
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p): return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def save(p,data):
    if not isinstance(data,bytes): data=(json.dumps(data,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
    assert not p.exists(),str(p)
    p.parent.mkdir(parents=True,exist_ok=True)
    t=p.with_name(p.name+'.tmp')
    with t.open('xb') as f: f.write(data)
    assert t.read_bytes()==data
    os.replace(t,p)
run=read(ATTEMPT/'run.json')
assert run['returncode']==0
assert sha(SOURCE)==run['source_sha256']==sha(ATTEMPT/SOURCE.name)
author_object=Path(run['command'][run['command'].index('-o')+1])
author_hash=sha(author_object)
source_text=SOURCE.read_text(encoding='utf-8')
targets=['TGLV351.'+x for x in re.findall(r'^#print axioms (\S+)\s*$',source_text,re.M)]
decls=re.findall(r'^(def|theorem)\s+(\w+)',source_text,re.M)
assert len(targets)==len(set(targets))==21
assert len(decls)==21 and sum(k=='def' for k,n in decls)==3
assert {'TGLV351.'+n for k,n in decls}==set(targets)
forbidden=re.findall(r'\b(?:sorry|admit|axiom|native_decide|trustCompiler|unsafe|implemented_by)\b',source_text)
assert not forbidden,forbidden
assert re.findall(r'^set_option (\S+) ',source_text,re.M)==['autoImplicit','linter.unusedSectionVars','maxHeartbeats']
def parse(s):
    rows=re.findall(r"^'(.+)' (?:depends on axioms: \[([^\]]*)\]|does not depend on any axioms)\s*$",s,re.M)
    result={n:[re.sub(r'\.\{[^{}]*\}$','',a.strip()) for a in axs.split(',') if a.strip()] for n,axs in rows}
    assert len(rows)==len(result)==21 and set(result)==set(targets),result
    assert all(set(a)<=ALLOWED for a in result.values()),result
    return result
author_stdout=(ATTEMPT/'stdout.txt').read_text(encoding='utf-8')
assert 'warning:' not in author_stdout and 'error:' not in author_stdout and (ATTEMPT/'stderr.txt').stat().st_size==0
author_axioms=parse(author_stdout)
for p in ATTEMPT.iterdir():
    if p.is_file(): save(OUT/'author_final'/p.name,p.read_bytes())

previous=read(PREV/'compilation.json');pf=read(PREV/'preflight.json')
assert previous['all_exit_zero'] and previous['pins_preserved'] and previous['binary_byte_equal_to_author']
marco=read(ROOT/'DEPENDENCIAS_A1_MARCO_BASE.json')
assert len(marco['entries'])==384
by_module={d['module']:d for d in marco['entries']}
for d in marco['entries']:
    assert sha(d['source'])==d['source_sha256'],d['module']
    assert sha(d['object'])==d['object_sha256'],d['module']
save(OUT/'milestone_manifest_verified.json',marco)
deps=[]
for d in read(PREV/'dependencies.json'):
    e=by_module[d['module']]
    old=Path(d['new_copy'])
    assert sha(old)==d['object_sha256']==e['object_sha256']
    assert sha(d['source'])==d['source_sha256']==e['source_sha256']
    deps.append({'module':d['module'],'source':d['source'],'source_sha256':d['source_sha256'],
                 'object_sha256':d['object_sha256'],'previous_own_object':str(old),
                 'inherited_prior_to_v351':e['inherited']})
e=by_module['TGLExt.V351BaseMoreauApproximants']
old=Path(previous['module']['command'][previous['module']['command'].index('-o')+1])
assert sha(old)==e['object_sha256']
deps.append({'module':e['module'],'source':e['source'],'source_sha256':e['source_sha256'],
             'object_sha256':e['object_sha256'],'previous_own_object':str(old),'inherited_prior_to_v351':False})
assert len(deps)==383 and len({d['module'] for d in deps})==383
for d in deps:
    dest=OUT/'build'/Path(*d['module'].split('.')).with_suffix('.olean')
    save(dest,Path(d['previous_own_object']).read_bytes());assert sha(dest)==d['object_sha256']
    d['own_copy']=str(dest)
save(OUT/'dependencies.json',deps)
packages=[p for p in pf['lean_path'] if '/.lake/packages/' in p.replace('\\','/')]
assert len(packages)==9
lean_path=[str(OUT/'build')]+packages
compiler=run['command'][0];assert sha(compiler)==pf['compiler_sha256']
mathlib=next(Path(p) for p in packages if '/packages/mathlib/' in p.replace('\\','/'))
countable_object=mathlib/'Mathlib/MeasureTheory/Integral/Lebesgue/Countable.olean'
countable_source=mathlib.parents[3]/'Mathlib/MeasureTheory/Integral/Lebesgue/Countable.lean'
pins={str(p):sha(p) for p in [SOURCE,author_object,ATTEMPT/'run.json',ATTEMPT/'stdout.txt',ATTEMPT/'stderr.txt',
    ROOT/'DEPENDENCIAS_A1_MARCO_BASE.json',ROOT/'BASE_E_FONTES.json',ROOT/'LACUNAS_A1.md',ROOT/'um.py',
    ROOT/'revisao/REVIEW_A1_APROXIMANTES_BASE_FINAL.md',PREV/'compilation.json',PREV/'dependencies.json',
    Path(compiler),countable_object,countable_source]}
save(OUT/'preflight.json',{'time':datetime.datetime.now().astimezone().isoformat(),'source_sha256':sha(SOURCE),
    'author_binary_sha256':author_hash,'targets':targets,'definitions':3,'theorems':18,'forbidden_tokens':forbidden,
    'pins':pins,'lean_path':lean_path,'compiler':compiler,'compiler_sha256':sha(compiler),
    'dependency_objects':len(deps),'manifest_records_verified':len(marco['entries']),
    'provenance':'383 own-tree objects reused, including 380 older inherited binaries not rebuilt here and 3 V351 independently compiled parents; contract object verified in 384 manifest but unnecessary in LEAN_PATH. Packages readonly, not rebuilt; Countable direct import pinned. No author project build in LEAN_PATH.'})
history=[]
for p in sorted((ROOT/'attempts').glob('*/run.json')):
    h=read(p)
    if Path(h.get('command',[''])[-1]).name!=SOURCE.name: continue
    s=(p.parent/'stdout.txt').read_text(encoding='utf-8')
    history.append({'run':str(p),'run_sha256':sha(p),'source_sha256':h.get('source_sha256'),
                    'returncode':h.get('returncode'),'stdout_sha256':sha(p.parent/'stdout.txt'),
                    'accepted':p.parent==ATTEMPT,'sorryAx_seen':'sorryAx' in s,
                    'diagnostics':[l for l in s.splitlines() if ': error:' in l or ': warning:' in l]})
save(OUT/'author_history.json',history)
module_src=OUT/'kernel/TGLExt'/SOURCE.name
save(module_src,SOURCE.read_bytes())
env=os.environ.copy();env['LEAN_PATH']=os.pathsep.join(lean_path)
env['TMP']=str(OUT/'tmp');env['TEMP']=str(OUT/'tmp');(OUT/'tmp').mkdir()
print('BUILD_STARTED '+str(OUT),flush=True)
def compile_one(label,src,obj):
    obj.parent.mkdir(parents=True,exist_ok=True)
    cmd=[compiler,'--root='+str(OUT/'kernel'),'-o',str(obj),str(src)]
    start=time.monotonic()
    with (OUT/(label+'.stdout.txt')).open('wb') as o,(OUT/(label+'.stderr.txt')).open('wb') as e:
        proc=subprocess.run(cmd,cwd=OUT/'kernel',env=env,stdout=o,stderr=e)
    result={'command':cmd,'returncode':proc.returncode,'seconds':time.monotonic()-start,
            'source_sha256':sha(src),'object_sha256':sha(obj) if obj.exists() else None,
            'stdout_sha256':sha(OUT/(label+'.stdout.txt')),'stderr_sha256':sha(OUT/(label+'.stderr.txt'))}
    save(OUT/(label+'_run.json'),result)
    stream=(OUT/(label+'.stdout.txt')).read_text(encoding='utf-8')
    assert proc.returncode==0 and 'warning:' not in stream and 'error:' not in stream and (OUT/(label+'.stderr.txt')).stat().st_size==0,result
    result['axioms']=parse(stream)
    assert result['axioms']==author_axioms
    save(OUT/(label+'.json'),result)
    print(label.upper()+'_RC0',flush=True)
    return result
module=compile_one('module',module_src,OUT/'build/TGLExt'/f'{NAME}.olean')
audit_src=OUT/'kernel/AuditBaseFunctionalEvaluation.lean'
save(audit_src,('import TGLExt.'+NAME+'\nset_option pp.universes true\n'+''.join('#check '+n+'\n#print axioms '+n+'\n' for n in targets)).encode('utf-8'))
auditor=compile_one('auditor',audit_src,OUT/'build/AuditBaseFunctionalEvaluation.olean')
preserved=all(sha(p)==h for p,h in pins.items()) and all(sha(d['source'])==d['source_sha256'] and sha(d['previous_own_object'])==d['object_sha256'] and sha(d['own_copy'])==d['object_sha256'] for d in deps)
equal=module['object_sha256']==author_hash==sha(author_object)
assert preserved and equal
save(OUT/'compilation.json',{'time':datetime.datetime.now().astimezone().isoformat(),
    'all_exit_zero':True,'exact_targets':True,'trio_only':True,'binary_byte_equal_to_author':equal,
    'pins_preserved':preserved,'module':module,'auditor':auditor})
print('FINAL_PASS '+str(OUT),flush=True)
