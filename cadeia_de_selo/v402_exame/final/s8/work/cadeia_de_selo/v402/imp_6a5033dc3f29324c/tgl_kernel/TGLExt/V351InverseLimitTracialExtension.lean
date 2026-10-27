import TGLExt.V351InverseLimitWeight
import TGLExt.V351RegularCoreTraceContract
import TGLExt.V350DualCutNormality

set_option autoImplicit false
set_option maxHeartbeats 1400000

namespace TGLV350.Regular
open TGLExt TGLV351 MeasureTheory Filter
open scoped Topology ENNReal
noncomputable section

private theorem dualSquare_le_of_strong {H : Type}
    [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (A : ℕ → RegularHilbert H →L[ℂ] RegularHilbert H)
    (S : RegularHilbert H →L[ℂ] RegularHilbert H) (v : RegularHilbert H)
    (hlim : ∀ w, Tendsto (fun n => A n w) atTop (𝓝 (S w)))
    (C : ℝ≥0∞) (hb : ∀ n, dualQuadraticIntegral (star (A n)*A n) v ≤ C) :
    dualQuadraticIntegral (star S*S) v ≤ C := by
  let f : ℕ → ℝ → ℝ≥0∞ := fun n s => ENNReal.ofReal dualHaarFactor *
    dualQuadraticIntegrand (star (A n)*A n) v s
  let g : ℝ → ℝ≥0∞ := fun s => ENNReal.ofReal dualHaarFactor *
    dualQuadraticIntegrand (star S*S) v s
  have hm (n : ℕ) : Measurable (f n) :=
    measurable_const.mul (dualQuadraticIntegrand_measurable _ _)
  have hl (s : ℝ) : Tendsto (fun n => f n s) atTop (𝓝 (g s)) := by
    have ht := (dualAmbient_tendsto_strong A S hlim s v).norm.pow 2
    have he := ENNReal.continuous_ofReal.continuousAt.tendsto.comp ht
    have hh := (ENNReal.continuous_const_mul (a := ENNReal.ofReal dualHaarFactor)
      ENNReal.ofReal_ne_top).continuousAt.tendsto.comp he
    simpa only [f,g,Function.comp_def,dualQuadraticIntegrand_star_mul] using hh
  have hi (n : ℕ) : (∫⁻ s, f n s) = dualQuadraticIntegral (star (A n)*A n) v :=
    lintegral_const_mul _ (dualQuadraticIntegrand_measurable _ _)
  have hg : (∫⁻ s, g s) = dualQuadraticIntegral (star S*S) v :=
    lintegral_const_mul _ (dualQuadraticIntegrand_measurable _ _)
  calc
    _ = ∫⁻ s, g s := hg.symm
    _ = ∫⁻ s, liminf (fun n => f n s) atTop :=
      lintegral_congr_ae (Eventually.of_forall fun s => (hl s).liminf_eq.symm)
    _ ≤ liminf (fun n => ∫⁻ s, f n s) atTop := lintegral_liminf_le hm
    _ ≤ C := liminf_le_of_frequently_le'
      (Eventually.of_forall (fun n => by rw [hi]; exact hb n)).frequently

/-- Strong limits preserve upper bounds on quadratic values of the SAME
candidate weight. No convergence of adjoints or finite bound is required. -/
theorem scalarInverseLimitWeight_square_le_of_strong (P : SiteProfile)
    (A : ℕ → (regularCoreAlgebra P).toStarSubalgebra)
    (S : (regularCoreAlgebra P).toStarSubalgebra)
    (hlim : ∀ v, Tendsto (fun n => (A n).val v) atTop (𝓝 (S.val v)))
    (C : ℝ≥0∞) (hb : ∀ n, scalarInverseLimitWeight P (positiveSquare P (A n)) ≤ C) :
    scalarInverseLimitWeight P (positiveSquare P S) ≤ C := by
  apply iSup_le
  intro k
  let b := hilbertPositiveSqrt (regularInverseGeneratorCutoff P (1/((k : ℝ)+1)))
  have h := dualSquare_le_of_strong (fun n => (A n).val*b) (S.val*b)
    (regularVacuum P) (fun v => hlim (b v)) C (fun n => ?_)
  · simpa only [scalarInverseCutoffWeight,positiveSquare,star_mul,mul_assoc,b] using h
  · have hh := (scalarInverseCutoffWeight_le_limit P k (positiveSquare P (A n))).trans (hb n)
    simpa only [scalarInverseCutoffWeight,positiveSquare,star_mul,mul_assoc,b] using hh

/-- Right averaging decreases the candidate weight on squares, by the old
dual-weight bound and the proved commutation of its cutoff roots. -/
theorem scalarInverseLimitWeight_right_average_le (P : SiteProfile)
    (A : (regularCoreAlgebra P).toStarSubalgebra) (δ : ℝ) :
    scalarInverseLimitWeight P (positiveSquare P
      (A * ⟨regularAverage P δ,regularAverage_mem P δ⟩)) ≤
      scalarInverseLimitWeight P (positiveSquare P A) := by
  apply iSup_le
  intro k
  apply le_iSup_of_le k
  let ε : ℝ := 1/((k : ℝ)+1)
  have hε : 0 < ε := by dsimp [ε]; positivity
  let b := hilbertPositiveSqrt (regularInverseGeneratorCutoff P ε)
  obtain ⟨hm,_⟩ := regularInverseGeneratorCutoff_sqrt_right P ε hε
  have hc := regularInverseCutoffSqrt_commutes_average P ε hε δ
  have he : (A.val*regularAverage P δ)*b = (A.val*b)*regularAverage P δ := by
    rw [mul_assoc,← hc.eq,← mul_assoc]
  have h := scalarWeight_right_average_le P (A*⟨b,hm⟩) δ
  change dualQuadraticIntegral (star b * (star (A.val*regularAverage P δ) *
      (A.val*regularAverage P δ)) * b) (regularVacuum P) ≤
    dualQuadraticIntegral (star b * (star A.val*A.val) * b) (regularVacuum P)
  have hs : star b * (star (A.val*regularAverage P δ) *
      (A.val*regularAverage P δ)) * b =
      star ((A.val*b)*regularAverage P δ) * ((A.val*b)*regularAverage P δ) := by
    rw [← he]
    simp only [star_mul,mul_assoc]
  rw [hs]
  simpa only [MulMemClass.coe_mul,star_mul,mul_assoc] using h

private theorem hilbert_contraction_left_square {H : Type}
    [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (c a : H →L[ℂ] H) (hc : ‖c‖ ≤ 1) :
    star (c*a)*(c*a) ≤ star a*a := by
  have hn : ‖star c*c‖ ≤ 1 := by
    calc
      _ ≤ ‖star c‖*‖c‖ := norm_mul_le _ _
      _ = ‖c‖*‖c‖ := by rw [_root_.norm_star]
      _ ≤ 1*1 := mul_le_mul hc hc (norm_nonneg _) zero_le_one
      _ = 1 := one_mul 1
  have hs := (CStarAlgebra.norm_le_one_iff_of_nonneg (star c*c)
    (star_mul_self_nonneg c)).mp hn
  have h := star_left_conjugate_le_conjugate hs a
  simpa only [star_mul,mul_assoc,one_mul] using h

/-- The old two-sided regularization decreases both quadratic values.
This is a weight inequality; no sandwich order in the conjugator is claimed. -/
theorem scalarInverseLimitWeight_sandwich_le (P : SiteProfile)
    (A : (regularCoreAlgebra P).toStarSubalgebra) (δ : ℝ) :
    scalarInverseLimitWeight P (positiveSquare P (regularSandwich P A δ)) ≤
      scalarInverseLimitWeight P (positiveSquare P A) := by
  let e : (regularCoreAlgebra P).toStarSubalgebra :=
    ⟨regularAverage P δ,regularAverage_mem P δ⟩
  have he : ‖star e.val‖ ≤ 1 := by
    simpa only [_root_.norm_star] using regularAverage_norm_le_one P δ
  have ho := hilbert_contraction_left_square (star e.val) (A.val*e.val) he
  have hp : positiveSquare P (regularSandwich P A δ) ≤ positiveSquare P (A*e) := by
    change star (star e.val*A.val*e.val)*(star e.val*A.val*e.val) ≤
      star (A.val*e.val)*(A.val*e.val)
    simpa only [mul_assoc] using ho
  exact (scalarInverseLimitWeight_mono P _ _ hp).trans
    (scalarInverseLimitWeight_right_average_le P A δ)

/-- Exact remaining obligation: traciality on the existing algebraic star
core is equivalent to traciality on all of N. This does not prove that premise. -/
theorem scalarInverseLimitWeight_tracial_iff_core (P : SiteProfile) :
    (∀ A : (regularCoreAlgebra P).toStarSubalgebra,
      scalarInverseLimitWeight P (positiveSquare P A) =
        scalarInverseLimitWeight P (positiveSquare P (star A))) ↔
    (∀ A : (regularCoreAlgebra P).toStarSubalgebra, A ∈ finiteDualStarCore P →
      scalarInverseLimitWeight P (positiveSquare P A) =
        scalarInverseLimitWeight P (positiveSquare P (star A))) := by
  constructor
  · exact fun h A _ => h A
  · intro hcore
    have hle (A : (regularCoreAlgebra P).toStarSubalgebra) :
        scalarInverseLimitWeight P (positiveSquare P A) ≤
          scalarInverseLimitWeight P (positiveSquare P (star A)) := by
      let d : ℕ → ℝ := fun n => 1/((n : ℝ)+1)
      have hd : Tendsto d atTop (𝓝[>] (0 : ℝ)) := by
        refine tendsto_nhdsWithin_iff.mpr ⟨tendsto_one_div_add_atTop_nhds_zero_nat,?_⟩
        exact Eventually.of_forall fun n => by
          change (0 : ℝ) < 1/((n : ℝ)+1)
          positivity
      apply scalarInverseLimitWeight_square_le_of_strong P
        (fun n => regularSandwich P A (d n)) A
        (fun v => (regularSandwich_tendsto P A v).comp hd)
      intro n
      rw [hcore _ (regularSandwich_mem_finiteDualStarCore P A (d n)
        (by dsimp [d]; positivity)),regularSandwich_star]
      exact scalarInverseLimitWeight_sandwich_le P (star A) (d n)
    intro A
    exact le_antisymm (hle A) (by simpa only [star_star] using hle (star A))

end
end TGLV350.Regular
