import TGLExt.F1Fecho394.RegularScalarGNSRepresentationR2
/-! Injectivity of a concrete operator survives the actual dual-orbit GNS representation. This reuses the coordinate proof incorporated in v393 and does not assume injectivity of an abstract representation on vectors. -/
set_option autoImplicit false
set_option maxHeartbeats 1200000
noncomputable section
namespace F1Fecho.RegularScalarGNSRepresentation
open TGLV350.Regular MeasureTheory Filter
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
theorem representation_vector_injective (D : F1Fecho.RegularScalarGNS.Context H)
    (a : D.algebra.toStarSubalgebra) (ha : Function.Injective a.val) :
    Function.Injective (scalarGNSRepresentation D a) := by
  have hi (s : ℝ) : Function.Injective (dualAmbient s a.val) := by
    rw [dualAmbient_apply, characterMultiplier_star]
    exact (characterMultiplierIsometry s).injective.comp
      (ha.comp (characterMultiplierIsometry (-s)).injective)
  intro x y h
  have he : operatorFieldLift (dualIntegralFamily a.val) x.val =
      operatorFieldLift (dualIntegralFamily a.val) y.val := congrArg Subtype.val h
  apply Subtype.ext
  apply Lp.ext
  filter_upwards [operatorFieldLift_ae (dualIntegralFamily a.val) x.val,
    operatorFieldLift_ae (dualIntegralFamily a.val) y.val] with s hx hy
  apply hi s
  exact hx.symm.trans ((congrArg (fun f : RegularHilbert (RegularHilbert H) => f s) he).trans hy)


end F1Fecho.RegularScalarGNSRepresentation
#print axioms F1Fecho.RegularScalarGNSRepresentation.representation_vector_injective
