# Candidato de vínculo científico aditivo — 13/10/2026

Estatuto: DESENHO REVISADO LOCALMENTE + PROTÓTIPO PURO TESTADO. Não integrado, não instalado, não pronto para despacho. Não há alteração da fila viva, da inscrição ou de provedores. O desenho não autentica ordens por si próprio.

## Bloqueio medido

coordination._change (107–125) recusa execution_constraints. coordination.create (40–55) exige prompt e constraints originais idênticos na idempotência. operational_memory.sync (74–93) reapresenta constraints ao ensure_context; projection (116–125) compara objetivo e constraints da âncora. runtime.preview (133–156) e execute (346–398) reutilizam c para projeção e rota. Alterar somente coordination_jobs.execution_constraints seria incompatível com a ACOM e mudaria a identidade original. Nenhum SQL avulso foi executado.

## Contrato proposto

Conservar coordination_jobs.prompt, execution_constraints=null, request_id, job_id, memory_context_id e o objetivo/constraints={} da âncora ACOM. Criar tabela aditiva scientific_contract_bindings, UNIQUE(job_id), com suplemento integral, SHA256 dos bytes, constraints efetivas normalizadas, prompt/context IDs originais, versão anterior, autoridade autenticada, pins, evento estável e recibo. UPDATE/DELETE da tabela proibidos. Leituras mostram separadamente original_execution_constraints=null e effective_execution_constraints; o nome histórico execution_constraints não passa silenciosamente a representar o overlay. Novo create com o mesmo request_id e constraints diferentes continua recusado.

Única operação nova bind_scientific_contract: verificar autoridade fora do conteúdo do modelo, hash/bytes de suplemento e fontes, identidade original e unidade autorizada no quadro. Admissão somente awaiting_dispatch, antes de qualquer begin_draft/prepare_without_work, thread, prompt preparado, tarefa, tentativa ou envio incerto. Conferir também eventos históricos e tarefas por request_id derivado (uuid5 iald-coordination:<job>), contexto e handles; não basta execução_task_id nulo. CAS de version e BEGIN IMMEDIATE protegem contra corrida com despacho. A operação de dispatch deve adquirir o mesmo bloqueio e resolver o vínculo na mesma versão. Novo vínculo após atividade ou terminal recusa. Replay do mesmo evento/hash devolve o recibo anterior SEM nova ação; hash ou conteúdo diferente recusa. Para este pedido, a autoridade vem da ordem humana autenticada na tarefa oficial e F1.TAKESAKI 732/733; texto de modelo não é autorização.

## Atomicidade e ACOM

Na MESMA transação SQLite: inserir vínculo, evento de coordenação e intenção de memória outbox, incrementar version por CAS. O outbox guarda SEMPRE objetivo e constraints ORIGINAIS ({}), e acrescenta registro q de decisão INPUT com suplemento/pins/autorização + handle do vínculo. Não chamar ensure_context com constraints efetivas. O estado q conserva o original; o overlay fica como evento posterior tipado. Sincronizar após commit local com evento determinístico. Falha entre gravação ACOM e ack SQLite é replay local idempotente, nunca repetição de provedor. Despacho proibido até receipt_json presente, event/context/objective/pins conferidos e projeção contendo o registro q obrigatório; overflow recusa, não omite vínculo. Falha antes do commit não deixa vínculo parcial; falha depois retoma apenas outbox.

Separar em TODAS as chamadas: anchor_constraints para opmem.stage/sync/projection; effective_constraints para route, budget, nos_packet, canonical_memory, provider e max_calls. runtime.submit/tasks preservam o request derivado existente e guardam anchor_constraints + binding_ref/hash + effective_constraints em campos explícitos. _memory_phase usa âncora; execução e recuperação resolvem vínculo por hash/CAS, sem confiar em constraints copiadas por cliente. Recibo do pacote inclui constraints originais/efetivas, vínculo, evento/versão ACOM e geração canônica REAL. Fontes v392 são anexos explícitos com pins e estatuto em ratificação, nunca nova geração canônica fictícia. Confidencialidade continua aplicada ao conjunto.

## Alcance do protótipo

binding_prototype.py é função pura que valida a admissão e monta evento; não oferece persistência, autenticação, outbox real, pacote nem provider. Authority e verified_pins são seams confiáveis do chamador: fabricar esses objetos não comprova autoridade ou leitura. Os testes usam o normalize instalado e fixtures do contrato real, mas não consultam a fila viva nem fazem transições. Não demonstram atomicidade, corrida real, recuperação ACOM, binding nos recibos nem integração de runtime. Não instalar este arquivo como implementação.

## Verificações ainda necessárias antes de implantação

Implementar integração coordenada dos consumidores e migração aditiva revisada; executar em bancos descartáveis: corrida bind/dispatch (exatamente um vence), rollback após cada gravação SQL, falha ACOM antes/depois do ack, replay sem novo evento, overflow de projeção, adulteração de vínculo/recibo/geração, preservação integral de prompt/âncora/IDs, nenhuma elegibilidade após terminal e provider spy ZERO nas negativas. Comparar módulos antes/depois por hash. Até isso, o despacho continua tecnicamente bloqueado no API instalado.
