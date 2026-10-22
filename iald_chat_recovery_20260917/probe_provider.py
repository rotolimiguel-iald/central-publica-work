"""One minimal billable diagnostic, within the existing global budget."""
from datetime import datetime
import json
import math
import os
from pathlib import Path
import sys

ROOT = Path(r'C:\IALD\projetos_pyhton\IALD')
WORK = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT))
os.environ['TIKTOKEN_CACHE_DIR'] = str(ROOT / '.iald_runtime/tokenizer_cache')


def main():
    import requests
    from dotenv import dotenv_values
    import iald_motores as motor
    from iald_orcamento import SpendingGuard, ReservedAccount, input_estimates, RESERVATION_MARGIN
    assert not (WORK / 'provider_probe.json').exists(), 'Diagnostic already performed'
    cfg = motor.carregar_config(dotenv_values(ROOT / '.env').get)
    owner = json.loads((ROOT / 'iald_users.json').read_bytes())['luiz']
    assert owner.get('admin') and owner.get('somente_limite_global') and motor.consentiu(owner)
    cfg = motor.config_da_conta(cfg, owner)
    assert cfg.url_base == 'https://api.openai.com/v1' and cfg.modelo == 'gpt-5.6-luna'
    assert cfg.cota_global_usd == 3
    model = motor.modelo_para(owner, cfg)
    payload = motor.montar_payload(cfg, model,
        [{'role': 'user', 'content': 'Responda apenas: OK'}],
        identificador='iald-connection-diagnostic-20260917')
    payload['max_completion_tokens'] = 32
    payload.pop('tools', None)
    payload.pop('tool_choice', None)
    guard = SpendingGuard(ROOT / 'iald_uso_openai.json.reservas.sqlite3', ROOT / 'iald_uso_openai.json')
    legacy = motor.ContaDoPedido(motor.RazaoDeUso(str(ROOT / 'iald_uso_openai.json')),
                                'luiz', model, cfg.precos(model))
    account = ReservedAccount(guard, legacy, cfg, 'luiz', True, model)
    _, estimated = input_estimates(payload)
    reserved = math.ceil(estimated * RESERVATION_MARGIN)
    rates = account._rates(reserved)
    cap = (reserved * max(rates[0], rates[1]) + 32 * rates[2]) / 1000000
    assert cap < .001
    result = {'at': datetime.now().astimezone().isoformat(), 'model': model,
              'single_call_cap_usd': cap, 'private_context_sent': False,
              'prompt': 'Responda apenas: OK'}
    try:
        account.iniciar_chamada(payload)
        with requests.post(cfg.url_base + '/chat/completions', json=payload,
            headers={'Authorization': 'Bearer ' + cfg.chave}, stream=True, timeout=(10,45)) as response:
            result['http_status'] = response.status_code
            if response.status_code != 200:
                if response.status_code in (400,401,403,404,413,422,429):
                    account.descartar_ultima_chamada()
                error = motor.erro_de_resposta(response)
                result['error'] = {'status': error.status, 'code': error.codigo, 'type': error.tipo}
            else:
                parts = []
                for line in response.iter_lines():
                    if not line.startswith(b'data: '):
                        continue
                    raw = line[6:]
                    if raw == b'[DONE]':
                        break
                    event = json.loads(raw)
                    if event.get('usage'):
                        account.uso(event['usage'])
                        result['usage'] = event['usage']
                    for choice in event.get('choices', []):
                        piece = choice.get('delta', {}).get('content') or ''
                        account.texto(piece)
                        parts.append(piece)
                        if choice.get('finish_reason'):
                            result['finish_reason'] = choice['finish_reason']
                result['answer'] = ''.join(parts)
    except Exception as error:
        result['exception_type'] = type(error).__name__
    finally:
        account.fechar()
    raw = json.dumps(result, ensure_ascii=False, indent=2).encode()
    temp = WORK / 'provider_probe.json.tmp'
    with temp.open('xb') as f:
        f.write(raw)
    assert temp.read_bytes() == raw
    temp.replace(WORK / 'provider_probe.json')
    print(json.dumps(result, ensure_ascii=False))


if __name__ == '__main__':
    main()
