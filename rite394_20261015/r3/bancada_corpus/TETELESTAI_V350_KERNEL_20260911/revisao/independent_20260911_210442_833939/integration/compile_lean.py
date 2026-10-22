"""Compile only a local Lean source; retain every attempt and its exact input hash."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

root = Path(__file__).resolve().parent
env_data = json.loads((root / 'environment.json').read_bytes())
relative = Path(sys.argv[1])
source = (root / 'kernel' / relative).resolve()
assert source.is_relative_to(root / 'kernel') and source.suffix == '.lean'
output = root / 'build' / relative.with_suffix('.olean')
output.parent.mkdir(parents=True, exist_ok=True)
logs = root / 'logs'
logs.mkdir(exist_ok=True)
stamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
prefix = logs / (source.stem + '_' + stamp)
raw = source.read_bytes()
env = os.environ.copy()
env['LEAN_PATH'] = os.pathsep.join(env_data['lean_path'])
command = [env_data['lean'], '-o', str(output), str(source)]
result = subprocess.run(command, cwd=root / 'kernel', env=env, capture_output=True)
prefix.with_suffix('.stdout.txt').write_bytes(result.stdout)
prefix.with_suffix('.stderr.txt').write_bytes(result.stderr)
record = {'source': str(source), 'sha256': hashlib.sha256(raw).hexdigest(),
          'returncode': result.returncode, 'command': command,
          'output_exists': output.exists(), 'timestamp': stamp,
          'output_sha256': hashlib.sha256(output.read_bytes()).hexdigest()
            if result.returncode == 0 and output.is_file() else None,
          'stdout': str(prefix.with_suffix('.stdout.txt')),
          'stderr': str(prefix.with_suffix('.stderr.txt'))}
prefix.with_suffix('.json').write_text(json.dumps(record, indent=2), encoding='utf-8')
print(result.stdout.decode('utf-8', errors='replace'))
print(result.stderr.decode('utf-8', errors='replace'))
print(json.dumps(record))
sys.exit(result.returncode)
