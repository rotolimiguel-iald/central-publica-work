"""Parent convenience: pin explicitly selected final snapshots; never find 'latest'."""
import argparse,json
from pathlib import Path
from prepare_memories import HERE,ROLES,sha,validate,new
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for role in ROLES:p.add_argument('--'+role,required=True)
    p.add_argument('--out',required=True);args=p.parse_args()
    config=dict(final_snapshot=True,receipts={})
    for role in ROLES:
        source=Path(getattr(args,role)).resolve()
        config['receipts'][role]=dict(path=str(source),sha256=sha(source.read_bytes()))
    validate(config) # All roles/schema/pins must verify before writing config.
    new(HERE/args.out,(json.dumps(config,ensure_ascii=False,indent=2)+'\n').encode())
    print('PINNED_FINAL_SNAPSHOTS_NOT_APPLIED')
