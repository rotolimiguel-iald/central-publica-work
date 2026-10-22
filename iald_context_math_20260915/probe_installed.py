"""One bounded provider diagnostic with installed context and shared spending guard."""
from datetime import datetime
import json
import math
import os
from pathlib import Path
import re
import sys
import requests
from dotenv import dotenv_values

WORK = Path(__file__).resolve().parent
ROOT = Path(r"C:\IALD\projetos_pyhton\IALD")
sys.path.insert(0, str(ROOT))
os.environ['TIKTOKEN_CACHE_DIR'] = str(ROOT / '.iald_runtime/tokenizer_cache')
import iald_memoria_canonica as memory
import iald_kernel as kernel
import iald_motores as motor
from iald_orcamento import SpendingGuard, ReservedAccount, input_estimates, RESERVATION_MARGIN, BudgetError

cfg = motor.carregar_config(dotenv_values(ROOT / '.env').get)
assert cfg.url_base == 'https://api.openai.com/v1'
assert cfg.modelo == 'gpt-5.6-luna' and cfg.memoria_modo == 'nucleo_kernel'
cfg.max_saida = 256
catalog = kernel.KernelCatalog(cfg.kernel_bundle, cfg.kernel_verification)
prompt, metadata = memory.CanonicalMemory(cfg.atlas_path, cfg.memoria_modo).prompt('', catalog)
messages, info = motor.montar_mensagens([{'role':'user','content':
    'Quem é o autor da Teoria da Gravitação Luminodinâmica (TGL)? Use somente os documentos já carregados e responda em duas frases, citando uma fonte.'}],
    prompt, cfg.modelo, [], cfg.janela, 256)
payload = motor.montar_payload(cfg, cfg.modelo, messages,
    identificador='iald-operator-approved-nucleus-test', chave_cache='iald-' + metadata['context_sha256'][:16])
guard = SpendingGuard(ROOT / 'iald_uso_openai.json.reservas.sqlite3', ROOT / 'iald_uso_openai.json')
legacy = motor.ContaDoPedido(motor.RazaoDeUso(str(WORK / 'diagnostic_usage.json')), 'luiz', cfg.modelo, cfg.precos(cfg.modelo))
account = ReservedAccount(guard, legacy, cfg, 'luiz', True, cfg.modelo)
counted, estimated = input_estimates(payload)
reserved_input = math.ceil(estimated * RESERVATION_MARGIN)
rates = account._rates(reserved_input)
single_call_cap = (reserved_input * max(rates[0], rates[1]) + 256 * rates[2]) / 1_000_000
assert single_call_cap <= .25, 'Diagnostic per-call cap exceeded; no request sent'
record = {'recorded_at': datetime.now().astimezone().isoformat(), 'model':cfg.modelo,
          'memory':metadata, 'kernel':catalog.status(), 'payload_tokens':memory.payload_tokens(payload),
          'prompt_characters':len(prompt), 'max_completion_tokens':payload['max_completion_tokens'],
          'single_call_cap_usd': single_call_cap}
print(json.dumps({'context_tokens':metadata['context_tokens'], 'payload_tokens':record['payload_tokens'],
                  'fixed_nucleus_complete':metadata['fixed_nucleus_complete']}), flush=True)
try:
    account.iniciar_chamada(payload)
    with requests.post(cfg.url_base + '/chat/completions', json=payload,
            headers={'Authorization':'Bearer ' + cfg.chave}, stream=True, timeout=(10,120)) as response:
        record['http_status'] = response.status_code
        record['rate_limits'] = {k:v for k,v in response.headers.items() if k.lower().startswith('x-ratelimit-') or k.lower()=='retry-after'}
        if response.status_code != 200:
            if response.status_code in (400,401,403,404,413,422,429):
                account.descartar_ultima_chamada()
            error = response.json().get('error', {})
            record['error'] = {k:re.sub(r'(?:org-|proj_)[A-Za-z0-9_-]+','[identifier]',motor.mascarar(v))
                               for k,v in error.items() if k in ('code','type','message','param')}
        else:
            parts = []
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
                    delta = choice.get('delta',{}).get('content') or ''
                    parts.append(delta)
                    account.texto(delta)
            record['answer'] = ''.join(parts)
except requests.exceptions.RequestException as error:
    record['network_error_type'] = type(error).__name__
except BudgetError as error:
    record['budget_error'] = str(error)
finally:
    account.fechar()
target = WORK / ('installed_probe_' + datetime.now().strftime('%Y%m%d_%H%M%S_%f') + '.json')
data = json.dumps(record, ensure_ascii=False, indent=2).encode('utf-8')
temp = target.with_suffix('.tmp')
with temp.open('xb') as handle:
    handle.write(data)
assert temp.read_bytes() == data
temp.replace(target)
print(json.dumps({k:v for k,v in record.items() if k not in ('memory','kernel')}, ensure_ascii=True), flush=True)
print('RECEIPT=' + str(target))
