"""Prepare only by default. Source authorization+deploy preflight required for commit or push."""
from pathlib import Path
import argparse, hashlib, json, subprocess
from run_android30_R1 import require_approval, fresh_preflight, save, pin, verify_main_plan

HERE=Path(__file__).resolve().parent
PLAN=HERE/'PRIVATE_MOBILE_PUBLISH_PLAN_R1.json'
def git(root,*args):
    cp=subprocess.run(['git','-C',str(root),*args],capture_output=True)
    if cp.returncode:raise RuntimeError('Git operation failed: '+args[0]+'; raw output intentionally not exposed')
    return cp.stdout
def lines(root,*args):return git(root,*args).decode('utf-8').strip()
def changed(root,*args):return {x for x in git(root,'diff',*args,'--name-only','-z').decode().split('\0') if x}
def run(operation,approval,preflight):
    plan=json.loads(PLAN.read_bytes());verify_main_plan(plan);require_approval(approval,'private_mobile_'+operation,PLAN)
    root=Path(plan['repository']);attempt=HERE/('git_'+operation+'_R1')
    attempt.mkdir(exist_ok=False)  # Existing attempt is uncertain, never replayed.
    fresh_preflight(preflight,attempt)
    branch=plan['branch'];base=plan['baseline_head'];allowed=set(plan['files'])
    if lines(root,'branch','--show-current')!=branch:raise RuntimeError('Unexpected private branch')
    url=lines(root,'remote','get-url','origin')
    pushurl=lines(root,'remote','get-url','--push','origin')
    # Never persist or print the URLs or credential-bearing command output.
    if url not in plan['exact_origins'] or pushurl not in plan['exact_origins']:raise RuntimeError('Unexpected private origin')
    for name,expected in plan['files'].items():
        if hashlib.sha256((root/name).read_bytes()).hexdigest()!=expected:raise RuntimeError('Installed mobile pin mismatch')
    if changed(root,'--cached'):raise RuntimeError('Existing index changes; do not mix commits')
    if operation=='commit':
        if lines(root,'rev-parse','HEAD')!=base or changed(root,'HEAD')!=allowed:raise RuntimeError('Unexpected tracked changes or HEAD')
        tracked=set(lines(root,'ls-files','--',*sorted(allowed)).splitlines())
        if tracked!=allowed:raise RuntimeError('Allowlist must contain only existing tracked files')
        save(attempt/'INTENT.json',dict(operation='commit',baseline_head=base,paths=sorted(allowed),no_repeat=True,plan=pin(PLAN)))
        for name in sorted(allowed):
            mode=git(root,'ls-files','--stage','--',name).decode().split()[0]
            if mode!='100644':raise RuntimeError('Unexpected tracked mode')
            oid=lines(root,'hash-object','-w','--no-filters','--',name)
            git(root,'update-index','--cacheinfo',mode,oid,name)
        if changed(root,'--cached')!=allowed:raise RuntimeError('Staged allowlist differs; manual reconciliation required')
        for name,expected in plan['files'].items():
            if hashlib.sha256(git(root,'show',':'+name)).hexdigest()!=expected:raise RuntimeError('Git filters changed exact asset/version bytes; manual review required')
        verify_main_plan(plan)
        git(root,'commit','-m','Update MiMo mobile assets and prepare iOS34 Android30')
        head=lines(root,'rev-parse','HEAD')
        if changed(root,base,head)!=allowed or lines(root,'rev-parse','HEAD^')!=base:raise RuntimeError('Unexpected resulting commit')
        save(attempt/'RESULT.json',dict(status='COMMITTED_NOT_PUSHED',commit=head,paths=sorted(allowed),plan=pin(PLAN)))
        return dict(status='COMMITTED_NOT_PUSHED',commit=head)
    receipt=json.loads((HERE/'git_commit_R1/RESULT.json').read_bytes())
    if receipt['plan']!=pin(PLAN) or lines(root,'rev-parse','HEAD')!=receipt['commit'] or changed(root,'HEAD'):
        raise RuntimeError('Pinned clean prepared commit required')
    remote=lines(root,'ls-remote','--heads','origin','refs/heads/'+branch).split()
    if len(remote)!=2 or remote[0]!=base or remote[1]!='refs/heads/'+branch:raise RuntimeError('Remote changed; no force push')
    save(attempt/'INTENT.json',dict(operation='push',commit=receipt['commit'],remote_baseline=base,no_repeat=True,plan=pin(PLAN)))
    verify_main_plan(plan)
    git(root,'push','--porcelain','origin','HEAD:refs/heads/'+branch)
    after=lines(root,'ls-remote','--heads','origin','refs/heads/'+branch).split()
    if len(after)!=2 or after[0]!=receipt['commit']:raise RuntimeError('Push outcome uncertain; reconcile without retry')
    save(attempt/'RESULT.json',dict(status='PUSHED_VERIFIED',commit=after[0],plan=pin(PLAN),store_build_verified=False))
    return dict(status='PUSHED_VERIFIED',commit=after[0],store_build_verified=False)
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);g=p.add_mutually_exclusive_group()
    g.add_argument('--commit',action='store_true');g.add_argument('--push',action='store_true')
    p.add_argument('--authorization','--approval',dest='approval',type=Path);p.add_argument('--preflight',type=Path);a=p.parse_args()
    if not a.commit and not a.push:print(json.dumps(dict(mode='PLAN_ONLY',commit=False,push=False,plan=str(PLAN))))
    elif not a.approval or not a.preflight:raise SystemExit('Pinned operator source linkage and current deploy preflight required')
    else:
        try:print(json.dumps(run('commit' if a.commit else 'push',a.approval,a.preflight)))
        except Exception as e:raise SystemExit(type(e).__name__+': operation did not complete; reconcile saved intent before any repetition')
