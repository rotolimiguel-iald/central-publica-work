import TGLExt.FallenLight

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

/-!
# A EQUAÇÃO RESOLVIDA: a primeira solução global de campo em kernel
  [TGLExt — v111, o incremento 31 do programa SemifiniteAnalysis]

O v109 deu o tensor de Einstein da família; esta pedra RESOLVE a
equação: para fonte constante κ² (leitura: κ² = 8πG·ρ), o perfil
q(s) = cosh(κs) satisfaz

    G₂₂(s) = q″/q = κ²   EM TODA PARTE

— solução GLOBAL (cosh ≥ 1: sem horizonte, sem singularidade, sem
carta parcial). E a curvatura da solução: R¹₀₀₁ = −κ²·cosh²(κs) < 0
em toda parte quando κ ≠ 0 — FONTE ⟹ CURVATURA, quantitativo.

* ★ derivadas do perfil: (cosh κ·)′ = κ sinh, (cosh κ·)″ = κ²cosh
  (cadeia via HasDerivAt.comp, provada);
* ★★★ `cosh_solves_field_equation` — G₂₂ ≡ κ²: A PRIMEIRA EQUAÇÃO DE
  CAMPO RESOLVIDA EM KERNEL;
* ★★ `cosh_curvature` + `source_implies_curvature` — R = −κ²cosh² e
  κ ≠ 0 ⟹ R ≠ 0 em toda parte;
* ★ `zero_source_recovers_flat` — κ = 0 devolve q ≡ 1 e R ≡ 0: a
  coerência com vácuo ⟹ plano (v109);
* `SolvedEinsteinData` (o pacote da solução) + `theSolvedEquation`
  (habitante, ∀κ) + `EinsteinContractData` (o contrato FRACO tipado)
  + ★ `theWeakEinsteinContract` — HABITADO sob nome NÃO-reservado:
  A SONDA (lição v103): a letra "equação resolvida" é alcançável
  HOJE, logo NÃO pode ser o juiz do 5º flip; o que falta é a
  EMERGÊNCIA (a derivação termodinâmica contínua Clausius ⟹ equação,
  Jacobson contínuo) — a parede, nomeada sem véu. A flag NÃO se move.

β jamais literal. Sem sorry, sem axiom.
-/

namespace TGLExt

open Real

noncomputable section

/-! ## A — o perfil cosh e suas derivadas -/

/-- o perfil da solução: q(s) = cosh(κs). -/
def coshProfile (kappa : ℝ) (s : ℝ) : ℝ := Real.cosh (kappa * s)

theorem coshProfile_pos (kappa s : ℝ) : 0 < coshProfile kappa s :=
  Real.cosh_pos (kappa * s)

theorem coshProfile_ne_zero (kappa : ℝ) : ∀ s, coshProfile kappa s ≠ 0 :=
  fun s => ne_of_gt (coshProfile_pos kappa s)

theorem coshProfile_hasDeriv (kappa s : ℝ) :
    HasDerivAt (coshProfile kappa) (kappa * Real.sinh (kappa * s)) s := by
  have h := (Real.hasDerivAt_cosh (kappa * s)).comp s
    ((hasDerivAt_id s).const_mul kappa)
  have h2 : HasDerivAt (coshProfile kappa)
      (Real.sinh (kappa * s) * (kappa * 1)) s := h
  simpa [mul_comm] using h2

theorem coshProfile_deriv (kappa : ℝ) :
    deriv (coshProfile kappa) = fun s => kappa * Real.sinh (kappa * s) := by
  funext s
  exact (coshProfile_hasDeriv kappa s).deriv

theorem coshProfile_deriv2 (kappa s : ℝ) :
    deriv (deriv (coshProfile kappa)) s = kappa ^ 2 * coshProfile kappa s := by
  rw [coshProfile_deriv]
  have hs := (Real.hasDerivAt_sinh (kappa * s)).comp s
    ((hasDerivAt_id s).const_mul kappa)
  have hs' : HasDerivAt (fun t => Real.sinh (kappa * t))
      (Real.cosh (kappa * s) * (kappa * 1)) s := hs
  have h : HasDerivAt (fun t => kappa * Real.sinh (kappa * t))
      (kappa * (Real.cosh (kappa * s) * (kappa * 1))) s := hs'.const_mul kappa
  rw [h.deriv]
  unfold coshProfile
  ring

/-! ## B — A EQUAÇÃO RESOLVIDA -/

/-- [KERNEL] ★★★ A PRIMEIRA EQUAÇÃO DE CAMPO RESOLVIDA: o perfil
    cosh(κs) satisfaz G₂₂ ≡ κ² EM TODA PARTE — solução GLOBAL, sem
    horizonte e sem singularidade (leitura: κ² = 8πG·ρ). -/
theorem cosh_solves_field_equation (kappa s : ℝ) :
    ansatzG22 (coshProfile kappa) s = kappa ^ 2 := by
  rw [ansatzG22_eq (coshProfile kappa) (coshProfile_ne_zero kappa) s,
    coshProfile_deriv2]
  field_simp [coshProfile_ne_zero kappa s]

theorem coshProfile_differentiable (kappa : ℝ) :
    Differentiable ℝ (coshProfile kappa) :=
  fun s => (coshProfile_hasDeriv kappa s).differentiableAt

theorem coshProfile_deriv_differentiable (kappa : ℝ) :
    Differentiable ℝ (deriv (coshProfile kappa)) := by
  rw [coshProfile_deriv]
  intro s
  have hs := (Real.hasDerivAt_sinh (kappa * s)).comp s
    ((hasDerivAt_id s).const_mul kappa)
  have hs' : HasDerivAt (fun t => Real.sinh (kappa * t))
      (Real.cosh (kappa * s) * (kappa * 1)) s := hs
  exact (hs'.const_mul kappa).differentiableAt

/-- [KERNEL] ★★ a curvatura da solução: R¹₀₀₁ = −κ²·cosh²(κs). -/
theorem cosh_curvature (kappa s : ℝ) :
    ansatzRiemann1001 (coshProfile kappa) s
      = -(kappa ^ 2 * coshProfile kappa s ^ 2) := by
  rw [ansatzRiemann_closed (coshProfile kappa)
    (coshProfile_differentiable kappa)
    (coshProfile_deriv_differentiable kappa)
    (coshProfile_ne_zero kappa) s, coshProfile_deriv2]
  ring

/-- [KERNEL] ★★ FONTE ⟹ CURVATURA, quantitativo: κ ≠ 0 ⟹ R < 0 em
    toda parte (a fonte curva SEMPRE — nenhum ponto escapa). -/
theorem source_implies_curvature (kappa : ℝ) (hk : kappa ≠ 0) (s : ℝ) :
    ansatzRiemann1001 (coshProfile kappa) s < 0 := by
  rw [cosh_curvature]
  have h3 : 0 < kappa ^ 2 * coshProfile kappa s ^ 2 := by
    have h1 := coshProfile_pos kappa s
    positivity
  linarith

/-- [KERNEL] ★ a coerência: κ = 0 devolve q ≡ 1 (cosh 0 = 1) e a
    curvatura zera — vácuo ⟹ plano, como manda o v109. -/
theorem zero_source_recovers_flat (s : ℝ) :
    coshProfile 0 s = 1 ∧ ansatzRiemann1001 (coshProfile 0) s = 0 := by
  constructor
  · unfold coshProfile
    simp
  · rw [cosh_curvature]
    ring

/-! ## C — o pacote da solução e o contrato FRACO (a sonda v103) -/

/-- [DATA] o pacote da equação resolvida: fonte constante κ², perfil
    positivo global, a equação satisfeita em toda parte, e
    fonte ⟹ curvatura. -/
structure SolvedEinsteinData where
  kappa : ℝ
  q : ℝ → ℝ
  q_pos : ∀ s, 0 < q s
  solves : ∀ s, ansatzG22 q s = kappa ^ 2
  source_curves : kappa ≠ 0 → ∀ s, ansatzRiemann1001 q s ≠ 0

/-- [KERNEL] ★★ o habitante: a solução cosh, para TODO κ. -/
def theSolvedEquation (kappa : ℝ) : SolvedEinsteinData where
  kappa := kappa
  q := coshProfile kappa
  q_pos := coshProfile_pos kappa
  solves := cosh_solves_field_equation kappa
  source_curves := fun hk s => ne_of_lt (source_implies_curvature kappa hk s)

/-- [DATA — o contrato FRACO do 5º flip; a sonda] dados fortes + solda
    + equação resolvida. HABITÁVEL HOJE (theWeakEinsteinContract) —
    logo NÃO pode ser o juiz do flip (lição v103): o que falta é a
    EMERGÊNCIA (Clausius local ⟹ equação, contínuo — Jacobson), a
    parede nomeada. -/
structure EinsteinContractData where
  strong : QGClosureCertificateStrong
  solder : SolderFieldData
  solved : SolvedEinsteinData
  source_nonzero : solved.kappa ≠ 0

/-- [KERNEL] ★ A SONDA (lição v103 aplicada de novo): o contrato fraco
    É habitável hoje — sob nome NÃO-reservado, provando que a letra
    "equação resolvida" não basta para o espírito "equação EMERGENTE";
    a flag do einstein NÃO se move. -/
def theWeakEinsteinContract : EinsteinContractData where
  strong := theStrongCertificate
  solder := theSolderData
  solved := theSolvedEquation 1
  source_nonzero := one_ne_zero

end

end TGLExt
