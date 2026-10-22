import TGLExt.TheMasterFires
import TGLExt.StrongFrame
import TGLExt.V354RegularLegacyWitness
import TGLExt.PoincareGroup
import TGLExt.ProfileEntropyLimits
import TGLExt.TheImportedEquilibrium

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option linter.unusedVariables false
set_option maxHeartbeats 1000000

/-!
# CONTRATO DE TIPO v3.1 DE H2 / H3 / IMPORT-H3 — O TIPO (só definições)
  [TGLExt — v371, pedra da gerência (25/09/2026), por ordem do operador «sim, entra tudo»; transposta de
   `scratchpad\contrato_v3\v31\ContratoQG_v31.lean` (sha16 e44e485a79dacf01): mudam SÓ o caminho do módulo, os imports locais, o namespace da reta de luz
   (se houver) e este cabeçalho; renomes para o índice da IALD não ver homônimo: screenBlock → screenBlockV31.
   NÃO cunha nome reservado; NÃO move o gate; PROVADA ≠ CONFIRMADA]
  ⚠ v371: entram no kernel SÓ o tipo (este arquivo), `ContratoQG_v31_Teoremas` e `FlagNetV31`. As
  `ContratoQG_v31_Paredes`, `PonteV3V31` e os probes ficam FORA: importam o contrato v2, a v3 e os brinquedos,
  e os probes falham por construção (rc = 1 esperado). O leitor H2/H3 (G_W2) segue DESLIGADO; os quatro
  índices (W₀, R₀), N₀, T₀ e o tipo de `m_pos` seguem [INPUT] a ratificar pelo operador.
  ⚠ VACUIDADE, dita: nenhum habitante de ContratoH2/ContratoH3 v3.1 é exibido no kernel; a não-vacuidade para o campo livre
  é argumento à mão (DIVERGENCIAS.md §2.7/§3), NÃO teorema — os teoremas deste contrato valem para todo habitante, possivelmente
  nenhum. O único par concreto do kernel, o legado, NÃO o habita (teorema). `ContratoImportH3.nonvacuous` é condicional; o índice
  h2 do import não entra em campo algum.


  A v3.1 é a v3 (74e2f6be62211c04) CORRIGIDA pelos dois céticos da rodada 1. Este arquivo tem SÓ o tipo;
  teoremas em `ContratoQG_v31_Teoremas.lean`, paredes em `ContratoQG_v31_Paredes.lean`. As divergências
  (o que se aceitou, o que se recusou e com que fonte) estão em `DIVERGENCIAS.md`.

  Os tipos que os nomes reservados terão de habitar (NENHUM é cunhado aqui):

    TGLExt.qgPrice_H2_smoothModularFourFrame_discharged    : ContratoH2 W₀ R₀ N₀
    TGLExt.qgPrice_H3_localHorizonEquilibrium_discharged  : ContratoH3 W₀ R₀ N₀ T₀
    TGLExt.qgImport_H3_horizonEquilibriumData_produced    : ContratoImportH3 W₀ R₀ N₀ T₀ qgPrice_H2_…

  com (W₀, R₀) o par a ratificar (partição M01), N₀ a NORMALIZAÇÃO DO KILLING e T₀ o TENSOR DE
  ENERGIA-MOMENTO do par. Os quatro são ÍNDICES, parametrizados; nenhum é escolhido aqui.

## O que muda da v3 para a v3.1 (e porquê — ver DIVERGENCIAS.md)
  (κ)  [cético 1 IMPORTANTE, cético 2 IMPORTANTE — ACEITO] na v3 o VALOR de κ era calibre (`rekappa`,
       `regauge`): o tipo só fixava o produto β_Killing·κ = 2π. Na v3.1 a calibração é um ÍNDICE EXTERNO
       `N : KillingNormalization` [INPUT]: o ponto de referência (relógio/detector) cuja aceleração
       própria é κ. Dentro de `ContratoH2 W R N`, κ é FIXO (teorema `kappa_fixed`); mas o par (W, R) NÃO
       fixa κ (teorema `kappa_is_input`: todo N' é realizado). A frase «κ amarrado» da v3 está retirada.
  (H3) [cético 1 BLOQUEANTE, cético 2 IMPORTANTE — ACEITO] H3 v3 era pagável por AJUSTE estado a estado
       (resposta e matéria livres por estado; `toyH3`, `adjustH3`, `genericImport`). Na v3.1:
       * a matéria NÃO é do habitante: é o índice `T : StressTensorData W` (a expectativa ⟨ψ, T_ab(x) ψ⟩,
         nula no vácuo e COVARIANTE por translações);
       * o elo matéria ↔ fluxo modular é campo: a energia modular de ψ é 2π × a carga nula de T no plano
         nulo do horizonte (`modular_charge`) [KNOWN como exigência: Casini–Teste–Torroba 2017;
         Faulkner–Leigh–Parrikar–Wang 2016];
       * a resposta geométrica NÃO é escolhida por estado: é h_ψ := 𝔉(T(ψ)), com o PROPAGADOR 𝔉 — um funcional
         FIXO do campo de tensão, escolhido junto com G, antes de todo ψ — nulo na fonte nula e COVARIANTE por
         translações (a opção 2 do cético 1: «response := 𝔉(matter ψ), 𝔉 escolhido junto com G»). Logo
         mesma ⟨T⟩ ⟹ mesma geometria (`same_source_same_geometry`) e a covariância da resposta é TEOREMA.
         h_ψ é simétrica, no gauge do cone de luz (h·n = 0), e obedece à lei LOCAL Raychaudhuri–Einstein
         ao longo de TODO gerador nulo de direção n, em TODO ponto x:
             d/dλ θ_ψ(x + λn) = −8πG·T_nn(ψ)(x),   θ_ψ := d/dλ (densidade de área linearizada);
       * Bekenstein–Hawking, Clausius e o 8πG passam a TEOREMAS DE JANELA (todo corte nulo c, toda janela
         [c, d] com expansão nula no fim), por integração exata (sem aproximação de janela pequena).
       Os ajustadores dos céticos (resposta por estado, matéria constante por estado) NÃO habitam
       (probes portados; refutações `slope_response_excluded`, `exp_response_excluded`,
       `expansion_not_constant`).
  (δS) [cético 2 IMPORTANTE — ACEITO] o δS da v3 era a energia modular BILATERAL (−log Δ = K_W − K_W′),
       sem termo de 1ª ordem em Ω + εφ; o rótulo «primeira lei, 1ª ordem» era falso para ela. Na v3.1 o
       δS de H3 é a carga UNILATERAL do corte nulo, 2π∫_c^d (λ − c)T_nn — lida de T, não de Δ; a energia
       bilateral fica só no elo `modular_charge`. A identidade «δQ = T_U·δS» é DEFINICIONAL (Clausius como
       leitura), e é dita assim.
  (G)  [cético 2 IMPORTANTE, parte «G é livre como um todo» — RECUSADO COMO DEFEITO, com fonte] na rota de
       Jacobson G = 1/(4ħη) é ENTRADA (η, a densidade de entropia por área, não é derivada) [KNOWN: Jacobson
       1995, PRL 75, 1260]. A v3.1 torna isso TEOREMA honesto (`G_not_predicted`) em vez de escondê-lo;
       fixar G é o item UV do gate (interacting_…_UV_scope), não H3.

## Convenções (as mesmas da v3, ditas)
  U(a) = e^{i a·P}, (+,−,−,−); Δ^{it} = e^{−itK}, K = −log Δ; V(s) = e^{isB}; BW ⟹ K = 2πB.
  T(U(a)ψ)(x) = T(ψ)(x − a)  (Ad U(a) net(O) = net(O + a), a convenção do kernel).
  O plano nulo do horizonte: λ·n + (0, 0, y), n = (1, 1, 0, 0); λ > 0 é o horizonte futuro da cunha direita.
  Linearização em torno de Minkowski: densidade de área da tela a(h) = −(h₂₂ + h₃₃)/2 [DERIVED à mão:
  √det(1 − h_s) ≈ 1 − tr h_s /2]; Raychaudhuri linear dθ/dλ = −R_nn e, no gauge h·n = 0,
  R_nn = −d²a/dλ² [KNOWN]; Einstein nn: R_nn = 8πG T_nn.

## Estatutos
  [DERIVED] os lemas geométricos; [KNOWN como exigência] BW, KMS, Borchers, CTT, Raychaudhuri, Jacobson;
  [INPUT] N (o relógio), T (o tensor do par), G, a classe admissível; [OPEN] o par físico, as outras
  componentes de Einstein (exigem a família de Lorentz de cunhas; W não tem rotações).
  β jamais literal. Sem sorry, sem axiom. Nada aqui move o gate.
-/

namespace TGLExt.ContratoQGv31

open TGL.SpecificAQFT TGL.ModularRealization
open MeasureTheory Matrix Complex
open scoped InnerProductSpace

noncomputable section

/-! ## 0. A geometria do boost da cunha (sem ler campo de contrato) — idêntica à v3 -/

/-- a ação geométrica do boost no plano (0,1) (rapidez `s`), com a matriz `TGLExt.boostMat` do kernel. -/
def wedgeBoostMap (s : ℝ) (x : Fin 4 → ℝ) : Fin 4 → ℝ := (boostMat s).mulVec x

/-- o campo de Killing do boost normalizado por κ: ξ_κ(x) = κ·(x¹, x⁰, 0, 0). -/
def killingField (κ : ℝ) (x : Fin 4 → ℝ) : Fin 4 → ℝ := κ • ![x 1, x 0, 0, 0]

/-- o vetor nulo do horizonte futuro da cunha: n = (1, 1, 0, 0). -/
def nullDir : Fin 4 → ℝ := ![1, 1, 0, 0]

/-- [DERIVED] ★ A LEI DE GRUPO DO BOOST: boostMat(a+b) = boostMat a · boostMat b (lida de `theBoost_add`,
    PoincareGroup.lean:173). -/
theorem boostMat_add (a b : ℝ) : boostMat (a + b) = boostMat a * boostMat b := by
  have h := congrArg Subtype.val (theBoost_add a b)
  change boostMat a * boostMat b = boostMat (a + b) at h
  exact h.symm

theorem boostMat_zero : boostMat 0 = 1 := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [boostMat]

theorem wedgeBoostMap_add (a b : ℝ) (x : Fin 4 → ℝ) :
    wedgeBoostMap (a + b) x = wedgeBoostMap a (wedgeBoostMap b x) := by
  simp only [wedgeBoostMap, boostMat_add, Matrix.mulVec_mulVec]

theorem wedgeBoostMap_zero (x : Fin 4 → ℝ) : wedgeBoostMap 0 x = x := by
  simp [wedgeBoostMap, boostMat_zero]

theorem wedgeBoostMap_smul (s c : ℝ) (x : Fin 4 → ℝ) :
    wedgeBoostMap s (c • x) = c • wedgeBoostMap s x := by
  simp [wedgeBoostMap, Matrix.mulVec_smul]

theorem wedgeBoostMap_apply0 (s : ℝ) (x : Fin 4 → ℝ) :
    wedgeBoostMap s x 0 = Real.cosh s * x 0 + Real.sinh s * x 1 := by
  simp [wedgeBoostMap, boostMat, Matrix.mulVec, dotProduct, Fin.sum_univ_four]

theorem wedgeBoostMap_apply1 (s : ℝ) (x : Fin 4 → ℝ) :
    wedgeBoostMap s x 1 = Real.sinh s * x 0 + Real.cosh s * x 1 := by
  simp [wedgeBoostMap, boostMat, Matrix.mulVec, dotProduct, Fin.sum_univ_four]

/-- [DERIVED] o vetor nulo é autodireção do boost com dilatação e^s. -/
theorem wedgeBoostMap_nullDir (s : ℝ) : wedgeBoostMap s nullDir = Real.exp s • nullDir := by
  funext i
  fin_cases i <;>
    simp [nullDir, wedgeBoostMap, boostMat, Matrix.mulVec, dotProduct, Fin.sum_univ_four,
      ← Real.cosh_add_sinh]

/-! ## 1. As condições analíticas nomeadas e as expectativas dos geradores — idênticas à v3 -/

def kmsStrip (β : ℝ) : Set ℂ := {z | 0 < z.im ∧ z.im < β}

def upperHalf : Set ℂ := {z | 0 < z.im}

def forwardCone : Set (Fin 4 → ℝ) := {a | 0 ≤ a 0 ∧ 0 ≤ minkowskiSq a}

/-- **KMS a β** (forma vetorial) de um grupo a um parâmetro α sobre (W.net cunha, W.vac). [KNOWN:
    caracteriza o grupo modular (Takesaki); aqui é DEFINIÇÃO de tipo.] -/
def KMSAt (W : TGLSpecificAQFTWitness) (α : ℝ → (W.H ≃ₗᵢ[ℂ] W.H)) (β : ℝ) : Prop :=
  ∀ A ∈ W.net rightWedge, ∀ B ∈ W.net rightWedge, ∃ F : ℂ → ℂ,
    DiffContOnCl ℂ F (kmsStrip β) ∧
    (∃ M : ℝ, ∀ z : ℂ, 0 ≤ z.im → z.im ≤ β → ‖F z‖ ≤ M) ∧
    (∀ t : ℝ, F t = ⟪(star A) W.vac, α t (B W.vac)⟫_ℂ) ∧
    (∀ t : ℝ, F (t + β * I) = ⟪(star B) W.vac, α (-t) (A W.vac)⟫_ℂ)

/-- **Energia positiva** (forma analítica) [KNOWN: equivalente a a·P ≥ 0; aqui é DEFINIÇÃO]. -/
def PositiveEnergy (W : TGLSpecificAQFTWitness) : Prop :=
  ∀ a ∈ forwardCone, ∀ ψ : W.H, ∃ F : ℂ → ℂ,
    DiffContOnCl ℂ F upperHalf ∧
    (∃ M : ℝ, ∀ z : ℂ, 0 ≤ z.im → ‖F z‖ ≤ M) ∧
    (∀ t : ℝ, F t = ⟪ψ, W.U (t • a) ψ⟫_ℂ)

/-- a expectativa do hamiltoniano modular BILATERAL K = −log Δ: d/dt ⟪ψ, Δ^{it}ψ⟫|₀ = −i·k. -/
def HasModularEnergy {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    (Δit : ℝ → (H ≃ₗᵢ[ℂ] H)) (ψ : H) (k : ℝ) : Prop :=
  HasDerivAt (fun t : ℝ => ⟪ψ, Δit t ψ⟫_ℂ) (-(I * (k : ℂ))) 0

/-- a expectativa do gerador do boost B (V(s) = e^{isB}): d/ds ⟪ψ, V(s)ψ⟫|₀ = i·b. -/
def HasBoostEnergy {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    (V : ℝ → (H ≃ₗᵢ[ℂ] H)) (ψ : H) (b : ℝ) : Prop :=
  HasDerivAt (fun s : ℝ => ⟪ψ, V s ψ⟫_ℂ) (I * (b : ℂ)) 0

/-- «Δit não tem autovetor fora da reta do vácuo» — a MESMA forma de `W5Final.Espectral.NoEigenOutsideVacuum`. -/
def NoEigenOutsideVacuum (W : TGLSpecificAQFTWitness) (D : ℝ → (W.H ≃ₗᵢ[ℂ] W.H)) : Prop :=
  ∀ (v : W.H) (r : ℝ), (∀ t : ℝ, D t v = ChatgptAudit.modularPhase t r • v) → v ∈ (ℂ ∙ W.vac)

/-! ## 2. O GRUPO DE BOOSTS da cunha, representado em W.H — idêntico à v3 -/

/-- **WedgeBoostRep W** — representação unitária fortemente contínua do grupo de boosts, tipada pela
    `boostMat` do kernel. As paredes `no_injective_isometric_boost_intertwiner` (ModularSignatureObstruction:102)
    e `tower_modular_cannot_intertwine_nonzero_boost` (Order007Bridges:47) NÃO são contrariadas: V age em W.H
    e U é multiplicativo; nenhuma aplicação LINEAR injetiva ℝ⁴ → W.H é entrelaçada. -/
structure WedgeBoostRep (W : TGLSpecificAQFTWitness) where
  V : ℝ → (W.H ≃ₗᵢ[ℂ] W.H)
  V_zero : V 0 = LinearIsometryEquiv.refl ℂ W.H
  V_add : ∀ a b : ℝ, V (a + b) = (V b).trans (V a)
  V_continuous : ∀ ψ : W.H, Continuous (fun s : ℝ => V s ψ)
  V_vac : ∀ s : ℝ, V s W.vac = W.vac
  V_translations : ∀ (s : ℝ) (a : Fin 4 → ℝ),
    (V s).conjStarAlgEquiv (W.U a) = W.U (wedgeBoostMap s a)
  V_net : ∀ (s : ℝ) (O : Set (Fin 4 → ℝ)) (T : W.H →L[ℂ] W.H),
    T ∈ W.net O → (V s).conjStarAlgEquiv T ∈ W.net (wedgeBoostMap s '' O)

/-! ## 2½. ★ NOVO: a NORMALIZAÇÃO DO KILLING, como índice externo [INPUT] -/

/-- **KillingNormalization** [INPUT, EXTERNO ao par] — o relógio que fixa a ESCALA do campo de Killing: um
    ponto de referência na cunha (o observador/detector cujo tempo próprio é o tempo físico). No espaço plano
    nada no par (W, R) escolhe esse ponto (teorema `kappa_is_input`); κ é a aceleração própria dele. Para o
    κ_H de um buraco negro, a normalização é a assintótica (ξ → ∂_t no infinito) — FORA deste tipo plano
    [OPEN]. -/
structure KillingNormalization where
  point : Fin 4 → ℝ
  point_in_wedge : point ∈ rightWedge

/-! ## 3. CONTRATO H2 v3.1 -/

/-- **ContratoH2 W R N** (v3.1) — igual à v3 (fidelidade, espectro contínuo, BW como campo, KMS), com o
    observador fiducial substituído pelo ÍNDICE N: `observer_unit` pede |ξ_κ| = 1 NO PONTO DE REFERÊNCIA de N,
    logo κ = 1/ρ(N) (teorema `kappa_eq_inv_radius`) — fixo dado N, livre como função de (W, R). -/
structure ContratoH2 (W : TGLSpecificAQFTWitness) (R : TGLModularRealization W)
    (N : KillingNormalization) where
  /-- (A) a normalização do campo de Killing — determinada por N (`observer_unit`). -/
  kappa : ℝ
  kappa_pos : 0 < kappa
  /-- (Δ) o implementador do fluxo de R em vetores. -/
  Δit : ℝ → (W.H ≃ₗᵢ[ℂ] W.H)
  /-- (Δ) o fluxo da camada 1A de R É Ad(Δ^{it}). -/
  flow_implemented : ∀ (t : ℝ) (a : R.modular.wedgeAlgebra.toStarSubalgebra),
    ((R.modular.modularFlow t) a).val = (Δit t).conjStarAlgEquiv a.val
  /-- (KMS) Δit é o grupo modular de (W.net rightWedge, W.vac): KMS a β = 1 para t ↦ Δit(−t). -/
  kms : KMSAt W (fun t => Δit (-t)) 1
  /-- (S) o grupo de boosts da cunha, representado em W.H. -/
  boost : WedgeBoostRep W
  /-- (S) BISOGNANO–WICHMANN COMO CAMPO: Δ^{it} = V(Λ(−2πt)). -/
  bw : ∀ t : ℝ, Δit t = boost.V (-(2 * Real.pi * t))
  /-- (P) translações fortemente contínuas. -/
  translations_continuous : ∀ ψ : W.H, Continuous (fun a : Fin 4 → ℝ => W.U a ψ)
  /-- (P) O DENTE DE FIDELIDADE: só a translação nula age trivialmente. -/
  translations_faithful : ∀ a : Fin 4 → ℝ, W.U a = 1 → a = 0
  /-- (P) energia positiva (condição espectral), forma analítica. -/
  positive_energy : PositiveEnergy W
  /-- (P) ergodicidade nula: os invariantes da translação nula são múltiplos do vácuo. -/
  null_ergodic : ∀ ψ : W.H, (∀ l : ℝ, W.U (l • nullDir) ψ = ψ) → ψ ∈ (ℂ ∙ W.vac)
  /-- (K) ★ NOVO: |ξ_κ| = 1 no ponto de referência de N — κ é a aceleração própria do relógio externo. -/
  observer_unit : minkowskiSq (killingField kappa N.point) = 1
  /-- (C) o campo de frames, REGIONAL. -/
  E : (Fin 4 → ℝ) → Matrix (Fin 4) (Fin 4) ℝ
  smooth_on : ∀ i j : Fin 4, ContDiffOn ℝ (⊤ : ℕ∞) (fun x => E x i j) rightWedge
  det_unit_on : ∀ x ∈ rightWedge, IsUnit (E x).det
  /-- (D) o jato: arrasto pelo diferencial da ação geométrica do boost. -/
  dragged : ∀ (s : ℝ) (x : Fin 4 → ℝ), x ∈ rightWedge →
    E (wedgeBoostMap s x) = boostMat s * E x
  /-- (E) a fiducial é a direção do tempo modular, positivamente. -/
  fiducial_is_modular : ∀ x ∈ rightWedge,
    ∃ c : ℝ, 0 < c ∧ (fun i => E x i 0) = c • killingField kappa x

namespace ContratoH2

variable {W : TGLSpecificAQFTWitness} {R : TGLModularRealization W} {N : KillingNormalization}

/-- a temperatura de Unruh em tempo de Killing: o NÚMERO κ/2π (que ela é a temperatura KMS do fluxo de
    Killing é o teorema `unruh_is_kms`). -/
def unruhTemperature (C : ContratoH2 W R N) : ℝ := C.kappa / (2 * Real.pi)

/-- o FLUXO DE KILLING do campo ξ_κ, em tempo de Killing τ: τ ↦ V(κτ). -/
def killingFlow (C : ContratoH2 W R N) (τ : ℝ) : W.H ≃ₗᵢ[ℂ] W.H := C.boost.V (C.kappa * τ)

end ContratoH2

/-! ## 4. ★ NOVO: o tensor de energia-momento DO PAR e a geometria linearizada do plano nulo -/

/-- **StressTensorData W** [INPUT: índice do par, não do habitante de H3] — a expectativa
    T(ψ)(x) = ⟨ψ, T_ab(x) ψ⟩ (componentes covariantes), nula no vácuo (ordenamento normal) e COVARIANTE por
    translações na convenção do kernel (Ad U(a) net(O) = net(O + a) ⟹ U(a)* T(x) U(a) = T(x − a)).
    ⚠ Não se tipa aqui a forma sesquilinear nem a covariância de Lorentz (não são necessárias às paredes
    abaixo; são refinamento [OPEN]). -/
structure StressTensorData (W : TGLSpecificAQFTWitness) where
  T : W.H → (Fin 4 → ℝ) → Matrix (Fin 4) (Fin 4) ℝ
  T_vac : ∀ x : Fin 4 → ℝ, T W.vac x = 0
  T_covariant : ∀ (a : Fin 4 → ℝ) (ψ : W.H) (x : Fin 4 → ℝ), T (W.U a ψ) x = T ψ (x - a)

/-- o pareamento T(u, v) = uᵀ T v. -/
def pairing (A : Matrix (Fin 4) (Fin 4) ℝ) (u v : Fin 4 → ℝ) : ℝ := dotProduct u (A.mulVec v)

/-- a densidade de energia nula T_nn(ψ)(x) = nᵃ nᵇ T_ab. -/
def nullEnergy {W : TGLSpecificAQFTWitness} (T : StressTensorData W) (ψ : W.H) (x : Fin 4 → ℝ) : ℝ :=
  pairing (T.T ψ x) nullDir nullDir

/-- o ponto transversal (0, 0, y², y³). -/
def screenEmbed (y : Fin 2 → ℝ) : Fin 4 → ℝ := ![0, 0, y 0, y 1]

/-- a CARGA NULA BILATERAL de ψ no plano nulo do horizonte: ∫∫ λ T_nn(λn + y) dλ d²y (sobre λ ∈ ℝ).
    [KNOWN: −log Δ = 2π × esta carga (CTT 2017); aqui é o lado direito do campo `modular_charge`.] -/
def nullPlaneCharge {W : TGLSpecificAQFTWitness} (T : StressTensorData W) (ψ : W.H) : ℝ :=
  ∫ p : ℝ × (Fin 2 → ℝ), p.1 * nullEnergy T ψ (p.1 • nullDir + screenEmbed p.2)

/-- o bloco (2,3) de uma métrica: a métrica induzida na tela. -/
def screenBlockV31 (g : Matrix (Fin 4) (Fin 4) ℝ) : Matrix (Fin 2) (Fin 2) ℝ :=
  !![g 2 2, g 2 3; g 3 2, g 3 3]

/-- a DENSIDADE DE ÁREA LINEARIZADA da tela numa perturbação de métrica h (fundo de tela plana −1₂):
    a(h)(x) = −(h₂₂ + h₃₃)/2. -/
def areaDensity (h : (Fin 4 → ℝ) → Matrix (Fin 4) (Fin 4) ℝ) (x : Fin 4 → ℝ) : ℝ :=
  -(h x 2 2 + h x 3 3) / 2

/-- a CARGA UNILATERAL da janela [c, d] do gerador por x, acima do corte c:
    ∫_c^d (λ − c)·T_nn(ψ)(x + λn) dλ (o campo de Killing do corte c é (λ − c)n). -/
def windowCharge {W : TGLSpecificAQFTWitness} (T : StressTensorData W) (ψ : W.H) (x : Fin 4 → ℝ)
    (c d : ℝ) : ℝ :=
  ∫ l in c..d, (l - c) * nullEnergy T ψ (x + l • nullDir)

/-- a entropia da janela: δS = 2π × a carga unilateral (a primeira lei do corte nulo [KNOWN: CTT 2017];
    por construção, δS = δQ/T_U — Clausius como LEITURA). -/
def windowEntropy {W : TGLSpecificAQFTWitness} (T : StressTensorData W) (ψ : W.H) (x : Fin 4 → ℝ)
    (c d : ℝ) : ℝ :=
  2 * Real.pi * windowCharge T ψ x c d

/-- o calor da janela com o Killing do corte normalizado por κ: δQ = κ × a carga unilateral. -/
def windowHeat {W : TGLSpecificAQFTWitness} (κ : ℝ) (T : StressTensorData W) (ψ : W.H)
    (x : Fin 4 → ℝ) (c d : ℝ) : ℝ :=
  κ * windowCharge T ψ x c d

/-- a variação da densidade de área entre os cortes c e d do gerador por x. -/
def windowArea (h : (Fin 4 → ℝ) → Matrix (Fin 4) (Fin 4) ℝ) (x : Fin 4 → ℝ) (c d : ℝ) : ℝ :=
  areaDensity h (x + d • nullDir) - areaDensity h (x + c • nullDir)

/-! ## 5. CONTRATO H3 v3.1 -/

/-- **ContratoH3 W R N T** (v3.1) — o tipo que `qgPrice_H3_localHorizonEquilibrium_discharged` terá de habitar.

    O MESMO horizonte (o `H2`, com o MESMO κ, Δit, boost e n); G fixo; a matéria é o ÍNDICE T (não um campo);
    a classe admissível é fechada por translações; o elo matéria ↔ fluxo modular é campo; a resposta é uma
    perturbação de métrica dada por um PROPAGADOR fixo e covariante, no gauge do cone de luz; e a lei é LOCAL em todo gerador nulo de
    direção n: dθ/dλ = −8πG·T_nn. Bekenstein–Hawking, Clausius e o 8πG são TEOREMAS de janela. -/
structure ContratoH3 (W : TGLSpecificAQFTWitness) (R : TGLModularRealization W)
    (N : KillingNormalization) (T : StressTensorData W) where
  /-- o MESMO horizonte: o contrato H2 sobre o MESMO par (W, R) e a MESMA normalização N. -/
  H2 : ContratoH2 W R N
  /-- G [INPUT na rota de Jacobson: G = 1/(4ħη)]. -/
  G : ℝ
  G_pos : 0 < G
  /-- a classe admissível de estados (vetores unitários), fechada por translações. -/
  admissible : Set W.H
  admissible_unit : ∀ ψ ∈ admissible, ‖ψ‖ = 1
  vac_admissible : W.vac ∈ admissible
  admissible_translate : ∀ (a : Fin 4 → ℝ) (ψ : W.H), ψ ∈ admissible → W.U a ψ ∈ admissible
  /-- ★ O ELO MATÉRIA ↔ FLUXO MODULAR: a energia modular (bilateral) é 2π × a carga nula de T. -/
  modular_charge : ∀ ψ ∈ admissible, ∀ k : ℝ, HasModularEnergy H2.Δit ψ k →
    k = 2 * Real.pi * nullPlaneCharge T ψ
  /-- o balanço não é vazio: há estado admissível de energia modular ≠ 0. -/
  admissible_nontrivial : ∃ ψ ∈ admissible, ∃ k : ℝ, HasModularEnergy H2.Δit ψ k ∧ k ≠ 0
  /-- regularidade: T_nn é contínua ao longo de cada gerador nulo. -/
  energy_continuous : ∀ ψ ∈ admissible, ∀ x : Fin 4 → ℝ,
    Continuous (fun l : ℝ => nullEnergy T ψ (x + l • nullDir))
  /-- o fundo da linearização É o de H2: a tela do frame de H2 é plana (−1₂) na cunha. -/
  background_screen_flat : ∀ x ∈ rightWedge, screenBlockV31 (solderMetric4 (H2.E x)⁻¹) = -1
  /-- ★ O PROPAGADOR: a lei FIXA (antes de todo ψ) que leva o campo de tensão à perturbação de métrica. -/
  propagator : ((Fin 4 → ℝ) → Matrix (Fin 4) (Fin 4) ℝ) → (Fin 4 → ℝ) → Matrix (Fin 4) (Fin 4) ℝ
  /-- fonte nula, resposta nula. -/
  propagator_zero : propagator 0 = 0
  /-- ★ COVARIÂNCIA DO PROPAGADOR: fonte transladada, resposta transladada. -/
  propagator_covariant : ∀ (a : Fin 4 → ℝ) (f : (Fin 4 → ℝ) → Matrix (Fin 4) (Fin 4) ℝ),
    propagator (fun x => f (x - a)) = fun x => propagator f (x - a)
  /-- a resposta dos estados admissíveis é simétrica. -/
  response_symm : ∀ ψ ∈ admissible, ∀ x : Fin 4 → ℝ,
    (propagator (T.T ψ) x)ᵀ = propagator (T.T ψ) x
  /-- gauge do cone de luz ao longo do gerador: h·n = 0 (λ afim; a(h) é a área). -/
  lightcone_gauge : ∀ ψ ∈ admissible, ∀ x : Fin 4 → ℝ, (propagator (T.T ψ) x).mulVec nullDir = 0
  /-- a expansão θ_ψ(x) := d/dλ a(h_ψ)(x + λn)|₀. -/
  theta : W.H → (Fin 4 → ℝ) → ℝ
  theta_is_expansion : ∀ ψ ∈ admissible, ∀ x : Fin 4 → ℝ,
    HasDerivAt (fun l : ℝ => areaDensity (propagator (T.T ψ)) (x + l • nullDir)) (theta ψ x) 0
  /-- ★★ A LEI LOCAL (Raychaudhuri linear + Einstein nn), em TODO ponto: dθ/dλ = −8πG·T_nn. -/
  raychaudhuri_einstein : ∀ ψ ∈ admissible, ∀ x : Fin 4 → ℝ,
    HasDerivAt (fun l : ℝ => theta ψ (x + l • nullDir))
      (-(8 * Real.pi * G) * nullEnergy T ψ x) 0

namespace ContratoH3

variable {W : TGLSpecificAQFTWitness} {R : TGLModularRealization W} {N : KillingNormalization}
  {T : StressTensorData W}

/-- a resposta geométrica de ψ: h_ψ := 𝔉(T(ψ)) (definição; não é campo). -/
def response (C : ContratoH3 W R N T) (ψ : W.H) : (Fin 4 → ℝ) → Matrix (Fin 4) (Fin 4) ℝ :=
  C.propagator (T.T ψ)

end ContratoH3

/-! ## 6. CONTRATO IMPORT-H3 v3.1 — INDEXADO pelo termo H2 do MESMO par e da MESMA normalização -/

/-- **ContratoImportH3 W R N T h2** (v3.1): o índice `h2` é o termo H2 do MESMO (W, R, N); a função produz, de
    todo H2 no par, um H3 sobre o MESMO H2 e o MESMO tensor T. -/
structure ContratoImportH3 (W : TGLSpecificAQFTWitness) (R : TGLModularRealization W)
    (N : KillingNormalization) (T : StressTensorData W) (h2 : ContratoH2 W R N) where
  produce : ContratoH2 W R N → ContratoH3 W R N T
  same_horizon : ∀ h : ContratoH2 W R N, (produce h).H2 = h

#print axioms boostMat_add
#print axioms boostMat_zero
#print axioms wedgeBoostMap_add
#print axioms wedgeBoostMap_zero
#print axioms wedgeBoostMap_smul
#print axioms wedgeBoostMap_nullDir

end

end TGLExt.ContratoQGv31
