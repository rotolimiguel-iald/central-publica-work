import TGLExt.NullRestFrame

set_option autoImplicit false
set_option maxHeartbeats 800000

/-!
# Dinâmica nula no setor futuro

Um `FutureNullState` tem as duas componentes estritamente positivas e integrais
integráveis em toda a sua órbita. O boost preserva o tipo. Em todo habitante,
`invariantMass=√(P₊P₋)` é positiva, invariante e igual à energia no referencial
de repouso construído. Não se afirma que esse tipo seja habitado; a realização
física não nula permanece uma etapa separada.
-/
namespace TGLExt.FutureNullDynamics
open Matrix TGLExt.ContratoQGv31 TGLExt.ContratoQGv32 MeasureTheory
open TGLExt.NullEnergyScaling TGLExt.NullMomentumInvariant
open TGLExt.NullRestSector TGLExt.NullRestFrame

/-- Estado futuro com as duas órbitas de integrabilidade e componentes positivas. -/
structure FutureNullState {W : TGL.SpecificAQFT.TGLSpecificAQFTWitness}
    (B : WedgeBoostRep W) (T : StressTensorDataLocalV32 W B) where
  vec : W.H
  integrablePlus : ∀ s : ℝ, Integrable (momentumIntegrand T.toStressTensorData (B.V s vec))
  integrableMinus : ∀ s : ℝ, Integrable (oppositeMomentumIntegrand T.toStressTensorData (B.V s vec))
  plus_pos : 0 < nullPlaneMomentum T.toStressTensorData vec
  minus_pos : 0 < oppositeNullPlaneMomentum T.toStressTensorData vec

/-- A ação de boost preserva o setor futuro. -/
noncomputable def futureBoost {W : TGL.SpecificAQFT.TGLSpecificAQFTWitness}
    (B : WedgeBoostRep W) (T : StressTensorDataLocalV32 W B)
    (s : ℝ) (ψ : FutureNullState B T) : FutureNullState B T where
  vec := B.V s ψ.vec
  integrablePlus := by
    intro t
    simpa only [B.V_add, LinearIsometryEquiv.trans_apply] using ψ.integrablePlus (t + s)
  integrableMinus := by
    intro t
    simpa only [B.V_add, LinearIsometryEquiv.trans_apply] using ψ.integrableMinus (t + s)
  plus_pos := by
    have h0 : Integrable (momentumIntegrand T.toStressTensorData ψ.vec) := by
      simpa [B.V_zero] using ψ.integrablePlus 0
    rw [nullPlaneMomentum_boost_scaling B T s ψ.vec h0 (ψ.integrablePlus s)]
    exact mul_pos (Real.exp_pos _) ψ.plus_pos
  minus_pos := by
    have h0 : Integrable (oppositeMomentumIntegrand T.toStressTensorData ψ.vec) := by
      simpa [B.V_zero] using ψ.integrableMinus 0
    rw [oppositeNullPlaneMomentum_boost_scaling B T s ψ.vec h0 (ψ.integrableMinus s)]
    exact mul_pos (Real.exp_pos _) ψ.minus_pos

@[simp] theorem futureBoost_vec {W : TGL.SpecificAQFT.TGLSpecificAQFTWitness}
    (B : WedgeBoostRep W) (T : StressTensorDataLocalV32 W B)
    (s : ℝ) (ψ : FutureNullState B T) : (futureBoost B T s ψ).vec = B.V s ψ.vec := rfl

theorem futureBoost_zero {W : TGL.SpecificAQFT.TGLSpecificAQFTWitness}
    (B : WedgeBoostRep W) (T : StressTensorDataLocalV32 W B)
    (ψ : FutureNullState B T) : futureBoost B T 0 ψ = ψ := by
  cases ψ
  simp [futureBoost, B.V_zero]

theorem futureBoost_add {W : TGL.SpecificAQFT.TGLSpecificAQFTWitness}
    (B : WedgeBoostRep W) (T : StressTensorDataLocalV32 W B)
    (s t : ℝ) (ψ : FutureNullState B T) :
    futureBoost B T (s + t) ψ = futureBoost B T s (futureBoost B T t ψ) := by
  cases ψ
  simp [futureBoost, B.V_add, LinearIsometryEquiv.trans_apply]

/-- Massa como raiz do invariante, sem parâmetro `μ²`. -/
noncomputable def invariantMass {W : TGL.SpecificAQFT.TGLSpecificAQFTWitness}
    (T : StressTensorData W) (ψ : W.H) : ℝ :=
  Real.sqrt (nullMomentumProduct T ψ)

/-- Todo estado futuro tem massa invariante estritamente positiva. -/
theorem invariantMass_pos {W : TGL.SpecificAQFT.TGLSpecificAQFTWitness}
    (B : WedgeBoostRep W) (T : StressTensorDataLocalV32 W B)
    (ψ : FutureNullState B T) : 0 < invariantMass T.toStressTensorData ψ.vec := by
  unfold invariantMass nullMomentumProduct
  exact Real.sqrt_pos.mpr (mul_pos ψ.plus_pos ψ.minus_pos)

/-- A massa é constante em toda a órbita futura. -/
theorem invariantMass_boost {W : TGL.SpecificAQFT.TGLSpecificAQFTWitness}
    (B : WedgeBoostRep W) (T : StressTensorDataLocalV32 W B)
    (s : ℝ) (ψ : FutureNullState B T) :
    invariantMass T.toStressTensorData (futureBoost B T s ψ).vec =
      invariantMass T.toStressTensorData ψ.vec := by
  have h0 : Integrable (momentumIntegrand T.toStressTensorData ψ.vec) := by
    simpa [B.V_zero] using ψ.integrablePlus 0
  have h0o : Integrable (oppositeMomentumIntegrand T.toStressTensorData ψ.vec) := by
    simpa [B.V_zero] using ψ.integrableMinus 0
  unfold invariantMass
  change Real.sqrt (nullMomentumProduct T.toStressTensorData (B.V s ψ.vec)) =
    Real.sqrt (nullMomentumProduct T.toStressTensorData ψ.vec)
  rw [nullMomentumProduct_boost_invariant B T s ψ.vec h0 (ψ.integrablePlus s)
    h0o (ψ.integrableMinus s)]

/-- O referencial de repouso construído, ainda dentro do setor futuro. -/
noncomputable def futureRestFrame {W : TGL.SpecificAQFT.TGLSpecificAQFTWitness}
    (B : WedgeBoostRep W) (T : StressTensorDataLocalV32 W B)
    (ψ : FutureNullState B T) : FutureNullState B T :=
  futureBoost B T (restRapidity T.toStressTensorData ψ.vec) ψ

/-- O referencial construído realmente anula o momento longitudinal. -/
theorem futureRestFrame_momentum_zero {W : TGL.SpecificAQFT.TGLSpecificAQFTWitness}
    (B : WedgeBoostRep W) (T : StressTensorDataLocalV32 W B)
    (ψ : FutureNullState B T) :
    longitudinalMomentum T.toStressTensorData (futureRestFrame B T ψ).vec = 0 := by
  have h0 : Integrable (momentumIntegrand T.toStressTensorData ψ.vec) := by
    simpa [B.V_zero] using ψ.integrablePlus 0
  have h0o : Integrable (oppositeMomentumIntegrand T.toStressTensorData ψ.vec) := by
    simpa [B.V_zero] using ψ.integrableMinus 0
  let s := restRapidity T.toStressTensorData ψ.vec
  have hrest : IsNullRest T.toStressTensorData (B.V s ψ.vec) :=
    isNullRest_boost_restRapidity B T ψ.vec h0 h0o ψ.plus_pos ψ.minus_pos
      (ψ.integrablePlus s) (ψ.integrableMinus s)
  exact isNullRest_momentum_zero T.toStressTensorData (B.V s ψ.vec) hrest

/-- Lei universal da energia de repouso no setor futuro. -/
theorem futureRestFrame_energy {W : TGL.SpecificAQFT.TGLSpecificAQFTWitness}
    (B : WedgeBoostRep W) (T : StressTensorDataLocalV32 W B)
    (ψ : FutureNullState B T) :
    energyReading T.toStressTensorData (futureRestFrame B T ψ).vec =
      invariantMass T.toStressTensorData ψ.vec := by
  have h0 : Integrable (momentumIntegrand T.toStressTensorData ψ.vec) := by
    simpa [B.V_zero] using ψ.integrablePlus 0
  have h0o : Integrable (oppositeMomentumIntegrand T.toStressTensorData ψ.vec) := by
    simpa [B.V_zero] using ψ.integrableMinus 0
  let s := restRapidity T.toStressTensorData ψ.vec
  exact energyReading_boost_restRapidity B T ψ.vec h0 h0o ψ.plus_pos ψ.minus_pos
    (ψ.integrablePlus s) (ψ.integrableMinus s)

/-- A energia de repouso é estritamente positiva em todo estado futuro. -/
theorem futureRestFrame_energy_pos {W : TGL.SpecificAQFT.TGLSpecificAQFTWitness}
    (B : WedgeBoostRep W) (T : StressTensorDataLocalV32 W B)
    (ψ : FutureNullState B T) :
    0 < energyReading T.toStressTensorData (futureRestFrame B T ψ).vec := by
  rw [futureRestFrame_energy]
  exact invariantMass_pos B T ψ

end TGLExt.FutureNullDynamics

#print axioms TGLExt.FutureNullDynamics.futureBoost_zero
#print axioms TGLExt.FutureNullDynamics.futureBoost_add
#print axioms TGLExt.FutureNullDynamics.invariantMass_pos
#print axioms TGLExt.FutureNullDynamics.invariantMass_boost
#print axioms TGLExt.FutureNullDynamics.futureRestFrame_momentum_zero
#print axioms TGLExt.FutureNullDynamics.futureRestFrame_energy
#print axioms TGLExt.FutureNullDynamics.futureRestFrame_energy_pos
