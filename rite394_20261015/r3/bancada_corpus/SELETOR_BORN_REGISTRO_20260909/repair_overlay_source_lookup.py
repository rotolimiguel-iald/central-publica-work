from pathlib import Path
from datetime import datetime
import os
p=Path(__file__).resolve().parent/'build_selector_bridge.py'
old=p.read_bytes()
s=old.decode('utf-8')
a='root=library;sr=root/(str(relative)+".lean");binary=root/(str(relative)+".olean")'
b='root=library;sr=root/(str(relative)+".lean");binary=root/(str(relative)+".olean")'+chr(10)+'   if not sr.is_file():sr=kernel/(str(relative)+".lean")'
assert s.count(a)==1
new=s.replace(a,b).encode('utf-8')
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
print('Canonical binary overlays read the canonical source when no source was copied; backup preserved.')
