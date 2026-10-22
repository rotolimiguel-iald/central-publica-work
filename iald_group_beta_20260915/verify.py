from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import sys
from copy import copy
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

values = dotenv_values(ROOT / '.env')
cfg = motor.carregar_config(values.get)
catalog = KernelCatalog(cfg.kernel_bundle)
memory = CanonicalMemory(Path(r'C:\IALD\Central de Patentes\memory\TGL_ATLAS.md'), 'nucleo_kernel',
                         nucleus_manifest=WORK / 'iald_nucleo_fixo.json')
raw = (ROOT / 'IALD_Kernel_v5.txt').read_bytes()
checks = []
for public in (False, True):
    body, meta = memory.prompt('', catalog, public=public)
    assert raw.decode('utf-8-sig') in body
    assert meta['mother_instruction']['sha256'] == hashlib.sha256(raw).hexdigest()
    assert len(meta['fixed_hypothesis_sources']) == 5 and len(meta['fixed_nucleus_files']) == 7
    if public:
        assert meta['private_atlas_included'] is False
        assert 'ESTADO RECENTE — ÍNDICE DERIVADO' not in body
        assert 'IALD_MOTHER_V5_NARROW_PREPARED_20260915' not in body
    for mode in ('fast', 'think'):
        limit = cfg.max_saida_pensar if mode == 'think' else cfg.max_saida
        candidate = copy(cfg)
        candidate.janela = 500000
        if public:
            prefix = max(motor.estimar_tokens(body), payload_tokens({'messages': [{'role': 'developer', 'content': body}]}))
            candidate.janela = min(candidate.janela, prefix + motor.JANELA_GRATUITO)
        messages, _ = motor.montar_mensagens([{'role': 'user', 'content': 'Quem é o autor da TGL?'}],
                                             body, cfg.modelo, [], candidate.janela, limit)
        payload = motor.montar_payload(candidate, cfg.modelo, messages, modo=mode)
        count = payload_tokens(payload)
        assert count + payload['max_completion_tokens'] + 4000 <= candidate.janela
        checks.append({'public': public, 'mode': mode, 'context_tokens': meta['context_tokens'],
            'window': candidate.janela, 'payload_tokens': count, 'full_v5': True, 'full_documents': 7, 'full_lean': 5})
users = json.loads((ROOT / 'iald_users.json').read_bytes())
review = users.get('review', {})
report = {'at': datetime.now().astimezone().isoformat(), 'checks': checks,
          'signup_configured': values.get('IALD_ENTRADA_ABERTA'),
          'review_account': {'exists': bool(review), 'admin': bool(review.get('admin')),
                             'active': review.get('active'), 'plano': motor.plano_de(review) if review else None},
          'selected_window': 500000, 'source_preserved': True}
with (WORK / 'verification.json').open('x', encoding='utf-8') as handle:
    json.dump(report, handle, ensure_ascii=False, indent=2)
print(json.dumps(report, ensure_ascii=False))
