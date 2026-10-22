from pathlib import Path
import datetime,hashlib,json,os,re,subprocess,time
R=Path(__file__).resolve().parents[1]
PREV=R/'revisao/functional_laws_independent_20260914_093642_937361'
O=R/'revisao'/('series_normality_independent_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
O.mkdir()
NAME='V351BaseSeriesNormality'
SOURCE=R/'kernel/TGLExt'/f'{NAME}.lean'
ATTEMPT=R/'attempts/20260914_093715_947928'
ALLOWED={'propext','Classical.choice','Quot.sound'}
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def save(p,data):
    assert not p.exists(),str(p)
    if not isinstance(data,bytes):data=(json.dumps(data,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
    p.parent.mkdir(parents=True,exist_ok=True);t=p.with_name(p.name+'.tmp')
    with t.open('xb') as f:f.write(data)
    assert t.read_bytes()==data;os.replace(t,p)
run=read(ATTEMPT/'run.json');old=read(PREV/'compilation.json');pf=read(PREV/'preflight.json')
assert run['returncode']==0 and old['all_exit_zero'] and old['pins_preserved'] and old['binary_byte_equal_to_author']
assert sha(SOURCE)==run['source_sha256']==sha(ATTEMPT/SOURCE.name)
author_object=Path(run['command'][run['command'].index('-o')+1]);author_sha=sha(author_object)
s=SOURCE.read_text(encoding='utf-8')
targets=['TGLV351.'+n for n in re.findall(r'^#print axioms (\S+)\s*$',s,re.M)]
decls=re.findall(r'^(def|theorem)\s+(\w+)',s,re.M)
assert len(targets)==len(set(targets))==4 and len(decls)==4 and all(k=='theorem' for k,n in decls)
assert {'TGLV351.'+n for k,n in decls}==set(targets)
assert not re.search(r'\b(sorry|admit|axiom|native_decide|trustCompiler|unsafe|implemented_by)\b',s)
assert re.findall(r'^set_option (\S+) ',s,re.M)==['autoImplicit','linter.unusedSectionVars','maxHeartbeats']
def parse(s):
    rows=re.findall(r"^'(.+)' (?:depends on axioms: \[([^\]]*)\]|does not depend on any axioms)\s*$",s,re.M)
    d={n:[re.sub(r'\.\{[^{}]*\}$','',a.strip()) for a in axs.split(',') if a.strip()] for n,axs in rows}
    assert len(rows)==len(d)==4 and set(d)==set(targets),d
    assert all(set(a)<=ALLOWED for a in d.values()),d
    return d
astdout=(ATTEMPT/'stdout.txt').read_text(encoding='utf-8')
assert 'error:' not in astdout and 'warning:' not in astdout and (ATTEMPT/'stderr.txt').stat().st_size==0
aaxioms=parse(astdout)
for p in ATTEMPT.iterdir():
    if p.is_file():save(O/'author_final'/p.name,p.read_bytes())
deps=[]
for d in read(PREV/'dependencies.json'):
    src=Path(d['source']);obj=Path(d['own_copy'])
    assert sha(src)==d['source_sha256'] and sha(obj)==d['object_sha256'],d['module']
    deps.append({'module':d['module'],'source':str(src),'source_sha256':d['source_sha256'],
                 'previous_own_object':str(obj),'object_sha256':d['object_sha256'],
                 'inherited_prior_to_v351':d['inherited_prior_to_v351']})
mod=old['module'];cmd=mod['command'];obj=Path(cmd[cmd.index('-o')+1]);src=R/'kernel/TGLExt/V351BaseFunctionalWeightLaws.lean'
assert sha(obj)==mod['object_sha256'] and sha(src)==mod['source_sha256']
deps.append({'module':'TGLExt.V351BaseFunctionalWeightLaws','source':str(src),'source_sha256':sha(src),
             'previous_own_object':str(obj),'object_sha256':sha(obj),'inherited_prior_to_v351':False})
assert len(deps)==len({d['module'] for d in deps})==385
for d in deps:
    dest=O/'build'/Path(*d['module'].split('.')).with_suffix('.olean')
    save(dest,Path(d['previous_own_object']).read_bytes());assert sha(dest)==d['object_sha256'];d['own_copy']=str(dest)
save(O/'dependencies.json',deps)
ficha=read(R/'REAPROVEITAMENTO_A1_NORMALIDADE_SERIES.json')
for x in ficha['providers']:
    assert sha(x['file'])==x['sha256'],x['file']
    assert x['statement'] in Path(x['file']).read_text(encoding='utf-8'),x['declaration']
pins={str(p):sha(p) for p in [SOURCE,author_object,ATTEMPT/'run.json',ATTEMPT/'stdout.txt',ATTEMPT/'stderr.txt',
    PREV/'compilation.json',PREV/'preflight.json',PREV/'dependencies.json',
    R/'revisao/REVIEW_A1_LEIS_FUNCIONAIS_FINAL.md',R/'DEPENDENCIAS_A1_MARCO_BASE.json',
    R/'REAPROVEITAMENTO_A1_NORMALIDADE_SERIES.md',R/'REAPROVEITAMENTO_A1_NORMALIDADE_SERIES.json',
    R/'um.py',R/'LACUNAS_A1.md']}
for f in ['REAPROVEITAMENTO_A1_NORMALIDADE_SERIES.md','REAPROVEITAMENTO_A1_NORMALIDADE_SERIES.json']:
    save(O/'inputs'/f,(R/f).read_bytes())
packages=[p for p in pf['lean_path'] if '/.lake/packages/' in p.replace('\\','/')]
assert len(packages)==9
compiler=run['command'][0];assert sha(compiler)==pf['compiler_sha256'];pins[compiler]=sha(compiler)
lean_path=[str(O/'build')]+packages
save(O/'preflight.json',{'time':datetime.datetime.now().astimezone().isoformat(),'source_sha256':sha(SOURCE),
    'author_object_sha256':author_sha,'targets':targets,'pins':pins,'compiler':compiler,'compiler_sha256':sha(compiler),
    'lean_path':lean_path,'providers_verified':len(ficha['providers']),'dependency_objects':len(deps),
    'provenance':'385 frozen own-tree inputs: 380 old inherited binaries not rebuilt; five V351 parents independently reproduced earlier (extended base, semifiniteness, Moreau, evaluation, functional laws). External packages readonly reused; no author project build in LEAN_PATH. Earlier milestone manifest is kept distinct from this expanded list.'})
history=[]
for p in sorted((R/'attempts').glob('*/run.json')):
    x=read(p)
    if Path(x.get('command',[''])[-1]).name!=SOURCE.name:continue
    txt=(p.parent/'stdout.txt').read_text(encoding='utf-8')
    history.append({'run':str(p),'run_sha256':sha(p),'returncode':x.get('returncode'),
       'source_sha256':x.get('source_sha256'),'stdout_sha256':sha(p.parent/'stdout.txt'),
       'accepted':p.parent==ATTEMPT,'sorryAx_seen':'sorryAx' in txt,
       'diagnostics':[l for l in txt.splitlines() if ': error:' in l or ': warning:' in l]})
save(O/'author_history.json',history)
module_src=O/'kernel/TGLExt'/SOURCE.name;save(module_src,SOURCE.read_bytes())
env=os.environ.copy();env['LEAN_PATH']=os.pathsep.join(lean_path)
(O/'tmp').mkdir();env['TMP']=env['TEMP']=str(O/'tmp')
print('BUILD_STARTED '+str(O),flush=True)
def compile_one(label,src,obj):
    obj.parent.mkdir(parents=True,exist_ok=True)
    cmd=[compiler,'--root='+str(O/'kernel'),'-o',str(obj),str(src)];start=time.monotonic()
    with (O/(label+'.stdout.txt')).open('wb') as stdout,(O/(label+'.stderr.txt')).open('wb') as stderr:
        q=subprocess.run(cmd,cwd=O/'kernel',env=env,stdout=stdout,stderr=stderr)
    result={'command':cmd,'returncode':q.returncode,'seconds':time.monotonic()-start,'source_sha256':sha(src),
            'object_sha256':sha(obj) if obj.exists() else None,'stdout_sha256':sha(O/(label+'.stdout.txt')),
            'stderr_sha256':sha(O/(label+'.stderr.txt'))}
    save(O/(label+'_run.json'),result)
    txt=(O/(label+'.stdout.txt')).read_text(encoding='utf-8')
    assert q.returncode==0 and 'error:' not in txt and 'warning:' not in txt and (O/(label+'.stderr.txt')).stat().st_size==0,result
    result['axioms']=parse(txt);assert result['axioms']==aaxioms
    save(O/(label+'.json'),result);print(label.upper()+'_RC0',flush=True);return result
module=compile_one('module',module_src,O/'build/TGLExt'/f'{NAME}.olean')
asrc=O/'kernel/AuditBaseSeriesNormality.lean'
save(asrc,('import TGLExt.'+NAME+'\nset_option pp.universes true\n'+''.join('#check '+n+'\n#print axioms '+n+'\n' for n in targets)).encode('utf-8'))
auditor=compile_one('auditor',asrc,O/'build/AuditBaseSeriesNormality.olean')
preserved=all(sha(path)==h for path,h in pins.items()) and all(sha(d['source'])==d['source_sha256'] and sha(d['previous_own_object'])==d['object_sha256'] and sha(d['own_copy'])==d['object_sha256'] for d in deps)
equal=module['object_sha256']==author_sha==sha(author_object)
assert preserved and equal
save(O/'compilation.json',{'time':datetime.datetime.now().astimezone().isoformat(),'all_exit_zero':True,
    'exact_targets':True,'trio_only':True,'binary_byte_equal_to_author':equal,'pins_preserved':preserved,
    'module':module,'auditor':auditor})
print('FINAL_PASS '+str(O),flush=True)
