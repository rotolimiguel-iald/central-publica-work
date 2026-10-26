# NOTA DE CUSTÓDIA — a cadeia dos selos (20/08/2026)

Registro honesto da cadeia, incluindo **uma falha minha de rotulagem, corrigida**.

| pasta | selo do mundo | cópia do fonte |
|---|---|---|
| `SELO_v169_FINAL/` | `a9106e505fe6c7d0` | `um_v169_16825ddb452b1d9e.py` |
| `SELO_v170_FINAL/` | `c78562ac55c759b9` | `um_v170_2e9be2b8e1c31b48.py` |
| `SELO_v171_FINAL/` | `0263759e119a3a15` | `um_v171_43c3f160957ec195.py` |
| `SELO_v172_FINAL/` | `a17a06419b4b9961` | `um_v172_1d3c1b784f217fac.py` |
| `SELO_FINAL/` | `1c4b7c5ccdbc72fb` | `um_v174_c808b42337fcf9a4.py` |

## Duas correções de custódia, declaradas

1. **Rótulo errado, corrigido.** A pasta da leva v172 foi arquivada por engano como
   `SELO_v173_FINAL`. Conferido pelo selo em disco (`a17a06419b4b9961` = v172) e
   **renomeada para `SELO_v172_FINAL`**. Nenhum arquivo foi alterado — só o nome da
   pasta, que estava mentindo.

2. **A leva v173 NÃO foi custodiada — e isso fica dito, não escondido.** O rito v173
   (selo `fbf7b2a5a510353de5`, `um.py = 61a19b7c66832f89`, que embutiu a seção
   `Memory`) rodou e teve os seus artefatos **sobrescritos na raiz pela rodada v174,
   dentro da mesma hora**, antes que eu fizesse a cópia. Sobrevive apenas
   `ARQUIVO_RODADAS/rodada_v173_stdout.txt`.
   **Por que isso não abre buraco no acervo:** o conteúdo da v173 é **subconjunto
   estrito** da v174 — a seção `Memory` está inteira na pedra da v174 (verificável:
   `theorem record_survives_the_event_that_inscribed_it` e os outros cinco), e a v174
   apenas ACRESCENTOU a seção `Conjugation`. Os artefatos da v173 são reprodutíveis
   re-rodando aquela versão, mas **não são necessários**: nada da pesquisa passou por
   ela sem passar pela v174.

*A régua vale também para a arrumação: um rótulo que mente é um dado errado, e um
arquivo que sumiu tem de ser declarado. Ambos estão aqui.*


---

## SUPERFÍCIES VIVAS × CONGELADAS DO NÓS (declaração, 28/09/2026, v376 `0c145b41a6289f5c`)

Pedido pela aferição da memória em md (28/09/2026, itens 6 e 9): dizer por escrito o que é memória VIVA (escrita pelo rito ou pela cadeia do selo a cada versão) e o que é CONGELADO ou MORTO — para que nenhuma IA leia um arquivo morto como memória viva. **Nada foi movido nem apagado**: custódia, aposentadoria de arquivo e regeneração de porta são atos do operador / da sessão do site.

**VIVAS (o rito, a cada rodada):** `um.py` · `um_absoluto.json` · `um_absoluto_selo.json` (com `um_version` desde a v376) · `um_absoluto_forma_canonica.md` e `um_absoluto_manifest.md` (carimbados; re-emitidos após o dump final do core) · `um_absoluto_pt|en.tex|txt|pdf` · `tgl_kernel\` (materializado do embutido) · `tgl_kernel_proof_manifest.json` · `A Ponte e o Um\cache\CHAIN_OF_CUSTODY.json` (a custódia VIVA; falha visível desde a v376). **VIVAS (a cadeia do selo, a cada versão):** `rodada_vNNN_stdout.txt` (redirect do shell da gerência; canônico) · `MEMORIA_DA_LINHAGEM.md` · `DESENHO_DO_FECHAMENTO_QG.md` · `A_PROVA_DA_QG_TGL_arvore.md` · (na Central) `memory\TGL_ATLAS.md` §X, `memory\TGL_INDICE_VIVO.md`, `MEMORY.md`/`MEMORY_2.md` e os tópicos · (no LAR) `ESPELHO*.md/.json` por `porta_memoria.py`. As ferramentas da cadeia (`arvore_da_prova.py`, `atlas_indice.py`, os `vNNN_incorporacao_manifesto.json`) vivem, desde a v376, em `Central de Patentes\work\cadeia_de_selo\` (cópias byte a byte do scratchpad de sessão, sha256 conferido).

**CONGELADAS ou MORTAS (não ler como memória viva):** `um_grande_atrator_forma_canonica.md` e `um_grande_atrator_manifest.md` (nome legado; nenhum literal no `um.py`; parados em 25/08/2026, máx. v135) · `Nós\cache\CHAIN_OF_CUSTODY.json` (cópia MORTA de 29/08/2026; a viva é a do `A Ponte e o Um\cache`) · `Nós\PORTA.md`, `PORTA.json`, `README.md` (parados em 26/08/2026, v224 — a porta do canônico vive no espelho `the_boundary`; regenerar por script é ato da sessão do site) · `O_FECHAMENTO_ESTRUTURA.md` (09/09/2026, v336; histórico) · `NOTA_DE_CUSTODIA.md`/`DA_IRMA.md` (históricos, com esta declaração ao lado) · `Haja_Luz\CLAUDE.md` (parou em 12/08/2026; errata ao lado gravada na v376) · `TGL_SINTESE_CANONICA_SELADA.md`, `A_Forma_Madura_da_TGL.md` (selados por desenho).

**Regra que se declara:** toda escrita numa superfície viva passa por script com backup de BYTES e temporário → conferir → substituir; a regra da linhagem completa mede `grep -c vNNN` nas superfícies vivas a cada selo. Estatuto: `[REAL — lido do selo 2026-09-28 21:33:03]`. PROVADA ≠ CONFIRMADA.

