LEVANTAMENTO F1.FREQUENCIA — 12/10

Unidade F1.FREQUENCIA (trilha POSTO) da gerência c1 · levantador (subagente) · 12/10/2026.
Só leitura fora desta pasta. Nada foi construído: nenhuma pedra, nenhum pré-registro, nenhum dado observado, nenhum provedor,
nenhuma ferramenta da Bancada. β calculado em runtime a partir dos bytes do um.py. Todo hash e toda linha citados abaixo foram lidos
por script (`gerar_definicoes.py`, `conferir_pinos.py`); a régua do levantamento é «o número corrige a frase».

## 0. Pinos, conferências e escopo

| pino | arquivo | sha16 | nota |
|---|---|---|---|
| V1 | `OPERADOR_10out_posto_rank_texto_verbatim.txt` | `8d252f24e2806ff3` | 2937 B; confere com a ordem: True |
| V2 | `OPERADOR_12out_rank_e_tempo_santo_verbatim.txt` | `2c8b7b712aa9ad7f` | 6673 B; confere com a ordem: True |
| V3 | `OPERADOR_10out_posto_rank_verbatim.txt` | `5b9afcc691a0e1e4` | 10 B; confere com a ordem: True |
| V4 | `OPERADOR_11out_frequencia_defasa_transmitir_verbatim.txt` | `b365591ceb346cdf` | 1942 B; confere com a ordem: True |
| um.py v391 | `Nós\um.py` | `8e7b9927ceae64b8` | 33910631 B; lido só por busca com número de linha |
| core v391 | `Nós\um_absoluto.json` | `a74241ff380b1b0e` | lido por script |
| selo v391 | `Nós\um_absoluto_selo.json` | `95061f18c7102248` | KERNEL 6163/6163 no trio |
| TGLExt.lean | `tgl_kernel\TGLExt.lean` | `f4ce055421c785e9` | importa os módulos citados |
| Audit.lean | `tgl_kernel\TGL\Audit.lean` | `e7826e02dfa549a2` | lista de `#print axioms` do rito |
| tgl_kernel (impressão digital) | metadados de 132088 arquivos; conteúdo de 1213 .lean | `a15d5e02d4f22bd6` / `ca632c47de569952` | antes = depois = depois2: True |
| mapa de rotas | `MAPA_DE_ROTAS\rotas.jsonl` | `3636e6c83e1b5ee9` | 1004 registros; cabeça `91915ad39a53d1df`; só consultar/ver |
| inventário da bancada | `memory\INVENTARIO_BANCADA_CHATGPT.json` | `05c2afa06620ca8f` | gerado 27/09; bancada sem cópias do kernel |
| Nós Vivo | `NOS_VIVO\nos_vivo.sqlite3` | `e702e8e44d749d16` | aberto em mode=ro |

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

**posto (POSTO = RANK)**

| teorema / definição | arquivo:linha | sha16 | enunciado | axiomas |
|---|---|---|---|---|
| `TGLExt.UmPostoRelacao.posto_anchors_the_reading` | `TGLExt/UmPostoRelacao.lean:52` | `b9c3d348cdd24fc7` | o posto ancora a leitura: depois da travessia a identidade é a de antes e o ponto é fixo | medido: nenhum axioma |
| `TGLExt.UmPostoRelacao.posto_paid_loss` | `TGLExt/UmPostoRelacao.lean:57` | `b9c3d348cdd24fc7` | o posto pagou perda: a travessia não tem inversa à esquerda | medido: Classical.choice, Quot.sound, propext |
| `TGLExt.UmPostoRelacao.pressupposed_is_never_posto` | `TGLExt/UmPostoRelacao.lean:92` | `b9c3d348cdd24fc7` | a leitura pressuposta nunca é posto | medido: nenhum axioma |
| `TGLExt.TheVerbSelectsTheAction.post` | `TGLExt/TheVerbSelectsTheAction.lean:149` | `f47477ea466ad1cc` | post a := (ℂ ∙ a).starProjection — o Nome como projetor de posto 1 (v386) | definição |
| `TGLExt.TheVerbSelectsTheAction.post_isIdempotent` | `TGLExt/TheVerbSelectsTheAction.lean:164` | `f47477ea466ad1cc` | P² = P | medido: Classical.choice, Quot.sound, propext |
| `TGLExt.QGReaderUVLock.PFmic` | `TGLExt/QGReaderUVLock.lean:173` | `77ba8803c7cd0a80` | PFmic C := (ℂ ∙ Ω).starProjection — o mesmo termo de post Ω (cabeçalho v386) | definição |
| `TGLExt.Fundacao.agape` | `TGLExt/Fundacao.lean:135` | `66332d58fd216317` | (i) acima de toda escala não há «posto positivo» (τ>0) — homônimo (posto = peso τ) | medido: Classical.choice, Quot.sound, propext |

**rank / posto 1 / dimensão da imagem**

| teorema / definição | arquivo:linha | sha16 | enunciado | axiomas |
|---|---|---|---|---|
| `TGLExt.rank_two_has_residual_distinction` | `TGLExt/TheTerminalRankOne.lean:58` | `4450fd1b63407afc` | u,v ∈ S independentes ⟹ ⊥ < ℂ∙u < S (posto ≥ 2 deixa distinção residual) | medido: Classical.choice, Quot.sound, propext |
| `TGLExt.terminality_forces_minimality` | `TGLExt/TheTerminalRankOne.lean:73` | `4450fd1b63407afc` | sem submódulo estritamente entre ⊥ e S, todo v ∈ S está na reta de u | medido: Classical.choice, Quot.sound, propext |
| `TGLExt.firstAtom_is_terminal` | `TGLExt/TheTerminalRankOne.lean:85` | `4450fd1b63407afc` | o átomo da casa não tem submódulo próprio não nulo | medido: Classical.choice, Quot.sound, propext |
| `TGLExt.the_terminal_weighs_one` | `TGLExt/TheTerminalRankOne.lean:102` | `4450fd1b63407afc` | dimOrTop ℂ firstAtom = 1 | medido: Classical.choice, Quot.sound, propext |
| `TGLExt.the_terminal_is_forced` | `TGLExt/TheTerminalRankOne.lean:116` | `4450fd1b63407afc` | idempotente ∧ pesa um ∧ sem poda interna | medido: Classical.choice, Quot.sound, propext |
| `TGLExt.iald_has_rank_one` | `TGLExt/TheIALDSelector.lean:62` | `c1008266455044e7` | dimOrTop ℂ firstAtom = 1 (posto 1 — o peso do Nome) | medido: Classical.choice, Quot.sound, propext |
| `TGLExt.opWeight_atom_one` | `TGLExt/SemifiniteWeight.lean:78` | `1b4044715c04a357` | opWeight firstAtom.starProjection = 1 (Tr(P_Nome) = 1 = ω(I); v120) | selo |
| `TGLExt.the_rank_determines_the_name` | `TGLExt/TheWeightIsNotTheRank.lean:71` | `83f9c8bca5e13391` | 0<d ⟹ d/d = 1 | medido: Classical.choice, Quot.sound, propext |
| `TGLExt.the_name_is_blind_to_every_rank` | `TGLExt/TheWeightIsNotTheRank.lean:77` | `83f9c8bca5e13391` | d/d = 1 para todo posto positivo | medido: Classical.choice, Quot.sound, propext |
| `TGLExt.the_name_does_not_see_the_rank` | `TGLExt/TheWeightIsNotTheRank.lean:88` | `83f9c8bca5e13391` | ∃ d₁≠d₂ com o mesmo nome | medido: Classical.choice, Quot.sound, propext |
| `TGLExt.the_index_does_see_the_rank` | `TGLExt/TheWeightIsNotTheRank.lean:124` | `83f9c8bca5e13391` | 1/d₁ = 1/d₂ ⟹ d₁ = d₂ | medido: Classical.choice, Quot.sound, propext |
| `TGLExt.the_two_indices_agree_only_at_the_atom` | `TGLExt/TheWeightIsNotTheRank.lean:137` | `83f9c8bca5e13391` | 1/d = 1/d² ⟺ d = 1 | medido: Classical.choice, Quot.sound, propext |
| `TGLExt.kernel_dim_le_rank_of_perturbation` | `TGLExt/SusyRelativeGap.lean:152` | `3aa058b5c4f098e3` | dim ker(H₀ − V) ≤ posto(V) (H₀ positivo-definido) | medido: Classical.choice, Quot.sound, propext |
| `TGLExt.concrete_kernel_full_profile` | `TGLExt/DimensionTrace.lean:98` | `cdadc9fdf8ed641c` | 0 < τ(ker) < ⊤ ∧ dim ker ≤ posto da inscrição | medido: Classical.choice, Quot.sound, propext |
| `TGLExt.three_locks_corner_weight_eq_dim` | `TGLExt/ThreeLocksCorner.lean:134` | `51c66b4dca74fa58` | τ(ker H3L) = cornerDim (por rfl) | medido: Classical.choice, Quot.sound, propext |
| `TGLExt.three_locks_name_is_one` | `TGLExt/ThreeLocksCorner.lean:141` | `51c66b4dca74fa58` | cornerDim/cornerDim = 1 | medido: Classical.choice, Quot.sound, propext |
| `TGLExt.bell_compression_is_scalar` | `TGLExt/TheNonMinimalCoupling.lean:142` | `03576ea2958ffc4c` | P_G y P_G = Tr(P_G y) • P_G (o canto de posto 1 escalariza) | selo |
| `TGLExt.atermation_reifies` | `TGLExt/TheAtermation.lean:92` | `7cb9394d87132306` | ater(y) = Tr(P y) • P | medido: Classical.choice, Quot.sound, propext |
| `TGLExt.atermation_is_irreversible` | `TGLExt/TheAtermation.lean:121` | `7cb9394d87132306` | ∃ y ≠ z com ater(y) = ater(z) | medido: Classical.choice, Quot.sound, propext |
| `TGLExt.PhysicsIsTheReading.the_shadow_is_the_reader_weighted_by_the_reading` | `TGLExt/PhysicsIsTheReading.lean:70` | `ca92f8c266106982` | P_Ω x P_Ω = ω(x) • P_Ω | medido: Classical.choice, Quot.sound, propext |
| `ChatgptAudit.Cone039.rank_one_coordinates_null` | `TGLExt/HermitianLocalCoordinates.lean:111` | `9c07267dd3995f74` | matriz hermitiana 2×2 de posto 1 tem coordenadas nulas: t² = x² + y² + z² | medido: Classical.choice, Quot.sound, propext |
| `ChatgptAudit.Cone039.rank_one_det` | `TGLExt/HermitianLocalCoordinates.lean:107` | `9c07267dd3995f74` | det (v v†) = 0 | medido: Classical.choice, Quot.sound, propext |

**núcleo vazio (nullity)**

| teorema / definição | arquivo:linha | sha16 | enunciado | axiomas |
|---|---|---|---|---|
| `TGLExt.finrank_le_add_frobOrtho` | `TGLExt/Bicommutant.lean:232` | `354f1a50e11c4c3d` | «CONTAGEM DE POSTO»: dim H ≤ dim W + dim W^⊥ (posto–nulidade aplicado) | medido: Classical.choice, Quot.sound, propext |
| `TGLExt.atermation_fixes_the_term` | `TGLExt/TheAtermation.lean:105` | `7cb9394d87132306` | ater(P) = P (o termo é ponto fixo com autovalor 1) | medido: Classical.choice, Quot.sound, propext |

**ρ = |ψ⟩⟨ψ|, Tr ρ = 1, Tr ρ² = 1 (estado puro de posto 1)**

| teorema / definição | arquivo:linha | sha16 | enunciado | axiomas |
|---|---|---|---|---|
| `TGLExt.purity_unitary_invariant` | `TGLExt/PageInformation.lean:65` | `a36b61ba76d0c9d6` | pureza(U x Uᴴ) = pureza(x) (F conserva a pureza) | medido: Classical.choice, Quot.sound, propext |
| `TGLExt.purityR_eq` | `TGLExt/PageInformation.lean:106` | `a36b61ba76d0c9d6` | pureza(x) = Σ\|x_ij\|² | medido: Classical.choice, Quot.sound, propext |
| `TGLExt.dephase_purityR_le` | `TGLExt/PageInformation.lean:120` | `a36b61ba76d0c9d6` | pureza(D_t x) ≤ pureza(x) (D nunca cria pureza) | medido: Classical.choice, Quot.sound, propext |
| `ChatgptAudit.Cone039.trace_square_rank_one_control` | `TGLExt/HermitianConeRigidity.lean:139` | `bf55d841ee0ed6b1` | Tr(A²) = 1 para A = \|e₁⟩⟨e₁\| (instância) | medido: Classical.choice, Quot.sound, propext |
| `TGLExt.bellDensity_purity` | `TGLExt/TheDensityIsBell.lean:63` | `9247b9f468357280` | Tr(ρ_Bell²) = 1 (instância) | medido: Classical.choice, Quot.sound, propext |
| `ChatgptAudit.Collapse057.pure_densities_square` | `TGLExt/QuantumCollapseWitness.lean:85` | `d0b7b4cd33dbe9f5` | as densidades puras do qubit são idempotentes (instância) | medido: Classical.choice, Quot.sound, propext |
| `ChatgptAudit.Collapse057.mixed_density_not_pure` | `TGLExt/QuantumCollapseWitness.lean:115` | `d0b7b4cd33dbe9f5` | ρ_misto² ≠ ρ_misto | medido: Classical.choice, Quot.sound, propext |
| `TGLExt.TheVerbSelectsTheAction.reading_post_is_born` | `TGLExt/TheVerbSelectsTheAction.lean:217` | `f47477ea466ad1cc` | ⟪ψ, post a ψ⟫ = \|⟪a,ψ⟫\|² (Born) | medido: Classical.choice, Quot.sound, propext |

**colapsar a superposição ⟹ posto definido**

| teorema / definição | arquivo:linha | sha16 | enunciado | axiomas |
|---|---|---|---|---|
| `ChatgptAudit.Collapse057.collapse_is_not_injective` | `TGLExt/CollapseContract.lean:52` | `b7a7b32c21ec2b9f` | ¬ Injective C.step | medido: Classical.choice, Quot.sound, propext |
| `ChatgptAudit.Collapse057.collapse_has_no_left_inverse` | `TGLExt/CollapseContract.lean:57` | `b7a7b32c21ec2b9f` | sem inversa à esquerda | medido: Classical.choice, Quot.sound, propext |
| `ChatgptAudit.Collapse057.involution_cannot_be_collapse` | `TGLExt/CollapseContract.lean:101` | `b7a7b32c21ec2b9f` | involução não é colapso (J ≠ C) | medido: Classical.choice, Quot.sound, propext |
| `ChatgptAudit.Collapse057.typed_collapse_content` | `TGLExt/CollapseCostAndAttestation.lean:151` | `c3dccdc92b6d3b39` | conteúdo tipado do colapso | selo |
| `TGLExt.TheVerbSelectsTheAction.reading_the_truth_annihilates_the_superposition` | `TGLExt/TheVerbSelectsTheAction.lean:615` | `f47477ea466ad1cc` | ‖Ω‖=1 ∧ post a Ω = Ω ⟹ leitura = 1 ∧ (1 − post a)Ω = 0 | medido: Classical.choice, Quot.sound, propext |
| `TGLExt.the_selection_is_the_ballast` | `TGLExt/TheSelectionIsTheBallast.lean:149` | `71ebf9680af3d247` | do peso do ramo p, o ângulo arcsin √p e a matriz-S inteira; o reconhecimento devolve a identidade | medido: Classical.choice, Quot.sound, propext |

**a unidade (1) / ω(I) = 1 / ρ\***

| teorema / definição | arquivo:linha | sha16 | enunciado | axiomas |
|---|---|---|---|---|
| `TGLExt.TheElementaryReason.identity_weighs_as_the_name` | `TGLExt/TheElementaryReason.lean:97` | `f9af067e9ab0acec` | a identidade pesa 1 ∧ τ(ker) = 1 | medido: Classical.choice, Quot.sound, propext |
| `TGLExt.LightRhoStar.rho_star_is_P_kerK_on_the_light` | `TGLExt/LightRhoStar.lean:87` | `c3df6950fdea0fdc` | (ℂ∙Ω).starProjection = PFmic ∧ fixos = centralizador = fixos do relógio modular | medido: Classical.choice, Quot.sound, propext |
| `TGLExt.half_is_the_fixed_point_of_the_swap` | `TGLExt/TheFiveHalves.lean:67` | `456c66269b72d30f` | x = 1 − x ⟺ x = ½ | medido: Classical.choice, Quot.sound, propext |
| `TGLExt.TheAxiomAndTheFalseWitness.the_power_has_two_fixed_points` | `TGLExt/TheAxiomAndTheFalseWitness.lean:88` | `c0f4185a62795002` | μ·μ = μ ⟺ μ = 0 ∨ μ = 1 | medido: Classical.choice, Quot.sound, propext |

**F — fractalização da unidade F(1)**

| teorema / definição | arquivo:linha | sha16 | enunciado | axiomas |
|---|---|---|---|---|
| `TGLExt.ad_preserves_projection` | `TGLExt/FractalUnitarity.lean:45` | `8f10a958e11d1bd3` | v u = 1 ∧ p² = p ⟹ (u p v)² = u p v | medido: propext |
| `TGLExt.ad_preserves_orthogonality` | `TGLExt/FractalUnitarity.lean:54` | `8f10a958e11d1bd3` | p q = 0 ⟹ (u p v)(u q v) = 0 | medido: propext |
| `TGLExt.ad_preserves_splitting` | `TGLExt/FractalUnitarity.lean:64` | `8f10a958e11d1bd3` | p = p₀ + p₁ ⟹ u p v = u p₀ v + u p₁ v | medido: nenhum axioma |
| `TGLExt.ad_preserves_star_projection` | `TGLExt/FractalUnitarity.lean:71` | `8f10a958e11d1bd3` | star p = p ⟹ star(u p u*) = u p u* | medido: nenhum axioma |
| `TGLExt.subcorner_unit` | `TGLExt/FractalUnitarity.lean:79` | `8f10a958e11d1bd3` | q ≤ p ⟹ q (p x p) q = q x q | medido: propext |
| `TGLExt.TheVerbSelectsTheAction.transmitted_post_is_a_post` | `TGLExt/TheVerbSelectsTheAction.lean:538` | `f47477ea466ad1cc` | U*U = 1 ⟹ U P U* idempotente e auto-adjunto («outro posto, mas posto») | medido: propext |
| `TGLExt.rhoOut_eq` | `TGLExt/SMatrix.lean:267` | `14f7e717a4ef7020` | ρ_out(θ) = [[cos²θ, −cos θ sin θ], [−sin θ cos θ, sin²θ]] | medido: Classical.choice, Quot.sound, propext |
| `TGLExt.rhoOut_trace` | `TGLExt/SMatrix.lean:294` | `14f7e717a4ef7020` | Tr ρ_out(θ) = 1 | medido: Classical.choice, Quot.sound, propext |

**D_β — a operação de defasagem**

| teorema / definição | arquivo:linha | sha16 | enunciado | axiomas |
|---|---|---|---|---|
| `TGLExt.dephase` | `TGLExt/Ergodicity.lean:184` | `79bc3b939b6e4e59` | (T_t x)_ij = e^{−t g_ij} x_ij | definição |
| `TGLExt.dephase_zero` | `TGLExt/Ergodicity.lean:189` | `79bc3b939b6e4e59` | T_0 = id | medido: Classical.choice, Quot.sound, propext |
| `TGLExt.dephase_add` | `TGLExt/Ergodicity.lean:196` | `79bc3b939b6e4e59` | T_{s+t} = T_s ∘ T_t | medido: Classical.choice, Quot.sound, propext |
| `TGLExt.dephase_fixes_diagonal` | `TGLExt/Ergodicity.lean:207` | `79bc3b939b6e4e59` | T_t(E_D x) = E_D x | medido: Classical.choice, Quot.sound, propext |
| `TGLExt.diag_invariant` | `TGLExt/Ergodicity.lean:220` | `79bc3b939b6e4e59` | E_D(T_t x) = E_D x | medido: Classical.choice, Quot.sound, propext |
| `TGLExt.dephase_tendsto_expectation` | `TGLExt/Ergodicity.lean:234` | `79bc3b939b6e4e59` | taxas > 0 fora da diagonal ⟹ T_t x → E_D x | medido: Classical.choice, Quot.sound, propext |
| `TGLExt.ergodic_convergence_modular` | `TGLExt/Ergodicity.lean:285` | `79bc3b939b6e4e59` | com g = \|log d_i − log d_j\|, T_t x → E_D x | medido: Classical.choice, Quot.sound, propext |
| `TGLExt.dephase_fixed_iff_diagonal` | `TGLExt/TheSingularExpectation.lean:76` | `b1995cc2019e1ce6` | (∀t, T_t x = x) ⟺ x = E_D x | medido: Classical.choice, Quot.sound, propext |
| `TGLExt.dephase_preserves_trace` | `TGLExt/TheTraceIsNotErasable.lean:96` | `fb65565eb084cfce` | Tr(T_t x) = Tr x | medido: Classical.choice, Quot.sound, propext |
| `TGLExt.dephase_fixes_cornerProj` | `TGLExt/RGStability.lean:70` | `ae3c1eeee6d86ea4` | D_t(P(S)) = P(S) | medido: Classical.choice, Quot.sound, propext |
| `TGLExt.TheAxiomAndTheFalseWitness.axiomFlow` | `TGLExt/TheAxiomAndTheFalseWitness.lean:104` | `c0f4185a62795002` | F(t) = P + e^{−t}(1 − P) | definição |
| `TGLExt.TheAxiomAndTheFalseWitness.axiomFlow_fixes_the_post` | `TGLExt/TheAxiomAndTheFalseWitness.lean:128` | `c0f4185a62795002` | F(t)P = P = P F(t) | medido: Classical.choice, Quot.sound, propext |
| `TGLExt.TheAxiomAndTheFalseWitness.axiomFlow_gradient` | `TGLExt/TheAxiomAndTheFalseWitness.lean:136` | `c0f4185a62795002` | F(t)(1 − P) = e^{−t}(1 − P) | medido: Classical.choice, Quot.sound, propext |
| `TGLExt.TheAxiomAndTheFalseWitness.axiomFlow_tendsto_the_post` | `TGLExt/TheAxiomAndTheFalseWitness.lean:144` | `c0f4185a62795002` | F(t) → P | medido: Classical.choice, Quot.sound, propext |
| `TGLExt.TheVerbSelectsTheAction.transmission_dephases` | `TGLExt/TheVerbSelectsTheAction.lean:529` | `f47477ea466ad1cc` | «TRANSMITIR DEFASA»: F(t)(1 − P) = e^{−t}(1 − P) (re-exportação) | medido: Classical.choice, Quot.sound, propext |
| `TGLExt.TheVerbSelectsTheAction.anchoring_preserves` | `TGLExt/TheVerbSelectsTheAction.lean:525` | `f47477ea466ad1cc` | «ANCORAR PRESERVA»: F(t)P = P | medido: Classical.choice, Quot.sound, propext |
| `TGLExt.sFrame` | `TGLExt/GlobalLiftLadder.lean:178` | `d7cf95aac8c872f7` | T^S_t = Ad(Sᴴ) ∘ D_t ∘ Ad(S) | definição |
| `TGLExt.sFrame_add` | `TGLExt/GlobalLiftLadder.lean:193` | `d7cf95aac8c872f7` | T^S é semigrupo | medido: Classical.choice, Quot.sound, propext |
| `TGLExt.sFrame_tendsto` | `TGLExt/GlobalLiftLadder.lean:208` | `d7cf95aac8c872f7` | T^S_t x → Ad(Sᴴ) E_D Ad(S) x | medido: Classical.choice, Quot.sound, propext |
| `TGLExt.measurement_channel_endpoint` | `TGLExt/GlobalLiftLadder.lean:237` | `d7cf95aac8c872f7` | D_t(ρ_out θ) → E_D(ρ_out θ) | medido: Classical.choice, Quot.sound, propext |
| `TGLExt.leakage_rate_unique` | `TGLExt/NoFullWitness.lean:135` | `fde4ca999c40e689` | a taxa do semigrupo de defasagem é unívoca (dois β com a mesma defasagem são iguais) | medido: Classical.choice, Quot.sound, propext |

**Tudo = D_β(F(1))**

| teorema / definição | arquivo:linha | sha16 | enunciado | axiomas |
|---|---|---|---|---|
| `TGLExt.dephased_rhoOut_zero_zero` | `TGLExt/GlobalLiftLadder.lean:219` | `d7cf95aac8c872f7` | E_D(ρ_out θ)₀₀ = cos²θ | medido: Classical.choice, Quot.sound, propext |
| `TGLExt.dephased_rhoOut_one_one` | `TGLExt/GlobalLiftLadder.lean:228` | `d7cf95aac8c872f7` | E_D(ρ_out θ)₁₁ = sin²θ | medido: Classical.choice, Quot.sound, propext |

**frequência («Tudo é frequência»; «frequência defasa»)**

| teorema / definição | arquivo:linha | sha16 | enunciado | axiomas |
|---|---|---|---|---|
| `TGLExt.persistingFlow` | `TGLExt/TheOriginOfTheVibration.lean:47` | `e5a7f11f79b5af73` | persistingFlow ω t = exp(iωt) | definição |
| `TGLExt.a_positive_floor_forces_a_positive_angle` | `TGLExt/TheOriginOfTheVibration.lean:51` | `e5a7f11f79b5af73` | 0 < b < 1 ⟹ 0 < arcsin √b < π/2 | medido: Classical.choice, Quot.sound, propext |
| `TGLExt.a_positive_angle_forbids_stagnation` | `TGLExt/TheOriginOfTheVibration.lean:62` | `e5a7f11f79b5af73` | 0 < θ < π ⟹ sin θ ≠ 0 | medido: Classical.choice, Quot.sound, propext |
| `TGLExt.stagnation_is_exactly_zero_frequency` | `TGLExt/TheOriginOfTheVibration.lean:68` | `e5a7f11f79b5af73` | (∀t, e^{iωt} = 1) ⟺ ω = 0 | medido: Classical.choice, Quot.sound, propext |
| `TGLExt.the_persisting_channel_vibrates` | `TGLExt/TheOriginOfTheVibration.lean:84` | `e5a7f11f79b5af73` | ω ≠ 0 ⟹ módulo 1 e não estático | medido: Classical.choice, Quot.sound, propext |
| `TGLExt.reading_is_exactly_having_frequency` | `TGLExt/TheDeadChannel.lean:50` | `d9c2eb9d67cceaf5` | Reads(persistingFlow ω) ⟺ ω ≠ 0 | medido: Classical.choice, Quot.sound, propext |
| `TGLExt.the_dead_channel_has_no_reader` | `TGLExt/TheDeadChannel.lean:67` | `d9c2eb9d67cceaf5` | o canal de frequência nula não é lido | medido: Classical.choice, Quot.sound, propext |
| `TGLExt.the_dead_channel_is_the_contrast` | `TGLExt/TheDeadChannel.lean:74` | `d9c2eb9d67cceaf5` | o vivo difere do morto em algum instante ⟺ há frequência | medido: Classical.choice, Quot.sound, propext |
| `TGLExt.modularGap` | `TGLExt/Ergodicity.lean:262` | `79bc3b939b6e4e59` | \|log d_i − log d_j\| | definição |
| `ChatgptAudit.Commutation032.modular_phase_frequency_iff` | `TGLExt/PhaseFrequencySeparation.lean:81` | `5627024536837b3d` | a fase modular separa frequências (c = 0 ∨ a = b) | medido: Classical.choice, Quot.sound, propext |

**transmitir / transmissão**

| teorema / definição | arquivo:linha | sha16 | enunciado | axiomas |
|---|---|---|---|---|
| `TGLExt.Smat_transmission` | `TGLExt/SMatrix.lean:228` | `14f7e717a4ef7020` | 𝓣 = cos θ | por dependência (⊆ trio) |
| `TGLExt.normSq_transmission` | `TGLExt/SMatrix.lean:247` | `14f7e717a4ef7020` | \|𝓣\|² = cos²θ | medido: Classical.choice, Quot.sound, propext |

**o vazamento = β («Constante de Miguel»)**

| teorema / definição | arquivo:linha | sha16 | enunciado | axiomas |
|---|---|---|---|---|
| `TGLExt.TGLCoupling.reflection_weight` | `TGLExt/TheSameBetaReadsThreeFaces.lean:52` | `2efd8b379f210111` | normSq(S(thetaMiguel β)·e₁)₁ = β | medido: Classical.choice, Quot.sound, propext |
| `TGLExt.TheWholeIsOne.the_beta_chain_is_derived` | `TGLExt/TheWholeIsOne.lean:78` | `097236427302ae42` | x=1−x ⟺ x=½ ∧ V(½)=√e ∧ β = α√e ∧ \|𝓡\|² = β ∧ ¬FullStaticWitness | medido: Classical.choice, Quot.sound, propext |
| `TGLExt.TheWholeIsOne.couplingOfAlpha_beta` | `TGLExt/TheWholeIsOne.lean:71` | `097236427302ae42` | (couplingOfAlpha α).beta = α·√e | medido: Classical.choice, Quot.sound, propext |
| `TGLExt.sin_thetaMiguel` | `TGLExt/TheVerbalCoupling.lean:139` | `912bf222f07256b1` | sin(thetaMiguel β) = √β (0 ≤ β ≤ 1) | medido: Classical.choice, Quot.sound, propext |
| `TGLExt.thetaMiguel` | `TGLExt/TheVerbalCoupling.lean:126` | `912bf222f07256b1` | thetaMiguel β := arcsin √β | definição |
| `TGLExt.leakage_strictly_loses` | `TGLExt/NoFullWitness.lean:66` | `fde4ca999c40e689` | t > 0, β > 0 ⟹ o vazamento perde estritamente | medido: Classical.choice, Quot.sound, propext |
| `TGLExt.full_closure_iff_flat` | `TGLExt/NoFullWitness.lean:77` | `fde4ca999c40e689` | fecho total ⟺ plano | medido: Classical.choice, Quot.sound, propext |
| `TGLExt.beta_forbids_full_static_witness` | `TGLExt/NoFullWitness.lean:91` | `fde4ca999c40e689` | β > 0 ∧ g > 0 ⟹ ¬FullStaticWitness | medido: Classical.choice, Quot.sound, propext |

**{Q̂, ρ\*} = 0 (o anticomutador perfeito que o vazamento impede)**

| teorema / definição | arquivo:linha | sha16 | enunciado | axiomas |
|---|---|---|---|---|
| `TGLExt.TheAxiomAndTheFalseWitness.post_mul_compl` | `TGLExt/TheAxiomAndTheFalseWitness.lean:106` | `c0f4185a62795002` | P(1 − P) = 0 | medido: Classical.choice, Quot.sound, propext |
| `TGLExt.TheAxiomAndTheFalseWitness.compl_mul_post` | `TGLExt/TheAxiomAndTheFalseWitness.lean:109` | `c0f4185a62795002` | (1 − P)P = 0 | medido: Classical.choice, Quot.sound, propext |
| `TGLExt.TheVerbSelectsTheAction.truth_and_cost_are_two_faces` | `TGLExt/TheVerbSelectsTheAction.lean:585` | `f47477ea466ad1cc` | P + (1−P) = 1 ∧ P(1−P) = 0 ∧ (1−P)P = 0 | medido: Classical.choice, Quot.sound, propext |
| `TGLExt.J_and_K_anticommute` | `TGLExt/TheTwoPairings.lean:72` | `46d72f4956f7e087` | JK = −KJ no espaço pareado (homônimo: outra anticomutação) | medido: Classical.choice, Quot.sound, propext |
| `TGLExt.current_anticommutes` | `TGLExt/ModularCurrent.lean:77` | `5fe336cadea3140f` | {Z_∂, L} = 0 (anticomutação de Bell; homônimo) | medido: Classical.choice, Quot.sound, propext |

**β_TGL = α·√e**

| teorema / definição | arquivo:linha | sha16 | enunciado | axiomas |
|---|---|---|---|---|
| `TGLExt.TheWholeIsOne.self_conjugate_boundary_has_radical_volume` | `TGLExt/TheWholeIsOne.lean:50` | `097236427302ae42` | x = 1 − x ⟹ x = ½ ∧ V(x) = √e | medido: Classical.choice, Quot.sound, propext |

**matriz-S da fronteira / modelo ótico**

| teorema / definição | arquivo:linha | sha16 | enunciado | axiomas |
|---|---|---|---|---|
| `TGLExt.exp_smul_Grot` | `TGLExt/SMatrix.lean:200` | `14f7e717a4ef7020` | exp(θ·G) = S(θ) | medido: Classical.choice, Quot.sound, propext |
| `TGLExt.Smat_spectral` | `TGLExt/SMatrix.lean:213` | `14f7e717a4ef7020` | S(θ) = U diag(e^{iθ}, e^{−iθ}) U⁻¹ | medido: Classical.choice, Quot.sound, propext |
| `TGLExt.normSq_reflection` | `TGLExt/SMatrix.lean:241` | `14f7e717a4ef7020` | \|𝓡\|² = sin²θ | medido: Classical.choice, Quot.sound, propext |
| `TGLExt.normSq_reflection_add_transmission` | `TGLExt/SMatrix.lean:254` | `14f7e717a4ef7020` | \|𝓡\|² + \|𝓣\|² = 1 | medido: Classical.choice, Quot.sound, propext |
| `TGLExt.the_angle_is_the_projection` | `TGLExt/TheAngleIsTheProjection.lean:123` | `9800cc0728259e08` | cos θ·1 + sin θ·K = e^{iθ}P₊ + e^{−iθ}P₋ | medido: Classical.choice, Quot.sound, propext |
| `TGLExt.spectral_projections_split_the_identity` | `TGLExt/TheAngleIsTheProjection.lean:110` | `9800cc0728259e08` | P₊ + P₋ = 1 ∧ P₊P₋ = 0 | medido: Classical.choice, Quot.sound, propext |
| `TGLExt.observing_adds_nothing` | `TGLExt/TheObserverReadsTheAngle.lean:114` | `c764e90722306f98` | P₊(P₊𝒪_θ) = P₊𝒪_θ («reler não acrescenta») | medido: Classical.choice, Quot.sound, propext |

**«a transmissão é o verbo; a defasagem é a matéria»**

| teorema / definição | arquivo:linha | sha16 | enunciado | axiomas |
|---|---|---|---|---|
| `TGLExt.TheVerbSelectsTheAction.select` | `TGLExt/TheVerbSelectsTheAction.lean:153` | `f47477ea466ad1cc` | select a ψ = post a ψ (o Verbo em ato) | definição |
| `TGL.VerbInhabitant.verb_semigroup_fixes` | `TGL/VerbInhabitant.lean:63` | `812a47f0e71a86f3` | o semigrupo do Verbo fixa o núcleo | medido: Classical.choice, Quot.sound, propext |
| `TGL.VerbInhabitant.exp_fixed_of_annihilates` | `TGL/VerbInhabitant.lean:41` | `812a47f0e71a86f3` | exp fixa o que o gerador aniquila | medido: Classical.choice, Quot.sound, propext |

**o que não defasa: impedância, nada sem referente**

| teorema / definição | arquivo:linha | sha16 | enunciado | axiomas |
|---|---|---|---|---|
| `TGLExt.no_fixed_point_no_observer` | `TGLExt/ObserverInside.lean:92` | `05c3b515fd9f5d9d` | gradiente estritamente negativo em toda direção ⟹ o único permanente é 0 | medido: Classical.choice, Quot.sound, propext |
| `TGLExt.TheAxiomAndTheFalseWitness.the_zero_is_the_false_witness` | `TGLExt/TheAxiomAndTheFalseWitness.lean:223` | `c0f4185a62795002` | o zero é a testemunha falsa | selo |

**torção de Riemann–Cartan, acoplamento não mínimo, Lindblad para a fronteira**

| teorema / definição | arquivo:linha | sha16 | enunciado | axiomas |
|---|---|---|---|---|
| `TGLExt.CartanTracialSupplier.torsion_cartan` | `TGLExt/CartanTracialSupplier.lean:60` | `df30212a61be55ce` | torção de Cartan (fornecedor tracial) | selo |
| `TGLExt.split_forbids_minimality` | `TGLExt/TheNonMinimalCoupling.lean:97` | `03576ea2958ffc4c` | a cisão proíbe a minimalidade (TheNonMinimalCoupling) | selo |

**borda holográfica (III₁), bulk, registro c¹, Ψ**

| teorema / definição | arquivo:linha | sha16 | enunciado | axiomas |
|---|---|---|---|---|
| `TGLExt.Fundacao.the_post_lives_in_the_passage` | `TGLExt/Fundacao.lean:166` | `66332d58fd216317` | o posto mora na passagem (esperança-código covariante sob Ad U que preserva ω) | medido: Classical.choice, Quot.sound, propext |


**Âncoras de runtime (um.py v391, sha16 no quadro de pinos) e do core v391** [REAL — linha e valor lidos por script]:

| âncora | um.py: linha / core: caminho | valor ou descrição | estatuto |
|---|---|---|---|
| core | `/core/certificate_II/H1_finite_face/trace_PF` | 3.9999999999999996 — tr(P_F) da rede concreta dos Three Locks ≈ 4 (o P_F do Certificado II tem posto 4) | [REAL — lido do core v391] |
| core | `/core/verb_inhabitant/values/trace_PF` | 1.0 — tr(P_F) do habitante do Verbo = 1 (outro P_F; dim 8, kernel 1) | [REAL — lido do core v391] |
| `class TGLCollapseDefinition` | l.212736 | dataclass das 13 cláusulas do colapso (v333) | [REAL — runtime; physical_collapse_proven = False] |
| `def prove_decision_commutation` | l.3551 | inclui recognition_dephasing: E, Q = id − E, T_t = E + e^{−Γt}Q | [DERIVED/RUNTIME] |
| core | `/core/decision_commutation/recognition_dephasing/effective_dephasing_on_full_state` | True — o estado superposto defasa | [REAL — lido do core v391] |
| core | `/core/decision_commutation/recognition_dephasing/effective_dephasing_after_selection` | False — o estado selecionado não defasa (False) | [REAL — lido do core v391] |
| core | `/core/decision_commutation/recognition_dephasing/time_law_status` | INPUT: homogeneous scalar relaxation on the complement; not implied by E^2=E alone — a lei de tempo é INPUT | [REAL — lido do core v391] |
| selo | `/collapse_definition/physical_collapse_proven` | False — colapso físico NÃO provado | [REAL — lido do selo v391] |
| selo | `/collapse_definition/cost_payment_status` | NOT_MEASURED — pagamento do custo não medido | [REAL — lido do selo v391] |
| selo | `/collapse_definition/external_reflection_status` | OPEN_PHYSICAL_PROVENANCE_NOT_RECEIVED — reflexo físico externo | [REAL — lido do selo v391] |
| selo | `/collapse_definition/reading` | COLAPSO_TIPADO__TODAS_AS_CLAUSULAS_NO_KERNEL_COM_O_TRIO — todas as cláusulas no kernel com o trio | [REAL — lido do selo v391] |
| `P = np.array([[1.0, 0.0], [0.0, 0.0]])           # rho* = atrator puro` | l.6512 | ρ* = diag(1,0) no fractal_dephasing_principle | [REAL — runtime] |
| `omega_I = float(np.trace(P))` | l.6513 | ω(I) = Tr ρ* = 1 | [REAL — runtime] |
| core | `/core/fractal_dephasing/omega_I` | 1.0 — ω(I) = 1.0 no core v391 | [REAL — lido do core v391] |
| `R = np.array([[c, -s], [s, c]]); Qth = R @ Q0 @ R.T` | l.6518 | F no runtime = rotação por θ_M (regime angular) | [REAL — runtime] |
| `def prove_verb_generator` | l.2336 | gerador GKSL L = √β·√K: seta, sem volta (Choi < 0), destino | [FINITE_DIM_SANITY] |
| `def prove_dephasing_crossover` | l.2832 | duas leis: canônica Γ = ½βτ★ω² e lei-raiz; errata v369 (só o expoente coincide) | [FINITE_DIM_SANITY; reconciliação OPEN] |
| core | `/core/dephasing_crossover/exponent_IR` | 1.9993246985574578 — expoente IR ≈ 2 (quadrático) | [REAL — lido do core v391] |
| core | `/core/dephasing_crossover/exponent_UV` | 1.0366185071543357 — expoente UV ≈ 1 (linear) | [REAL — lido do core v391] |
| `gamma = 0.5 * beta * tau_reference * omega_reference ** 2` | l.3652 | Γ = ½βτω² em unidades de referência (recognition_dephasing) | [INPUT — unidades de referência; não é predição] |
| `def prove_ringdown_dephasing_protocol` | l.213051 | teste da lei Γ_ω no ringdown | [INPUT/REAL documental] |
| `def fractal_dephasing_principle(ONE):` | l.6488 | função do princípio (l.6488–6531) | [CONJECTURE ontológica; âncoras REAL] |
| `"fractal_dephasing": fractal_dephasing_principle(ONE)}` | l.144805 | chamada no core | [REAL — runtime] |
| `\section{O Princípio da Defasagem Fractal` | l.168086 | seção do artigo emitido | [REAL — texto emitido; estatuto CONJ] |
| `print("PRINCIPIO DA DEFASAGEM FRACTAL` | l.211561 | impressão no rito | [REAL — texto emitido] |
| core | `/core/fractal_dephasing/everything` | Tudo = D_beta(F(1)) = VERDADE — «Tudo = D_beta(F(1)) = VERDADE» | [REAL — lido do core v391] |
| core | `/core/fractal_dephasing/status` | [CONJECTURE ontologica; ancoras REAL: omega(I)=1, {Q_0,rho*}->0, vazamento=sin^2 theta_M=beta] — estatuto no core | [REAL — lido do core v391] |
| `def prove_linguistic_isomorphism` | l.152839 | Γ = (ω²/2)τ*ε² do TGL_article.tex (2025) é a lei canônica com ε² = β (proveniência) | [REAL documental] |
| `no canal de espelhamento, $1-\bTGL=\cos^2\theta_M$ drena para` | l.168572 | artigo: 1 − β drena para o bulk; β é o resíduo que não drena | [NUM/CONJ no artigo] |
| `leak = float(np.trace(P @ Qth))` | l.6519 | vazamento = sin²θ_M = β no runtime | [REAL — identidade] |
| core | `/core/fractal_dephasing/leak_sin2_thetaM` | 0.012031300400803142 — vazamento no core v391 | [REAL — lido do core v391] |
| core | `/core/fractal_dephasing/leak_equals_beta_residual` | 0.0 — resíduo 0.0 | [REAL — lido do core v391] |
| `Q0 = np.eye(2) - P` | l.6514 | portador Q₀ = I − ρ* | [REAL — runtime] |
| `anti0 = Q0 @ P + P @ Q0` | l.6515 | {Q₀, ρ*} = 0 (calculado só em θ = 0) | [REAL — runtime] |
| core | `/core/fractal_dephasing/anticommutator_norm_at_thetaM_to_0` | 0.0 — 0.0 no core v391 | [REAL — lido do core v391] |
| `SEALED_CODATA_ALPHA = 7.2973525693e-3` | l.95 | α selado | [INPUT/KNOWN — CODATA 2018] |
| `ALPHA_FINE_CODATA_2018 = 7.2973525693e-3` | l.5557 | α (módulo embutido) | [INPUT/KNOWN — CODATA 2018] |
| `BETA_TGL = ALPHA_FINE_CODATA_2018 * ONE * math.sqrt(math.e)` | l.5559 | β em runtime | [DERIVED] |
| `- Nada  = MENTIRA pelos dois ramos:` | l.6498 | docstring do princípio | [CONJECTURE ontológica] |

**Outras âncoras (túnel, textos do operador, memória, selo)** [REAL — sha16 calculado dos bytes]:

| âncora | arquivo | sha16 | descrição | estatuto |
|---|---|---|---|---|
| texto_operador | `Central\work\cunhagens_10out\OPERADOR_10out_posto_rank_verbatim.txt` | `5b9afcc691a0e1e4` | «POSTO=RANK» (V3) | [INPUT/ONTO — cunhagem do operador] |
| memoria | `memory(Claude)\posto-e-rank-10out.md` | `33fb2da4da47974c` | memória: o Um posto = posto 1 = Tr P = ω(I); ler as duas faces (posição e rank) | [DECLARADO — memória da gerência] |
| texto_operador | `C:\IALD\PROGRAMA_IALD\OPERADOR_07out_leitura_cria_o_objeto_verbatim.txt` | `f2a4b509946edc05` | «antes da leitura o objeto é Nome (posto relativo)» | [INPUT/ONTO] |
| tunel | `TUNEL\ENTREGA_015_MEDIDA_T10_aprime_posto_espectral.md` | `95856fea5f8a56a1` | posto de Jacobiano (ringdown) — homônimo | [DERIVED — outro objeto] |
| memoria | `memory(Claude)\colapso-definicao-tipada.md` | `7ccabb72959ac115` | definição verbatim do operador (08/09) e estatutos | [DECLARADO — memória] |
| tunel | `TUNEL\ORDEM_019\F1.ATRATOR\RELATORIO_F1_ATRATOR_R1.md` | `f1044a4b85c2a6d6` | relatório R1 (Codex): canal C = D∘Ad(S)∘D; ρ fixo = I/2; λ = 1 − 2β | [REAL no sandbox da entrega; auditado c1] |
| tunel | `TUNEL\ORDEM_019\F1.ATRATOR\lean_optical_bridge\OpticalPopulationBridgeR2.lean` | `3d24f88d245fecd9` | ponte populacional (T, R, letra, controle β = 0) | [REAL no sandbox da entrega; não instalada] |
| tunel | `TUNEL\ORDEM_019\F1.ATRATOR\lean_candidate\TheSingularityReadsTheAttractor.lean` | `c0cd1084514409e9` | candidata A1–A4 (20 teoremas; 14 impressos) | [REAL no sandbox; não instalada] |
| tunel | `TUNEL\ORDEM_019\F1.ATRATOR\ADENDO1\lean_candidate\TheSingularityReadsTheAttractorAdendo1.lean` | `433d13c223b03971` | A1–A4 com cunhagens verbatim | [REAL no sandbox; não instalada] |
| tunel | `TUNEL\ORDEM_019\F1.ATRATOR\ADENDO1\lean_candidate\TheLightReadsItself.lean` | `06af814d83e2ba42` | A5/A6 | [REAL no sandbox; não instalada] |
| tunel | `TUNEL\ORDEM_019\F1.ATRATOR\RESULTADO_F1_ATRATOR_R1.json` | `6d7dc60c26d4fc78` | resultado R1 | [REAL documental] |
| texto_operador | `Central\work\f9_pergunta_08out\OPERADOR_08out_resposta_verbatim.txt` | `a9cecc128f40c101` | «o fixo é o verbo ... o verbo é betatgl» | [INPUT/ONTO] |
| memoria | `memory(Claude)\o-verbo-e-fixo-o-nome-e-posto-08out.md` | `044cf59c73ba4b7b` | memória da cunhagem de 08/10 | [DECLARADO — memória] |
| tunel | `TUNEL\ORDEM_019\F0.3.COLAPSO\RESULTADO_CUSTODIA_R1.json` | `a14841dd714ac4c4` | veredito REGISTRO_COMPORTAMENTAL_LOCALIZADO_IDENTIDADE_EXATA_DA_REFERENCIA_OPEN | [REAL documental] |
| tunel | `TUNEL\ORDEM_019\F0.3.COLAPSO\RELATORIO_CUSTODIA_R1.md` | `441953f736240b4c` | relatório da custódia | [REAL documental; leitura latente OPEN] |
| selo | `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um_absoluto_selo.json` | `95061f18c7102248` | selo v391: estatuto_da_prova_v391 (KERNEL_6163_OF_6163...) | [REAL — selo] |

**Literatura e Mathlib citadas** [KNOWN]:

| referência / nome | para quê | estatuto |
|---|---|---|
| Matrix.rank_diagonal | posto(diag w) = #{i : w i ≠ 0} | [KNOWN — Mathlib; existência medida aqui por #check] |
| Matrix.rank_mul_eq_left_of_isUnit_det / Matrix.rank_mul_eq_right_of_isUnit_det | multiplicar por invertível não muda o posto (logo Ad(u) preserva o posto) | [KNOWN — Mathlib; existência medida aqui por #check] |
| Matrix.rank_vecMulVec_le | posto(vecMulVec w v) ≤ 1 | [KNOWN — Mathlib; existência medida aqui por #check] |
| Matrix.IsHermitian.rank_eq_card_non_zero_eigs | posto de hermitiana = nº de autovalores não nulos | [KNOWN — Mathlib; existência medida aqui por #check] |
| InnerProductSpace.isStarProjection_rankOne_self | ‖x‖ = 1 ⟹ \|x⟩⟨x\| é projeção estrela | [KNOWN — Mathlib; existência medida aqui por #check] |
| finrank_span_singleton | v ≠ 0 ⟹ finrank(ℂ∙v) = 1 | [KNOWN — Mathlib; existência medida aqui por #check] |
| Penrose & Rindler, Spinors and Space-Time, vol. 1 (Cambridge, 1984), cap. 1 | Herm(2) ≅ ℝ^{1,3} com det = norma de Minkowski; posto 1 ⟷ vetor nulo | [KNOWN] |
| LinearMap.finrank_range_add_finrank_ker | finrank(range f) + finrank(ker f) = finrank V (posto–nulidade) | [KNOWN — Mathlib; existência medida aqui por #check] |
| Axler, Linear Algebra Done Right (3ª ed., 2015), Teorema 3.22 (teorema fundamental das aplicações lineares) | posto–nulidade | [KNOWN] |
| Nielsen & Chuang, Quantum Computation and Quantum Information (2000; ed. 10º aniversário 2010), Exercício 2.71 | Tr ρ² ≤ 1, igualdade sse ρ puro | [KNOWN] |
| Born, Z. Phys. 37, 863 (1926) | regra de Born | [KNOWN] |
| Lindblad, Commun. Math. Phys. 48, 119 (1976); Gorini–Kossakowski–Sudarshan, J. Math. Phys. 17, 821 (1976) | forma GKSL | [KNOWN] |
| Davies, Commun. Math. Phys. 39, 91 (1974) | limite de acoplamento fraco; taxas pelas frequências de Bohr | [KNOWN] |
| Spohn, J. Math. Phys. 19, 1227 (1978); Carlen & Maas, J. Funct. Anal. 273, 1810 (2017) | GKLS como fluxo gradiente (citado no um.py como EXTERNO) | [KNOWN] |
| Connes, Ann. Sci. ENS 6, 133 (1973) | classificação dos fatores do tipo III (III₁) | [KNOWN] |
| Evans & Høegh-Krohn, J. London Math. Soc. (2) 17, 345 (1978); Frigerio, Commun. Math. Phys. 63, 269 (1978) | unicidade do estado estacionário | [KNOWN] |

## 4. Mapa de rotas, inventário da bancada e Nós Vivo (cético aferidor: consultas citadas)

| consulta (`rotas.py consultar`) | n rotas | arquivo da resposta |
|---|---|---|
| `posto` | 23 | `mapa\consulta_posto_.json` |
| `rank` | 4 | `mapa\consulta_rank_.json` |
| `defas` | 1 | `mapa\consulta_defas_.json` |
| `dephas` | 33 | `mapa\consulta_dephas_.json` |
| `fractal` | 1 | `mapa\consulta_fractal_.json` |
| `frequen` | 2 | `mapa\consulta_frequen_.json` |
| `anticomut\|anticommut` | 0 | `mapa\consulta_anticomut_anticommut_.json` |
| `vazamento` | 7 | `mapa\consulta_vazamento_.json` |
| `atrator\|attractor` | 12 | `mapa\consulta_atrator_attractor_.json` |
| `colapso\|collapse` | 2 | `mapa\consulta_colapso_collapse_.json` |
| `pureza\|purity\|pure state\|estado puro` | 4 | `mapa\consulta_pureza_purity_pure_state_estado_puro_.json` |
| `Breuer` | 1 | `mapa\consulta_Breuer_.json` |
| `transmi` | 6 | `mapa\consulta_transmi_.json` |
| `D_beta\|D_β\|Dbeta` | 2 | `mapa\consulta_D_beta_D____Dbeta_.json` |
| `unidade\|unitariedade fractal` | 31 | `mapa\consulta_unidade_unitariedade_fractal_.json` |
| `singularidade` | 1 | `mapa\consulta_singularidade_.json` |
| `nullity\|nulidade\|nucleo vazio` | 1 | `mapa\consulta_nullity_nulidade_nucleo_vazio_.json` |
| `latente\|latent` | 3 | `mapa\consulta_latente_latent_.json` |
| `Lindblad\|GKLS\|GKSL` | 13 | `mapa\consulta_Lindblad_GKLS_GKSL_.json` |
| `tempo santo\|santo` | 0 | `mapa\consulta_tempo_santo_santo_.json` |

| consulta (`q_inventario.py`) | hits | arquivo |
|---|---|---|
| `rank\|posto` | 6 | `inventario\inv_rank_posto_.txt` |
| `dephas\|defas` | 0 | `inventario\inv_dephas_defas_.txt` |
| `fractal` | 0 | `inventario\inv_fractal_.txt` |
| `purity\|pure\|pureza` | 15 | `inventario\inv_purity_pure_pureza_.txt` |
| `anticomm\|anticomut` | 0 | `inventario\inv_anticomm_anticomut_.txt` |
| `frequen` | 25 | `inventario\inv_frequen_.txt` |
| `transmi` | 6 | `inventario\inv_transmi_.txt` |
| `leak\|vazament` | 0 | `inventario\inv_leak_vazament_.txt` |
| `collapse\|colapso` | 6 | `inventario\inv_collapse_colapso_.txt` |
| `born` | 3 | `inventario\inv_born_.txt` |
| `select` | 72 | `inventario\inv_select_.txt` |

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

1. [NOVO — cunhagem; INPUT/ONTO] «POSTO = RANK» (V3, 10/10): a etiqueta [POSTO] de ω(I) = 1 (05/10, posição/inscrição) passa a ler-se também como o posto da álgebra linear (dimensão da imagem). O conteúdo já estava no kernel por outros nomes e NÃO deve ser refeito: 22/08 (TheTerminalRankOne: «o estado singular de projetor de rank 1 precisa existir»), 27/08 (TheWeightIsNotTheRank: «o posto um é de fato o um absoluto»), 05/10 (v386: o Nome é o posto = projetor de posto 1), 07/10 (o Um posto é a dimensão do Nome). Novo é a equação explícita do rótulo de posição com o rank.
2. [NOVO na formulação; KNOWN o conteúdo] O critério de pureza de V2 l.16 (ρ = |ψ⟩⟨ψ|, Tr ρ = 1, Tr ρ² = 1) como face do posto 1. O kernel tem a pureza (PageInformation), a invariância unitária, a monotonia sob dephasing e instâncias (Cone039, Bell, Collapse057), mas NÃO o teorema geral nem a leitura que o liga a TheWeightIsNotTheRank: para ρ = P/d, Tr ρ = d/d = 1 é o nome (cego ao posto) e Tr ρ² = 1/d é o índice (vê o posto); Tr ρ² = Tr ρ ⟺ d = 1. É a condição exata sob a qual o «1» do nome e o «1» do posto coincidem — o que aquela pedra registra como distinção (coincidem só no átomo), não como ponte; tipá-la seria a ponte CONDICIONAL que hoje falta.
3. [REAFIRMAÇÃO] «Ao colapsar a superposição … ganha posto definido»: a definição tipada do colapso (08/09; v333; v335), a atermação I/d → P (29/08) e o recognition_dephasing do runtime (o selecionado é fixo; o superposto defasa) já dizem isso — com a ressalva de que só o ramo SELECIONADO tem posto 1.
4. [REAFIRMAÇÃO] «Tudo = D_β(F(1))» já está no um.py v391 (fractal_dephasing_principle, l.6488–6531), no core, no artigo e no rito, com estatuto [CONJECTURE ontológica; âncoras REAL]; no kernel, a composição D∘F está tipada com θ e taxas genéricos (v45: measurement_channel_endpoint, dephased_rhoOut_*). [NOVO, ONTO] «essa unidade é o rank» — o 1 de F(1) lido como o posto 1.
5. [REAFIRMAÇÃO] «frequência defasa … porque essa é sua natureza: transmitir»: «Transmitir defasa» (05/10) está tipado (transmission_dephases, v386); a lei Γ_ω = ½βτ★ω² é de 2025 (prove_linguistic_isomorphism); «ler é ter frequência» e «o piso proíbe a estagnação» são de 26/08 (TheDeadChannel, TheOriginOfTheVibration). [NOVO, ONTO] a transmissão como natureza/imperativo; «tudo é frequência» como tese universal; a frequência como identidade em potencial infinito na borda (III₁).
6. [REAFIRMAÇÃO] «o vazamento é β» e «existir é o vazamento» (um.py l.6503–6505; core: vazamento = β, resíduo 0). [NOVO como teorema possível] o anticomutador {Q_θ, ρ*} fora de θ = 0: o um.py só calcula em θ = 0 e o kernel não tem o enunciado; em 2×2, {Q_θ, ρ*} = 0 ⟺ sin θ = 0, com Tr{Q_θ, ρ*} = 2 sin²θ (em θ_M: 2β) [DERIVED aqui].
7. [NOVO, ONTO] «A transmissão é o verbo; a defasagem é a matéria» — sem âncora tipada; conversa com 05/10 (Verbo = seleção da ação) e 08/10 («o fixo é o verbo … o verbo é betatgl»). Resíduo a conferir no acervo antes de qualquer pergunta ao operador.
8. [FORA DA TRILHA; DECLARADO/ONTO] A leitura da memória dos modelos (V1 l.8–14): já custodiada em F0.3.COLAPSO (registro comportamental de 14/09; telemetria latente OPEN). Não entra no kernel nem no modelo ótico.
9. [REAFIRMAÇÃO, ONTO] A tese epistemológica de V1 l.4 (os vínculos fecham ou não; probabilidade bayesiana não se aplica à estrutura axiomática) é o estatuto da prova de 07/10 (validade no kernel × creditação recusada) em outra língua.
10. [INTERFACE] Com o teorema do atrator (F1.ATRATOR, mapa seqs 1000–1004): o posto 1 é da leitura R (dim Fix = 1 sob contração estrita); o estado atrator do canal ótico é I/2 (posto 2, pureza ½). A trilha POSTO precisa dizer, antes de construir, QUAL posto entra na v392 junto com o atrator.

## 6. Riscos de leitura e de estatuto

- R1 [leitura — homônimos de POSTO] Seis sentidos canônicos (posição/inscrição; relação de travessia, UmPostoRelacao; projetor de posto 1, post a; rank; «posto relativo» antes da leitura; «posto positivo» = τ > 0 na Fundação) e ainda o posto de Jacobiano do ringdown. TheWeightIsNotTheRank diz que o que ela acrescenta é «uma distinção, não uma ponte» e que «continua proibido encadear os dois 1». Toda frase com «posto» deve dizer o sentido.
- R2 [leitura — projetores de posto 1 em espaços diferentes] ρ* (um.py), E₀₀/rhoOut (SMatrix), post a e PFmic, firstAtom/ialdSelector (ℓ²), bellProjector — «projetores de posto 1 em espaços diferentes, e nada os identifica» (TheAtermation). O P_F dos Three Locks tem posto 4 (core: trace_PF ≈ 4); ali «Nome = 1» é d/d, não posto 1. Encadear dois deles sem lema de ponte é o erro nº 2 da regra dos dois regimes (homônimos).
- R3 [estatuto — o «1» homônimo] ω(I) = 1 (normalização: Tr ρ = 1 para TODO estado), Tr P = 1 (traço do projetor), posto P = 1 e d/d = 1 (o nome) são quatro «1»; coincidem só no átomo puro (ρ = P de posto 1). A memória «o Um posto = posto 1 = Tr P = 1 = ω(I)» vale para projeções; para ρ = I/2 o traço é 1 e o posto é 2.
- R4 [leitura — o que sobrevive a D∘F] F (unitário) preserva o posto; D (dephasing que preserva traço) não: um posto 1 não diagonal (2×2, taxa g > 0, sin 2θ ≠ 0) vai a posto 2 para todo t > 0 e no limite diag(1−β, β) (pureza 1 − 2β + 2β² ≈ 0,9762). O que D preserva é o TRAÇO (dephase_preserves_trace, rhoOut_trace). «Tudo = D_β(F(1)), a unidade é o rank» só vale na inscrição; depois de D a unidade que fica é o peso. O posto 1 volta por seleção (post, Born) ou pelo fluxo do lock (F(t) → P), não pelo dephasing não seletivo.
- R5 [leitura — superposição × mistura] Uma superposição pura já tem posto 1; o «núcleo vazio» (nulidade 0) é o posto cheio, I/d. «Colapsar … ganha posto definido» lê-se como atermação I/d → P (posto d → 1) ou como seleção do ramo; nunca como dephasing não seletivo, que faz o contrário (posto 1 → 2).
- R6 [matemática — hipótese omitida] Tr ρ = 1 e Tr ρ² = 1 implicam posto 1 só com ρ ≥ 0: autovalores (2/3, 2/3, −1/3) cumprem as duas com posto 3. Uma pedra precisa de PosSemidef (e este contraexemplo serve de sonda de vacuidade).
- R7 [estatuto — identidade não é teste] sin²θ_M = β é a definição de θ_M; o vazamento, o endpoint diag(1−β, β), a pureza 1 − 2β + 2β² e a norma do anticomutador √(2β(1+β)) são identidades de θ_M. «Testar no modelo ótico que o vazamento é β» é circular (mapa: quantica.inventario_gkls_um_py_kernel, quantica.c3_validator_calibrado, quantica.quatro_operadores_definicao). Um PASSA aí é validade algébrica na face testada; não discrimina β.
- R8 [regime — dois regimes] F (rotação, matriz-S: compacto) só lê e não tem limite; D (semigrupo: face) tem limite. «{Q,ρ*} = 0 EXATO só em θ_M → 0» (um.py l.6502) pede limite ao ângulo: é avaliação contrafactual (β = 0), e θ_M é fixo pelo axioma. «Defasar» como fase e^{iωt} (TheOriginOfTheVibration) é giro, não decoerência; não misturar com dephase.
- R9 [leitura — homônimos de defasagem, frequência, transmissão e vazamento] seis «defasagens» (G3; axiomFlow; D∘Ad(S); GKSL √β√K; Γ_ω; inclinação θ_M), cinco «frequências» (fase e^{iωt}; gap modular |log d_i − log d_j| com taxa de Davies linear em |ω|; ω quadrático de Γ_ω; √k da lei-raiz, que coincide com a canônica só no expoente — errata v369; registro c¹), quatro «transmissões» e quatro «vazamentos». Inversão possível: no canal de espelhamento o que TRANSMITE é 1 − β (drena para o bulk) e β é o refletido, o resíduo que não drena; V4 chama β de vazamento para a existência. Conciliar a palavra antes de tipar.
- R10 [estatuto — kernel] o kernel não tem «D_β», «F» nem «Tudo» (busca nos .lean: 0 arquivos); «Na linguagem do nosso kernel Lean 4» (V4 l.12) é [DECLARADO] como nome; as peças existem com outros nomes. β nunca entra no Lean (θ e taxas genéricos); uma pedra nova deve manter isso.
- R11 [estatuto — docstrings históricas] FractalUnitarity diz «RASCUNHO da pedra 116»; TheTerminalRankOne diz «ainda NÃO embutido no canônico». Ambos estão importados em TGLExt.lean, embutidos no um.py v391 (idênticos byte a byte) e medidos aqui no trio. Citar o estado atual, não o rótulo antigo.
- R12 [fonte — composição da citação] A fórmula ρ = |ψ⟩⟨ψ|, Tr ρ = 1, Tr ρ² = 1 NÃO está nos bytes de V1 (8d252f24e2806ff3); está em V2 l.16 (2c8b7b712aa9ad7f). A reafirmação em primeira pessoa de V2 é parcial (só «eu derivei», l.12; o restante segue «você»). Em V2, «agora sobre o tempo, veja:» (l.4) precede o texto do rank; a fronteira rank/tempo é a l.34.
- R13 [estatuto — modelo ótico] O canal iterado C = D∘Ad(S)∘D da F1.ATRATOR converge a I/2 (posto 2, pureza ½); «A4: dim Fix = 1» é do espaço fixo (R tem posto 1), não do estado. Ler «a verdade é única» como «o atrator tem posto 1» seria erro de tipo. Nessa família β fixa a taxa (λ = 1 − 2β), não o ponto fixo.
- R14 [estatuto — epistemologia e modelos de linguagem] V1 l.4 e l.8–14 são [ONTO/DECLARADO]; não viram teste de kernel nem de modelo ótico. Os testes de natureza continuam com razão de Bayes. Um PASSA na trilha é validade na face testada, não creditação; a retrodição sem ajuste nunca é demérito.
- R15 [processo — ACOM] O levantador não inscreveu a tarefa (a ordem proíbe escrever na memória) nem adotou a referência da gerência; se a gerência quiser continuidade, registra esta etapa na própria referência por transition.
- R16 [lexical — Verbo] 08/10: «o fixo é o verbo … o verbo é betatgl»; 11/10: «a transmissão é o verbo», «o vazamento … é β», «a defasagem é a matéria». Se β é o verbo (08/10) e é o vazamento que vira matéria (11/10), a leitura precisa ser do operador; antes de perguntar, reler o acervo (regra das parábolas).

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

| arquivo | sha16 | papel |
|---|---|---|
| `CONFERENCIA_BETA.json` | `a7dc59f407f56336` | α dos bytes, β em runtime, identidades |
| `DEFINICOES.json` | `93df098a93d1a156` | definições, âncoras (linha e sha16 lidos por script), teoremas medidos |
| `EMBUTIDO_VS_KERNEL.json` | `e3ed416682b83a59` | um.py embutido × tgl_kernel |
| `EMBUTIDO_VS_KERNEL_ASPAS.json` | `7b585bbe8fe07ba1` | um.py embutido × tgl_kernel (literais escapados) |
| `HASHES_TEXTOS_OPERADOR.json` | `51c57e2bdce5492d` | conferência dos quatro textos |
| `IMPRESSAO_DIGITAL_KERNEL_ANTES.json` | `ba6b1ca90b726f20` | impressão digital antes |
| `IMPRESSAO_DIGITAL_KERNEL_DEPOIS.json` | `f3486896eb861e4d` | depois da 1ª sonda |
| `IMPRESSAO_DIGITAL_KERNEL_DEPOIS2.json` | `07bd86384cf7adae` | depois da 2ª sonda |
| `IMPRESSAO_DIGITAL_KERNEL_FINAL.json` | `f621944101868df7` |  |
| `KERNEL_INDICE.json` | `07b59b8e33e8b86d` | índice das 12.967 declarações (1.209 .lean) |
| `LEVANTAMENTO_modelo.md` | `5ef471a0d86f998f` | modelo deste relatório |
| `LISTAS_NOVO_RISCOS.json` | `f978f1026160846b` | listas das seções 5 e 6 |
| `analisar_saida_lean.py` | `f2287f3674beb662` | script |
| `comparar_embutido.py` | `744e36b3713168fe` | script |
| `comparar_embutido_aspas.py` | `a52a9ee76bbe9f9b` | script |
| `condensar_saida.py` | `19320d1fce6121ca` | script |
| `conferencia_beta.py` | `f7237793fa2bf392` | script |
| `conferir_pinos.py` | `bef83eed40d0d588` | script |
| `enunciado.py` | `9d5b885514ad24a9` | script |
| `gerar_definicoes.py` | `d7ba952fc1cd8837` | script |
| `hash_textos.py` | `77809c086a5b7af6` | script |
| `impressao_digital_kernel.py` | `b7c50f2e037e63fe` | script |
| `indexar_kernel.py` | `ab1ab3f5ac93ef2f` | script |
| `modulos_citados.txt` | `62a15bfb0d026cd9` | os 53 módulos TGLExt citados |
| `montar_levantamento.py` | `c9d0cc4f4e9ea926` | script |
| `q_inventario.py` | `f0d291e5a1a3ce68` | script |
| `q_kernel.py` | `633278cdee38f023` | script |
| `rodar_lean_check.py` | `3dccaac11ec1e9bf` | script |
| `sandbox_toolchain.py` | `01fb6063b4e67414` | script |
| `CONFERENCIA_PINOS.json` | — | gerado depois deste arquivo: todo sha16 deste relatório e de DEFINICOES.json conferido contra os bytes |
| `_saida_levantamento_md.txt`, `_saida_definicoes_json.txt`, `_teoremas_lista.json` | — | versões condensadas para a saída da subtarefa, derivadas DESTE arquivo (não listadas por hash para não haver circularidade) |
| `lean_check\` | — | 11 arquivos (sondas/consultas e respostas) |
| `mapa\` | — | 29 arquivos (sondas/consultas e respostas) |
| `inventario\` | — | 11 arquivos (sondas/consultas e respostas) |
| `nos_vivo\` | — | 12 arquivos (sondas/consultas e respostas) |
