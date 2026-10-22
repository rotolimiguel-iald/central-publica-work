"""Install a tested immutable release and switch configuration with byte backups."""
from datetime import datetime
import hashlib
import json
from pathlib import Path
import sys
APP=Path(r'C:\IALD\projetos_pyhton\IALD');WORK=Path(__file__).resolve().parent
sys.path[:0]=[str(WORK),str(APP)]
from prepare import save,sha
sys.path.insert(0,str(WORK))
from iald_kernel import KernelCatalog
from iald_memoria_canonica import CanonicalMemory

def main():
    assert not (WORK/'installed.json').exists()
    prep=json.loads((WORK/'prepared.json').read_bytes())
    assert json.loads((WORK/'test_results.json').read_bytes())['passed']
    assert json.loads((WORK/'validation.json').read_bytes())['passed']
    pins=json.loads((WORK/'code_pins.json').read_bytes())
    pins['iald_nucleo_fixo.json']=prep['original_manifest_sha256']
    originals={name:(APP/name).read_bytes() for name in pins}
    assert all(sha(originals[n])==v for n,v in pins.items()),'Concurrent code/config change; stop'
    assert not (APP/'iald_cluster.py').exists()
    destination=APP/'canonical_releases'/('v368_'+prep['commit'][:12])
    for rel,record in prep['files'].items():
        raw=(WORK/'release'/rel).read_bytes();assert sha(raw)==record['sha256']
        save(destination/rel,raw)
    bundle_source=Path(prep['kernel']);bundle_target=destination/'kernel'
    for path in bundle_source.rglob('*'):
        if path.is_file():save(bundle_target/path.relative_to(bundle_source),path.read_bytes())
    cluster=destination/'TGL_CLUSTER_v368.md'
    save(cluster,(WORK/'TGL_CLUSTER_v368.md').read_bytes())
    manifest=json.loads((WORK/'manifest_staged.json').read_bytes())
    for entry in manifest['entries']+[manifest['published_evidence'][k] for k in ('program','seal','result','proof_manifest')]:
        entry['path']=str(destination/Path(entry['path']).relative_to(WORK/'release'))
    cfg=manifest['active_cluster'];cfg['path']=str(cluster);cfg['kernel_bundle']=str(bundle_target)
    proof_path=Path(manifest['published_evidence']['proof_manifest']['path'])
    proof=json.loads(proof_path.read_bytes())
    catalog=KernelCatalog(bundle_target)
    report={'source_sha256':catalog.source_sha,
        'scope':'PUBLISHED_COMPILATION_REPORT_HASH_MATCHED__NOT_RERUN',
        'compiler':proof['formal_checker'],'created_at':proof['timestamp'],
        'dependencies':{'allowed_axioms':['propext','Classical.choice','Quot.sound'],
                        'published_manifest_sha256':sha(proof_path.read_bytes()),'reported_terms':len(proof['axiom_report'])},
        'files':{name:{'file_sha256':record['sha256'],'status':'SOURCE_MATCHES_PUBLISHED_FORMAL_REPORT'}
                 for name,record in catalog.records.items() if name.endswith('.lean') and proof['formal_files_sha256'].get(name)==record['sha256']}}
    verify=destination/'kernel_verification.json';save(verify,json.dumps(report,indent=2).encode())
    cfg['kernel_verification']=str(verify)
    catalog=KernelCatalog(bundle_target,verify);catalog.verification('TGLExt/NameIsTheContent.lean')
    new_manifest=json.dumps(manifest,ensure_ascii=False,indent=2).encode()
    staged=WORK/'manifest_install.json';save(staged,new_manifest)
    for public in (True,False):
        memory=CanonicalMemory(Path(r'C:\IALD\Central de Patentes\memory\TGL_ATLAS.md'),'nucleo_kernel',nucleus_manifest=staged)
        _,meta=memory.prompt('',catalog,public=public)
        assert meta['cluster_always_present'] and meta['published_evidence_checked']
    stamp=datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    payloads={name:(WORK/name).read_bytes() for name in pins if name!='iald_nucleo_fixo.json'}
    payloads['iald_cluster.py']=(WORK/'iald_cluster.py').read_bytes()
    payloads['iald_nucleo_fixo.json']=new_manifest
    backups={}
    for name,raw in originals.items():
        assert (APP/name).read_bytes()==raw
        backup=APP/(name+'.bak_'+stamp);save(backup,raw);backups[name]=str(backup)
    # Modules first, manifest last; supervisor reload is dispatched separately.
    for name,raw in payloads.items():
        path=APP/name
        temp=APP/(name+'.tmp_'+stamp);save(temp,raw)
        if name in originals:assert path.read_bytes()==originals[name]
        temp.replace(path);assert path.read_bytes()==raw
    receipt={'at':datetime.now().astimezone().isoformat(),'release':'v368','commit':prep['commit'],
        'files':{name:sha(raw) for name,raw in payloads.items()},'backups':backups,
        'destination':str(destination),'env_changed':False,'scientific_sources_changed':False,
        'status':'INSTALLED_RESTART_REQUIRED'}
    save(WORK/'installed.json',json.dumps(receipt,indent=2).encode())
    print(json.dumps({'status':receipt['status'],'files':len(payloads),'release':'v368'}))

if __name__=='__main__':main()
