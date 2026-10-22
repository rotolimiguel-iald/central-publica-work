Contrato R1 — Cicero / coordenação; somente staging, missão bcf544f7-1878-5d27-b532-f1e1aad466aa

Correções ao CONTRACT_R0: saída é dinâmica 131072..16384; JEV automático está autorizado a escolher política por pedido sem confirmação humana adicional; 300 é DEFAULT_MAX_FRAME_TOKEN, não max_frames. Vídeo tem teto oficial de 2048 frames; fps padrão 2, resolução default ou max. Imagem legada permanece com bound UTF8/base64 conservador existente, sem novo estimador. Nenhuma mudança em retenção/consentimento/carteira é feita nesta frente.

1. APIs implementadas em `iald_media_budget.py`

```python
adapt_resolved_metadata(resolved) -> list[dict]
# resolved é EXATAMENTE o retorno autenticado de resolve_media_metadata(
# messages, store=store, scope=scope, provider='mimo', worker=False).
# campos Cicero: type='iald_media',media_ref,kind,mime,bytes,duration_seconds,
# sha256,width,height,has_audio,encoded_bytes_upper = base64_bytes + 128.
# adapter valida comprimento e retorna id/kind/sha256/decoded_bytes/encoded_bytes/
# duration_seconds/width/height/has_audio. Não autentica o browser por aparência.

resolved_options(full_body_preview, resolved, proposals, *, rates, **kwargs)
# -> {'standard': plan|{'status':'REFUSED','reason':...}, 'detail': ...}
# full_body_preview é o corpo completo de Evaluation._api ANTES da expansão:
# model/messages com prefixo TGL+histórico+ACOM INTEIROS/tools/thinking/etc.
# Não usar só client, prompt do JEV ou summary de request_media para contagem.
# proposals = {'standard': {'fps':2., 'media_resolution':'default'},
#              'detail': {'fps':2., 'media_resolution':'max'},
#              'motion': {'fps':5., 'media_resolution':'default'}}
# Não existe max_frames como parâmetro wire; não enviar esse campo à API.
# rates = {'input':host_rates[0], 'cache_read':host_rates[1], 'output':host_rates[2]}
# kwargs: intent_limits={'min_fps':..., 'require_max_resolution':bool},
# maximum_output=131072, context_limit=1048576,
# group_remaining_usd=None,provider_remaining_usd=None (metadados, não permissão).

admit_resolved(body, resolved, maximum=131072, window=1048576, *, rates,
               policy=None,intent_limits=None,group_remaining_usd=None,
               provider_remaining_usd=None) -> {
  'input_bound': int, 'output_reserve': int, 'text_utf8_bytes': int,
  'media_estimated_tokens': int, 'provider_http_bytes_upper': int,
  'estimation': str, 'media_budget': plan
}
# Substitui, NÃO soma, o estimador temporário de PrivateMediaRuntime.admit.
# Compatível com os nomes de retorno já usados pelo provider staging.
# Inclui margem estrutural 4096+128 no input_bound, mídia com +20% (mínimo256).
# Cada ocorrência no histórico é contada, inclusive mesma referência repetida.
# Sem duração máxima arbitrária. Sem corte, remoção de histórico ou redução de TGL.

reserve_existing(spending, compact_body, plan) -> existing_reservation_id
# Requer SPENDING_INTEGRATION.diff aplicado pela coordenação a app_spend.before.
# Chama spending.before('mimo',body,input_bound,media_plan=plan) UMA vez.
# Não chamar também o before antigo: seria reserva duplicada.
# Usa mesmo SpendingGuard/grupo/carteira, liquidação existente e idempotência.
# Sem nova admissão de tarefa, checagem de saldo ou interrupção por saldo negativo.

validate_video_wire_policy(expanded_body, plan['policy']) -> True | BudgetRefusal
validate_final_wire_bytes(len(actual_serialized_provider_json_bytes)) -> int | BudgetRefusal
# No momento imediatamente anterior ao POST: fps e media_resolution efetivamente
# enviados precisam corresponder ao plano; revalidar cada tool round.
# 64MB é limite do JSON real, separado de tokens. A estimativa não substitui esse check.

assert_private_media_destination(body,provider) -> True | BudgetRefusal
# Workers/TypeSafe/OpenAI/Kimi/DeepSeek/nativa não recebem refs/URLs áudio/vídeo.
# Lookup owner+generation+conversation, consentimentos MiMo2/Auto3, blobs/pins,
# decrypt e bloqueio de worker continuam sob o backend, não neste módulo puro.
```

2. Fluxo antes e depois do JEV

```python
# Host: cliente já autenticado/autorizado, nenhuma chave/rede.
resolved = resolve_media_metadata(client, store=store, scope=scope)
summary = request_media(client)  # Cicero/Hipatia acrescentam metadados verificados.
plans = resolved_options(full_body_preview, resolved, proposals,
                         rates=rates, intent_limits=intent_limits)
chosen, receipt = app_router.choose(summary['prompt'], candidates,
    media=summary, multimodal=bool(summary['kinds']), media_integrated=True,
    media_budget_options=plans, ...)  # argumentos existentes preservados
selected_policy = receipt['media_budget']['policy']
# configure explicitamente runtime.media_policy/intent_limits/rates pelo HOST.
# PrivateMediaRuntime.admit(body, maximum, window):
canonical_messages = runtime.canonicalize(body['messages'])
resolved = resolve_media_metadata(canonical_messages, store=store, scope=scope)
admission = admit_resolved({**body,'messages':canonical_messages}, resolved,
    maximum, window, rates=rates, policy=selected_policy, intent_limits=intent_limits)
plan = admission['media_budget']
body['max_completion_tokens'] = admission['output_reserve']
# Ledger: reservar UMA vez pelo caminho integrado (inclusive carteiras isentas
# mantêm os guards globais existentes), antes de expandir para um único POST.
if spending is not None: reserve_existing(spending, body, plan)
expanded = runtime.expand(body, provider='mimo')
# expand injeta os dois campos raiz em cada video_url conforme selected_policy.
validate_video_wire_policy(expanded,selected_policy)
validate_final_wire_bytes(len(serialized_wire_bytes))
# authorize_dispatch novamente; falha local => discard_undispatched existente;
# envio incerto => custodiar/recuperar sem retry. Somente então POST único.
```

Não precisamos canonicalizar mensagens de outros provedores para esse orçamento. A prévia deve reutilizar o builder real do motor; se ela não existe no ponto atual do servidor, criar callback local do builder antes de chamar choose, sem importar/executar ciência ou fazer chamadas remotas. Depois do JEV, recontar corpo completo com política já escolhida em cada rodada de ferramentas. Não executar JEV novamente para recontar contexto.

3. Recibo/retornos e métricas

`plan` contém version/status ESTIMADO, text_tokens_bound, media_tokens_estimate, media_slack_tokens, input_tokens_bound, output_reserved_tokens, context_total, policy, items por ocorrência, reservation_nanousd/reservation_usd, cache_basis, group_estimate_notices e fingerprint textual. Os campos de vídeo expõem sampled_frames/requested_frames/vendor_frame_cap_applied e dimensões estimadas; o cap oficial não é escondido. O host valida intenção (OCR/max/movimento) antes de oferecer uma opção. Nenhuma nova confirmação humana rotineira é necessária para a escolha automática autorizada.

O JEV recebe somente `routing_options(plans)`: números de contexto/custo, políticas e duração/dimensões/frames do histórico; sem referência opaca, sha, URL ou conteúdo. `route_instruction(receipt)` expõe política/custo/saída escolhidos, sempre estimados e sujeitos à recontagem final. Dados ricos podem ser acrescentados por request_media depois de lookup do store, nunca aceitos do cliente sem verificação.

`iald_routing_metrics.stamp(record,messages,media_plan=plan)` grava perfil de custo/resolução/frames completo sem blob; aceita typed refs. Comparação histórica de três amostras foi DESABILITADA para mídia nesta entrega: duração/resolução/frames ainda não são classes controladas. Texto mantém comparação antiga; mídia usa admissão separada. Sem transformar contagem de anexos em conhecimento de carga.

4. Dependências e limite desta frente

Providers/store/runtime/server continuam de Cicero/coordenação; este pacote não os edita nem instala nada. SPENDING_INTEGRATION.diff é snippet testado sobre método real sob guard simulado, não implantação. Não somar o estimador temporário do store com este estimador; usar apenas admit_resolved. A aproximação oficial tem uso final determinado pelo fornecedor; a margem adicional é política de engenharia explícita, não garantia matemática de cobrança/contexto. Cache não é presumido: acertos apenas após usage medido.

ADENDO R2 — caminho concreto de cliente antigo e Runtime atualizado

O staging atual do Cicero já chama `plan_request` diretamente e retorna o plano com `input_tokens_bound`/`output_reserved_tokens`, em vez dos aliases antigos de `admit_resolved`. Isso é correto: usar apenas essa chamada, sem somar outro estimador. `admit_resolved` permanece adaptador opcional; não é exigido se Runtime já possui `budget_metadata` no formato id/kind/sha256/decoded_bytes/encoded_bytes/duration/dimensões.

O exemplo executável está em `SERVER_GLUE_EXAMPLE.py`. Chamada concreta, apenas para o motor MiMo, antes do choose:

```python
from private_media_store import resolve_media_metadata
from iald_mimo_multimodal import validate_upload
from SERVER_GLUE_EXAMPLE import build_options

# wire e full_tools precisam vir do BUILDER REAL do motor: prefixo inteiro,
# ACOM/histórico inteiros, ferramentas admitidas e mesmas opções de thinking.
payload = dict(model='mimo-v2.6-pro', messages=wire, tools=full_tools,
               stream=True, stream_options={'include_usage':True},
               thinking={'type':'enabled'}, max_completion_tokens=131072)
resolved = resolve_media_metadata(wire,store=store,scope=scope,
                                  provider='mimo',worker=False)
items, budget_OPTIONS = build_options(
    full_body=payload, resolved_facts=resolved, validate_upload=validate_upload,
    rates={'input':spec['rates'][0], 'cache_read':spec['rates'][1],
           'output':spec['rates'][2]},
    proposals={
        'standard': {'fps':2.0,'media_resolution':'default'},
        'detail': {'fps':2.0,'media_resolution':'max'}},
    intent_limits=intent_limits)
summary = app_providers.request_media(client)
chosen,receipt = app_router.choose(summary['prompt'], candidates,
    media=summary,multimodal=bool(summary['kinds']),media_integrated=True,
    media_budget_options=budget_OPTIONS, ...)  # manter argumentos existentes
```

`resolved=[]` NÃO significa ausência de mídia: cliente antigo pode ter `input_audio`/`video_url` inline no histórico. `build_options` sempre soma `legacy_inline_metadata(payload['messages'],validate_upload=validate_upload)` ao resultado do resolver. O helper decodifica Base64 limitado, chama o decoder local do Cicero para validar MIME/assinatura/faixas/duração/dimensões e calcula pin dos bytes. Não usa metadados do navegador e não busca URL. Imagem legada/texto são ignorados pelo helper de áudio/vídeo e continuam no bound conservador de texto. Cada ocorrência histórica entra novamente no custo; nenhum dedup por hash omite consumo.

Vinculação de IDs: cada `iald_media.media_ref` em payload precisa corresponder a um `items[].id`, com a mesma modalidade; multiplicidade é preservada. Inline não tem media_ref e recebe id técnico `inline:<ocorrência>:<sha256>`, sem exigir lookup do store. `_slots` verifica que a quantidade/modalidade de itens corresponde exatamente às ocorrências no corpo. O backend continua responsável por pin/owner/dimensões confiáveis antes da expansão.

Na execução de cada tool round, o Cicero deve usar os MESMOS metadados combinados: `runtime.budget_metadata` para refs + `legacy_inline_metadata(body['messages'],validate_upload=validate_upload)` para inline. Chamar `plan_request` sobre corpo completo com `max_completion_tokens=maximum`, política selecionada e rates do host. Não retornar ao output_budget UTF8 puro só porque `contains_refs` é falso: inline também exige a admissão por modalidade. O detector do branch deve incluir input_audio/video_url no histórico, ou adotar a chamada única plan_request para MiMo com items combinados (lista vazia para só texto/imagem preserva o bound legado e saída dinâmica).

Durante expansão, referências viram dados inline; itens legados já são inline. Injetar fps/media_resolution escolhidos em TODOS os video_url, novos e legados; validar `validate_video_wire_policy` no corpo final e recontar bytes reais. Reservar exatamente uma vez pelo guard integrado. Não incrementar versão de consentimento: permanecem MiMo2/Auto3 já autorizados, sem autoconcessão e sem confirmação nova por plano automático.

Cobertura offline: cliente antigo somente áudio inline, mistura inline+typed refs, WAV real com `validate_upload` do staging do Cicero, imagem/texto legados sem novo estimador. A migração do cliente não é pré-condição para roteamento/admissão desses formatos antigos.
