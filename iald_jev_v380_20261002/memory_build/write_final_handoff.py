from pathlib import Path
from datetime import datetime
import hashlib,json
B=Path(__file__).resolve().parent;W=B.parent;S=W/'memory_stage'
read=lambda p:json.loads(Path(p).read_bytes());sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
count_path=W/'count_20261002_113914_901730.json';count=read(count_path)
check_path=B/'provider_checks_20261002_115012_364687.json';checks=read(check_path)
delivery_path=B/'delivery_20261002_115012_880732.json';delivery=read(delivery_path)
review_path=W/'validation/memory_review.json';review=read(review_path)
assert checks['status']==review['status']=='PASS' and delivery['status']=='READY_FOR_MAIN_INTEGRATION'
assert count['draft_sha256']==checks['prefix_sha256']==sha(S/'haiku_prefix.md')==sha(S/'haiku_runtime/prefix.md')
manifest=read(S/'manifest_staged.json');runtime=read(S/'haiku_runtime/manifest.json')
assert runtime['budget']==count['budget'] and runtime['deployment']==delivery['deployment_identity']
assert count['cluster_sha256']==sha(S/'TGL_CLUSTER_v380.md')==manifest['active_cluster']['sha256']
text=f'''# Handoff final — memória v380 e checks de contexto/gasto

[REAL — verificações locais encerradas; implantação pertence ao main]

Release científica: **v380**. Prefixo, cluster, fontes, catálogos, manifestos e scripts do build continuam congelados após a correção revisada. Nenhuma chamada remota adicional, leitura de credencial/configuração secreta, acesso ao razão real ou escrita em produção nesta verificação.

## Pins finais

| Artefato | SHA256 |
|---|---|
| Programa custodiado | `{count['source_sha256']}` |
| Cluster | `{count['cluster_sha256']}` |
| Haiku, {runtime['budget']['permanent_tokens']} tokens permanentes | `{count['draft_sha256']}` |
| Manifesto staged | `{sha(S/'manifest_staged.json')}` |
| Manifesto install | `{sha(S/'manifest_install.json')}` |
| Pacote Haiku runtime/manifest.json | `{sha(S/'haiku_runtime/manifest.json')}` |

Contagem real obtida pelo main: `{count_path.name}`. Entrada de referência **{count['budget']['request_input_tokens']}**, saída reservada **4096**, margem **1024**, folga **{count['budget']['remaining_tokens']}** na janela **200000**. `load_package` + `snapshot_from_manifest` reais validaram offline o pacote final; nenhuma nova contagem foi chamada. Não transferir essa medida aos tokenizers de outros provedores.

## Verificações concluídas

- **21 testes locais da memória** (11 integração + 10 codec), **56/56 da revisão independente**, **7/7 adicionais de orçamento/contexto**.
- 362 tópicos, v5 integral, núcleo anterior byte a byte com adendo atual, forma canônica integral e catálogo 1209/1209 fontes. Os 15 valores nos três mapas de vereditos novos estão inline no cluster/Haiku. Provas completas e detalhes referenciados continuam recuperáveis; contexto projetado não significa corpus inteiro inline nem instalação em pesos.
- `_chat_avaliacao`, `_automatic_budget_available` e `_chat_externo` do servidor proposto são AST-idênticos à produção para estas funções; os controles de OpenAI/Sonnet, chineses e Haiku não foram afrouxados pela integração v380.
- MiMo/DeepSeek/Kimi continuam recebendo o pacote Haiku verificado. MiMo/DeepSeek executam `check_window` sobre o corpo final em cada volta e reservam antes do HTTP; o Kimi verifica o JSON final encapsulado antes do cliente oficial. Nenhum prefixo foi truncado.
- O orçamento público de MiMo/DeepSeek reserva entrada sem cache pelo limite UTF-8 conservador + saída máxima. Recusa impede o HTTP; encerramento sem uso mantém a reserva inteira. A pré-seleção consulta exaustão com reservas ativas; a admissão definitiva continua sendo a reserva imediatamente anterior ao envio.
- Haiku usa a contagem nativa do pedido final e o grupo `haiku_public`; mantém margem de reserva financeira e de contexto. MiMo/DeepSeek usam seu razão/grupo existentes `mimo_public`, separado do Haiku. Isso preserva a política atual; não significa que esses gastos sejam um único grupo global.
- Nenhum teto novo para Luiz/MiMo/Kimi. Saldo e parâmetros financeiros reais não foram lidos: os testes usam cotas sintéticas e provam recusa/isolamento, sem declarar disponibilidade financeira da conta real.

## Payloads de referência medidos localmente

MiMo/DeepSeek: prefixo final + mensagem sintética + 14 ferramentas públicas/de tarefa. Kimi: prefixo + mensagem e recuperação sintética de 24000 caracteres Unicode. Os números abaixo seguem exatamente a fórmula conservadora de `check_window` (bytes JSON + reserva de saída + 4096), não contagem nativa desses provedores. Novos históricos, perfis, instruções de bancada ou resultados de ferramentas exigem o mesmo check a cada pedido.

| Provedor | Entrada UTF-8 JSON | Reserva de saída | Folga conservadora | Reserva USD calculada pelo código de referência |
|---|---:|---:|---:|---:|
'''
for provider in ('mimo','deepseek','kimi'):
    r=checks['provider_reference_checks'][provider]
    amount=f"{r['cold_hold_usd_reference']:.9f}" if 'cold_hold_usd_reference' in r else 'assinatura; política preservada'
    text+=f"| {provider} | {r['input_json_utf8_bound']} | {r['output_reserve']} | {r['remaining_conservative_bound']} | {amount} |\n"
text+='''
Os valores em USD são reservas conservadoras com as tarifas do código e saída máxima; não são faturas nem leitura de saldo. Orçamento inferior à reserva é recusado antes do transporte. O teste inicial teve uma configuração sintética incompleta para Haiku, corrigida no fixture; nenhum arquivo de runtime mudou.

## Recibos e integração

'''
for label,path in [('Entrega READY e mapa de 1224 arquivos',delivery_path),('Checks adicionais 7/7',check_path),('Revisão independente 56/56',review_path),('Contagem nativa real do main',count_path)]:
    text+=f'- {label}: `{path}`; SHA256 `{sha(path)}`.\n'
text+='''
O main já preparou `memory_stage/haiku_runtime`. Usar o mapa de instalação do recibo READY e `manifest_install.json`; o controller e sua integração são responsabilidade do main. O pacote não executa deploy nem altera contas/RAM. Não copiar backups/recibos antigos como ativos. Quiet, baseline, backups e validação ao vivo continuam no instalador principal.

Repetição autorizada somente offline: `C:/Python314/python.exe -X utf8 -B memory_build/test_provider_budget_context.py`. Não reexecutar o builder nem modificar bytes congelados sem novo achado e coordenação com o main. Orquestração global permanece separada.
'''
def save(path,data):
    raw=data.encode('utf-8')
    if path.exists():
        old=path.read_bytes();backup=path.with_name(path.name+'.bak_'+datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
        with backup.open('xb') as f:f.write(old)
        assert backup.read_bytes()==old
    temp=path.with_name(path.name+'.tmp')
    with temp.open('xb') as f:f.write(raw)
    assert temp.read_bytes()==raw and len(raw)>100
    temp.replace(path)
final=B/'FINAL_RELEASE_HANDOFF.md';save(final,text)
old=B/'HANDOFF.md';oldtext=old.read_text(encoding='utf-8')
addition='\n> Atualização final: contagem 181836 permanentes / 11570 livres e pacote runtime validado; 7/7 checks adicionais PASS. Consulte `FINAL_RELEASE_HANDOFF.md` e `delivery_20261002_115012_880732.json`. As pendências de recontagem descritas abaixo são o retrato anterior, preservado.\n'
head,rest=oldtext.split('\n',1);save(old,head+'\n'+addition+rest)
assert count['draft_sha256']==sha(S/'haiku_prefix.md') and count['cluster_sha256']==sha(S/'TGL_CLUSTER_v380.md')
print(json.dumps({'handoff':str(final),'bytes':final.stat().st_size,'sha256':sha(final),'prefix_still_frozen':count['draft_sha256'],'cluster_still_frozen':count['cluster_sha256'],'status':'FINAL_READY_NO_RUNTIME_EDITS'}))