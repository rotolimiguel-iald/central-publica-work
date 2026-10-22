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
baseline = json.loads((WORK.parent / 'iald_hypotheses_20260915/suite_gate.json').read_bytes())
assert '9 SUITE(S) COM FALHA' in text
assert rows == baseline['results'], 'Regression results changed'
report = {'at': datetime.now().astimezone().isoformat(), 'passed': True, 'suites': len(rows),
          'old_failures': 9, 'new_failures': 0, 'results': rows, 'log_sha256': hashlib.sha256(data).hexdigest()}
with (WORK / 'suite_gate.json').open('x', encoding='utf-8') as handle: json.dump(report, handle, indent=2)
print('Regression passed: 24 green / same 9 old red / no new failures.')
