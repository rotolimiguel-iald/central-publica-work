from pathlib import Path
from datetime import datetime
import os
import subprocess
import sys

root = Path(r'C:\IALD\Central de Patentes\Chatgpt').resolve()
out = Path(__file__).resolve().parent
assert out.is_relative_to(root)
source = (root / 'REEXAME_SUFICIENCIA_069_20260909/capture_current069.py').read_text(encoding='utf-8')
source = source.replace('REEXAME_SUFICIENCIA_068_20260909/ESTADO_CANONICO_068.json', 'REEXAME_SUFICIENCIA_069_20260909/ESTADO_CANONICO_069.json')
source = source.replace('comparison_with_delivery068', 'comparison_with_delivery069')
source = source.replace("'ESTADO_CANONICO_069.json'", "'ESTADO_CANONICO_070.json'")
data = source.encode('utf-8')
target = out / 'capture_current070.py'
assert not target.exists()
temporary = target.with_name(target.name + '.tmp_' + datetime.now().strftime('%H%M%S_%f'))
with temporary.open('xb') as stream:
    stream.write(data)
    stream.flush()
    os.fsync(stream.fileno())
assert temporary.read_bytes() == data
temporary.rename(target)
assert target.read_bytes() == data
subprocess.run([sys.executable, '-B', str(target)], check=True)
