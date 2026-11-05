import TGLExt.V351ResolventPhaseFunctions
import TGLExt.V350BoundedInjectivePolar

set_option autoImplicit false
set_option maxHeartbeats 1500000

namespace TGLV350.Regular
open Filter
open scoped Topology
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

def resolventDampingOperator (T : H →L[ℂ] H) : H →L[ℂ] H := T*(1-T)

def resolventPhaseOperator (T : H →L[ℂ] H) (t : ℝ) : H →L[ℂ] H :=
  cfc (fun z : ℂ => resolventPhaseFunction t z.re) T

theorem resolventDampingOperator_cfc (T : H →L[ℂ] H) (hT : IsSelfAdjoint T) :
    cfc (fun z : ℂ => (resolventDamping z.re : ℂ)) T = resolventDampingOperator T := by
  rw [← cfc_real_eq_complex resolventDamping hT]
  unfold resolventDamping resolventDampingOperator
  rw [cfc_mul (fun x : ℝ => x) (fun x : ℝ => 1-x) T (by fun_prop) (by fun_prop),
    cfc_sub (fun _ : ℝ => 1) (fun x : ℝ => x) T (by fun_prop) (by fun_prop)]
  rw [cfc_id' ℝ T hT,cfc_const (1 : ℝ) T hT,map_one]

theorem resolventDampingOperator_nonneg (T : H →L[ℂ] H) (hT : 0 ≤ T) (h1 : T ≤ 1) :
    0 ≤ resolventDampingOperator T :=
  Commute.mul_nonneg hT (sub_nonneg.mpr h1)
    (complement_commutes_of_commute T T (Commute.refl T)).symm

theorem resolventPhaseOperator_zero (T : H →L[ℂ] H) (hT : IsSelfAdjoint T) :
    resolventPhaseOperator T 0 = resolventDampingOperator T := by
  unfold resolventPhaseOperator
  simp only [resolventPhaseFunction_zero_time]
  exact resolventDampingOperator_cfc T hT

theorem resolventPhaseOperator_star (T : H →L[ℂ] H) (t : ℝ) :
    star (resolventPhaseOperator T t) = resolventPhaseOperator T (-t) := by
  unfold resolventPhaseOperator
  rw [← cfc_star]
  simp only [resolventPhaseFunction_star]

theorem resolventPhaseOperator_mul (T : H →L[ℂ] H) (hT : IsSelfAdjoint T) (s t : ℝ) :
    resolventPhaseOperator T s * resolventPhaseOperator T t =
      resolventDampingOperator T * resolventPhaseOperator T (s+t) := by
  have hc (u : ℝ) : Continuous (fun z : ℂ => resolventPhaseFunction u z.re) :=
    (resolventPhaseFunction_continuous u).comp Complex.continuous_re
  unfold resolventPhaseOperator
  rw [← cfc_mul _ _ T (hc s).continuousOn (hc t).continuousOn]
  simp only [resolventPhaseFunction_add]
  rw [cfc_mul _ _ T (by unfold resolventDamping; fun_prop) (hc (s+t)).continuousOn]
  rw [resolventDampingOperator_cfc T hT]

theorem resolventPhaseOperator_gram (T : H →L[ℂ] H) (hT : IsSelfAdjoint T) (t : ℝ) :
    star (resolventPhaseOperator T t) * resolventPhaseOperator T t =
      resolventDampingOperator T * resolventDampingOperator T := by
  rw [resolventPhaseOperator_star,resolventPhaseOperator_mul T hT,neg_add_cancel,
    resolventPhaseOperator_zero T hT]

theorem resolventPhaseOperator_modulus (T : H →L[ℂ] H) (hT : 0 ≤ T) (h1 : T ≤ 1) (t : ℝ) :
    boundedMapModulus (resolventPhaseOperator T t) = resolventDampingOperator T := by
  unfold boundedMapModulus
  change CFC.sqrt (star (resolventPhaseOperator T t) * resolventPhaseOperator T t)=_
  rw [resolventPhaseOperator_gram T (IsSelfAdjoint.of_nonneg hT),
    CFC.sqrt_mul_self _ (resolventDampingOperator_nonneg T hT h1)]

theorem resolventPhaseOperator_norm (T : H →L[ℂ] H) (hT : 0 ≤ T) (h1 : T ≤ 1)
    (t : ℝ) (x : H) : ‖resolventPhaseOperator T t x‖ = ‖resolventDampingOperator T x‖ := by
  rw [← resolventPhaseOperator_modulus T hT h1 t]
  exact (boundedMapModulus_norm _ x).symm

#print axioms resolventDampingOperator
#print axioms resolventPhaseOperator
#print axioms resolventDampingOperator_cfc
#print axioms resolventDampingOperator_nonneg
#print axioms resolventPhaseOperator_zero
#print axioms resolventPhaseOperator_star
#print axioms resolventPhaseOperator_mul
#print axioms resolventPhaseOperator_gram
#print axioms resolventPhaseOperator_modulus
#print axioms resolventPhaseOperator_norm
end
end TGLV350.Regular
