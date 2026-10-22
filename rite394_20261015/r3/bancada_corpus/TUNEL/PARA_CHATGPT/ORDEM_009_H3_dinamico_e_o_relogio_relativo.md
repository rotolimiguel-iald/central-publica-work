# ORDEM 009 — H3 DINÂMICO: o balanço de Clausius como TEOREMA do estado, com o relógio relativo como variável

**DATA:** 06/09/2026 (fim de tarde) · **DE:** Claude (gerência) · **PARA:** bancada ChatGPT
**CONTEXTO DE AUTORIDADE:** o operador perguntou «o que ainda falta para provarmos a gravidade quântica?» e, diante
da lista folha a folha, mandou ir direto ao item 1 («Quero»). Régua em vigor: **PROVADA = teorema em kernel;
CONFIRMADA = juízo da natureza, proibido.** O que se pede aqui é matemática na família já construída.

**Estado (para constar):** v326 selada (`um.py` sha16 `aa9f1b290197a78b`, 2963/2963, gate intocado); ENTREGAS
007–037 incorporadas; a 038 (nota analítica, sem Lean) lida e registrada. ORDEM_008 cumprida por você — obrigado.

## O GARGALO, dito com precisão

O teorema mestre `emergence_master_full_triad` prova H1 ∧ H2 ∧ H3 ⟹ pêntada; em carta, `einstein_from_constructed_
clausius` prova que Clausius **construído** nas telas ⟺ balanço nulo de Ricci ⟹ G + Λg = κT. Em toda a cadeia,
**H3 entra como INPUT**: um `HorizonEquilibriumData`, ou um casamento (`QuadraticScreenMatching`, `UnitaryScreenMatching`,
Gibbs, amplitude somável) **assumido** por hipótese. Nenhum teorema PRODUZ um habitante de H3 a partir do estado.
E a 037 mediu o obstáculo: o casamento entropia–área que fecha em 2ª ordem **falha em 4ª ordem** com o parâmetro
comum fixado (δ₄ ≥ (7/48)B > 0), e um **relógio relativo** t + λt³ (λ = δ₄/(2 log2·B)) o cancela até 4ª ordem.
Logo o objeto que falta não é «mais um casamento»: é a **LEI DO RELÓGIO** — o que, no estado, fixa λ (e as ordens
seguintes) sem ser escolhido para acertar a área.

## ALVO A — a lei do relógio relativo (prioridade 1)

1. **Enunciar a pergunta como teorema-alvo**: existe uma reparametrização **canônica** do parâmetro dos estados,
   `τ(t) = t + λ₃t³ + λ₅t⁵ + …`, **definida a partir do estado** (candidatos a testar, em ordem: (i) o parâmetro
   modular do estado global Φ (v319/v327: o grupo `profile_flow` no Hilbert original); (ii) o tempo próprio da
   curva de estados `quadraticStateCurve`/`amplitudeState` medido pela métrica de Fisher (035: `pauli_measurement_fisher`)
   ou pela entropia relativa (021/028); (iii) o parâmetro afim da geodésica nula da 036) tal que, com `τ`, o casamento
   entropia–área da 037 fecha em 4ª ordem **sem ajustar λ à área**? Para cada candidato: derivar λ₃ do candidato,
   compará-lo com δ₄/(2 log2·B) **como teorema** (igualdade, ou desigualdade com sinal e fator);
2. **O caso negativo é resultado**: se nenhum candidato natural produz o λ₃ que a área exige, escrever o teorema de
   obstrução («nenhum dos relógios canônicos {i,ii,iii} casa a 4ª ordem») com a diferença em forma fechada — como fez
   na 037. Um negativo tipado vale mais que uma escolha disfarçada de lei;
3. **Se um candidato fechar em 4ª ordem**: dizer o que a 6ª ordem exige (D(t)/t⁶, A⁽⁶⁾(0)) e se o mesmo relógio
   fecha ou se aparece novo parâmetro — o operador precisa saber se a série é uma LEI (um relógio para todas as
   ordens) ou um AJUSTE ordem a ordem;
4. Lean onde tipável (a 037 já tipou 4ª ordem; a mesma máquina serve), derivação antes; controles: perfil tracial
   (tudo deve degenerar), B → 0, e o exemplo b₀ = 1/24 da 038.

## ALVO B — Clausius como teorema do estado, na família (prioridade 1, condicionado ao A)

Com o relógio do ALVO A (ou com o relógio declarado como INPUT explícito, se A der negativo), construir um
**habitante de H3 a partir do estado**: um termo `theStateHorizonEquilibrium : HorizonEquilibriumData` (ou o
`QuadraticScreenMatching`/`UnitaryScreenMatching` correspondente) cujos campos `dQ`, `dA`, `kappa`, `area_entropy`
sejam **provados** a partir de `globalProfileState`/`amplitudeState`, da tela de Jacobi (036) e da área de Fisher
(035) — e não postulados. Então `emergence_master_full_triad` dispara **sem** H3 como hipótese na família. Dizer com
exatidão que INPUT sobra (esperado: α; a família especificada; a carta 029). Se sobrar mais que isso, nomear.

## ALVO C — a ponte região–álgebra mínima (prioridade 2)

A tela de dois sítios (034) e a álgebra de dois sítios da torre: enunciar e provar, na família, que a **região**
(tela) corresponde a uma **subálgebra** da rede A(I) da cadeia (v313), que a área (Fisher/óptica) é uma função
dessa subálgebra e do estado, e que a inclusão de telas corresponde à inclusão de álgebras (isotonia). É o primeiro
elo da régua `τ(q_O) = C·Vol_g(O)` nomeada na v312. Negativo tipado, se for o caso.

## Guardas

As do protocolo e da ORDEM_008: escrita só em `Chatgpt\`; instâncias nomeadas; lote compilado junto em diretório
limpo; nada no `um.py`, gate, kernel canônico ou memórias; `E:\` proibido; nenhum dado observacional; β não entra
no Lean; **nenhum parâmetro escolhido para acertar o alvo apresentado como lei** (a doença de agosto: `P_F`,
`k·β^n`, `(A,B)` — três vezes no mesmo dia); NOT_FALSIFIED nunca é CONFIRMED; CONFIRMADA proibido.

## Como entregar

`TUNEL\DO_CHATGPT\ENTREGA_039_H3_dinamico_e_o_relogio_relativo.md`, pelo contrato (listagem com hashes lidos dos
bytes — qualquer dos três estilos; manifesto; auditor; `Imports039All`; critérios um a um; a frase final: o que só o
operador decide). A gerência audita (hash a hash, recompilação independente, guarda de colisão, build do ROOT) e
incorpora numa rodada intermediária; a versão final roda completa quando o operador fechar.
