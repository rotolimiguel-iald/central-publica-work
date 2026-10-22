from pathlib import Path
from datetime import datetime
import json, os, sys
folder=Path(__file__).resolve().parent
spec=json.loads(Path(sys.argv[1]).read_bytes())
p=folder/spec['file'];assert p.resolve().parent==folder
raw=p.read_bytes();text=raw.decode('utf8')
for change in spec['changes']:
    a,b,count=change
    assert text.count(a)==count,(a,text.count(a))
    text=text.replace(a,b)
stamp=datetime.now().strftime('%Y%m%d_%H%M%S_%f')
bak=p.with_name(p.name+'.bak_'+stamp)
with bak.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
assert bak.read_bytes()==raw
data=text.encode('utf8');tmp=p.with_name(p.name+'.tmp_'+stamp)
with tmp.open('xb') as f:f.write(data);f.flush();os.fsync(f.fileno())
assert tmp.read_bytes()==data and p.read_bytes()==raw and len(data)>0
os.replace(tmp,p);assert p.read_bytes()==data
print('Edited '+p.name+' with verified immediate byte backup.')
