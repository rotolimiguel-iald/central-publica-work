# ORDEM DE HANDOFF DA GERÊNCIA c1 À SESSÃO DE CUSTÓDIA — v408 SELADA (05/11/2026)

> Para a sessão de custódia (o papel que fez a custódia da v407 pelo G1). Escrita em arquivo porque, às 05:3x de 05/11, a sessão de custódia não estava aberta nesta máquina (a única sessão viva da Central era a do gerente do LAR, que respondeu «não sou a custódia»). Vale a regra «custodiar sempre que o handoff aparecer»: as três marcas estão no Nós.

## A ordem do operador

Verbatim em `C:\IALD\Central de Patentes\work\cunhagens_13out\OPERADOR_04nov_ordem_v408_liste_as_pedras_produza_rode_handoff_custodia_completa_verbatim.txt` (sha16 `685b8d8bcf0ddbbd`): «produza a v408, rode e quando estiver completa, dê a ordem de handoff para a sessão irmã realizar a custódia completa e atualizar tudo (site, repositório, e todos os links), todos os dispositovos e a central de patentes e em seguida publicar, push e commit de tudo». E a divisão de 04/11 (sha16 `2f91335e57a144e0`): a custódia inteira é da sessão de custódia; a c1 fica só com o um.py.

## O estado, lido em 05/11

- Selo do Nós **v408 COMPLETO** (timestamp 2026-11-05 04:08:27, `FAIL_CLOSED_SELFTEST_PASSED`); `um.py` sha16 **`e7bc6b10e8ff76be`** (43.466.447 B); gate intocado.
- Rito 03:14–05:05, `RITO_RC=0`; pós-rito 0 → 14 OK; Bancada: B17 aplicado (evento 1473, hash `22fd56397613658d`), serviço religado.
- `Nós\HANDOFF_v408_CUSTODIA.md` (78.843 B) com os sete textos (`TITULO_EN_v408`, `ENTROU_EN_v408`, `KERNEL_LEITURA_EN_v408`, `ABERTOS_EN_v408`, `ARCO_EN_v408`, `ARCO_PT_v408`, `COMMIT_v408`) e os parágrafos prontos; recibo `work\cadeia_de_selo\v408\pos_rito\RECIBO_TEXTOS_CUSTODIA_HANDOFF_v408.json` (parser do G1 7/7, 0 problemas).
- `custodiar.py planejar --versao v408 --seco` → rc 1 (pronto; saída em `work\cadeia_de_selo\v408\orquestrador\g1_planejar_seco_c1_05nov.txt`).
- O orquestrador da c1 foi PARADO antes do S7 (custódia) e do S10 (release do app), porque os dois são da custódia.

## O que é da custódia, na ordem

1. `custodiar.py planejar --versao v408 --seco` (rc 1) → `custodiar.py executar --versao v408 --publicar --ordem "<o caminho do verbatim acima>"` → `custodiar.py auditar --versao v408`. Nunca `--aceitar-molde`; não editar insumos. O insumo do psíon no acervo foi pinado PURGADO na v408 (0 ocorrências na guarda), então a E03 não deve parar. Contar ~2 h no C18.
2. A release v408 do app (C21): a ORDEM ao app no túnel `C:\IALD\TUNEL_CLAUDE_APP\` pelo molde `work\cadeia_de_selo\v408\orquestrador\ORDEM_RELEASE_APP_TEMPLATE.md` (placeholders lidos do selo e do git), com a decisão **D53** da gerência sobre a janela P2 do `shared` (folga 11.856 B na v407): no `shared` ficam em literal completo só a v408 e a v407; as anteriores viram tópicos regenerados, sem compactar `the_iald_index` nem os literais `limites`/`diz`/`nao_diz` da corrente; se ainda não couber, o app MEDE e propõe o teto antes do finalize. O reinício do serviço web é do operador, por versão, em uma linha.
3. Os dispositivos (16 FINAL), a Central, o site e os links pelo G1, e o commit e o push de tudo, com `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`.
4. A linha «HANDOFF v408 … PUBLICADA» no MEMORY.md é promoção da gerência: depositar na fila (`memoria.py depositar`, pasta = quem, `tipo` obrigatório) e avisar a c1. O MEMORY.md tem folga (22.910 B).

## As «decisões do operador abertas» que o G1 lista no handoff

A correção pública da ressalva do X de 04/11 JÁ FOI FEITA (o operador apagou o post errado; a IALD republicou às 19:44: https://x.com/rotolimiguel/status/2118112166343745858). D48–D54 são da gerência e estão aplicadas; os quatro nomes foram ratificados pelo operador («Excelente, ratificado. Prossigamos», sha16 `388edbab08d0babc`). D2 [LEGAL] e o README pinado (D39) seguem como na v407. Nada disso trava a custódia.

Validade no kernel não é creditação; `NOT_FALSIFIED` nunca é `CONFIRMED`; o gate não se move.

— gerência c1, 05/11/2026.
