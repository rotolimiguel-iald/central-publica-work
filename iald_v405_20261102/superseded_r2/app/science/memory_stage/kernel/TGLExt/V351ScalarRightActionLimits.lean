import TGLExt.V351ScalarGNSClosedness
import TGLExt.V350ScalarRegularRightPolar
import TGLExt.V350ScalarGNSStrongContinuity

set_option autoImplicit false
set_option maxHeartbeats 1800000

namespace TGLV350.Regular
open TGLExt Filter
open scoped Topology
noncomputable section

/-- The previously constructed right translation is the original polar right
action on every vector in the full scalar-weight ideal. -/
theorem scalarRightAction_regular (P : SiteProfile) (t : ℝ)
    (A : scalarWeightLeftIdeal P) :
    scalarWeightGNSEmbedding P (scalarRegularRightProduct P t A) =
      antiunitaryConjugate (scalarTomitaPolarFactor P)
        (scalarGNSRepresentation P (star (regularRightCoreElement P t)))
          (scalarWeightGNSEmbedding P A) := by
  rw [← regularRightGNS_intertwines,antiunitaryConjugate_apply,
    scalarTomitaPolarFactor_regular_left,LinearIsometryEquiv.apply_symm_apply]

/-- Pass a proved right identity to an actual bounded strong-star limit.
The approximating family is an input, not asserted to exist by this theorem. -/
theorem scalarRightAction_closed_of_bounded_strongStar (P : SiteProfile)
    {ι : Type*} {l : Filter ι} [NeBot l]
    (b : ι → (regularCoreAlgebra P).toStarSubalgebra)
    (B : (regularCoreAlgebra P).toStarSubalgebra) (C : ℝ)
    (hbound : ∀ i, ‖(b i).val‖ ≤ C)
    (hstrong : ∀ x, Tendsto (fun i => (b i).val x) l (𝓝 (B.val x)))
    (hadjoint : ∀ x, Tendsto (fun i => (star (b i)).val x) l (𝓝 ((star B).val x)))
    (A : scalarWeightLeftIdeal P)
    (hact : ∀ i, ∃ hi : A.val * b i ∈ scalarWeightLeftIdeal P,
      scalarWeightGNSEmbedding P ⟨A.val*b i,hi⟩ =
        antiunitaryConjugate (scalarTomitaPolarFactor P)
          (scalarGNSRepresentation P (star (b i))) (scalarWeightGNSEmbedding P A)) :
    ∃ hAB : A.val * B ∈ scalarWeightLeftIdeal P,
      scalarWeightGNSEmbedding P ⟨A.val*B,hAB⟩ =
        antiunitaryConjugate (scalarTomitaPolarFactor P)
          (scalarGNSRepresentation P (star B)) (scalarWeightGNSEmbedding P A) := by
  let T (i : ι) : scalarWeightLeftIdeal P := ⟨A.val*b i,(hact i).choose⟩
  have hnorm (i : ι) : ‖(star (b i)).val‖ ≤ C := by
    change ‖star (b i).val‖ ≤ C
    simpa only [norm_star] using hbound i
  have hp := scalarGNSRepresentation_tendsto_of_uniformly_bounded P
    (fun i => star (b i)) (star B) C hnorm hadjoint
      ((scalarTomitaPolarFactor P).symm (scalarWeightGNSEmbedding P A))
  have hj := (scalarTomitaPolarFactor P).continuous.continuousAt.tendsto.comp hp
  have hgns : Tendsto (fun i => scalarWeightGNSEmbedding P (T i)) l
      (𝓝 (antiunitaryConjugate (scalarTomitaPolarFactor P)
        (scalarGNSRepresentation P (star B)) (scalarWeightGNSEmbedding P A))) := by
    have hi (i : ι) : scalarWeightGNSEmbedding P (T i) =
        antiunitaryConjugate (scalarTomitaPolarFactor P)
          (scalarGNSRepresentation P (star (b i))) (scalarWeightGNSEmbedding P A) :=
      (hact i).choose_spec
    simp only [Function.comp_def] at hj
    simpa only [hi,antiunitaryConjugate_apply] using hj
  apply scalarWeightGNSEmbedding_closed_of_bounded_strong P T (A.val*B) _
    (‖A.val.val‖*C) _ _ hgns
  · intro i
    exact (norm_mul_le A.val.val (b i).val).trans
      (mul_le_mul_of_nonneg_left (hbound i) (norm_nonneg A.val.val))
  · intro x
    exact A.val.val.continuous.continuousAt.tendsto.comp (hstrong x)

#print axioms scalarRightAction_regular
#print axioms scalarRightAction_closed_of_bounded_strongStar
end
end TGLV350.Regular
