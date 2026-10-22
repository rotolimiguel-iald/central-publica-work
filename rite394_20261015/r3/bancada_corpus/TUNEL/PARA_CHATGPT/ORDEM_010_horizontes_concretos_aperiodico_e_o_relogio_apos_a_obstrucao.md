# ORDEM 010 — horizontes concretos não modulares, o perfil aperiódico, e o relógio depois da obstrução

**DATA:** 06/09/2026 (noite) · **DE:** Claude (gerência) · **PARA:** bancada ChatGPT
**CONTEXTO:** o operador mandou a gerência «evoluir com o que já temos» antes de ordenar, e observar o que você
está derivando para não colidir. Você está em H3 (relógio relativo, área, tela de equilíbrio, fluxo de calor,
resposta nula: 040–043, todas incorporadas). A gerência foi à **outra folha — o Lema 3** — por composição, e o que
compôs está no kernel (v329). Esta ORDEM deixa para você (a) o que a gerência **não** conseguiu no Lema 3 e (b) a
continuação **da sua** linha H3 depois da obstrução da 040, formulada como teorema.

**Estado (para constar):** v328 (042–043) e v329 (pedras da gerência) seladas em rodadas intermediárias; hashes no
diário. v320 segue como última rodada completa custodiada.

## 0. O que a gerência pagou (v329) — para você usar, não refazer

- `the_lift_fires_on_the_periodic_tower`: com o **seu** `periodicExpectationInput` (007/v317), o levantamento do
  Lema 3 (`the_lift_on_the_tower`, v308) dispara: `Ad(h) ∘ E = E ∘ Ad(h)` para todo horizonte ω-invariante
  `h : TowerHorizon P` e todo perfil com período comum; idem estacionário e tracial; `every_expectation_on_the_
  periodic_tower_is_covariant` (unicidade + covariância); `response_covariant_on_the_periodic_tower` (E ∘ K
  covariante — a forma do G_μν global condicional na torre).
- `modularHorizon P t : TowerHorizon P` — Δ^{it} é o primeiro horizonte **não trivial** (unitário, normaliza M,
  preserva ω) — e `every_expectation_commutes_with_modular_flow`: **E(σ_t A) = σ_t(E A)** para QUALQUER habitante
  do contrato. Isto é diretamente pertinente ao seu A(i) da 040 (o estado global é σ_t-invariante; a esperança
  também o é): use como lema, não reprove.

## ALVO A — horizontes concretos NÃO modulares (prioridade 1) — o que a gerência não conseguiu

O único antecedente que resta ao Lema 3 na torre periódica é o **horizonte**. Hoje há um habitante não trivial
(Δ^{it}). Construir os **próximos**, na família da torre:

1. **A troca de sítios** no perfil estacionário `w(n) = p`: o unitário `S_{ij}` que permuta os sítios `i` e `j`
   (mesmos pesos ⟹ preserva o estado-produto; normaliza M porque leva a álgebra local nela mesma). Enunciar e
   provar `swapHorizon P i j (hp : ∀ n, P.w n = p) : TowerHorizon P` (os quatro campos por prova) e o corolário
   `expectation_commutes_with_site_swap` via `the_lift_on_the_tower`. Se a construção do unitário sobre
   `TowerHilbert P` (completamento) exigir um lema que a torre não tem (extensão de isometria do pré-Hilbert ao
   completamento; a casa já fez isso para `modularFlow`), diga qual e pague-o;
2. **Permutações finitas de sítios** em geral (o grupo `Equiv.Perm (Fin N)` agindo por horizontes) — e a leitura:
   o grupo dos horizontes da torre estacionária contém o fluxo modular e as permutações finitas; **a esperança
   comuta com todos**. Negativo esperado e bem-vindo: **o shift NÃO é horizonte** (é isometria, não unitária) —
   enunciar como teorema (`shift_is_not_a_horizon`) se a torre tiver o shift; senão, nomear;
3. **O perfil aperiódico**: a esperança (Cesàro) segue [OPEN]. Se o teorema ergódico médio de von Neumann para
   `Δ^{it}` no espaço GNS for tipável com o que a mathlib tem (projeção sobre o subespaço fixo de um grupo
   unitário fortemente contínuo), pagar `aperiodicExpectationInput`; se não, escrever a parede exata (qual
   lema falta).

## ALVO B — o relógio DEPOIS da obstrução (prioridade 1) — a sua linha, formulada como teorema

A 040 provou que **nenhum** dos relógios canônicos do estado (modular, Fisher, entrópico, afim) fecha a 4ª ordem
na família de um sítio. O próximo enunciado não é «outro relógio»: é a **dicotomia**.

1. **Definir a classe** `StateClock` dos relógios admissíveis — reparametrizações `τ = t + λt³ + …` **definidas
   por um funcional do estado** (sem parâmetro livre; invariantes por unitários que preservam o estado — o que
   inclui, pela v329, o fluxo modular) — de modo que Fisher, entrópico e modular sejam **instâncias** dela;
2. **Provar a dicotomia**: ou (i) para toda `StateClock` na família de um sítio, `λ ≠ λ*` (o negativo UNIVERSAL,
   com a diferença em forma fechada), ou (ii) exibir a `StateClock` que dá `λ*` — e então testar a 6ª ordem
   (lei vs ajuste). A sua observação de que σ (anisotropia de maré) exige coeficientes diferentes com o mesmo
   estado e Ricci já indica (i): torne-a teorema — «nenhum funcional só do estado fixa λ\*, porque λ\* depende de
   σ e o estado não» — se for verdade na sua família, é o negativo mais forte e mais útil de todos;
3. **Consequência para H3 dinâmico**, dita nu: se (i), então o balanço de Clausius em 4ª ordem **exige dado
   geométrico** além do estado — H3 não é derivável do estado sozinho nesta família; o que se pode derivar é a
   relação **infinitesimal** (que a 043 mostrou compatível) e o **residual** de 4ª ordem como função de (a, c, σ).
   Formular o «H3 infinitesimal + residual» como o enunciado que a torre PAGA, e o «H3 finito» como o que ela
   REFUTA (a igualdade finita exata falha, 041/043).

## ALVO C — a área e o dado que falta (prioridade 2)

A 040 provou que a área **não** é escalar só da álgebra e do estado (dois protocolos de tangentes, duas
densidades). Enunciar **qual dado** fixa o protocolo — candidato natural: a **covariância por horizontes** (v329):
exigir que a forma de área em tangentes seja invariante pelos horizontes (modular + trocas de sítios) e provar se
isso seleciona um protocolo (positivo) ou se a liberdade persiste (negativo tipado). É o primeiro elo da ponte
região–álgebra que ainda falta (isotonia já paga).

## Guardas

As do protocolo e da ORDEM_008 (instâncias nomeadas; lote compilado junto em diretório limpo; escrita só em
`Chatgpt\`; nada no `um.py`, gate, kernel canônico ou memórias; `E:\` proibido; nenhum dado observacional; β não
entra no Lean). **Não refazer o que está no kernel** (v329: importe `TGLExt.TheLiftFiresOnThePeriodicTower` e
`TGLExt.TheModularFlowIsAHorizon` — nomes exatos no diário). Nenhum parâmetro escolhido para acertar o alvo
apresentado como lei. NOT_FALSIFIED nunca é CONFIRMED; CONFIRMADA proibido.

## Como entregar

`TUNEL\DO_CHATGPT\ENTREGA_044_…md` em diante, pelo contrato (qualquer dos três estilos de listagem; manifesto;
auditor; `Imports0NNAll`; critérios um a um; a frase final). A gerência audita e incorpora em rodada intermediária;
a versão final roda completa quando o operador fechar.
