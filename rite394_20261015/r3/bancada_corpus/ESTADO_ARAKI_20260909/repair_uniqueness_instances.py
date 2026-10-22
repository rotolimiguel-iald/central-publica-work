from pathlib import Path
from datetime import datetime
import os
p=Path(__file__).resolve().parent/'UnitaryCocycleUniqueness.lean'
old=p.read_bytes()
src=old.decode('utf-8')
a='  simpa only [star_mul, hA t, neg_mul, mul_neg, mul_assoc, add_neg_cancel] using hd'
b='  convert! hd using 1 <;>\n+    simp only [star_mul, hA t, neg_mul, mul_neg, mul_assoc, add_neg_cancel]'
assert src.count(a)==1
new=src.replace(a,b).encode('utf-8')
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
print('Updated instance conversion, preserving byte backup.')
