[INPUT/DERIVED — contrato proposto, somente staging]
Missão própria: bcf544f7-1878-5d27-b532-f1e1aad466aa, project revisão 2 confirmado.

Entrada de iald_media_budget.plan_request: text_tokens_bound (TGL + histórico + ferramentas + ACOM completos, base64 excluído), output_reserve inalterado, context_limit, lista de metadados resolvidos/validados pelo backend do Cicero, rates explícitas, proposta FPS/resolução do JEV.

Metadados por mídia: id, kind audio/video/image, encoded_bytes (somente base64), decoded_bytes, sha256, duration_seconds quando áudio/vídeo, width/height quando imagem/vídeo. Vídeo também informa presença de faixa de áudio. Todas as mídias do histórico efetivamente transmitido entram; sem URL, base64, credencial ou acesso remoto no módulo de orçamento.

Transporte: teto por item 50_000_000 bytes de base64, aproximadamente 37_500_000 bytes decodificados; agregado separado e validado pelo host. Sem duração máxima arbitrária. Contexto, payload real e limites globais continuam decisivos.

Tokens: áudio ceil(duration_seconds * 6.25), com folga explícita adicional; vídeo usa estimador oficial local validado/pinado, faixa FPS 0.1..10 e máximo 2048 frames, max_frames default 300; sem copiar fórmula de memória. Vídeo/imagem sem estimador local conferido recusam orçamento, nunca assumem zero. Texto usa bound conservador independente; mídia nunca vira tokens por bytes UTF-8/base64.

Política: JEV recebe alternativas de FPS/resolução com estimativa de custo/contexto. Host valida parâmetros e reconta os bytes finais antes de dispatch. Não transformar, cortar, reduzir qualidade ou trocar parâmetros implicitamente. Ajuste de qualidade exige proposta explícita aprovada pelo fluxo do pedido; sem opção admissível, recusa com motivo e estimativa. Reserva de saída e memória jamais diminuem para caber.

Carteira: retornar reservation_usd estimada para a chamada completa, sob rates do host e sem presumir cache; chamador integra à reserva existente do ledger/wallet, não cria débito paralelo. Tarefa admitida conserva seu ciclo; orçamento não consulta saldo nem encerra tarefa por saldo negativo. Cotas globais e estado de envio incerto permanecem externos/preservados.

Saída: policy/version, text/media/slack/output tokens separados, contagens/identidades de mídia, parâmetros propostos, contexto total, reserva USD, estatuto ESTIMADO e motivo de recusa. Integração fornece contrato puro, sem I/O/rede. Dependência pendente: schema final dos metadados resolvidos e trecho/código oficial do estimador de vídeo em cache local do Cicero/coordenação. Esta frente não edita PROVIDERS.
