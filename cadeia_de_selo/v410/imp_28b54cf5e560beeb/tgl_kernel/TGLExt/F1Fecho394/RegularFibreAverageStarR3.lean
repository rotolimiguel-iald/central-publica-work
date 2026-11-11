import TGLExt.F1Fecho394.RegularAverageAdjointR4
import TGLExt.F1Fecho394.RegularFiniteFibreRightR3
import TGLExt.F1Fecho394.RegularCoreFiniteWeightR3
/-! Finite adjunction pairs with base coefficients in the same regular core.
Their existence will supply the interval graph core; no modular identity is assumed. -/
set_option autoImplicit false
set_option maxHeartbeats 1000000
noncomputable section
namespace F1Fecho.RegularFibreAverageStar
open TGLV350.Regular F1Fecho.RegularCovariantCore
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

theorem fibre_average_star (B : UnitaryFlow H) (A : H→L[ℂ]H) (h : ℝ) :
    star (fibre A*RegularCoreAverage.regularAverage B h)=
      regularUnitary B (-h)*(RegularCoreAverage.regularAverage B h*fibre (star A)) := by
  rw [star_mul,RegularAverageAdjoint.regularAverage_star,←fibre_star,mul_assoc]

theorem fibre_average_finite (B : UnitaryFlow H) (A : H→L[ℂ]H)
    (h : ℝ) (hh : 0<h) :
    HasFiniteDualSquare (fibre A*RegularCoreAverage.regularAverage B h) ∧
      HasFiniteDualSquare (star (fibre A*RegularCoreAverage.regularAverage B h)) := by
  constructor
  · exact HasFiniteDualSquare.left_mul _ _
      (RegularCoreFiniteWeight.regularAverage_hasFiniteDualSquare B h hh)
  · rw [fibre_average_star]
    exact HasFiniteDualSquare.left_mul _ _
      (RegularFiniteFibreRight.right_fibre _
        (RegularCoreFiniteWeight.regularAverage_hasFiniteDualSquare B h hh) (star A))

theorem fibre_average_mem (B : UnitaryFlow H) (M : VonNeumannAlgebra H)
    (A : H→L[ℂ]H) (hA : A∈M) (h : ℝ) :
    fibre A*RegularCoreAverage.regularAverage B h∈core B M :=
  (core B M).mul_mem (fibre_mem B M A hA) (RegularCoreAverage.regularAverage_mem B M h)

end F1Fecho.RegularFibreAverageStar
#print axioms F1Fecho.RegularFibreAverageStar.fibre_average_star
#print axioms F1Fecho.RegularFibreAverageStar.fibre_average_finite
#print axioms F1Fecho.RegularFibreAverageStar.fibre_average_mem
