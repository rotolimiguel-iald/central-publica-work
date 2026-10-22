"""Prepare six mobile targets and non-installable effective18; never install/build/push."""
from pathlib import Path
import ast,hashlib,json
S=Path(__file__).resolve().parent;W=S.parent;R=Path('C:/IALD/projetos_pyhton/IALD')
OLD=S/'android30_bound_final';PACKET=S/'mobile_R7_binding';OUT=S/'android30_R7_bound'
def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def pin(p):return dict(path=str(p),sha256=digest(p))
def put(p,raw):
    p.parent.mkdir(parents=True,exist_ok=True)
    if not isinstance(raw,bytes):raw=(json.dumps(raw,ensure_ascii=False,indent=2)+'\n').encode()
    with p.open('xb') as f:f.write(raw)
    assert p.read_bytes()==raw
def main():
    PACKET.mkdir(exist_ok=False);OUT.mkdir(exist_ok=False)
    original=W/'install_plan.json';hotfix=S/'bootstrap_hotfix_R7/install_plan_R7_FINAL.json'
    assert digest(original)=='72d19db34439ebc2ecad0bb29d55388780ee10a084ebd817c71b08141c2b5103'
    base=json.loads(original.read_bytes());fix=json.loads(hotfix.read_bytes())
    assert len(base['files'])==18 and len(fix['files'])==4
    changes={x['destination']:x for x in fix['files']}
    six=[]
    oldmobile=json.loads((S/'release_R6/install_plan_R6_FINAL.json').read_bytes())
    for entry in oldmobile['files']:
        chosen=changes.get(entry['destination'],entry);source=Path(chosen['source'])
        assert digest(source)==chosen['sha256']
        dest=Path(entry['destination']);staged=PACKET/'six_targets'/dest.relative_to(R)
        put(staged,source.read_bytes())
        six.append(dict(source=str(staged),destination=str(dest),sha256=chosen['sha256'],installed_by='hotfix4' if str(dest) in changes else 'original18'))
        if str(dest) not in changes:assert digest(dest)==chosen['sha256'],'Native35/30 baseline changed'
    mobile=PACKET/'CLIENT6_R7_NOT_INSTALLABLE.json'
    put(mobile,dict(status='NOT_INSTALLABLE_MOBILE_BUILD_INPUTS',installable=False,files=six,versions=dict(ios=35,android=30),instruction='Only hotfix4 is a new installation; native versions already installed by original18.'))
    effective=[]
    for entry in base['files']:
        selected=changes.get(entry['destination'],entry)
        assert digest(selected['source'])==selected['sha256']
        effective.append(dict(source=selected['source'],destination=entry['destination'],sha256=selected['sha256'],bytes=Path(selected['source']).stat().st_size,origin='hotfix4' if entry['destination'] in changes else 'original18'))
    effective_path=PACKET/'EFFECTIVE18_R7_NOT_INSTALLABLE.json'
    # Preserve original installation receipt bytes even if parent writes new R7 receipts elsewhere.
    installed=W/'INSTALLED_VERIFICATION.json';review=W/'validation/review_final.json'
    for src,name in [(installed,'ORIGINAL18_INSTALLED_VERIFICATION.json'),(review,'ORIGINAL18_REVIEW_FINAL.json')]:
        data=json.loads(src.read_bytes());assert data['status']=='PASS' and data['plan_sha256']==digest(original)
        put(PACKET/name,src.read_bytes())
    chain=dict(original18_plan=pin(original),hotfix4_plan=pin(hotfix),
        original18_installed=pin(PACKET/'ORIGINAL18_INSTALLED_VERIFICATION.json'),original18_review=pin(PACKET/'ORIGINAL18_REVIEW_FINAL.json'))
    put(effective_path,dict(status='NOT_INSTALLABLE_EFFECTIVE_STATE',installable=False,files=effective,original18_plan=pin(original),hotfix4_plan=pin(hotfix),
        installation_receipts=[dict(role='original18',**chain['original18_installed']),dict(role='hotfix4',path=None,sha256=None,status='PENDING_ACTUAL_HOTFIX_INSTALLATION')],
        instruction='A derived effective build/provenance view only; never apply original18 again. Install only the separately reviewed hotfix4 plan.'))
    put(OUT/'EFFECTIVE18_R7_FROZEN_NOT_INSTALLABLE.json',effective_path.read_bytes())
    for name in ['run_android30_R1.py','audit_android30_R1.py','private_mobile_publish_R1.py','public_archive_parsers_source.py','android30_R1.init.gradle']:
        raw=(OLD/name).read_bytes()
        if name=='android30_R1.init.gradle':raw=raw.replace((OLD/'attempts').as_posix().encode(),(OUT/'attempts').as_posix().encode())
        if name=='run_android30_R1.py':
            text=raw.decode();text=text.replace('import argparse','from release_lineage_R7 import verify_effective, verify_release_admission\nimport argparse',1)
            mark='    for key in ("main_plan_current_pin", "main_plan_frozen_pin"):'
            assert mark in text;text=text.replace(mark,'    verify_effective(plan, WORK)\n'+mark,1)
            start=text.index('    for gate in ("independent_review", "installed_verification"):')
            end=text.index('    for source in receipt["sources"]:',start)
            text=text[:start]+'    verify_release_admission(receipt, json.loads(plan_path.read_bytes()), WORK)\n'+text[end:]
            raw=text.encode()
        if name.endswith('.py'):ast.parse(raw)
        put(OUT/name,raw)
    put(OUT/'release_lineage_R7.py',(S/'release_lineage_guard_R7.py').read_bytes())
    expected={x['destination'].lower():x['sha256'] for x in six}
    build=json.loads((OLD/'ANDROID30_BUILD_PLAN_R1.json').read_bytes())
    build.update(status='R7_BOUND_PENDING_REVIEW_HOTFIX_INSTALL_UI_AND_PARENT_EXECUTION_ORDER',accepted_js_sha256=six[0]['sha256'],resource_plan=pin(mobile),
        main_plan_current_pin=pin(effective_path),main_plan_frozen_pin=pin(OUT/'EFFECTIVE18_R7_FROZEN_NOT_INSTALLABLE.json'),installation_chain=chain,
        candidate_files=[pin(OUT/n) for n in ['run_android30_R1.py','audit_android30_R1.py','private_mobile_publish_R1.py','public_archive_parsers_source.py','android30_R1.init.gradle','release_lineage_R7.py']],
        parser_source=pin(OUT/'public_archive_parsers_source.py'))
    for group in ['protected_inputs','resource_files']:
        for item in build[group]:item['sha256']=expected.get(item['path'].lower(),item['sha256'])
    put(OUT/'ANDROID30_BUILD_PLAN_R1.json',build)
    publisher=json.loads((OLD/'PRIVATE_MOBILE_PUBLISH_PLAN_R1.json').read_bytes())
    publisher.update(status=build['status'],accepted_js_sha256=six[0]['sha256'],main_plan_current_pin=build['main_plan_current_pin'],main_plan_frozen_pin=build['main_plan_frozen_pin'],installation_chain=chain,script=pin(OUT/'private_mobile_publish_R1.py'))
    publisher['files']={p:expected[str(R/'iald-app'/p).lower()] for p in publisher['files']}
    publisher.pop('authorization_sources',None)
    put(OUT/'PRIVATE_MOBILE_PUBLISH_PLAN_R1.json',publisher)
    for op,name in [('android30_build','ANDROID30_BUILD_PLAN_R1.json'),('private_mobile_commit','PRIVATE_MOBILE_PUBLISH_PLAN_R1.json'),('private_mobile_push','PRIVATE_MOBILE_PUBLISH_PLAN_R1.json')]:
        reviews=[dict(role='original18',**chain['original18_review']),dict(role='hotfix4',path=None,sha256=None)]
        installations=[dict(role='original18',**chain['original18_installed']),dict(role='hotfix4',path=None,sha256=None)]
        put(OUT/('TEMPLATE_'+op.upper()+'.json'),dict(status='TEMPLATE_INVALID_WAIT_PARENT_RELEASE_AFTER_UI',operation=op,reference=str(W/'SESSION_REFERENCE.json'),plan_sha256=digest(OUT/name),authority='source_linkage_not_identity_authentication',sources=[],review_receipts=reviews,installation_receipts=installations,ui_verification=None,required_future_source='New parent execution authorization after R7 installation and actual UI PASS; earlier R6 execution authorization remains blocked.'))
    put(OUT/'DELIVERY_PREPARED_R7.json',dict(status=build['status'],effective_manifest=pin(effective_path),mobile6=pin(mobile),installation_chain=chain,
        files=[pin(p) for p in OUT.iterdir() if p.is_file()],build=False,commit=False,push=False,install=False,
        instruction='NOT_INSTALLABLE effective18; original18 already installed, only hotfix4 still pending. Two independent actual-plan installation receipts plus UI evidence and new parent execution order required.'))
    print(json.dumps(pin(OUT/'DELIVERY_PREPARED_R7.json')))
if __name__=='__main__':main()
