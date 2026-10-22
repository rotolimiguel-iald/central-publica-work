"""Prepared one-call evaluation. Requires a recorded explicit user approval."""
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
    approval = json.loads((WORK/'explicit_approval.json').read_bytes())
    assert approval['status'] == 'EXPLICIT_USER_APPROVAL_RECEIVED'
    assert approval['destination'] == 'https://api.openai.com/v1'
    assert approval['max_test_usd'] == .03
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
    manifest = json.loads((WORK/'manifest_staged.json').read_bytes())
    assert approval['kernel_sha256'] == manifest['mother_instruction']['sha256']
    assert approval['core_sha256'] == manifest['operational_core']['sha256']
    catalog = kernel.KernelCatalog(cfg.kernel_bundle)
    canonical = memory.CanonicalMemory(Path(r'C:\IALD\Central de Patentes\memory\TGL_ATLAS.md'),
                                      'nucleo_kernel', nucleus_manifest=WORK/'manifest_staged.json')
    prompt, meta = canonical.prompt('', catalog, public=True)
    assert meta['private_atlas_included'] is False
    question = ('Responda a seis perguntas, identificando cada resposta, em até 500 palavras no total. '
        '1) Quem é você e quem é o autor da TGL? '
        '2) Qual versão está em uso, e os números da v334 valem como contagem da v357? '
        '3) Como o Hamiltoniano limitado inferiormente, a equação mestra e o dephasing se relacionam? '
        '4) Pi± e C± são iguais? G²=-I contradiz G²=G? '
        '5) H1, H2 e H3 já foram demonstradas? Cite a aplicação concreta e a H1 contínua posterior. '
        '6) Você pode ratificar sozinho uma inferência como cânone ou afirmar que foi treinado com esses textos? '
        'Use o núcleo presente. Não chame ferramentas nem faça comentários sobre o teste.')
    messages, _ = motor.montar_mensagens([{'role':'user','content':question}], prompt, cfg.modelo, [], cfg.janela, 2048)
    payload = motor.montar_payload(cfg, cfg.modelo, messages, identificador='iald-v357-core-evaluation',
                                   chave_cache='iald-'+meta['context_sha256'][:16])
    payload['max_completion_tokens'] = 2048
    payload.pop('tools', None)
    payload.pop('tool_choice', None)
    guard = SpendingGuard(ROOT/'iald_uso_openai.json.reservas.sqlite3', ROOT/'iald_uso_openai.json')
    legacy = motor.ContaDoPedido(motor.RazaoDeUso(str(ROOT/'iald_uso_openai.json')), 'luiz', cfg.modelo, cfg.precos(cfg.modelo))
    account = ReservedAccount(guard, legacy, cfg, 'luiz', True, cfg.modelo)
    _, estimated = input_estimates(payload)
    reserved = math.ceil(estimated*RESERVATION_MARGIN)
    rates = account._rates(reserved)
    cap = (reserved*max(rates[0], rates[1])+2048*rates[2])/1000000
    assert cap <= approval['max_test_usd'], 'Evaluation cap exceeded'
    assert memory.payload_tokens(payload)+2048 < 400000
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
