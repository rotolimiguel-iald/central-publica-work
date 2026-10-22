"""Generate a new guarded Android29 workflow; never execute Gradle or Git mutations."""
from pathlib import Path
import ast, hashlib, json

HERE=Path(__file__).resolve().parent
WORK=HERE.parent
OUT=HERE/'android29'
OLD=Path(r'C:\IALD\Central de Patentes\work\memoria_organismo_20261016\mobile_build')
ROOT=Path(r'C:\IALD\projetos_pyhton\IALD\iald-app')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def pin(p):return dict(path=str(p),sha256=sha(p))
def new(p,v):
    raw=v if isinstance(v,bytes) else json.dumps(v,ensure_ascii=False,indent=2).encode()
    with p.open('xb') as f:f.write(raw)
    assert p.read_bytes()==raw
OUT.mkdir(exist_ok=False)
oldplan=json.loads((OLD/'ANDROID28_BUILD_PLAN_R1.json').read_bytes())
mobileplan_path=HERE/'packages/client_R4_final_ios34_android29/install_plan_mobile_R4_FINAL.json'
mobile=json.loads(mobileplan_path.read_bytes())
mainplan=json.loads((WORK/'install_plan.json').read_bytes())
for item in mobile['files']:
    assert item in mainplan['files']
expected={str(Path(x['destination']).resolve()):x['sha256'] for x in mobile['files']}

runner=(OLD/'run_android28.py').read_text(encoding='utf-8-sig')
runner=runner.replace('WORK = HERE.parent','WORK = HERE.parent.parent')
runner=runner.replace('ANDROID28_BUILD_PLAN_R1.json','ANDROID29_BUILD_PLAN_R1.json').replace('android28.init.gradle','android29.init.gradle')
runner=runner.replace('fresh D','fresh deploy').replace("'D'","'deploy'").replace('Current root D lease required','Current deploy lease required')
runner=runner.replace("'codex-gerente-tgl'","'codex-app-01a094df'")
runner=runner.replace("if not path.is_relative_to((WORK / 'receipts').resolve()):","if not path.is_relative_to(WORK.resolve()):")
runner=runner.replace("versionCode='28'","versionCode='29'").replace('4.1(28)','4.1(29)')
runner=runner.replace('Published27 comparison artifact changed','Previous28 comparison artifact changed').replace('published27','previous28')
runner=runner.replace('Expected single public signing certificate not established','Expected single public signing certificate not established')
runner=runner.replace("    parser.add_argument('--preflight', type=Path)","    parser.add_argument('--preflight', type=Path)\n    parser.add_argument('--approval', type=Path)")
runner=runner.replace("    if differences or not args.preflight:","    if differences or not args.preflight or not args.approval:")
needle="    if digest(plan['baseline_apk']['path']) != plan['baseline_apk']['sha256']:"
runner=runner.replace(needle,"    require_approval(args.approval, 'android29_build', PLAN)\n"+needle)
approval='''def require_approval(path, operation, plan_path):
    """Local evidence of explicit human OK, not an authentication mechanism."""
    path=Path(path).resolve(strict=True)
    if not path.is_relative_to(WORK.resolve()): raise RuntimeError("Approval must be in this mission")
    no_reparse(path)
    approval=json.loads(path.read_bytes())
    if (approval.get("authorized") is not True or approval.get("operation") != operation
            or approval.get("reference") != str(REFERENCE)
            or approval.get("plan_sha256") != digest(plan_path)
            or not approval.get("human_ok_source")):
        raise RuntimeError("Explicit human OK receipt for this exact operation/plan is required")
    return pin(path)


'''
runner=runner.replace('def main():',approval+'def main():',1)
runner=runner.replace("'run_requires': '--run --preflight <fresh deploy receipt>'","'run_requires': '--run --preflight <fresh deploy receipt> --approval <explicit human OK receipt>'")
ast.parse(runner)
new(OUT/'run_android29.py',runner.encode())
init=(OLD/'android28.init.gradle').read_text(encoding='utf-8-sig')
init=init.replace('run_android28.py','run_android29.py').replace(str(OLD.as_posix())+'/attempts',str((OUT/'attempts').as_posix()))
assert 'memoria_organismo_20261016/mobile_build/attempts' not in init
init=init.replace('versionCode != 27','versionCode != 29').replace('versionCode = 28','versionCode = 29').replace('4.1(28)','4.1(29)')
new(OUT/'android29.init.gradle',init.encode())

# The archive parser is copied into this new delivery and only named functions
# may be compiled by audit_android29.py. Its historical top-level never runs.
parser=Path(r'C:\IALD\Central de Patentes\work\iald_monthly_wallet_20261007\audit_mobile.py')
new(OUT/'public_archive_parsers_source.py',parser.read_bytes())
tools=oldplan['tools']
for item in oldplan['tool_pins']:assert sha(item['path'])==item['sha256'],'Toolchain bytes changed; stop and review'
protected=[]
for entry in oldplan['protected_inputs']:
    p=Path(entry['path']);key=str(p.resolve())
    assert p.is_file()
    # Earlier audited list excludes credentials and private/configuration files.
    assert not any(t in p.name.lower() for t in ['.env','keystore','credential','secret'])
    protected.append(dict(path=str(p),sha256=expected.get(key,sha(p))))
for item in mobile['files']:
    if item['destination'] not in {x['path'] for x in protected}:
        protected.append(dict(path=item['destination'],sha256=item['sha256']))
native=ROOT/'android/app/src/main/assets/public'
resources=[]
for p in sorted(native.rglob('*')):
    if not p.is_file():continue
    assert not any(t in p.name.lower() for t in ['.env','keystore','credential','secret'])
    resources.append(dict(path=str(p),relative=p.relative_to(native).as_posix(),sha256=expected.get(str(p.resolve()),sha(p))))
previous=json.loads((OLD/'attempts/20261017T003613_760785Z/RESULT_R1.json').read_bytes())['artifacts']['apk']
assert sha(previous['path'])==previous['sha256']
plan=dict(schema='iald-mobile-build-plan/v2',status='PREPARED_NOT_AUTHORIZED_TO_RUN',
    unit='F9.MIMO26_UPGRADE_20261020',reference=pin(WORK/'SESSION_REFERENCE.json'),
    actor='codex-app-01a094df',task_id='deploy',versionCode=29,versionName='4.1',
    accepted_js_sha256=mobile['candidate_origin']['sha256'],resource_plan=pin(mobileplan_path),
    main_plan_preparation_pin=pin(WORK/'install_plan.json'),
    apple_baseline=pin(HERE/'APPLE_BASELINE.txt'),
    protected_inputs=protected,resource_files=resources,
    registry=pin(ROOT/'android/app/src/main/assets/capacitor.plugins.json'),
    tools=tools,tool_pins=oldplan['tool_pins'],baseline_apk=previous,
    wrapper=oldplan['wrapper'],android_project=oldplan['android_project'],android_sdk=oldplan['android_sdk'],
    gradle_user_home=oldplan['gradle_user_home'],build_tasks=[':app:bundleRelease',':app:assembleRelease'],
    candidate_files=[],
    parser_source=pin(OUT/'public_archive_parsers_source.py'),
    approval_contract=dict(authorized=True,operation='android29_build',reference=str(WORK/'SESSION_REFERENCE.json'),plan_sha256='<SHA256 of this final plan>',human_ok_source='<real operator OK source/receipt>'),
    preconditions=['Independent real review of this runner/init/auditor and pins.','Main installs accepted20-file plan first; six expected mobile destinations must match.','Explicit human OK; current deploy check receipt wrapped as {ok:true,result:<check result>}; current matching revision, scope, lease and owner.','No old intent replay; new runner has a new durable intent and isolated outputs.','Existing SDK/JDK/Gradle/cache/signing loader only; offline Gradle and no signing credentials inspected or printed.'],
    not_executed=dict(install=True,build=True,signature_commands=True,push=True),
    limitations=['Gradle cache/lock writes happen only on future authorized build.','Source byte guards do not replace an OS sandbox around Gradle plugins.','Main plan may be amended independently; protected resources and exact asset pins are enforced, main-plan pin here records preparation basis.'])
new(OUT/'ANDROID29_BUILD_PLAN_DRAFT_R1.json',plan)
print(json.dumps(dict(prepared=str(OUT),protected=len(protected),resources=len(resources),build_started=False)))
