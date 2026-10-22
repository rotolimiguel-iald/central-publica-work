from pathlib import Path
from datetime import datetime
import json,hashlib
B=Path(__file__).resolve().parent;S=B.parent/'memory_stage'
p=B/'FINAL_RELEASE_HANDOFF.md';raw=p.read_bytes();text=raw.decode('utf-8')
rp=B/'provider_checks_20261002_120542_740846.json';r=json.loads(rp.read_bytes());assert r['status']=='PASS'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
assert r['prefix_sha256']==sha(S/'haiku_prefix.md')
old='- `_chat_avaliacao`, `_automatic_budget_available` e `_chat_externo` do servidor proposto são AST-idênticos à produção para estas funções; os controles de OpenAI/Sonnet, chineses e Haiku não foram afrouxados pela integração v380.'
new='- [ATUALIZAÇÃO — revisão restrita de routing_instruction] A igualdade AST integral de `_chat_avaliacao`/`_chat_externo` registrada anteriormente é histórica. O main acrescentou o argumento keyword `routing_instruction=None` e, em cada função, um único append à nota/instrução quando `routing_instruction` está presente e `task_scope is None`. Removendo exatamente essas duas adições de cada AST, o corpo remanescente coincide com a base anterior: montagem, `check_window`, contagem e reservas posteriores não foram alterados. Esta revisão não aprova mudanças fora dessas duas funções.'
assert old in text;text=text.replace(old,new)
old='MiMo/DeepSeek: prefixo final + mensagem sintética + 14 ferramentas públicas/de tarefa. Kimi: prefixo + mensagem e recuperação sintética de 24000 caracteres Unicode.'
new='MiMo/DeepSeek: prefixo final + nota de serviço/diretiva sintética de roteamento + mensagem sintética + 14 ferramentas públicas/de tarefa. Kimi: esse prefixo com diretiva + mensagem e recuperação sintética de 24000 caracteres Unicode. A diretiva acrescentou 83 bytes ao JSON MiMo/DeepSeek e está incluída na reserva. Os montadores reais de OpenAI/Sonnet/Haiku também preservaram a diretiva, sem duplicá-la quando já há task_scope.'
assert old in text;text=text.replace(old,new)
for provider in ('mimo','deepseek','kimi'):
    value=r['provider_reference_checks'][provider]
    lines=text.splitlines();start=next(i for i,line in enumerate(lines) if line.startswith('| '+provider+' |'))
    amount=f"{value['cold_hold_usd_reference']:.9f}" if 'cold_hold_usd_reference' in value else 'assinatura; política preservada'
    lines[start]=f"| {provider} | {value['input_json_utf8_bound']} | {value['output_reserve']} | {value['remaining_conservative_bound']} | {amount} |"
    text='\n'.join(lines)+'\n'
needle='Contagem real obtida pelo main:'
lines=text.splitlines();at=next(i for i,line in enumerate(lines) if line.startswith(needle))
lines.insert(at+1,'\nA referência 183310/11570 pertence ao recibo do pacote; não é uma medição da nova diretiva de cada chamada. `routing_instruction` é conteúdo dinâmico posterior ao prefixo e entra no contador nativo por pedido. Nesta regressão, o contador falso acrescentou 37 tokens sintéticos para verificar o aumento da reserva; esse número NÃO é contagem Anthropic real. Prefixo e recibo originais permanecem intactos.')
text='\n'.join(lines)+'\n'
old_line=next(line for line in text.splitlines() if line.startswith('- Checks adicionais 7/7:'))
text=text.replace(old_line,f'- Checks atuais 7/7, incluindo routing_instruction: `{rp}`; SHA256 `{sha(rp)}`. O recibo anterior permanece como história, sem representar o novo diff.')
text+='\n## Congelamento após a revisão da diretiva\n\n'
text+=f"Servidor staged lido nesta regressão: SHA256 `{r['source_pins'][str(B.parent/'app_patch/iald_web_server.py')]}`. Teste atualizado: SHA256 `{r['source_pins'][str(B/'test_provider_budget_context.py')]}`. Nenhum arquivo de servidor, controller ou memória foi editado por esta revisão; somente teste, novo recibo e este handoff. Nada foi enviado a provedores.\n"
backup=p.with_name(p.name+'.bak_'+datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
with backup.open('xb') as f:f.write(raw)
assert backup.read_bytes()==raw
temp=p.with_name(p.name+'.tmp');newraw=text.encode()
with temp.open('xb') as f:f.write(newraw)
assert temp.read_bytes()==newraw and len(newraw)>len(raw);temp.replace(p)
count=json.loads((B.parent/'count_20261002_113914_901730.json').read_bytes())
assert sha(S/'haiku_prefix.md')==count['draft_sha256'] and sha(S/'TGL_CLUSTER_v380.md')==count['cluster_sha256']
print(json.dumps({'handoff':str(p),'sha256':sha(p),'checks':r['status'],'tests':r['tests'],'prefix_unchanged':count['draft_sha256'],'cluster_unchanged':count['cluster_sha256']}))