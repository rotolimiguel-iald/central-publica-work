from pathlib import Path
from datetime import datetime
import os

root = Path(r'C:\IALD\Central de Patentes\Chatgpt').resolve()
out = Path(__file__).resolve().parent
source = root / 'REEXAME_SUFICIENCIA_068_20260909/capture_current068.py'
raw = source.read_bytes()
content = raw.decode('utf-8')
content = content.replace('REEXAME_SUFICIENCIA_067_20260909/ESTADO_CANONICO_067.json', 'REEXAME_SUFICIENCIA_068_20260909/ESTADO_CANONICO_068.json')
content = content.replace('comparison_with_delivery067', 'comparison_with_delivery068')
content = content.replace("'ESTADO_CANONICO_068.json'", "'ESTADO_CANONICO_069.json'")
assert source.read_bytes() == raw
data = content.encode('utf-8')
target = out / 'capture_current069.py'
assert target.is_relative_to(root) and not target.exists() and data
temporary = out / ('snapshot_script.tmp_' + datetime.now().strftime('%H%M%S_%f'))
with temporary.open('xb') as stream:
    stream.write(data)
    stream.flush()
    os.fsync(stream.fileno())
assert temporary.read_bytes() == data
temporary.rename(target)
assert target.read_bytes() == data
print(str(target))
