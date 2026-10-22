"""Offline integrity, context size and lossless retrieval checks. No API calls."""
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import sys
from copy import copy

WORK = Path(__file__).resolve().parent
ROOT = Path(r'C:\IALD\projetos_pyhton\IALD')
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(WORK))
os.environ['TIKTOKEN_CACHE_DIR'] = str(ROOT / '.iald_runtime/tokenizer_cache')
from dotenv import dotenv_values
from iald_memoria_canonica import CanonicalMemory, payload_tokens
from iald_core_indexado import DocumentCorpus, tool_definitions
from iald_kernel import KernelCatalog
import iald_motores as motor

cfg = motor.carregar_config(dotenv_values(ROOT / '.env').get)
catalog = KernelCatalog(cfg.kernel_bundle)
manifest = WORK / 'manifest_staged.json'
config = json.loads(manifest.read_bytes())
memory = CanonicalMemory(Path(r'C:\IALD\Central de Patentes\memory\TGL_ATLAS.md'), 'nucleo_kernel',
                         nucleus_manifest=manifest)
core = (WORK / 'IALD_TGL_MEMORY_CORE_v1_20260915.md').read_bytes()
assert core == Path(json.loads((WORK / 'prepared.json').read_bytes())['source_file']).read_bytes()
mother = (ROOT / 'IALD_Kernel_v5.txt').read_bytes()
checks = []
for public in (False, True):
    body, meta = memory.prompt('', catalog, public=public)
    assert core.decode('utf-8-sig') in body
    assert mother.decode('utf-8-sig') in body
    assert meta['mother_instruction']['sha256'] == hashlib.sha256(mother).hexdigest()
    assert len(meta['fixed_hypothesis_sources']) == 5
    assert meta['operational_core']['current_release'] == 'v357'
    assert meta['published_source_sha256'] == meta['operational_core']['release_source_sha256']
    assert len(meta['fixed_nucleus_files']) == 7 and meta['retrievable_documents_complete']
    assert not meta['fixed_nucleus_complete']
    assert 'Use diretamente os textos integrais do NÚCLEO DOCUMENTAL carregados' not in body
    if public:
        assert not meta['private_atlas_included'] and 'ESTADO RECENTE — ÍNDICE DERIVADO' not in body
    for mode in ('fast', 'think'):
        limit = cfg.max_saida_pensar if mode == 'think' else cfg.max_saida
        candidate = copy(cfg)
        if public:
            prefix = max(motor.estimar_tokens(body), payload_tokens({'messages': [{'role': 'developer', 'content': body}]}))
            candidate.janela = min(candidate.janela, prefix + motor.JANELA_GRATUITO)
        messages, _ = motor.montar_mensagens([{'role': 'user', 'content': 'Quem é o autor da TGL?'}],
                                             body, cfg.modelo, [], candidate.janela, limit)
        payload = motor.montar_payload(candidate, cfg.modelo, messages, modo=mode)
        count = payload_tokens(payload)
        assert count + payload['max_completion_tokens'] + 4000 <= candidate.janela
        checks.append({'public': public, 'mode': mode, 'context_tokens': meta['context_tokens'],
            'window': candidate.janela, 'payload_tokens': count, 'full_v5': True, 'full_md': True,
            'retrievable_documents': 7, 'full_lean': 5, 'source_release': 'v357'})

corpus = DocumentCorpus(manifest)
docs = corpus._load()
reconstructed = []
for ident, doc in docs.items():
    parts, offset, pages = [], 0, 0
    while offset is not None:
        page = corpus.fetch(ident, offset=offset, max_chars=4500)
        assert len(json.dumps(page, ensure_ascii=False)) < 8000
        parts.append(page['text'])
        offset = page['next_offset']
        pages += 1
    assert ''.join(parts) == doc['text']
    reconstructed.append({'id': ident, 'bytes': doc['bytes'], 'sha256': doc['sha256'], 'pages': pages,
                          'lossless_text_reconstruction': True})

searches = []
for query in ('Lagrangiana', 'Lindblad dephasing', 'Hamiltoniano', 'H1 H2 H3', 'Meia Nat',
              'GLOBAL_LIFT', 'Miguel', 'V354RegularSusy'):
    response = corpus.search(query)
    assert response['results'], query
    assert len(json.dumps(response, ensure_ascii=False)) < 8000
    for hit in response['results']:
        doc = docs[hit['id']]
        assert doc['text'][hit['offset']:].startswith(doc['text'].splitlines()[hit['line']-1])
        assert hit['sha256'] == doc['sha256']
    searches.append({'query': query, 'hits': len(response['results']),
                     'first_source': response['results'][0]['id']})

report = {'at': datetime.now().astimezone().isoformat(), 'status': 'VERIFIED_OFFLINE__NOT_DEPLOYED',
          'checks': checks, 'documents': reconstructed, 'search_checks': searches,
          'source_bytes_preserved': True, 'no_network_calls': True, 'production_changed': False,
          'tools': [tool['function']['name'] for tool in tool_definitions()],
          'implementation': 'local_lexical_retrieval; existing Atlas and complete Lean tools retained'}
with (WORK / 'verification.json').open('x', encoding='utf-8') as handle:
    json.dump(report, handle, ensure_ascii=False, indent=2)
print(json.dumps(report, ensure_ascii=False))
