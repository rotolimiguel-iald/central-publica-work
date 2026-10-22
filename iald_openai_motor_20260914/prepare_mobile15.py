"""Preserve the parallel UI revision and prepare version 15 without reusing receipts."""
from pathlib import Path
from datetime import datetime
import os
import tempfile

WORK = Path(__file__).parent
ROOT = Path(r'C:\IALD\projetos_pyhton\IALD\iald-app')
stamp = datetime.now().strftime('%Y%m%d_%H%M%S')
for name, before, after in [
    ('android/app/build.gradle', b'versionCode 14', b'versionCode 15'),
    ('ios/App/App.xcodeproj/project.pbxproj', b'CURRENT_PROJECT_VERSION = 14;', b'CURRENT_PROJECT_VERSION = 15;')]:
    path = ROOT / name
    old = path.read_bytes()
    data = old.replace(before, after)
    assert old != data
    backup = path.with_name(path.name + '.bak_' + stamp)
    backup.write_bytes(old)
    assert backup.read_bytes() == old
    fd, tempname = tempfile.mkstemp(prefix='.' + path.name + '.', dir=path.parent)
    os.close(fd)
    temporary = Path(tempname)
    temporary.write_bytes(data)
    assert temporary.read_bytes() == data
    assert path.read_bytes() == old, 'Concurrent edit'
    os.replace(temporary, path)

for kind in ['audit', 'publish']:
    src = WORK / (kind + '_mobile14.py')
    dst = WORK / (kind + '_mobile15.py')
    assert not dst.exists()
    data = src.read_bytes().replace(b'mobile14', b'mobile15')
    data = data.replace(b'build 14 with OpenAI consent and refreshed interface',
                        b'build 15 with usage limits, response reports and beta symbol')
    dst.write_bytes(data)
print('BUILD_15_PREPARED_WITH_VERSION_BACKUPS')
