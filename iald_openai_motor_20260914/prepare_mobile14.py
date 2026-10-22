from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

ROOT = Path(r'C:\IALD\projetos_pyhton\IALD\iald-app')
WORK = Path(__file__).parent
stamp = datetime.now().strftime('%Y%m%d_%H%M%S')

def replace(path, old_text, new_text):
    old = path.read_bytes()
    updated = old.replace(old_text, new_text)
    if old == updated:
        raise RuntimeError('Expected release version not found: ' + path.name)
    backup = path.with_name(path.name + '.bak_' + stamp)
    backup.write_bytes(old)
    assert backup.read_bytes() == old
    fd, temporary_name = tempfile.mkstemp(prefix='.' + path.name + '.', dir=path.parent)
    os.close(fd)
    temporary = Path(temporary_name)
    temporary.write_bytes(updated)
    assert temporary.read_bytes() == updated
    if path.read_bytes() != old:
        raise RuntimeError('Concurrent source edit')
    os.replace(temporary, path)

replace(ROOT / 'android/app/build.gradle', b'versionCode 13', b'versionCode 14')
replace(ROOT / 'ios/App/App.xcodeproj/project.pbxproj', b'CURRENT_PROJECT_VERSION = 11;', b'CURRENT_PROJECT_VERSION = 14;')
print('RELEASE_VERSIONS=4.1 (14)')
