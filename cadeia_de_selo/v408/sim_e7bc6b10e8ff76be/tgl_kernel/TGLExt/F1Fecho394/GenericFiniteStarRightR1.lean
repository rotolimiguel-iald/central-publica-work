import TGLExt.F1Fecho394.RegularScalarWeightStarAlgebraR2
/-! Right products in the full finite-star domain, proved before specialization. -/
set_option autoImplicit false
noncomputable section
namespace F1Fecho.GenericFiniteStarRight
open TGLV350.Regular F1Fecho.RegularScalarGNS F1Fecho.RegularScalarWeightDomain
open F1Fecho.RegularScalarWeightStarAlgebra
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
variable (D : Context H)
def product (A : scalarWeightStarCore D) (b : D.algebra.toStarSubalgebra)
    (h : A.val*b ∈ scalarWeightLeftIdeal D) : scalarWeightStarCore D :=
  ⟨A.val*b,h,by
    change HasFiniteScalarSquare D (star (A.val.val*b.val))
    rw [star_mul]
    exact HasFiniteScalarSquare.left_mul D _ _ A.property.2⟩
theorem product_star (A : scalarWeightStarCore D) (b : D.algebra.toStarSubalgebra)
    (h : A.val*b ∈ scalarWeightLeftIdeal D) :
    (star (product D A b h)).val = star b * star A.val := star_mul A.val b
end F1Fecho.GenericFiniteStarRight
#print axioms F1Fecho.GenericFiniteStarRight.product
#print axioms F1Fecho.GenericFiniteStarRight.product_star
