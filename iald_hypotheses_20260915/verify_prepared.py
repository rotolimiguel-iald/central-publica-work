from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import sys
sys.dont_write_bytecode = True
WORK = Path(__file__).resolve().parent
ROOT = Path(r'C:\IALD\projetos_pyhton\IALD')
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(WORK))
os.environ['TIKTOKEN_CACHE_DIR'] = str(ROOT / '.iald_runtime/tokenizer_cache')
from iald_memoria_canonica import CanonicalMemory
from iald_kernel import KernelCatalog
from iald_orcamento import input_estimates, RESERVATION_MARGIN
import math

cfg = {}
for line in (ROOT / '.env').read_text(encoding='utf-8-sig').splitlines():
    key, sep, value = line.partition('=')
    if key in ('IALD_KERNEL_BUNDLE', 'IALD_OPENAI_JANELA'): cfg[key] = value.strip()
catalog = KernelCatalog(cfg['IALD_KERNEL_BUNDLE'])
manifest = json.loads((WORK / 'iald_nucleo_fixo.json').read_bytes())
memory = CanonicalMemory(Path(r'C:\IALD\Central de Patentes\memory\TGL_ATLAS.md'), 'nucleo_kernel',
                         nucleus_manifest=WORK / 'iald_nucleo_fixo.json')
body, meta = memory.prompt('', catalog)
assert len(meta['fixed_hypothesis_sources']) == 5
assert len(meta['fixed_nucleus_files']) == 7
for entry in manifest['published_evidence']['hypothesis_sources']:
    assert catalog._read_checked(entry['catalog_path']) in body
assert body.index('H1, H2 E H3 — CONSTRUÇÕES') < body.index('DISCIPLINA DE CONSULTA E RESPOSTA')
assert '"discharged_in_kernel": false' in body
assert '"modo": "OPEN"' in body
payload = {'messages': [{'role': 'system', 'content': body}, {'role': 'user', 'content': 'Explique H1 H2 H3.'}]}
measured, estimated = input_estimates(payload)
conservative = math.ceil(estimated * RESERVATION_MARGIN)
print(json.dumps({'actual': meta['context_tokens'], 'payload_measured': measured,
                  'estimated': estimated, 'reservation_estimate': conservative}), flush=True)
assert meta['context_tokens'] + 8192 < int(cfg['IALD_OPENAI_JANELA'])
assert measured + 8192 < int(cfg['IALD_OPENAI_JANELA'])
report = {'at': datetime.now().astimezone().isoformat(), 'context_tokens': meta['context_tokens'],
          'window_counted_tokens': measured, 'financial_reservation_estimate': conservative,
          'window': int(cfg['IALD_OPENAI_JANELA']),
          'full_documents': len(meta['fixed_nucleus_files']), 'full_lean_sources': meta['fixed_hypothesis_sources'],
          'context_sha256': meta['context_sha256'], 'all_sources_complete': True,
          'original_negative_flags_preserved': True, 'api_called': False}
data = json.dumps(report, ensure_ascii=False, indent=2).encode()
with (WORK / 'verification.json').open('xb') as handle: handle.write(data)
assert (WORK / 'verification.json').read_bytes() == data
print(json.dumps({key: value for key, value in report.items() if key != 'full_lean_sources'}))
