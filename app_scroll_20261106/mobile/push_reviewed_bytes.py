"""Push the reviewed commit after a line-ending-only preflight refusal.

No prior PUSH_INTENT exists: refusal preceded network mutation. Git attributes
normalize *.gradle to LF, while the exact reviewed/installed blob is CRLF.
Compare actual bytes to both plan and commit, keeping all other push guards.
"""
import git_release42 as g
from publication_guards import HERE,D,FILES,checked,intent,pin,read,report,require,sha

def push():
    review=read(HERE.parent/'review/PUSH_BYTES_REVIEW.json')
    require(review['status']=='PASS' and review['script_sha256']==sha((HERE/'push_reviewed_bytes.py').read_bytes()),'Review missing')
    plan,audit,authorization=checked('push');g.branch()
    c=read(D/'COMMIT.json');tip=c['commit'];base=plan['baseline']['base_commit']
    require(c['status']=='COMMITTED_VERIFIED' and c['base']==base and set(c['pins'])==FILES,'Commit receipt mismatch')
    require(g.head()==tip and g.git('rev-parse',tip+'^').decode().strip()==base,'Unexpected ancestry')
    require(not g.names('diff','--cached','--name-only'),'Index changed')
    dirty=g.names('diff','HEAD','--name-only')
    require(dirty=={'android/app/build.gradle'},'Different preflight failure; stop')
    require(not g.names('diff','--ignore-space-at-eol','HEAD','--name-only'),'Non-line-ending diff')
    require(g.pins(plan)==c['pins'] and g.names('diff','--name-only',base,tip)==FILES,'Working/plan/commit pins mismatch')
    require(all(sha(g.git('show',tip+':'+n))==h for n,h in c['pins'].items()),'Committed bytes drift')
    require(g.remote()==base,'Remote changed or already pushed; reconcile')
    intent('PUSH',dict(base=base,commit=tip,branch=g.BRANCH,receipt=pin(D/'COMMIT.json'),
                       review=pin(HERE.parent/'review/PUSH_BYTES_REVIEW.json'),line_ending_only=sorted(dirty)))
    g.git('push','--porcelain','--no-follow-tags','origin',tip+':'+g.BRANCH)
    require(g.remote()==tip,'Remote verification failed; preserve uncertain intent')
    report(D/'PUSH.json',dict(status='PUSHED_VERIFIED',commit=tip,branch=g.BRANCH,ios=47,
                             cloud='NOT_OBSERVED',groups='NOT_OBSERVED',line_ending_preflight_reconciled=True))
if __name__=='__main__':push()
