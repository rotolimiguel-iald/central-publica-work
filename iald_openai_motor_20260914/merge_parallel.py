from pathlib import Path
from datetime import datetime
import hashlib
import json
import os
import subprocess

root = Path(__file__).parent
stamp = datetime.now().strftime('%Y%m%d_%H%M%S')
for name in ('iald_motores.py', 'iald_web_server.py', 'tests/test_motores.py'):
    current = root / 'stage' / name
    backup = current.with_name(current.name + '.premerge_' + stamp)
    backup.write_bytes(current.read_bytes())
    result = subprocess.run(['git', 'merge-file', '-p', str(current), str(root / 'baseline' / name),
                             str(root / 'incoming' / name)], capture_output=True)
    if result.returncode < 0 or result.returncode > 127:
        raise RuntimeError('merge-file failed')
    temp = current.with_name(current.name + '.merging')
    temp.write_bytes(result.stdout)
    os.replace(temp, current)
    print(name + ': conflicts=' + str(result.returncode))
# Freeze the exact incoming versions; installation still compares all hashes.
record = {name: {'bytes': len((root/'incoming'/name).read_bytes()),
                'sha256': hashlib.sha256((root/'incoming'/name).read_bytes()).hexdigest()}
          for name in json.loads((root/'source_manifest.json').read_bytes())}
(root/'incoming_manifest.json').write_bytes(json.dumps(record, indent=2).encode())
