from pathlib import Path
import datetime,hashlib,json,os,re,subprocess,sys,time
sys.stdout.reconfigure(encoding='utf-8')
REV=Path(__file__).resolve().parent;ROOT=REV.parent
RUN=REV/('phase_variational_independent_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
PREV=Path((REV/'adjoint_polar_graph_final_latest_run.txt').read_text().strip())
sha=lambda b:hashlib.sha256(b).hexdigest();hf=lambda p:sha(Path(p).read_bytes());load=lambda p:json.loads(Path(p).read_bytes())
allowed={'propext','Classical.choice','Quot.sound'}
def write(p,b):
 assert p.resolve().is_relative_to(REV)
 p.parent.mkdir(parents=True,exist_ok=True)
 if p.exists():
  before=p.read_bytes();bk=p.with_name(p.name+'.bak_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
  with bk.open('xb') as f:f.write(before)
  assert bk.read_bytes()==before
 q=p.with_name(p.name+'.tmp')
 with q.open('xb') as f:f.write(b)
 assert q.read_bytes()==b;q.replace(p);assert p.read_bytes()==b
def save(p,d):write(p,(json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode())
def axioms(t):
 d={}
 for n,v in re.findall(r"'([\w.']+)' depends on axioms: \[([^\]]*)\]",t,re.S):
  a=sorted(x.strip() for x in v.split(',') if x.strip());assert n not in d or d[n]==a;d[n]=a
 for n in re.findall(r"'([\w.']+)' does not depend on any axioms",t):
  assert n not in d or not d[n];d[n]=[]
 return d
pm,pc=load(PREV/'manifest.json'),load(PREV/'compilation.json')
assert pc['complete'] and pc['all_exit_zero'] and pc['all_axioms_allowed'] and pc['external_direct_pins_preserved']
pkg=pm['lean_path'].split(os.pathsep)[1:];assert len(pkg)==8 and all('.lake\\packages\\' in s for s in pkg)
parent=ROOT/'adjoint_polar_graph_custody.json';pv=ROOT/'adjoint_polar_graph_custody_verification.json'
p,pp=load(parent),load(pv);assert pp['custody_ok'] and pp['custody_sha256']==hf(parent)
assert hf(ROOT/'um.py')==p['working_sha256'] and hf(ROOT/'gate_extension.py')==p['artifacts']['gate_extension.py']
assert len(p['remaining_flags'])==6 and all(v is False for v in p['remaining_flags'].values())
for path in [parent,pv]:write(RUN/path.name,path.read_bytes())
src=ROOT/'kernel/TGLV350/RealPhaseVariational.lean';raw=src.read_bytes()
lp=ROOT/'logs/RealPhaseVariational_20260913_032929_894153.json';log=load(lp);authorbin=Path(log['command'][2])
assert log['returncode']==log['lean_returncode']==0 and log['output_exists'] and log['source_unchanged_during_compile']
assert Path(log['source'])==src and sha(raw)==log['sha256'] and hf(authorbin)==log['output_sha256']
targets=['TGLV350.Regular.'+n for n in re.findall(r'^#print axioms ([\w.]+)$',raw.decode(),re.M)]
assert len(targets)==len(set(targets))==12
imps=re.findall(r'^import\s+([\w.]+)',raw.decode(),re.M);assert all(n.startswith('Mathlib.') for n in imps)
stripped=re.sub(r'/\-.*?\-/|--[^\n]*','',raw.decode(),flags=re.S)
assert not re.search(r'\b(?:axiom|sorry|admit|unsafe)\b|\[(?:irreducible|reducible)\]',stripped)
authorax=axioms(Path(log['stdout']).read_text(encoding='utf-8'));assert set(authorax)==set(targets) and all(set(x)<=allowed for x in authorax.values())
assert not Path(log['stderr']).read_bytes()
write(RUN/'sources/TGLV350/RealPhaseVariational.lean',raw)
history=[]
for path in sorted((ROOT/'logs').glob('RealPhaseVariational_*.json')):
 b=path.read_bytes();d=json.loads(b);write(RUN/'author_history'/path.name,b)
 row={'log':str(path),'log_sha256':sha(b),'returncode':d['returncode'],'source_sha256':d['sha256'],'accepted_final':path==lp}
 for k in ['stdout','stderr']:
  stream=Path(d[k]).read_bytes();write(RUN/'author_history'/Path(d[k]).name,stream);row[k+'_sha256']=sha(stream)
 history.append(row)
external=dict(pm['external_direct_pins'])
lib=next(Path(x) for x in pkg if '\\mathlib\\' in x)
for name in imps:
 rel=Path(*name.split('.'));source=lib.parents[3]/rel.with_suffix('.lean');binary=lib/rel.with_suffix('.olean')
 external[name]={'source':str(source),'source_sha256':hf(source),'binary':str(binary),'binary_sha256':hf(binary)}
for d in external.values():assert hf(d['source'])==d['source_sha256'] and hf(d['binary'])==d['binary_sha256']
cfg=load(ROOT/'environment.json');assert hf(cfg['lean'])==pm['compiler_sha256']
env=os.environ.copy();env['LEAN_PATH']=os.pathsep.join([str(RUN/'build')]+pkg)
assert str(ROOT/'build') not in env['LEAN_PATH']
(RUN/'tmp').mkdir(parents=True);env['TMP']=env['TEMP']=str(RUN/'tmp')
readonly={str(path):hf(path) for path in [parent,pv,ROOT/'um.py',ROOT/'gate_extension.py',src,authorbin,lp,Path(log['stdout']),Path(log['stderr']),PREV/'manifest.json',PREV/'compilation.json']}
manifest={'run':str(RUN),'timestamp':datetime.datetime.now().astimezone().isoformat(),'scope':'PARTIAL_SINGLE_MODULE_12_TARGETS_NO_STAGE_DRAFT',
 'source':str(src),'source_sha256':sha(raw),'source_snapshot':str(RUN/'sources/TGLV350/RealPhaseVariational.lean'),'author_binary':str(authorbin),'author_binary_sha256':hf(authorbin),
 'author_final_log':str(lp),'author_final_log_sha256':hf(lp),'author_axioms':authorax,'declarations':targets,'imports':imps,
 'parent_custody_sha256':hf(parent),'parent_full_reaudit':False,'previous_own_run':str(PREV),'previous_manifest_sha256':hf(PREV/'manifest.json'),
 'compiler':cfg['lean'],'compiler_sha256':pm['compiler_sha256'],'lean_version':pm['lean_version'],'lean_path':env['LEAN_PATH'],
 'project_dependencies':{},'external_direct_pins':external,'packages_rebuilt':False,'author_project_build_on_lean_path':False,'readonly_pins':readonly}
save(RUN/'manifest.json',manifest);save(RUN/'author_history.json',history);write(REV/'phase_variational_latest_run.txt',str(RUN).encode())
aud='import TGLV350.RealPhaseVariational\n'+''.join('set_option pp.universes true in\n#check '+n+'\n#print axioms '+n+'\n' for n in targets)
write(RUN/'sources/PhaseVariationalAudit.lean',aud.encode())
print(json.dumps({'run':str(RUN),'targets':len(targets),'project_dependencies':0,'external_direct_pins':len(external),'excluded_author_rc1':sum(x['returncode']!=0 for x in history)}),flush=True)
records=[]
for module in ['TGLV350/RealPhaseVariational.lean','PhaseVariationalAudit.lean']:
 sp=RUN/'sources'/module;op=RUN/'build'/Path(module).with_suffix('.olean');op.parent.mkdir(parents=True,exist_ok=True);assert not op.exists()
 cmd=[cfg['lean'],'-o',str(op),str(sp)];t=time.monotonic();r=subprocess.run(cmd,cwd=RUN/'sources',env=env,capture_output=True)
 out=RUN/'logs'/(Path(module).stem+'.stdout.txt');err=RUN/'logs'/(Path(module).stem+'.stderr.txt');write(out,r.stdout);write(err,r.stderr)
 ax=axioms(r.stdout.decode('utf-8',errors='replace'))
 row={'module':module,'command':cmd,'returncode':r.returncode,'seconds':round(time.monotonic()-t,3),'source_sha256':hf(sp),'output_sha256':hf(op) if op.exists() else None,
      'stdout':str(out),'stderr':str(err),'stdout_sha256':sha(r.stdout),'stderr_sha256':sha(r.stderr),'axioms':ax,'exact_targets':set(ax)==set(targets),'axioms_match_author':ax==authorax,'axioms_allowed':bool(ax) and all(set(x)<=allowed for x in ax.values())}
 if module.startswith('TGLV350/'):row['binary_equals_author']=row['output_sha256']==hf(authorbin)
 records.append(row);save(RUN/'compilation.json',{'complete':False,'records':records});print(json.dumps({k:row[k] for k in ['module','returncode','seconds','exact_targets','axioms_allowed']}),flush=True)
 if r.returncode:print(r.stdout.decode('utf-8',errors='replace'),flush=True);break
result={'complete':len(records)==2,'records':records,'all_exit_zero':len(records)==2 and all(x['returncode']==0 for x in records),'exact_12_targets':len(records)==2 and all(x['exact_targets'] for x in records),
 'all_axioms_allowed':all(x['axioms_allowed'] for x in records),'all_axioms_match_author':all(x['axioms_match_author'] for x in records),'binary_equal_author':records[0].get('binary_equals_author',False),
 'source_snapshot_preserved':hf(RUN/'sources/TGLV350/RealPhaseVariational.lean')==sha(raw),'readonly_artifacts_preserved':all(hf(path)==h for path,h in readonly.items()),
 'external_direct_pins_preserved':all(hf(d['source'])==d['source_sha256'] and hf(d['binary'])==d['binary_sha256'] for d in external.values())}
save(RUN/'compilation.json',result);print(json.dumps({k:v for k,v in result.items() if k!='records'}),flush=True)
