"""Verify custody and sealed scientific bytes without running any scientific code."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,subprocess
import task
W=Path(__file__).resolve().parent;V=Path(r'C:\IALD\Central de Patentes\vault\originals_copy\um_unificado_v394');N=Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós');P=Path(r'C:\IALD\Artigo\the_boundary')
digest=lambda b:hashlib.sha256(b).hexdigest()
def main():
    task.check('sources')
    raw=(V/'CUSTODY_MANIFEST.json').read_bytes();m=json.loads(raw)
    assert m['version']==m['um_version_no_selo']=='v394' and not m['mismatches']
    artifacts=[]
    for entry in m['artifacts']:
        p=(V/entry['file']).resolve();assert p.is_relative_to(V.resolve())
        blob=p.read_bytes();assert digest(blob)==entry['sha256'],entry['file']
        artifacts.append({'file':entry['file'],'bytes':len(blob),'sha256':digest(blob)})
    seal=json.loads((V/'um_absoluto_selo.json').read_bytes());proof=json.loads((V/'tgl_kernel_proof_manifest.json').read_bytes())
    assert seal['um_version']=='v394' and seal['fail_closed_selftest']=='FAIL_CLOSED_SELFTEST_PASSED'
    assert seal['formal_source_hash']==proof['formal_source_hash']==m['formal_source_hash']
    for name in ['um.py','um_absoluto.json','tgl_kernel_proof_manifest.json','um_absoluto_forma_canonica.md']:
        blob=(V/name).read_bytes();assert digest(blob)==seal['sha256'][name]
        assert (N/name).read_bytes()==blob,'Canonical source differs: '+name
    assert digest((V/'um.py').read_bytes())==m['um_py_pin']
    command=['git','-C',str(P)]
    head=subprocess.check_output(command+['rev-parse','HEAD']).decode().strip()
    remote=subprocess.check_output(command+['ls-remote','origin','refs/heads/main']).decode().split()[0]
    # Derive the path from tracked inventory, not a guessed article folder name.
    tracked=subprocess.check_output(command+['ls-tree','-r','--name-only','-z',head]).decode().split('\0')
    paths=[p for p in tracked if Path(p).name=='um_absoluto_selo.json'];assert len(paths)==1
    public=json.loads(subprocess.check_output(command+['show',head+':'+paths[0]]))
    out={'status':'CUSTODY_AND_SEAL_VERIFIED','checked_at':datetime.now(timezone.utc).isoformat(),
       'release':'v394','custody_manifest':{'path':str(V/'CUSTODY_MANIFEST.json'),'sha256':digest(raw)},
       'artifacts':artifacts,'artifact_count':len(artifacts),'source_sha256':m['um_py_pin'],
       'seal_timestamp':seal.get('timestamp'),'formal_source_hash':m['formal_source_hash'],
       'kernel_counts_declared_in_custody':m['kernel'],'custody_statistics_scope':'Documentary verification; no Lean/program execution.',
       'published':{'local_head':head,'remote_main':remote,'release':public['um_version'],'v394_ready':head==remote and public['um_version']=='v394'},
       'science_executed':False,'gate_modified':False}
    task.new('sources_verified.json',out)
    print(json.dumps({k:out[k] for k in ['status','release','artifact_count','source_sha256','published']}))
if __name__=='__main__':main()
