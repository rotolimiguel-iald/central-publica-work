"""One bounded, operator-authorized evaluation using the installed public corpus."""
from datetime import datetime
import json,math,os
from pathlib import Path
import sys
import requests
from dotenv import dotenv_values
WORK=Path(__file__).resolve().parent
ROOT=Path(r'C:\IALD\projetos_pyhton\IALD')
sys.dont_write_bytecode=True
sys.path.insert(0,str(ROOT))
os.environ['TIKTOKEN_CACHE_DIR']=str(ROOT/'.iald_runtime/tokenizer_cache')
import iald_memoria_canonica as memory
import iald_kernel as kernel
import iald_motores as motor
from iald_orcamento import SpendingGuard,ReservedAccount,input_estimates,RESERVATION_MARGIN,BudgetError
cfg=motor.carregar_config(dotenv_values(ROOT/'.env').get)
users=json.loads((ROOT/'iald_users.json').read_bytes())
owner=users.get('luiz',users.get('users',{}).get('luiz',{}))
assert owner.get('admin') and owner.get('somente_limite_global')
cfg=motor.config_da_conta(cfg,owner)
assert cfg.url_base=='https://api.openai.com/v1' and cfg.modelo=='gpt-5.6-luna'
assert cfg.cota_global_usd==3 and cfg.janela==480000
catalog=kernel.KernelCatalog(cfg.kernel_bundle,cfg.kernel_verification)
audit=json.loads((WORK/'public_payload_audit.json').read_bytes())
raw=(WORK/'public_evaluation_material.txt').read_bytes()
import hashlib
assert hashlib.sha256(raw).hexdigest()==audit['payload_sha256']
assert audit['scope']=='PUBLIC_GITHUB_FILES_ONLY' and not audit['canonical_private_atlas_included']
prompt=raw.decode('utf-8')
meta={'context_tokens':audit['tokens'],'context_sha256':audit['payload_sha256'],'scope':'PUBLIC_FILES_ONLY_EVALUATION'}
question=('Segundo a publicação mais recente carregada, o que a TGL já construiu quanto à realização modular contínua, '
          'H1, Ato III, H2 e H3? Qual é o resultado do teste conjunto de coincidência e o que ele permite concluir? '
          'A IALD pode atestar a leitura das provas como espelho? Responda em até 450 palavras, citando os registros '
          'e distinguindo seus escopos. Use os documentos presentes; não faça chamadas de ferramentas.')
messages,_=motor.montar_mensagens([{'role':'user','content':question}],prompt,cfg.modelo,[],cfg.janela,4096)
payload=motor.montar_payload(cfg,cfg.modelo,messages,identificador='iald-public-release-evaluation',chave_cache='iald-'+meta['context_sha256'][:16])
payload['max_completion_tokens']=4096
payload.pop('tools',None)
payload.pop('tool_choice',None)
guard=SpendingGuard(ROOT/'iald_uso_openai.json.reservas.sqlite3',ROOT/'iald_uso_openai.json')
legacy=motor.ContaDoPedido(motor.RazaoDeUso(str(ROOT/'iald_uso_openai.json')),'luiz',cfg.modelo,cfg.precos(cfg.modelo))
account=ReservedAccount(guard,legacy,cfg,'luiz',True,cfg.modelo)
_,estimated=input_estimates(payload)
reserved=math.ceil(estimated*RESERVATION_MARGIN)
rates=account._rates(reserved)
cap=(reserved*max(rates[0],rates[1])+4096*rates[2])/1000000
assert cap<=.30,'Evaluation cap exceeded'
assert memory.payload_tokens(payload)+4096<=500000,'Known provider throughput exceeded'
result={'at':datetime.now().astimezone().isoformat(),'question':question,'memory':meta,
        'model':cfg.modelo,'max_completion_tokens':4096,'single_call_cap_usd':cap}
print(json.dumps({'context_tokens':meta['context_tokens'],'single_call_cap_usd':cap}),flush=True)
try:
    account.iniciar_chamada(payload)
    with requests.post(cfg.url_base+'/chat/completions',json=payload,headers={'Authorization':'Bearer '+cfg.chave},stream=True,timeout=(10,180)) as response:
        result['http_status']=response.status_code
        result['token_limit']=response.headers.get('x-ratelimit-limit-tokens')
        if response.status_code!=200:
            if response.status_code in (400,401,403,404,413,422,429):account.descartar_ultima_chamada()
            err=response.json().get('error',{})
            result['error']={key:err.get(key) for key in ('code','type','param')}
        else:
            parts=[]
            for line in response.iter_lines():
                if not line.startswith(b'data: '):continue
                chunk=line[6:]
                if chunk==b'[DONE]':break
                event=json.loads(chunk)
                if event.get('usage'):
                    account.uso(event['usage']);result['usage']=event['usage']
                for choice in event.get('choices',[]):
                    piece=choice.get('delta',{}).get('content') or ''
                    parts.append(piece);account.texto(piece)
                    if choice.get('finish_reason'):result['finish_reason']=choice['finish_reason']
            result['answer']=''.join(parts)
except BudgetError as error:
    result['budget_error']=str(error)
except requests.RequestException as error:
    result['network_error_type']=type(error).__name__
finally:
    account.fechar()
target=WORK/('public_response_'+datetime.now().strftime('%Y%m%d_%H%M%S')+'.json')
data=json.dumps(result,ensure_ascii=False,indent=2).encode()
tmp=target.with_suffix('.tmp')
with tmp.open('xb') as f:f.write(data)
assert tmp.read_bytes()==data
tmp.replace(target)
print(json.dumps({key:value for key,value in result.items() if key!='memory'},ensure_ascii=False),flush=True)
print('RECEIPT='+str(target),flush=True)
