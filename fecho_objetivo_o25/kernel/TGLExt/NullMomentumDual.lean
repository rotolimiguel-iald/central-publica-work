import TGLExt.NullEnergyScaling
import TGLExt.GlobalLiftLadder

set_option autoImplicit false
set_option maxHeartbeats 800000

/-!
# Ação dual objetiva sobre estados de momento nulo integrável

O domínio contém somente estados cuja órbita inteira sob o boost tem integrando
integrável. Isso é uma restrição de domínio, não uma dinâmica nem uma casca de
massa. A ação é a representação de boost já existente; `τ` é o momento nulo
 derivado em `NullEnergyScaling`, não a carga modular e não uma massa.
-/
namespace TGLExt.NullMomentumDual
open Matrix TGLExt.ContratoQGv31 TGLExt.ContratoQGv32 MeasureTheory
open TGLExt.NullEnergyScaling

/-- Estados cuja órbita inteira permanece no domínio do momento nulo. -/
structure BoostIntegrableState {W : TGL.SpecificAQFT.TGLSpecificAQFTWitness}
    (B : WedgeBoostRep W) (T : StressTensorDataLocalV32 W B) where
  vec : W.H
  integrable : ∀ s : ℝ, Integrable (momentumIntegrand T.toStressTensorData (B.V s vec))

/-- A ação de boost está fechada no domínio pela lei de grupo. -/
noncomputable def boostState {W : TGL.SpecificAQFT.TGLSpecificAQFTWitness}
    (B : WedgeBoostRep W) (T : StressTensorDataLocalV32 W B)
    (s : ℝ) (ψ : BoostIntegrableState B T) : BoostIntegrableState B T where
  vec := B.V s ψ.vec
  integrable := by
    intro t
    simpa only [B.V_add, LinearIsometryEquiv.trans_apply] using ψ.integrable (t + s)

@[simp] theorem boostState_vec {W : TGL.SpecificAQFT.TGLSpecificAQFTWitness}
    (B : WedgeBoostRep W) (T : StressTensorDataLocalV32 W B)
    (s : ℝ) (ψ : BoostIntegrableState B T) :
    (boostState B T s ψ).vec = B.V s ψ.vec := rfl

theorem boostState_zero {W : TGL.SpecificAQFT.TGLSpecificAQFTWitness}
    (B : WedgeBoostRep W) (T : StressTensorDataLocalV32 W B)
    (ψ : BoostIntegrableState B T) : boostState B T 0 ψ = ψ := by
  cases ψ
  simp [boostState, B.V_zero]

theorem boostState_add {W : TGL.SpecificAQFT.TGLSpecificAQFTWitness}
    (B : WedgeBoostRep W) (T : StressTensorDataLocalV32 W B)
    (s t : ℝ) (ψ : BoostIntegrableState B T) :
    boostState B T (s + t) ψ = boostState B T s (boostState B T t ψ) := by
  cases ψ
  simp [boostState, B.V_add, LinearIsometryEquiv.trans_apply]

/-- A realização física da escala dual, sem massa, casca ou Einstein como dados. -/
noncomputable def nullMomentumDual {W : TGL.SpecificAQFT.TGLSpecificAQFTWitness}
    (B : WedgeBoostRep W) (T : StressTensorDataLocalV32 W B) :
    TGLExt.DualScalingData (BoostIntegrableState B T) where
  tau ψ := nullPlaneMomentum T.toStressTensorData ψ.vec
  theta s ψ := boostState B T s ψ
  scaling s ψ := by
    have h0 : Integrable (momentumIntegrand T.toStressTensorData ψ.vec) := by
      simpa [B.V_zero] using ψ.integrable 0
    exact nullPlaneMomentum_boost_scaling B T s ψ.vec h0 (ψ.integrable s)

theorem nullMomentumDual_scaling {W : TGL.SpecificAQFT.TGLSpecificAQFTWitness}
    (B : WedgeBoostRep W) (T : StressTensorDataLocalV32 W B)
    (s : ℝ) (ψ : BoostIntegrableState B T) :
    (nullMomentumDual B T).tau ((nullMomentumDual B T).theta s ψ) =
      Real.exp (-s) * (nullMomentumDual B T).tau ψ :=
  (nullMomentumDual B T).scaling s ψ

theorem nullMomentumDual_theta_zero {W : TGL.SpecificAQFT.TGLSpecificAQFTWitness}
    (B : WedgeBoostRep W) (T : StressTensorDataLocalV32 W B)
    (ψ : BoostIntegrableState B T) : (nullMomentumDual B T).theta 0 ψ = ψ :=
  boostState_zero B T ψ

theorem nullMomentumDual_theta_add {W : TGL.SpecificAQFT.TGLSpecificAQFTWitness}
    (B : WedgeBoostRep W) (T : StressTensorDataLocalV32 W B)
    (s t : ℝ) (ψ : BoostIntegrableState B T) :
    (nullMomentumDual B T).theta (s + t) ψ =
      (nullMomentumDual B T).theta s ((nullMomentumDual B T).theta t ψ) :=
  boostState_add B T s t ψ

/-- O integrando do vácuo é identicamente nulo. -/
theorem momentumIntegrand_vac {W : TGL.SpecificAQFT.TGLSpecificAQFTWitness}
    (T : StressTensorData W) (p : ℝ × (Fin 2 → ℝ)) :
    momentumIntegrand T W.vac p = 0 := by
  unfold momentumIntegrand
  exact nullEnergy_vac T _

/-- O vácuo pertence ao domínio; portanto a realização não é vazia. -/
noncomputable def vacuumState {W : TGL.SpecificAQFT.TGLSpecificAQFTWitness}
    (B : WedgeBoostRep W) (T : StressTensorDataLocalV32 W B) : BoostIntegrableState B T where
  vec := W.vac
  integrable := by
    intro s
    rw [B.V_vac]
    have hzero : momentumIntegrand T.toStressTensorData W.vac = fun _ => (0 : ℝ) := by
      funext p
      exact momentumIntegrand_vac T.toStressTensorData p
    rw [hzero]
    exact integrable_zero _ _ _

instance {W : TGL.SpecificAQFT.TGLSpecificAQFTWitness}
    (B : WedgeBoostRep W) (T : StressTensorDataLocalV32 W B) :
    Nonempty (BoostIntegrableState B T) := ⟨vacuumState B T⟩

theorem nullMomentumDual_vacuum_tau {W : TGL.SpecificAQFT.TGLSpecificAQFTWitness}
    (B : WedgeBoostRep W) (T : StressTensorDataLocalV32 W B) :
    (nullMomentumDual B T).tau (vacuumState B T) = 0 := by
  change nullPlaneMomentum T.toStressTensorData W.vac = 0
  unfold nullPlaneMomentum
  have hzero : momentumIntegrand T.toStressTensorData W.vac = fun _ => (0 : ℝ) := by
    funext p
    exact momentumIntegrand_vac T.toStressTensorData p
  rw [hzero]
  simp

end TGLExt.NullMomentumDual

#print axioms TGLExt.NullMomentumDual.boostState_zero
#print axioms TGLExt.NullMomentumDual.boostState_add
#print axioms TGLExt.NullMomentumDual.nullMomentumDual_scaling
#print axioms TGLExt.NullMomentumDual.nullMomentumDual_theta_zero
#print axioms TGLExt.NullMomentumDual.nullMomentumDual_theta_add
#print axioms TGLExt.NullMomentumDual.momentumIntegrand_vac
#print axioms TGLExt.NullMomentumDual.nullMomentumDual_vacuum_tau
