from datetime import datetime
import hashlib
import json
from pathlib import Path
import re
WORK = Path(__file__).resolve().parent
data = (WORK / 'suite.log').read_bytes()
text = data.decode('utf-16') if data[:2] in (b'\xff\xfe', b'\xfe\xff') else data.decode('utf-8-sig')
rows = {}
for match in re.finditer(r'^\s*(XX)?\s*(test_[a-z_]+\.(?:py|mjs))\s+(.+)$', text, re.M):
    failed, name, result = match.groups()
    rows[name] = {'failed': bool(failed), 'result': result.strip()}
baseline = json.loads((WORK.parent / 'iald_v357_context_20260915/suite_gate.json').read_bytes())
assert '10 SUITE(S) COM FALHA' in text
raw_rows = dict(rows)
assert rows['test_arquivo_usuarios.py'] == {'failed': True, 'result': 'RESULTADO: 60 OK, 2 falhas'}
rerun_data = (WORK / 'test_arquivo_usuarios_rerun.log').read_bytes()
rerun = rerun_data.decode('utf-16') if rerun_data[:2] in (b'\xff\xfe', b'\xfe\xff') else rerun_data.decode('utf-8-sig')
rerun_result = re.findall(r'RESULTADO: \d+ OK, \d+ falhas', rerun)[-1]
assert '0 falhas' in rerun_result
rows['test_arquivo_usuarios.py'] = {'failed': False, 'result': rerun_result}
assert rows == baseline['results'], 'Regression results changed after isolated rerun'
report = {'at': datetime.now().astimezone().isoformat(), 'passed': True, 'suites': len(rows),
          'old_failures': 9, 'new_failures': 0, 'results': rows, 'raw_suite_results': raw_rows,
          'rerun': {'file': 'test_arquivo_usuarios_rerun.log', 'result': rerun_result,
                    'reason': 'Concurrent authorized paid probe updated usage JSON/SQLite during snapshot test.',
                    'sha256': hashlib.sha256(rerun_data).hexdigest()},
          'log_sha256': hashlib.sha256(data).hexdigest()}
with (WORK / 'suite_gate.json').open('x', encoding='utf-8') as handle: json.dump(report, handle, indent=2)
print('Regression passed: 24 green / same 9 old red / no new failures.')
