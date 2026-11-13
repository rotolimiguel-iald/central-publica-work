"""Fresh-process read-only verification; no provider calls and no science execution."""
import argparse,json,sys
from pathlib import Path

def main():
    p=argparse.ArgumentParser();p.add_argument('--config',required=True);p.add_argument('--candidate',required=True);a=p.parse_args()
    cfg=json.loads(Path(a.config).read_bytes());candidate=Path(a.candidate)
    sys.path.insert(0,cfg['runtime'])
    from iald_science_snapshot import ScienceSnapshot
    from claude_memory_package import load_package
    from claude_profiles import HAIKU,SONNET
    expected=json.loads((candidate/'package/release.json').read_bytes())['identity']
    snap=ScienceSnapshot.capture(cfg['installed_catalog'])
    if any(snap.identity.get(k)!=v for k,v in expected.items()): raise ValueError('Loaded identity mismatch')
    for name,profile in [('haiku55',HAIKU),('sonnet',SONNET)]:
        load_package(snap.package_path(name),science_snapshot=snap,expected_model=profile.model)
    print(json.dumps({'verified':True,'identity':snap.check(),'scope':'fresh_process_bytes_loaders_native_packages; no model call'}))

if __name__=='__main__': main()
