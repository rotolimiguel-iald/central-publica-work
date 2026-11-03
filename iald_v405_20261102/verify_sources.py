"""Verify custody and sealed scientific bytes without running any scientific code.

Release-parametrized (app/RELEASE.json). NOTE: the git step uses `git ls-remote origin` (network, read-only,
free) to confirm that the pinned commit is the published one. Run only in phase B.
`--offline` skips it (no network): remote_main stays null and release_ready null; the push is then a [DECLARADO] fact.
"""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,subprocess,sys
import release_cfg
cfg=release_cfg.load(require_commit=True)
import task
W=Path(__file__).resolve().parent;V=cfg.vault;N=release_cfg.NOS;P=release_cfg.REPO
digest=lambda b:hashlib.sha256(b).hexdigest()
def main():
    task.check('sources',actor=cfg.builder)
    raw=(V/'CUSTODY_MANIFEST.json').read_bytes();m=json.loads(raw)
    assert m['version']==m['um_version_no_selo']==cfg.release and not m['mismatches']
    artifacts=[]
    for entry in m['artifacts']:
        p=(V/entry['file']).resolve();assert p.is_relative_to(V.resolve())
        blob=p.read_bytes();assert digest(blob)==entry['sha256'],entry['file']
        artifacts.append({'file':entry['file'],'bytes':len(blob),'sha256':digest(blob)})
    seal=json.loads((V/'um_absoluto_selo.json').read_bytes());proof=json.loads((V/'tgl_kernel_proof_manifest.json').read_bytes())
    assert seal['um_version']==cfg.release and seal['fail_closed_selftest']=='FAIL_CLOSED_SELFTEST_PASSED'
    assert seal['formal_source_hash']==proof['formal_source_hash']==m['formal_source_hash']
    for name in ['um.py','um_absoluto.json','tgl_kernel_proof_manifest.json','um_absoluto_forma_canonica.md']:
        blob=(V/name).read_bytes();assert digest(blob)==seal['sha256'][name]
        # The live Nos may already have moved to a newer release; compare only while it is still this one.
        live=json.loads((N/'um_absoluto_selo.json').read_bytes())['um_version']
        if live==cfg.release:assert (N/name).read_bytes()==blob,'Canonical source differs: '+name
    assert digest((V/'um.py').read_bytes())==m['um_py_pin']==cfg.um_py_sha256
    command=['git','-C',str(P)]
    head=subprocess.check_output(command+['rev-parse','HEAD']).decode().strip()
    OFFLINE='--offline' in sys.argv
    remote=None if OFFLINE else subprocess.check_output(command+['ls-remote','origin','refs/heads/main']).decode().split()[0]
    pinned=cfg.espelho_commit
    assert subprocess.call(command+['merge-base','--is-ancestor',pinned,head])==0,'Pinned commit is not in the local history'
    # Derive the path from the tracked inventory AT THE PINNED COMMIT, not a guessed article folder name.
    tracked=subprocess.check_output(command+['ls-tree','-r','--name-only','-z',pinned]).decode().split('\0')
    paths=[p for p in tracked if Path(p).name=='um_absoluto_selo.json']
    candidates=[(p,subprocess.check_output(command+['show',pinned+':'+p])) for p in paths]
    paths=[p for p,b in candidates if b==(V/'um_absoluto_selo.json').read_bytes()];assert len(paths)==1,paths
    public=json.loads(subprocess.check_output(command+['show',pinned+':'+paths[0]]))
    out={'status':'CUSTODY_AND_SEAL_VERIFIED','checked_at':datetime.now(timezone.utc).isoformat(),
       'release':cfg.release,'custody_manifest':{'path':str(V/'CUSTODY_MANIFEST.json'),'sha256':digest(raw)},
       'artifacts':artifacts,'artifact_count':len(artifacts),'source_sha256':m['um_py_pin'],
       'seal_timestamp':seal.get('timestamp'),'formal_source_hash':m['formal_source_hash'],
       'kernel_counts_declared_in_custody':m['kernel'],'custody_statistics_scope':'Documentary verification; no Lean/program execution.',
       'published':{'pinned_commit':pinned,'local_head':head,'remote_main':remote,'release':public['um_version'],
                    'remote_checked':not OFFLINE,'pinned_is_local_head':head==pinned,
                    'release_ready':None if OFFLINE else (head==remote and public['um_version']==cfg.release)},
       'science_executed':False,'gate_modified':False}
    task.new('sources_verified.json',out)
    print(json.dumps({k:out[k] for k in ['status','release','artifact_count','source_sha256','published']}))
if __name__=='__main__':main()
