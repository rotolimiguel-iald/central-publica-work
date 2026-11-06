import Mathlib.Analysis.InnerProductSpace.Adjoint
/-! The range projection of an actual isometry and a checked intertwining criterion. -/
set_option autoImplicit false
set_option maxErrors 3
set_option maxHeartbeats 600000
noncomputable section
namespace F1Fecho.IsometricReducingRange
variable {E F : Type} [NormedAddCommGroup E] [InnerProductSpace ℂ E] [CompleteSpace E]
  [NormedAddCommGroup F] [InnerProductSpace ℂ F] [CompleteSpace F]

def projection (V : E →ₗᵢ[ℂ] F) : F →L[ℂ] F :=
  V.toContinuousLinearMap.comp V.toContinuousLinearMap.adjoint

theorem projection_apply_image (V : E →ₗᵢ[ℂ] F) (x : E) : projection V (V x)=V x := by
  change V (V.toContinuousLinearMap.adjoint (V.toContinuousLinearMap x))=V x
  have h := congrArg (fun T : E →L[ℂ] E => T x) V.adjoint_comp_self
  exact congrArg V h

theorem mem_range_iff (V : E →ₗᵢ[ℂ] F) (y : F) :
    y ∈ Set.range V ↔ projection V y=y := by
  constructor
  · rintro ⟨x,rfl⟩; exact projection_apply_image V x
  · intro h; exact ⟨V.toContinuousLinearMap.adjoint y,h⟩

theorem projection_idem (V : E →ₗᵢ[ℂ] F) : projection V * projection V=projection V := by
  ext1 x
  exact projection_apply_image V (V.toContinuousLinearMap.adjoint x)

theorem projection_star (V : E →ₗᵢ[ℂ] F) : star (projection V)=projection V := by
  simp only [projection,ContinuousLinearMap.star_eq_adjoint,ContinuousLinearMap.adjoint_comp,
    ContinuousLinearMap.adjoint_adjoint]

theorem projection_commutes (V : E →ₗᵢ[ℂ] F) (A : E →L[ℂ] E) (B : F →L[ℂ] F)
    (h : B.comp V.toContinuousLinearMap=V.toContinuousLinearMap.comp A)
    (hs : (star B).comp V.toContinuousLinearMap=V.toContinuousLinearMap.comp (star A)) :
    B * projection V=projection V * B := by
  have hh := congrArg ContinuousLinearMap.adjoint hs
  simp only [ContinuousLinearMap.adjoint_comp,ContinuousLinearMap.star_eq_adjoint,
    ContinuousLinearMap.adjoint_adjoint] at hh
  ext1 x
  change B (V (V.toContinuousLinearMap.adjoint x)) =
    V (V.toContinuousLinearMap.adjoint (B x))
  have h1 := congrArg (fun T : E →L[ℂ] F => T (V.toContinuousLinearMap.adjoint x)) h
  have h2 := congrArg (fun T : F →L[ℂ] E => T x) hh
  exact h1.trans (congrArg V h2.symm)

theorem preserves_range_of_commutes (V : E →ₗᵢ[ℂ] F) (B : F →L[ℂ] F)
    (h : B * projection V=projection V * B) :
    Set.MapsTo B (Set.range V) (Set.range V) := by
  intro x hx
  apply (mem_range_iff V (B x)).mpr
  have hh := congrArg (fun T : F →L[ℂ] F => T x) h
  change B (projection V x)=projection V (B x) at hh
  rw [(mem_range_iff V x).mp hx] at hh
  exact hh.symm

end F1Fecho.IsometricReducingRange
#print axioms F1Fecho.IsometricReducingRange.projection_apply_image
#print axioms F1Fecho.IsometricReducingRange.mem_range_iff
#print axioms F1Fecho.IsometricReducingRange.projection_idem
#print axioms F1Fecho.IsometricReducingRange.projection_star
#print axioms F1Fecho.IsometricReducingRange.projection_commutes
#print axioms F1Fecho.IsometricReducingRange.preserves_range_of_commutes
