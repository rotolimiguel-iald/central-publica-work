# PEDIDO DE CORREÇÃO R1 — revisão de terceiro da v409 (Sonnet, 05/11/2026)

Candidato revisado: `um_v409_candidato.py` sha16 `eab2d12055b47df0` (lido ao abrir e ao fechar; não mudou). Resultado: `aprovada: false` — **0 ALTO, 1 MÉDIO, 10 BAIXO** (`REVISAO_TERCEIRO_v409.json`). O que passou está em `REVISAO_TERCEIRO_v409.md`; abaixo, só o que trava.

## MÉDIO 1 — o par na face de Fock aparece [OPEN] em texto novo, contra o próprio registro e contra o item (d)

Em três lugares de texto NOVO o par na face de Fock (e a identidade Ω = uniforme) ainda aparece como [OPEN], embora o kernel o ligue (`TGLExt.ParNaFaceDeFock.o_par_na_face_de_fock`, que compilei no trio) e o registro, o artigo e o handoff digam «ligado nesta versão» e «identidade podada». A guarda de frases não pega nenhum dos três (provado por `t5_guarda_probes.py`).

| # | onde (fonte e montado) | texto atual | o que deve ficar |
|---|---|---|---|
| 1 | `registros_v409.py:162-163`, `_V409_TRADUCAO_TEXT['estatuto']` (embutido no candidato; vai ao core, ao Atlas, ao core memory, ao HANDOFF e ao **cabeçalho do parágrafo pronto do README/site**) | «… [OPEN] o par na face de Fock como ligacao; o Omega do psion = o uniforme; a independencia de P vs NP dos axiomas; o teste com a natureza» | «… [REAL] o par na face de Fock LIGADO (ParNaFaceDeFock); PODADA a identidade de vetores Omega = uniforme (a ponte e' a inscricao); [OPEN] a independencia de P vs NP dos axiomas; a igualdade com o leitor que so' conta (E28); o teste com a natureza» |
| 2 | `pos_rito/textos_v409_novo.pysnip:282` (função `_respostas`) e o montado `pos_rito/textos_v409.py:1091` | «O que NÃO decide: … nem o par na face de Fock, que segue [OPEN].» | «… nem que o par finito de Bell e o par de Fock sejam o mesmo objeto (espaços distintos, a MESMA Meia-Nat); o par na face de Fock está ligado nesta versão.» |
| 3 | `pos_rito/textos_v409_novo.pysnip:499` e o montado `textos_v409.py:511` (bloco `[OPEN] …` do core memory) | «[OPEN] A discriminação a 5σ …, o par de psíons na face de Fock (ligação), o Ω do psíon da luz como o uniforme da instância, a independência …» | tirar da lista [OPEN] «o par de psíons na face de Fock (ligação)» e «o Ω do psíon da luz como o uniforme da instância» (o par está ligado; a identidade Ω = uniforme está podada, a ponte é a inscrição). A lista [OPEN] do handoff (`handoff.txt`) já está certa; alinhar o core memory a ela. |

**Guarda (para não voltar):** estender a F41 (`_v409_guarda_frases` em `runtime_v409.py` e o espelho em `guarda_frases_v409.py`) para reprovar `[OPEN]`, «em aberto» ou «segue aberto» a até ~80 caracteres de «face de Fock» / «Fock face» / «ParNaFaceDeFock» (com a exceção das citações da errata E21 e do histórico «o [OPEN] da v407»), e a F40 para reprovar «Ω … uniforme» dentro de lista [OPEN]. Acrescentar ao controle negativo as quatro sondas que passam hoje: `nem o par na face de Fock, que segue [OPEN].` · `[OPEN] o par na face de Fock como ligacao;` · `[OPEN] o Ω do psíon da luz como o uniforme da instância` · `a ligação do par de Fock segue em aberto`.

**Consequência de processo:** o item 1 está no candidato, então o candidato muda de sha16. Regenerar candidato, ESPERADOS, ensaio a seco, harness dos textos, PRONTA; rodar a R2 sobre o novo sha16. Os scripts desta pasta (`a_intocados*.py`, `a2_mudados.py`, `d_kernel.py`, `c_fail_closed.py`, `k_funcoes_vivas.py`, `h_guardas.py`, `e_citacoes.py`, `f_hashes.py`, `l_orquestrador.py`) rodam sem edição se os nomes de arquivo não mudarem; o Lean não precisa ser refeito (nenhuma pedra muda).

## Aproveitar a mesma regeneração (BAIXOS, não travam)

- `_paragrafo_v409_de` (`textos_v409_novo.pysnip:629-633`): índices fixos de `diz` trocaram os marcadores do parágrafo pronto do README/site (o «O dicionário de Turing» traz a D61; «A trava no Nome» traz a máquina com o leitor; «O que não muda» traz o dicionário). Buscar o item pelo conteúdo.
- Redação «a igualdade completa SÓ para o leitor que se lê» / «holds ONLY for the reader that reads itself» → «está estabelecida (BGS 1975) para o leitor que se lê; com o leitor que só conta não está provada».
- `cunhagens_v409` u1 («as 17 checagens») e a docstring de `v409_traducao_mechanics` («62 âncoras», «17 checagens») → 20 e 82.
- Opcional: F44 contra «igualdade vale … leitor que só conta» sem negação e contra o EN curto «Clay resolved».

## O que NÃO precisa mudar

Kernel e pedras (82 âncoras no trio, 223 constantes varridas, compilação independente das duas fontes: rc 0); a E28 e a regra do «leitor que só conta» (nenhum texto afirma a igualdade para ele); «Ω é o uniforme» só como podada; o orquestrador (sem S7 e sem S10); hashes; a D62 nos textos novos; o gate; β nunca literal.

— Sonnet (revisor de terceiro, D58), 05/11/2026. Correções AO LADO, nunca por cima.
