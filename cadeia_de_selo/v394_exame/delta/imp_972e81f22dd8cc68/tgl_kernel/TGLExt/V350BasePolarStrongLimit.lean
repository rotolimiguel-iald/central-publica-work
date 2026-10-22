import TGLExt.V350LevelExpectationStrongLimit
import TGLExt.V350LocalBasePolarCommutation

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1500000

namespace TGLV350.Regular
open TGLExt ChatgptAudit Filter
open scoped Topology
noncomputable section

theorem antiunitaryConjugate_tendsto {H : Type} [NormedAddCommGroup H]
    [InnerProductSpace ℂ H] [CompleteSpace H] (U : H ≃ₛₗᵢ[starRingEnd ℂ] H)
    {ι : Type*} {l : Filter ι} (T : ι → H →L[ℂ] H) (A : H →L[ℂ] H)
    (hT : ∀ v, Tendsto (fun n => T n v) l (𝓝 (A v))) (v : H) :
    Tendsto (fun n => antiunitaryConjugate U (T n) v) l
      (𝓝 (antiunitaryConjugate U A v)) :=
  (U.continuous.tendsto (A (U.symm v))).comp (hT (U.symm v))

/-- Only one operator varies; strong convergence suffices to preserve its
commutation with a fixed bounded operator. -/
theorem commute_of_strong_tendsto {H : Type} [NormedAddCommGroup H]
    [InnerProductSpace ℂ H] [CompleteSpace H]
    {ι : Type*} {l : Filter ι} [NeBot l] (T : ι → H →L[ℂ] H) (A B : H →L[ℂ] H)
    (hT : ∀ v, Tendsto (fun n => T n v) l (𝓝 (A v)))
    (hc : ∀ n, Commute (T n) B) : Commute A B := by
  apply ContinuousLinearMap.ext
  intro v
  have hl := hT (B v)
  have hr := (B.continuous.tendsto (A v)).comp (hT v)
  have hr' : Tendsto (fun n => T n (B v)) l (𝓝 (B (A v))) :=
    hr.congr' (Eventually.of_forall (fun n =>
      (congrArg (fun F : H →L[ℂ] H => F v) (hc n).eq).symm))
  exact tendsto_nhds_unique hl hr'

/-- Every element of the entire base von Neumann algebra is covered in the
same GNS and with the actual J. This is not the whole crossed-product algebra. -/
theorem base_polar_commutes (P : SiteProfile)
    (A : (theFactorObject P).toStarSubalgebra) (B : (regularCoreAlgebra P).toStarSubalgebra) :
    Commute (antiunitaryConjugate (scalarTomitaPolarFactor P)
      (scalarGNSRepresentation P (regularCoreEmbedding P A))) (scalarGNSRepresentation P B) := by
  apply commute_of_strong_tendsto (l := (atTop : Filter ℕ))
    (fun N => antiunitaryConjugate (scalarTomitaPolarFactor P)
      (scalarGNSRepresentation P (levelCoreApproximation P N A)))
  · exact antiunitaryConjugate_tendsto (scalarTomitaPolarFactor P) _ _
      (represented_levelExpectation_strong_tendsto P A)
  · intro N
    exact localBase_polar_commutes P N (expectationMatrix P N A.val) B

#print axioms antiunitaryConjugate_tendsto
#print axioms commute_of_strong_tendsto
#print axioms base_polar_commutes
end
end TGLV350.Regular
