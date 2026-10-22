from pathlib import Path
from datetime import datetime
import os
import tempfile
import hashlib
import json

WORK=Path(__file__).parent
ROOT=Path(r'C:\IALD\projetos_pyhton\IALD')
stamp=datetime.now().strftime('%Y%m%d_%H%M%S')
changes={ROOT/'iald_web_server.py': (
    b"        'app/img/iald_logo_dark_transparent_final.png',",
    b"        'app/img/iald_logo_dark_transparent_final.png',\n        'app/img/betatgl.png', 'app/img/betatgl.ico',"),
    ROOT/'tests/test_app_assets.py': (
    b'    "app/img/iald_logo_dark_transparent_final.png",',
    b'    "app/img/iald_logo_dark_transparent_final.png",\n    "app/img/betatgl.png", "app/img/betatgl.ico",')}
records={}
for path,(before,after) in changes.items():
    old=path.read_bytes()
    assert old.count(before)==1
    data=old.replace(before,after)
    compile(data,str(path),'exec')
    backup=path.with_name(path.name+'.bak_'+stamp)
    backup.write_bytes(old)
    assert backup.read_bytes()==old
    fd,tempname=tempfile.mkstemp(prefix='.'+path.name+'.',dir=path.parent)
    os.close(fd)
    temp=Path(tempname)
    temp.write_bytes(data)
    assert temp.read_bytes()==data and path.read_bytes()==old
    os.replace(temp,path)
    records[str(path)]={'sha256':hashlib.sha256(data).hexdigest(),'backup':str(backup)}
(WORK/'beta_assets_installation.json').write_bytes(json.dumps(records,indent=2).encode())
print('TWO_EXPLICIT_BETA_ASSETS_ADDED_WITH_BACKUPS')
