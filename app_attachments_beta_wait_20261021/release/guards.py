"""Read-only final gates shared by future installation and build."""
from pathlib import Path
import json, sys
from prepare import W, ROOT, MOBILE, SURFACES, NATIVES, sha, load, safe

def science():
    baseline=load(W/'SCIENCE_BASELINE.json')
    for f in baseline['files']:
        if sha(f['path']) != f['sha256']:
            raise ValueError('Scientific bytes changed')
    return baseline

def preflight():
    # Parent owns delivery; never borrow a repair/waiting lease.
    sys.path.insert(0,str(W.parent))
    import task
    result=task.check('delivery')
    if not result['ready']:
        raise ValueError('Delivery not ready')
    return result

def reviewed(installed=False):
    plan=load(W/'install_plan.json')
    review=load(W/'validation/review_final.json')
    validation=load(W/'validation/final_checks.json')
    if review['status'] != 'PASS' or review['plan_sha256'] != sha(W/'install_plan.json'):
        raise ValueError('Final independent review missing or stale')
    if not review.get('reviewer') or review['reviewer'] == 'codex-app-01a094df':
        raise ValueError('Independent reviewer required; name alone is not authentication')
    if validation['passed'] is not True or validation['plan_sha256'] != sha(W/'install_plan.json'):
        raise ValueError('Final validation missing or stale')
    required={'prepare.py','guards.py','transaction.py','maintenance.py','deploy_controlled.py',
              'mobile_release.py','android33.init.gradle','mobile_prepare/build_log.py',
              'mobile_prepare/TOOL_PLAN.json','SCIENCE_BASELINE.json','NATIVE_PLAN.json','INPUT_MANIFEST.json',
              'PRIVATE_GIT_PLAN.json','publish_apk33.py'}
    if set(review['tool_pins']) != required:
        raise ValueError('Incomplete reviewed tool set')
    for name,h in review['tool_pins'].items():
        if sha(W/name) != h:
            raise ValueError('Reviewed tooling changed')
    if plan['science_sha256'] != sha(W/'SCIENCE_BASELINE.json'):
        raise ValueError('Science baseline pin changed')
    protected={Path(f['path']).resolve() for f in science()['files']}
    destinations=[]
    allowed={surface/name for surface in SURFACES for name in plan['assets']}
    allowed.update(MOBILE/n for n in NATIVES)
    allowed.update(Path(f['destination']) for f in load(W/'INPUT_MANIFEST.json').get('runtime',[]))
    for f in plan['files']:
        source,target=safe(f['source']),safe(f['destination'])
        if not source.is_relative_to(W) or target not in allowed or target in protected:
            raise ValueError('Unreviewable scope')
        if sha(source)!=f['sha256']:
            raise ValueError('Staged bytes changed')
        actual=sha(target) if target.exists() else None
        if actual != (f['sha256'] if installed else f['baseline']):
            raise ValueError('Target CAS mismatch')
        destinations.append(target)
    if len(destinations)!=len(set(destinations)) or set(destinations)!=allowed:
        raise ValueError('Duplicate or incomplete destinations')
    native=load(W/'NATIVE_PLAN.json')
    if native['ios']!='4.1(38)' or native['android']!='4.1(33)':
        raise ValueError('Native release mismatch')
    preflight()
    return plan
