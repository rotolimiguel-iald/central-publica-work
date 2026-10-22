"""Create an isolated, unsigned compilation workspace from tracked mobile files."""
from pathlib import Path
import hashlib,json,subprocess
W=Path(__file__).parent
ROOT=Path(r'C:\IALD\projetos_pyhton\IALD\iald-app')
OUT=W/'mobile-review'
assert not OUT.exists(),'Do not replace another build workspace'
files=subprocess.check_output(['git','-c','safe.directory='+str(ROOT),'-C',str(ROOT),'ls-files','-z']).decode().split('\0')
for name in filter(None,files):
    p=ROOT/name
    if not p.is_file():raise RuntimeError('Tracked file missing: '+name)
    if p.name in ('.env','keystore.properties') or p.suffix in ('.p8','.p12','.jks','.keystore'):
        raise RuntimeError('Credential unexpectedly tracked')
    q=OUT/name;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(p.read_bytes())
manifest=json.loads((W/'notifications'/'patch-manifest.json').read_bytes())
for row in manifest['files']:
    # Prepared sources only. This does not enable any capability in a cloud account.
    p=ROOT/row['path'];q=OUT/row['path'];raw=(W/'notifications'/'proposed'/row['path']).read_bytes()
    assert hashlib.sha256(raw).hexdigest()==row['proposed_sha256']
    assert (hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else None)==row['source_sha256']
    q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(raw)
(OUT/'package-lock.json').write_bytes((W/'native-dependencies'/'package-lock.json').read_bytes())
print(json.dumps({'workspace':str(OUT),'signed':False,'production_changed':False}))
