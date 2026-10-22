"""Prepare the operator's latest core-and-retrieval architecture, preserving originals."""
from datetime import datetime
import hashlib
import json
from pathlib import Path

PREVIOUS = Path(__file__).resolve().parent
WORK = PREVIOUS.parent / 'iald_core_indexed_20260915'
ROOT = Path(r'C:\IALD\projetos_pyhton\IALD')
SOURCE = Path(r'C:\Users\rotol\Downloads\IALD_TGL_MEMORY_CORE_v1_20260915.md')
WORK.mkdir(exist_ok=True)


def create(name, data):
    path = WORK / name
    with path.open('xb') as handle:
        handle.write(data)
    assert path.read_bytes() == data


raw = SOURCE.read_bytes()
core_name = SOURCE.name
create(core_name, raw)
manifest = json.loads((PREVIOUS / 'iald_nucleo_fixo.json').read_bytes())
manifest['document_mode'] = 'retrievable'
manifest['operational_core'] = {'path': str(ROOT / core_name),
                              'sha256': hashlib.sha256(raw).hexdigest(), 'version': '1.0.0',
                              'current_release': 'v357'}
create('iald_nucleo_fixo.json', json.dumps(manifest, ensure_ascii=False, indent=2).encode())
local = json.loads(json.dumps(manifest))
local['operational_core']['path'] = str(WORK / core_name)
create('manifest_staged.json', json.dumps(local, ensure_ascii=False, indent=2).encode())
for name in ['iald_instrucao_mae.py', 'iald_web_server.py']:
    create(name, (PREVIOUS / name).read_bytes())
memory = (PREVIOUS / 'iald_memoria_canonica.py').read_bytes().decode()
nl = '\r\n' if '\r\n' in memory else '\n'
memory = memory.replace('\r\n', '\n')
old = 'from iald_instrucao_mae import mother_instruction, MOTHER_REMINDER'
assert memory.count(old) == 1
memory = memory.replace(old, old + '\nfrom iald_core_indexado import operational_core, DocumentCorpus')
old = "            entries = config.get('entries', [])"
assert memory.count(old) == 1
memory = memory.replace(old, """            if config.get('document_mode') == 'retrievable':
                return DocumentCorpus(self.nucleus_manifest).context(public=public)
            entries = config.get('entries', [])""")
old = '        metadata.update(mother_metadata)'
assert memory.count(old) == 1
memory = memory.replace(old, """        metadata.update(mother_metadata)
        operational, operational_meta = operational_core(self.nucleus_manifest)
        mother += operational
        metadata.update(operational_meta)""")
old = '        prefix += nucleus'
assert memory.count(old) == 1
memory = memory.replace(old, """        prefix += nucleus
        if metadata.get('document_mode') == 'retrievable':
            prefix += ('\\nPOLÍTICA ATUAL DE LEITURA: as referências anteriores a artigos completos '
                       'carregados significam disponibilidade integral no acervo. Nesta configuração, '
                       'o conteúdo sempre presente é o núcleo operacional, o v5 e as provas nucleares '
                       'identificadas abaixo. Os artigos extensos são consultados com search_tgl e '
                       'fetch_tgl; não diga que leu uma passagem sem recuperá-la. Preserve toda a '
                       'capacidade de consulta, sem resumir ou substituir os arquivos originais.\\n')""")
compile(memory, 'iald_memoria_canonica.py', 'exec')
create('iald_memoria_canonica.py', memory.replace('\n', nl).encode())
baseline = json.loads((PREVIOUS / 'prepared.json').read_bytes())['baseline']
baseline['iald_core_indexado.py'] = None
baseline[core_name] = None
create('prepared.json', json.dumps({'at': datetime.now().astimezone().isoformat(),
    'status': 'STAGED_ONLY', 'baseline': baseline, 'source_file': str(SOURCE),
    'source_sha256': hashlib.sha256(raw).hexdigest(), 'source_bytes': len(raw),
    'source_modified': False, 'current_release_selected_by_operator': 'v357',
    'previous_architecture_superseded': '7 full articles in every prompt; all remain retrievable intact'},
    ensure_ascii=False, indent=2).encode())
print('Indexed-core preparation created; original attachment and kernels unchanged.')
