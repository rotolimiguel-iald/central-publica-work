from datetime import datetime
import hashlib
import json
from pathlib import Path
WORK = Path(__file__).resolve().parent
ROOT = Path(r'C:\IALD\projetos_pyhton\IALD')
APP = (ROOT/'iald-app').resolve()
stamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
receipt=WORK/'mobile_preparation.json'
assert not receipt.exists()
dest_root=APP/('_backups_packaging_'+stamp)
rows=[]
for name in ['www','ios/App/App/public','android/app/src/main/assets/public']:
    source_root=(APP/name).resolve()
    assert source_root.is_relative_to(APP)
    for path in source_root.rglob('*.bak_*'):
        source=path.resolve()
        assert source.is_file() and source.is_relative_to(source_root)
        destination=(dest_root/source.relative_to(APP)).resolve()
        assert destination.is_relative_to(dest_root.resolve()) and not destination.exists()
        before=source.read_bytes()
        destination.parent.mkdir(parents=True,exist_ok=True)
        source.rename(destination)
        assert destination.read_bytes()==before and not source.exists()
        rows.append({'from':str(source),'to':str(destination),'sha256':hashlib.sha256(before).hexdigest()})
for asset in ['iald.js','iald.css','index.html']:
    data=(ROOT/'app'/asset).read_bytes()
    for name in ['www','ios/App/App/public','android/app/src/main/assets/public']:
        assert (APP/name/asset).read_bytes()==data,name+'/'+asset
assert b'versionCode 16' in (APP/'android/app/build.gradle').read_bytes()
assert (APP/'ios/App/App.xcodeproj/project.pbxproj').read_bytes().count(b'CURRENT_PROJECT_VERSION = 16;')==2
with receipt.open('xb') as f:f.write(json.dumps({'at':datetime.now().astimezone().isoformat(),'build':16,'backups_relocated':rows,'asset_copies_identical':True},indent=2).encode())
print('Build 16 sources synchronized; preserved',len(rows),'backups outside packaged assets.')
