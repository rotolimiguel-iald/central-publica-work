"""One-shot six-file private commit and non-force push; no automatic recovery."""
import argparse
import subprocess
from publication_guards import HERE,REPO,D,FILES,checked,intent,pin,read,report,require,sha,scan

BRANCH='refs/heads/codex/mobile-release'
URLS={'https://github.com/rotolimiguel-iald/iald-app.git','git@github.com:rotolimiguel-iald/iald-app.git'}

def git(*args):
    result=subprocess.run(['git','-C',str(REPO),*args],capture_output=True)
    require(result.returncode==0,'Git failed; inspect state safely, do not repeat an intent')
    return result.stdout

def head():return git('rev-parse','HEAD').decode().strip()

def names(*args):return set(git(*args,'-z').decode().strip('\0').split('\0'))-{''}

def remote():
    for flags in ([],['--push']):
        urls=git('remote','get-url','--all',*flags,'origin').decode().splitlines()
        require(len(urls)==1 and urls[0] in URLS,'Unexpected fetch/push destination')
    # Query the validated effective fetch URL; push URL is independently checked.
    rows=git('ls-remote','--exit-code','--heads','origin',BRANCH).decode().split()
    require(len(rows)==2 and rows[1]==BRANCH,'Unexpected remote ref')
    return rows[0]

def branch():
    require(git('symbolic-ref','HEAD').decode().strip()==BRANCH,'Branch drift')

def pins(plan):
    rows={r['target']:r for r in plan['rows']}
    result={}
    for name in sorted(FILES):
        path=REPO/name
        require(path.resolve(strict=True)==path,'Redirected tracked file')
        raw=path.read_bytes();scan(raw)
        require(sha(raw)==rows[str(path)]['new'],'Working bytes not reviewed')
        require(git('ls-files','--stage','--',name).startswith(b'100644 '),'Unexpected tracked mode')
        result[name]=sha(raw)
    return result

def commit():
    plan,audit,authorization=checked('commit');branch()
    base=plan['baseline']['base_commit']
    require(head()==base and remote()==base,'Local/remote baseline drift')
    require(not names('diff','--cached','--name-only'),'Index must be empty')
    require(names('diff','HEAD','--name-only')==FILES,'Unexpected tracked diff')
    values=pins(plan)
    intent('COMMIT',dict(base=base,pins=values,plan=pin(HERE/'PLAN.json'),audit=pin(D/'AUDIT.json')))
    for name,digest in values.items():
        oid=git('hash-object','-w','--no-filters','--',name).decode().strip()
        require(sha(git('cat-file','blob',oid))==digest,'Blob drift')
        git('update-index','--cacheinfo','100644',oid,name)
    require(names('diff','--cached','--name-only')==FILES,'Index contaminated')
    for name,digest in values.items():
        require(sha(git('show',':'+name))==digest,'Staged bytes drift')
    require(head()==base and remote()==base,'Baseline changed before commit')
    git('commit','-m','Fix user-controlled chat scrolling; iOS 47 Android 42')
    tip=head()
    require(git('rev-parse','HEAD^').decode().strip()==base and names('diff','--name-only',base,tip)==FILES,'Unexpected commit delta')
    require(all(sha(git('show',tip+':'+n))==h for n,h in values.items()),'Commit bytes drift')
    require(not names('diff','--cached','--name-only'),'Index not empty after commit')
    report(D/'COMMIT.json',dict(status='COMMITTED_VERIFIED',base=base,commit=tip,pins=values))

def push():
    plan,audit,authorization=checked('push');branch()
    c=read(D/'COMMIT.json');tip=c['commit'];base=plan['baseline']['base_commit']
    require(c['status']=='COMMITTED_VERIFIED' and c['base']==base and set(c['pins'])==FILES,'Commit receipt mismatch')
    require(head()==tip and git('rev-parse',tip+'^').decode().strip()==base,'Unexpected commit ancestry')
    require(not names('diff','--cached','--name-only') and not names('diff','HEAD','--name-only'),'Index/worktree changed')
    require(pins(plan)==c['pins'] and names('diff','--name-only',base,tip)==FILES,'Commit pins mismatch')
    require(all(sha(git('show',tip+':'+n))==h for n,h in c['pins'].items()),'Committed blob drift')
    require(remote()==base,'Remote changed or already pushed; reconcile without repeat')
    intent('PUSH',dict(base=base,commit=tip,branch=BRANCH,receipt=pin(D/'COMMIT.json')))
    git('push','--porcelain','--no-follow-tags','origin',tip+':'+BRANCH)
    require(remote()==tip,'Remote verification failed; preserve uncertain intent')
    report(D/'PUSH.json',dict(status='PUSHED_VERIFIED',commit=tip,branch=BRANCH,ios=47,
        cloud='NOT_OBSERVED',groups='NOT_OBSERVED'))

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('phase',choices=['commit','push'])
    args=parser.parse_args()
    {'commit':commit,'push':push}[args.phase]()
