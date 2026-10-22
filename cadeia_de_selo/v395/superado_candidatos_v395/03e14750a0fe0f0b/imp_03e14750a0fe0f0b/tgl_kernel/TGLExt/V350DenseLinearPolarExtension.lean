import Mathlib.Analysis.Normed.Operator.Extend
import Mathlib.Analysis.InnerProductSpace.Basic

set_option autoImplicit false
set_option linter.unusedSectionVars false

namespace TGLV350.Regular
noncomputable section
variable {E H K : Type} [AddCommGroup E] [Module ℂ E]
  [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
  [NormedAddCommGroup K] [InnerProductSpace ℂ K] [CompleteSpace K]
variable (f : E →ₗ[ℂ] K) (e : E →ₗ[ℂ] H)
variable (hd : DenseRange e) (hn : ∀ x, ‖f x‖ = ‖e x‖)
include hd hn

theorem denseLinearExtension_apply (x : E) : f.extendOfNorm e (e x) = f x :=
  LinearMap.extendOfNorm_eq hd ⟨1,fun x => by simp only [one_mul,hn x]; exact le_rfl⟩ x

theorem denseLinearExtension_norm (x : H) : ‖f.extendOfNorm e x‖ = ‖x‖ := by
  refine hd.induction ?_ (isClosed_eq (by fun_prop) continuous_norm) x
  rintro _ ⟨y,rfl⟩
  rw [denseLinearExtension_apply f e hd hn y,hn y]

def denseLinearIsometry : H →ₗᵢ[ℂ] K where
  toLinearMap := (f.extendOfNorm e).toLinearMap
  norm_map' := denseLinearExtension_norm f e hd hn

theorem denseLinearIsometry_surjective (hf : DenseRange f) :
    Function.Surjective (denseLinearIsometry f e hd hn) := by
  have hs : Set.range f ⊆ Set.range (denseLinearIsometry f e hd hn) := by
    rintro _ ⟨x,rfl⟩
    exact ⟨e x,denseLinearExtension_apply f e hd hn x⟩
  have hc : IsClosed (Set.range (denseLinearIsometry f e hd hn)) :=
    (denseLinearIsometry f e hd hn).isometry.isClosedEmbedding.isClosed_range
  intro y
  exact hc.closure_subset (closure_mono hs (hf y))

/-- Both dense-range hypotheses are proved separately at each application. -/
def denseLinearEquiv (hf : DenseRange f) : H ≃ₗᵢ[ℂ] K :=
  LinearIsometryEquiv.ofSurjective (denseLinearIsometry f e hd hn)
    (denseLinearIsometry_surjective f e hd hn hf)

theorem denseLinearEquiv_apply (hf : DenseRange f) (x : E) :
    denseLinearEquiv f e hd hn hf (e x) = f x :=
  denseLinearExtension_apply f e hd hn x

#print axioms denseLinearExtension_apply
#print axioms denseLinearExtension_norm
#print axioms denseLinearIsometry
#print axioms denseLinearIsometry_surjective
#print axioms denseLinearEquiv
#print axioms denseLinearEquiv_apply
end
end TGLV350.Regular

