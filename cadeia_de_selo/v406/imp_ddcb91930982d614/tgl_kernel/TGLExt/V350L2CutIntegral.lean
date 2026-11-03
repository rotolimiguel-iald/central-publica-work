import TGLExt.V350ConstantFibreCandidate

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 700000

namespace TGLV350.Regular
open MeasureTheory Filter
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

theorem setIntegral_measurableCut (S T : Set ℝ) (hT : MeasurableSet T)
    (f : RegularHilbert H) :
    (∫ x in S, measurableCut T hT f x) = ∫ x in S ∩ T, f x := by
  calc
    _ = ∫ x in S, T.indicator f x :=
      integral_congr_ae (ae_restrict_of_ae (measurableCut_ae T hT f))
    _ = _ := by
      rw [integral_indicator hT, Measure.restrict_restrict hT, Set.inter_comm]

theorem unitCut_integral_eq_read_cut (S : Set ℝ) (hS : MeasurableSet S)
    (f : RegularHilbert H) :
    (∫ x in S, unitCut f x) = testEmbeddingCLM.adjoint (measurableCut S hS f) := by
  rw [testEmbedding_adjoint]
  change (∫ x in S, measurableCut (Set.Ioc (0 : ℝ) 1) measurableSet_Ioc f x) = _
  rw [setIntegral_measurableCut, setIntegral_measurableCut, Set.inter_comm]

theorem testEmbedding_adjoint_fibre (C : H →L[ℂ] H) (f : RegularHilbert H) :
    testEmbeddingCLM.adjoint (fibre C f) = C (testEmbeddingCLM.adjoint f) := by
  rw [testEmbedding_adjoint, testEmbedding_adjoint]
  calc
    _ = ∫ x in Set.Ioc (0 : ℝ) 1, C (f x) :=
      integral_congr_ae (ae_restrict_of_ae (fibre_ae C f))
    _ = _ := C.integral_comp_comm
      (integrableOn_Lp_of_measure_ne_top f (by norm_num) (by simp))

theorem fibre_commutes_measurableCut (C : H →L[ℂ] H)
    (S : Set ℝ) (hS : MeasurableSet S) :
    measurableCut S hS * fibre C = fibre C * measurableCut S hS := by
  ext1 f
  apply Lp.ext
  filter_upwards [measurableCut_ae S hS (fibre C f), fibre_ae C f,
    fibre_ae C (measurableCut S hS f), measurableCut_ae S hS f] with x h1 h2 h3 h4
  change measurableCut S hS (fibre C f) x = fibre C (measurableCut S hS f) x
  rw [h1,h3,h4]
  by_cases hx : x ∈ S
  · simp only [Set.indicator_of_mem hx]
    exact h2
  · simp only [Set.indicator_of_notMem hx, map_zero]

/-- A local operator with zero interval read vanishes on that interval.
The proof uses all finite-set Bochner integrals, not point evaluation in L2. -/
theorem unitCut_mul_eq_zero_of_zero_read
    (A : RegularHilbert H →L[ℂ] RegularHilbert H)
    (hcut : ∀ (S : Set ℝ) (hS : MeasurableSet S), measurableCut S hS * A = A * measurableCut S hS)
    (hread : ∀ f : RegularHilbert H, testEmbeddingCLM.adjoint (A f) = 0) :
    unitCut * A = 0 := by
  ext1 f
  apply Lp.ext
  have hz : (unitCut (A f) : ℝ → H) =ᵐ[volume] 0 := by
    apply Lp.ae_eq_zero_of_forall_setIntegral_eq_zero (unitCut (A f)) (by norm_num) (by norm_num)
    · intro S hS hfin
      exact integrableOn_Lp_of_measure_ne_top _ (by norm_num) hfin.ne
    · intro S hS _
      rw [unitCut_integral_eq_read_cut S hS]
      have hc := congrArg (fun T : RegularHilbert H →L[ℂ] RegularHilbert H => T f) (hcut S hS)
      change measurableCut S hS (A f) = A (measurableCut S hS f) at hc
      rw [hc, hread]
  exact hz.trans (Lp.coeFn_zero H 2 volume).symm

#print axioms setIntegral_measurableCut
#print axioms unitCut_integral_eq_read_cut
#print axioms testEmbedding_adjoint_fibre
#print axioms fibre_commutes_measurableCut
#print axioms unitCut_mul_eq_zero_of_zero_read
end
end TGLV350.Regular
