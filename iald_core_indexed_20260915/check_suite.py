from datetime import datetime
import hashlib
import json
from pathlib import Path
import re

WORK = Path(__file__).resolve().parent
raw = (WORK/'suite.log').read_bytes()
text = raw.decode('utf-16') if raw[:2] in (b'\xff\xfe',b'\xfe\xff') else raw.decode('utf-8-sig')
rows = {}
for match in re.finditer(r'^\s*(XX)?\s*(test_[a-z_]+\.(?:py|mjs))\s+(.+)$',text,re.M):
    failed,name,result = match.groups()
    rows[name] = {'failed':bool(failed),'result':result.strip()}
baseline = json.loads((WORK.parent/'iald_hypotheses_20260915/suite_gate.json').read_bytes())['results']
assert len(rows) == len(baseline) == 33,'Suite incomplete'
new = {name:row for name,row in rows.items() if row != baseline[name]}
assert not new,json.dumps(new)
assert '9 SUITE(S) COM FALHA' in text
report = {'at':datetime.now().astimezone().isoformat(),'passed':True,'suites':len(rows),
          'old_failures':9,'new_failures':0,'results':rows,'log_sha256':hashlib.sha256(raw).hexdigest()}
with (WORK/'suite_gate.json').open('x',encoding='utf-8') as handle:
    json.dump(report,handle,ensure_ascii=False,indent=2)
print('33 suites: same 24 green and 9 historical failures, no new regression.')
