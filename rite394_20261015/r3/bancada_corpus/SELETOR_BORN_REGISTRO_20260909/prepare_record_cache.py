from pathlib import Path
import json,os
p=Path(__file__).resolve().parent
c=json.loads((p/'CONFIG_BUILD.json').read_text())
c['cached']={'CanonicalSelectorBorn':{'source':(p/'CanonicalSelectorBorn.lean').as_posix(),
    'build':(p/'BUILD_20260909_172830_186727').as_posix()}}
data=(json.dumps(c,indent=2)+'\n').encode()
target=p/'CONFIG_RECORD.json'
assert not target.exists()
tmp=target.with_name(target.name+'.tmp')
with tmp.open('xb') as f:
    f.write(data);f.flush();os.fsync(f.fileno())
assert tmp.read_bytes()==data
os.rename(tmp,target)
print(target)
