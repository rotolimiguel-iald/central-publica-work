from datetime import datetime
import hashlib
import json
from pathlib import Path
WORK=Path(__file__).resolve().parent
ROOT=Path(r'C:\IALD\projetos_pyhton\IALD')
path=ROOT/'iald_web_server.py'
stage=WORK/'stage/iald_web_server.py'
before=path.read_bytes()
assert before==stage.read_bytes()
old='''                yield "data: " + json.dumps({"iald_modelo": modelo}, ensure_ascii=False) + "\\n\\n"
                yield from original'''
new='''                first = True
                for chunk in original:
                    if first:
                        first = False
                        prefix = "data: " + json.dumps({"iald_modelo": modelo}, ensure_ascii=False) + "\\n\\n"
                        # Add provenance to the first existing chunk, never advance the
                        # response lifecycle with an extra yield before upstream starts.
                        yield prefix.encode("utf-8") + chunk if isinstance(chunk, bytes) else prefix + chunk
                    else:
                        yield chunk'''
text=before.decode().replace('\r\n','\n')
assert text.count(old)==1
text=text.replace(old,new)
after=text.replace('\n','\r\n' if b'\r\n' in before else '\n').encode()
compile(after,str(path),'exec')
stamp=datetime.now().strftime('%Y%m%d_%H%M%S_%f')
for target in (path,stage):
    assert target.read_bytes()==before
    backup=target.with_name(target.name+'.bak_'+stamp)
    with backup.open('xb') as f:f.write(before)
    temp=target.with_name(target.name+'.tmp_'+stamp)
    with temp.open('xb') as f:f.write(after)
    assert temp.read_bytes()==after and target.read_bytes()==before
    temp.replace(target)
report={'at':datetime.now().astimezone().isoformat(),'fix':'No extra SSE yield before upstream starts; metadata joins first original chunk',
        'before_sha256':hashlib.sha256(before).hexdigest(),'after_sha256':hashlib.sha256(after).hexdigest(),'restart':False}
with (WORK/'stream_fix.json').open('xb') as f:f.write(json.dumps(report,indent=2).encode())
print('Stream lifecycle fix installed; awaiting tests and restart.')
