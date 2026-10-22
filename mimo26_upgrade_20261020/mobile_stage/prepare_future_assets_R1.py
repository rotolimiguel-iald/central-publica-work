"""Package an explicitly pinned future asset into this staging directory only.

No install/sync/build/push mode exists. Main reviews the emitted transaction plan.
"""
from pathlib import Path
import argparse, hashlib, json, re

HERE=Path(__file__).resolve().parent
WORK=HERE.parent
def digest(raw):return hashlib.sha256(raw).hexdigest()
def local(path,root):
    original=Path(path).absolute()
    path=original.resolve(strict=True)
    if not path.is_relative_to(root.resolve(strict=True)):raise ValueError('Path outside authorized staging')
    for item in [original,*original.parents,path,*path.parents]:
        if getattr(item.lstat(),'st_file_attributes',0)&0x400:raise ValueError('Reparse point refused')
    return path
def proposed_plan(raw,source,baseline):
    if not raw:raise ValueError('Empty asset')
    return dict(schema='iald.mobile.asset-plan.v1',status='CANDIDATE_NOT_INSTALLED',
        source_sha256=digest(raw),files=[dict(source=str(source),destination=x['path'],
            sha256=digest(raw),baseline=x['sha256']) for x in baseline['assets']],
        build_started=False,published=False,
        limits=['This is an exact four-target asset plan, not permission to deploy.',
                'Native build numbers, archive signing and TestFlight/store distribution are separate steps.'])
def prepare(asset,expected_sha256,name):
    if not re.fullmatch(r'[0-9a-f]{64}',expected_sha256):raise ValueError('Explicit SHA256 required')
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]{0,63}',name):raise ValueError('Invalid unique package name')
    asset=local(asset,WORK)
    if asset.name!='iald.js':raise ValueError('Only reviewed iald.js is supported')
    raw=asset.read_bytes()
    if digest(raw)!=expected_sha256:raise ValueError('Candidate pin mismatch')
    baseline=json.loads((HERE/'MOBILE_BASELINE_R1.json').read_bytes())
    for item in baseline['assets']+baseline['baseline_inputs']:
        if digest(Path(item['path']).read_bytes())!=item['sha256']:raise ValueError('Runtime baseline changed; refresh/review a new baseline')
    folder=HERE/'packages'/name
    folder.parent.mkdir(exist_ok=True)
    local(folder.parent,HERE)
    folder.mkdir(exist_ok=False)
    target=folder/'iald.js'
    with target.open('xb') as f:f.write(raw)
    if target.read_bytes()!=raw:raise OSError('Candidate copy failed')
    plan=proposed_plan(raw,target,baseline)
    plan['baseline_receipt_sha256']=digest((HERE/'MOBILE_BASELINE_R1.json').read_bytes())
    output=folder/'install_plan.json'
    blob=json.dumps(plan,ensure_ascii=False,indent=2).encode()
    with output.open('xb') as f:f.write(blob)
    if output.read_bytes()!=blob:raise OSError('Plan verification failed')
    return dict(plan=str(output),sha256=digest(blob),files=len(plan['files']),build_started=False,published=False)
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--asset',type=Path,required=True)
    p.add_argument('--sha256',required=True)
    p.add_argument('--package',required=True)
    args=p.parse_args()
    print(json.dumps(prepare(args.asset,args.sha256,args.package)))
