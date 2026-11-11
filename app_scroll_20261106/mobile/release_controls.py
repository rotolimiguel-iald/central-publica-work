"""Validation only. Installation/commit/push belong to the parent, not this helper."""
from pathlib import Path
from prepare_mobile import HERE, REPO, SURFACES, ASSETS, git, read, require, sha

D = HERE/'release'
APP = REPO.parent

def release_installed():
    plan = read(HERE/'PLAN.json')
    authorization = read(HERE/'PARENT_BUILD_READY.json')
    require(authorization.get('status')=='BUILD_AUTHORIZED' and
            authorization.get('parent')=='codex-app-scroll-01a094df' and
            authorization.get('plan_sha256')==sha((HERE/'PLAN.json').read_bytes()), 'Parent build authorization missing or stale')
    review_path = Path(authorization['review_path']).resolve(strict=True)
    require(review_path.is_relative_to(HERE.parent), 'Review outside mission')
    require(sha(review_path.read_bytes())==authorization['review_sha256'], 'Review drift')
    review = read(review_path)
    require(review.get('status')=='PASS' and review.get('plan_sha256')==authorization['plan_sha256'] and
            review.get('reviewer') and review['reviewer'] != 'codex-mobile-prep', 'Independent review required')
    for row in plan['rows']:
        target = Path(row['target'])
        source = Path(row['source'])
        require(target.resolve(strict=True)==target and source.resolve(strict=True).is_relative_to(HERE/'prepared'), 'Redirected path')
        require(sha(source.read_bytes())==row['new']==sha(target.read_bytes()), 'Installed bytes differ from plan')
    assets = {}
    for name in ASSETS:
        values = {sha((REPO/s/name).read_bytes()) for s in SURFACES}
        require(len(values)==1, 'Mobile asset surfaces differ')
        assets[name] = values.pop()
        changed = [r for r in plan['rows'] if r['target']==str(REPO/'www'/name)]
        expected = changed[0]['new'] if changed else plan['baseline']['asset_pins']['www/'+name]
        require(assets[name]==expected, 'Companion asset drift')
    return {'assets':assets, 'review':dict(path=str(review_path),sha256=authorization['review_sha256'])}

def remote_preflight():
    # Deliberately local: remote checking and publication remain parent actions.
    baseline = read(HERE/'BASELINE.json')
    require(git('rev-parse','HEAD').decode().strip()==baseline['base_commit'], 'HEAD changed')
    require(git('branch','--show-current').decode().strip()==baseline['branch'], 'Branch changed')
    require(not (APP/('downloads/IALD-%s-%s.apk'%(baseline['version'],baseline['next_android']))).exists(), 'APK already exists; reconcile')
    release_installed()
