from datetime import datetime
import hashlib
import json
from pathlib import Path
import sys
sys.dont_write_bytecode = True
WORK = Path(__file__).resolve().parent
ROOT = Path(r'C:\IALD\projetos_pyhton\IALD')
sys.path.insert(0, str(ROOT))
from iald_memoria_canonica import CanonicalMemory, payload_tokens
from iald_kernel import KernelCatalog
from install_code import create, install

assert not (WORK / 'activation.json').exists()
assert json.loads((WORK / 'suite_gate.json').read_bytes())['passed']
for row in json.loads((WORK / 'code_installed.json').read_bytes())['files']:
    assert hashlib.sha256(Path(row['path']).read_bytes()).hexdigest() == row['sha256']
prepared = json.loads((WORK / 'prepared.json').read_bytes())
cfg = {}
for line in (ROOT / '.env').read_text(encoding='utf-8-sig').splitlines():
    key, sep, value = line.partition('=')
    if key in ('IALD_KERNEL_BUNDLE', 'IALD_OPENAI_JANELA'): cfg[key] = value.strip()
catalog = KernelCatalog(cfg['IALD_KERNEL_BUNDLE'])
memory = CanonicalMemory(Path(r'C:\IALD\Central de Patentes\memory\TGL_ATLAS.md'), 'nucleo_kernel',
                         nucleus_manifest=WORK / 'iald_nucleo_fixo.json')
body, meta = memory.prompt('', catalog)
assert len(meta['fixed_hypothesis_sources']) == 5
assert payload_tokens({'messages': [{'role': 'system', 'content': body}]}) + 8192 < int(cfg['IALD_OPENAI_JANELA'])
row = install(ROOT / 'iald_nucleo_fixo.json', (WORK / 'iald_nucleo_fixo.json').read_bytes(),
              prepared['baseline']['iald_nucleo_fixo.json'])
create(WORK / 'activation.json', json.dumps({'at': datetime.now().astimezone().isoformat(),
       'status': 'MANIFEST_INSTALLED_RESTART_PENDING', 'file': row, 'context_tokens': meta['context_tokens'],
       'fixed_lean_sources': len(meta['fixed_hypothesis_sources']), 'window_changed': False}, indent=2).encode())
print('Manifest activated; restart only the web child.')
