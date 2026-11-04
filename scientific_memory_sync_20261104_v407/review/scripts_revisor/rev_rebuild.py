"""Reconstrucao independente do indice a partir do catalogo staged (aponta para as copias do snapshot), em diretorio do SCRATCHPAD (nada em Chatgpt\)."""
import sys, json, time, hashlib
sys.dont_write_bytecode = True
from pathlib import Path
BASE = Path(r'C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923')
sys.path.insert(0, str(BASE))
from iald_orchestrator import canonical_memory as cm
W = Path(r'C:\IALD\Central de Patentes\work\scientific_memory_sync_20261104_v407')
EPOCH = 'v407_4323b401f15cc971'
target = Path(r'C:\Users\rotol\AppData\Local\Temp\claude\b4ca26c934d2167f\fda3adae-8303-4906-a1c4-4eb0c0b6c4e4\scratchpad\rebuild_v407')
assert 'scratchpad' in str(target)
t0 = time.time()
m = cm.build(target, W / ('CATALOG_' + EPOCH + '.json'))
rel = json.loads((cm.RELEASES / EPOCH / 'manifest.json').read_bytes())
res = {'elapsed_s': round(time.time() - t0, 1), 'rebuilt_generation': m['generation'], 'release_generation': rel['generation'], 'generation_equal': m['generation'] == rel['generation'],
       'rebuilt_index_sha256': m['index_sha256'], 'release_index_sha256': rel['index_sha256'], 'index_bytes_identical': m['index_sha256'] == rel['index_sha256'],
       'rebuilt_chunks': m['chunks'], 'release_chunks': rel['chunks'], 'chunks_equal': m['chunks'] == rel['chunks'],
       'rebuilt_docs_eq_release_docs(name,sha,bytes)': [(d['name'], d['sha256'], d['bytes']) for d in m['documents']] == [(d['name'], d['sha256'], d['bytes']) for d in rel['documents']],
       'sqlite_version': __import__('sqlite3').sqlite_version}
print(json.dumps(res, indent=1))
(W / 'review' / 'REV_REBUILD.json').write_text(json.dumps(res, indent=1), encoding='utf-8')
