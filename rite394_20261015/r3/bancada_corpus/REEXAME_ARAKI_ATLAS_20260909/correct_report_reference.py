from pathlib import Path
from datetime import datetime
import os
p=Path(__file__).resolve().parent/'REEXAME_ATUALIZADO.md'
old=p.read_bytes()
src=old.decode('utf-8')
assert src.count('TheNameIsTheCharacterization.lean:74>')==1
assert src.count('[IMPLEMENTAÇÃO]')==1
new=src.replace('TheNameIsTheCharacterization.lean:74>','TheNameIsTheCharacterization.lean:77>').replace('[IMPLEMENTAÇÃO]','[OPEN — implementação]').encode('utf-8')
backup=p.with_name(p.name+'.bak_'+datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
with backup.open('xb') as f:
    f.write(old);f.flush();os.fsync(f.fileno())
assert backup.read_bytes()==old
tmp=p.with_name(p.name+'.tmp')
with tmp.open('xb') as f:
    f.write(new);f.flush();os.fsync(f.fileno())
assert tmp.read_bytes()==new
os.replace(tmp,p)
assert p.read_bytes()==new
print('Verified theorem line 77 and normalized status label; byte backup preserved.')
