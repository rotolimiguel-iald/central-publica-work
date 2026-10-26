import TGLExt.NullMomentumInvariant

set_option autoImplicit false
set_option maxHeartbeats 800000

/-!
# Energia, momento longitudinal e setor de repouso nulo

As normalizações são as mesmas das coordenadas nulas não normalizadas:
`E=(P₊+P₋)/2`, `p=(P₊−P₋)/2`. A relação `E²−p²=P₊P₋` é derivada por
álgebra das definições. No repouso, `E=√(P₊P₋)` exige somente `P₊≥0`.
Não se afirma aqui a existência de um estado de repouso não nulo.
-/
namespace TGLExt.NullRestSector
open Matrix TGLExt.ContratoQGv31 TGLExt.ContratoQGv32 MeasureTheory
open TGLExt.NullEnergyScaling TGLExt.NullMomentumInvariant

/-- Positividade da componente nula sob positividade pontual da densidade. -/
theorem nullPlaneMomentum_nonneg {W : TGL.SpecificAQFT.TGLSpecificAQFTWitness}
    (T : StressTensorData W) (ψ : W.H)
    (h : ∀ p, 0 ≤ momentumIntegrand T ψ p) : 0 ≤ nullPlaneMomentum T ψ := by
  unfold nullPlaneMomentum
  exact integral_nonneg h

/-- Positividade da componente conjugada sob positividade pontual da densidade. -/
theorem oppositeNullPlaneMomentum_nonneg {W : TGL.SpecificAQFT.TGLSpecificAQFTWitness}
    (T : StressTensorData W) (ψ : W.H)
    (h : ∀ p, 0 ≤ oppositeMomentumIntegrand T ψ p) : 0 ≤ oppositeNullPlaneMomentum T ψ := by
  unfold oppositeNullPlaneMomentum
  exact integral_nonneg h

/-- O invariante é não negativo quando ambas as densidades nulas o são. -/
theorem nullMomentumProduct_nonneg {W : TGL.SpecificAQFT.TGLSpecificAQFTWitness}
    (T : StressTensorData W) (ψ : W.H)
    (hp : ∀ p, 0 ≤ momentumIntegrand T ψ p)
    (hm : ∀ p, 0 ≤ oppositeMomentumIntegrand T ψ p) :
    0 ≤ nullMomentumProduct T ψ :=
  mul_nonneg (nullPlaneMomentum_nonneg T ψ hp) (oppositeNullPlaneMomentum_nonneg T ψ hm)

/-- Leitura de energia nas coordenadas nulas não normalizadas. -/
noncomputable def energyReading {W : TGL.SpecificAQFT.TGLSpecificAQFTWitness}
    (T : StressTensorData W) (ψ : W.H) : ℝ :=
  (nullPlaneMomentum T ψ + oppositeNullPlaneMomentum T ψ) / 2

/-- Leitura do momento longitudinal nas mesmas coordenadas. -/
noncomputable def longitudinalMomentum {W : TGL.SpecificAQFT.TGLSpecificAQFTWitness}
    (T : StressTensorData W) (ψ : W.H) : ℝ :=
  (nullPlaneMomentum T ψ - oppositeNullPlaneMomentum T ψ) / 2

/-- A transformação da energia é derivada das duas escalas nulas. -/
theorem energyReading_boost {W : TGL.SpecificAQFT.TGLSpecificAQFTWitness}
    (B : WedgeBoostRep W) (T : StressTensorDataLocalV32 W B)
    (s : ℝ) (ψ : W.H)
    (hF : Integrable (momentumIntegrand T.toStressTensorData ψ))
    (hB : Integrable (momentumIntegrand T.toStressTensorData (B.V s ψ)))
    (hFo : Integrable (oppositeMomentumIntegrand T.toStressTensorData ψ))
    (hBo : Integrable (oppositeMomentumIntegrand T.toStressTensorData (B.V s ψ))) :
    energyReading T.toStressTensorData (B.V s ψ) =
      (Real.exp (-s) * nullPlaneMomentum T.toStressTensorData ψ +
        Real.exp s * oppositeNullPlaneMomentum T.toStressTensorData ψ) / 2 := by
  unfold energyReading
  rw [nullPlaneMomentum_boost_scaling B T s ψ hF hB,
    oppositeNullPlaneMomentum_boost_scaling B T s ψ hFo hBo]

/-- A transformação do momento longitudinal é derivada pelas mesmas duas leis. -/
theorem longitudinalMomentum_boost {W : TGL.SpecificAQFT.TGLSpecificAQFTWitness}
    (B : WedgeBoostRep W) (T : StressTensorDataLocalV32 W B)
    (s : ℝ) (ψ : W.H)
    (hF : Integrable (momentumIntegrand T.toStressTensorData ψ))
    (hB : Integrable (momentumIntegrand T.toStressTensorData (B.V s ψ)))
    (hFo : Integrable (oppositeMomentumIntegrand T.toStressTensorData ψ))
    (hBo : Integrable (oppositeMomentumIntegrand T.toStressTensorData (B.V s ψ))) :
    longitudinalMomentum T.toStressTensorData (B.V s ψ) =
      (Real.exp (-s) * nullPlaneMomentum T.toStressTensorData ψ -
        Real.exp s * oppositeNullPlaneMomentum T.toStressTensorData ψ) / 2 := by
  unfold longitudinalMomentum
  rw [nullPlaneMomentum_boost_scaling B T s ψ hF hB,
    oppositeNullPlaneMomentum_boost_scaling B T s ψ hFo hBo]

/-- Relação de dispersão derivada, sem casca de massa como premissa. -/
theorem energy_sq_sub_momentum_sq {W : TGL.SpecificAQFT.TGLSpecificAQFTWitness}
    (T : StressTensorData W) (ψ : W.H) :
    energyReading T ψ ^ 2 - longitudinalMomentum T ψ ^ 2 = nullMomentumProduct T ψ := by
  unfold energyReading longitudinalMomentum nullMomentumProduct
  ring

/-- Repouso significa igualdade das duas componentes nulas. -/
def IsNullRest {W : TGL.SpecificAQFT.TGLSpecificAQFTWitness}
    (T : StressTensorData W) (ψ : W.H) : Prop :=
  nullPlaneMomentum T ψ = oppositeNullPlaneMomentum T ψ

theorem isNullRest_momentum_zero {W : TGL.SpecificAQFT.TGLSpecificAQFTWitness}
    (T : StressTensorData W) (ψ : W.H) (hrest : IsNullRest T ψ) :
    longitudinalMomentum T ψ = 0 := by
  unfold longitudinalMomentum
  unfold IsNullRest at hrest
  rw [← hrest]
  ring

/-- No repouso, a energia é a raiz não negativa do invariante de momento. -/
theorem isNullRest_energy_eq_sqrt_product {W : TGL.SpecificAQFT.TGLSpecificAQFTWitness}
    (T : StressTensorData W) (ψ : W.H) (hrest : IsNullRest T ψ)
    (hp : 0 ≤ nullPlaneMomentum T ψ) :
    energyReading T ψ = Real.sqrt (nullMomentumProduct T ψ) := by
  have hm : 0 ≤ oppositeNullPlaneMomentum T ψ := by
    unfold IsNullRest at hrest
    rw [← hrest]
    exact hp
  have hE : 0 ≤ energyReading T ψ := by
    unfold energyReading
    linarith
  have hsq : energyReading T ψ ^ 2 = nullMomentumProduct T ψ := by
    unfold energyReading nullMomentumProduct
    unfold IsNullRest at hrest
    rw [← hrest]
    ring
  rw [← hsq, Real.sqrt_sq hE]

end TGLExt.NullRestSector

#print axioms TGLExt.NullRestSector.nullPlaneMomentum_nonneg
#print axioms TGLExt.NullRestSector.oppositeNullPlaneMomentum_nonneg
#print axioms TGLExt.NullRestSector.nullMomentumProduct_nonneg
#print axioms TGLExt.NullRestSector.energyReading_boost
#print axioms TGLExt.NullRestSector.longitudinalMomentum_boost
#print axioms TGLExt.NullRestSector.energy_sq_sub_momentum_sq
#print axioms TGLExt.NullRestSector.isNullRest_momentum_zero
#print axioms TGLExt.NullRestSector.isNullRest_energy_eq_sqrt_product
