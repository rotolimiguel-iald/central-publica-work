import TGLExt.V351InverseLimitSemifiniteness
import TGLExt.V351InverseLimitTracialExtension

set_option autoImplicit false
set_option maxHeartbeats 1400000

namespace TGLV350.Regular
open TGLExt TGLV351 MeasureTheory Filter
open scoped Topology ENNReal NNReal
noncomputable section

/-- Actual finite-square contractions in the same core, converging strongly
to I. This does not assume traciality or create another approximate unit. -/
theorem scalarInverseLimitWeight_finite_contractions (P : SiteProfile) :
    ∃ E : ℕ → (regularCoreAlgebra P).toStarSubalgebra,
      (∀ n, ‖(E n).val‖ ≤ 1) ∧
      (∀ n, scalarInverseLimitWeight P (positiveSquare P (E n)) < ⊤) ∧
      (∀ v, Tendsto (fun n => (E n).val v) atTop (𝓝 v)) := by
  let d : ℕ → ℝ := fun n => 1/((n : ℝ)+1)
  have hd (n : ℕ) : 0 < d n := by dsimp [d]; positivity
  let e (n : ℕ) : (regularCoreAlgebra P).toStarSubalgebra :=
    ⟨regularAverage P (d n),regularAverage_mem P (d n)⟩
  let E (n : ℕ) := e n * regularDomainCut P (d n)
  have hqn (n : ℕ) : ‖(regularDomainCut P (d n)).val‖ ≤ 1 := by
    obtain ⟨h0,h1⟩ := regularDomainCut_bounds P (d n) (hd n)
    exact (CStarAlgebra.norm_le_norm_of_nonneg_of_le h0 h1).trans ContinuousLinearMap.norm_id_le
  refine ⟨E,?_,?_,?_⟩
  · intro n
    exact (norm_mul_le _ _).trans (by
      simpa only [one_mul] using mul_le_mul (regularAverage_norm_le_one P (d n))
        (hqn n) (norm_nonneg _) zero_le_one)
  · intro n
    let a : scalarWeightLeftIdeal P := ⟨e n,HasFiniteDualSquare.scalar_finite P _
      (regularAverage_hasFiniteDualSquare P (d n) (hd n))⟩
    exact scalarInverseLimitWeight_domainCut_finite P (d n) (hd n) a
  · intro v
    have ht : Tendsto d atTop (𝓝[≠] (0 : ℝ)) := by
      refine tendsto_nhdsWithin_iff.mpr ⟨tendsto_one_div_add_atTop_nhds_zero_nat,?_⟩
      exact Eventually.of_forall fun n => by
        simp only [Set.mem_compl_iff,Set.mem_singleton_iff]
        exact ne_of_gt (hd n)
    exact bounded_application_tendsto atTop (fun n => (e n).val) 1
      (fun n => regularAverage_norm_le_one P (d n))
      (fun n => (regularDomainCut P (d n)).val v) v v
      (regularDomainCut_tendsto_identity P v)
      ((regularAverage_tendsto_identity P v).comp ht)

private theorem hilbert_square_norm_bound {H : Type}
    [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (a : H →L[ℂ] H) : star a*a ≤ (‖a‖^2 : ℝ) • (1 : H →L[ℂ] H) := by
  simpa only [Algebra.algebraMap_eq_smul_one] using
    (CStarAlgebra.star_mul_le_algebraMap_norm_sq (a := a))

/-- The exact finite-positive-minorants field of the trace contract follows
from the STILL EXPLICIT traciality premise and the already constructed finite
contractions. It is not asserted for the original nontracial dual weight. -/
theorem scalarInverseLimitWeight_finite_minorants (P : SiteProfile)
    (htr : ∀ a : (regularCoreAlgebra P).toStarSubalgebra,
      scalarInverseLimitWeight P (positiveSquare P a) =
        scalarInverseLimitWeight P (positiveSquare P (star a)))
    (X : PositiveCoreInput P) :
    scalarInverseLimitWeight P X =
      ⨆ (Y : PositiveCoreInput P) (_ : Y ≤ X)
        (_ : scalarInverseLimitWeight P Y < ⊤), scalarInverseLimitWeight P Y := by
  letI : IsClosed ((regularCoreAlgebra P).toStarSubalgebra :
      Set (RegularHilbert (TowerHilbert P) →L[ℂ] RegularHilbert (TowerHilbert P))) :=
    vonNeumann_norm_closed (regularCoreAlgebra P)
  have hm : CFC.sqrt X.val ∈ regularCoreAlgebra P := by
    rw [CFC.sqrt_eq_real_sqrt X.val X.property.2]
    exact cfcₙ_mem (𝕜' := ℂ) (s := (regularCoreAlgebra P).toStarSubalgebra)
      Real.sqrt X.property.1
  let a : (regularCoreAlgebra P).toStarSubalgebra := ⟨CFC.sqrt X.val,hm⟩
  have hX : positiveSquare P a = X := by
    apply Subtype.ext
    change star (CFC.sqrt X.val)*CFC.sqrt X.val = X.val
    rw [(CFC.sqrt_nonneg X.val).isSelfAdjoint.star_eq,CFC.sqrt_mul_sqrt_self X.val X.property.2]
  obtain ⟨E,hn,hf,ht⟩ := scalarInverseLimitWeight_finite_contractions P
  let Y (n : ℕ) := positiveSquare P (E n*a)
  have hy (n : ℕ) : Y n ≤ X := by
    have hs := hilbert_square_norm_bound (E n).val
    have hc : (‖(E n).val‖^2 : ℝ) ≤ 1 := by
      nlinarith only [hn n,norm_nonneg (E n).val]
    have hc' : (‖(E n).val‖^2 : ℝ) • (1 : RegularHilbert (TowerHilbert P) →L[ℂ] _) ≤ 1 := by
      simpa only [one_smul] using smul_le_smul_of_nonneg_right hc
        (show (0 : RegularHilbert (TowerHilbert P) →L[ℂ] _) ≤ 1 from zero_le_one)
    have hp := star_left_conjugate_le_conjugate (hs.trans hc') a.val
    rw [← hX]
    simpa only [Y,positiveSquare,MulMemClass.coe_mul,star_mul,mul_assoc,one_mul] using hp
  have hfin (n : ℕ) : scalarInverseLimitWeight P (Y n) < ⊤ := by
    let r : ℝ≥0 := ⟨‖a.val‖^2,sq_nonneg _⟩
    have hs := hilbert_square_norm_bound (star a.val)
    simp only [star_star,_root_.norm_star] at hs
    have ho := star_left_conjugate_le_conjugate hs (star (E n).val)
    have hp : positiveSquare P (star (E n*a)) ≤ (positiveSquare P (star (E n))).scale r := by
      simpa only [positiveSquare,PositiveCoreInput.scale,MulMemClass.coe_mul,
        StarMemClass.coe_star,star_mul,star_star,mul_assoc,mul_smul_comm,smul_mul_assoc,
        one_mul,r] using ho
    have hle := scalarInverseLimitWeight_mono P _ _ hp
    rw [scalarInverseLimitWeight_scale,← htr (E n)] at hle
    have hfinite := hle.trans_lt (ENNReal.mul_lt_top ENNReal.coe_lt_top (hf n))
    exact (htr (E n*a)).trans_lt hfinite
  apply le_antisymm
  · rw [← hX]
    apply scalarInverseLimitWeight_square_le_of_strong P (fun n => E n*a) a
      (fun v => ht (a.val v))
    intro n
    exact le_iSup_of_le (Y n) (le_iSup_of_le (hy n) (le_iSup_of_le (hfin n) le_rfl))
  · apply iSup_le
    intro Z
    apply iSup_le
    intro hZX
    apply iSup_le
    intro _
    exact scalarInverseLimitWeight_mono P Z X hZX

end
end TGLV350.Regular
