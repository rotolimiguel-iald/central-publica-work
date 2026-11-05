import Mathlib.Analysis.Normed.Operator.Extend
import Mathlib.Analysis.InnerProductSpace.Basic

set_option autoImplicit false
set_option linter.unusedSectionVars false

namespace TGLV350.Regular
noncomputable section
variable {E H : Type} [AddCommGroup E] [Module ℂ E]
  [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
variable (f : E →ₛₗ[starRingEnd ℂ] H) (e : E →ₗ[ℂ] H)
variable (hd : DenseRange e) (hn : ∀ x, ‖f x‖=‖e x‖)
include hd hn

/-- The same ambient Hilbert space is used on both sides of the extension. -/
theorem denseAntilinearExtension_apply (x : E) : f.extendOfNorm e (e x)=f x :=
  LinearMap.extendOfNorm_eq hd ⟨1,fun x => by simp only [one_mul,hn x]; exact le_rfl⟩ x

theorem denseAntilinearExtension_norm (x : H) : ‖f.extendOfNorm e x‖=‖x‖ := by
  refine hd.induction ?_ (isClosed_eq (by fun_prop) continuous_norm) x
  rintro _ ⟨y,rfl⟩
  rw [denseAntilinearExtension_apply f e hd hn y,hn y]

def denseAntilinearIsometry : H →ₛₗᵢ[starRingEnd ℂ] H where
  toLinearMap := (f.extendOfNorm e).toLinearMap
  norm_map' := denseAntilinearExtension_norm f e hd hn

theorem denseAntilinearIsometry_surjective (hf : DenseRange f) :
    Function.Surjective (denseAntilinearIsometry f e hd hn) := by
  have hs : Set.range f ⊆ Set.range (denseAntilinearIsometry f e hd hn) := by
    rintro _ ⟨x,rfl⟩
    exact ⟨e x,denseAntilinearExtension_apply f e hd hn x⟩
  have hc : IsClosed (Set.range (denseAntilinearIsometry f e hd hn)) :=
    (denseAntilinearIsometry f e hd hn).isometry.isClosedEmbedding.isClosed_range
  intro y
  exact hc.closure_subset (closure_mono hs (hf y))

/-- Dense image of f is required for an antiunitary equivalence, not just an isometry. -/
def denseAntilinearEquiv (hf : DenseRange f) : H ≃ₛₗᵢ[starRingEnd ℂ] H :=
  LinearIsometryEquiv.ofSurjective (denseAntilinearIsometry f e hd hn)
    (denseAntilinearIsometry_surjective f e hd hn hf)

theorem denseAntilinearEquiv_apply (hf : DenseRange f) (x : E) :
    denseAntilinearEquiv f e hd hn hf (e x)=f x :=
  denseAntilinearExtension_apply f e hd hn x

#print axioms denseAntilinearExtension_apply
#print axioms denseAntilinearExtension_norm
#print axioms denseAntilinearIsometry
#print axioms denseAntilinearIsometry_surjective
#print axioms denseAntilinearEquiv
#print axioms denseAntilinearEquiv_apply
end
end TGLV350.Regular
