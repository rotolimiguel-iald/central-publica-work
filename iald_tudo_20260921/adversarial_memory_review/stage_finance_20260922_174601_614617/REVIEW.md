# Stage Claude — mudanças necessárias

## P1 S1 — Haiku gratuito anunciado disponível, mas cota global do grupo é sempre zero

Regressão de integração: gratuito agora admitido, configuração legada ainda o proíbe.

Evidência: `{"option_available": true, "group_cap": 0.0, "zero_usage_denial": "global_gratuito", "plan_daily_usd": 0.02, "factor": 1.6}`

Correção: Definir política financeira Haiku explícita e autorizada (grupo e plano), validá-la antes de anunciar disponibilidade; não remover o guarda. O plano herdado de US$0,02 também é inferior à entrada fria de uma memória de180k tokens com as tarifas configuradas.

## P2 S2 — Contagem nativa não alimenta reserva nem liquidação sem usage

Estimador legado preservado apesar da nova medição; perda de consistência financeira na integração.

Evidência: `{"synthetic_native_input": 184609, "legacy_estimate_before_factor": 180000, "factor": 1.6, "reserved_input_estimate": 288000, "reserved_usd": 0.43448, "same_formula_using_native_usd": 0.28585625, "missing_usage_quota_tokens": 146800, "native_input_minus_prefix": 1474, "limitation": "Fixture isolation of legacy accounting. Not a provider count or incurred cost; do not merely set factor1 on an o200k estimator."}`

Correção: Propagar medição nativa do mesmo payload para reserva e fallback de entrada por chamada, inclusive voltas de ferramenta. Não multiplicar uma medição nativa por fator o200k; manter reservas separadas de saída ambígua.

## P2 S3 — Rota de contexto devolve janela legada e falha sem resposta controlada ao indisponibilizar Haiku

Nova configuração pode levantar; chamada e regra32k antigas preservadas.

Evidência: `{"context_route_window": 32768, "selected_profile_window": 200000, "package_unavailable_exception_escapes": true, "no_remaining_dynamic_field": true}`

Correção: Responder perfil Haiku medido com unidades e saldo dinâmico explícitos; tratar indisponibilidade como fazem /api/motor e active-model.

## P2 S4 — Hash medido das ferramentas não é conferido no stage

Obrigação de integração antes pendente não implementada.

Evidência: `{"declared_tools_hash": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", "changed_tools_forwarded": true, "tools_hash_checks_in_stage": 0, "security_scope": "No private-tool execution demonstrated; breaks pinning to reviewed tool schema. Native recount still protects token window."}`

Correção: Conferir hash canônico do schema efetivamente enviado contra o manifesto, ou versionar explicitamente subconjuntos permitidos; divergência deve ficar visível e impedir anunciar pacote íntegro.

13 testes fornecidos passaram. Fragmentos AST e classes financeiras testados isoladamente; teste completo_chat_externo não duplicado. Sem rede, API, dados privados ou escrita em produção. Hashes e limites em review.json.
