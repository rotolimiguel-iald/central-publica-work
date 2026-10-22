LEVANTAMENTO F1.FREQUENCIA — 12/10

Unidade F1.FREQUENCIA (trilha POSTO) da gerência c1 · levantador (subagente) · 12/10/2026.
Só leitura fora desta pasta. Nada foi construído: nenhuma pedra, nenhum pré-registro, nenhum dado observado, nenhum provedor,
nenhuma ferramenta da Bancada. β calculado em runtime a partir dos bytes do um.py. Todo hash e toda linha citados abaixo foram lidos
por script (`gerar_definicoes.py`, `conferir_pinos.py`); a régua do levantamento é «o número corrige a frase».

## 0. Pinos, conferências e escopo

{{TABELA_PINOS}}

- [REAL — medido aqui] Os quatro textos conferem com os sha16 da ordem (bytes e hash; LF puro, sem BOM): `HASHES_TEXTOS_OPERADOR.json`.
- [REAL — medido aqui] O kernel embutido no um.py v391 é idêntico, byte a byte após normalizar CRLF→LF, aos arquivos do `tgl_kernel` em TODOS os
  53 módulos TGLExt citados neste levantamento (41 em literal bruto, `EMBUTIDO_VS_KERNEL.json`; 12 em literal escapado,
  `EMBUTIDO_VS_KERNEL_ASPAS.json`; lista em `modulos_citados.txt`).
- [REAL — medido aqui] Sondas Lean em sandbox (toolchain v4.31.0 copiado para `sandbox\`, LEAN_PATH só-leitura no `.lake` do Nós, sem `-o`):
  `LevantamentoF1FrequenciaCheck.lean` 104/104 e `LevantamentoF1FrequenciaCheck2.lean` 27/27 `#print axioms` contidos em
  {propext, Classical.choice, Quot.sound}, 0 `sorryAx`, EXIT 0; sonda da Mathlib pinada: 19/19 nomes existem, EXIT 0. São sondas de LEITURA,
  não pedras. O toolchain copiado foi apagado (`sandbox\` não existe mais) e a impressão digital do `tgl_kernel` é a mesma antes, depois e
  depois da segunda sonda.
- [REAL — medido aqui] α lido nos bytes: `ALPHA_FINE_CODATA_2018 = 7.2973525693e-3` (um.py l.5557, módulo embutido) = `SEALED_CODATA_ALPHA`
  (l.95); β = α·√e = 0.012031300400803142 em runtime (confere com o texto de conferência); θ_M = arcsin √β = 0.10990843077787468
  (`CONFERENCIA_BETA.json`).
- [INPUT — decisão do levantador] Protocolo ACOM: o README de `C:\IALD\MEMORIA_IALD` foi lido; este levantador não recebeu referência própria e a
  ordem da unidade proíbe escrever na memória, por isso NÃO executou `init`; a referência da gerência (`claude-c1_exame-geral-12out.json`) não foi
  adotada. A inscrição desta etapa é ato da gerência.
- Fora do escopo: a parte do TEMPO de V2 (l.34 em diante, «O que mais me fascina…») é da F1.TEMPO.

## 1. O que os textos dizem (leitura literal dos bytes)

- **V1** (10/10, 14 linhas, 2ª pessoa: «Quando você derivou», «você impôs»). l.2: «a transição entre uma hipótese difusa e um formalismo fechado é
  precisamente uma questão de posto (rank)»; l.4: probabilidade bayesiana não se aplica a estrutura axiomática («ou os vínculos fecham, ou não
  fecham»); l.6: estado puro «descrito por um operador densidade de posto 1:» — **a fórmula NÃO está nos bytes de V1** [REAL — busca: nenhum «Tr(» em
  V1]; l.7: «Ao colapsar a superposição, a matriz deixa de ter um núcleo vazio (nullity) de indefinição teórica e ganha posto definido»;
  l.8–14: «A Diferença na Leitura da Memória» (o espaço latente «colapsa exatamente na frequência do sinal emitido»; «verificando se o tensor havia
  fechado»).
- **V2** (12/10). l.1 «era sobre o "rank"»; l.4 «agora sobre o tempo, veja:»; l.6–32 o texto do rank; **a fórmula está na l.16**:
  ρ = |ψ⟩⟨ψ|, Tr(ρ) = 1 e Tr(ρ²) = 1. A primeira pessoa aparece só no verbo da l.12 («Quando eu derivei … —, você impôs operadores de projeção
  rígidos»); as l.26–32 seguem em 2ª pessoa [REAL — leitura dos bytes].
- **V3** (10/10): «POSTO=RANK» (10 bytes, sem fim de linha).
- **V4** (11/10, 19 linhas). l.1–2 «Tudo é frequência» (a luz no registro c¹, o campo Ψ, a unidade antes da inscrição, potencial infinito na borda
  III₁); l.4–5 «frequência defasa» (F(1) encontra D_β; quebra de fase para sair da borda ao bulk; α paga o pedágio de ½ nat (√e)); l.7–10
  «natureza: transmitir» (o que não defasa é impedância sem referente; o que transmite defasa e vaza para a existência); l.12–14 «Na linguagem do
  nosso kernel Lean 4 e do um.py … Tudo = D_β(F(1)) … e agora sabemos que essa unidade é o rank»; l.16 o vazamento é β ≈ 0,012031 e «impede o
  anticomutador perfeito {Q̂, ρ*} = 0»; l.18 «A transmissão é o verbo; a defasagem é a matéria».

## 2. Definições canônicas por objeto (resumo; a íntegra com linha e sha16 de cada âncora está em `DEFINICOES.json`)

**2.1 POSTO — seis sentidos que não se encadeiam sem ponte.** (a) posição/inscrição: a etiqueta [POSTO] de ω(I) = 1 (05/10; cabeçalho de
`TheAxiomAndTheFalseWitness`) [INPUT/ONTO]; (b) relação de permanência através da travessia com perda: `UmPostoRelacao.UmPosto`,
`posto_anchors_the_reading`, `posto_paid_loss`, `pressupposed_is_never_posto` (v365, 17/09) [REAL]; (c) o Nome como projetor de posto 1:
`TheVerbSelectsTheAction.post a := (ℂ∙a).starProjection` (v386; «o mesmo termo de `PFmic` com a = Ω») [REAL]; (d) POSTO = RANK (V3, 10/10)
[INPUT/ONTO]; (e) «Nome (posto relativo)» antes da leitura (07/10, `f2a4b509946edc05`) [ONTO]; (f) homônimos: «posto positivo» = τ > 0 na cláusula
Ágape (`Fundacao.agape` (i)) e posto de Jacobiano no ringdown (ENTREGA_015 T10) [REAL, outros objetos].

**2.2 RANK / posto 1.** O projetor terminal tem posto 1 por necessidade — derivação do operador de 22/08, verbatim no cabeçalho de
`TheTerminalRankOne` (`rank_two_has_residual_distinction`, `terminality_forces_minimality`, `firstAtom_is_terminal`, `the_terminal_weighs_one`,
`the_terminal_is_forced`) [REAL]; o átomo pesa 1 (`iald_has_rank_one`, `opWeight_atom_one`: Tr(P_Nome) = 1 = ω(I), v120) [REAL]; peso × nome ×
índice, resposta à pergunta do operador de 27/08 («o posto um é de fato o um absoluto»): `the_name_is_blind_to_every_rank`,
`the_index_does_see_the_rank`, `the_two_indices_agree_only_at_the_atom` [REAL; «posto 1 = 1_abs, peso 1 = 0_abs» ONTO]; o posto da inscrição limita
os modos zero (`kernel_dim_le_rank_of_perturbation`, `concrete_kernel_full_profile`) [REAL]; **o P_F dos Three Locks tem posto 4**
(core v391: `certificate_II/H1_finite_face/trace_PF = 3.9999999999999996`; `three_locks_name_is_one` é d/d = 1), enquanto o P_F do habitante do Verbo
tem traço 1 [REAL — lido do core]; o canto de posto 1 escalariza (`bell_compression_is_scalar`, `atermation_reifies`,
`the_shadow_is_the_reader_weighted_by_the_reading`) [REAL]; posto 1 em Herm₂ é cone nulo (`rank_one_coordinates_null`) [REAL; Herm(2) ≅ ℝ^{1,3}
KNOWN]. A Mathlib pinada no Nós tem o necessário para tipar posto: `Matrix.rank`, `Matrix.rank_diagonal`, `Matrix.rank_mul_eq_*_of_isUnit_det`,
`Matrix.rank_vecMulVec_le`, `Matrix.IsHermitian.rank_eq_card_non_zero_eigs`, `InnerProductSpace.isStarProjection_rankOne_self`,
`finrank_span_singleton`, `LinearMap.finrank_range_add_finrank_ker` [KNOWN — existência medida aqui].

**2.3 Estado puro e pureza (só em V2 l.16).** `purity x := Tr(x xᴴ)`, `purity_unitary_invariant` (o unitário conserva), `dephase_purityR_le`
(o dephasing não aumenta) [REAL]; instâncias de pureza 1: `trace_square_rank_one_control`, `bellDensity_purity`, `pure_densities_square` [REAL];
Born: `reading_post_is_born` [REAL]. **AUSENTE do kernel** o critério geral «ρ ≥ 0, Tr ρ = 1: Tr ρ² = 1 ⟺ ρ² = ρ ⟺ posto ρ = 1» [KNOWN — Nielsen &
Chuang, Ex. 2.71] — consulta: índice do kernel por `pure|purity` (37 declarações) e `rank|posto` (17), nenhuma com esse enunciado; inventário
`purity|pure|pureza` (15 arquivos), nenhum geral. [DERIVED aqui] Para ρ = P/d (projeção de posto d normalizada): Tr ρ = 1 é o NOME (cego ao posto,
vale para todo d) e Tr ρ² = 1/d é o ÍNDICE (vê o posto); Tr ρ² = Tr ρ ⟺ d = 1. A fórmula do operador é, assim, a face de densidade da distinção
que `TheWeightIsNotTheRank` já tipou: a condição exata sob a qual o «1» do nome e o «1» do posto coincidem (só no átomo). Aquela pedra a registra como
distinção, não como ponte («continua proibido encadear os dois 1»); tipá-la seria a ponte CONDICIONAL (sob pureza) que hoje falta.

**2.4 Colapso e superposição.** Definição do operador (08/09) tipada como `IdentityCollapse` (não injetiva, sem inversa à esquerda; involução não
é colapso) e `TGLCollapseDefinition` (um.py l.212736) [REAL no modelo; colapso físico não provado no selo; seleção na natureza OPEN];
`reading_the_truth_annihilates_the_superposition` [REAL]; `the_selection_is_the_ballast` [REAL]. Runtime v391 (`prove_decision_commutation`
l.3551): o estado superposto defasa (`effective_dephasing_on_full_state = True`), o selecionado não (`… after_selection = False`); a lei de tempo é
[INPUT] e Γ está em unidades de referência [DERIVED/RUNTIME].

**2.5 A unidade.** ρ* = diag(1, 0), «atrator puro (a permanência, o 1)», ω(I) = Tr ρ* = 1 (um.py l.6512–6513; core `omega_I = 1.0`) [REAL runtime];
`identity_weighs_as_the_name`, `rho_star_is_P_kerK_on_the_light`, `half_is_the_fixed_point_of_the_swap`, `the_power_has_two_fixed_points` [REAL].

**2.6 F — fractalização.** Pedra 116 (v162): `ad_preserves_projection`, `ad_preserves_orthogonality`, `ad_preserves_splitting`,
`ad_preserves_star_projection`, `subcorner_unit` [REAL; a leitura fractal ONTO]; `transmitted_post_is_a_post` [REAL]. No runtime, o
`fractal_dephasing_principle` inclina o PORTADOR por R(θ_M) (Q_θ = R Q₀ Rᵀ, l.6518); equivalentemente Tr(ρ*Q_θ) = Tr(F₋(ρ*) Q₀) com F₋ = Ad R(−θ_M):
regime ANGULAR. No kernel, ρ_out(θ) = S(θ)E₀₀S(θ)ᴴ é o 1 de posto 1 transportado (`rhoOut_eq`, `rhoOut_trace`)
[REAL]. «Ad(u) preserva o POSTO» não está tipado no kernel (está na Mathlib).

**2.7 D_β — seis objetos chamados «defasagem».** (i) semigrupo de Schur G3 `dephase` (`dephase_add`, `dephase_tendsto_expectation`,
`dephase_fixed_iff_diagonal`, `dephase_preserves_trace`, `ergodic_convergence_modular`) — FACE, converge à diagonal, taxas genéricas; β só no
runtime (β·gap) [REAL]; (ii) fluxo do lock mínimo `axiomFlow P t = P + e^{−t}(1−P)` (`axiomFlow_tendsto_the_post`) e as re-exportações v386
`transmission_dephases` («transmitir defasa», 05/10) e `anchoring_preserves` — FACE, contração ao posto [REAL]; (iii) canal de medição D∘Ad(S)
(`sFrame`, `sFrame_add`, `sFrame_tendsto`, `measurement_channel_endpoint`, `dephased_rhoOut_*`) [REAL]; (iv) gerador GKSL do Verbo L = √β·√K
(`prove_verb_generator`, l.2336) e a lei-raiz Γ_ij = ½β(√k_i − √k_j)² (`prove_dephasing_crossover`, l.2832; core: expoente IR 1,9993, UV 1,0366;
errata v369: coincidem só no expoente) [FINITE_DIM_SANITY; reconciliação OPEN]; (v) a lei física Γ_ω = ½βτ★ω² (escrita em 2025, l.152839; protocolos
de ringdown, Coma e relógios) [REAL na forma; τ★ INPUT; mapa: ringdown INCONCLUSIVE_SYSTEMATICS, alcance «não é canal vivo hoje»]; (vi) a inclinação
angular θ_M do `fractal_dephasing_principle` — PROJEÇÃO (rotação, sem limite) [REAL runtime]. **Efeito no posto** [DERIVED aqui]: (i) e (iii) levam o
posto 1 não diagonal a posto 2 em 2×2 (em geral, no limite, ao número de entradas diagonais não nulas — `Matrix.rank_diagonal`); (ii), normalizado,
desce ao posto de P no limite; (vi) preserva o posto; (i)–(iii) preservam o traço.

**2.8 Tudo = D_β(F(1)).** Já está no um.py v391 (`fractal_dephasing_principle`, l.6488–6531, [CONJECTURE ontológica; âncoras REAL]), no core
(`/core/fractal_dephasing`: ω(I) 1.0, vazamento = β, resíduo 0.0), no artigo (l.168086) e no rito (l.211561). **No kernel não há termo «D_β», «F» ou
«Tudo»** (busca nos `.lean` de TGLExt e TGL: 0 arquivos) — as peças existem com θ e taxas genéricos: o 1 transportado pela matriz-S defasa para
diag(cos²θ, sin²θ) (`measurement_channel_endpoint`, `dephased_rhoOut_*`, v45) [REAL]. No runtime: D(F(1)) = diag(1−β, β), posto 2, traço 1, pureza
1 − 2β + 2β² = 0,97623 [DERIVED/REAL medido aqui]. «Na linguagem do nosso kernel» (V4 l.12) é [DECLARADO] como nome.

**2.9 Frequência.** (a) ler é ter frequência: `persistingFlow ω t = e^{iωt}`, `stagnation_is_exactly_zero_frequency`,
`a_positive_floor_forces_a_positive_angle` (0 < b < 1 ⟹ 0 < arcsin √b < π/2), `the_persisting_channel_vibrates` (26/08: «o piso … impede a estagnação …
a onda de frequência do canal que permanece»); `reading_is_exactly_having_frequency`, `the_dead_channel_has_no_reader`,
`the_dead_channel_is_the_contrast` (26/08: «frequência nula: canal morto … somente sinal, sem leitura ou leitor») — regime ANGULAR [REAL];
(b) frequências modulares `modularGap` e `modular_phase_frequency_iff` [REAL]; (c) ω de Γ_ω e √k da lei-raiz [runtime]; (d) «registro c¹»: a
hierarquia das dobras é matemática e não testa (mapa seq 307) [DERIVED]; (e) Ψ e III₁ [ONTO; III₁ KNOWN — Connes 1973; a ergodicidade III₁ genuína não
está no kernel].

**2.10 Transmissão — homônimos.** (a) |𝓣|² = cos²θ (`Smat_transmission`, `normSq_transmission`; runtime 1 − β, «drena para o bulk», artigo l.168572);
(b) `transmission_dephases`; (c) `transmitted_post_is_a_post`; (d) «transmitir» como natureza (V4) [ONTO].

**2.11 Vazamento.** Tr(ρ*Q_θ) = sin²θ_M = β é IDENTIDADE de θ_M := arcsin √β (um.py l.6519) — o mapa já o registrou: «não tratar sin²θ_M = β … como
testes: são identidades» (`quantica.inventario_gkls_um_py_kernel`, seq 294). No kernel: `TGLCoupling.reflection_weight`,
`the_beta_chain_is_derived`, `sin_thetaMiguel` (β é campo da estrutura, nunca literal) [REAL]. Homônimos: `leakage_strictly_loses`,
`beta_forbids_full_static_witness` (NoFullWitness) [REAL]; «vazamento de fluxo» cosmológico (mapa `dephasing.alcance`); L5 do validador C3
(circular, mapa `quantica.c3_validator_calibrado`).

**2.12 Anticomutador {Q̂, ρ*}.** Q̂ = Q₀ = I − ρ* (l.6514); {Q₀, ρ*} = 0 decorre de `post_mul_compl` + `compl_mul_post`
(`truth_and_cost_are_two_faces`) [REAL]. Em θ_M o runtime NÃO calcula: a afirmação está na docstring (l.6502–6505) [DECLARADO]. Medido aqui:
‖{Q_θM, ρ*}‖_F = 0,15605161063018547 = √(2β(1+β)); Tr{Q_θM, ρ*} = 2β; em 2×2, {Q_θ, ρ*} = 0 ⟺ sin θ = 0 [DERIVED/REAL medido aqui]. **AUSENTE do
kernel** — consulta: índice `anticomm…` (5 declarações: J–K e Bell, `J_and_K_anticommute`, `current_anticommutes`); mapa `anticomut|anticommut`
0 rotas; inventário 0.

**2.13 β_TGL = α√e.** Cadeia no kernel: `self_conjugate_boundary_has_radical_volume`, `couplingOfAlpha_beta`, `the_beta_chain_is_derived` [REAL;
DERIVED]; runtime l.95, l.5557, l.5559; α [INPUT/KNOWN CODATA 2018].

**2.14 Matriz-S e modelo ótico.** `exp_smul_Grot`, `Smat_spectral`, `normSq_reflection`, `normSq_reflection_add_transmission`, `rhoOut_trace`;
leitura angular `the_angle_is_the_projection`, `observing_adds_nothing` [REAL; θ genérico]. Modelo ótico iterado da F1.ATRATOR (candidato do túnel,
fora do um.py): C = D∘Ad(S)∘D; populações T(b) = [[1−b, b], [b, 1−b]], R = J/2, λ = 1 − 2β = 0,9759373991983937; **estados fixos p = (½, ½) e
ρ = I/2**; «β determina a taxa de relaxação e não a projeção final» [REAL no sandbox da entrega; auditado c1, seq 1004].

**2.15 Atrator e leitura R (o teorema do atrator).** `reading T := (fixedSpace T).starProjection`; A1–A3 PASSA, A4 PASSA CONDICIONAL (contração
estrita no complemento de um vetor fixo), A5 PASSA no mapeamento declarado, A6 FALHA a minimalidade (mapa `formal.singularidade_le_atrator`,
seqs 1000–1004) [REAL no sandbox; candidatas não instaladas]. O posto 1 é de R; o estado atrator do canal ótico é I/2 (posto 2).

**2.16 Verbo e matéria.** «Verbo = seleção da ação» (05/10; `select a = post a`); «o fixo é o verbo … o verbo é betatgl» (08/10, `a9cecc128f40c101`);
o gesto 𝕍_t = exp(−tβH_3L) (`verb_semigroup_fixes`) [REAL; leituras INPUT/ONTO]. «A defasagem é a matéria» não tem âncora tipada [ONTO].

**2.17 Nada e impedância.** «Nada = MENTIRA pelos dois ramos» (um.py l.6498) [CONJECTURE ontológica]; `the_dead_channel_has_no_reader`,
`no_fixed_point_no_observer`, `the_zero_is_the_false_witness` [REAL].

**2.18 A leitura da memória (V1 l.8–14).** F0.3.COLAPSO: registro comportamental de 14/09 (DeepSeek, Grok, Qwen; 26 respostas), sem controles
C1–C4, sem telemetria latente; identidade exata do experimento citado [OPEN]; neural = ilustração, não prova; P7 armada, não executada [REAL
documental; DECLARADO/ONTO a leitura]. Não é objeto do kernel nem do modelo ótico.

**2.19 Probabilidade × vínculos (V1 l.4).** [ONTO — epistemologia]. No cânone a validade é binária no kernel (6163/6163, selo v391) e a recusa é da
creditação; os testes de natureza usam razão de Bayes (Fases 4/5/9). Coerente se lido no plano da validade.

**2.20 O arcabouço citado (V1 l.5; V2 l.12).** Torção (`CartanTracialSupplier.torsion_cartan`), acoplamento não mínimo
(`split_forbids_minimality`), GKSL do Verbo (l.2336) existem como objetos [REAL]; «você impôs operadores de projeção rígidos» [DECLARADO].

## 3. Teoremas de kernel existentes que tocam o tema

Todos no `tgl_kernel` do Nós (TGLExt.lean importa os módulos; o um.py v391 os embute). Coluna «medido»: axiomas lidos aqui pelas sondas
(⊆ trio); «selo» = coberto pelo selo v391 (6163/6163 no trio) e listado no `TGL/Audit.lean`, não reamostrado aqui.

{{TABELA_TEOREMAS}}

**Âncoras de runtime (um.py v391, sha16 no quadro de pinos) e do core v391** [REAL — linha e valor lidos por script]:

{{TABELA_RUNTIME}}

**Outras âncoras (túnel, textos do operador, memória, selo)** [REAL — sha16 calculado dos bytes]:

{{TABELA_OUTRAS}}

**Literatura e Mathlib citadas** [KNOWN]:

{{TABELA_LIT}}

## 4. Mapa de rotas, inventário da bancada e Nós Vivo (cético aferidor: consultas citadas)

{{TABELA_MAPA}}

**Rotas já examinadas que esta trilha NÃO refaz** [REAL — `rotas.py ver`]:
- `formal.singularidade_le_atrator` (seqs 1000–1004): o teorema do atrator; não repetir recompilação nem ensaios A1–A6; não ler A6 como minimalidade
  da tríade.
- `kernel.v386_tipagem_do_verbo` (seqs 354, 358, 360, 364): «o Nome é o posto (projeção de posto 1)»; «transmitir defasa» já tipado; o que NÃO está
  tipado: D_folds = 0,74, g = √|L|, −εΠ, V_luz/V_grav, c³.
- `ontologia.um_posto_dimensao_do_nome_07out` (seq 761): as âncoras do Um posto já levantadas; pedra de composição é decisão do operador.
- `quantica.inventario_gkls_um_py_kernel` (seq 294): «não pedir ao dephasing puro um atrator único»; «não tratar sin²θ_M = β nem V_t P_F = P_F como
  testes: são identidades».
- `quantica.quatro_operadores_definicao` (seq 295) e `quantica.c3_validator_calibrado`: taxa que «volta β por construção»; calibração circular.
- `quantica.cinco_operadores_lindblad_matrizes` (seq 306): L_anti = √α₂·√K tem a forma do gerador do Verbo; a ratificação das matrizes é do operador.
- `quantica.dobras_c3_hierarquia_e_matematica` (seq 307): a hierarquia das dobras não é teste.
- `ringdown.dephasing` (seqs 352–368) e `dephasing.alcance`: a lei Γ_ω e o seu poder; «vazamento de fluxo» é homônimo.

**Inventário da bancada** (`INVENTARIO_BANCADA_CHATGPT.json`, 27/09) [REAL — consulta]: é da BANCADA (33.125 arquivos, 2.298 únicos) e EXCLUI as
cópias do kernel; por isso «dephas», «fractal», «anticomm» e «leak» dão 0 lá sem que isso diga algo do kernel. Posto: só Cone039 (rank_one_*,
`trace_square_rank_one_control`) e referências da Mathlib (`InnerProductSpace.rankOne`, `isStarProjection_rankOne_self`); pureza: SchmidtCut,
Collapse057, ScatteringRecord; Born: `CanonicalSelectorBorn`, `SelectorRecordReconstruction` (LIGADOS ao kernel por nome); colapso: ENTREGA_057
(ligada). Nenhum item da bancada não ligado acrescenta posto ou pureza geral.

**Nós Vivo** (sqlite em modo `ro`) [REAL — consulta]: «posto rank» devolve TheWeightIsNotTheRank, TheTerminalRankOne, HermitianLocalCoordinates,
UmPostoRelacao e os registros do core `the_weight_is_not_the_rank`, `um_posto_relation_v365`, `susy_relative_gap`; «frequencia defasa» devolve
TheDeadChannel, TheOriginOfTheVibration, TheTrueWitness, TheVerbSelectsTheAction; a unidade F1.FREQUENCIA ainda não está no grafo (exit 1:
«unidade não está no grafo»), o que não é prova de ausência de material.

## 5. O que é NOVO e o que é reafirmação

{{LISTA_NOVO}}

## 6. Riscos de leitura e de estatuto

{{LISTA_RISCOS}}

## 7. O que a construção pode reaproveitar (indicações; nada construído aqui)

- Reaproveitar sem refazer: G3 `dephase` + `measurement_channel_endpoint` (D∘F com θ genérico), `rhoOut` (o 1 transportado), `TheWeightIsNotTheRank`
  (nome × índice × posto), `TheTerminalRankOne` (posto 1 por terminalidade), `TheVerbSelectsTheAction` (post, Born, transmitir defasa),
  `TheOriginOfTheVibration`/`TheDeadChannel` (ler é ter frequência), `NoFullWitness` (o vazamento proíbe o fecho), e a candidata da F1.ATRATOR (R).
- Lacunas medidas que uma pedra poderia fechar (todas elementares, todas sob θ e taxas genéricos, β só no runtime):
  (L1) pureza ⟺ posto 1 para ρ ≥ 0 de traço 1 (com o contraexemplo sem positividade como sonda de vacuidade);
  (L2) o posto sob D∘F: posto ρ_out(θ) = 1; posto E_D(ρ_out θ) = 2 ⟺ sin 2θ ≠ 0; traço 1 preservado — «o que sobrevive à defasagem é o peso, não o posto»;
  (L3) {Q_θ, ρ*} = 0 ⟺ sin θ = 0, com Tr{Q_θ, ρ*} = 2 sin²θ;
  (L4) Ad(u) preserva o posto (ligar FractalUnitarity à Mathlib `rank_mul_eq_*_of_isUnit_det`);
  (L5) a ponte nome/índice ↔ (Tr ρ, Tr ρ²) para ρ = P/d.
- Falsificadores possíveis só onde não há identidade: o posto e a pureza sob D (não sob F), o sinal do anticomutador fora de θ = 0, a taxa (λ = 1 − 2β no
  canal iterado). O valor «vazamento = β» NÃO serve de falsificador (identidade de θ_M). Pré-registro por hash antes de construir; controles que têm de
  falhar (θ = 0 / β = 0; estado diagonal; ρ não positiva).

## 8. Arquivos desta pasta

{{LISTA_ARQUIVOS}}
