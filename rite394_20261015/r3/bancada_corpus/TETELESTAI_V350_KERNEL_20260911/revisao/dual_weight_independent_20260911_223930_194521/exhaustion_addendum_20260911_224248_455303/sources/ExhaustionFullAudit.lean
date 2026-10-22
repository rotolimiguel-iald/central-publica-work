import TGLV350.DualWeightExhaustion
set_option pp.universes true in
#check TGLV350.Regular.lintegral_eq_iSup_symmetric_cuts
#print axioms TGLV350.Regular.lintegral_eq_iSup_symmetric_cuts
set_option pp.universes true in
#check TGLV350.Regular.dualQuadraticIntegral_eq_iSup_cuts
#print axioms TGLV350.Regular.dualQuadraticIntegral_eq_iSup_cuts
set_option pp.universes true in
#check TGLV350.Regular.dual_unit_cut_supremum_infinite
#print axioms TGLV350.Regular.dual_unit_cut_supremum_infinite

set_option autoImplicit false
open MeasureTheory TGLV350.Regular TGLV350.StrongIntegral
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

-- Coercion of the restricted action gives the very same integrand, on the whole algebra.
example (P : TGLExt.SiteProfile) (A : (regularCoreAlgebra P).toStarSubalgebra)
    (R : ℝ) (v : RegularHilbert (TGLExt.TowerHilbert P)) :
    dualWeightCut R A.val v = ∫ s in (-R)..R,
      ((regularDualAction P s A).val : RegularHilbert (TGLExt.TowerHilbert P) →L[ℂ]
        RegularHilbert (TGLExt.TowerHilbert P)) v := rfl

-- Fixed Haar factor, without division by the growing interval length.
example (R : ℝ) (A : RegularHilbert H →L[ℂ] RegularHilbert H) :
    normalizedDualCut R A = ((2 * Real.pi)⁻¹ : ℝ) • dualWeightCut R A := rfl

-- The integral in operatorIntegral_apply has Hilbert vectors as values.
example (F : Family (H := H)) (a b : ℝ) (v : H) :
    operatorIntegral F a b v = (∫ t in a..b, F.op t v : H) := rfl
end
