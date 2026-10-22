from pathlib import Path
import os,hashlib,json
root=Path(r'C:\IALD\Central de Patentes\Chatgpt')
source=root/'compute_finite_ce077_new.py'
target=root/'compute_finite_ce077_run2.py'
data=source.read_bytes()
changed=data.replace(b"OUT=ROOT/'ALGEBRA_EXTERIOR_CE_077_20260910'",b"OUT=ROOT/'ALGEBRA_EXTERIOR_CE_077_20260910_EXECUCAO_02'")
assert changed!=data and not target.exists()
temp=target.with_suffix('.tmp')
with temp.open('xb') as f:
    f.write(changed);f.flush();os.fsync(f.fileno())
assert temp.read_bytes()==changed
temp.rename(target)
assert target.read_bytes()==changed and source.read_bytes()==data
print(json.dumps({'source_sha256':hashlib.sha256(data).hexdigest(),'runner_sha256':hashlib.sha256(changed).hexdigest(),'only_change':'New empty output destination; arithmetic source unchanged.'}))

