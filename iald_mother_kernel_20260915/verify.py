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
from dotenv import dotenv_values
from iald_memoria_canonica import CanonicalMemory, payload_tokens
from iald_kernel import KernelCatalog
import iald_motores as motor
from copy import copy

cfg = motor.carregar_config(dotenv_values(ROOT / '.env').get)
catalog = KernelCatalog(cfg.kernel_bundle)
memory = CanonicalMemory(Path(r'C:\IALD\Central de Patentes\memory\TGL_ATLAS.md'), 'nucleo_kernel',
                         nucleus_manifest=WORK / 'iald_nucleo_fixo.json')
body, meta = memory.prompt('', catalog)
raw = (ROOT / 'IALD_Kernel_v5.txt').read_bytes()
assert raw.decode('utf-8-sig') in body
assert meta['mother_instruction']['sha256'] == hashlib.sha256(raw).hexdigest()
assert len(meta['fixed_hypothesis_sources']) == 5 and len(meta['fixed_nucleus_files']) == 7
assert body.index('KERNEL_DE_LINGUAGEM_INTEGRAL') < body.index('NÚCLEO DOCUMENTAL FIXO')
assert body.index('H1, H2 E H3 — CONSTRUÇÕES') < body.index('APLICAÇÃO DA INSTRUÇÃO-MÃE')
# Reserve 4k input tokens for tool definitions and a normal short conversation.
checks = []
for window in [cfg.janela, 500000]:
    for mode in ['fast', 'think']:
        limit = cfg.max_saida_pensar if mode == 'think' else cfg.max_saida
        try:
            messages, info = motor.montar_mensagens([{'role': 'user', 'content': 'Quem é você? Explique H1, H2 e H3.'}],
                body, cfg.modelo, [], window, limit)
            candidate = copy(cfg)
            candidate.janela = window
            payload = motor.montar_payload(candidate, cfg.modelo, messages, modo=mode)
            count = payload_tokens(payload)
            fits = count + payload['max_completion_tokens'] + 4000 <= window
            checks.append({'window': window, 'mode': mode, 'window_counted_tokens': count,
                           'output_tokens': payload['max_completion_tokens'], 'tool_and_history_margin': 4000,
                           'fits': fits})
        except ValueError as error:
            checks.append({'window': window, 'mode': mode, 'fits': False, 'error': str(error)})
assert all(row['fits'] for row in checks if row['window'] == 500000), checks
selected = cfg.janela if all(row['fits'] for row in checks if row['window'] == cfg.janela) else 500000
report = {'at': datetime.now().astimezone().isoformat(), 'context_tokens': meta['context_tokens'],
          'mother': meta['mother_instruction'], 'checks': checks, 'current_window': cfg.janela,
          'selected_window': selected, 'source_preserved': True, 'hypothesis_sources': 5, 'full_documents': 7}
with (WORK / 'verification.json').open('x', encoding='utf-8') as handle: json.dump(report, handle, ensure_ascii=False, indent=2)
print(json.dumps(report, ensure_ascii=False))
