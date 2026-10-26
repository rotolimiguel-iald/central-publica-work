import TGLExt.NullRestSector

set_option autoImplicit false
set_option maxHeartbeats 800000

/-!
# Construção do referencial de repouso nulo

Para componentes futuras estritamente positivas, a rapidez
`s*=log(P₊/P₋)/2` leva o estado ao setor `P₊=P₋`. A energia nesse referencial
é `√(P₊P₋)` calculada no estado original. Não se escolhe `μ²` nem se postula
uma casca; as integrabilidades no ponto e no estado boosted permanecem explícitas.
-/
namespace TGLExt.NullRestFrame
open Matrix TGLExt.ContratoQGv31 TGLExt.ContratoQGv32 MeasureTheory
open TGLExt.NullEnergyScaling TGLExt.NullMomentumInvariant TGLExt.NullRestSector

/-- A rapidez que simetriza as duas componentes nulas positivas. -/
noncomputable def restRapidity {W : TGL.SpecificAQFT.TGLSpecificAQFTWitness}
    (T : StressTensorData W) (ψ : W.H) : ℝ :=
  Real.log (nullPlaneMomentum T ψ / oppositeNullPlaneMomentum T ψ) / 2

/-- A rapidez construída leva qualquer par futuro positivo ao repouso nulo. -/
theorem isNullRest_boost_restRapidity {W : TGL.SpecificAQFT.TGLSpecificAQFTWitness}
    (B : WedgeBoostRep W) (T : StressTensorDataLocalV32 W B)
    (ψ : W.H)
    (hF : Integrable (momentumIntegrand T.toStressTensorData ψ))
    (hFo : Integrable (oppositeMomentumIntegrand T.toStressTensorData ψ))
    (hp : 0 < nullPlaneMomentum T.toStressTensorData ψ)
    (hm : 0 < oppositeNullPlaneMomentum T.toStressTensorData ψ)
    (hB : Integrable (momentumIntegrand T.toStressTensorData
      (B.V (restRapidity T.toStressTensorData ψ) ψ)))
    (hBo : Integrable (oppositeMomentumIntegrand T.toStressTensorData
      (B.V (restRapidity T.toStressTensorData ψ) ψ))) :
    IsNullRest T.toStressTensorData (B.V (restRapidity T.toStressTensorData ψ) ψ) := by
  let s := restRapidity T.toStressTensorData ψ
  let a := nullPlaneMomentum T.toStressTensorData ψ
  let b := oppositeNullPlaneMomentum T.toStressTensorData ψ
  have hs : 2 * s = Real.log (a / b) := by
    dsimp [s, restRapidity, a, b]
    ring
  have habpos : 0 < a / b := div_pos hp hm
  have hexp : Real.exp (2 * s) = a / b := by
    rw [hs, Real.exp_log habpos]
  have ha : a = Real.exp (2 * s) * b :=
    (div_eq_iff (ne_of_gt hm)).mp hexp.symm
  have hscale : Real.exp (-s) * a = Real.exp s * b := by
    calc
      Real.exp (-s) * a = Real.exp (-s) * (Real.exp (2 * s) * b) := by rw [← ha]
      _ = (Real.exp (-s) * Real.exp (2 * s)) * b := by ring
      _ = Real.exp s * b := by
        rw [← Real.exp_add]
        congr 2
        ring
  unfold IsNullRest
  rw [nullPlaneMomentum_boost_scaling B T s ψ hF hB,
    oppositeNullPlaneMomentum_boost_scaling B T s ψ hFo hBo]
  exact hscale

/-- A componente nula permanece positiva no referencial construído. -/
theorem restRapidity_nullPlaneMomentum_pos {W : TGL.SpecificAQFT.TGLSpecificAQFTWitness}
    (B : WedgeBoostRep W) (T : StressTensorDataLocalV32 W B)
    (ψ : W.H)
    (hF : Integrable (momentumIntegrand T.toStressTensorData ψ))
    (hp : 0 < nullPlaneMomentum T.toStressTensorData ψ)
    (hB : Integrable (momentumIntegrand T.toStressTensorData
      (B.V (restRapidity T.toStressTensorData ψ) ψ))) :
    0 < nullPlaneMomentum T.toStressTensorData (B.V (restRapidity T.toStressTensorData ψ) ψ) := by
  rw [nullPlaneMomentum_boost_scaling B T _ ψ hF hB]
  exact mul_pos (Real.exp_pos _) hp

/-- Energia de repouso derivada diretamente do invariante do estado original. -/
theorem energyReading_boost_restRapidity {W : TGL.SpecificAQFT.TGLSpecificAQFTWitness}
    (B : WedgeBoostRep W) (T : StressTensorDataLocalV32 W B)
    (ψ : W.H)
    (hF : Integrable (momentumIntegrand T.toStressTensorData ψ))
    (hFo : Integrable (oppositeMomentumIntegrand T.toStressTensorData ψ))
    (hp : 0 < nullPlaneMomentum T.toStressTensorData ψ)
    (hm : 0 < oppositeNullPlaneMomentum T.toStressTensorData ψ)
    (hB : Integrable (momentumIntegrand T.toStressTensorData
      (B.V (restRapidity T.toStressTensorData ψ) ψ)))
    (hBo : Integrable (oppositeMomentumIntegrand T.toStressTensorData
      (B.V (restRapidity T.toStressTensorData ψ) ψ))) :
    energyReading T.toStressTensorData (B.V (restRapidity T.toStressTensorData ψ) ψ) =
      Real.sqrt (nullMomentumProduct T.toStressTensorData ψ) := by
  let s := restRapidity T.toStressTensorData ψ
  have hrest : IsNullRest T.toStressTensorData (B.V s ψ) :=
    isNullRest_boost_restRapidity B T ψ hF hFo hp hm hB hBo
  have hpos : 0 < nullPlaneMomentum T.toStressTensorData (B.V s ψ) :=
    restRapidity_nullPlaneMomentum_pos B T ψ hF hp hB
  have he := isNullRest_energy_eq_sqrt_product T.toStressTensorData (B.V s ψ) hrest hpos.le
  rw [nullMomentumProduct_boost_invariant B T s ψ hF hB hFo hBo] at he
  exact he

end TGLExt.NullRestFrame

#print axioms TGLExt.NullRestFrame.isNullRest_boost_restRapidity
#print axioms TGLExt.NullRestFrame.restRapidity_nullPlaneMomentum_pos
#print axioms TGLExt.NullRestFrame.energyReading_boost_restRapidity
