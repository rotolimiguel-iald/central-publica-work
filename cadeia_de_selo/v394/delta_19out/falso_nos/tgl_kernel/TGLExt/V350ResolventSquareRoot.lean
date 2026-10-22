import TGLExt.V350PartialOperatorSquare
import Mathlib.Analysis.SpecialFunctions.ContinuousFunctionalCalculus.Rpow.Basic
import Mathlib.Analysis.CStarAlgebra.ContinuousFunctionalCalculus.Commute

set_option autoImplicit false
set_option maxHeartbeats 1800000

namespace TGLV350.Regular
open ChatgptAudit.Continuous049
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

theorem positive_sqrt_injective (R : H →L[ℂ] H) (hR : 0 ≤ R)
    (hi : Function.Injective R) : Function.Injective (CFC.sqrt R : H →L[ℂ] H) := by
  intro x y h
  apply hi
  have hh := congrArg (fun z : H => (CFC.sqrt R : H →L[ℂ] H) z) h
  change (CFC.sqrt R * CFC.sqrt R) x = (CFC.sqrt R * CFC.sqrt R) y at hh
  simpa only [CFC.sqrt_mul_sqrt_self R hR] using hh

theorem resolvent_sqrt_pair_commute (R : H →L[ℂ] H) :
    CFC.sqrt R * CFC.sqrt (1-R) = CFC.sqrt (1-R) * CFC.sqrt R := by
  have hc : Commute R (1-R) := resolvent_graph_commute R
  rw [CFC.sqrt_eq_cfc, CFC.sqrt_eq_cfc]
  exact ((hc.cfc_nnreal NNReal.sqrt).symm.cfc_nnreal NNReal.sqrt).symm

theorem resolvent_sqrt_pair_square_sum (R : H →L[ℂ] H) (hR : 0 ≤ R) (hone : R ≤ 1) :
    CFC.sqrt R * CFC.sqrt R + CFC.sqrt (1-R) * CFC.sqrt (1-R) = 1 := by
  rw [CFC.sqrt_mul_sqrt_self R hR, CFC.sqrt_mul_sqrt_self (1-R) (sub_nonneg.mpr hone)]
  abel

/-- A positive square root of the resolvent graph, constructed from bounded CFC roots. -/
def resolventSquareRoot (R : H →L[ℂ] H) (hR : 0 ≤ R) (hi : Function.Injective R) :
    H →ₗ.[ℂ] H := boundedGraphOperator (CFC.sqrt R) (CFC.sqrt (1-R))
      (positive_sqrt_injective R hR hi)

theorem resolventSquareRoot_domain (R : H →L[ℂ] H) (hR : 0 ≤ R)
    (hi : Function.Injective R) :
    (resolventSquareRoot R hR hi).domain = (CFC.sqrt R).range := rfl

theorem resolventSquareRoot_closed (R : H →L[ℂ] H) (hR : 0 ≤ R)
    (hi : Function.Injective R) (hone : R ≤ 1) :
    (resolventSquareRoot R hR hi).IsClosed :=
  bounded_graph_closed _ _ _ (resolvent_sqrt_pair_commute R)
    (resolvent_sqrt_pair_square_sum R hR hone)

theorem resolventSquareRoot_dense (R : H →L[ℂ] H) (hR : 0 ≤ R)
    (hi : Function.Injective R) : Dense ((resolventSquareRoot R hR hi).domain : Set H) :=
  bounded_graph_domain_dense _ _ _ (IsSelfAdjoint.of_nonneg (CFC.sqrt_nonneg R))

theorem resolventSquareRoot_formalAdjoint (R : H →L[ℂ] H) (hR : 0 ≤ R)
    (hi : Function.Injective R) :
    (resolventSquareRoot R hR hi).IsFormalAdjoint (resolventSquareRoot R hR hi) :=
  bounded_graph_formal_adjoint _ _ _ (IsSelfAdjoint.of_nonneg (CFC.sqrt_nonneg R))
    (IsSelfAdjoint.of_nonneg (CFC.sqrt_nonneg (1-R))) (resolvent_sqrt_pair_commute R)

theorem resolventSquareRoot_selfadjoint (R : H →L[ℂ] H) (hR : 0 ≤ R)
    (hi : Function.Injective R) (hone : R ≤ 1) :
    IsSelfAdjoint (resolventSquareRoot R hR hi) :=
  bounded_graph_selfadjoint _ _ _ (IsSelfAdjoint.of_nonneg (CFC.sqrt_nonneg R))
    (IsSelfAdjoint.of_nonneg (CFC.sqrt_nonneg (1-R)))
    (resolvent_sqrt_pair_commute R) (resolvent_sqrt_pair_square_sum R hR hone)

theorem resolventSquareRoot_positive (R : H →L[ℂ] H) (hR : 0 ≤ R)
    (hi : Function.Injective R) (x : (resolventSquareRoot R hR hi).domain) :
    0 ≤ (inner ℂ (x : H) (resolventSquareRoot R hR hi x)).re := by
  apply bounded_graph_positive (CFC.sqrt R) (CFC.sqrt (1-R)) _
  intro u
  have hp := (ContinuousLinearMap.nonneg_iff_isPositive _).mp (CFC.sqrt_nonneg R)
  have hprod : 0 ≤ CFC.sqrt R * CFC.sqrt (1-R) :=
    Commute.mul_nonneg (CFC.sqrt_nonneg R) (CFC.sqrt_nonneg (1-R))
      (show Commute (CFC.sqrt R) (CFC.sqrt (1-R)) from resolvent_sqrt_pair_commute R)
  rw [hp.inner_left_eq_inner_right]
  exact ((ContinuousLinearMap.nonneg_iff_isPositive _).mp hprod).re_inner_nonneg_right u

theorem resolventSquareRoot_square (R : H →L[ℂ] H) (hR : 0 ≤ R)
    (hi : Function.Injective R) (hone : R ≤ 1) :
    partialOperatorSquare (resolventSquareRoot R hR hi) = resolventGraphOperator R hi :=
  boundedGraph_square_eq_resolvent _ _ R _ hi (resolvent_sqrt_pair_commute R)
    (CFC.sqrt_mul_sqrt_self R hR) (CFC.sqrt_mul_sqrt_self (1-R) (sub_nonneg.mpr hone))

#print axioms positive_sqrt_injective
#print axioms resolvent_sqrt_pair_commute
#print axioms resolvent_sqrt_pair_square_sum
#print axioms resolventSquareRoot_domain
#print axioms resolventSquareRoot_closed
#print axioms resolventSquareRoot_dense
#print axioms resolventSquareRoot_formalAdjoint
#print axioms resolventSquareRoot_selfadjoint
#print axioms resolventSquareRoot_positive
#print axioms resolventSquareRoot_square
end
end TGLV350.Regular
