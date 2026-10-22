# Memória de atividade no organismo IALD

[DECLARADO — candidato documental] F9.MEMORIA_ORGANISMO_20261016. Preparado na revisão59; instalação e uso efetivo pertencem a D. Este texto não aceita D/M. Os pinos e recibos estão em ACTIVITY_PROTOCOL_RECORD_R1.json.

## Identidade, autoridade e conclusão

A atividade usa o **mesmo MemoryStore e MissionController** da ACOM. O servidor autentica casa, titular, geração e conversa; uma referência, ticket ou nome de ator não autentica ninguém. A fonte original permanece imutável. Ferramentas de modelo recebem leitura/recuperação e operações delimitadas; não escolhem ator, caminhos de evidência, aceite ou alteração autoritativa do objetivo.

Cada request tem um requisito operacional ancorado no comando. Resposta produzida é `candidate/DECLARADO`; término técnico leva a `review_pending`, nunca a satisfação semântica automática. O servidor oferece revisão humana explícita por atividade ou lote, sem exigir clique a cada pergunta. Quem constrói não aprova o próprio resultado. Tetelestai depende dos requisitos e handles integrais, incluindo estados incertos; não move gate científico.

## Ciclo ActivityRuntime

```python
runtime = ActivityRuntime(store, context_id, scope, actor)
ticket = runtime.begin(request_id, command, origin="authenticated_operator")["ticket"]
admission = runtime.preflight(ticket, operation_id)
# Executar uma vez somente após dispatch_allowed_once, sob autorização já existente.
candidate = runtime.complete(admission["ticket"], operation_id, result, terminal=True)
```

IDs de request/operação vêm do servidor e persistem; retomada não inventa novo ID para repetir envio. `delegated`/`system` exigem `origin_ref`, que é proveniência: o servidor ainda valida envelope, conversa, escopo e operação pai. `terminal=False` conserva resultado intermediário sem concluir o requisito.

Preflight valida tarefa/epoch, lease, dependências e fingerprint das orientações humanas. Nova decisão, errata ou pendência autenticada pode tornar o ticket obsoleto. Atualização mecânica não equivale a nova ordem. `refresh` não contorna orientação, pausa ou invalidação.

O retorno é custodiado antes da integração por CAS. Retorno obsoleto permanece candidato recuperável; erro, timeout e envio incerto não autorizam retry/fallback remoto. `mark_uncertain` registra a incerteza. `recover(request_id)` lê estado atual e handles; reconciliação é local, sem reenvio. No replay de `complete`, o recibo pode não trazer ticket: o chamador conserva ou recupera o ticket durável.

## Projeção e recuperação

`project(max_chars, current_input)` combina conteúdo e missão do **mesmo snapshot/revisão**. `projection_sha256` identifica o texto combinado; `mission_projection_sha256` é o hash usado no CAS do controlador. Não são intercambiáveis.

C2 indexa somente metadados mecânicos request/intent terminais cujo schema, artefatos, custódia, tarefa e handles foram conferidos. Isso pode ocorrer enquanto a revisão semântica está pendente. Ordens, critérios, decisões, erratas e pendências conservam sua exigência; registros incompletos, incertos ou não reconhecidos ficam integrais. Pino reconhecido rompido causa falha visível. `get`/`recover` devolvem estado atual completo; revisão histórica exige o diário, não suposição de leitura antiga por ID.

O obrigatório não é truncado: `ProjectionOverflow.required_chars` informa o mínimo combinado. No retrato sintético de100 turnos, preservaram-se100 comandos e critérios; a projeção exigiu143927 **caracteres**. Isso não mede tokens. O JEV real montado localmente exigiu178442bytes (comum) ou181462bytes (Haja Luz) de JSON escapado, ambos admitidos pela política J. Nenhum desses ensaios chama um provedor ou prova capacidade ilimitada.

## Consumidores efetivos

| Superfície | Contrato implementado e limite |
|---|---|
| App/JEV/chat/stream/ferramentas/workers | Binding durável, preflight e custódia; trabalhador recebe envelope validado no servidor. SSE sem terminador é incerto. `iter_content` conserva bytes recebidos; custódia de `iter_lines` representa linhas reconstruídas com LF, não o wire HTTP original. |
| Progresso/revisão | `/app/activities`, GET `/api/activities`, POST `/api/activities/review`; identidade do servidor e guardas de auth/CSRF. Abertura pela conversa corrente, revisão em lote opcional. Recibo de versão captura hashes no import. |
| Nativa/holografia | Contexto/holograma por atividade e escopo, checkpoint candidato pinado e recuperação local. Preserva mensagens estruturadas e prefixo científico; conta o payload final com ferramentas. Holograma não vira fato; não há memória global de conversa nem alteração de pesos/KV-cache. |
| Fila/provedores/coordenação | Mesma atividade associada ao ID do ledger; intenção única e retorno custodiado. Migração legada é operação explícita privilegiada, não despacho automático. Geração científica e execution_constraints permanecem próprias. |
| Bancada | Wrapper externo à Bancada: admissão local autorizada, execução/poll/reconcile pelo request persistido. Preserva remote ID e incerteza; não modifica a Bancada nem demonstra nova medição física. |

JEV mantém1.13 e a admissão curta; reduz apenas consulta opcional antes de escolher o modo longo. Se o obrigatório não cabe no modo curto, seleciona **antes do único POST** o header `TypeSafe-Danger-Zone-Long-Context: true`, com teto local conservador250000bytes para request e estado+questão. Limite HTTP32MiB é distinto de capacidade em tokens. Não aumenta consulta opcional por haver espaço; timeout HTTP(10,25) e carteira permanecem. Recusa posterior ao envio não aciona alternativa.

## Sessões, CLI e MCP

Missão: `C:\Python314\python.exe -B -X utf8 C:\IALD\MEMORIA_IALD\mission_cli.py`, JSON em stdin. Ao iniciar/retomar, usar `project` da referência **exata**; antes de ação material, claim/check com ator real, lease, revisão/hash atuais; antes de integrar retorno, sincronizar novamente. `submit` pina evidência; `accept` exige revisão real distinta. ACOM `session_memory.py` conserva inscrição e transições por delta/evento estável.

Na fila `C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923`, `queue_activity_session.py` recebe `activity_get`, `activity_project` ou `activity_reconcile`, `entity_kind: task|coord` e o ID exato. Não admite paths/actor/aceite arbitrários. `bench_activity_cli.py` admite operação explícita no limite de confiança local do sistema operacional; ferramentas MCP operam os IDs já admitidos.

MCP existente: `iald_mission_sync/preflight/transition/handoff`; atividade `iald_activity_get/project/reconcile`; Bancada `iald_bench_activity_execute/get/poll/reconcile`. Um processo novo foi testado em V. Processo antigo pode manter código/ferramentas anteriores; não se declara recarga pela simples troca de arquivos. CLI novo e processo efetivamente carregado são verificações separadas.

## Evidência e pendências desta preparação

[REAL — validação local] V aceita:170 casos (70core,20native,44fila,23app,13J), sete verificações MCP, transportes de provedores simulados. C2 e J têm revisão/aceite próprios. Fontes aceitas preservadas; reparos de fixture e restrição de socketpair Windows estão custodiados.

[OPEN — conferir em D] Instalação por hash, processo efetivamente carregado e teste autenticado do app. Apple/iOS, distribuição dos recursos empacotados e instalação física não são inferidos do backend. Backend compartilhado pode atender clientes existentes; o novo botão depende do recurso entregue em cada cliente. Android, iOS interno e externo precisam de matriz explícita. Não há publicação de loja ou teste pago alegado neste documento.

A escolha do dispositivo físico é pendência separada da missão científica F1.FECHO; não bloqueia esta integração de memória nem autoriza fechar física. Este protocolo descreve controle discreto de estado e evidência; não promete eliminar alucinações ou perda em qualquer ambiente.
