"""One bounded real call with the complete canonical Atlas; metadata-only log."""
from datetime import datetime
import json
import os
from pathlib import Path
import re
import sys
import requests
from dotenv import dotenv_values

WORK = Path(__file__).parent
sys.path[:0] = [str(WORK / 'stage'), str(WORK / 'dependencies')]
os.environ['TIKTOKEN_CACHE_DIR'] = str(WORK / 'tokenizer_cache')
import iald_kernel as kernel
import iald_memoria_canonica as memory
import iald_motores as motor
from iald_orcamento import ReservedAccount, SpendingGuard

cfg = motor.Config(chave=dotenv_values(r'C:\IALD\projetos_pyhton\IALD\.env').get('IALD_OPENAI_API_KEY'),
                   modelo='gpt-4.1-nano', janela=1047576, max_saida=256, cota_operador_usd=.20)
catalog = kernel.KernelCatalog(next((WORK / 'bundles').glob('kernel-*')))
atlas = memory.CanonicalMemory(r'C:\IALD\Central de Patentes\memory\TGL_ATLAS.md')
nucleus, _ = motor.ler_prompt_canonico(r'C:\IALD\projetos_pyhton\IALD\app\kernel_prompt_loja.js')
prompt, metadata = atlas.prompt(nucleus, catalog)
messages, info = motor.montar_mensagens([{'role': 'user', 'content':
    'Segundo a seção I.1 do Atlas, qual é o axioma único e seu estatuto? Responda em até duas frases e não execute ferramentas.'}],
    prompt, cfg.modelo, [], cfg.janela, 256)
payload = motor.montar_payload(cfg, cfg.modelo, messages, identificador='iald-operator-integration-probe', chave_cache='iald-' + metadata['context_sha256'][:16])
ledger = motor.RazaoDeUso(str(WORK / 'api_integration_usage.json'))
guard = SpendingGuard(WORK / 'api_integration_reservations.sqlite3')
account = ReservedAccount(guard, motor.ContaDoPedido(ledger, 'operator_integration_probe', cfg.modelo, cfg.precos(cfg.modelo)),
                          cfg, 'operator_integration_probe', True, cfg.modelo)
record = {'memory': metadata, 'kernel': catalog.status(), 'payload_tokens_with_overhead': memory.payload_tokens(payload)}
try:
    account.iniciar_chamada(payload)
    with requests.post('https://api.openai.com/v1/chat/completions', json=payload,
            headers={'Authorization': 'Bearer ' + cfg.chave}, stream=True, timeout=(10, 120)) as response:
        record['status'] = response.status_code
        record['rate_limits'] = {k: v for k, v in response.headers.items() if k.lower().startswith('x-ratelimit-')}
        if response.status_code != 200:
            if response.status_code in (400, 401, 403, 404, 413, 422, 429):
                account.descartar_ultima_chamada()
            error = response.json().get('error', {})
            record['error'] = {k: re.sub(r'org-[A-Za-z0-9_-]+', '[organization]', motor.mascarar(v))
                               for k, v in error.items() if k in ('code', 'type', 'message', 'param')}
        else:
            text = []
            for line in response.iter_lines():
                if not line.startswith(b'data: '):
                    continue
                data = line[6:]
                if data == b'[DONE]':
                    break
                event = json.loads(data)
                if event.get('usage'):
                    account.uso(event['usage'])
                    record['usage'] = event['usage']
                for choice in event.get('choices', []):
                    delta = choice.get('delta', {}).get('content') or ''
                    account.texto(delta)
                    text.append(delta)
            record['answer'] = ''.join(text)
except requests.exceptions.RequestException as error:
    record['network_error_type'] = type(error).__name__
finally:
    account.fechar()
record['spending'] = guard.summary()
path = WORK / ('full_atlas_probe_' + datetime.now().strftime('%Y%m%d_%H%M%S') + '.json')
path.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')
print(json.dumps(record, ensure_ascii=False, indent=2))
