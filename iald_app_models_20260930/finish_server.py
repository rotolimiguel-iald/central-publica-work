from pathlib import Path
from datetime import datetime
import ast, hashlib, json, os

root = Path(r'C:\IALD\projetos_pyhton\IALD')
work = Path(__file__).parent
stamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
live = root/'iald_web_server.py'
stage = work/'stage/iald_web_server.py'
old = stage.read_bytes()
assert live.read_bytes() == old, 'Concurrent server changes: stop'
needle = b"        client = req_json.get('messages')\r\n"
if needle not in old: needle = needle.replace(b'\r\n', b'\n')
assert old.count(needle) == 1
new = old.replace(needle, needle + b"        if not isinstance(client, list) or any(not isinstance(m, dict) for m in client):\n            raise ValueError('Invalid message list')\n")
ast.parse(new.decode('utf-8'))
for path in (stage, live):
    assert path.read_bytes() == old
    backup = Path(str(path)+'.bak_'+stamp)
    backup.write_bytes(old)
    tmp = Path(str(path)+'.tmp_'+stamp)
    tmp.write_bytes(new)
    assert tmp.read_bytes() == new and backup.read_bytes() == old
    os.replace(tmp, path)
print(json.dumps({'server_sha256':hashlib.sha256(new).hexdigest(),'backup':str(live)+'.bak_'+stamp}))
