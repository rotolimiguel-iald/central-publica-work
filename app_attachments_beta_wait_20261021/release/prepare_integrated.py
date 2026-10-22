"""Prepare the received integration once; pin existing real test evidence."""
from pathlib import Path
import ast, json, sys
from prepare import W, ROOT, SURFACES, sha, load, save, assemble
sys.path.insert(0,str(W.parent))
import task

def pin(path):
    path=Path(path)
    return dict(path=str(path),sha256=sha(path),bytes=path.stat().st_size)

def verify_pin(row):
    path=Path(row['path']).resolve()
    if not path.is_relative_to(W.parent):raise ValueError('Evidence escaped mission')
    actual=pin(path)
    if actual['sha256']!=row['sha256'] or actual['bytes']!=row['bytes']:
        raise ValueError('Evidence pin changed: '+str(path))
    return actual

def main():
    preflight=task.check('delivery')
    save(W/'PARENT_PREFLIGHT_PREPARE.json',preflight)
    delivery_path=W.parent/'integration/DELIVERY.json'
    delivery=load(delivery_path)
    allpins=[]
    for field in ['sourcespins','files','test_reports','patches','artifacts']:
        allpins.extend(verify_pin(row) for row in delivery[field])
    verify_pin(delivery['same_byte_checks'])
    combined=load(delivery['same_byte_checks']['path'])
    if combined['status']!='PASS':raise ValueError('Same-byte check failed')
    files={Path(row['path']).name:row for row in delivery['files']}
    if set(files)!={'iald.js','iald.css','iald_app_providers.py'}:
        raise ValueError('Unexpected integrated scope')
    if combined['same_js_sha256']!=files['iald.js']['sha256']:
        raise ValueError('Tests refer to different JS')
    reports=[]
    for row in delivery['test_reports']:
        report=load(row['path'])
        if report['status']!='PASS' or report.get('failures',0)!=0:
            raise ValueError('Behavior report failed')
        if 'results' in report:
            if len(report['results'])!=report['tests'] or not all(x.get('pass') is True or x.get('status')=='PASS' for x in report['results']):
                raise ValueError('Behavior counts/results disagree')
        reports.append(dict(**pin(row['path']),tests=report['tests'],scope=report['scope']))
    if sum(x['tests'] for x in reports)!=51 or delivery['tests_passed']!=51:
        raise ValueError('Expected integration test count changed')
    repair=load(W.parent/'repair/install_plan.json')
    backend=next(x for x in repair['files'] if Path(x['destination']).name=='iald_app_providers.py')
    if files['iald_app_providers.py']['sha256']!=backend['sha256']:
        raise ValueError('Integrated backend differs from accepted repair')
    if sha(backend['destination'])!=backend['baseline']:
        raise ValueError('Backend production baseline changed')
    manifest=dict(assets=[],runtime=[dict(source=files['iald_app_providers.py']['path'],
        destination=backend['destination'],sha256=backend['sha256'],baseline=backend['baseline'])])
    for name in ['iald.js','iald.css']:
        manifest['assets'].append(dict(name=name,source=files[name]['path'],sha256=files[name]['sha256'],
            baselines={str(surface/name):sha(surface/name) for surface in SURFACES}))
    # Production must still match the original sources from which the patch was made.
    for name in ['iald.js','iald.css']:
        baseline=W.parent/'waiting'/(name+'.baseline')
        if sha(ROOT/'app'/name)!=sha(baseline):raise ValueError('Web baseline drift')
    save(W/'MANIFEST_INTEGRATED.json',manifest)
    assemble(W/'MANIFEST_INTEGRATED.json')
    plan=load(W/'install_plan.json')
    for row in plan['files']:
        if sha(row['source'])!=row['sha256'] or sha(row['destination'])!=row['baseline']:
            raise ValueError('Plan source or target drift')
        if Path(row['source']).suffix=='.py':ast.parse(Path(row['source']).read_bytes())
    science=load(W/'SCIENCE_BASELINE.json')
    for row in science['files']:
        if sha(row['path'])!=row['sha256']:raise ValueError('Science changed')
    checks=dict(passed=True,status='PASS_WITH_SCOPE_PENDING_INDEPENDENT_REVIEW',
        plan_sha256=sha(W/'install_plan.json'),files=len(plan['files']),assets=plan['assets'],
        integration_delivery=pin(delivery_path),same_byte_checks=pin(delivery['same_byte_checks']['path']),
        tests_passed=51,test_reports=reports,test_artifacts=allpins,
        tests_rerun_this_step=False,scope='Existing real integration test receipts and all pinned artifacts verified; exact combined bytes frozen into plan. No claim of independent reproduction, browser/device or live provider validation.',
        science_files=len(science['files']),preflight=pin(W/'PARENT_PREFLIGHT_PREPARE.json'),
        parent_owner=task.OWNER,installed=False,builds_executed=0)
    save(W/'validation/final_checks.json',checks)
    request=dict(status='REVIEW_REQUEST_READY_NOT_SENT_TOOL_UNAVAILABLE',
        reviewer_id='01a14479-5823-76a1-bbdd-da2b5edf6705',
        reference=str(task.REF),task_id='delivery',parent_owner=task.OWNER,
        plan=pin(W/'install_plan.json'),checks=pin(W/'validation/final_checks.json'),
        instruction='Review integrated plan, pinned tests and release tools; produce validation/review_final.json with required tool_pins from guards.py plus transaction_sha256, maintenance_sha256 and verifier_sha256. Real independent review required. Do not install, build, commit, push, publish or restart.',
        tooling=[pin(p) for p in [*W.glob('*.py'),W/'android33.init.gradle',W/'mobile_prepare/build_log.py',W/'mobile_prepare/TOOL_PLAN.json']])
    save(W/'REVIEW_REQUEST.json',request)
    print(json.dumps(dict(status='PLAN_PREPARED_REVIEW_PENDING',files=len(plan['files']),tests=51,
        plan_sha256=sha(W/'install_plan.json'),review_request=str(W/'REVIEW_REQUEST.json'))))

if __name__=='__main__':main()
