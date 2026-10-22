"""Append the verified delivery to all seven established memories with byte backups."""
from pathlib import Path
from datetime import datetime
import hashlib,json,os
W=Path(__file__).parent
previous=json.loads((W.parent/'iald_public_models_20260930/jev_activation_delivery.json').read_bytes())
delivery=json.loads((W/'delivery.json').read_bytes())
notes=(W/'delivery_notes.txt').read_text(encoding='utf-8')
tag='IALD_TASK_TOOLS_PILOT_20260930'
stamp=datetime.now().strftime('%Y%m%d_%H%M%S_%f')
records=[]
for row in previous['memory']:
    path=Path(row['path']);before=path.read_bytes()
    assert tag.encode() not in before,'Delivery already recorded'
    backup=path.with_name(path.name+'.bak_'+stamp);backup.write_bytes(before)
    assert backup.read_bytes()==before
    addition=('\r\n\r\n## 30/09/2026 — Ferramentas e etapas automáticas no app IALD\r\n\r\n<!-- '+tag+' -->\r\n\r\n'+notes.replace('\r\n','\n').replace('\n','\r\n')+'\r\n').encode('utf-8')
    after=before+addition;temp=path.with_name(path.name+'.tmp_'+stamp)
    temp.write_bytes(after);assert temp.read_bytes()==after and len(after)>len(before)
    assert path.read_bytes()==before,'Concurrent memory change'
    os.replace(temp,path);assert path.read_bytes()==after
    records.append({'path':str(path),'backup':str(backup),'sha256':hashlib.sha256(after).hexdigest()})
delivery['memory']=records
raw=json.dumps(delivery,ensure_ascii=False,indent=2).encode('utf-8')
temp=W/'delivery.tmp';temp.write_bytes(raw);assert temp.read_bytes()==raw
os.replace(temp,W/'delivery.json')
print(json.dumps({'memories_updated':len(records),'delivery':str(W/'delivery.json')}))
