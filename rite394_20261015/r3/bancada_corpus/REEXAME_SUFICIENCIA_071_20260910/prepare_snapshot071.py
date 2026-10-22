from pathlib import Path
from datetime import datetime
import os

root = Path(r'C:\IALD\Central de Patentes\Chatgpt').resolve()
out = Path(__file__).resolve().parent
assert out.is_relative_to(root)
source = (root / 'REEXAME_SUFICIENCIA_070_20260909/capture_current070.py').read_text(encoding='utf-8')
source = source.replace('REEXAME_SUFICIENCIA_069_20260909/ESTADO_CANONICO_069.json',
                        'REEXAME_SUFICIENCIA_070_20260909/ESTADO_CANONICO_070.json')
source = source.replace('comparison_with_delivery069', 'comparison_with_delivery070')
source = source.replace('ESTADO_CANONICO_070.json', 'ESTADO_CANONICO_071.json')
# Restore the prior snapshot path after the output-name replacement.
source = source.replace('REEXAME_SUFICIENCIA_070_20260909/ESTADO_CANONICO_071.json',
                        'REEXAME_SUFICIENCIA_070_20260909/ESTADO_CANONICO_070.json')
path = out / 'capture_current071.py'
assert not path.exists()
raw = source.encode('utf-8')
compile(raw, str(path), 'exec')
temp = path.with_name(path.name + '.tmp_' + datetime.now().strftime('%H%M%S_%f'))
with temp.open('xb') as stream:
    stream.write(raw)
    stream.flush()
    os.fsync(stream.fileno())
assert temp.read_bytes() == raw
temp.rename(path)
assert path.read_bytes() == raw
print({'status': 'NEW_READ_ONLY_CAPTURE_PREPARED', 'path': str(path)})
