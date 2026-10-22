from pathlib import Path
from datetime import datetime
import json, os
A=Path(__file__).resolve().parent
def save(name,value):
 p=A/name;assert p.parent==A
 raw=(json.dumps(value,ensure_ascii=False,indent=2)+'\n').encode('utf8')
 if p.exists():p.with_name(p.name+'.bak_'+datetime.now().strftime('%Y%m%d_%H%M%S_%f')).write_bytes(p.read_bytes())
 t=p.with_name(p.name+'.tmp');t.write_bytes(raw);assert t.read_bytes()==raw;os.replace(t,p)
def walk(value,p=''):
 if isinstance(value,dict):
  for k,v in value.items():yield from walk(v,p+'/'+str(k).replace('~','~0').replace('/','~1'))
 elif isinstance(value,list):
  for i,v in enumerate(value):yield from walk(v,p+'/'+str(i))
 else:yield p,value
