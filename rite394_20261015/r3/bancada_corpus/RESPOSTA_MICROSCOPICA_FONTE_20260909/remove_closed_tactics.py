"""Remove tactics after field_simp has already closed both goals; keep the failed source."""
from pathlib import Path
from datetime import datetime
import os
path=Path(__file__).resolve().parent/'ProbeResponseRecord.lean'
before=path.read_bytes()
old=b'field_simp [Real.pi_ne_zero] <;> ring'
assert before.count(old)==2
after=before.replace(old,b'field_simp [Real.pi_ne_zero]')
backup=path.with_name(path.name+'.bak_'+datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
with backup.open('xb') as f:f.write(before);f.flush();os.fsync(f.fileno())
assert backup.read_bytes()==before
temp=path.with_name(path.name+'.tmp_clean')
with temp.open('xb') as f:f.write(after);f.flush();os.fsync(f.fileno())
assert temp.read_bytes()==after and path.read_bytes()==before
os.replace(temp,path)
assert path.read_bytes()==after
print('Removed two unused tactics; exact byte backup preserved.')
