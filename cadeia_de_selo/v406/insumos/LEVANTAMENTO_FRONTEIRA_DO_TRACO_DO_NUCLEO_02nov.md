# LEVANTAMENTO DA FRONTEIRA DO TRAÇO DO NÚCLEO — 02/11/2026

> **Procedência:** relatório de um agente leitor (Sonnet, só-leitura) a serviço da gerência c1, devolvido em 02/11/2026 e gravado aqui pela gerência sem edição de conteúdo (o agente não tinha permissão de escrita). **Estatuto global: [DECLARADO pelo leitor]** até a gerência conferir cada item na fonte. O leitor NÃO compilou nada: todo «EXIT0» abaixo vem de recibos (`attempts\*\RECEIPT.json`, `AXIOMS.txt`) e de `.olean` que ele leu. A gerência confere os itens de maior peso em `CONFERENCIA_DO_LEVANTAMENTO_02nov.json` (ao lado).
> Rótulos do próprio leitor: [REAL] = leu no código ou no recibo; [DECLARADO] = docstring, comentário ou manifesto sem teorema ou recibo; [DERIVADO] = leitura dele a partir de [REAL].

=== RESUMO (5 achados) ===
1. A premissa "falta o habitante" vale só para o kernel tgl_kernel. A bancada tem um habitante dos 21 campos: B\takesaki_fock\CanonicalFockModularCoreInputR1.lean:77 `modularCoreInput` (trace := `cyclicTraceCandidate`). Recibo EXIT0 em B\orbital_rotation\attempts\20261016T210640_174717Z\RECEIPT.json. Parecer R52_R7_FULL_REVIEW_R1.json: `PASS_R7_CRITERION_WITH_EXPLICIT_SCOPE`, `filled_field_count` 21. R7 "satisfied" em 16/10 (R52_R7_ACCEPT_RECEIPT_R1.json). Nada disso está no kernel: 162 módulos da cadeia do traço (299-300 com a rede física) não existem em F1Fecho394. Os 44 módulos comuns são idênticos, e todo import externo existe.
2. No kernel (F1Fecho394) só há a 1ª metade: peso dual, GNS, Tomita, `scalarTomitaImaginaryPower`. Não encontrei teorema que ligue essa potência a `regularUnitary` ou à ação dual. Há 0 ocorrências de cutoff, sine, window, Radon, Nikodym, Pedersen e Haagerup; "perturb" só aparece como negação (CanonicalFockDualWeightR3.lean:13).
3. O molde completo de (i)-(iv) já está no kernel para a TORRE (T\V351*, T\V354*), mas (i) e (iv) usam unidades de matriz e sítios da torre, então não portam. Para Fock a bancada fez (i) por `actual_modular_implementation` (R17:89) e (iv) pelo nilpotente de Weyl (`core_matrix_corner`, MatrixCornerR2:192).
4. Armadilha do contrato: `trace_tracial` vale para todo x y, e `trace` é total em `RepresentedCore`. Estender o peso positivo por 0 ou ⊤ NÃO é cíclico (T\V354TraceReaderWall.lean:13; T\O16\TraceInfinityExtension_v3.lean:47). A saída usada é a completação ENNReal por `ShiftRelated`. Escopo declarado: não linear, sem afirmar tipo II∞.
5. Os arquivos Candidate, CutoffOrder, SineWindow e ChargeNormalization de B\mission_review_20261016 são tentativas não compiladas, canceladas ou fragmentos, superadas por uma cadeia EXIT0. Os quatro itens abertos são R3 (rito integral, isto é, integrar ao kernel), R4 e R5 (bloqueados: o operador não identificou MQC, Supercondutor ou Psi-NET) e R10 (revisão e ratificação da c1).

=== RELATÓRIO COMPLETO ===
Data: 2026-11-02. Rótulos: [REAL] = li no código ou recibo; [DECLARADO] = docstring, comentário ou manifesto sem teorema ou recibo; [DERIVADO] = leitura minha a partir de [REAL].
Aliases de caminho (absolutos):
- K = C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt\F1Fecho394\
- T = C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt\ (V350*, V351*, V354*, O16\)
- B = C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F1.FECHO_20261015\
- AV = C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\AVISO_GERENCIA.md
- M = C:\t\k405c\final\.lake\packages\mathlib\Mathlib\

Método e limites:
- Li os 15 arquivos de K citados e os genéricos.
- Fiz grep em K (184 arquivos), T (V350/V351/V354 e O16) e na bancada.
- Calculei o fecho de imports da bancada com um script somente-leitura.
- Varri 1299 recibos `attempts\*\RECEIPT.json`. Essa varredura pode ter falsos negativos.
- Não li os ~800 arquivos da bancada, só cabeçalhos e enunciados da cadeia.
- K, V351/V354 e a bancada não têm `sorry`, `admit`, `axiom` nem `native_decide` (grep). Na bancada isso vale para o fecho do traço (162 módulos) e o fecho completo.
- O sandbox C:\t\k405c\final tem TGLExt/F1Fecho394 idêntico ao kernel (diff -rq vazio), com 184/184 .olean de F1Fecho394 (amostra de 19/10) e V351/V354 de 26/09.

## 1. PERGUNTA 1 — passos (i)-(iv)

### 1.0 Três camadas
- **K (kernel Fock):** só a 1ª metade, na ordem: núcleo regular, ação dual, peso dual, GNS, Tomita fechado, S†S auto-adjunto, resolvente, `scalarTomitaImaginaryPower`.
- **T (kernel torre `SiteProfile P`, sobre `RegularHilbert (TowerHilbert P)`):** os quatro passos completos, todos com `(P : SiteProfile)`. Há blocos genéricos em H (`{H : Type}`) reaproveitáveis.
- **B (bancada):** porte para Fock de tudo isso. `takesaki_fock` tem 388 .lean (134 radicais; 33 também no kernel, 101 ausentes). `gns_coefficient_tomita` tem 232 .lean (102 radicais; 0 no kernel).

### 1.1 Passo (i): σ^φ̃_t = Ad λ(t)
**K, entradas ([REAL]):**
- λ(t): `regularUnitary` (K\CanonicalFockRegularCoreR2.lean:33; def em K\RegularCovariantCoreR3.lean:64 = `fibre (boostCLM B t) * shift t`).
  - Leis: `regular_mul` (R2:49), `regular_star` (:53), `regular_unitary` (:56), `regular_strongly_continuous` (:61).
  - `regular_covariance` (:68): λ_t fibre(A) λ_t* = fibre(flow t A).
  - `automorphism_is_concrete_boost` (:65, rfl).
  - `fockFlow` (:22): U t := gamma (B0 (-(2π t))).
- Ação dual:
  - `dualAction` (R2:36; RegularCovariantCoreR3:163), `dualAction_zero` (R2:80), `dualAction_add` (R2:83), `dual_fixes_embedding` (R2:87).
  - `dual_eigencharacter` (R2:91): θ_s λ_t = characterPhase s t • λ_t.
  - Pontos fixos = base: `dualFixed_eq_amplified_base` (K\RegularCoreFixedR3.lean:222), `fixed_core_is_base` (K\CanonicalFockFaithfulWeightR2.lean:23).
- Modular do VÁCUO na base M (não do peso dual):
  - `actualModularFlow_eq_gamma` (K\CanonicalFockBWR2.lean:34), `canonical_pair_tomita` (:40), `canonical_bw_kms` (K\CanonicalWedgeKMSR4.lean:32).
  - `actualModularFlow` (K\CanonicalFockModularFlowR2.lean:15), `actual_tomita_polar` (K\CanonicalFockPolarR1.lean:27).
- Tomita do peso dual:
  - `closedTomita` (K\CanonicalFockWeightClosedTomitaR2.lean:16): `domain_dense` :18, `graph_eq` :23, `graph_closed` :29, `involutive` :36, `extends_star` :40.
  - `actualClosedInput` (K\CanonicalFockWeightModularOperatorR3.lean:16), `scalarTomitaSquare` (:24), `scalarTomitaSquare_selfadjoint` (:44), `scalarTomitaResolvent` (:25) com `_nonneg` :66, `_le_one` :69, `_injective` :63, `_graph` :72.
  - `scalarTomitaImaginaryPower` (K\CanonicalFockWeightModularFlowR3.lean:13): `_damping` :16, `_unique` :21, `_zero` :27, `_add` :31, `_strongly_continuous` :36, `_inverse` :40.
  - Genéricos: `ClosedTomitaOperator.Input` (K\ClosedTomitaOperatorR1.lean:19), `ClosedTomitaFlow.scalarTomitaImaginaryPower` (K\ClosedTomitaFlowR1.lean:37).
- Transporte genérico em K: `imaginaryPower_intertwine` (K\ImaginaryPowerIntertwiningR2.lean:32), `cfc_intertwine` (K\CFCIntertwiningR3.lean:12), `hom_intertwine` (K\ContinuousHomIntertwiningR2.lean:19), `imaginaryPower_eq_phase` (K\ScalarL2ImaginaryR5.lean:86).

**K, a ligação potência imaginária ↔ λ(t) / ação dual: NÃO ENCONTRADA.** Onde procurei:
- `scalarTomitaImaginaryPower` ocorre só em CanonicalFockWeightModularFlowR3.lean e ClosedTomitaFlowR1.lean.
- Nenhum arquivo de K cita ao mesmo tempo potência imaginária e `regularUnitary|regularRightCoreElement|dualAction|dualAmbient`.
- Busca por "regularConjugation|implementation|implementer" não acha teorema.
- [DECLARADO] K\CanonicalFockWeightModularFlowR3.lean:5 ("The equality with regular conjugation and the trace law remain separate").
- [DECLARADO] K\ClosedTomitaFlowR1.lean:2-5, K\CanonicalFockRegularCoreR2.lean:12-13, K\CanonicalFockWeightClosedTomitaR2.lean:5-6, K\CanonicalFockDualWeightR3.lean:13-14.

**T (molde da torre):**
- `scalarTomitaImaginaryPower_eq_regular_implementation` (T\V351ModularImplementation.lean:16): Δ^{it}x = π(λ_t)(ρ(-t)x).
- `scalarTomitaImaginaryPower_core_conjugation` (T\V351ScalarImaginaryCoreAction.lean:47): Δ^{it}π(A)x = π(λ_t A λ_t*)Δ^{it}x.
- Base da prova da torre: `matrixUnit_regular_core_conjugation` (:16) e `matrixUnit_imaginaryPower_base_scaling` (:31). Usam `localBaseCore`, `localEigenvalue` e `represented_levelExpectation_strong_tendsto`. [DERIVADO] Não portável a Fock.

**B (Fock):**
- `coefficientUnitary : RegularHilbert F ≃ₗᵢ[ℂ] GNSHilbert` (B\takesaki_fock\CanonicalFockCoefficientGNSR1.lean:111).
- `regularConjugationGNS t := scalarGNSRepresentation (regularRightCoreElement t) * regularRightGNS (-t)` (CanonicalFockConjugationActionR3.lean:16).
- Em CanonicalFockModularIdentificationR17.lean: `target_graph_eq` :23, `unitary_graph` :32, `resolvent_intertwines` :58, `imaginary_intertwines` :73, **`actual_modular_implementation (t) (y) : scalarTomitaImaginaryPower t y = regularConjugationGNS t y`** (:89), `actual_regular_conjugation_group`.
- Recibo: B\takesaki_fock\attempts\20261016T095304_909045Z\RECEIPT.json (761,8 s; AXIOMS.txt só o trio).
- Cadeia de suporte:
  - `CanonicalFockModularGraphEqualityR1`, `ModularTransportTargetR1`.
  - `CanonicalFockPolarFlipR4`: J troca T por 1-T.
  - `CanonicalFockRightPolarBridgeR5`: J troca multiplicação regular esquerda/direita.
  - `CanonicalFockRightRootR10`, `CanonicalFockRightTomitaR3`.
- Diário: AV:1243 (R31) "[REAL - sandbox; actual_modular] ... O grupo modular é igual à conjugação regular por termo".

### 1.2 Passo (ii): h^{it} = λ(t); τ = φ̃(h⁻¹·) é traço
**K:** nada para h (0 arquivos com `regularPositiveGenerator|regularSpectralResolvent|regularInverseGeneratorCutoff|inverseSupremum|cutoffWeight|scalarInverseLimitWeight|cyclicTraceCandidate|ShiftRelated|boundedPolar`).

Entradas de K:
- `UnitaryFlow` (K\RegularCovariantCoreR3.lean:12).
- `regularAverage` (K\RegularCoreAverageR2.lean:33) e `regularAverage_tendsto_identity` (:65).
- `regularAverage_dualQuadraticIntegral` (K\RegularCoreFiniteWeightR3.lean:95): φ̃(Aₕ*Aₕ)(v) = ofReal(h⁻¹‖v‖²).
- `weight` (K\CanonicalFockDualWeightR3.lean:62), com `weight_add` :67, `weight_scale` :70, `weight_mono` :78, `weight_dual_invariant` :81, `weight_one` :85 (= ⊤), `weight_monotone_strong_limit` :100.
- `weight_faithful` (K\CanonicalFockFaithfulWeightR2.lean:42).
- `weight_internal_normal` (K\CanonicalFockFiniteWeightR4.lean:17), `weight_averageSquare` (:31), `exists_positive_finite_weight` (:38).
- `finiteStarCore` (K\CanonicalFockFiniteStarCoreR1.lean:14), `finiteStarCore_strongStar_approximation` (:25).

[DERIVADO] O peso não perturbado não é traço: `weight_dual_invariant` (:81) mais `weight_averageSquare` (FiniteWeightR4:31) violam a escala exp(-s). É o mesmo argumento de `scalarDualWeight_not_trace_provider` (T\V351RegularCoreTraceContract.lean:98).

**T (todas com `(P : SiteProfile)`):**
- Gerador h:
  - `regularSpectralResolvent` (T\V351RegularPositiveGraph.lean:78), `regularPositiveGenerator` (:122).
  - `regularPositiveGenerator_imaginaryPower` (T\V351RegularImaginaryPowers.lean:90): potências imaginárias de h = `regularUnitary P t`.
  - `sigmoidMultiplier_imaginaryPower` (:24, genérico em H).
  - `regularPositiveGenerator_commutant_graph` (T\V351RegularGeneratorAffiliation.lean:76).
- Corte inverso:
  - `regularInverseGeneratorCutoff` (T\V351InverseGeneratorCutoff.lean:13) = (ε⁻¹)•dualAmbient(log ε)(resolvente).
  - `regularInverseGeneratorCutoff_cfc` (T\V351InverseCutoffCFC.lean:62).
  - `regularDomainCut` (T\V351RegularDomainCut.lean:13).
  - Janela seno: `regularSineWindowCore` (T\V351SineResolventApprox.lean:26), `regularSineResolvent` (:95), `regularSineResolvent_cfc` (:101), `regularSpectralResolvent_right` (:231).
- Peso perturbado:
  - `scalarInverseCutoffWeight` (T\V351InverseLimitWeight.lean:15), `scalarInverseLimitWeight` (:87), `_add` :98, `_scale` :104, `_mono` :109, `_normal` :115.
  - `_faithful` (T\V351InverseLimitFaithful.lean:50), `_finite_minorants` (T\V351InverseLimitFiniteMinorants.lean:84).
- Tracialidade:
  - **`scalarInverseLimitWeight_tracial`** (T\V351QuadraticTrace.lean:243).
  - `scalarInverseLimitWeight_tracial_iff_core` (T\V351InverseLimitTracialExtension.lean:125).
  - `scalarTomitaResolvent_double_cut_balance` (T\V351ModularCutBalance.lean:512).
- Contrato: `RegularCoreTraceData` (T\V351RegularCoreTraceContract.lean:43), `scalarInverseLimitTraceData` (T\V351RegularCoreTraceConstruction.lean:15), `regularCoreDualScalingData` (T\V351DualScalingBridge.lean:26).

**B (genérico em `UnitaryFlow H`, depois Fock):**
- Gerador h:
  - `regularSpectralCoordinates` (B\gns_coefficient_tomita\GeneralRegularPositiveGraphR2.lean:16), `regularSpectralResolvent` (:22), `regularPositiveGenerator` (:66).
  - `regularPositiveGenerator_imaginaryPower` (GeneralRegularImaginaryPowersR1.lean:33).
  - `regularSpectralResolvent_mem` (GeneralRegularAffiliationR1.lean:15), `regularPositiveGenerator_commutant_graph` (:59).
- Pesos:
  - `regularInverseGeneratorCutoff` (GeneralRegularInverseCutoffR1.lean:15).
  - `cutoffWeight` (B\takesaki_fock\GeneralInverseCutoffWeightR3.lean:18) = dualQuadraticIntegral(√B_ε* X √B_ε).
  - `inverseSupremum` (GeneralInverseSupremumR3.lean:14) = ⨆ sobre todo ε>0.
  - `CanonicalFockInverseSupremum.value` (CanonicalFockInverseSupremumR2.lean:20), com `value_faithful` :55, `value_normal` :67, `value_subadditive` :75.
  - `value_add` (B\gns_coefficient_tomita\CanonicalFockActualInverseAdditivityR2.lean:212), `value_finite_minorants` (B\takesaki_fock\CanonicalFockActualInverseFinitenessR2.lean:194), `value_one` (CanonicalFockInverseNormalR1.lean:29).
- Tracialidade:
  - `GenericPolarModularBalanceR1.balance` (B\gns_coefficient_tomita\:13).
  - `CanonicalFockActualModularBalanceR6.actual_balance` (:213).
  - `inverseSupremum_star_core` (CanonicalFockActualStarCoreTracialR1.lean:114).
  - `inverseSupremum_tracial` (CanonicalFockActualTracialExtensionR1.lean:56).
- Pacote: `PositiveTraceData` (B\takesaki_fock\CanonicalFockActualPositiveTracePackageR2.lean:90) e `actualPositiveTrace` (:110), com `value_tracial` :65 e `exists_positive_finite` :130.

### 1.3 Passo (iii): θ_s(h) = e^{-s}h ⇒ τ∘θ_s = e^{-s}τ
- **K:** só as leis da ação dual de 1.1 e `weight_dual_invariant`. Nada de escala.
- **T:**
  - `regularPositiveGenerator_dual_scaling` (T\V351RegularGeneratorDualScaling.lean:124), `regularInverseGeneratorCutoff_dual` (T\V351InverseGeneratorCutoff.lean:81).
  - `regularInverseCutoffSqrt_dual` (T\V351InverseLimitScaling.lean:35), `scalarInverseCutoffWeight_dual` (:46), `scalarInverseLimitWeight_scaled_sequence` (:69).
  - `scalarInverseLimitWeight_dual` (:91).
- **B:**
  - `regularPositiveGenerator_dual_scaling` (GeneralRegularDualScalingR2.lean:60; é covariância do grafo; o docstring :1-3 diz que não é teorema de escala do traço).
  - `regularInverseGeneratorCutoff_dual` (GeneralRegularInverseCutoffR1.lean:83), `cutoffWeight_dual` (GeneralInverseCutoffWeightR3.lean:90).
  - `inverseSupremum_dual` (GeneralInverseSupremumR3.lean:71), `value_dual` (CanonicalFockInverseSupremumR2.lean:28), `cyclicTraceCandidate_dual` (CanonicalFockCyclicTraceCompletionR3.lean:105).

### 1.4 Passo (iv): projeção finita partida em metades
- **K:** só `exists_positive_finite_weight` (FiniteWeightR4:38), do peso NÃO perturbado, que é inútil para PF. Insumos de Weyl: `wedge_nonabelian` (K\WedgeNonabelianR4.lean), `FieldWeyl.W` (K\FieldWeylR3.lean).
- **T:**
  - Genéricos em H: `positive_operator_has_threshold_projection` (T\V354SpectralThreshold.lean:16), `kernel_projection_mem_vonNeumann` (T\V354FiniteTraceSupport.lean:36), `boundedPolar` (T\V354BoundedPolar.lean:73), `boundedPolar_transports_shift_factors` (T\V354PolarIntertwining.lean:59).
  - Da torre: `scalarTrace_finite_subprojection_exists` (T\V354SpectralThreshold.lean:93), `regularCore_matrix_corner` (T\V354RegularMatrixCorner.lean:13; usa `siteMark`/`siteOperator`), `scalarTrace_finite_equal_split` (T\V354FiniteEqualSplit.lean:11), `scalarTrace_dual_calibration` (T\V354NormalizedSplit.lean:12), `scalarTrace_normalized_split_exists` (:27).
- **B:**
  - Canto: `matrix_corner_of_square_zero` (B\takesaki_fock\MatrixCornerFromNilpotentR3.lean:51).
  - Em CanonicalFockMatrixCornerR2.lean: `nilpotent_of_sign_flip` :33, `weyl_real_part_ne_zero` :136, `wedge_nilpotent_exists` :147, `core_nilpotent_exists` :179, `core_matrix_corner` :192. A fonte do canto é A=W(f)+W(f)*, U=W(g), U A U*=-A.
  - Em CanonicalFockFiniteProjectionR3.lean: `finite_positive_below` :56, `finite_subprojection_exists` :74, `finite_projection_exists` :110, `dual_calibration` :121, `normalized_projection_exists` :133.
  - Em CanonicalFockNormalizedSplitR5.lean: `finite_equal_split` :203, `finite_split_support` :213, **`normalized_split_exists`** :225: ∃ q r, projeções, q*r=0, value(q+r)=1, value q = value r.

### 1.5 Extensão total do traço (campos `trace_*` sobre todo o núcleo)
- **Muro:** o peso positivo estendido por 0 não é cíclico: `positiveTraceReader_not_cyclic` (T\V354TraceReaderWall.lean:13). Estender por ⊤ também não: `infinity_extension_not_cyclic` (T\O16\TraceInfinityExtension_v3.lean:47).
- **T:**
  - `ShiftRelated` (T\V354TraceShiftEquivalence.lean:11), `ShiftRelated.cyclic` (:62).
  - `cyclicTraceCandidate` (T\V354CyclicTraceCompletion.lean:15) com `_cyclic` :33, `_star` :50, `_dual` :73, `_zero` :131, `_positive_faithful` :143, `_positive_of_compatibility` :155.
  - `positiveShift_trace_compatible` (T\V354PositiveShiftCompatibility.lean:13), `cyclicTraceCandidate_positive` (:32), `scalarTrace_transport_of_support` (T\V354PositiveTraceTransport.lean:54).
- **B:**
  - `positiveAsCore` (B\takesaki_fock\CanonicalFockPositiveShiftTransportR2.lean:90), `positiveShift_value_compatible` (:105).
  - `cyclicTraceCandidate` (CanonicalFockCyclicTraceCompletionR3.lean:31), com `_cyclic` :48, `_star` :64, `_dual` :105, `_positive` :137, `_zero` :145.
- **K:** nada.

### 1.6 Busca por palavras-chave em K (184 arquivos)
| termo | resultado |
|---|---|
| cutoff, sine, window, Radon, Nikodym, Pedersen, Haagerup, traciality | 0 ocorrências |
| perturb | 1: K\CanonicalFockDualWeightR3.lean:13 ("No faithfulness, semifiniteness, tracial law, inverse-generator perturbation, full modular implementation or Fock-to-tower equivalence is asserted here"), negação |
| tracial | só o campo `trace_tracial` em CanonicalFockAssemblyR1.lean:123, CanonicalFockAntiAssemblyR4.lean:64, CanonicalWeylAssemblyR5.lean:50, CanonicalModularCoreAssemblyR1.lean:50 (e prints em NetworkProofAuditR3.lean:67,323); negações em CanonicalFockFiniteStarCoreR1.lean:5 e CanonicalFockDualWeightR3.lean:13 |
| scaling | campo `trace_dual_scaling` nos mesmos 4 arquivos; negações em CanonicalFockDualWeightR3.lean:9 ("not the exp(-s)-scaling trace") e CanonicalFockFiniteStarCoreR1.lean:5 |
| inverse | só inversos de unitários e de resolvente (ex.: `scalarTomitaResolvent_inverse`, `modularR_inverse`); nenhum "gerador inverso" |
| Takesaki / Connes | só comentários nos campos (CanonicalFockAssemblyR1.lean:111,127 etc.) |

Fora de K:
- Gerador inverso, corte e janela seno: só na torre (T\V351InverseGeneratorCutoff, V351InverseCutoffCFC, V351SineResolventApprox, V351InverseLimit*, V351PerturbedWeight*) e na bancada.
- Radon-Nikodym não tipado (só cociclo finito): T\Cocycle.lean:46,63; `dual_weight` (T\FiniteCrossedProduct.lean:559) é a "sombra finita" de Haagerup 1978, com matrizes e grupo finito.
- T\BreuerTrace.lean:104 `opWeight_star_mul_self_comm` é τ(a*a)=τ(aa*) em `ellTwo`, outro habitante.
- Os sete nomes pedidos (`RegularCovariantCore`, `RegularCoreAverage`, `RegularCoreFiniteWeight`, `RegularFiniteStarCore`, `RegularScalarGNSRepresentation`, `ClosedTomitaOperator`, `ClosedTomitaFlow`) só ocorrem em K. Em T e O16 o único acerto é T\ClosedTomitaOperator.lean (namespace `ChatgptAudit`, torre), um HOMÔNIMO de `F1Fecho.ClosedTomitaOperator`; cuidado ao importar.

### 1.7 Respostas diretas
- **Existe teorema que ligue `scalarTomitaImaginaryPower` (K) aos unitários regulares ou à ação dual?**
  - Em K: não encontrei (busca acima).
  - Em T: sim, só para a torre.
  - Em B: sim, para Fock (`actual_modular_implementation`).
- **Insumo legado de contrato:** T\O16\PhotonModularRealization.lean tem `ContinuousCoreData` (:71), `ThreeLocksCoreData` (:103) e `dualInvariant_PF_no_go` (:170). É a versão abstrata dos mesmos campos, com o no-go: PF não pode ser dual-invariante, senão Tr(PF) ∈ {0,∞}. O PF da bancada é calibrado por `dual_calibration`, não invariante.

## 2. PERGUNTA 2 — bancada

### 2.1 Inventário (B\takesaki_fock, B\gns_coefficient_tomita, B\mission_review_20261016)
- **takesaki_fock** (388 .lean, 134 radicais, 33 no kernel): famílias ausentes de K:
  - GNS por coeficientes: `CanonicalFockCoefficient*`.
  - Peso inverso: `CanonicalFockInverse*`, `GeneralInverse*`.
  - Completação cíclica: `CanonicalFockCyclicTraceCompletion*`, `PositiveShiftTransport*`.
  - Projeção, canto e split: `FiniteProjection*`, `MatrixCorner*`, `NormalizedSplit*`.
  - Identificação modular: `ModularIdentification*`, `ModularBridge*`, `ModularGraphEquality*`.
  - Ferramentas `Regular*`.
  - Montagem final: `CanonicalFockModularCoreInputR1`, `CanonicalTracedCoreAssemblyR1`.
  - Os arquivos .lean não têm "Candidate" no nome. Só os manifestos `CANONICAL_FOCK_*_CANDIDATE_R*.json`, com `status: DECLARADO_UNCOMPILED` no nascimento.
- **gns_coefficient_tomita** (232 .lean, 102 radicais, 0 no kernel): `GeneralRegular*`, `GenericPolar*`, `CanonicalFockActual*`, `CanonicalFockPolarRight*`, `R7SineWindow*`, Gaussian*, `GenericClosedEquationsCFC*` etc.
- **mission_review_20261016** (149 arquivos; 4 .lean): ver 2.2.
- Status de compilação dos módulos da cadeia: ver 2.3.

### 2.2 Arquivos pedidos
Legenda: Afirma / NÃO afirma / recibo / no kernel?

**CutoffOrder**
- B\gns_coefficient_tomita\CanonicalFockPolarRightCutoffOrderR10.lean (244 linhas):
  - Afirma [DECLARADO]: "The proved polar right identity commutes with the actual Fock left action". NÃO afirma: "No commutant equality or polar factor identification is assumed here".
  - Recibo [REAL]: attempts\20261016T105344_102192Z, exit_code 4294967295 (processo morto), 7383 s, BUILD.log só "import took 339s". Sem .olean.
  - No kernel: não.
- B\gns_coefficient_tomita\CanonicalFockPolarRightCutoffOrderR12.lean (255):
  - Afirma [DECLARADO]: "Cutoff and right-action consequences using the compiled first-resolvent module". NÃO afirma: "The full scaled trace/PF construction remains a later obligation".
  - Recibo: exit 4294967295 (647 s), sem .olean.
  - No kernel: não.
- B\mission_review_20261016\CanonicalFockPolarRightCutoffOrderR11Candidate.lean (296):
  - Afirma [DECLARADO]: "Experimental source-only candidate, DECLARADO, NOT COMPILED. Alternative to R10... Explicit ambient CFC carrier". Define `regularSineWindowCore` (:22), `regularSineResolvent_right` (:44), `regularSpectralResolvent_right` (:62). NÃO afirma compilação.
  - Recibo: exit 4294967295 (2378 s, morto). Sem .olean.
  - No kernel: não.
  - Recomendação de cancelar R10: B\mission_review_20261016\R7_CANCELLATION_AND_REPLACEMENT_RECOMMENDATION_R1.json.
- Sucessor que compilou: B\gns_coefficient_tomita\CanonicalFockPolarRightCutoffsR13.lean (EXIT0, 79 s).
  - Prova `regularSpectralResolvent_right` (:22), `regularInverseGeneratorCutoff_right` (:54), `scalarRightAction_sqrt` (:86), `regularInverseGeneratorCutoff_sqrt_right` (:102).
  - Contém `#eval IO.FS.withFile "R7_stages.log"`, uma instrumentação que escreve arquivo.

**SineWindow**
- B\gns_coefficient_tomita\R7SineWindowPrefixProbeR1.lean (25): "Diagnostic prefix only", EXIT0 (310 s).
- R7SineWindowClosureProbeR2/R3/R4 (97-116 linhas): "Bounded synchronous diagnostic: first resolvent only, with direct file markers". Exit 1 em todas.
- R7SineWindowClosureProbeR5 (103): mesmo docstring, EXIT0 (84,9 s). Prova `regularSineWindowCore` (:25), `regularSineResolvent_eq_window_cfc` (:74), `regularSineResolvent_right` (:89).
- B\mission_review_20261016\R7SineWindowEqualityTransportFragmentR1.lean (33): "DECLARADO / UNCOMPILED replacement fragment, not a standalone module", reescreve só o corpo de `regularSineResolvent_eq_window_cfc` (:10) congelando a instância CFC. Sem recibo nem .olean.
- No kernel: nenhum. Na torre o análogo compilado está em T\V351SineResolventApprox.lean:26-135.

**ModularBalance**
- B\gns_coefficient_tomita\CanonicalFockActualModularBalanceR1-R4: "UNCOMPILED CANDIDATE" (R1 118 linhas, R4 406). R5 (221 linhas): exit 1.
- R6 (CanonicalFockActualModularBalanceR6.lean): EXIT0 (165 s). Prova `actual_balance` (:213): `Commute T B ∧ Injective B ∧ (1-T)*A*(1-B) = T*(1-A)*B`.
  - NÃO afirma [DECLARADO]: "The double-cut limits, tracial law, total trace interface and PF remain open".
- GenericPolarModularBalanceR1.lean (88): "The analytic balance needed by the cut trace, with every modular premise explicit". EXIT0 (178,8 s); `PolarModularBalance.balance` (:13).
- B\mission_review_20261016\CanonicalFockActualModularBalanceCandidateR1.lean (118): "UNCOMPILED CANDIDATE ... does not import R12, assume a modular implementation, or establish a trace".
  - Enuncia o mesmo `actual_balance` (:62), consumindo `actual_modular_implementation`. Sem recibo nem .olean; superada por R6.
- No kernel: nenhum. A versão genérica da torre é T\V351ModularCutBalance.lean:512.

**ChargeNormalization**
- B\mission_review_20261016\R8ChargeNormalizationCandidateR1.lean (48):
  - "Review candidate only: NOT COMPILED. No new Maxwell hypothesis and no certificate inhabitant".
  - Define `angularStressFactor := ((2π)^3)⁻¹`, `normalizedTensorCandidate`, e deixa como Prop ABERTA `rawChargeLinkRemaining` e `rawNontrivialRemaining`.
  - É da frente Maxwell (R8) e recebe `A : RemainingModularCoreInput D` como parâmetro (:16-17). Ou seja, consome o contrato do traço, não o fornece.
  - Sem recibo nem .olean. O AV:1686 (R52) registra R8 como aceito depois, com "identidade de carga".
- No kernel: não.

**Candidate (conclusão)**
- Os 3 .lean com "Candidate" em mission_review (`CanonicalFockActualModularBalanceCandidateR1`, `CanonicalFockPolarRightCutoffOrderR11Candidate`, `R8ChargeNormalizationCandidateR1`) e o fragmento SineWindow NÃO entraram no kernel. Também não entraram: os 101 radicais de takesaki_fock, os 102 de gns_coefficient_tomita e os 4 de mission_review (comparei com a lista de 184 de K).
- Dois arquivos do kernel têm "Candidate" no nome: T\ClosedModulatorCandidate.lean (import em TGLExt.lean:255) e T\V350ConstantFibreCandidate.lean (:775). São da torre, antigos e transpostos mecanicamente da bancada em 05/09/2026. Não confundir.
- Caso especial: `CanonicalFockModularCoreInputR1` tem manifesto `CANONICAL_FOCK_MODULAR_CORE_INPUT_CANDIDATE_R1.json` com `statute: DECLARADO`, `compiled: false` (21:05 UTC). O recibo mostra EXIT0 às 21:06-21:07 UTC e o aceite às 21:12 UTC. O "Candidate" do nome é estado de nascimento, não estado atual.

### 2.3 Cadeia aceita (R7) vs kernel
- Raízes `CanonicalFockCyclicTraceCompletionR3` + `CanonicalFockNormalizedSplitR5` (+ `CanonicalFockModularCoreInputR1`, `CanonicalFockModularIdentificationR17`, `PositiveShiftTransportR2`, `ActualPositiveTracePackageR2`, `ActualStarCoreTracialR1`, `ActualTracialExtensionR1`, `ActualModularBalanceR6`).
- Fecho de imports locais da bancada [REAL, script somente-leitura]:

| fecho | módulos | não estão em F1Fecho394 |
|---|---|---|
| cadeia do traço (Cyclic R3 + Split R5) | 188 | **162** (80 de gns_coefficient_tomita, 81 de takesaki_fock, 1 de gamma_unbounded) |
| completo (`modularCoreInput` + rede física `PhysicalFockNetRealizationR2`) | 344 | **300** (incluem Maxwell/orbital_rotation; 3 só como .olean em dependency_cache: GeometricIdentification, FourierConjugation, WedgeReflectionTranslations) |

- Compatibilidade com o kernel:
  - Os 44 módulos do fecho completo que já existem em K são IDÊNTICOS aos do kernel, após normalizar o prefixo `import TGLExt.F1Fecho394.`.
  - Todos os 130 imports `TGLExt.*` externos existem no kernel e os 72 `Mathlib.*` existem no mathlib do sandbox. A integração é só adição.
  - Os 26 módulos de K usados pela cadeia do traço: CanonicalFockBWR2, DualWeightR3, FaithfulWeightR2, FiniteStarCoreR1, FiniteWeightR4, GNSR5, GNSRepresentationR6, RegularCoreR2, WeightClosedTomitaR2, WeightModularFlowR3, WeightModularOperatorR3, ClosedTomitaOperatorR1, L2UnitaryMapR2, PositiveRegularizedRootR3, RegularCoreAverageR2, RegularCoreFiniteWeightR3, RegularCoreFixedR3, RegularCovariantCoreR3, RegularFiniteStarCoreR2, RegularScalarClosedTomitaR1, RegularScalarGNSActionR2, RegularScalarGNSR3, RegularScalarGNSRepresentationR2, RegularScalarGNSStrongContinuityR1, WedgeNonabelianR4, WeylAntiunitaryR4.
- Compilação [REAL]:
  - Cada um dos 162 módulos tem recibo EXIT0 (varredura dos 1299 recibos). Soma dos tempos: ≈33 989 s (≈9,4 h de `lean -j2` por módulo, incluindo import; não é estimativa de lake build).
  - O build final usou LEAN_PATH = `...\tgl_kernel\.lake\build\lib\lean` (e pacotes do kernel) + `dependency_cache` com 474 .olean planos: 175 homônimos de K e 299 fora de K.
  - Toolchain Lean 4.31.0, igual ao `lean-toolchain` do kernel.
- Higiene da cadeia do traço: sem sorry, admit, axiom ou native_decide; 14 módulos com `#eval`; 2 com `IO.FS` (CanonicalFockPolarRightCutoffsR13, R7SineWindowClosureProbeR5); maxHeartbeats até 2 500 000 (GeneralRegularImaginaryPowersR1, GeneralRegularAffiliationR1).

### 2.4 Relatório sobre os quatro itens abertos
Os quatro itens abertos são R3, R4, R5 e R10, e não campos do contrato do traço (R7 está aceito na bancada).
- B\mission_review_20261016\R52_R7_ACCEPT_PREPARATION_R1.json, `other_requirements`:
  - R10: "Revisao independente e entrega conjunta. ... ratificacao da c1 distinta ..." (open).
  - R3: "Rito integral da candidata v394. Main completo na copia, kernel/consumidores/artigos/saidas e recibos; nenhum baseline substitui execucao atual." (open).
  - R4: "Ligacao fisica do espectro e relogio..." (open). R5: "Rede global e realizacao do dispositivo..." (open). R8 estava "working" e foi aceito depois.
- B\mission_review_20261016\R53_JOINT_SOURCE_REVIEW_R1.json: veredito `PASS_DIAGNOSTIC_ONLY_R4_R5_REMAIN_OPEN`. `remaining`: "R4: identificação física de estado, energia/zero, referencial, relógio SI, N e domínios do mesmo sistema." e "R5: setor do aparelho e representação/limite controlado com V completo e localização; rede física e R7/R8 já aceitos são reutilizados."
- B\R54_DEVICE_IDENTITY_PENDING.json: R4 e R5 "blocked". `pending_input`: "Identify the intended mechanical device/sector: MQC, Supercondutor or Psi-NET." Nota: "Resume only after the identifying input".
- B\CONFERENCIA_PONTE_DISPOSITIVO_R55.txt [DERIVED]: a exigência de escolher um só dispositivo "foi prematura"; R4/R5 seguem bloqueados no registro (revisão 424).
- AV:1686 (R52): "[REAL] R7 aceito por revisor distinto no criterio original. Os 21 campos de RemainingModularCoreInput foram preenchidos e especializados em physicalCanonicalNet/physicalFockCertificate. ... [OPEN] R4/R5 ...; R3: candidato e rito integral; R10: revisao final. A missao nao terminou." AV:1705 (R53): "R4/R5, R3 e R10 continuam abertos". Antecedentes: AV:1631 (R49, lei tracial), AV:1646 (R50, pacote positivo), AV:1665 (R51, extensão cíclica e split aberto).
- Escopo do aceite R7 (R52_R7_FULL_REVIEW_R1.json, `trace_scope.not_claimed`): "Funcional complexo linear em todo o core"; "Aditividade total fora do cone positivo"; "Classificação do fator como tipo II∞"; "Equivalência do core Fock com SiteProfile". O revisor é `codex-mission-memory-review` (distinto do autor, declarado). Não há ratificação humana nem da c1 (isso é R10).
- Frente separada (gravitação H3): B\completion_audit_r90\BALANCO_DA_META_R90.md (AV:2175, R90) lista três pendências (variação→ação integrada, estacionariedade de δS_total[P], fonte completa). Não é a frente do traço.

## 3. PERGUNTA 3 — tipos

**`RepresentedCore`** (K\CanonicalModularCoreAssemblyR1.lean:23; namespace `F1Fecho.NetworkModularCore`):
- `abbrev RepresentedCore := F1Fecho.CanonicalFockRegular.core.toStarSubalgebra`, que é um `StarSubalgebra ℂ (RegularHilbert F →L[ℂ] RegularHilbert F)`. Em `trace : RepresentedCore → ENNReal` ele é coagido ao subtipo `{x // x ∈ ...}`.
- Cadeia de tipos:
  - `F` = `F1Rede.BosonicFock.F` := `SumSpace Sectors` (K\BosonicFock.lean:17), o Fock bosônico.
  - `RegularHilbert F` = `Lp F 2 (volume : Measure ℝ)` (T\V350L2OperatorLift.lean:12), ou seja, L²(ℝ; Fock).
  - `F1Fecho.CanonicalFockRegular.core` (K\CanonicalFockRegularCoreR2.lean:34) := `RegularCovariantCore.core fockFlow M : VonNeumannAlgebra (RegularHilbert F)` (K\RegularCovariantCoreR3.lean:113).
  - Isso é `generatedAlgebra (generators B M)` (T\V350RegularGeneratedAlgebra.lean:14), o bicomutante estrela de `fibre '' M ∪ range (regularUnitary fockFlow)`.
  - `M` = `CanonicalWedgeFlow.M` = `FieldWeyl.R KWR...` : `VonNeumannAlgebra F` (K\CanonicalWedgeFlowR2.lean:77).
- Instâncias do subtipo [REAL, mathlib do sandbox]:
  - `Ring`: via `StarSubalgebra.subringClass` (M\Algebra\Star\Subalgebra.lean:89) e `SubringClass.toRing`.
  - `StarRing`: `StarSubalgebra.starRing` (:94).
  - `Algebra ℂ`: `StarSubalgebra.algebra` (:100).
  - Também `StarModule ℂ`: `StarSubalgebra.starModule` (:103).
  - `CStarAlgebra` só com `[IsClosed]` (`StarSubalgebra.cstarAlgebra`, M\Analysis\CStarAlgebra\Classes.lean:50); o kernel usa `vonNeumann_norm_closed` localmente (ex.: T\V354PositiveTraceTransport.lean:31).
- `toRemainingWeyl` (K\CanonicalModularCoreAssemblyR1.lean:73-115) preenche `instCR`, `instCS`, `instCA` com `inferInstance`. O mesmo bloco de 21 campos aparece em `RemainingFockInput` (CanonicalFockAssemblyR1.lean), `RemainingAnalyticInput` (CanonicalFockAntiAssemblyR4.lean) e `RemainingWeylInput` (CanonicalWeylAssemblyR5.lean:19-70).
- `dualAction : ℝ → (RepresentedCore ≃⋆ₐ[ℂ] RepresentedCore)` (K\RegularCovariantCoreR3.lean:163).
- O `trace` pedido é uma função TOTAL do subtipo em `ENNReal`, sem exigir ordem. Exige `trace_tracial` para todo par x y e `trace_star` para todo x, não só para positivos.
- O contrato exige a escala só em PF = Pp+Pm; não exige aditividade geral do traço.
- Também precisa de `D : CanonicalNetInput` (K\CanonicalFockAssemblyR1.lean:24). Não há habitante de `CanonicalNetInput` no kernel (busca em T, K, TGL: só `#print axioms` em NetworkProofAuditR3.lean:252-257). Na bancada: `physicalCanonicalNet` (B\orbital_rotation\PhysicalCanonicalNetCompleteR1.lean). O `modularCoreInput` da bancada é genérico em D.

## 4. PERGUNTA 4 — mathlib do sandbox (só nomes)
**CFC limitado.**
- Arquivos: M\Analysis\CStarAlgebra\ContinuousFunctionalCalculus\{Basic,Commute,Continuity,Instances,Integral,Isometric,NonUnital,Order,Pi,Projection,Range,RealImaginaryPart,Restrict,Unique,Unital,Unitary}.lean; M\Analysis\SpecialFunctions\ContinuousFunctionalCalculus\{Abs, ExpLog\{Basic,Order}, PosPart\{Basic,Isometric}, Rpow\{Basic,ConjSqrt,IntegralRepresentation,Isometric,Order,RingInverseOrder}}.lean.
- Decls usadas pelos arquivos:
  - Unital.lean: `cfc`, `cfc_apply`, `cfc_mul`, `cfc_comp'`, `cfc_id'`, `cfc_congr`, `cfc_const`, `cfc_algebraMap`, `cfc_add`, `cfc_sub`, `cfc_neg`, `cfc_star`, `cfc_commute_cfc`, `cfc_const_mul`, `cfc_const_add`, `cfc_const_mul_id`, `cfc_map_div`, `cfcHom`, `cfcHomSuperset`, `cfcHom_continuous`, `cfcHom_id`.
  - Outras: `cfc_real_eq_complex` (Instances), `cfcₙ`, `cfcₙ_eq_cfc` (NonUnital), `cfcₙ_mem`, `cfc_mem` (Range), `StarAlgHomClass.map_cfc` (Unique).
  - Rpow\Basic: `CFC.sqrt`, `CFC.sqrt_nonneg`, `CFC.sqrt_mul_sqrt_self`, `CFC.sqrt_eq_real_sqrt`, `CFC.sqrt_unique`, `CFC.sqrt_eq_iff`, `CFC.sqrt_mul_self`, `CFC.sqrt_zero`, `CFC.mul_self_eq_mul_self_iff`.
  - PosPart\Basic: `CFC.posPart_nonneg`, `CFC.negPart_def`, `CFC.negPart_nonneg`, `CFC.negPart_mul_posPart`, `CFC.posPart_eq_zero_iff`, `CFC.posPart_sub_negPart`.
  - CFC\Order: `CStarAlgebra.norm_le_norm_of_nonneg_of_le`, `CStarAlgebra.norm_le_iff_le_algebraMap`, `CStarAlgebra.norm_le_one_iff_of_nonneg`.
  - Ordem e adjunta: `IsSelfAdjoint.of_nonneg`, `star_left_conjugate_nonneg`, `star_left_conjugate_le_conjugate` (M\Algebra\Order\Star\Basic.lean); `CStarRing.star_mul_self_eq_zero_iff` (M\Analysis\CStarAlgebra\Basic.lean); `ContinuousLinearMap.instLoewnerPartialOrder`, `ContinuousLinearMap.nonneg_iff_isPositive` (M\Analysis\InnerProductSpace\Positive.lean).
- Nomes "cfc_*" que NÃO são do mathlib e são do kernel: `cfc_intertwine` (K\CFCIntertwiningR3.lean:12), `real_cfc_intertwines` (T\V350PositiveRootIntertwining.lean:15), `realScalarMultiplier_cfc_ae` (T\V351ScalarMultiplierCalculus.lean:73).

**Não limitado / resolvente.**
- Mathlib: M\Analysis\InnerProductSpace\LinearPMap.lean (`LinearPMap.adjoint_isClosed`, `adjoint_graph_eq_graph_adjoint`, `adjoint_isFormalAdjoint`, `isSelfAdjoint_def`, `IsFormalAdjoint`); M\LinearAlgebra\LinearPMap.lean (`mem_graph_iff`, `mem_domain_of_mem_graph`, `le_of_le_graph`, `le_graph_of_le`, `eq_of_eq_graph`); M\Analysis\Normed\Operator\Extend.lean (`extendOfNorm`, `extendOfNorm_eq`).
- Não encontrei no mathlib CFC, teorema espectral nem Stone para auto-adjunto ilimitado. Procurei "unbounded|Stone's theorem|spectral measure|Cayley transform|spectral theorem" em Analysis e Algebra; acertos só em InnerProductSpace\Spectrum.lean e Matrix\*Spectrum*.
- Em casa (construído sobre cfc): `partialPositiveResolvent` (T\V350PartialPositiveResolvent.lean:43), `resolventGraphOperator` (T\V350ResolventGraph.lean:13), `resolventDampingOperator` / `resolventPhaseOperator` (T\V351ResolventPhaseCalculus.lean:13,15), `resolventDamping` / `resolventPhaseFunction` (T\V351ResolventPhaseFunctions.lean:14,17), `selfadjointSquareResolvent` (T\O16\SelfadjointSquareResolvent.lean), `modularR` (K\CanonicalFockGraphRealizationR3.lean:74).

**Potências imaginárias.**
- Mathlib não tem potência imaginária de operador (só `CFC.nnrpow`, M\...\Rpow\Basic.lean:90).
- Insumos do mathlib: `Real.sigmoid`, `sigmoid_nonneg`, `sigmoid_le_one`, `sigmoid_pos`, `sigmoid_lt_one`, `sigmoid_neg`, `sigmoid_mul_rexp_neg` (M\Analysis\SpecialFunctions\Sigmoid.lean); `Real.sinc` (M\Analysis\SpecialFunctions\Trigonometric\Sinc.lean); `Complex.exp*`, `Real.log*`, `Real.exp_*`.
- Em casa: `resolventImaginaryPower` (T\V351ResolventImaginaryPowers.lean:38), `modularPhase` (T\ModularFlowLevel.lean:28).
- Arquivos de K que usam essas peças: CFCIntertwiningR3, CanonicalFockGraphRealizationR3, CanonicalFockModularFlowR2, ClosedTomitaFlowR1, ImaginaryPowerIntertwiningR2, PositiveRegularizedRootR3, ScalarL2CalculusR4, ScalarL2ImaginaryR5, TensorResolventScalarsR4.

**ENNReal / pesos.**
- Arquivos: M\Data\ENNReal\{Basic,Operations,Inv,Real}.lean; M\Topology\Instances\ENNReal\Lemmas.lean; M\MeasureTheory\Integral\Lebesgue\{Basic,Add}.lean; M\MeasureTheory\Integral\Bochner\Basic.lean.
- Decls: `ENNReal.ofReal_toReal` (Basic), `ofReal_coe_nnreal` (Basic), `iSup_add_iSup_of_monotone` (Operations), `mul_iSup` (Inv), `ofReal_inv_of_pos` (Inv), `toReal_ofReal_mul` (Real), `ofReal_mul` (Real), `ofReal_lt_one` (Real), `continuous_ofReal` e `continuous_const_mul` (Topology\...\Lemmas), `lintegral_const_mul`, `lintegral_liminf_le`, `lintegral_iSup`, `lintegral_add_left` (Lebesgue\Add), `lintegral_congr_ae` (Lebesgue\Basic), `ofReal_integral_eq_lintegral_ofReal` (Bochner\Basic).
- Em casa: `dualQuadraticIntegral` (T\V350DualWeightForm.lean:62), `dualHaarFactor` (:17), `HasFiniteDualSquare` (T\V350DualSemifiniteIdeal.lean:18), `dualAmbient` (T\V350RegularDualAction.lean:18).

**Fourier, Plancherel e operadores.**
- Mathlib: `Lp.fourierTransformₗᵢ` (M\Analysis\Fourier\LpSpace.lean); `Real.fourier_real_eq_integral_exp_smul` (M\Analysis\Fourier\FourierTransform.lean); `intervalIntegral.integral_hasDerivAt_right` (M\MeasureTheory\Integral\IntervalIntegral\FundThmCalculus.lean); `Measure.integral_comp_div` (M\MeasureTheory\Measure\Haar\NormedSpace.lean:167).
- Em casa: `Fourier.fourier_integral_memLp_two` e `Fourier.fourier_integral_norm_sq` (T\V350FourierL1L2.lean:51,71).
- Mathlib (estrutura): `VonNeumannAlgebra` (M\Analysis\VonNeumannAlgebra\Basic.lean:55), `StarSubalgebra` (M\Algebra\Star\Subalgebra.lean), `Submodule.starProjection` (M\Analysis\InnerProductSpace\Projection\Basic.lean), `conjStarAlgEquiv` e `Unitary.linearIsometryEquiv` (M\Analysis\InnerProductSpace\Adjoint.lean), `Unitary.conjStarAlgAut` (M\Algebra\Star\UnitaryStarAlgAut.lean).

## 5. O QUE FALTA, EM ORDEM

**Leitura**
- Contra o kernel como está, todos os passos faltam, mas nenhum precisa de matemática nova: o molde existe compilado (torre) e a portada existe compilada (bancada).
- O trabalho restante é de integração (R3) e revisão (R10), não de construção.
- Não verifiquei se um `lake build` do kernel com os módulos adicionados passa; os recibos da bancada foram obtidos com módulos de nome plano e `lean -o` individual.

**Mapa dos 21 campos** (fornecedor na bancada, `modularCoreInput`, CanonicalFockModularCoreInputR1.lean:77-105)

| campo | fornecedor |
|---|---|
| trace | `cyclicTraceCandidate` (CyclicTraceCompletionR3:31) |
| trace_zero | `cyclicTraceCandidate_zero` (:145) |
| trace_tracial | `cyclicTraceCandidate_cyclic` (:48) |
| trace_star | `cyclicTraceCandidate_star` (:64) |
| trace_dual_scaling | `cyclicTraceCandidate_dual` (:105) |
| PF, PF_sa, PF_idem | `positiveAsCore (add q r)` com (q, r) por `Classical.choose normalized_split_exists` (SplitR5:225); `IsStarProjection.add` |
| PF_ne | de trace PF = 1 e `trace_zero` |
| PF_pos, PF_fin | `cyclicTraceCandidate_positive` (CyclicR3:137) e value(q+r)=1 |
| Pp, Pm, Pp_sa, Pp_idem, Pm_sa, Pm_idem | `positiveAsCore q`, `positiveAsCore r`, `chosen_split` |
| split | `rfl` |
| orth | `q.val*r.val=0` de `normalized_split_exists` |
| trace_additive | `value_add` (ActualInverseAdditivityR2:212) mais `cyclicTraceCandidate_positive` |
| equal_halves | igualdade `value q = value r` do split (SplitR5, via lei quadrática de `finite_equal_split_generic`) |

**Sub-passos, em ordem de dependência** (bancada = B, torre = T, entradas já em K entre parênteses)
1. **Gerador positivo h genérico:** grafo, resolvente, h^{it}=λ(t), afiliação, escala dual.
   - B: GeneralRegularPositiveGraphR2, GeneralRegularSpectralGraphR2, GeneralRegularImaginaryPowersR1, GeneralRegularAffiliationR1, GeneralRegularDualScalingR2.
   - T: V351RegularPositiveGraph, V351RegularImaginaryPowers.
   - K: `UnitaryFlow`, `regularUnitary`, `dualAmbient`, `ImaginaryPowerIntertwiningR2`.
2. **Cortes:** inverso (h+ε)^{-1}, domínio, janela seno, fecho CFC e álgebra polar direita.
   - B: GeneralRegularInverseCutoffR1, GeneralRegularDomainCutR1, GeneralSineResolventApproxR2, GenericClosedEquationsCFCR5, R7SineWindowClosureProbeR5, CanonicalFockPolarRightClosureR10, CanonicalFockPolarRightCutoffsR13.
   - T: V351InverseGeneratorCutoff, V351InverseCutoffCFC, V351SineResolventApprox.
   - K: `cfc_intertwine`, `PositiveRegularizedRootR3`.
3. **Passo (i):** unitário de coeficientes e identificação modular Δ^{it}=λ_t ρ_{-t}.
   - B: CanonicalFockCoefficientGNSR1 (e CoefficientIntervals/Inclusion/Unitary/Dense), CanonicalFockModularGraphEqualityR1, CanonicalFockPolarFlipR4, CanonicalFockRightPolarBridgeR5, CanonicalFockModularIdentificationR17.
   - K: `scalarTomitaImaginaryPower`, `closedTomita`, `scalarTomitaResolvent`, `canonical_pair_tomita`.
4. **Balanço modular limitado, duplo corte, formas de raiz, aditividade:**
   - B: GenericPolarModularBalanceR1, CanonicalFockActualModularBalanceR6, CanonicalFockActualDoubleCutR2, CanonicalFockActualRootCutFormsR2, CanonicalFockActualInverseAdditivityR2.
   - T: V351ModularCutBalance, V351QuadraticTrace (moldes).
5. **Peso perturbado e pacote positivo:**
   - B: GeneralInverseCutoffWeightR3, GeneralInverseSupremumR3, CanonicalFockInverseSupremumR2, CanonicalFockInverseNormalR1, CanonicalFockActualInverseFinitenessR2, CanonicalFockActualPositiveTracePackageR2.
   - K: `weight`, `weight_faithful`, `finiteStarCore`, `regularSandwich`.
6. **Lei tracial:** star-core finito e depois todo o núcleo limitado.
   - B: CanonicalFockActualStarCoreTracialR1, CanonicalFockActualTracialExtensionR1, GeneralInverseFiniteApproximationR1.
   - K: `finiteStarCore_strongStar_approximation`.
7. **Completação cíclica ENNReal** (5 campos `trace_*`):
   - B: CanonicalFockPositiveShiftTransportR2, CanonicalFockCyclicTraceCompletionR3.
   - T/genérico já em casa: V354TraceShiftEquivalence, V354BoundedPolar, V354PolarIntertwining.
8. **Canto, subprojeção finita, split normalizado** (16 campos PF/Pp/Pm/trace_additive/equal_halves):
   - B: MatrixCornerFromNilpotentR3, CanonicalFockMatrixCornerR2, CanonicalFockFiniteProjectionR3, CanonicalFockNormalizedSplitR5.
   - T genérico: V354SpectralThreshold, V354FiniteTraceSupport.
   - K: `wedge_nonabelian`, `FieldWeyl.W`.
9. **Montagem:** `modularCoreInput` (CanonicalFockModularCoreInputR1). Com `D : CanonicalNetInput` explícito; para `physicalFockCertificate` usar `physicalCanonicalNet` (rede física, ~138 módulos extras Maxwell/orbital_rotation).

**Pontos de atenção antes de integrar**
- Copiar só a versão MAIS ALTA de cada radical que está no fecho. Não importar R10/R11/R12 de CutoffOrder (mortos).
- Reescrever imports para `TGLExt.F1Fecho394.`; remover os `#eval IO.FS...` de CanonicalFockPolarRightCutoffsR13 e R7SineWindowClosureProbeR5 e os demais `#eval`.
- Registrar os módulos em TGLExt.lean/NetworkProofAuditR*.
- O docstring dos fontes diz "UNCOMPILED CANDIDATE" em muitos arquivos já compilados. É texto de nascimento; vale o recibo.
- O traço é ENNReal-cíclico: não é funcional linear, não afirma tipo II∞.
- R4 e R5 dependem de decisão humana sobre o dispositivo e não bloqueiam os 21 campos.
- R10 (ratificação da c1) e R3 (rito integral) continuam abertos.
- Aceitação R7 é de revisor Codex declarado distinto, não de auditoria Claude nem humana.
