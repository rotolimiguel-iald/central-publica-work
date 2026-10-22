import TGLV350.RegularDualAction
import TGLV350.L2BoundedStrongContinuity
set_option autoImplicit false
set_option maxHeartbeats 1000000
open TGLExt TGLV350.Regular Filter
open scoped Topology
noncomputable section
universe u
namespace DualIndependentTypes
example (P : SiteProfile) (s t : ℝ) :
    (regularDualAction P s ⟨regularUnitary P t, regularUnitary_mem P t⟩).val =
      Complex.exp (-Complex.I * (s : ℂ) * (t : ℂ)) • regularUnitary P t := by
  change dualAmbient s (regularUnitary P t) = _
  exact dualAmbient_regular P s t
example (P : SiteProfile) (s : ℝ) (A : (regularCoreAlgebra P).toStarSubalgebra) :
    regularDualAction P (-s) (regularDualAction P s A) = A := by
  calc
    _ = regularDualAction P (s + -s) A := by rw [regularDualAction_add]; rfl
    _ = A := by rw [add_neg_cancel, regularDualAction_zero]; rfl
example (P : SiteProfile) (s : ℝ) (A : (theFactorObject P).toStarSubalgebra) :
    regularDualAction P s (regularCoreEmbedding P A) = regularCoreEmbedding P A :=
  regularDualAction_fixes_embedding P s A
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
def anyFilter {ι : Type u} (l : Filter ι)
    (T : ι → (H →L[ℂ] H)) (S : H →L[ℂ] H) (C : ℝ)
    (hbound : ∀ i, ‖T i‖ ≤ C)
    (hT : ∀ v : H, Tendsto (fun i => T i v) l (𝓝 (S v)))
    (f : RegularHilbert H) :
    Tendsto (fun i => fibre (T i) f) l (𝓝 (fibre S f)) :=
  fibre_tendsto_of_uniformly_bounded T S C hbound hT f
#check anyFilter
#print axioms anyFilter
end DualIndependentTypes
end
