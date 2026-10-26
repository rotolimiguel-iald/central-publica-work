import TGLExt.V350HilbertProjectionBlocks
import Mathlib.Analysis.InnerProductSpace.Positive

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 200000

namespace TGLV350.Regular
open TGLExt WithLp
noncomputable section
variable {H E : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
  [AddCommGroup E] [Module ℂ E]

theorem hilbertBlockA_adjoint
    (S : Submodule ℂ (WithLp 2 (H × H))) [CompleteSpace S] :
    (hilbertBlockA S.starProjection).adjoint = hilbertBlockA S.starProjection := by
  unfold hilbertBlockA
  rw [ContinuousLinearMap.adjoint_comp,ContinuousLinearMap.adjoint_comp,
    ContinuousLinearMap.adjoint_adjoint,S.starProjection_isSymmetric.clm_adjoint_eq]
  exact ContinuousLinearMap.comp_assoc _ _ _

theorem hilbertBlockD_adjoint
    (S : Submodule ℂ (WithLp 2 (H × H))) [CompleteSpace S] :
    (hilbertBlockD S.starProjection).adjoint = hilbertBlockD S.starProjection := by
  unfold hilbertBlockD
  rw [ContinuousLinearMap.adjoint_comp,ContinuousLinearMap.adjoint_comp,
    ContinuousLinearMap.adjoint_adjoint,S.starProjection_isSymmetric.clm_adjoint_eq]
  exact ContinuousLinearMap.comp_assoc _ _ _

theorem hilbertBlockA_energy
    (S : Submodule ℂ (WithLp 2 (H × H))) [CompleteSpace S] (v : H) :
    (inner ℂ v (hilbertBlockA S.starProjection v)).re =
      ‖S.starProjection (hilbertPairInl v)‖^2 := by
  change (inner ℂ v ((hilbertPairInl (H:=H)).adjoint (S.starProjection (hilbertPairInl v)))).re = _
  rw [ContinuousLinearMap.adjoint_inner_right]
  exact (inner_re_symm (𝕜 := ℂ) (hilbertPairInl v)
    (S.starProjection (hilbertPairInl v))).trans (S.re_inner_starProjection_eq_normSq _)

theorem hilbertBlockA_nonneg
    (S : Submodule ℂ (WithLp 2 (H × H))) [CompleteSpace S] :
    0 ≤ hilbertBlockA S.starProjection := by
  apply (ContinuousLinearMap.nonneg_iff_isPositive _).mpr
  apply ContinuousLinearMap.isPositive_def'.mpr
  refine ⟨hilbertBlockA_adjoint S,?_⟩
  intro v
  change 0 ≤ (inner ℂ (hilbertBlockA S.starProjection v) v).re
  have he : (inner ℂ (hilbertBlockA S.starProjection v) v).re =
      ‖S.starProjection (hilbertPairInl v)‖^2 :=
    (inner_re_symm (𝕜 := ℂ) (hilbertBlockA S.starProjection v) v).trans (hilbertBlockA_energy S v)
  rw [he]
  exact sq_nonneg _

private theorem inlNormSq (v : H) : ‖hilbertPairInl v‖^2 = ‖v‖^2 := by
  have hi : inner ℂ (hilbertPairInl v) (hilbertPairInl v) = inner ℂ v v := by
    rw [WithLp.prod_inner_apply]
    change inner ℂ v v + inner ℂ (0:H) 0 = inner ℂ v v
    simp only [inner_zero_left,add_zero]
  exact (inner_self_eq_norm_sq (𝕜 := ℂ) (hilbertPairInl v)).symm.trans
    ((congrArg Complex.re hi).trans (inner_self_eq_norm_sq (𝕜 := ℂ) v))

theorem hilbertBlockA_le_one
    (S : Submodule ℂ (WithLp 2 (H × H))) [CompleteSpace S] :
    hilbertBlockA S.starProjection ≤ 1 := by
  apply sub_nonneg.mp
  apply (ContinuousLinearMap.nonneg_iff_isPositive _).mpr
  apply ContinuousLinearMap.isPositive_def'.mpr
  refine ⟨?_,?_⟩
  · change star (1-hilbertBlockA S.starProjection)=1-hilbertBlockA S.starProjection
    rw [star_sub,star_one]
    exact congrArg (fun T : H →L[ℂ] H => 1-T) (hilbertBlockA_adjoint S)
  · intro v
    change 0 ≤ (inner ℂ (v-hilbertBlockA S.starProjection v) v).re
    rw [inner_sub_left,Complex.sub_re]
    have he : (inner ℂ (hilbertBlockA S.starProjection v) v).re =
        ‖S.starProjection (hilbertPairInl v)‖^2 :=
      (inner_re_symm (𝕜 := ℂ) (hilbertBlockA S.starProjection v) v).trans (hilbertBlockA_energy S v)
    have hv : (inner ℂ v v).re = ‖v‖^2 := inner_self_eq_norm_sq (𝕜 := ℂ) v
    rw [he,hv]
    have hp := S.norm_sq_eq_add_norm_sq_starProjection (hilbertPairInl v)
    rw [inlNormSq] at hp
    linarith only [hp,sq_nonneg ‖S.orthogonal.starProjection (hilbertPairInl v)‖]

private theorem pairDecompose (p : WithLp 2 (H × H)) :
    hilbertPairInl ((hilbertPairInl (H:=H)).adjoint p) +
      hilbertPairInr ((hilbertPairInr (H:=H)).adjoint p) = p := by
  rw [hilbertPairInl_adjoint_apply,hilbertPairInr_adjoint_apply]
  change toLp 2 ((ofLp p).1+0,0+(ofLp p).2) = toLp 2 ((ofLp p).1,(ofLp p).2)
  rw [add_zero,zero_add]

private theorem projectionInlDecompose
    (S : Submodule ℂ (WithLp 2 (H × H))) [CompleteSpace S] (v : H) :
    S.starProjection (hilbertPairInl v) =
      hilbertPairInl (hilbertBlockA S.starProjection v) +
        hilbertPairInr ((hilbertBlockB S.starProjection).adjoint v) := by
  rw [hilbertBlockB_adjoint]
  exact (pairDecompose (S.starProjection (hilbertPairInl v))).symm

private theorem projectionInrDecompose
    (S : Submodule ℂ (WithLp 2 (H × H))) [CompleteSpace S] (v : H) :
    S.starProjection (hilbertPairInr v) =
      hilbertPairInl (hilbertBlockB S.starProjection v) +
        hilbertPairInr (hilbertBlockD S.starProjection v) :=
  (pairDecompose (S.starProjection (hilbertPairInr v))).symm

private theorem firstProjectionOnInserts
    (S : Submodule ℂ (WithLp 2 (H × H))) [CompleteSpace S] (x y : H) :
    (hilbertPairInl (H:=H)).adjoint (S.starProjection (hilbertPairInl x + hilbertPairInr y)) =
      hilbertBlockA S.starProjection x + hilbertBlockB S.starProjection y := by
  rw [map_add,map_add]
  rfl

private theorem projectionFirstIdempotence
    (S : Submodule ℂ (WithLp 2 (H × H))) [CompleteSpace S] :
    hilbertBlockA S.starProjection * hilbertBlockA S.starProjection +
      hilbertBlockB S.starProjection * star (hilbertBlockB S.starProjection) =
        hilbertBlockA S.starProjection := by
  ext1 v
  calc
    _ = (hilbertPairInl (H:=H)).adjoint (S.starProjection
        (hilbertPairInl (hilbertBlockA S.starProjection v) +
          hilbertPairInr ((hilbertBlockB S.starProjection).adjoint v))) := (firstProjectionOnInserts S _ _).symm
    _ = (hilbertPairInl (H:=H)).adjoint (S.starProjection (S.starProjection (hilbertPairInl v))) :=
      congrArg (fun x => (hilbertPairInl (H:=H)).adjoint (S.starProjection x)) (projectionInlDecompose S v).symm
    _ = _ := congrArg (hilbertPairInl (H:=H)).adjoint
      (Submodule.starProjection_eq_self_iff.mpr (S.starProjection_apply_mem (hilbertPairInl v)))

theorem hilbertBlockB_mul_adjoint
    (S : Submodule ℂ (WithLp 2 (H × H))) [CompleteSpace S] :
    hilbertBlockB S.starProjection * star (hilbertBlockB S.starProjection) =
      hilbertBlockA S.starProjection * (1-hilbertBlockA S.starProjection) := by
  have he := projectionFirstIdempotence S
  rw [mul_sub,mul_one]
  exact eq_sub_of_add_eq' he

theorem hilbertBlockB_mul_D
    (S : Submodule ℂ (WithLp 2 (H × H))) [CompleteSpace S] :
    hilbertBlockB S.starProjection * hilbertBlockD S.starProjection =
      (1-hilbertBlockA S.starProjection) * hilbertBlockB S.starProjection := by
  have he : hilbertBlockA S.starProjection * hilbertBlockB S.starProjection +
      hilbertBlockB S.starProjection * hilbertBlockD S.starProjection =
        hilbertBlockB S.starProjection := by
    ext1 v
    calc
      _ = (hilbertPairInl (H:=H)).adjoint (S.starProjection
          (hilbertPairInl (hilbertBlockB S.starProjection v) +
            hilbertPairInr (hilbertBlockD S.starProjection v))) := (firstProjectionOnInserts S _ _).symm
      _ = (hilbertPairInl (H:=H)).adjoint (S.starProjection (S.starProjection (hilbertPairInr v))) :=
        congrArg (fun x => (hilbertPairInl (H:=H)).adjoint (S.starProjection x)) (projectionInrDecompose S v).symm
      _ = _ := congrArg (hilbertPairInl (H:=H)).adjoint
        (Submodule.starProjection_eq_self_iff.mpr (S.starProjection_apply_mem (hilbertPairInr v)))
  rw [sub_mul,one_mul]
  exact eq_sub_of_add_eq' he

theorem complexGraph_blockA_injective (e f : E →ₗ[ℂ] H) (he : DenseRange e) :
    Function.Injective (hilbertBlockA (complexGraphClosure e f).starProjection) := by
  have hz : ∀ v : H, hilbertBlockA (complexGraphClosure e f).starProjection v=0 → v=0 := by
    intro v hv
    by_contra hn
    have hp := sq_pos_of_pos (norm_pos_iff.mpr (complexGraph_projection_inl_ne_zero e f he v hn))
    have hE := hilbertBlockA_energy (complexGraphClosure e f) v
    rw [hv,inner_zero_right,Complex.zero_re] at hE
    linarith only [hp,hE]
  intro x y hxy
  apply sub_eq_zero.mp
  apply hz
  rw [map_sub,hxy,sub_self]

#print axioms hilbertBlockA_adjoint
#print axioms hilbertBlockD_adjoint
#print axioms hilbertBlockA_energy
#print axioms hilbertBlockA_nonneg
#print axioms hilbertBlockA_le_one
#print axioms hilbertBlockB_mul_adjoint
#print axioms hilbertBlockB_mul_D
#print axioms complexGraph_blockA_injective
end
end TGLV350.Regular
