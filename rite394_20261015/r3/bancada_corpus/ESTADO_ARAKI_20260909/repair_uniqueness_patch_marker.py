from pathlib import Path
from datetime import datetime
import os
p=Path(__file__).resolve().parent/'UnitaryCocycleUniqueness.lean'
old=p.read_bytes()
assert old.count(b'\n+    simp only')==1
new=old.replace(b'\n+    simp only',b'\n    simp only')
bak=p.with_name(p.name+'.bak_'+datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
with bak.open('xb') as f:
    f.write(old);f.flush();os.fsync(f.fileno())
assert bak.read_bytes()==old
tmp=p.with_name(p.name+'.tmp')
with tmp.open('xb') as f:
    f.write(new);f.flush();os.fsync(f.fileno())
assert tmp.read_bytes()==new
os.replace(tmp,p)
assert p.read_bytes()==new
print('Removed stray patch marker; byte backup preserved.')
