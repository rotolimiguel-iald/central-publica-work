"""Parent-only explicit application after independent review; no automatic resume."""
from pathlib import Path
import argparse,json,sys
from atomic_append import append_reviewed,exclusive,sha
HERE=Path(__file__).resolve().parent
W=HERE.parent

def load(p):return json.loads(Path(p).read_bytes())
def checked_pin(p):
    raw=Path(p['path']).read_bytes()
    if sha(raw)!=p['sha256'] or ('bytes' in p and len(raw)!=p['bytes']):
        raise ValueError('Pinned evidence changed: '+str(p['path']))
    return raw
def save(p,value):exclusive(p,json.dumps(value,ensure_ascii=False,indent=2).encode())

def main(plan_path,review_path):
    plan_path=Path(plan_path).resolve();review_path=Path(review_path).resolve()
    if not plan_path.is_relative_to(HERE) or not review_path.is_relative_to(W):
        raise ValueError('Plan/review outside mission')
    out=plan_path.parent
    if (out/'APPLY_INTENT.json').exists():raise ValueError('Prior intent exists: reconcile partial result, never repeat automatically')
    plan=load(plan_path);review=load(review_path)
    if plan['status']!='FINAL_STAGING_REQUIRES_REVIEW' or plan['final_snapshot'] is not True:
        raise ValueError('Nonfinal staging refused')
    if (review['status']!='PASS' or review.get('reviewer') in (None,'','codex-app-01a094df')
        or review['plan_sha256']!=sha(plan_path.read_bytes())
        or review['applicator_sha256']!=sha(Path(__file__).read_bytes())
        or review['helper_sha256']!=sha((HERE/'atomic_append.py').read_bytes())):
        raise ValueError('Independent review/pins missing or stale')
    if plan['reference']!=str(W/'SESSION_REFERENCE.json') or plan['parent_owner']!='codex-app-01a094df':
        raise ValueError('Wrong mission/owner')
    surfaces=load(plan['reuse']['surfaces']['path'])['surfaces']
    checked_pin(plan['reuse']['surfaces'])
    expected={Path(r['path']).resolve() for r in surfaces}
    actual=[Path(r['path']).resolve() for r in plan['surfaces']]
    if len(actual)!=8 or len(set(actual))!=8 or set(actual)!=expected:
        raise ValueError('Exact eight surfaces required')
    for item in plan['sources']:checked_pin(item)
    chunk=checked_pin(plan['append'])
    for row in plan['surfaces']:
        target=Path(row['path']);before=target.read_bytes()
        if target.name.upper()=='MEMORY.MD' or sha(before)!=row['before_sha256'] or len(before)!=row['before_bytes']:
            raise ValueError('Memory CAS mismatch; refresh staging before any write')
        if sha(before+chunk)!=row['expected_after_sha256'] or len(before+chunk)!=row['expected_after_bytes']:
            raise ValueError('Expected append mismatch')
    sys.path.insert(0,str(W))
    import task
    preflight=task.check('memory_postdelivery')
    save(out/'APPLY_INTENT.json',dict(no_repeat=True,plan_sha256=sha(plan_path.read_bytes()),
        review_sha256=sha(review_path.read_bytes()),preflight=preflight))
    done=[]
    try:
        for index,row in enumerate(plan['surfaces'],1):
            result=append_reviewed(row['path'],chunk,row['before_sha256'],row['expected_after_sha256'],apply=True)
            done.append(result);save(out/('APPLIED_%02d.json'%index),result)
        for row in plan['surfaces']:
            if sha(Path(row['path']).read_bytes())!=row['expected_after_sha256']:raise ValueError('Post-apply pin mismatch')
    except BaseException as exc:
        save(out/'APPLY_STOPPED.json',dict(status='STOPPED_RECONCILE_NO_AUTORETRY',completed=done,error_type=type(exc).__name__,whole_set_atomic=False))
        raise
    save(out/'APPLIED.json',dict(status='APPLIED_VERIFIED',files=done,surfaces=8,whole_set_atomic=False,
        scope='Operational append only; no scientific/runtime/build changes; backups retained'))

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--plan',required=True);p.add_argument('--review',required=True)
    p.add_argument('--apply',action='store_true');a=p.parse_args()
    if not a.apply:raise SystemExit('Preparation only: explicit --apply required from parent after review')
    main(a.plan,a.review)
