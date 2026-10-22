import PeriodicCentralizerExpectation
import CentralizerContractBridge
import ModularSignatureObstruction

set_option autoImplicit false
set_option maxHeartbeats 1200000
namespace ChatgptAudit
open TGLExt Matrix
noncomputable section
variable {P : SiteProfile}

theorem periodic_expectation_unique (T : ℝ) (hT : 0<T) (hp : LocalPhasePeriod P T)
    (F : ExpectationInput P) (x : TowerHilbert P →L[ℂ] TowerHilbert P)
    (hx : x ∈ theFactorObject P) : (periodicExpectationInput P T hT hp).E x=F.E x :=
  the_expectation_is_unique _ F x hx

theorem periodic_expectation_local (T : ℝ) (hT : 0<T) (hp : LocalPhasePeriod P T)
    (N : ℕ) (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    (periodicExpectationInput P T hT hp).E (towerPi P a)=towerPi P (specExpect (towerW P N) a) :=
  global_expectation_restricts_to_pinching _ N a

theorem boost4_is_canonical_generator (s : ℝ) :
    boost4 s = 1 + Real.sinh s • K1 + (Real.cosh s-1) • (K1*K1) := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [boost4,K1]

theorem boost4_is_canonical_block (s : ℝ) (i j : Fin 2) :
    boost4 s (Fin.castLE (by decide : 2≤4) i) (Fin.castLE (by decide : 2≤4) j)=
      TGLExt.boost s i j := by
  fin_cases i <;> fin_cases j <;> rfl

theorem tower_modular_cannot_intertwine_nonzero_boost (t s : ℝ)
    (F : (Fin 4 → ℝ) →ₗ[ℝ] TowerHilbert P) (hF : Function.Injective F)
    (hintertwine : ∀ v, modularFlow P t (F v)=F ((boost4 s).mulVec v)) : s=0 := by
  let U : TowerHilbert P →ₗᵢ[ℝ] TowerHilbert P := {
    toLinearMap := (modularFlowLinear P t).restrictScalars ℝ
    norm_map' := modularFlow_norm t }
  exact no_injective_isometric_boost_intertwiner U F hF hintertwine

#print axioms periodic_expectation_unique
#print axioms periodic_expectation_local
#print axioms boost4_is_canonical_generator
#print axioms boost4_is_canonical_block
#print axioms tower_modular_cannot_intertwine_nonzero_boost
end
end ChatgptAudit
