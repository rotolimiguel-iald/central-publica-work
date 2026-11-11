from pathlib import Path
import ast,json,hashlib,os,datetime,types
W=Path(r'C:\IALD\Central de Patentes\work\app_scroll_20261106'); R=W/'review'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def pin(p):return {'path':str(p),'sha256':sha(p)}
plan=json.loads((W/'mobile/PLAN.json').read_bytes()); install=json.loads((W/'INSTALL_PLAN.json').read_bytes())
checks=[]
def ok(name,condition):
 assert condition,name
 checks.append(name)
ok('mobile_eight_unique_targets',len(plan['rows'])==8==len({r['target'] for r in plan['rows']}))
for row in plan['rows']:
 ok('mobile_hash_'+str(len(checks)),sha(row['source'])==row['new'] and sha(row['target'])==row['old'])
 src=Path(row['source']);target=Path(row['target'])
 if src.suffix=='.js':ok('asset_exact_stage_'+str(len(checks)),src.read_bytes()==(W/'stage'/src.name).read_bytes())
 else:
  old=target.read_bytes();new=src.read_bytes()
  before,after=(b'CURRENT_PROJECT_VERSION = 46;',b'CURRENT_PROJECT_VERSION = 47;') if src.suffix=='.pbxproj' else (b'versionCode 41',b'versionCode 42')
  ok('version_only_'+src.name,old.replace(before,after)==new and old.count(before)==(2 if src.suffix=='.pbxproj' else 1))
ok('manifest_pinned',sha(plan['parent_manifest']['path'])==plan['parent_manifest']['sha256'])
ok('install_mobile_link',sha(install['mobile_plan']['path'])==install['mobile_plan']['sha256'])
ok('ten_install_targets',len(install['rows'])==10==len({r['target'] for r in install['rows']}))
ok('install_includes_exact_mobile_rows',install['rows'][:8]==plan['rows'])
ok('install_sources_targets_baseline',all(sha(r['source'])==r['new'] and sha(r['target'])==r['old'] for r in install['rows']))
ok('all_protected_pins',all(sha(r['path'])==r['sha256'] for r in install['preserve']))
ok('no_protected_target_overwritten',not ({r['path'] for r in install['preserve']} & {r['target'] for r in install['rows']}))
for p in [W/'prepare_fix.py',W/'install_static.py',*list((W/'mobile').glob('*.py'))]:ast.parse(p.read_text(encoding='utf-8-sig'));checks.append('syntax_'+p.name)
# Execute only installer function definitions, with task globals replaced by a synthetic review-owned tree.
parsed=ast.parse((W/'install_static.py').read_text()); definitions=ast.Module(body=[n for n in parsed.body if isinstance(n,ast.FunctionDef)],type_ignores=[])
cases=[]
for mode in ['success','stale_target','source_drift_after_preflight','replace_failure','protected_drift_after_write']:
 base=R/('install_fixture_'+mode);base.mkdir();sandbox=base/'runtime';sandbox.mkdir();work=base/'work';work.mkdir()
 rows=[]
 for i in range(2):
  src=work/f'new{i}.js';dest=sandbox/f'file{i}.js';src.write_bytes(b'NEW'+str(i).encode());dest.write_bytes(b'OLD'+str(i).encode());rows.append({'source':str(src),'target':str(dest),'old':sha(dest),'new':sha(src)})
 protected=sandbox/'protected.py';protected.write_bytes(b'UNCHANGED');p={'rows':rows,'preserve':[pin(protected)]}
 (work/'INSTALL_PLAN.json').write_text(json.dumps(p));(work/'review.json').write_text(json.dumps({'status':'PASS','reviewer':'synthetic-distinct','install_plan_sha256':sha(work/'INSTALL_PLAN.json')}))
 call_count=[0]
 def replace(src,dest):
  if '.scroll_' in str(src):
   call_count[0]+=1
   if mode=='replace_failure' and call_count[0]==2:raise OSError('SYNTHETIC_REPLACE_FAILURE')
  os.replace(src,dest)
  if mode=='protected_drift_after_write' and call_count[0]==2 and '.scroll_' in str(src):protected.write_bytes(b'SYNTHETIC_CONCURRENT_DRIFT')
 def save(name,value):
  (work/name).write_text(json.dumps(value))
  if mode=='source_drift_after_preflight' and name=='INSTALL_INTENT.json':Path(rows[0]['source']).write_bytes(b'DRIFT')
 namespace={'Path':Path,'json':json,'datetime':datetime,'os':types.SimpleNamespace(fsync=os.fsync,replace=replace),'W':work,'R':sandbox,'pin':pin,'save':save,'check':lambda task:None}
 exec(compile(definitions,'review-extracted-installer','exec'),namespace)
 if mode=='stale_target':Path(rows[0]['target']).write_bytes(b'NEWER_CONCURRENT')
 error=None
 try:namespace['install']('review.json')
 except (AssertionError,OSError) as e:error=type(e).__name__
 if mode=='success':assert error is None and all(sha(r['target'])==r['new'] for r in rows)
 elif mode=='stale_target':assert error and Path(rows[0]['target']).read_bytes()==b'NEWER_CONCURRENT' and not list(sandbox.glob('*.bak_*'))
 else:assert error and all(sha(r['target'])==r['old'] for r in rows)
 if mode in ('success','replace_failure','protected_drift_after_write'):assert all(any(sha(b)==r['old'] for b in sandbox.glob(Path(r['target']).name+'.bak_*')) for r in rows)
 cases.append({'name':mode,'status':'PASS','observed_error':error})
report={'status':'PASS','checks':checks,'installer_tests':cases,'protected_count':len(install['preserve']),'plan_sha256':sha(W/'mobile/PLAN.json'),'install_plan_sha256':sha(W/'INSTALL_PLAN.json'),'scope':'Only read real plans/destinations; installer execution restricted by injected globals to synthetic review fixtures; no build/install/runtime changes'}
(R/'STATIC_AND_INSTALLER.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps({'status':'PASS','checks':len(checks),'installer_cases':len(cases),'protected':len(install['preserve'])}))
