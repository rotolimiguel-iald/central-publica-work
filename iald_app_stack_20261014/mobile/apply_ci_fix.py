from pathlib import Path
import json,hashlib,subprocess,sys
W=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(W))
from transaction import atomic,write_evidence,digest
R=Path('C:/IALD/projetos_pyhton/IALD/iald-app')
def git(*args):
    return subprocess.run(['git','-C',str(R),*args],check=True,capture_output=True,text=True).stdout.strip()
p=json.loads((W/'mobile/ci_fix_plan.json').read_bytes());dest=Path(p['destination']);src=Path(p['source'])
assert git('branch','--show-current')=='codex/mobile-release'
assert not git('status','--porcelain'), 'Concurrent changes: stop'
remote=git('remote','get-url','origin')
assert remote.rstrip('/').removesuffix('.git').endswith('github.com/rotolimiguel-iald/iald-app'), 'Unexpected destination'
assert digest(dest.read_bytes())==p['baseline_sha256'] and digest(src.read_bytes())==p['sha256']
atomic(W/'mobile/ci_post_clone.original.sh',dest.read_bytes())
atomic(dest,src.read_bytes())
relative=dest.relative_to(R).as_posix()
assert git('diff','--name-only')==relative
git('diff','--check')
git('add','--',relative)
assert git('diff','--cached','--name-only')==relative
git('commit','-m','Pin verified Node distribution for Xcode Cloud dependency setup')
commit=git('rev-parse','HEAD')
write_evidence(W/'mobile/ci_commit.json',dict(commit=commit,branch='codex/mobile-release',files=[relative],sha256=p['sha256'],pushed=False))
print(json.dumps(dict(commit=commit,changed=relative)))
