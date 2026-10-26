-- ---------------------------------------------------------------------
-- PEDRA DA GERENCIA (Claude, sessao d554e796) — 06/09/2026 — v329
-- O FLUXO MODULAR E UM HORIZONTE: o primeiro habitante NAO TRIVIAL de `TowerHorizon P`.
-- `Delta^{it}` (o `modularFlowUnitary` da v311) e unitario, normaliza o fator
-- (`modularConjugation_preserves_factor`) e preserva omega
-- (`modularConjugation_preserves_state`): logo e um `TowerHorizon`, e o levantamento
-- (`the_lift_on_the_tower`) da, para o habitante periodico da esperanca, a
-- COVARIANCIA MODULAR da esperanca: E(sigma_t A) = sigma_t(E A). Composicao de
-- teoremas do kernel; nenhum axioma novo. NAO move gate; nao e fisica.
-- ---------------------------------------------------------------------
import TGLExt.ModularPower
import TGLExt.TheOathOnTheTower
import TGLExt.PeriodicCentralizerExpectation

set_option autoImplicit false
set_option maxHeartbeats 400000
namespace TGLExt
open ChatgptAudit
noncomputable section
variable {P : SiteProfile}

/-- o unitario `Delta^{it}` como operador limitado. -/
def modularFlowCLM (P : SiteProfile) (t : ℝ) : TowerHilbert P →L[ℂ] TowerHilbert P :=
  ((modularFlowUnitary P t).toContinuousLinearEquiv : TowerHilbert P →L[ℂ] TowerHilbert P)

theorem modularFlowCLM_apply (t : ℝ) (x : TowerHilbert P) :
    modularFlowCLM P t x = modularFlow P t x := rfl

theorem modularFlowCLM_mul (s t : ℝ) :
    modularFlowCLM P s * modularFlowCLM P t = modularFlowCLM P (s + t) := by
  ext x
  change modularFlow P s (modularFlow P t x) = modularFlow P (s + t) x
  exact modularFlow_group s t x

theorem modularFlowCLM_zero : modularFlowCLM P 0 = 1 := by
  ext x
  exact modularFlow_zero_time x

/-- o adjunto de `Delta^{it}` e `Delta^{-it}` (isometria sobrejetiva). -/
theorem modularFlowCLM_star (t : ℝ) : star (modularFlowCLM P t) = modularFlowCLM P (-t) := by
  rw [ContinuousLinearMap.star_eq_adjoint]
  apply ContinuousLinearMap.ext
  intro y
  apply ext_inner_left ℂ
  intro x
  rw [ContinuousLinearMap.adjoint_inner_right]
  change inner ℂ (modularFlow P t x) y = inner ℂ x (modularFlow P (-t) y)
  have h := (modularFlowIsometry P t).inner_map_map x (modularFlow P (-t) y)
  change inner ℂ (modularFlow P t x) (modularFlow P t (modularFlow P (-t) y)) = inner ℂ x (modularFlow P (-t) y) at h
  rw [modularFlow_group, add_neg_cancel, modularFlow_zero_time] at h
  exact h

theorem modularConjugation_eq_sandwich (t : ℝ) (A : TowerHilbert P →L[ℂ] TowerHilbert P) :
    modularConjugation P t A = modularFlowCLM P t * A * star (modularFlowCLM P t) := by
  rw [modularFlowCLM_star]
  ext x
  rfl

/-- ★★★ [KERNEL] **o fluxo modular E um horizonte da torre** — unitario, normaliza M, preserva omega. -/
def modularHorizon (P : SiteProfile) (t : ℝ) : TowerHorizon P where
  U := modularFlowCLM P t
  unitary_left := by rw [modularFlowCLM_star, modularFlowCLM_mul, neg_add_cancel, modularFlowCLM_zero]
  unitary_right := by rw [modularFlowCLM_star, modularFlowCLM_mul, add_neg_cancel, modularFlowCLM_zero]
  normalizes := by
    intro A hA
    rw [← modularConjugation_eq_sandwich]
    exact (modularConjugation_preserves_factor P t A).mp hA
  normalizes_inv := by
    intro A hA
    have hst : modularFlowCLM P t = star (modularFlowCLM P (-t)) := by
      rw [modularFlowCLM_star, neg_neg]
    rw [modularFlowCLM_star, hst, ← modularConjugation_eq_sandwich]
    exact (modularConjugation_preserves_factor P (-t) A).mp hA
  preserves := by
    intro A _
    rw [← modularConjugation_eq_sandwich]
    exact modularConjugation_preserves_state t A

theorem adT_modularHorizon (t : ℝ) (A : TowerHilbert P →L[ℂ] TowerHilbert P) :
    adT (modularHorizon P t) A = modularConjugation P t A :=
  (modularConjugation_eq_sandwich t A).symm

/-- ★★★★ [KERNEL] **a esperanca de Takesaki construida COMUTA com o fluxo modular** (perfil periodico):
    `E (sigma_t A) = sigma_t (E A)` para todo A no fator — o levantamento do Lema 3 disparando num
    horizonte CONCRETO e nao trivial. -/
theorem periodic_expectation_commutes_with_modular_flow (T : ℝ) (hT : 0 < T)
    (hp : LocalPhasePeriod P T) (t : ℝ) :
    ∀ A ∈ theFactorObject P,
      modularConjugation P t ((periodicExpectationInput P T hT hp).E A)
        = (periodicExpectationInput P T hT hp).E (modularConjugation P t A) := by
  intro A hA
  have h := the_lift_on_the_tower (periodicExpectationInput P T hT hp) (modularHorizon P t) A hA
  rwa [adT_modularHorizon, adT_modularHorizon] at h

/-- ★★ [KERNEL] o mesmo para QUALQUER habitante do contrato (unicidade): a esperanca de Takesaki,
    seja qual for a sua construcao, comuta com o fluxo modular. -/
theorem every_expectation_commutes_with_modular_flow (I : ExpectationInput P) (t : ℝ) :
    ∀ A ∈ theFactorObject P,
      modularConjugation P t (I.E A) = I.E (modularConjugation P t A) := by
  intro A hA
  have h := the_lift_on_the_tower I (modularHorizon P t) A hA
  rwa [adT_modularHorizon, adT_modularHorizon] at h

#print axioms modularFlowCLM_star
#print axioms modularConjugation_eq_sandwich
#print axioms modularHorizon
#print axioms adT_modularHorizon
#print axioms periodic_expectation_commutes_with_modular_flow
#print axioms every_expectation_commutes_with_modular_flow
end
end TGLExt
