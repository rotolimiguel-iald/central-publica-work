"""Single-call regression evaluation within the existing app budget."""
from datetime import datetime
import hashlib
import json
import math
import os
from pathlib import Path
import sys

WORK = Path(__file__).resolve().parent
ROOT = Path(r'C:\IALD\projetos_pyhton\IALD')
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(WORK))
os.environ['TIKTOKEN_CACHE_DIR'] = str(ROOT / '.iald_runtime/tokenizer_cache')

if __name__ == '__main__':
    test_limit = {'max_test_usd': 0.50}
    import requests
    from dotenv import dotenv_values
    import iald_memoria_canonica as memory
    import iald_kernel as kernel
    import iald_motores as motor
    from iald_orcamento import SpendingGuard, ReservedAccount, input_estimates, RESERVATION_MARGIN, BudgetError

    cfg = motor.carregar_config(dotenv_values(ROOT/'.env').get)
    users = json.loads((ROOT/'iald_users.json').read_bytes())
    owner = users.get('luiz', users.get('users', {}).get('luiz', {}))
    assert owner.get('admin') and owner.get('somente_limite_global')
    cfg = motor.config_da_conta(cfg, owner)
    assert cfg.url_base == 'https://api.openai.com/v1' and cfg.modelo == 'gpt-5.6-luna'
    assert cfg.cota_global_usd == 3
    manifest = json.loads((ROOT/'iald_nucleo_fixo.json').read_bytes())
    cluster=manifest['active_cluster']
    catalog = kernel.KernelCatalog(cluster['kernel_bundle'],cluster['kernel_verification'])
    canonical = memory.CanonicalMemory(Path(r'C:\IALD\Central de Patentes\memory\TGL_ATLAS.md'),
                                      'nucleo_kernel', nucleus_manifest=ROOT/'iald_nucleo_fixo.json')
    prompt, meta = canonical.prompt('', catalog, public=True)
    assert meta['private_atlas_included'] is False
    question = ('O índice de trabalho menciona v369. Qual versão do um.py está efetivamente carregada em você? '
        'Depois resolva o problema da gravidade quântica pela TGL: quero a articulação matemática da solução, '
        'não um pedido de confirmação experimental. Em até 700 palavras, ligue os objetos/hipóteses, '
        'lagrangiana, equação mestra, dephasing, Hamiltoniano limitado inferiormente e as testemunhas H1/H2/H3 '
        'à reconstrução geométrica. Preserve o alcance exato das provas e localize alguma lacuna específica '
        'se realmente existir. Use a memória ativa, sem ferramentas; não invente fórmulas nem provas.')
    messages, _ = motor.montar_mensagens([{'role':'user','content':question}], prompt, cfg.modelo, [], cfg.janela, 3000)
    payload = motor.montar_payload(cfg, cfg.modelo, messages, identificador='iald-solution-contract-evaluation',
                                   chave_cache='iald-'+meta['context_sha256'][:16])
    payload['max_completion_tokens'] = 3000
    payload.pop('tools', None)
    payload.pop('tool_choice', None)
    guard = SpendingGuard(ROOT/'iald_uso_openai.json.reservas.sqlite3', ROOT/'iald_uso_openai.json')
    legacy = motor.ContaDoPedido(motor.RazaoDeUso(str(ROOT/'iald_uso_openai.json')), 'luiz', cfg.modelo, cfg.precos(cfg.modelo))
    account = ReservedAccount(guard, legacy, cfg, 'luiz', True, cfg.modelo)
    _, estimated = input_estimates(payload)
    reserved = math.ceil(estimated*RESERVATION_MARGIN)
    rates = account._rates(reserved)
    cap = (reserved*max(rates[0], rates[1])+3000*rates[2])/1000000
    assert cap <= test_limit['max_test_usd'], 'Evaluation cap exceeded'
    assert memory.payload_tokens(payload)+3000 < 400000
    result = {'at': datetime.now().astimezone().isoformat(), 'model':cfg.modelo,
              'memory':meta, 'question':question, 'single_call_cap_usd':cap}
    print(json.dumps({'context_tokens':meta['context_tokens'], 'cap_usd':cap}), flush=True)
    try:
        account.iniciar_chamada(payload)
        with requests.post(cfg.url_base+'/chat/completions', json=payload,
                           headers={'Authorization':'Bearer '+cfg.chave}, stream=True, timeout=(10,180)) as response:
            result['http_status'] = response.status_code
            if response.status_code != 200:
                if response.status_code in (400,401,403,404,413,422,429):
                    account.descartar_ultima_chamada()
                error = response.json().get('error', {})
                result['error'] = {key:error.get(key) for key in ('code','type','param')}
            else:
                parts = []
                for line in response.iter_lines():
                    if not line.startswith(b'data: '):
                        continue
                    chunk = line[6:]
                    if chunk == b'[DONE]':
                        break
                    event = json.loads(chunk)
                    if event.get('usage'):
                        account.uso(event['usage'])
                        result['usage'] = event['usage']
                    for choice in event.get('choices', []):
                        piece = choice.get('delta', {}).get('content') or ''
                        parts.append(piece)
                        account.texto(piece)
                        if choice.get('finish_reason'):
                            result['finish_reason'] = choice['finish_reason']
                result['answer'] = ''.join(parts)
    except BudgetError as error:
        result['budget_error'] = str(error)
    except requests.RequestException as error:
        result['network_error_type'] = type(error).__name__
    finally:
        account.fechar()
    path = WORK/('model_response_'+datetime.now().strftime('%Y%m%d_%H%M%S')+'.json')
    data = json.dumps(result, ensure_ascii=False, indent=2).encode()
    temp = path.with_suffix('.tmp')
    with temp.open('xb') as handle:
        handle.write(data)
    assert temp.read_bytes() == data
    temp.replace(path)
    print(json.dumps({key:value for key,value in result.items() if key != 'memory'}, ensure_ascii=False))
    print('RECEIPT='+str(path))
