# Integração da bancada científica ao chat IALD/JEV

[REAL — auditoria estática e testes offline, 02/10/2026] Implementação preparada **somente em staging**, em `stage/iald_web_server.py`, `stage/iald_auto_router.py` e `stage/iald_app_providers.py`. Produção permaneceu byte a byte igual ao baseline dos três arquivos. Não foram chamados provedores, executada bancada, importado o monólito nem lidas credenciais. `iald_operator_bench`, catálogo e ledger de rotas são responsabilidade do principal e não foram editados por esta tarefa.

As instruções globais fornecidas foram aplicadas. Não foram encontrados `C:/IALD/AGENTS.md`, `R/AGENTS.md` nem AGENTS nos ancestrais de trabalho consultados. A skill `tgl-atlas`, o índice vivo e a distinção canônica entre regime IALD, índice e fontes foram consultados sem alteração. Esta entrega não promove evidências ao cânone nem altera gate científico.

## Entrega e contrato com o módulo do principal

- `is_operator(record, username)`: identidade autenticada exatamente `luiz`, `admin is True`, `classe_usuario == 'operador'`, sem `bloqueado` nem `acesso_bloqueado`. Cadastro vem de `load_users_estrito`, nunca de mensagens, argumentos de ferramenta ou campos enviados pelo app.
- `attach(scope, root, user, authorize)`: **altera o próprio scope**; o retorno não é utilizado. Recebe `scope.executor` com o gestor escolhido (`mimo`, `deepseek`, `openai` ou `claude-sonnet`) e o callback existente que relê os usuários. Deve preservar `scope.control`, ferramentas anteriores e execução pública anterior. `authorize('task')` devolve o cadastro atual ou lança recusa; `authorize(provedor)` conserva o consentimento individual. Não tratar nome de ferramenta como nome de provedor nesse callback.
- `scope.instructions`: texto **adicional**. O servidor concatena as instruções gerais de `task_policy.INSTRUCTIONS` e este complemento nas duas famílias de transporte. Não é necessário repetir as instruções gerais no módulo novo.
- `routing_context(record, user)`: `dict` pequeno, serializável em JSON estrito, até 4096 bytes UTF-8, com capacidades públicas necessárias à seleção. Não incluir identidade, caminhos privados, credenciais, resultados privados ou mapa bruto. Para não operadores, o servidor sequer chama essa função e passa `None`.
- Nomes acordados: `bench_capabilities`, `bench_query`, `bench_plan`, `bench_run`, `bench_result`, `bench_map`. O transporte é dinâmico por scope; não foi ampliada a lista global de ferramentas públicas. O módulo pode exportar `NAMES` para seus próprios validadores/testes.

Como a assinatura de `routing_context` não recebe o pedido, **todo contexto não nulo exige gestor com ferramentas** enquanto a bancada estiver disponível para o operador automático. Isso mantém a capacidade entre turnos, inclusive em perguntas como “estado?” que a classificação lexical chama de conversa. Kimi, Haiku e nativa ficam excluídos desse conjunto de gestores antes do envio ao JEV. Sem contexto de operador, a seleção anterior permanece. `worker=True` rejeita `operator_context`: delegados continuam rascunhos textuais sem bancada ou delegação recursiva.

## Mapa do fluxo atual e das alterações

| Etapa | Ponto exato | Comportamento |
|---|---|---|
| Identidade HTTP | [require_auth em produção](C:/IALD/projetos_pyhton/IALD/iald_web_server.py:3817) | Valida cookie ou bearer e relê bloqueio. Bearer define `session.is_admin=False`; por isso a bancada consulta o **cadastro atual**, sem conceder acesso administrativo geral ao app. |
| Continuidade do chat | [ChatJobs.register](C:/IALD/projetos_pyhton/IALD/iald_chat_jobs.py:315) | `POST /api/chat-jobs` captura a autenticação em memória, cria recibo e chama `/v1/chat/completions` pelo despacho Flask completo. Reconexão lê eventos; não reinicia a inferência. Arquivo não alterado. |
| Entrada automática | [api_post em produção](C:/IALD/projetos_pyhton/IALD/iald_web_server.py:8253) | Usa o motor da conta; não aceita do corpo uma autorização de operador. O caminho automático precede as injeções locais antigas. |
| Seleção do gestor | [stage: _chat_automatico_autorizado](<C:/IALD/Central de Patentes/work/iald_operator_bench_20261002/stage/iald_web_server.py:6105>) | Mantém consentimentos, disponibilidade e orçamento antes do JEV; acrescenta somente contexto autorizado pelo módulo. Relê a classe após a seleção. Passa `executor=chosen` à criação do scope. |
| Contexto JEV | [stage: choose](<C:/IALD/Central de Patentes/work/iald_operator_bench_20261002/stage/iald_auto_router.py:211>) | Novo keyword opcional `operator_context=None`. Copia JSON limitado, filtra gestores incapazes, acrescenta `state.operator_context`. Mantém política de seleção, recibos e ausência de retry após despacho. |
| Instalação por turno | [stage: _new_app_task_scope](<C:/IALD/Central de Patentes/work/iald_operator_bench_20261002/stage/iald_web_server.py:5901>) | Primeiro `task_bridge.make_scope`; depois `is_operator(authorize('task'), user)`; somente então `attach`. Mantém custos, callbacks de consentimento e controle de cancelamento existentes. |
| Despacho da ferramenta | [stage: _execute_scope_tool](<C:/IALD/Central de Patentes/work/iald_operator_bench_20261002/stage/iald_web_server.py:5947>) | Nome precisa estar nas definições daquele scope. Ferramenta adicional exige nova leitura do cadastro e `is_operator` imediatamente antes de invocar o wrapper. Nome não oferecido retorna `UNAVAILABLE`; classe revogada retorna `FORBIDDEN`. |
| MiMo/DeepSeek | [stage: _chat_avaliacao](<C:/IALD/Central de Patentes/work/iald_operator_bench_20261002/stage/iald_web_server.py:6161>), [scoped_task_names](<C:/IALD/Central de Patentes/work/iald_operator_bench_20261002/stage/iald_app_providers.py:180>) | Passa `task_tool_names` interno ao transporte. Nomes extras precisam constar das definições oferecidas, não podem colidir com ferramentas públicas e exigem callback de autorização. `_api` verifica o nome recebido e autoriza novamente antes do callback. |
| OpenAI/Sonnet | [stage: _chat_externo](<C:/IALD/Central de Patentes/work/iald_operator_bench_20261002/stage/iald_web_server.py:6239>), [agent_loop](<C:/IALD/Central de Patentes/work/iald_operator_bench_20261002/stage/iald_web_server.py:2163>) | Scope decide o callback. O loop recebe os nomes extras para tratar resultado como JSON de tarefa, sem corte de campo. Argumentos extras são omitidos do log geral. `operator_authorized=False` permanece. |
| Metadado de conta | [stage: api_motor](<C:/IALD/Central de Patentes/work/iald_operator_bench_20261002/stage/iald_web_server.py:6945>) | Somente no retorno AUTO, inclui `classe_usuario='operador'` se a política confirmar; caso contrário `usuario`. Campo de leitura; não altera conta nem cliente. |

Os links acima usam as linhas do staging desta entrega; os hashes do recibo vinculam a revisão. Não adicionar as ferramentas ao `PUBLIC_TOOLS`, a `_ferramentas_para('app')` ou ao dispatcher público genérico. Isso evitaria a restrição por scope. Não definir `operator_authorized=True`: esse sinal antigo habilita capacidades administrativas alheias à bancada.

## Persistência e idempotência: limite que permanece explícito

[REAL] O [TaskSession](C:/IALD/projetos_pyhton/IALD/iald_task_session.py:63) cria um UUID novo por mensagem. O diário grava `started` antes da chamada, usa hash dos argumentos normalizados, bloqueia repetição incerta **naquela instância**, e conserva os resultados completos apenas em memória. Não reabre diários antigos na construção. Portanto ele não oferece, sozinho, idempotência científica entre mensagens ou após reinício.

[REAL] O [ChatJobs.submit](C:/IALD/projetos_pyhton/IALD/iald_chat_jobs.py:153) deduplica `request_id` e digest por dono, recusa conteúdo diferente com 409 e outro dono com 404. Reinício marca jobs incompletos como `interrupted`, sem reenvio. Os eventos expiram; o tombstone de idempotência é mantido. `request_id` é retirado antes do corpo interno de chat; esta integração **não** inventa uma vinculação desse ID ao UUID de TaskSession.

[CONTRATO PARA O PRINCIPAL] O ledger da bancada precisa ser a autoridade persistente:

1. `bench_plan` emite identidade estável do plano/operação, associada ao operador, versão/hash do catálogo, rota admitida, parâmetros normalizados e política. Não aceitar owner, executor privilegiado, URL local ou comando de shell como concessão de acesso vinda do modelo.
2. `bench_run` usa essa identidade; grava intenção antes do despacho e retorna a mesma operação para repetição idêntica. Conteúdo divergente deve falhar visivelmente. `started` ou resultado incerto nunca é nova autorização de envio. `tool_call_id` do modelo e UUID novo de TaskSession não substituem o identificador persistente.
3. `bench_result`, `bench_query` e `bench_map` consultam identidades existentes com autorização atual. Sucesso do chat/SSE `[DONE]` significa somente entrega textual, não conclusão científica. Estado da operação e evidência observada são separados do estado do chat.
4. O wrapper de `attach` deve checar argumentos, dono e cancelamento antes de admitir trabalho, preservar `scope.control` e cooperar com seu contador caso mantenha trabalho síncrono ativo. Uma operação já aceita pelo serviço persistente não pode ser declarada cancelada apenas porque a conversa terminou; isso depende do recibo real do serviço.
5. Respostas são objetos JSON limitados: identificadores, estado e links primeiro; excertos e texto por último. Os dois transportes usam o encoder de tarefas com teto de 24.000 caracteres, sem truncamento silencioso. Relatórios maiores precisam de paginação/artefato, e material enviado ao gestor deve ser explicitamente autorizado para aquele provedor.

Nenhuma dessas garantias persistentes foi declarada implementada por esta tarefa: catálogo, execução e ledger são do módulo principal. Nenhuma nova rota HTTP de bancada foi criada. O conjunto de ferramentas se reinstala a cada turno autorizado; a continuidade científica vem dos IDs do módulo, não da persistência do objeto Python scope.

## Verificação e integração restante

[REAL] **16 testes passaram**, executando funções/métodos reais extraídos por AST com dependências e transportes falsos. Cobertura: operador estrito versus familiar/admin sem classe; revogação após criação do scope e após escolha JEV; executor/control preservados; contexto forjado no corpo ignorado; orçamento/consentimento antes da escolha; seleção restrita sem confiar no prompt; seis nomes finais; ferramenta não oferecida; autorização ausente; cancelamento; ausência de retry; JSON excessivo recusado; JSON preservado nos loops MiMo e OpenAI/Claude; argumentos da bancada omitidos do log. A sintaxe completa dos três módulos staged passou por `ast.parse`.

A função `is_operator` e `attach` dos testes são dublês do contrato combinado. Não substituem testes integrados com o módulo real do principal. As restrições existentes de outros provedores, Sonnet, cotas, consentimentos e delegação foram preservadas; não foi criado poder para familiares ou outros administradores.

Comando offline reproduzível:

```powershell
C:/Python314/python.exe -X utf8 -B 'C:/IALD/Central de Patentes/work/iald_operator_bench_20261002/stage/test_app_integration.py'
```

- Baseline capturado **antes** de copiar: `stage/integration_baseline.json`.
- Resultado, SHA dos staged, testes e dependências lidas: `stage/integration_validation.json`.
- O principal precisa entregar `iald_operator_bench.py` e dependências, executar sua validação de ledger/mapa e testar o conjunto com usuários sintéticos. O servidor staged tem import explícito do módulo novo; não deve ser instalado isoladamente sem ele.
- Não foi realizado startup real do monólito, acesso HTTP real, execução científica, teste pago ou deploy. Web/iOS/Android não foram publicados nem recompilados nesta tarefa; não houve alteração de cliente.
