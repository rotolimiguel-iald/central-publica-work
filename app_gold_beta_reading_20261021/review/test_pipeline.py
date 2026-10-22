from pathlib import Path
import ast,json,hashlib,types,sys,tempfile,copy,shutil
w=Path('work/app_gold_beta_reading_20261021/release').resolve(); out=w.parent/'review'
results=[]
def test(name,fn):
 try:fn();results.append({'name':name,'passed':True})
 except Exception as e:results.append({'name':name,'passed':False,'error':type(e).__name__+': '+str(e)})
def yes(cond):assert cond
for p in list(w.glob('*.py'))+list((w/'mobile_prepare').glob('*.py')):test('syntax_'+str(p.relative_to(w)),lambda p=p:ast.parse(p.read_bytes()))
# Execute the actual reviewed guard source, with all paths redirected to disposable local fixtures.
f=Path(tempfile.mkdtemp(prefix='guard_fixture_',dir=out)); W=f/'release';ROOT=f/'root';MOBILE=ROOT/'mobile';SURFACES=(ROOT/'app',MOBILE/'www',MOBILE/'ios/public',MOBILE/'android/public'); NATIVES=('ios/version','android/version')
h=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
def put(p,v):p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(json.dumps(v).encode() if not isinstance(v,bytes) else v)
def load(p):return json.loads(Path(p).read_bytes())
def safe(p):return Path(p).resolve()
prep=types.ModuleType('prepare');prep.W=W;prep.ROOT=ROOT;prep.MOBILE=MOBILE;prep.SURFACES=SURFACES;prep.NATIVES=NATIVES;prep.sha=h;prep.load=load;prep.safe=safe;sys.modules['prepare']=prep
required={'prepare.py','guards.py','transaction.py','maintenance.py','deploy_controlled.py','mobile_release.py','android34.init.gradle','mobile_prepare/build_log.py','mobile_prepare/TOOL_PLAN.json','SCIENCE_BASELINE.json','NATIVE_PLAN.json','INPUT_MANIFEST.json','PRIVATE_GIT_PLAN.json','publish_apk34.py','apply_static.py'}
for n in required:put(W/n,b'fixture tool')
science=ROOT/'science';put(science,b'science');put(W/'SCIENCE_BASELINE.json',{'files':[{'path':str(science),'sha256':h(science)}]});put(W/'NATIVE_PLAN.json',{'ios':'4.1(39)','android':'4.1(34)'});put(W/'INPUT_MANIFEST.json',{'runtime':[]})
rows=[]
for dest in [s/n for s in SURFACES for n in ['iald.js','iald.css']]+[MOBILE/n for n in NATIVES]:
 source=W/'stage'/dest.relative_to(ROOT);put(source,b'new');put(dest,b'old');rows.append({'source':str(source),'destination':str(dest),'sha256':h(source),'baseline':h(dest)})
plan={'assets':['iald.js','iald.css'],'files':rows,'science_sha256':h(W/'SCIENCE_BASELINE.json')};put(W/'install_plan.json',plan)
validation={'passed':True,'plan_sha256':h(W/'install_plan.json')};put(W/'validation/final_checks.json',validation)
review={'status':'PASS','reviewer':'actual-independent-fixture','plan_sha256':h(W/'install_plan.json'),'tool_pins':{n:h(W/n) for n in required}};put(W/'validation/review_final.json',review)
mod=types.ModuleType('guards_under_test');exec(compile((w/'guards.py').read_bytes(),str(w/'guards.py'),'exec'),mod.__dict__);mod.preflight=lambda:{'ready':True}
test('guard_accepts_complete_fixture',lambda:yes(mod.reviewed()==plan))
# Each mutation is restored byte-for-byte; no production or mission state touched.
def rejected(name,path,transform,repin=False):
 def run():
  original=path.read_bytes();rv=(W/'validation/review_final.json').read_bytes()
  try:
   value=load(path);transform(value);put(path,value)
   if repin:
    v=load(W/'validation/review_final.json');v['tool_pins'][str(path.relative_to(W))]=h(path);put(W/'validation/review_final.json',v)
   try:mod.reviewed()
   except (ValueError,KeyError,StopIteration,FileNotFoundError):return
   raise AssertionError('guard accepted invalid fixture')
  finally:path.write_bytes(original);(W/'validation/review_final.json').write_bytes(rv)
 test(name,run)
rejected('reject_review_stale_plan',W/'validation/review_final.json',lambda v:v.update(plan_sha256='0'*64))
rejected('reject_author_self_review',W/'validation/review_final.json',lambda v:v.update(reviewer='codex-gold-release'))
rejected('reject_checks_false',W/'validation/final_checks.json',lambda v:v.update(passed=False))
rejected('reject_tool_pin_missing',W/'validation/review_final.json',lambda v:v['tool_pins'].pop('apply_static.py'))
rejected('reject_tool_pin_changed',W/'validation/review_final.json',lambda v:v['tool_pins'].update({'apply_static.py':'0'*64}))
rejected('reject_runtime_in_manifest',W/'INPUT_MANIFEST.json',lambda v:v.update(runtime=['backend.py']),True)
rejected('reject_wrong_native_version',W/'NATIVE_PLAN.json',lambda v:v.update(ios='4.1(40)'),True)
def mutate_raw(name,p):
 def run():
  original=p.read_bytes()
  try:
   p.write_bytes(b'concurrent edit')
   try:mod.reviewed()
   except ValueError:return
   raise AssertionError('accepted changed bytes')
  finally:p.write_bytes(original)
 test(name,run)
mutate_raw('reject_concurrent_destination',Path(rows[0]['destination']));mutate_raw('reject_stage_changed',Path(rows[0]['source']));mutate_raw('reject_science_changed',science)
# Review the explicit no-process-control entry point without running it.
a=ast.parse((w/'apply_static.py').read_bytes());imports=[x.module for x in ast.walk(a) if isinstance(x,ast.ImportFrom)];test('static_apply_does_not_import_maintenance',lambda:yes('maintenance' not in imports));test('old_deploy_entrypoint_retired',lambda:yes('raise SystemExit' in (w/'deploy_controlled.py').read_text()))
report={'status':'PASS' if all(x['passed'] for x in results) else 'FAIL','tests':results,'scope':'Actual guards.py executed on disposable local fixtures, all syntax parsed, no production/state/network/model/build/Git write. Fixture reviewer names are synthetic tests only, never review_final author identities.','fixture':str(f),'source_pins':{str(p):h(p) for p in w.glob('*.py')}}
p=out/'PIPELINE_TESTS.json';p.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps({'status':report['status'],'tests':len(results),'failures':[x for x in results if not x['passed']]}))
