**Custódia v407 (04/11/2026): PUBLICADA. C19, C20 e C17C esperam a release v407 do app (ORDEM 006).**

**Estado [REAL]:**
- v407 `833121339e649f71`. O espelho the_boundary `bf901715` e a Central `cc10b8f4` são iguais a origin/main.
- O site e a Central pública estão no ar.
- C15 (conferência final), C16 (PUBLICADA e rota `custodia.v407`), C17B (ACOM t2) e C18 passaram.
- `auditar` rc 0.

**O que parou e o conserto:**
- **C18 levou 7.386 s, cerca de 2 h** (3 repositórios, /central/ e um.acom). Quem retoma a custódia deve contar com isso antes de presumir travamento.
- **C19 parou com 4 DEFASADO.** Nenhum é falha de publicação:
  - (a) A F0.3 da v407 foi feita pelo orquestrador app, com recibo `DELIVERY_v407.json` de `estado` `ATIVADA_PELA_API_COM_CAS__CURRENT_EM_PROCESSO_NOVO`. O quadro (`estado_do_organismo.py`, l.253) só lê `DELIVERY_*R1.json` com `release`/`status ACTIVATED_VERIFIED…`, o esquema da fila do Codex. Pedi ao produtor o recibo no esquema do leitor (ORDEM 006, item 1), em vez de mexer no quadro: o arquivo tem uma alteração não commitada de outra sessão (o recibo do X diário).
  - (b) e (c) O contrato `jev_control_v407.json` e a Torre nascem com a release do app.
  - (d) A linha do HANDOFF v407 no MEMORY.md depende da promoção pela c1. Os depósitos `custodia_v407_*publicada*` estão em `depositos\claude-site\`, com aviso de 96% do teto de 24 KB.
- **O S10 do `pos_treino_v407` não rodou**, porque a cadeia parou em S7 e a c1 mandou não relançá-la. Por isso a custódia escreveu a ORDEM 006 com a função `renderizar_ordem` do próprio orquestrador, importada (o `main` é guardado), com versão, pino e commits lidos.

**ORDEM 006:** `C:\IALD\TUNEL_CLAUDE_APP\ORDEM_006_release_v407_do_app.md`, sha16 `0e832dc6eebc3ad6`, com um quadro de vigência do túnel do app.
- A ORDEM 004: §1 cumprida, §2 superada, §3 não se repete, §§4 e 5 superadas.
- As lições da v406 que ela leva: sai `_v402` da janela P2 (folga mínima declarada na v406: 41.975 B, DeepSeek); entra o F1 do parecer; o D4 é reescrito; os três campos são medidos e não lidos de constante; `quiet()` é conferido antes do reinício.

**How to apply:** quando o orquestrador devolver o RESULTADO 006, rode `custodiar.py executar --versao v407 --publicar` para C21, C19, C20 e C17C. O reinício da porta 8082 é do operador. Relacionado: [[licoes-cadeia-v407-04nov]] · [[handoff-v407-custodia]] · [[licoes-custodia-v406-03nov]].
