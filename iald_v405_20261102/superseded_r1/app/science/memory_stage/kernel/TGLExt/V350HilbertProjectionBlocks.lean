import TGLExt.V350ComplexGraphProjection

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1500000

namespace TGLV350.Regular
open TGLExt WithLp
noncomputable section
variable {H E : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
  [AddCommGroup E] [Module ℂ E]

theorem hilbertPairInl_adjoint_apply (p : WithLp 2 (H × H)) :
    (hilbertPairInl (H := H)).adjoint p = (ofLp p).1 := by
  apply ext_inner_right ℂ
  intro y
  rw [ContinuousLinearMap.adjoint_inner_left]
  rw [WithLp.prod_inner_apply]
  change inner ℂ (ofLp p).1 y + inner ℂ (ofLp p).2 0 = inner ℂ (ofLp p).1 y
  rw [inner_zero_right,add_zero]

theorem hilbertPairInr_adjoint_apply (p : WithLp 2 (H × H)) :
    (hilbertPairInr (H := H)).adjoint p = (ofLp p).2 := by
  apply ext_inner_right ℂ
  intro y
  rw [ContinuousLinearMap.adjoint_inner_left,WithLp.prod_inner_apply]
  change inner ℂ (ofLp p).1 0 + inner ℂ (ofLp p).2 y = inner ℂ (ofLp p).2 y
  rw [inner_zero_right,zero_add]

def hilbertBlockA (P : WithLp 2 (H × H) →L[ℂ] WithLp 2 (H × H)) : H →L[ℂ] H :=
  hilbertPairInl.adjoint.comp (P.comp hilbertPairInl)

def hilbertBlockB (P : WithLp 2 (H × H) →L[ℂ] WithLp 2 (H × H)) : H →L[ℂ] H :=
  hilbertPairInl.adjoint.comp (P.comp hilbertPairInr)

def hilbertBlockD (P : WithLp 2 (H × H) →L[ℂ] WithLp 2 (H × H)) : H →L[ℂ] H :=
  hilbertPairInr.adjoint.comp (P.comp hilbertPairInr)

theorem hilbertBlockB_adjoint
    (S : Submodule ℂ (WithLp 2 (H × H))) [CompleteSpace S] :
    (hilbertBlockB S.starProjection).adjoint =
      hilbertPairInr.adjoint.comp (S.starProjection.comp hilbertPairInl) := by
  unfold hilbertBlockB
  rw [ContinuousLinearMap.adjoint_comp,ContinuousLinearMap.adjoint_comp,
    ContinuousLinearMap.adjoint_adjoint,S.starProjection_isSymmetric.clm_adjoint_eq]
  exact ContinuousLinearMap.comp_assoc _ _ _

theorem hilbertPairDiagonal_inl (T : H →L[ℂ] H) (v : H) :
    hilbertPairDiagonal T (hilbertPairInl v) = hilbertPairInl (T v) := by
  change toLp 2 (T v,T 0) = toLp 2 (T v,0)
  rw [map_zero]

theorem hilbertPairDiagonal_inr (T : H →L[ℂ] H) (v : H) :
    hilbertPairDiagonal T (hilbertPairInr v) = hilbertPairInr (T v) := by
  change toLp 2 (T 0,T v) = toLp 2 (0,T v)
  rw [map_zero]

theorem hilbertBlockA_commutes
    (P : WithLp 2 (H × H) →L[ℂ] WithLp 2 (H × H)) (T : H →L[ℂ] H)
    (hc : ∀ x, P (hilbertPairDiagonal T x) = hilbertPairDiagonal T (P x)) :
    Commute (hilbertBlockA P) T := by
  ext1 v
  change hilbertPairInl.adjoint (P (hilbertPairInl (T v))) =
    T (hilbertPairInl.adjoint (P (hilbertPairInl v)))
  rw [← hilbertPairDiagonal_inl,hc,hilbertPairInl_adjoint_apply,hilbertPairInl_adjoint_apply]
  rfl

theorem hilbertBlockB_commutes
    (P : WithLp 2 (H × H) →L[ℂ] WithLp 2 (H × H)) (T : H →L[ℂ] H)
    (hc : ∀ x, P (hilbertPairDiagonal T x) = hilbertPairDiagonal T (P x)) :
    Commute (hilbertBlockB P) T := by
  ext1 v
  change hilbertPairInl.adjoint (P (hilbertPairInr (T v))) =
    T (hilbertPairInl.adjoint (P (hilbertPairInr v)))
  rw [← hilbertPairDiagonal_inr,hc,hilbertPairInl_adjoint_apply,hilbertPairInl_adjoint_apply]
  rfl

theorem hilbertBlockD_commutes
    (P : WithLp 2 (H × H) →L[ℂ] WithLp 2 (H × H)) (T : H →L[ℂ] H)
    (hc : ∀ x, P (hilbertPairDiagonal T x) = hilbertPairDiagonal T (P x)) :
    Commute (hilbertBlockD P) T := by
  ext1 v
  change hilbertPairInr.adjoint (P (hilbertPairInr (T v))) =
    T (hilbertPairInr.adjoint (P (hilbertPairInr v)))
  rw [← hilbertPairDiagonal_inr,hc,hilbertPairInr_adjoint_apply,hilbertPairInr_adjoint_apply]
  rfl

theorem hilbertBlockB_from_rotated
    (P : WithLp 2 (H × H) →L[ℂ] WithLp 2 (H × H)) (x y : H)
    (hp : P (toLp 2 (y,-x)) = 0) : hilbertBlockB P x = hilbertBlockA P y := by
  have he : toLp 2 (y,-x) = hilbertPairInl y - hilbertPairInr x := by
    change toLp 2 (y,-x) = toLp 2 (y-0,0-x)
    rw [sub_zero,zero_sub]
  rw [he,map_sub] at hp
  exact (congrArg (hilbertPairInl (H := H)).adjoint (sub_eq_zero.mp hp)).symm

theorem hilbertBlockBadjoint_from_fixed
    (S : Submodule ℂ (WithLp 2 (H × H))) [CompleteSpace S] (x y : H)
    (hp : S.starProjection (toLp 2 (x,y)) = toLp 2 (x,y)) :
    (hilbertBlockB S.starProjection).adjoint x = y - hilbertBlockD S.starProjection y := by
  have he : toLp 2 (x,y) = hilbertPairInl x + hilbertPairInr y := by
    change toLp 2 (x,y) = toLp 2 (x+0,0+y)
    rw [add_zero,zero_add]
  have hq := congrArg (hilbertPairInr (H := H)).adjoint hp
  rw [he,map_add,map_add,hilbertPairInr_adjoint_apply,hilbertPairInr_adjoint_apply] at hq
  change (ofLp (S.starProjection (hilbertPairInl x))).2 +
      (ofLp (S.starProjection (hilbertPairInr y))).2 = _ at hq
  have hr : (hilbertPairInr (H := H)).adjoint (hilbertPairInl x + hilbertPairInr y) = y := by
    rw [hilbertPairInr_adjoint_apply]
    change 0+y=y
    rw [zero_add]
  rw [hr] at hq
  rw [hilbertBlockB_adjoint]
  change hilbertPairInr.adjoint (S.starProjection (hilbertPairInl x)) =
    y - hilbertPairInr.adjoint (S.starProjection (hilbertPairInr y))
  rw [hilbertPairInr_adjoint_apply,hilbertPairInr_adjoint_apply]
  exact eq_sub_of_add_eq hq

def hilbertProjectionWitness
    (S : Submodule ℂ (WithLp 2 (H × H))) [CompleteSpace S] (v : H) : H :=
  hilbertBlockA S.starProjection v + v - hilbertBlockD S.starProjection v

theorem hilbertProjectionWitness_energy
    (S : Submodule ℂ (WithLp 2 (H × H))) [CompleteSpace S] (v : H) :
    (inner ℂ v (hilbertProjectionWitness S v)).re =
      ‖S.starProjection (hilbertPairInl v)‖^2 +
        ‖S.orthogonal.starProjection (hilbertPairInr v)‖^2 := by
  have ha : (inner ℂ v (hilbertBlockA S.starProjection v)).re =
      ‖S.starProjection (hilbertPairInl v)‖^2 := by
    change (inner ℂ v (hilbertPairInl.adjoint (S.starProjection (hilbertPairInl v)))).re = _
    rw [ContinuousLinearMap.adjoint_inner_right]
    exact (inner_re_symm (𝕜 := ℂ) (hilbertPairInl v)
      (S.starProjection (hilbertPairInl v))).trans (S.re_inner_starProjection_eq_normSq _)
  have hd : (inner ℂ v (hilbertBlockD S.starProjection v)).re =
      ‖S.starProjection (hilbertPairInr v)‖^2 := by
    change (inner ℂ v (hilbertPairInr.adjoint (S.starProjection (hilbertPairInr v)))).re = _
    rw [ContinuousLinearMap.adjoint_inner_right]
    exact (inner_re_symm (𝕜 := ℂ) (hilbertPairInr v)
      (S.starProjection (hilbertPairInr v))).trans (S.re_inner_starProjection_eq_normSq _)
  have hi : inner ℂ (hilbertPairInr v) (hilbertPairInr v) = inner ℂ v v := by
    rw [WithLp.prod_inner_apply]
    change inner ℂ (0 : H) 0 + inner ℂ v v = inner ℂ v v
    rw [inner_zero_left,zero_add]
  have hn : ‖hilbertPairInr v‖^2 = (inner ℂ v v).re :=
    (inner_self_eq_norm_sq (𝕜 := ℂ) (hilbertPairInr v)).symm.trans (congrArg Complex.re hi)
  have hpy := S.norm_sq_eq_add_norm_sq_starProjection (hilbertPairInr v)
  unfold hilbertProjectionWitness
  rw [inner_sub_right,inner_add_right,Complex.sub_re,Complex.add_re,ha,hd]
  linarith only [hn,hpy]

/-- Norm density of the first graph coordinate makes the positive witness
strictly detect every nonzero vector; no boundedness of f is used. -/
theorem complexGraph_projection_inl_ne_zero (e f : E →ₗ[ℂ] H)
    (he : DenseRange e) (v : H) (hv : v ≠ 0) :
    (complexGraphClosure e f).starProjection (hilbertPairInl v) ≠ 0 := by
  intro hp
  apply hv
  apply he.eq_zero_of_inner_right (𝕜 := ℂ)
  intro a
  have ho := (Submodule.starProjection_apply_eq_zero_iff (complexGraphClosure e f)).mp hp
  have hh := ho _ (complexGraphEmbedding_mem e f a)
  rw [WithLp.prod_inner_apply] at hh
  change inner ℂ (e a) v + inner ℂ (f a) 0 = 0 at hh
  simpa only [inner_zero_right,add_zero] using hh

theorem complexGraph_witness_positive (e f : E →ₗ[ℂ] H) (he : DenseRange e)
    (v : H) (hv : v ≠ 0) :
    0 < (inner ℂ v (hilbertProjectionWitness (complexGraphClosure e f) v)).re := by
  rw [hilbertProjectionWitness_energy]
  have hp := sq_pos_of_pos (norm_pos_iff.mpr (complexGraph_projection_inl_ne_zero e f he v hv))
  exact add_pos_of_pos_of_nonneg hp (sq_nonneg _)

#print axioms hilbertPairInl_adjoint_apply
#print axioms hilbertPairInr_adjoint_apply
#print axioms hilbertBlockA
#print axioms hilbertBlockB
#print axioms hilbertBlockD
#print axioms hilbertBlockB_adjoint
#print axioms hilbertPairDiagonal_inl
#print axioms hilbertPairDiagonal_inr
#print axioms hilbertBlockA_commutes
#print axioms hilbertBlockB_commutes
#print axioms hilbertBlockD_commutes
#print axioms hilbertBlockB_from_rotated
#print axioms hilbertBlockBadjoint_from_fixed
#print axioms hilbertProjectionWitness
#print axioms hilbertProjectionWitness_energy
#print axioms complexGraph_projection_inl_ne_zero
#print axioms complexGraph_witness_positive
end
end TGLV350.Regular
