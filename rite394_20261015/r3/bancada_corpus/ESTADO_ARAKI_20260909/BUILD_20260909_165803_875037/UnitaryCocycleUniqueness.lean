import UnitaryDuhamel
import CanonicalCocycleDerivative
import Mathlib.Analysis.Calculus.Deriv.Star
import Mathlib.Analysis.Calculus.MeanValue

set_option autoImplicit false
set_option maxHeartbeats 1000000
namespace ChatgptAudit.CocycleUniqueness
open TGLExt ChatgptAudit.UnitaryDuhamel ChatgptAudit.CocycleDerivative
noncomputable section

theorem same_generator_product_derivative (P : SiteProfile)
    (u v A : ℝ → Operator P) (hA : ∀ t, star (A t) = -A t)
    (hu : ∀ t, HasDerivAt u (u t * A t) t)
    (hv : ∀ t, HasDerivAt v (v t * A t) t) (t : ℝ) :
    HasDerivAt (fun s => u s * star (v s)) 0 t := by
  have hd := (hu t).mul ((hv t).star)
  convert! hd using 1 <;>
+    simp only [star_mul, hA t, neg_mul, mul_neg, mul_assoc, add_neg_cancel]

theorem same_generator_product_constant (P : SiteProfile)
    (u v A : ℝ → Operator P) (hA : ∀ t, star (A t) = -A t)
    (hu : ∀ t, HasDerivAt u (u t * A t) t)
    (hv : ∀ t, HasDerivAt v (v t * A t) t) (t : ℝ) :
    u t * star (v t) = u 0 * star (v 0) := by
  have hd := same_generator_product_derivative P u v A hA hu hv
  exact is_const_of_deriv_eq_zero (fun s => (hd s).differentiableAt)
    (fun s => (hd s).deriv) t 0

theorem unitary_right_generator_unique (P : SiteProfile)
    (u v A : ℝ → Operator P) (hA : ∀ t, star (A t) = -A t)
    (hu : ∀ t, HasDerivAt u (u t * A t) t)
    (hv : ∀ t, HasDerivAt v (v t * A t) t)
    (hu0 : u 0 = 1) (hv0 : v 0 = 1)
    (hvu : ∀ t, v t ∈ unitary _) : u = v := by
  funext t
  have he := same_generator_product_constant P u v A hA hu hv t
  rw [hu0, hv0, star_one, mul_one] at he
  have hc := congrArg (fun B : Operator P => B * v t) he
  simpa only [mul_assoc, Unitary.star_mul_self_of_mem (hvu t), mul_one,
    one_mul] using hc

theorem canonical_generator_skew (P : SiteProfile) (V : Operator P)
    (hV : IsSelfAdjoint V) (t : ℝ) :
    star (Complex.I • modularConjugation P t V) =
      -(Complex.I • modularConjugation P t V) := by
  rw [star_smul, ← map_star, hV.star_eq]
  simp only [Complex.star_def, Complex.conj_I, neg_smul]

theorem canonical_right_generator_unique (P : SiteProfile)
    (u v : ℝ → Operator P) (V : Operator P) (hV : IsSelfAdjoint V)
    (hu : ∀ t, HasDerivAt u (u t * (Complex.I • modularConjugation P t V)) t)
    (hv : ∀ t, HasDerivAt v (v t * (Complex.I • modularConjugation P t V)) t)
    (hu0 : u 0 = 1) (hv0 : v 0 = 1)
    (hvu : ∀ t, v t ∈ unitary _) : u = v :=
  unitary_right_generator_unique P u v _ (canonical_generator_skew P V hV)
    hu hv hu0 hv0 hvu

theorem canonical_cocycle_unique_from_derivative (P : SiteProfile)
    (u v : ℝ → Operator P) (V : Operator P) (hV : IsSelfAdjoint V)
    (huc : ∀ s t, u (s+t) = u s * modularConjugation P s (u t))
    (hvc : ∀ s t, v (s+t) = v s * modularConjugation P s (v t))
    (hud : HasDerivAt u (Complex.I • V) 0)
    (hvd : HasDerivAt v (Complex.I • V) 0)
    (hu0 : u 0 = 1) (hv0 : v 0 = 1)
    (hvu : ∀ t, v t ∈ unitary _) : u = v :=
  canonical_right_generator_unique P u v V hV
    (canonical_cocycle_generator_equation P u V huc hud)
    (canonical_cocycle_generator_equation P v V hvc hvd) hu0 hv0 hvu

#print axioms same_generator_product_derivative
#print axioms same_generator_product_constant
#print axioms unitary_right_generator_unique
#print axioms canonical_generator_skew
#print axioms canonical_right_generator_unique
#print axioms canonical_cocycle_unique_from_derivative
end
end ChatgptAudit.CocycleUniqueness
