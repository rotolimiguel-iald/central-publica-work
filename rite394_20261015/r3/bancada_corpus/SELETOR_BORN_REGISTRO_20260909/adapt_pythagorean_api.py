from pathlib import Path
from datetime import datetime
import os
p=Path(__file__).resolve().parent/'CanonicalSelectorBorn.lean'
old=p.read_bytes()
a=b'rw [scalarPreparation,norm_add_sq_eq_norm_sq_add_norm_sq_of_inner_eq_zero _ _ ho]'
b=b'rw [scalarPreparation,pow_two,norm_add_sq_eq_norm_sq_add_norm_sq_of_inner_eq_zero _ _ ho]'
assert old.count(a)==1
new=old.replace(a,b).replace(b'simp only [norm_smul,inscription_norm,mul_one,Complex.norm_real,Real.norm_eq_abs,',b'simp only ['+b'\xe2\x86\x90'+b' pow_two,norm_smul,inscription_norm,mul_one,Complex.norm_real,Real.norm_eq_abs,')
backup=p.with_name(p.name+'.bak_'+datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
with backup.open('xb') as f:
    f.write(old);f.flush();os.fsync(f.fileno())
assert backup.read_bytes()==old
t=p.with_name(p.name+'.tmp')
with t.open('xb') as f:
    f.write(new);f.flush();os.fsync(f.fileno())
assert t.read_bytes()==new
os.replace(t,p)
assert p.read_bytes()==new
print('Adapted actual multiplication form of Pythagorean API; backup preserved.')
