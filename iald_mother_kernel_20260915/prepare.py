from datetime import datetime
import hashlib
import json
from pathlib import Path
import sys
sys.dont_write_bytecode = True
WORK = Path(__file__).resolve().parent
ROOT = Path(r'C:\IALD\projetos_pyhton\IALD')


def create(path, data):
    with path.open('xb') as handle: handle.write(data)
    assert path.read_bytes() == data


sources = {}
for version in ['v4', 'v5', 'v13']:
    path = ROOT / ('IALD_Kernel_' + version + '.txt')
    raw = path.read_bytes()
    sources[version] = {'path': str(path), 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}
manifest = json.loads((ROOT / 'iald_nucleo_fixo.json').read_bytes())
assert 'mother_instruction' not in manifest
manifest['mother_instruction'] = {key: sources['v5'][key] for key in ['path', 'sha256']}
manifest['mother_instruction']['version'] = 'v5'
create(WORK / 'iald_nucleo_fixo.json', json.dumps(manifest, ensure_ascii=False, indent=2).encode())
code = (ROOT / 'iald_memoria_canonica.py').read_text(encoding='utf-8')
anchor = 'from iald_estado_publicado import published_evidence, PublishedEvidenceError\n'
assert code.count(anchor) == 1
code = code.replace(anchor, anchor + 'from iald_instrucao_mae import mother_instruction, MOTHER_REMINDER\n', 1)
anchor = '        metadata.update(nucleus_metadata)\n'
assert code.count(anchor) == 1
addition = '''        mother, mother_metadata = '', {}
        if self.nucleus_manifest is not None:
            try:
                mother_config = json.loads(self.nucleus_manifest.read_bytes()).get('mother_instruction')
                mother, mother_metadata = mother_instruction(mother_config)
            except (OSError, ValueError, KeyError, TypeError) as error:
                raise MemoryUnavailable('Instrução-mãe indisponível: ' + str(error)) from error
        metadata.update(mother_metadata)
'''
code = code.replace(anchor, anchor + addition, 1)
anchor = '            + CANONICAL_IDENTITY + "\\n\\n" + FRAMEWORK_PROTOCOL\n'
assert code.count(anchor) == 1
code = code.replace(anchor, '            + mother + "\\n" + CANONICAL_IDENTITY + "\\n\\n" + FRAMEWORK_PROTOCOL\n', 1)
anchor = '        metadata["context_tokens"] = count_tokens(prefix)\n'
assert code.count(anchor) == 1
code = code.replace(anchor, '        if mother:\n            prefix += MOTHER_REMINDER\n' + anchor, 1)
compile(code, 'iald_memoria_canonica.py', 'exec')
create(WORK / 'iald_memoria_canonica.py', code.encode())
baseline = {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
            for name in ['iald_nucleo_fixo.json', 'iald_memoria_canonica.py']}
baseline['iald_instrucao_mae.py'] = None
create(WORK / 'prepared.json', json.dumps({'at': datetime.now().astimezone().isoformat(), 'sources': sources,
       'baseline': baseline, 'selected': 'v5', 'originals_modified': False}, indent=2).encode())
print('Prepared full v5 identity instruction plus explicit reconciliation; production and original kernels unchanged.')
