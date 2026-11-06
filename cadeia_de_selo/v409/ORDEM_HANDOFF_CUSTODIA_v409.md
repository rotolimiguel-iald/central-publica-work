# ORDEM DE HANDOFF DA GERÊNCIA c1 À SESSÃO DE CUSTÓDIA — v409 SELADA (06/11/2026)

> Para a sessão de custódia (o papel que fez a custódia da v408 pelo G1). Escrita em arquivo porque, às 02h de 06/11, nenhuma sessão de custódia estava aberta nesta máquina. Vale a regra «custodiar sempre que o handoff aparecer»: as três marcas estão no Nós.

## A ordem do operador

- `OPERADOR_05nov_prossigamos_v409_concordo_com_os_nomes_verbatim.txt` (sha16 `8b9b77e992902ff4`): «Perfeito, é isso. Prossigamos para a próxima verão do um.py; concordo com todos os nomes que foram dados».
- `OPERADOR_05nov_tudo_na_v409_nada_para_a_v410_verbatim.txt` (sha16 `fb3dc69e3c9b5516`): «eu quero que entre tudo na versão 409 não deixar nada para a v410, senão roda isso, espera e faz tudo de novo pra rodar, gasto tokens de forma desnecessária».
- `OPERADOR_05nov_energia_caiu_de_novo_continue_ate_v409_publicada_verbatim.txt` (sha16 `209636842f72466d`): «energia caiu de novo, continue até termos a v409 publicada» — a ORDEM DE PUBLICAÇÃO desta versão (use este caminho em `--ordem`).
- A divisão de 04/11 (`OPERADOR_04nov_custodia_e_da_sessao_de_custodia_c1_so_um_py_verbatim.txt`, sha16 `2f91335e57a144e0`): a custódia inteira é da sessão de custódia; a c1 fica só com o um.py.

## O estado, lido em 06/11 por script

- Selo do Nós **v409** (timestamp 2026-11-06 00:40:06; `FAIL_CLOSED_SELFTEST_PASSED`; `RITO_RC=0`); `um.py` sha16 **`53284ba461ecd940`** (43970027 B); escada **12187/12187**; gate intocado (`TGL_QG_MODEL_FORMALLY_CLOSED__NATURE_TEST_COMPLETED_WITHIN_L…`).
- Rito 23:46–01:36 (05→06/11); pós-rito 0 → 14 OK; Bancada: B18 aplicado (evento 1491, hash `0cee635b5a77d5c4`), serviço religado.
- `Nós\HANDOFF_v409_CUSTODIA.md` (91452 B, sha16 `4e8dca197d007988`) com os sete textos e os parágrafos prontos; recibo `work\cadeia_de_selo\v409\pos_rito\RECIBO_TEXTOS_CUSTODIA_HANDOFF_v409.json` (sha16 `55974e8a9e53a1bd`); o portão do G1 rodou sobre o HANDOFF INTEIRO no S6d: limpo (D57c).
- O orquestrador da v409 NÃO tem S7 (G1 --publicar) nem S10 (release do app): pela D57, a cadeia termina no handoff; a custódia é sua.
- Revisão de terceiro: Sonnet, R3 aprovada (0 ALTO, 0 MÉDIO, 12 BAIXOS escritos) — `work\cadeia_de_selo\v409\revisao_terceiro\REVISAO_TERCEIRO_v409.json`.

## O que entrou (para a custódia saber o que publica)

Dois módulos de kernel: `TGLExt.TraducaoTuring` (a tradução das classes do dicionário às classes de Turing: P = nP no modo seleção, RELATIVO AO LEITOR; a trava no Nome; a fita é o hamiltoniano oculto; Z é o modo leitor e o psíon da luz o lê pela inscrição; uma leitura decide SAT; a máquina sem leitor é a fita sem escala; o Pai da Mentira; a identidade performada) e `TGLExt.ParNaFaceDeFock` (o par de psíons no setor 2 do Fock concreto, com a Meia-Nat na marginal — a ligação aberta desde a v407, fechada). Ressalvas ditas em todo texto: com o leitor que só conta, vale NP com uma leitura e a igualdade completa NÃO está provada (E28); a igualdade P = NP das máquinas de Turing do Mathlib não é decidida; Ω = uniforme como identidade está podada (a ponte é a inscrição); nenhum teste com a natureza; validade no kernel não é creditação; o gate não se move.

## O que é da custódia, na ordem

1. `custodiar.py planejar --versao v409 --seco` → `custodiar.py executar --versao v409 --publicar --ordem "C:\IALD\Central de Patentes\work\cunhagens_13out\OPERADOR_05nov_energia_caiu_de_novo_continue_ate_v409_publicada_verbatim.txt"` → `custodiar.py auditar --versao v409`. Nunca `--aceitar-molde`; não editar insumos.
2. A release v409 do app (C21): a ORDEM ao app no túnel `C:\IALD\TUNEL_CLAUDE_APP\` pelo molde da v408 (`work\cadeia_de_selo\v408\orquestrador\ORDEM_RELEASE_APP_TEMPLATE.md`, rótulos 408→409, placeholders lidos do selo e do git), com a D53 em vigor: no `shared` ficam em literal completo só a v409 e a v408; as anteriores viram tópicos regenerados. O reinício do serviço web é do operador, em uma linha.
3. Os dispositivos (16 FINAL), a Central, o site e os links pelo G1, e o commit e o push de tudo, com `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`.
4. A linha «HANDOFF v409 … PUBLICADA» no MEMORY.md é promoção da gerência: depositar na fila (`memoria.py depositar`) e avisar a c1.

## Notas

- `work\cadeia_de_selo\v409\insumos\` contém seis backups `.bak_*` da gerência (versões anteriores das pedras e do recibo; nada confidencial); eles estão listados no manifesto de incorporação do pós-rito (`pos_rito\v409_incorporacao_manifesto.json`) e por isso NÃO foram movidos. Se o G1 os levar ao espelho, é por esse manifesto.
- Os nomes `ParNaFaceDeFock` e os da R9 foram ratificados pelo operador em 05/11 («Ratifico os nomes», D62); as docstrings das pedras dizem «[DECLARADO] até a ratificação» como registro de época.

Validade no kernel não é creditação; `NOT_FALSIFIED` nunca é `CONFIRMED`; o gate não se move.

— gerência c1, 06/11/2026.
