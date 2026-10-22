import TGLExt.V350L2OperatorLift

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

namespace TGLV350.Regular
open MeasureTheory
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

structure FiniteFibreSet where
  carrier : Set ℝ
  measurable : MeasurableSet carrier
  finiteMeasure : volume carrier ≠ ⊤

def finiteSetEmbeddingLinear (s : FiniteFibreSet) : H →ₗ[ℂ] RegularHilbert H where
  toFun v := indicatorConstLp 2 s.measurable s.finiteMeasure v
  map_add' _ _ := indicatorConstLp_add.symm
  map_smul' c v := by
    apply Lp.ext
    filter_upwards [indicatorConstLp_coeFn (p := (2 : ENNReal))
      (hs := s.measurable) (hμs := s.finiteMeasure) (c := c • v),
      Lp.coeFn_smul c (indicatorConstLp 2 s.measurable s.finiteMeasure v),
      indicatorConstLp_coeFn (p := (2 : ENNReal))
        (hs := s.measurable) (hμs := s.finiteMeasure) (c := v)] with x h1 h2 h3
    change indicatorConstLp 2 s.measurable s.finiteMeasure (c • v) x =
      (c • indicatorConstLp 2 s.measurable s.finiteMeasure v) x
    rw [h1,h2,Pi.smul_apply,h3]
    by_cases hx : x ∈ s.carrier <;> simp [hx]

def finiteSetEmbedding (s : FiniteFibreSet) : H →L[ℂ] RegularHilbert H :=
  (finiteSetEmbeddingLinear s).mkContinuous (volume.real s.carrier ^ (1/(2 : ℝ))) (by
    intro v
    change ‖indicatorConstLp 2 s.measurable s.finiteMeasure v‖ ≤ _
    rw [norm_indicatorConstLp (by norm_num) (by norm_num)]
    simp only [ENNReal.toReal_ofNat]
    exact le_of_eq (mul_comm _ _))

theorem finiteSetEmbedding_adjoint (s : FiniteFibreSet) (f : RegularHilbert H) :
    (finiteSetEmbedding s).adjoint f = ∫ x in s.carrier, f x := by
  apply ext_inner_left ℂ
  intro v
  rw [ContinuousLinearMap.adjoint_inner_right]
  exact L2.inner_indicatorConstLp_eq_inner_setIntegral ℂ s.measurable s.finiteMeasure v f

/-- All finite-set reads determine the L2 vector, with no point evaluation. -/
theorem finiteSetEmbedding_reads_separate (f : RegularHilbert H)
    (h : ∀ s : FiniteFibreSet, (finiteSetEmbedding s).adjoint f = 0) : f = 0 := by
  apply Lp.ext
  have hz : (f : ℝ → H) =ᵐ[volume] 0 := by
    apply Lp.ae_eq_zero_of_forall_setIntegral_eq_zero f (by norm_num) (by norm_num)
    · intro S hS hfin
      exact integrableOn_Lp_of_measure_ne_top f (by norm_num) hfin.ne
    · intro S hS hfin
      exact (finiteSetEmbedding_adjoint ⟨S,hS,hfin.ne⟩ f).symm.trans (h ⟨S,hS,hfin.ne⟩)
  exact hz.trans (Lp.coeFn_zero H 2 volume).symm

theorem finiteSetEmbedding_intertwines (s : FiniteFibreSet) (A : H →L[ℂ] H) :
    (fibre A).comp (finiteSetEmbedding s) = (finiteSetEmbedding s).comp A := by
  ext1 v
  apply Lp.ext
  filter_upwards [fibre_ae A (finiteSetEmbedding s v),
    indicatorConstLp_coeFn (p := (2 : ENNReal))
      (hs := s.measurable) (hμs := s.finiteMeasure) (c := v),
    indicatorConstLp_coeFn (p := (2 : ENNReal))
      (hs := s.measurable) (hμs := s.finiteMeasure) (c := A v)] with x h1 h2 h3
  change fibre A (finiteSetEmbedding s v) x = finiteSetEmbedding s (A v) x
  rw [h1,show finiteSetEmbedding s v x = _ from h2,
    show finiteSetEmbedding s (A v) x = _ from h3]
  by_cases hx : x ∈ s.carrier <;> simp [hx]

theorem finiteSetEmbedding_adjoint_intertwines (s : FiniteFibreSet) (A : H →L[ℂ] H) :
    (finiteSetEmbedding s).adjoint.comp (fibre A) = A.comp (finiteSetEmbedding s).adjoint := by
  have h := congrArg ContinuousLinearMap.adjoint (finiteSetEmbedding_intertwines s (star A))
  simpa only [ContinuousLinearMap.adjoint_comp,← ContinuousLinearMap.star_eq_adjoint,
    ← fibre_star,star_star] using h

#print axioms finiteSetEmbeddingLinear
#print axioms finiteSetEmbedding
#print axioms finiteSetEmbedding_adjoint
#print axioms finiteSetEmbedding_reads_separate
#print axioms finiteSetEmbedding_intertwines
#print axioms finiteSetEmbedding_adjoint_intertwines
end
end TGLV350.Regular
