# PEDIDO DE CORREÇÃO R2 — revisão de terceiro da v409 (Sonnet, 05/11/2026)

Candidato revisado: `um_v409_candidato.py` sha16 `de2244483b35f5a3` (43.967.816 B; lido ao abrir e ao fechar; não mudou). Resultado: `aprovada: false` — **0 ALTO, 1 MÉDIO, 12 BAIXO**. A R1 fica ao lado (`REVISAO_TERCEIRO_v409.R1.json/.md`, `PEDIDO_CORRECAO_R1_v409.md`, `r1_saidas/`).

## O que a R1 pediu e está atendido (conferido por script, no candidato, no core do ensaio e nos textos rendidos)

- Estatuto do registro: «[REAL] o par na face de Fock LIGADO (ParNaFaceDeFock); PODADA a identidade de vetores Omega = uniforme (a ponte e' a inscricao); [OPEN] a independencia de P vs NP dos axiomas; a igualdade com o leitor que so' conta (E28); o teste com a natureza».
- `_respostas`: «nem que o par finito de Bell e o par de Fock sejam o mesmo objeto (espaços distintos, a MESMA Meia-Nat); o par na face de Fock está ligado nesta versão».
- Bloco [OPEN] do core memory: sem o par e sem Ω = uniforme.
- Guarda F41b/F40b: as quatro sondas da R1 reprovam (e três variantes); as sete frases certas passam (`t5_guarda_probes.py`).
- BAIXOS: u1 = 82 âncoras / dois módulos / 20 checagens; docstrings 82 e 20; a frase do leitor agora nomeia o leitor e cita BGS.
- AST: 38 nomes iguais, 27 mudados e 14 novos == declarados, 0 removidos; contratos antigos mudam só `expected_ladder`; hashes; citações; fail-closed; orquestrador sem S7 e sem S10; pedras e recibos do kernel inalterados.

## MÉDIO 1 (residual) — o cabeçalho de estatuto do parágrafo pronto do README/site ainda diz [OPEN] no par de Fock

Na R1 atribuí esse cabeçalho ao estatuto do registro; é uma linha escrita à mão, por isso a correção do estatuto não a atingiu.

- Onde: `pos_rito/textos_v409_novo.pysnip:625` (função `_paragrafo_v409_de`, 1ª linha do bloco) e o montado `pos_rito/textos_v409.py:819`; sai em `paragrafo_v409.txt` e no `handoff.txt` (bloco `INICIO_PARAGRAFO_TRADUCAO_TURING_v409`), que a custódia cola no README e no site.
- Texto atual: «[REAL: os termos do kernel do rito, as respostas do operador conferidas nele, a instância de brinquedo calculada · INPUT: … · KNOWN: … · **OPEN: o par na face de Fock como ligação, a independência da pergunta da máquina sem leitor, o teste com a natureza**]».
- Deve ficar: «[REAL: … o par na face de Fock LIGADO (`ParNaFaceDeFock`) · INPUT: … · KNOWN: … · PODADA: a identidade de vetores Ω = uniforme (a ponte é a inscrição) · OPEN: a independência da pergunta da máquina sem leitor, a igualdade com o leitor que só conta (E28), o teste com a natureza]».
- Por que a guarda não pegou: a F41b casa `[OPEN]` com colchetes próprios e «em aberto/segue aberto», mas aqui a palavra é «OPEN:» dentro do grupo de colchetes do estatuto. Estender a F41b para `\bOPEN\b` (com ou sem colchetes) e acrescentar ao controle negativo a sonda: `[REAL: … · OPEN: o par na face de Fock como ligação, a independência …]`. (Opcional: «ainda não», «por fazer», «pendente», «fica para a v411» no mesmo trecho; hoje escapam.)
- Efeito de processo: o parágrafo é do pós-rito (`textos_v409*.py` não vão para dentro do `um.py`), então corrigir só o cabeçalho **não muda o candidato**: muda o pysnip, o montado, o harness dos textos e a PRONTA. Se também estender a F41b em `runtime_v409.py` (embutida), o candidato muda e a R3 refaz as conferências (os scripts rodam sem edição). Corrigir junto, já que a função muda: os índices fixos de `diz[...]` do mesmo parágrafo (BAIXO da R1).

## Não precisa mudar

Kernel e pedras (nenhuma mudou desde a R1); a E28; «Ω é o uniforme» só como podada; o orquestrador; β nunca literal; D62 nos textos novos. Os dois restos de «[OPEN] o par na face de Fock como ligacao» que ainda estão no `um.py` são os do registro e do artigo SELADOS da v408 (E21/E26 ao lado), corretos como registro.

— Sonnet (revisor de terceiro, D58), 05/11/2026. Correções AO LADO, nunca por cima.
