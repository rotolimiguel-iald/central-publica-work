import TGLExt.V354CyclicTraceCompletion

set_option autoImplicit false
open TGLV354.TraceCompletion TGLExt TGLV350.Regular TGLV351

/-- A concrete noncommuting pair: identifying cyclic readings never means
that the original products commute or are equal. -/
theorem related_products_are_not_equality :
    let x : Matrix (Fin 2) (Fin 2) ℝ := !![0,1;0,0]
    let y : Matrix (Fin 2) (Fin 2) ℝ := !![0,0;1,0]
    ShiftRelated (x*y) (y*x) ∧ x*y ≠ y*x := by
  dsimp
  refine ⟨ShiftRelated.cyclic _ _,?_⟩
  intro h
  have he := congrArg (fun m : Matrix (Fin 2) (Fin 2) ℝ => m 0 0) h
  norm_num [Matrix.mul_apply, Fin.sum_univ_two] at he

/-- Every actual positive nonzero input rules out the all-zero-reader shortcut. -/
theorem positive_reading_rejects_zero (P : SiteProfile) (p : PositiveCoreInput P)
    (hp : p ≠ PositiveCoreInput.zero P) :
    cyclicTraceCandidate P ⟨p.val,p.property.1⟩ ≠ 0 := by
  intro h
  exact hp ((cyclicTraceCandidate_positive_faithful P p).mp h)

#print axioms related_products_are_not_equality
#print axioms positive_reading_rejects_zero
