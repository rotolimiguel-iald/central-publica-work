from pathlib import Path
from datetime import datetime
import os
p=Path(__file__).resolve().parent/'FiniteResponseErrorBounds.lean'
raw=p.read_bytes();text=raw.decode('utf8')
for a,b,count in [(' (hG : 0≤G)','',3),('hB hG','hB',2),('field_simp [ht]; ring','field_simp [ht]',2)]:
    assert text.count(a)==count,(a,text.count(a))
    text=text.replace(a,b)
stamp=datetime.now().strftime('%Y%m%d_%H%M%S_%f');bak=p.with_name(p.name+'.bak_'+stamp)
with bak.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
assert bak.read_bytes()==raw
data=text.encode();tmp=p.with_name(p.name+'.tmp_'+stamp)
with tmp.open('xb') as f:f.write(data);f.flush();os.fsync(f.fileno())
assert tmp.read_bytes()==data
os.replace(tmp,p);assert p.read_bytes()==data
print('Removed redundant metric-sign input and already closed tactics; byte backup verified.')
