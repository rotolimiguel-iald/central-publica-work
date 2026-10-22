"""Prepare/bind final19 mobile workflow. Never install, build, commit or push."""
from pathlib import Path
import argparse,ast,hashlib,json,sys
S=Path(__file__).resolve().parent;W=S.parent;R=Path('C:/IALD/projetos_pyhton/IALD')
HERE=S/'mobile_R9_preparation_R2';CONFIG=HERE/'R8_RELEASE_CONTRACT.json';OLD=S/'android30_R7_bound'
sys.path.insert(0,str(S));import release_lineage_guard_R9 as guard
def pin(p):return dict(path=str(p),sha256=guard.digest(p))
def put(p,raw):
    p.parent.mkdir(parents=True,exist_ok=True)
    if not isinstance(raw,bytes):raw=(json.dumps(raw,ensure_ascii=False,indent=2)+'\n').encode()
    with p.open('xb') as f:f.write(raw)
    assert p.read_bytes()==raw
def prepare(label_review=None):
    HERE.mkdir(exist_ok=False)
    layers=[]
    specs=[('original18',W,18,W/'validation/review_final.json'),
      ('R7four',S/'bootstrap_hotfix_R7',4,W/'review_bootstrap_R7/REVIEW_R7.json'),
      ('capabilitythree',W/'host_followup/capability_R2',3,W/'host_followup/capability_R2/validation/review_final.json'),
      ('availabilitytwo',W/'host_followup/availability_deploy_R1',2,W/'host_followup/availability_deploy_R1/validation/review_final.json'),
      ('label4',S/'media_label_R8',4,label_review or W/'REVIEW_LABEL_R8.json')]
    names={'original18':'install_plan.json','R7four':'install_plan_R7_FINAL.json','capabilitythree':'install_plan.json','availabilitytwo':'install_plan.json','label4':'install_plan_LABEL_R8.json'}
    union=set()
    for role,folder,count,review in specs:
        plan=folder/names[role];data=json.loads(plan.read_bytes());destinations=list(guard.file_map(data));assert len(destinations)==count
        if role=='original18':assert pin(plan)['sha256']=='72d19db34439ebc2ecad0bb29d55388780ee10a084ebd817c71b08141c2b5103'
        if role in ('R7four','label4'):assert set(destinations)=={str(R/p) for p in ['app/iald.js','iald-app/www/iald.js','iald-app/ios/App/App/public/iald.js','iald-app/android/app/src/main/assets/public/iald.js']}
        if role=='capabilitythree':assert set(destinations)=={str(R/p) for p in ['new_private_media_host.py','iald_auto_router.py','iald_web_server.py']}
        if role=='availabilitytwo':assert set(destinations)=={str(R/p) for p in ['iald_auto_router.py','iald_jev_connection_evidence.json']}
        union.update(destinations)
        layer=dict(role=role,count=count,plan=pin(plan),destinations=destinations,review=pin(review) if review.exists() else dict(path=str(review),sha256=None,status='PENDING_ACTUAL_REVIEW'))
        for kind in ['deployment','restart']:
            p=folder/(kind+'.json');layer[kind]=pin(p) if p.exists() else dict(path=str(p),sha256=None,status='PENDING_ACTUAL_RECEIPT')
        layers.append(layer)
    assert len(union)==19
    mobile_path=S/'mobile_R7_binding/CLIENT6_R7_NOT_INSTALLABLE.json';mobile=json.loads(mobile_path.read_bytes())
    label=json.loads((S/'media_label_R8/install_plan_LABEL_R8.json').read_bytes());label_map={x['destination']:x for x in label['files']}
    mobile['files']=[label_map.get(x['destination'],x) for x in mobile['files']]
    mobile.update(status='NOT_INSTALLABLE_MOBILE_BUILD_INPUTS_LABEL_R9',installable=False)
    mobile_path=HERE/'CLIENT6_LABEL_R9_NOT_INSTALLABLE.json';put(mobile_path,mobile)
    config=dict(schema='iald.mobile.final19-binding/v1',status='PREPARATION_NOT_EXECUTION_AUTHORITY',layers=layers,allowed_runtime_destinations=sorted(union),
        only_added_health_file=str(R/'iald_jev_connection_evidence.json'),mobile6=guard.file_map(mobile),mobile6_manifest=pin(mobile_path),
        science_baseline=pin(W/'SCIENCE_BASELINE.json'),reference=pin(W/'SESSION_REFERENCE.json'),guard_source=pin(S/'release_lineage_guard_R9.py'),
        engineering_phase_review=pin(W/'REVIEW_BUILD_PUSH_PHASE_R8.json'),private_mobile_allowlist=['android/app/build.gradle','ios/App/App.xcodeproj/project.pbxproj','ios/App/App/public/iald.js','www/iald.js'],repository_baseline_head='58b17734efa8f7c815942ba60e95c5cc3dc033d0',
        final_manifest_contract=dict(path=str(W/'FINAL_RUNTIME_PINS.json'),status='PASS_EFFECTIVE_RUNTIME_NOT_INSTALLABLE (or PASS)',files='Exactly19 unique path(or destination)/sha256 rows; ordered four-layer union. No unknown path is read.'),
        phase_addendum_contract=dict(status='PASS',actor='real distinct reviewer',phase_review_sha256='SHA of actual phase review',final_manifest_sha256='SHA of actual new final19',execution_plan_sha256={'android30_build':'new build plan SHA','private_mobile_commit':'new private plan SHA','private_mobile_push':'same new private plan SHA'}),
        not_installable=True,execution=False)
    put(CONFIG,config)
    pending=[]
    try:guard.check_chain(config,W,installed=False)
    except RuntimeError as e:
        if str(e)!='Pending pinned evidence':raise
        pending.append('label4 distinct review')
    guard.check_science(config,W)
    put(HERE/'DELIVERY_PREPARED_R8.json',dict(status='PREPARED_WAIT_FINAL19_AND_ALL_INSTALLATION_RECEIPTS_AUTOTEST',contract=pin(CONFIG),guard=pin(S/'release_lineage_guard_R9.py'),builder=pin(Path(__file__)),layers=5,pending=pending,unique_destinations=19,mobile_targets=6,versions=dict(ios=35,android=30),build=False,commit=False,push=False,runtime_writes=False))
    return dict(status='PREPARED_PENDING_NOT_READY',delivery=pin(HERE/'DELIVERY_PREPARED_R8.json'))
def complete_config(args):
    config=json.loads(CONFIG.read_bytes());None # guard code pin is verified directly below
    if guard.digest(config['guard_source']['path'])!=config['guard_source']['sha256']:raise RuntimeError('Guard source changed')
    for layer in config['layers']:
        if layer['role']=='label4':
            for kind, supplied in [('review',args.label_review),('deployment',args.label_deployment),('restart',args.label_restart)]:
                if supplied:layer[kind]=pin(guard.safe(supplied,W))
            if not layer['review'].get('sha256'):
                layer['review']=pin(guard.safe(layer['review']['path'],W))
        for kind in ['deployment','restart']:
            item=layer[kind]
            if item.get('sha256') is None:
                p=Path(item['path'])
                if not p.is_file():raise RuntimeError('PENDING '+layer['role']+' '+kind)
                layer[kind]=pin(p)
    return config
def bind(args):
    final=args.final_manifest.resolve(strict=True)
    if final!=W/'FINAL_RUNTIME_PINS.json' or guard.digest(final)!=args.final_sha256:
        raise RuntimeError('Exact parent final19 path and measured SHA required')
    config=complete_config(args);expected=guard.check_final(config,pin(final),W)
    out=args.out.resolve();assert out.parent==S.resolve();out.mkdir(exist_ok=False)
    put(out/'RELEASE_BINDING_FINAL19_R8.json',config);put(out/'FINAL_RUNTIME_PINS_FROZEN_NOT_INSTALLABLE.json',final.read_bytes())
    scripts=['run_android30_R1.py','audit_android30_R1.py','private_mobile_publish_R1.py','public_archive_parsers_source.py','android30_R1.init.gradle']
    for name in scripts:
        raw=(OLD/name).read_bytes()
        if name=='run_android30_R1.py':
            raw=raw.replace(b'from release_lineage_R7 import verify_effective, verify_release_admission',b'from release_lineage_R8 import verify_final_state, verify_release_admission').replace(b'verify_effective(plan, WORK)',b'verify_final_state(plan, WORK)')
        if name=='android30_R1.init.gradle':raw=raw.replace((OLD/'attempts').as_posix().encode(),(out/'attempts').as_posix().encode())
        if name.endswith('.py'):ast.parse(raw)
        put(out/name,raw)
    put(out/'release_lineage_R8.py',(S/'release_lineage_guard_R9.py').read_bytes())
    build=json.loads((OLD/'ANDROID30_BUILD_PLAN_R1.json').read_bytes())
    build.pop('installation_chain',None)
    build.update(status='FINAL19_LABEL_BOUND_WAIT_PHASE_ADDENDUM_AND_CONCRETE_PARENT_GO',accepted_js_sha256=next(v for k,v in config['mobile6'].items() if Path(k).name=='iald.js'),resource_plan=config['mobile6_manifest'],main_plan_current_pin=pin(final),main_plan_frozen_pin=pin(out/'FINAL_RUNTIME_PINS_FROZEN_NOT_INSTALLABLE.json'),main_plan_file_count=19,main_plan_installable=False,
        release_binding=pin(out/'RELEASE_BINDING_FINAL19_R8.json'),candidate_files=[pin(out/n) for n in [*scripts,'release_lineage_R8.py']],parser_source=pin(out/'public_archive_parsers_source.py'),
        preconditions=['All four actual deployments+reviews+restarts pinned; source and overlay baseline continuity verified.','Only latest19 runtime hashes required, historical18 source evidence retained.','Science/mobile6 current; engineering review and distinct effective-pin/binding addendum PASS plus concrete parent execution release required. Provider perception/additional USD test remains PENDING and is not a build/push gate.','Current deploy preflight and exact private allowlist; no force/retry of uncertain intent.'])
    for group in ['protected_inputs','resource_files']:
        for item in build[group]:item['sha256']=expected.get(item['path'],item['sha256'])
    science=json.loads(Path(config['science_baseline']['path']).read_bytes())
    existing={x['path'] for x in build['protected_inputs']}
    build['protected_inputs'] += [dict(path=p,sha256=h) for p,h in expected.items() if p not in existing]
    build['protected_inputs'] += [dict(path=x['path'],sha256=x['sha256']) for x in science['files'] if x['path'] not in existing]
    put(out/'ANDROID30_BUILD_PLAN_R1.json',build)
    pub=json.loads((OLD/'PRIVATE_MOBILE_PUBLISH_PLAN_R1.json').read_bytes());pub.pop('installation_chain',None)
    pub.update(status=build['status'],main_plan_current_pin=build['main_plan_current_pin'],main_plan_frozen_pin=build['main_plan_frozen_pin'],main_plan_file_count=19,main_plan_installable=False,release_binding=build['release_binding'],script=pin(out/'private_mobile_publish_R1.py'),preconditions=build['preconditions'])
    pub['accepted_js_sha256']=build['accepted_js_sha256']
    pub['files']={name:expected[str(R/'iald-app'/name)] for name in pub['files']}
    put(out/'PRIVATE_MOBILE_PUBLISH_PLAN_R1.json',pub)
    for op,name in [('android30_build','ANDROID30_BUILD_PLAN_R1.json'),('private_mobile_commit','PRIVATE_MOBILE_PUBLISH_PLAN_R1.json'),('private_mobile_push','PRIVATE_MOBILE_PUBLISH_PLAN_R1.json')]:
        put(out/('TEMPLATE_'+op.upper()+'.json'),dict(status='TEMPLATE_NOT_EXECUTION_AUTHORITY',operation=op,reference=str(W/'SESSION_REFERENCE.json'),plan_sha256=guard.digest(out/name),authority='source_linkage_not_identity_authentication',sources=[],phase_binding_addendum=None,execution_authorized_now=False,provider_perception_status='PENDING_OR_NEGATIVE_NOT_SUCCESS',release_binding=build['release_binding']))
    put(out/'DELIVERY_BOUND_R8.json',dict(status=build['status'],final19=pin(final),release_binding=build['release_binding'],files=[pin(p) for p in out.iterdir() if p.is_file()],build=False,commit=False,push=False,install=False))
    return dict(status='BOUND_NOT_EXECUTED',delivery=pin(out/'DELIVERY_BOUND_R8.json'))
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--prepare',action='store_true');p.add_argument('--bind',action='store_true');p.add_argument('--final-manifest',type=Path);p.add_argument('--final-sha256');p.add_argument('--out',type=Path);p.add_argument('--label-review',type=Path);p.add_argument('--label-deployment',type=Path);p.add_argument('--label-restart',type=Path);a=p.parse_args()
    if a.prepare:result=prepare(a.label_review)
    elif a.bind:
        if not a.final_manifest or not a.final_sha256 or not a.out:raise RuntimeError('Final manifest/SHA/new output required')
        result=bind(a)
    else:
        config=json.loads(CONFIG.read_bytes());guard.check_chain(config,W,installed=False);guard.check_science(config,W)
        result=dict(status='WAIT_LABEL_REVIEW_INSTALL_FINAL19_PHASE_ADDENDUM_PARENT_GO',ready=False,build=False)
    print(json.dumps(result))
if __name__=='__main__':
    try:main()
    except Exception as e:print(json.dumps(dict(status='REFUSED_NOT_READY',error=str(e),build=False,commit=False,push=False)));raise SystemExit(2)
