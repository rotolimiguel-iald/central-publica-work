"""Continue the reconciled pre-commit refusal; preserve raw approved JS bytes.

No source, attributes, config or allowlist changes. Do not replay uncertain Git calls.
"""
from pathlib import Path
import argparse, hashlib, json
from private_mobile_publish_R2 import git, lines, changed, PLAN
from run_android29_R2 import require_approval, fresh_preflight, verify_main_plan, save, pin

HERE=Path(__file__).resolve().parent
def resume(preflight):
    p=json.loads(PLAN.read_bytes());verify_main_plan(p)
    require_approval(HERE/'AUTHORIZATION_PRIVATE_COMMIT_R2.json','private_mobile_commit',PLAN)
    attempt=HERE/'git_commit_R1'
    reconciliation=json.loads((attempt/'RECONCILIATION_R1.json').read_bytes())
    if (attempt/'RESULT.json').exists() or (attempt/'RAW_BLOB_CONTINUATION_INTENT_R1.json').exists():
        raise RuntimeError('Prior result/continuation must be reconciled; no replay')
    if reconciliation['head']!=p['baseline_head'] or not all(x['only_CRLF_normalization'] for x in reconciliation['files'].values()):
        raise RuntimeError('This continuation is only for verified pre-commit CRLF refusal')
    checkdir=attempt/'continuation_preflight_R1';checkdir.mkdir(exist_ok=False)
    fresh_preflight(preflight,checkdir)
    root=Path(p['repository']);allowed=set(p['files'])
    if lines(root,'rev-parse','HEAD')!=p['baseline_head'] or changed(root,'HEAD')!=allowed or changed(root,'--cached')!=allowed:
        raise RuntimeError('HEAD/index/allowlist changed during reconciliation')
    for args in [('remote','get-url','origin'),('remote','get-url','--push','origin')]:
        if lines(root,*args) not in p['exact_origins']:raise RuntimeError('Unexpected private origin')
    if lines(root,'branch','--show-current')!=p['branch']:raise RuntimeError('Unexpected private branch')
    for name,expected in p['files'].items():
        if hashlib.sha256((root/name).read_bytes()).hexdigest()!=expected:raise RuntimeError('Installed bytes changed')
    save(attempt/'RAW_BLOB_CONTINUATION_INTENT_R1.json',dict(status='PRE_COMMIT_REFUSAL_RECONCILED',
        reconciliation=pin(attempt/'RECONCILIATION_R1.json'),plan=pin(PLAN),baseline_head=p['baseline_head'],
        method='Raw approved blobs via hash-object --no-filters and exact existing update-index modes; no attributes/config changes.',no_repeat=True))
    for name in sorted(allowed):
        expected=p['files'][name]
        if hashlib.sha256(git(root,'show',':'+name)).hexdigest()==expected:continue
        mode=lines(root,'ls-files','-s','--',name).split()[0]
        if mode!='100644':raise RuntimeError('Unexpected file mode')
        oid=lines(root,'hash-object','-w','--no-filters','--',str(root/name))
        git(root,'update-index','--cacheinfo',mode,oid,name)
    if changed(root,'--cached')!=allowed:raise RuntimeError('Staged allowlist changed')
    for name,expected in p['files'].items():
        if hashlib.sha256(git(root,'show',':'+name)).hexdigest()!=expected:raise RuntimeError('Exact staged-byte guard failed')
    verify_main_plan(p)
    git(root,'commit','-m','Update MiMo mobile assets and prepare iOS34 Android29')
    head=lines(root,'rev-parse','HEAD')
    if changed(root,p['baseline_head'],head)!=allowed or lines(root,'rev-parse','HEAD^')!=p['baseline_head']:
        raise RuntimeError('Unexpected resulting commit; reconcile without repetition')
    for name,expected in p['files'].items():
        if hashlib.sha256(git(root,'show',head+':'+name)).hexdigest()!=expected:raise RuntimeError('Committed bytes differ')
    save(attempt/'RESULT.json',dict(status='COMMITTED_NOT_PUSHED',commit=head,paths=sorted(allowed),
        plan=pin(PLAN),continuation=pin(attempt/'RAW_BLOB_CONTINUATION_INTENT_R1.json'),exact_committed_bytes=True))
    return dict(status='COMMITTED_NOT_PUSHED',commit=head,files=len(allowed),exact_bytes=True)
if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--preflight',type=Path,required=True)
    args=parser.parse_args()
    try:print(json.dumps(resume(args.preflight)))
    except Exception as exc:raise SystemExit(type(exc).__name__+': continuation did not complete; preserve intent and reconcile')
