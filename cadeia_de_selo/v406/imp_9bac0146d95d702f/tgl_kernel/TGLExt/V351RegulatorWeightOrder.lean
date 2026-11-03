import TGLExt.V351AllPositiveWeightOrder

set_option autoImplicit false
set_option maxHeartbeats 1400000

namespace TGLV350.Regular
open TGLExt
noncomputable section

private theorem hilbert_commuting_positive_product {H : Type}
    [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (A B : H →L[ℂ] H) (hA : 0 ≤ A) (hB : 0 ≤ B) (hc : Commute A B) :
    0 ≤ A*B := Commute.mul_nonneg hA hB hc

private theorem hilbertPositiveSqrt_mul_star {H : Type}
    [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (A : H →L[ℂ] H) (hA : 0 ≤ A) :
    hilbertPositiveSqrt A * star (hilbertPositiveSqrt A) = A := by
  change CFC.sqrt A * star (CFC.sqrt A) = A
  rw [(CFC.sqrt_nonneg A).isSelfAdjoint.star_eq,CFC.sqrt_mul_sqrt_self A hA]

theorem regularInverseGeneratorCutoff_commutes (P : SiteProfile)
    (ε η : ℝ) (hε : 0 < ε) (hη : 0 < η) :
    Commute (regularInverseGeneratorCutoff P ε) (regularInverseGeneratorCutoff P η) := by
  rw [regularInverseGeneratorCutoff_cfc P ε hε,regularInverseGeneratorCutoff_cfc P η hη]
  exact cfc_commute_cfc _ _ _

/-- The inverse identity is obtained on the graph of the same unbounded h. -/
theorem regularInverseGeneratorCutoff_resolvent_identity (P : SiteProfile)
    (ε η : ℝ) (hε : 0 < ε) (hη : 0 < η) :
    regularInverseGeneratorCutoff P ε - regularInverseGeneratorCutoff P η =
      ((η-ε : ℝ) : ℂ) • (regularInverseGeneratorCutoff P η * regularInverseGeneratorCutoff P ε) := by
  ext1 x
  have hh := (regularInverseGeneratorCutoff_graph_iff P η hη
    (regularInverseGeneratorCutoff P ε x)
    (x-(ε : ℂ) • regularInverseGeneratorCutoff P ε x)).mp
      (regularInverseGeneratorCutoff_graph P ε hε x)
  rw [map_add,map_sub,map_smul,map_smul] at hh
  change regularInverseGeneratorCutoff P ε x - regularInverseGeneratorCutoff P η x =
    ((η-ε : ℝ) : ℂ) • (regularInverseGeneratorCutoff P η (regularInverseGeneratorCutoff P ε x))
  rw [Complex.ofReal_sub,sub_smul]
  have he := congrArg (fun v => v-regularInverseGeneratorCutoff P η x) hh
  calc
    _ = (regularInverseGeneratorCutoff P η x -
        (ε : ℂ) • regularInverseGeneratorCutoff P η (regularInverseGeneratorCutoff P ε x) +
        (η : ℂ) • regularInverseGeneratorCutoff P η (regularInverseGeneratorCutoff P ε x)) -
          regularInverseGeneratorCutoff P η x := he.symm
    _ = _ := by abel

/-- Decreasing a positive regulator increases the actual inverse cutoff. -/
theorem regularInverseGeneratorCutoff_antitone (P : SiteProfile)
    (ε η : ℝ) (hε : 0 < ε) (hη : 0 < η) (hεη : ε ≤ η) :
    regularInverseGeneratorCutoff P η ≤ regularInverseGeneratorCutoff P ε := by
  apply sub_nonneg.mp
  rw [regularInverseGeneratorCutoff_resolvent_identity P ε η hε hη]
  have hp := hilbert_commuting_positive_product
    (regularInverseGeneratorCutoff P η) (regularInverseGeneratorCutoff P ε)
    (regularInverseGeneratorCutoff_nonneg P η hη) (regularInverseGeneratorCutoff_nonneg P ε hε)
    (regularInverseGeneratorCutoff_commutes P η ε hη hε)
  apply (ContinuousLinearMap.nonneg_iff_isPositive _).mpr
  apply ((ContinuousLinearMap.nonneg_iff_isPositive _).mp hp).smul_of_nonneg
  exact_mod_cast sub_nonneg.mpr hεη

/-- All-positive perturbed-weight order; no GNS-domain or commutation premise
remains for these original cutoffs. Values may be infinite. -/
theorem scalarWeight_inverseCutoff_antitone (P : SiteProfile)
    (ε η : ℝ) (hε : 0 < ε) (hη : 0 < η) (hεη : ε ≤ η)
    (X : PositiveCoreInput P) :
    dualQuadraticIntegral
      (star (hilbertPositiveSqrt (regularInverseGeneratorCutoff P η)) * X.val *
        hilbertPositiveSqrt (regularInverseGeneratorCutoff P η)) (regularVacuum P) ≤
    dualQuadraticIntegral
      (star (hilbertPositiveSqrt (regularInverseGeneratorCutoff P ε)) * X.val *
        hilbertPositiveSqrt (regularInverseGeneratorCutoff P ε)) (regularVacuum P) := by
  obtain ⟨hmε,hrε⟩ := regularInverseGeneratorCutoff_sqrt_right P ε hε
  obtain ⟨hmη,hrη⟩ := regularInverseGeneratorCutoff_sqrt_right P η hη
  let b : (regularCoreAlgebra P).toStarSubalgebra :=
    ⟨hilbertPositiveSqrt (regularInverseGeneratorCutoff P η),hmη⟩
  let c : (regularCoreAlgebra P).toStarSubalgebra :=
    ⟨hilbertPositiveSqrt (regularInverseGeneratorCutoff P ε),hmε⟩
  have ho : b*star b ≤ c*star c := by
    change hilbertPositiveSqrt (regularInverseGeneratorCutoff P η) *
        star (hilbertPositiveSqrt (regularInverseGeneratorCutoff P η)) ≤
      hilbertPositiveSqrt (regularInverseGeneratorCutoff P ε) *
        star (hilbertPositiveSqrt (regularInverseGeneratorCutoff P ε))
    rw [hilbertPositiveSqrt_mul_star _ (regularInverseGeneratorCutoff_nonneg P η hη),
      hilbertPositiveSqrt_mul_star _ (regularInverseGeneratorCutoff_nonneg P ε hε)]
    exact regularInverseGeneratorCutoff_antitone P ε η hε hη hεη
  exact scalarWeight_right_perturbed_mono_all_positive P b c hrη hrε ho
    (fun δ => regularInverseCutoffSqrt_commutes_average P η hη δ)
    (fun δ => regularInverseCutoffSqrt_commutes_average P ε hε δ) X

end
end TGLV350.Regular
