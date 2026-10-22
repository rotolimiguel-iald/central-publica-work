from datetime import datetime
from pathlib import Path
import hashlib
import json
import os
import re
import subprocess
import sys

root = Path(__file__).parent
source = Path('C:/IALD/projetos_pyhton/IALD')
base = root / sys.argv[1] if len(sys.argv) > 1 else root/'incoming'
previous_path = base/'manifest.json' if (base/'manifest.json').exists() else root/'incoming_manifest.json'
previous = json.loads(previous_path.read_bytes())
incoming = root / ('incoming_' + datetime.now().strftime('%Y%m%d_%H%M%S'))
incoming.mkdir()
manifest = {}
for name in previous:
    data = (source/name).read_bytes()
    path = incoming/name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    manifest[name] = {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}
    if manifest[name]['sha256'] != previous[name]['sha256']:
        staged = root/'stage'/name
        backup = staged.with_name(staged.name + '.before_second_merge_' + incoming.name)
        backup.write_bytes(staged.read_bytes())
        result = subprocess.run(['git','merge-file','-p',str(staged),str(base/name),str(path)], capture_output=True)
        if result.returncode > 127 or result.returncode < 0:
            raise RuntimeError('merge failed')
        temporary = staged.with_suffix(staged.suffix+'.merging')
        temporary.write_bytes(result.stdout)
        os.replace(temporary, staged)
        print(name + ': conflicts=' + str(result.returncode))
(incoming/'manifest.json').write_bytes(json.dumps(manifest,indent=2).encode())
print('INCOMING=' + str(incoming))
