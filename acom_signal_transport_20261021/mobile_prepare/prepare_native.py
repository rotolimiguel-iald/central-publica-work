"""Read-only verifier for the parent's native stage; creates no alternate plan.

Run only explicitly before installation. Current 31/36 -> proposed 32/37.
"""
from pathlib import Path
import hashlib
import json

W=Path(__file__).resolve().parent.parent
R=Path(r'C:\IALD\projetos_pyhton\IALD\iald-app')

def verify():
    plan=json.loads((W/'NATIVE_PLAN.json').read_bytes())
    assert plan['ios']=='4.1(37)' and plan['android']=='4.1(32)'
    expected={
        R/'ios/App/App.xcodeproj/project.pbxproj':(b'CURRENT_PROJECT_VERSION = 36;',b'CURRENT_PROJECT_VERSION = 37;',2),
        R/'android/app/build.gradle':(b'versionCode 31',b'versionCode 32',1),
    }
    assert len(plan['files'])==2
    assert {Path(f['destination']) for f in plan['files']}==set(expected)
    for row in plan['files']:
        target=Path(row['destination']);source=Path(row['source']).resolve(strict=True)
        assert source.is_relative_to(W.resolve())
        raw=target.read_bytes();before,after,count=expected[target]
        assert raw.count(before)==count and hashlib.sha256(raw).hexdigest()==row['baseline']
        assert source.read_bytes()==raw.replace(before,after)
        assert hashlib.sha256(source.read_bytes()).hexdigest()==row['sha256']
    return {'status':'NATIVE_CANDIDATES_VERIFIED_NOT_INSTALLED'}

if __name__=='__main__':
    print(json.dumps(verify()))
