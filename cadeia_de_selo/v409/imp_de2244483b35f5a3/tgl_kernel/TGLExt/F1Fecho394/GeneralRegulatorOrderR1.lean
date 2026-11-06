import TGLExt.F1Fecho394.GeneralRegularCutoffCFCR1
/-! Resolvent identities and order for the same regular generator. Reuse of proofs incorporated in v393, with no trace monotonicity inferred from sandwich order. -/
set_option autoImplicit false
set_option maxHeartbeats 2400000
set_option synthInstance.maxHeartbeats 200000
noncomputable section
namespace F1Fecho.RegularPositiveFlow
open TGLV350.Regular TGLExt ChatgptAudit MeasureTheory Filter
open scoped Topology
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
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

theorem regularInverseGeneratorCutoff_commutes (B : F1Fecho.RegularCovariantCore.UnitaryFlow H)
    (ε η : ℝ) (hε : 0 < ε) (hη : 0 < η) :
    Commute (regularInverseGeneratorCutoff B ε) (regularInverseGeneratorCutoff B η) := by
  rw [regularInverseGeneratorCutoff_cfc B ε hε,regularInverseGeneratorCutoff_cfc B η hη]
  exact cfc_commute_cfc _ _ _

/-- The inverse identity is obtained on the graph of the same unbounded h. -/
theorem regularInverseGeneratorCutoff_resolvent_identity (B : F1Fecho.RegularCovariantCore.UnitaryFlow H)
    (ε η : ℝ) (hε : 0 < ε) (hη : 0 < η) :
    regularInverseGeneratorCutoff B ε - regularInverseGeneratorCutoff B η =
      ((η-ε : ℝ) : ℂ) • (regularInverseGeneratorCutoff B η * regularInverseGeneratorCutoff B ε) := by
  ext1 x
  have hh := (regularInverseGeneratorCutoff_graph_iff B η hη
    (regularInverseGeneratorCutoff B ε x)
    (x-(ε : ℂ) • regularInverseGeneratorCutoff B ε x)).mp
      (regularInverseGeneratorCutoff_graph B ε hε x)
  rw [map_add,map_sub,map_smul,map_smul] at hh
  change regularInverseGeneratorCutoff B ε x - regularInverseGeneratorCutoff B η x =
    ((η-ε : ℝ) : ℂ) • (regularInverseGeneratorCutoff B η (regularInverseGeneratorCutoff B ε x))
  rw [Complex.ofReal_sub,sub_smul]
  have he := congrArg (fun v => v-regularInverseGeneratorCutoff B η x) hh
  calc
    _ = (regularInverseGeneratorCutoff B η x -
        (ε : ℂ) • regularInverseGeneratorCutoff B η (regularInverseGeneratorCutoff B ε x) +
        (η : ℂ) • regularInverseGeneratorCutoff B η (regularInverseGeneratorCutoff B ε x)) -
          regularInverseGeneratorCutoff B η x := he.symm
    _ = _ := by abel

/-- Decreasing a positive regulator increases the actual inverse cutoff. -/
theorem regularInverseGeneratorCutoff_antitone (B : F1Fecho.RegularCovariantCore.UnitaryFlow H)
    (ε η : ℝ) (hε : 0 < ε) (hη : 0 < η) (hεη : ε ≤ η) :
    regularInverseGeneratorCutoff B η ≤ regularInverseGeneratorCutoff B ε := by
  apply sub_nonneg.mp
  rw [regularInverseGeneratorCutoff_resolvent_identity B ε η hε hη]
  have hp := hilbert_commuting_positive_product
    (regularInverseGeneratorCutoff B η) (regularInverseGeneratorCutoff B ε)
    (regularInverseGeneratorCutoff_nonneg B η hη) (regularInverseGeneratorCutoff_nonneg B ε hε)
    (regularInverseGeneratorCutoff_commutes B η ε hη hε)
  apply (ContinuousLinearMap.nonneg_iff_isPositive _).mpr
  apply ((ContinuousLinearMap.nonneg_iff_isPositive _).mp hp).smul_of_nonneg
  exact_mod_cast sub_nonneg.mpr hεη


end F1Fecho.RegularPositiveFlow
#print axioms F1Fecho.RegularPositiveFlow.regularInverseGeneratorCutoff_commutes
#print axioms F1Fecho.RegularPositiveFlow.regularInverseGeneratorCutoff_resolvent_identity
#print axioms F1Fecho.RegularPositiveFlow.regularInverseGeneratorCutoff_antitone
