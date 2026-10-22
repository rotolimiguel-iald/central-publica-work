"""Explicit reviewed client-only copy; no process control or web restart."""
from pathlib import Path
import argparse,datetime,json
from prepare import W,MOBILE,SURFACES,NATIVES,sha
from guards import reviewed,science
from transaction import atomic,backup,write_evidence

def main():
    plan=reviewed()
    if (W/'STATIC_APPLY_INTENT.json').exists() or (W/'deployment.json').exists():
        raise ValueError('Prior application exists; inspect receipts, never auto-repeat')
    expected={s/n for s in SURFACES for n in ('iald.js','iald.css')}|{MOBILE/n for n in NATIVES}
    if len(plan['files'])!=10 or {Path(f['destination']).resolve() for f in plan['files']}!=expected:
        raise ValueError('Exactly eight client files and two native versions required')
    old={};new={};backups={};written=[]
    for f in plan['files']:
        dest=Path(f['destination']);old[dest]=dest.read_bytes();new[dest]=Path(f['source']).read_bytes()
        if sha(dest)!=f['baseline']:raise ValueError('Baseline CAS changed')
    write_evidence(W/'STATIC_APPLY_INTENT.json',dict(no_repeat=True,plan_sha256=sha(W/'install_plan.json'),restart=False))
    stamp=datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    try:
        for dest,raw in old.items():
            if dest.is_relative_to(MOBILE):
                saved=W/'mobile_backups'/dest.relative_to(MOBILE)
                saved=saved.with_name(saved.name+'.bak_'+stamp)
                if saved.exists():raise ValueError('Backup already exists')
                atomic(saved,raw);backups[str(dest)]=str(saved)
            else:backups[str(dest)]=backup(dest,stamp)
        reviewed()
        for dest,raw in new.items():
            if dest.read_bytes()!=old[dest]:raise ValueError('Concurrent target edit')
            atomic(dest,raw);written.append(str(dest))
        for dest,raw in new.items():
            if dest.read_bytes()!=raw:raise ValueError('Post-copy mismatch')
        science()
    except BaseException as exc:
        write_evidence(W/'STATIC_APPLY_STOPPED.json',dict(status='PARTIAL_OR_FAILED_RECONCILE_NO_RETRY',
            written=written,backups=backups,error_type=type(exc).__name__,restart=False,whole_set_atomic=False))
        raise
    report=dict(status='INSTALLED_STATIC_NO_RESTART',plan_sha256=sha(W/'install_plan.json'),
        files={str(p.resolve()):sha(p) for p in new},backups=backups,restart=False,
        backend_modified=False,wallet_modified=False,whole_set_atomic=False)
    write_evidence(W/'deployment.json',report)
    print(json.dumps(dict(status=report['status'],files=len(new),restart=False)))

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--apply',action='store_true');a=p.parse_args()
    if not a.apply:raise SystemExit('Explicit --apply after review required')
    main()
