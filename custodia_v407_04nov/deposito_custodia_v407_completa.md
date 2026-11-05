**Custódia v407 (04/11/2026, 15:24): COMPLETA.** G1 com C19, C20, C21 e C17C aplicados; `executar` rc 5 (o que é da G1 terminou; só restam decisões do operador); `auditar` rc 0 (0 números citados defasados, 0 rótulos errados).

**Como fechou [REAL]:**
- O app v407 foi instalado pelo orquestrador às 14:51–14:52 (janela de 34 s) depois do «Autorizo o reinício» do operador no chat; ORDEM 006 cumprida (`RESULTADOS\006_RESULTADO.json`).
- A custódia conferiu na fonte os quatro elos (`work\custodia_v407_04nov\conferir_recibo_app_v407.py`): INSTALLED_VERIFICATION PASS v407 (sha16 `e9199e03d96bd03f`); `jev_control` v407 sha16 `f2268cd01c699285` = o arquivo `canonical_releases\v407_bf9017157406\jev_control_v407.json`, com `source_sha256` = o pino; `iald_nucleo_fixo.json` com `current_release` v407 e `release_source_sha256` = o pino.
- O `DELIVERY_TECHNICAL_R1.json` da F0.3, no esquema do quadro, cita o `DELIVERY_v407.json` com o sha256 que está em disco (`753016234e685585`).
- O último DEFASADO do C19 foi a linha do HANDOFF v407 no MEMORY.md, promovida pela c1 às 15:22.
- Recibos: `work\custodia_G1\runs\v407_20261104_152329`.

**Para a c1, pela regra da ab-rogação de 04/11 (nada cumprido fica parecendo pendente):** a G1 lê como «decisões do operador abertas» o parágrafo «Pendências SÓ do operador» do `HANDOFF_v407_CUSTODIA.md`, l.92. Nele:
- o README pinado (D39) já foi ordenado pelo operador em 03/11 («chegou a hora de finalizaremos o readme como vc sugeriu pinado», verbatim em `work\cunhagens_13out\OPERADOR_03nov_…_verbatim.txt`) e está feito (`readme_pinado.py`, commit 907a65156);
- o mesmo verbatim de 03/11 traz «prossigamos com tudo, ratifico tudo»; se isso cobre D41–D47, é leitura sua;
- o teste (d) depende de poder medido, não de decisão nova (opção (c) dele já dada).
No handoff da v408, convém que a lista traga só o que segue dele: D2 [LEGAL], o conteúdo observável do motor contínuo (D45), o início de estimação em dado real do teste (d) se houver poder, e os atos de painel e depósito (iald.ia.br llms/sitemap/robots 404 desde 23/10; Zenodo em v401).

**Aviso do orquestrador para a v408 [DECLARADO pelo orquestrador]:** a folga mínima da janela P2 do `shared` caiu para 11.856 B (era 41.975 na v406); uma v408 do mesmo porte pede decisão de projeto da gerência antes do finalize. A autorização de reinício vale por versão.

**How to apply:** a v407 não volta à custódia. Na v408, o S10 do orquestrador deve rodar (se a cadeia parar antes, a custódia escreve a ORDEM com `renderizar_ordem`, como em 04/11). Relacionado: [[handoff-v407-custodia]] · [[licoes-cadeia-v407-04nov]] · [[orquestrador-e-o-app-claude-03nov]].
