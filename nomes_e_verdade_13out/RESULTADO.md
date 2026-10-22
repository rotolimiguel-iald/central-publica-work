NOMES E VERDADE — 13/10

Rodada de NOMES e da IDENTIDADE r3 (unidade F1.IDENTIDADE, gerência c1; construtor em nome próprio). Decisões do operador: verbatim `work\cunhagens_13out\OPERADOR_13out_nomes_identidade_cordeiro_torre_verbatim.txt`, sha16 `0ddffcdb0a9c7b5e` (conferido por script). As pedras são CANDIDATAS, vivem só em sandbox, NÃO foram instaladas no Nós; nada aqui move o gate; validade no kernel não é creditação. Entre aspas angulares só trechos do operador, conferidos nos bytes (`medidas\CONFERENCIA_ASPAS.json`: 12 citações novas, 0 fora dos bytes).

## 1. As quatro pedras (fonte e .olean por sha)

| módulo | fonte | sha16 fonte | olean | sha16 olean | EXIT | erros | avisos | sorry |
|---|---|---|---|---|---|---|---|---|
| `TGLExt.Posto` | `1_POSTO\Posto.lean` | `63ad023f015de883` | `1_POSTO\Posto.olean` | `5a635e2a764dbd59` | 0 | 0 | 0 | 0 |
| `TGLExt.Santo` | `2_SANTO\Santo.lean` | `245b5a7a666c1547` | `2_SANTO\Santo.olean` | `ad1741220bcd1ded` | 0 | 0 | 0 | 0 |
| `TGLExt.IALD` | `3_IALD\IALD.lean` | `884b327423888ddc` | `3_IALD\IALD.olean` | `88d88d530b46862d` | 0 | 0 | 10 | 0 |
| `TGLExt.Verdade` | `4_VERDADE\Verdade.lean` | `2b7639bab440005a` | `4_VERDADE\Verdade.olean` | `02bb2e7bdd359fc3` | 0 | 0 | 0 | 0 |

Sha256 inteiros nos recibos `logs\f1_posto_RECIBO.json`, `f2_santo`, `f3_iald`, `f4_verdade`. Toolchain `lean` v4.31.0 copiado (sha16 `9b216deb50d37c32`), LEAN_PATH só-leitura ao `.lake` do Nós (kernel copiado byte a byte para a sobreposição `ov`, agregado `34a70b88…` igual à origem), `-o` só no sandbox `C:\t\nm1`. Zero `declaration uses \`sorry\`` no formato real (crase); o contador foi validado por controle positivo (`meta\CtlSorry.lean`: contagem 2 e `sorryAx`). Os 10 avisos de `IALD` são os 10 da r3 original (`ContinuousLinearMap.mul_apply` deprecado), herdados, sem mudança de bytes de código. Reprodutibilidade: o `.olean` de `Verdade` saiu idêntico (`02bb2e7b…`) em duas compilações; o de `TheIdentityHasAName` r2 recompilado aqui saiu `cc232917…`, igual ao registrado.

**collectAxioms de TODAS as constantes** (lido pelo `Meta_*.lean` no kernel do sandbox, não só dos `#print axioms`): Posto 221, Santo 167, IALD 69, Verdade 206 constantes; **0 fora do trio** {propext, Classical.choice, Quot.sound} em todas; 0 `sorryAx`; 0 `axiom`/`opaque`/`unsafe`.

## 2. PARTE 1 — tabela de invariância das renomeações (lida do kernel)

Método: `Meta_*.lean` lê, no kernel do MESMO sandbox, TIPO e VALOR de cada constante do módulo antigo (original pinado por sha, compilado aqui) e do novo, em duas serializações — SA (De Bruijn, sem nomes de binder; é o que o kernel compara) e SN (com nomes de binder) —, passa as cadeias do antigo pelo mapa de nomes (prefixo do módulo + renomeações listadas) e compara CADEIAS INTEIRAS. Antigos compilados na mesma sobreposição: rank r3 `e95775d6…`, tempo R2 `4d8a8259…`, IALD r3 `d7c1f1d3…`.

| pedra | módulo | constantes (antigo / novo) | idênticas SA | idênticas SN | só nome de binder | docstring mudou | axiomas fora do trio | veredito |
|---|---|---|---|---|---|---|---|---|
| Posto | `TGLExt.TheUnitIsTheRank` → `TGLExt.Posto` | 221 / 221 | 221 | 221 | 0 | 2 | 0 | INVARIANTE |
| Santo | `TGLExt.TheTimeIsNotAPost` → `TGLExt.Santo` | 167 / 167 | 167 | 164 | 3 | 1 | 0 | INVARIANTE |
| IALD | `TGLExt.IALD` → `TGLExt.IALD` | 69 / 69 | 69 | 69 | 0 | 2 | 0 | INVARIANTE |

**Veredito geral: INVARIANTE_100_POR_CENTO.** Em todas as constantes (públicas, internas, lemas de equação) o TIPO e o TERMO são iguais em SA; o conjunto de nomes é o mesmo depois do mapa. Em SN, a diferença é só de nomes higiênicos de binder: no Posto e no IALD zero; no Santo 3 (`face_has_a_limit`, `the_face_lands`, `the_two_regimes_of_time`), cujos binders derivam do nome da própria declaração renomeada. A ordem de `constNames` no módulo difere em Posto e Santo (é ordem de tabela hash, depende dos nomes); o conjunto é o mesmo.

Renomeações (N1–N4 da auditoria `a1185ceb`; A-R2-01 e N2 do relatório R2 do tempo):

| pedra | nome antigo | nome novo | kernel |
|---|---|---|---|
| Posto | `reading_weights_are_truth_and_cost` | `rhoStar_and_Q0_traces_of_diag_one_sub_b_b` | tipo e termo iguais (SA) |
| Posto | `inscription_at_thetaMiguel` | `dephasing_acts_and_endpoint_entry_at_thetaMiguel` | tipo e termo iguais (SA) |
| Santo | `face_has_a_limit` | `orbit_tendsto_center_reexport` | tipo e termo iguais (SA) |
| Santo | `face_distinguishes_instants` | `diagFlow_distinguishes_instants_reexport` | tipo e termo iguais (SA) |
| Santo | `the_face_lands` | `dephase_tendsto_expectation_reexport` | tipo e termo iguais (SA) |
| Santo | `face_clock_has_no_period` | `decay_clock_has_no_period` | tipo e termo iguais (SA) |
| Santo | `the_two_regimes_of_time` | `isometry_dephasing_and_clock_conjunction` | tipo e termo iguais (SA) |

N1 (nome do módulo): `TGLExt.Posto`. N4: a docstring de `reading_returns_the_post` não diz mais «projetor» (o tipo não pede ⟨a, a⟩ = 1) — única docstring alterada além da de `rhoStar_and_Q0_traces_of_diag_one_sub_b_b` (que perdeu «verdade» e «custo» do nome; ficam como leitura [ONTO] na docstring). Docstrings alteradas no IALD: as duas que citavam `TheTimeIsNotAPost.…`. Títulos: Posto «rank=posto=nome»; Santo «tempo=relação modular=Santo»; IALD «organismo=IALD=Verbo Vivo» (título «IALD = Verbo Vivo», imports re-pinados para `TGLExt.Posto` e `TGLExt.Santo`).

## 3. PARTE 2 — `TGLExt.Verdade`: resultado por afirmação (ADENDO R3, congelado ANTES)

`2_PREREGISTRO\ADENDO_R3.json` (sha16 `cc4696392ca5130e`) e `FREEZE_ADENDO_R3.json` (sha16 `043d0496fb211cb5`; `pedra_r3_existe_no_congelamento: false`; 15 anexos; 11 citações, 0 fora dos bytes) em `work\identidade_cordeiro_13out\2_PREREGISTRO` (arquivos novos; nada existente alterado). Congelado em 2026-10-13T12:08:51.701819-03:00.

| id | termo Lean | veredito | o que diz |
|---|---|---|---|
| V1.a | `reflexivity_is_vacuous` | PASSA | x = x vale para qualquer objeto (`rfl`, sem hipótese): não distingue nada |
| V1.b | `reflexivity_holds_for_every_inscription` | PASSA | identityProj a = identityProj a para todo a real; em a = 5 (TESTE) vale e o traço ≠ 1: vale também onde NÃO há identidade |
| V1.c | `reflexivity_does_not_separate_identities` | PASSA | a ≠ b em (0,1): a = a e b = b valem, e as duas projeções são distintas |
| V2.a | `Verdade (estrutura em Prop, 10 campos)` | PASSA | quadrática 1 = q²+α²; projeção (traço 1, idempotente, posto 1); reler n+1 = ler 1 (matriz, vetor, post); unicidade; relação modular (fluxo fixa Ω, preserva ω, age no portador da towerIALD preservando a leitura); reconhecimento recursivo da towerIALD estável e que devolve a leitura; pontos fixos = centralizador de ω; inscrição na torre unitária com ω lendo q em toda iteração |
| V2.b | `verdade_of_unit_interval` | PASSA | para todo a em [0,1], Verdade a (α como parâmetro; nenhum número de α ou β) |
| V2.c | `the_projection_is_forced_by_its_truth` | PASSA | unicidade: hermitiana idempotente de traço 1 que fixa a inscrição é identityProj a (D = E − ω é hermitiana, idempotente, traço 0, logo 0; usa `trace_conjTranspose_mul_self_eq_zero_iff`, Mathlib). Não falhou |
| V2.d | `the_identity_is_the_truth; identity_iff_truth` | PASSA | toda identidade nomeada N carrega Verdade N.alpha; (∃ N, N.alpha = a) ↔ 0 < a ∧ a < 1 ∧ Verdade a |
| V2.e | `no_truth_above_one; no_truth_below_minus_one` | PASSA | controle negativo: sem Verdade para a > 1 nem a < −1 (campo quadrático falha) |
| CORDEIRO.a | `refPost_eq` | PASSA | refPost = |e₀⟩⟨e₀| = !![1,0;0,0] (E₀₀) |
| CORDEIRO.b | `commutator_explicit` | PASSA | [ω, E₀₀] = (q·α) • !![0,−1;1,0], q = qOf α, para todo α real |
| CORDEIRO.c | `commutator_ne_zero_iff; commutator_ne_zero_on_the_unit_interval` | PASSA | comutador ≠ 0 ↔ q·α ≠ 0 (todo α real); em [0,1], ↔ 0 < α < 1 |
| CORDEIRO.d | `identity_coincides_with_the_post_iff_alpha_zero` | PASSA | em [0,1]: ω = E₀₀ ↔ α = 0; enquanto α ≠ 0 a identidade nunca coincide totalmente com o posto |
| CORDEIRO.e | `the_commutator_blocks_the_coincidence; a_nonzero_commutator_forbids_coincidence` | PASSA | 0 < α < 1 ⟹ comutador ≠ 0 ∧ ω ≠ E₀₀; forma geral: comutador ≠ 0 ⟹ x ≠ y |
| CORDEIRO.f | `the_commutator_is_odd_under_the_reflection (+ reflection_sq)` | PASSA | J := 2E₀₀ − 1: J·J = 1 e J·K·J = −K, K = [ω, E₀₀] |
| CORDEIRO.g | `the_reflection_anticommutes_with_the_commutator; the_reflection_and_the_commutator_are_inseparable` | PASSA | por IMPORT do kernel instalado (`TheVerbSelectsTheAction.J_anticommutes_with_K`, `light_and_gravity_are_inseparable`; a forma canônica é `JKJ_eq_neg_K`, DecisionCommutation.lean l.149): J·K = −(K·J) e, se K ≠ 0, J·K ≠ 0 e [J,K] ≠ 0 |
| CORDEIRO.h | `the_poles_have_no_commutator` | PASSA | α = 0: ω = E₀₀ e comutador 0; α = 1: ω = E₁₁, comutador 0 |
| TORRE | `campos IALDTowerIdentity / Verdade (towerIALD); in_the_tower mantido` | PASSA | instância principal towerIALD; TowerHilbert (I6.a) é a face unitária (campo `in_the_tower` mantido) |
| NOME | `ofName; every_name_bears_the_same_identity; the_name_enters_no_proof; the_structure_does_not_fix_the_name` | PASSA | MANTIDAS (tipo e termo iguais à r2); 0 das 161 constantes do núcleo da Verdade menciona `NamedIdentity.name` ou `postedName` (lido do kernel) |
| B1, B2 | `docstrings de I6.b′ e I2.d` | FEITO | marcadas [INPUT da gerência] |

Sondas de não-vacuidade: `probe_the_truth` (Verdade 1/2), `probe_the_commutator` (comutador ≠ 0 e ω ≠ E₀₀ em α = 1/2, número de TESTE), `probe_named_identity`, `probe_tower_identity`, `probe_IALD_tower` (da r2, mantidas).

### Tabela r2 → r3 da Verdade (lida do kernel; `TABELA_R2_R3.json`)

150 constantes na r2, 206 na r3: **144 MANTIDA** (tipo e termo iguais em SA), **59 NOVA**, **3 REMOVIDA** (`alicerce_fundante`, `alicerce_fundante_habitado` e uma prova auxiliar de `halfProfile`), **2 TIPO_MUDOU** e **1 VALOR_MUDOU**, os três de `halfProfile` (perfil de TESTE): o campo de dado `w` é idêntico; muda só o nome do lema auxiliar de prova de `Nat.AtLeastTwo 2` (o literal 2 de `reflection` criou `reflection._proof_1`, que `halfProfile` reutiliza); por irrelevância de prova é o mesmo objeto. Nenhum enunciado público da r2 mudou. `NamedIdentity` e suas projeções: MANTIDAS (não acrescentei campo).

## 4. As quatro juntas sob `open TGLExt` (sem colisão)

`meta\Juntas_A.lean` importa Posto, Santo, IALD e Verdade e, com `open TGLExt`, faz `#check @Mod.nome` de **564 nomes públicos**: EXIT 0, 0 erros. `meta\Colisoes.lean` varre no kernel os 598 nomes curtos das quatro: **0 colisões com `open TGLExt`** (nenhum `Mod.nome` existe na raiz). Controle positivo (`meta\AmbControle.lean`, `open TGLExt TGLExt.IALD` + `#check @dephase`): ERRO «Ambiguous term», como esperado. No regime extremo (abrir também os quatro namespaces) há 3 ambiguidades, nenhuma nova no sentido de mudar enunciado: `dephase` (`TGLExt.dephase` × `TGLExt.IALD.dephase`, o homônimo C4 já rotulado na pedra do motor) e `dephased_det` (em `Posto` e em `Verdade`, de origens independentes). `COLISOES.json`.

## 5. Impressão digital do tgl_kernel, antes e depois

Sem seguir junções (`.lake/packages` é junção e foi pulada). ANTES = DEPOIS em tudo: 11049 arquivos, 7559742119 bytes, metadados `42953f27bcd15ba2`, conteúdo das 1216 fontes fora de `.lake` `22557eadef61ef50`, conteúdo dos 1189 `.olean` de TGLExt `aef5f8dcd469aa79`. Nada foi escrito no Nós.

## 6. Correções de fraseado e limites (o número corrige a frase)

* O pedido diz que o fluxo modular «fixa ω/Ω, já em I6.c». Na r2 o fluxo que fixa Ω e preserva ω está em I6.a (`TowerHilbert`); I6.c (`towerIALD`) traz `read`/`recognize`. A Verdade junta as duas e acrescenta a ponte: o fluxo age no portador da `towerIALD` e preserva a leitura (`the_modular_flow_preserves_the_IALD_reading`).
* `Verdade a` vale para TODO α em [0,1]: ela não fixa α (α é parâmetro [INPUT], testemunhado, não derivado); `identity_iff_truth` diz que a estrutura nomeada e a Verdade determinam-se mutuamente, não que a Verdade discrimine a natureza. Ler a estrutura como «verdade absoluta» é leitura [ONTO] do operador sobre o termo.
* A unicidade (V2.c) usa as hipóteses nomeadas: hermitiana, idempotente, traço 1 (o ω(I) = 1 da casa) e E v = v. É o que o termo prova.
* O comutador é 2×2, no modelo v = (q, α): que ele seja «o cordeiro imolado» é decisão do operador sobre o termo; que J seja a Luz e K o gradiente é [ONTO]; o termo é JKJ = −K. O posto LITERAL de P_v em B(H_φ) segue [OPEN]; a leitura «o posto 1 não permanece na torre» segue [INPUT da gerência].
* ANTERIORIDADE: o ADENDO R3 foi congelado antes de `Verdade` existir; as pedras mecânicas (Posto, Santo, IALD) já existiam no congelamento (seus shas estão no FREEZE) e foram regeneradas depois só para trocar « » por “ ” em frases que não são do operador (convenção); a compilação e a tabela usam as fontes finais acima. A anterioridade apoia-se em carimbo de arquivo e na recusa do script (BAIXA, como na r1/r2).
* Fora do pedido, nada foi feito: sem instalação no Nós, sem tocar no um.py, quadro, mapa, memória, túnel, Bancada, site, git; sem init/transition ACOM.

## 7. O que é ato de quem

* Gerência: auditoria cética independente das quatro pedras; instalação na v392 sob os nomes `Posto`, `Santo`, `IALD`, `Verdade` (recompilar no lake do Nós, importar em `TGLExt.lean`, `#print axioms` no `TGL/Audit.lean`, embutir no um.py); registrar `registro_mapa_F1.IDENTIDADE_R3.json` no mapa.
* Operador: se o rename de `dephased_det` (colide Posto × Verdade só no regime extremo) vale a pena; se `commutatorWithPost` é de fato o termo do cordeiro (decisão dele, dada); o Nome no core do um.py.

Limpeza: toolchain e sobreposição de `C:\t\nm1` apagados ao final (ver `medidas\LIMPEZA.json`).
