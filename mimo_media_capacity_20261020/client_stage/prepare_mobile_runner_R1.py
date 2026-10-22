"""Prepare new Android30/private-mobile workflow, never build, commit or push.

Optional --main-plan binds an existing reviewed aggregate into a NEW directory.
No original scripts, pinned delivery or runtime files are modified.
"""
from pathlib import Path
import argparse,ast,hashlib,json,sys
S=Path(__file__).resolve().parent;W=S.parent
OLD=W.parent/'mimo26_upgrade_20261020/mobile_stage/android29_R2'
R=Path('C:/IALD/projetos_pyhton/IALD');REPO=R/'iald-app'
def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def pin(p):return dict(path=str(p),sha256=digest(p))
def put(p,data):
    raw=data if isinstance(data,bytes) else (json.dumps(data,ensure_ascii=False,indent=2)+'\n').encode()
    with Path(p).open('xb') as f:f.write(raw)
    assert Path(p).read_bytes()==raw
def main():
    a=argparse.ArgumentParser(description=__doc__);a.add_argument('--out',required=True,type=Path);a.add_argument('--main-plan',type=Path);a.add_argument('--main-sha256');args=a.parse_args()
    out=args.out.resolve();assert out.parent==S.resolve();out.mkdir(exist_ok=False)
    mobile_path=S/'release_R5/install_plan_R5.json';mobile=json.loads(mobile_path.read_bytes())
    entries=mobile['files'];expected={x['destination'].lower():x['sha256'] for x in entries}
    for x in entries:assert digest(x['source'])==x['sha256']
    frozen=None;current=None
    if args.main_plan:
        p=args.main_plan.resolve();assert p.is_relative_to(W.resolve()) and digest(p)==args.main_sha256
        aggregate=json.loads(p.read_bytes());assert len(aggregate['files'])==18
        actual={str(Path(x['destination'])).lower():x['sha256'] for x in aggregate['files']}
        assert all(actual.get(k)==v for k,v in expected.items()),'Aggregate does not contain the exact six client pins'
        put(out/'MAIN_INSTALL_PLAN_FROZEN.json',p.read_bytes());current=pin(p);frozen=pin(out/'MAIN_INSTALL_PLAN_FROZEN.json')
    old=json.loads((OLD/'ANDROID29_BUILD_PLAN_R2.json').read_bytes())
    publisher=json.loads((OLD/'PRIVATE_MOBILE_PUBLISH_PLAN_R2.json').read_bytes())
    sources=['run_android29_R2.py','audit_android29_R2.py','android29_R2.init.gradle','private_mobile_publish_R2.py','public_archive_parsers_source.py','resume_private_commit_CRLF_R1.py','ANDROID29_BUILD_PLAN_R2.json','PRIVATE_MOBILE_PUBLISH_PLAN_R2.json']
    lineage=[pin(OLD/n) for n in sources]
    # Reuse audited behavior, with literal version/name/path changes only.
    names={'run_android29_R2.py':'run_android30_R1.py','audit_android29_R2.py':'audit_android30_R1.py','android29_R2.init.gradle':'android30_R1.init.gradle','private_mobile_publish_R2.py':'private_mobile_publish_R1.py'}
    for src,dst in names.items():
        text=(OLD/src).read_bytes().decode('utf-8')
        text=text.replace('android29_R2','android30_R1').replace('ANDROID29_BUILD_PLAN_R2','ANDROID30_BUILD_PLAN_R1').replace('PRIVATE_MOBILE_PUBLISH_PLAN_R2','PRIVATE_MOBILE_PUBLISH_PLAN_R1')
        text=text.replace('Android29','Android30').replace('android29_build','android30_build').replace('iOS34 Android29','iOS35 Android30')
        text=text.replace('4.1(29)','4.1(30)').replace("versionCode='29'","versionCode='30'").replace('compiled_versionCode=29','compiled_versionCode=30').replace('manifest29','manifest30')
        text=text.replace('versionCode != 29','versionCode != 30').replace('versionCode = 29','versionCode = 30').replace('Previous28','Previous29').replace('previous28','previous29')
        if dst.endswith('.gradle'):
            text=text.replace('C:/IALD/Central de Patentes/work/mimo26_upgrade_20261020/mobile_stage/android30_R1/attempts',(out/'attempts').as_posix())
        if dst=='run_android30_R1.py':
            marker='    for key in ("main_plan_current_pin", "main_plan_frozen_pin"):'
            assert marker in text
            text=text.replace(marker,'    if not plan.get("main_plan_current_pin") or not plan.get("main_plan_frozen_pin"):\n        raise RuntimeError("UNBOUND: aggregate 18-file plan not pinned; prepare a new bound workflow")\n'+marker)
            marker='    for source in receipt["sources"]:'
            assert marker in text
            text=text.replace(marker,'    for gate in ("independent_review", "installed_verification"):\n        evidence=receipt.get(gate)\n        if not evidence or evidence.get("main_plan_sha256") != json.loads(plan_path.read_bytes())["main_plan_current_pin"]["sha256"]:\n            raise RuntimeError("Matching independently reviewed/installed main plan evidence required")\n        item=Path(evidence["path"]).resolve(strict=True)\n        if not item.is_relative_to(WORK.resolve()) or digest(item)!=evidence["sha256"]:\n            raise RuntimeError("Review or installation evidence changed")\n'+marker)
        if dst=='private_mobile_publish_R1.py':
            # Exact byte staging avoids text:auto / core.autocrlf normalization.
            text=text.replace('from run_android30_R1 import','from run_android30_R1 import')
            marker="        git(root,'add','--',*sorted(allowed))"
            assert marker in text
            text=text.replace(marker,"        for name in sorted(allowed):\n            mode=git(root,'ls-files','--stage','--',name).decode().split()[0]\n            if mode!='100644':raise RuntimeError('Unexpected tracked mode')\n            oid=lines(root,'hash-object','-w','--no-filters','--',name)\n            git(root,'update-index','--cacheinfo',mode,oid,name)")
        if dst.endswith('.py'):ast.parse(text)
        put(out/dst,text.encode())
    put(out/'public_archive_parsers_source.py',(OLD/'public_archive_parsers_source.py').read_bytes())
    plan=old.copy()
    # Remove old authorization/command/publication pointers, never reuse old lease.
    for key in ['apple_baseline','main_plan_preparation_pin','authorization_sources','execution_command','audit_command','supersedes_workflow']:
        plan.pop(key,None)
    plan.update(status='BOUND_WAIT_REVIEW_INSTALL' if current else 'UNBOUND_WAIT_GOODALL_FINAL_18_FILE_PLAN',
        unit='F9.MIMO_MEDIA_CAPACITY_20261020',reference=pin(W/'SESSION_REFERENCE.json'),versionCode=30,
        accepted_js_sha256=entries[0]['sha256'],resource_plan=pin(mobile_path),
        main_plan_current_pin=current,main_plan_frozen_pin=frozen,main_plan_file_count=18,
        parser_source=pin(out/'public_archive_parsers_source.py'),
        candidate_files=[pin(out/n) for n in [*names.values(),'public_archive_parsers_source.py']],
        preconditions=['Independent parent review and installed verification before effects.','Current deploy lease/preflight, source-linked authorization with review/install pins.','No existing intent may be retried; reconcile PID, output and Git state.'],
        limitations=['No build/push executed. iOS35 availability unverified. No UI navigation.','No Google Play publication.','Archive checks require real artifacts and unchanged toolchain.'])
    # Read only audited public build-input allowlist; never enumerate secrets.
    for group in ['protected_inputs','resource_files','tool_pins']:
        fresh=[]
        for e in old[group]:
            p=Path(e['path']);item=e.copy();item['sha256']=expected.get(str(p).lower(),digest(p));fresh.append(item)
        plan[group]=fresh
    plan['registry']=pin(old['registry']['path'])
    previous=OLD/'attempts/20261020T193653_239278Z/projects/app/outputs/apk/release/app-release.apk'
    delivery=json.loads((OLD/'DELIVERY_EXECUTED_R1.json').read_bytes())
    assert previous.is_file() and digest(previous)=='ba0b31ad897c2e90ac4876d320fb7c6298690bb6804ac4f91e68f19411fdac9a'
    plan['baseline_apk']=pin(previous)
    plan['not_executed']=dict(build=True,signature_commands=True,commit=True,push=True,install=True)
    put(out/'ANDROID30_BUILD_PLAN_R1.json',plan)
    # Repository baseline is read from actual .git HEAD/ref bytes (no credentials).
    gitdir=REPO/'.git';assert gitdir.is_dir()
    ref=(gitdir/'HEAD').read_text().strip();assert ref=='ref: refs/heads/codex/mobile-release'
    branchref=gitdir/ref[5:];head=branchref.read_text().strip()
    assert len(head)==40 and all(c in '0123456789abcdef' for c in head)
    files={str(Path(x['destination']).relative_to(REPO)).replace('\\','/'):x['sha256'] for x in entries if Path(x['destination']).is_relative_to(REPO)}
    files.pop('android/app/src/main/assets/public/iald.js') # ignored generated resource, never force-add
    assert len(files)==4
    publisher.update(status=plan['status'],baseline_head=head,files=files,main_plan_current_pin=current,
        main_plan_frozen_pin=frozen,main_plan_file_count=18,script=pin(out/'private_mobile_publish_R1.py'),
        preconditions=plan['preconditions']+['Exact origin and branch; clean index; only four tracked allowlist changes.','Raw blob hash-object --no-filters and update-index; no git add, no force.','Push can trigger Xcode Cloud; no uncertain retry.'],commit=False,push=False)
    publisher.pop('supersedes_workflow',None)
    put(out/'PRIVATE_MOBILE_PUBLISH_PLAN_R1.json',publisher)
    templates={}
    for op,filename in [('android30_build','ANDROID30_BUILD_PLAN_R1.json'),('private_mobile_commit','PRIVATE_MOBILE_PUBLISH_PLAN_R1.json'),('private_mobile_push','PRIVATE_MOBILE_PUBLISH_PLAN_R1.json')]:
        templates[op]=dict(operation=op,reference=str(W/'SESSION_REFERENCE.json'),plan_sha256=digest(out/filename),
            authority='source_linkage_not_identity_authentication',sources=[pin(W/'ORIGINAL.txt')],
            independent_review=None,installed_verification=None,status='TEMPLATE_NOT_EXECUTION_AUTHORITY')
    put(out/'AUTHORIZATION_TEMPLATES_NOT_VALID.json',templates)
    result=dict(status=plan['status'],files=[pin(p) for p in out.iterdir() if p.is_file()],reuse_sources=lineage,
        baseline_head_readonly=head,client_plan=pin(mobile_path),execution=False,
        pending=['Goodall aggregate exact18-file pin','Parent independent review','Installation PASS','Fresh deploy preflight','Completed authorization source linkage receipts'])
    put(out/'DELIVERY_PREPARED_R1.json',result);print(json.dumps(pin(out/'DELIVERY_PREPARED_R1.json')))
if __name__=='__main__':main()
