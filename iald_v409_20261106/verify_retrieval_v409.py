"""Read installed v409 through the app's scientific tools, without inference."""
import json
from time import perf_counter
from verify_installed import W, R, offline_loader_guard

attempts = offline_loader_guard()
from iald_kernel import KernelCatalog
from iald_core_indexado import execute_tool

manifest = R / 'iald_nucleo_fixo.json'
config = json.loads(manifest.read_bytes())
assert config['operational_core']['current_release'] == 'v409'
cluster = config['active_cluster']
kernel = KernelCatalog(cluster['kernel_bundle'], cluster['kernel_verification'])
highlights = json.loads((W / 'app/KERNEL_HIGHLIGHTS.json').read_bytes())
anchor = next(a for a in highlights['anchors'] if a['symbol'] == 'TGLExt.TraducaoTuring.p_igual_np_no_modo_selecao')
symbol = anchor['symbol'].rsplit('.', 1)[-1]
started = perf_counter()
hits = kernel.search(symbol, limit=5)['results']
assert any(r['path'] == anchor['path'] for r in hits)
lines = kernel.read_file(anchor['path'], anchor['lines'][0], anchor['lines'][1] - anchor['lines'][0] + 1)
assert anchor['statement'] in lines['text']
documents = execute_tool(manifest, 'search_tgl', {'query': symbol, 'limit': 5})['results']
assert documents
recovered = []
for result in documents:
    fetched = execute_tool(manifest, 'fetch_tgl', {'id': result['id'], 'offset': result['offset'], 'max_chars': 4500})
    assert fetched['sha256'] == result['sha256']
    recovered.append({'id': result['id'], 'hash_matches': True, 'symbol_present': symbol in fetched['text']})
assert any(row['symbol_present'] for row in recovered)
assert not any(attempts.values())
report = {'status': 'PASS', 'release': 'v409', 'source_sha256': kernel.source_sha,
          'anchor': {'symbol': anchor['symbol'], 'path': anchor['path'], 'sha256': anchor['sha256'], 'lines': anchor['lines']},
          'statement_exact': True, 'document_results': recovered, 'elapsed_seconds': perf_counter()-started,
          'audit_attempts': attempts, 'scope': 'Installed search_tgl/fetch_tgl and formal source reader; no LLM response, theorem execution or scientific confirmation.'}
with (W / 'INSTALLED_RETRIEVAL.json').open('x', encoding='utf8') as f:
    json.dump(report, f, ensure_ascii=False, indent=2)
print(json.dumps(report, ensure_ascii=False))
