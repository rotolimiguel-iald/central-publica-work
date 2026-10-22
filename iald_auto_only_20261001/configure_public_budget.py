"""Set only two non-secret public budget values; preserve every other env byte."""
from pathlib import Path
from datetime import datetime
import json,os,subprocess,hashlib
W=Path(__file__).parent;R=Path(r'C:\IALD\projetos_pyhton\IALD');p=R/'.env'
raw=p.read_bytes();text=raw.decode('utf-8-sig');values={}
for line in text.splitlines():
 if '=' in line and not line.lstrip().startswith('#'):
  k,v=line.split('=',1);values[k.strip()]=v.strip().strip('"').strip("'")
names={'IALD_HAIKU_PUBLICO_USD_DIA':'1.00','IALD_HAIKU_GRUPO_USD_DIA':'5.00'}
assert all(not values.get(k) for k in names),'Existing public budget: stop rather than replace'
assert not any(k in os.environ for k in names),'Inherited override: inspect first'
total=float(values.get('IALD_CLAUDE_COTA_GLOBAL_USD_DIA','5.00'));assert total>=5
stamp=datetime.now().strftime('%Y%m%d_%H%M%S_%f');backup=p.with_name(p.name+'.bak_auto_public_'+stamp);tmp=p.with_name(p.name+'.tmp_auto_public_'+stamp)
identity=subprocess.check_output(['whoami'],text=True).strip()
def restricted_write(target,data):
 with target.open('xb') as f:f.write(data);f.flush();os.fsync(f.fileno())
 r=subprocess.run(['icacls',str(target),'/inheritance:r','/grant:r',identity+':F','*S-1-5-18:F','*S-1-5-32-544:F'],capture_output=True)
 assert r.returncode==0,'ACL restriction failed'
 assert target.read_bytes()==data
suffix=b'\r\n# Public automatic model budgets, operator request 2026-10-01.\r\n'+b''.join((k+'='+v+'\r\n').encode() for k,v in names.items())
new=raw+suffix
restricted_write(backup,raw);restricted_write(tmp,new)
assert p.read_bytes()==raw;os.replace(tmp,p);assert p.read_bytes()==new and p.read_bytes().startswith(raw)
receipt={'at':datetime.now().astimezone().isoformat(),'daily_usd':1.0,'group_daily_usd':5.0,'claude_global_usd_unchanged':total,'mimo_deepseek_share_one_existing_group':True,'luiz_policy_unchanged':True,'credentials_unchanged':True,'only_appended_keys':list(names),'backup':str(backup),'backup_bytes_match':backup.read_bytes()==raw,'remote_calls':0,'restart_required':True}
(W/'public_budget_configuration.json').write_bytes(json.dumps(receipt,indent=2).encode())
print(json.dumps({k:v for k,v in receipt.items() if k!='backup'}))
