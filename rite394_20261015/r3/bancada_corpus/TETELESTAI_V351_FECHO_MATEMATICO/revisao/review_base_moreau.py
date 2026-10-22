from pathlib import Path
import datetime, hashlib, json, os, re, subprocess, time

ROOT = Path(__file__).resolve().parents[1]
PREVIOUS = ROOT/'revisao/scalar_semifiniteness_independent_20260914_085400_122493'
OUT = ROOT/'revisao'/('base_moreau_independent_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
OUT.mkdir()
NAME = 'V351BaseMoreauApproximants'
SOURCE = ROOT/'kernel/TGLExt'/f'{NAME}.lean'
ATTEMPT = ROOT/'attempts/20260914_090140_683505'
TARGETS = ['TGLV351.dualResolvent_minimum_energy_value','TGLV351.exists_base_moreau_approximant','TGLV351.exists_monotone_base_dual_approximation']
ALLOWED = {'propext','Classical.choice','Quot.sound'}
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p): return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def save(p, data):
    if not isinstance(data, bytes): data=(json.dumps(data, ensure_ascii=False, indent=2)+'\n').encode('utf-8')
    assert not p.exists(), str(p)
    p.parent.mkdir(parents=True, exist_ok=True)
    t=p.with_name(p.name+'.tmp')
    with t.open('xb') as f: f.write(data)
    assert t.read_bytes()==data
    os.replace(t,p)
def parse(s):
    rows=re.findall(r"^'(.+)' (?:depends on axioms: \[([^\]]*)\]|does not depend on any axioms)\s*$",s,re.M)
    result={n:[re.sub(r'\.\{[^{}]*\}$','',a.strip()) for a in axs.split(',') if a.strip()] for n,axs in rows}
    assert len(rows)==len(result)==3 and set(result)==set(TARGETS), result
    assert all(set(axs)<=ALLOWED for axs in result.values()),result
    return result

run=read(ATTEMPT/'run.json')
assert run['returncode']==0
assert sha(SOURCE)==run['source_sha256']==sha(ATTEMPT/SOURCE.name)
author_object=Path(run['command'][run['command'].index('-o')+1])
author_pin=sha(author_object)
src_text=SOURCE.read_text(encoding='utf-8')
assert ['TGLV351.'+x for x in re.findall(r'^#print axioms (\S+)\s*$',src_text,re.M)]==TARGETS
author_stdout=(ATTEMPT/'stdout.txt').read_text(encoding='utf-8')
assert 'warning:' not in author_stdout and 'error:' not in author_stdout
assert (ATTEMPT/'stderr.txt').stat().st_size==0
author_axioms=parse(author_stdout)
for path in ATTEMPT.iterdir():
    if path.is_file(): save(OUT/'author_final'/path.name,path.read_bytes())

previous_preflight=read(PREVIOUS/'preflight.json')
previous_compile=read(PREVIOUS/'compilation.json')
assert previous_compile['all_exit_zero'] and previous_compile['source_dependency_and_review_pins_preserved']
deps=read(PREVIOUS/'dependencies.json')
assert len(deps)==382
for d in deps:
    assert sha(d['source'])==d['source_sha256'],d['module']
    assert sha(d['copied_to'])==d['object_sha256'],d['module']
    target=OUT/'build'/Path(*d['module'].split('.')).with_suffix('.olean')
    save(target,Path(d['copied_to']).read_bytes())
    assert sha(target)==d['object_sha256']
    d['new_copy']=str(target)
save(OUT/'dependencies.json',deps)
marco=read(ROOT/'DEPENDENCIAS_A1_MARCO_BASE.json')
assert len(marco['entries'])==384
for d in marco['entries']:
    assert sha(d['source'])==d['source_sha256'],d['module']
    assert sha(d['object'])==d['object_sha256'],d['module']
save(OUT/'milestone_manifest_verified.json',marco)

ficha=read(ROOT/'REAPROVEITAMENTO_A1_APROXIMANTES_BASE.json')
adendo=read(ROOT/'ADENDO_REAPROVEITAMENTO_A1_APROXIMANTES_BASE.json')
for p in ficha['providers']: assert sha(p['file'])==p['sha256'],p['file']
assert sha(adendo['file'])==adendo['sha256']
assert adendo['statement'] in Path(adendo['file']).read_text(encoding='utf-8')
pins={}
for fn in ['REAPROVEITAMENTO_A1_APROXIMANTES_BASE.md','REAPROVEITAMENTO_A1_APROXIMANTES_BASE.json','ADENDO_REAPROVEITAMENTO_A1_APROXIMANTES_BASE.json','LACUNAS_A1.md','BASE_E_FONTES.json','DEPENDENCIAS_A1_MARCO_BASE.json','AUDITORIA_A1_APROXIMANTES_BASE.json']:
    path=ROOT/fn;pins[str(path)]=sha(path);save(OUT/'inputs'/fn,path.read_bytes())
for path in [SOURCE,ROOT/'um.py',ROOT/'revisao/REVIEW_A1_BASE_ESTENDIDA_FINAL.md',ROOT/'revisao/REVIEW_A1_SEMIFINITUDE_FINAL.md',ROOT/'revisao/REVIEW_A1_CONTRATO_FINAL.md',ROOT/'revisao/CONSULTA_A1_MOREAU_PREDUAL.md']:
    pins[str(path)]=sha(path)
assert pins[str(ROOT/'um.py')]==read(ROOT/'BASE_E_FONTES.json')['program_sha256']

history=[]
for path in sorted((ROOT/'attempts').glob('*/run.json')):
    data=read(path)
    if Path(data.get('command',[''])[-1]).name!=SOURCE.name: continue
    stream=path.parent/'stdout.txt'
    s=stream.read_text(encoding='utf-8')
    row={'run':str(path),'run_sha256':sha(path),'source_sha256':data.get('source_sha256'),
         'returncode':data.get('returncode'),'stdout_sha256':sha(stream),'accepted':path.parent==ATTEMPT,
         'diagnostics':[line for line in s.splitlines() if ': error:' in line or ': warning:' in line],
         'sorryAx_seen':'sorryAx' in s}
    history.append(row)
save(OUT/'author_history.json',history)

packages=[p for p in previous_preflight['lean_path'] if '/.lake/packages/' in p.replace('\\','/')]
lean_path=[str(OUT/'build')]+packages
env=os.environ.copy();env['LEAN_PATH']=os.pathsep.join(lean_path)
compiler=run['command'][0]
assert sha(compiler)==previous_preflight['compiler_sha256']
save(OUT/'preflight.json',{'time':datetime.datetime.now().astimezone().isoformat(),'source_sha256':sha(SOURCE),
    'author_binary_sha256':author_pin,'names':TARGETS,'pins':pins,'lean_path':lean_path,
    'compiler':compiler,'compiler_sha256':sha(compiler),'dependency_objects':len(deps),
    'provenance':'382 objects reused from own semifiniteness frozen build: 380 older inherited binaries (not independently rebuilt), 2 V351 parents previously independently compiled. No author project build in LEAN_PATH. External packages readonly and not rebuilt.',
    'provider_records_verified':len(ficha['providers']),'corrected_provider_verified':adendo['statement']})
module_source=OUT/'kernel/TGLExt'/SOURCE.name
save(module_source,SOURCE.read_bytes())
print('BUILD_STARTED '+str(OUT),flush=True)

def compile_one(label,src,obj):
    obj.parent.mkdir(parents=True,exist_ok=True)
    cmd=[compiler,'--root='+str(OUT/'kernel'),'-o',str(obj),str(src)]
    start=time.monotonic()
    with (OUT/(label+'.stdout.txt')).open('wb') as o,(OUT/(label+'.stderr.txt')).open('wb') as e:
        p=subprocess.run(cmd,cwd=OUT/'kernel',env=env,stdout=o,stderr=e)
    result={'command':cmd,'returncode':p.returncode,'seconds':time.monotonic()-start,
        'source_sha256':sha(src),'object_sha256':sha(obj) if obj.exists() else None,
        'stdout_sha256':sha(OUT/(label+'.stdout.txt')),'stderr_sha256':sha(OUT/(label+'.stderr.txt'))}
    save(OUT/(label+'_run.json'),result)
    s=(OUT/(label+'.stdout.txt')).read_text(encoding='utf-8')
    assert p.returncode==0 and 'error:' not in s and 'warning:' not in s and (OUT/(label+'.stderr.txt')).stat().st_size==0,result
    result['axioms']=parse(s)
    assert result['axioms']==author_axioms
    save(OUT/(label+'.json'),result)
    print(label.upper()+'_RC0',flush=True)
    return result
module=compile_one('module',module_source,OUT/'build/TGLExt'/f'{NAME}.olean')
auditsource=OUT/'kernel/AuditBaseMoreau.lean'
audittext='import TGLExt.'+NAME+'\nset_option pp.universes true\n'+''.join('#check '+n+'\n#print axioms '+n+'\n' for n in TARGETS)
save(auditsource,audittext.encode('utf-8'))
auditor=compile_one('auditor',auditsource,OUT/'build/AuditBaseMoreau.olean')
unchanged=all(sha(p)==h for p,h in pins.items()) and all(sha(d['source'])==d['source_sha256'] and sha(d['copied_to'])==d['object_sha256'] and sha(d['new_copy'])==d['object_sha256'] for d in deps)
equal=module['object_sha256']==author_pin==sha(author_object)
assert unchanged and equal
save(OUT/'compilation.json',{'all_exit_zero':True,'exact_targets':True,'trio_only':True,'pins_preserved':unchanged,
    'binary_byte_equal_to_author':equal,'module':module,'auditor':auditor,'time':datetime.datetime.now().astimezone().isoformat()})
print('FINAL_PASS '+str(OUT),flush=True)
