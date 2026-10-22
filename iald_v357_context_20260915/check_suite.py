from datetime import datetime
import hashlib,json,re
from pathlib import Path
WORK=Path(__file__).resolve().parent
data=(WORK/'suite.log').read_bytes()
text=data.decode('utf-16') if data[:2] in (b'\xff\xfe',b'\xfe\xff') else data.decode('utf-8-sig')
rows={}
for m in re.finditer(r'^\s*(XX)?\s*(test_[a-z_]+\.(?:py|mjs))\s+(.+)$',text,re.M):
    fail,name,result=m.groups();rows[name]={'failed':bool(fail),'result':result.strip()}
baseline=json.loads((WORK.parent/'iald_tres_modelos_20260915/suite_gate.json').read_bytes())
assert '9 SUITE(S) COM FALHA' in text
assert rows==baseline['results'],'Regression results changed'
report={'at':datetime.now().astimezone().isoformat(),'passed':True,'suites':len(rows),'old_failures':9,
        'new_failures':0,'results':rows,'log_sha256':hashlib.sha256(data).hexdigest()}
with (WORK/'suite_gate.json').open('x',encoding='utf-8') as f:json.dump(report,f,ensure_ascii=False,indent=2)
print('Regression gate passed: 24 green / same 9 old red / zero new failures.')
