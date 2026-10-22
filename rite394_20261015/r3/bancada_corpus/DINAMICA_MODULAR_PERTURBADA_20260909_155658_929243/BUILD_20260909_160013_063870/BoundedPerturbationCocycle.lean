import UnitaryDuhamel

set_option autoImplicit false
set_option maxHeartbeats 1200000
namespace ChatgptAudit.BoundedPerturbation
open TGLExt Filter Topology Set ChatgptAudit.UnitaryDuhamel
noncomputable section

def innerAction {P : SiteProfile} (H : Operator P) (t : ℝ) (A : Operator P) : Operator P :=
  evolution H t * A * evolution H (-t)

def boundedCocycle {P : SiteProfile} (H V : Operator P) (t : ℝ) : Operator P :=
  evolution (H+V) t * evolution H (-t)

theorem inner_action_zero {P : SiteProfile} (H A : Operator P) :
    innerAction H 0 A = A := by simp [innerAction, evolution_zero]

theorem inner_action_group {P : SiteProfile} (H A : Operator P) (s t : ℝ) :
    innerAction H s (innerAction H t A) = innerAction H (s+t) A := by
  unfold innerAction
  rw [evolution_add H s t, show -(s+t) = -t + -s by ring, evolution_add]
  simp only [mul_assoc]

theorem inner_action_norm {P : SiteProfile} (H A : Operator P)
    (hH : IsSelfAdjoint H) (t : ℝ) : ‖innerAction H t A‖ = ‖A‖ := by
  unfold innerAction
  rw [CStarRing.norm_mul_mem_unitary _ (evolution_unitary H hH (-t)),
    CStarRing.norm_mem_unitary_mul _ (evolution_unitary H hH t)]

theorem bounded_cocycle_zero {P : SiteProfile} (H V : Operator P) :
    boundedCocycle H V 0 = 1 := by simp [boundedCocycle, evolution_zero]

theorem bounded_cocycle_no_perturbation {P : SiteProfile} (H : Operator P) (t : ℝ) :
    boundedCocycle H 0 t = 1 := by
  simpa only [boundedCocycle, add_zero] using evolution_mul_neg H t

theorem bounded_cocycle_unitary {P : SiteProfile} (H V : Operator P)
    (hH : IsSelfAdjoint H) (hV : IsSelfAdjoint V) (t : ℝ) :
    boundedCocycle H V t ∈ unitary _ :=
  (unitary _).mul_mem (evolution_unitary (H+V) (hH.add hV) t)
    (evolution_unitary H hH (-t))

theorem bounded_cocycle_continuous {P : SiteProfile} (H V : Operator P) :
    Continuous (boundedCocycle H V) := by
  exact (evolution_continuous (H+V)).mul
    ((evolution_continuous H).comp continuous_neg)

/-- The genuine twisted law; no modular-fixed or commutation premise. -/
theorem bounded_cocycle_twisted {P : SiteProfile} (H V : Operator P) (s t : ℝ) :
    boundedCocycle H V (s+t) =
      boundedCocycle H V s * innerAction H s (boundedCocycle H V t) := by
  calc
    boundedCocycle H V (s+t) =
        (evolution (H+V) s * evolution (H+V) t) *
          (evolution H (-t) * evolution H (-s)) := by
      unfold boundedCocycle
      rw [evolution_add, show -(s+t) = -t + -s by ring, evolution_add]
    _ = evolution (H+V) s * (evolution H (-s) * evolution H s) *
        evolution (H+V) t * evolution H (-t) * evolution H (-s) := by
      rw [evolution_neg_mul]
      simp only [mul_one, mul_assoc]
    _ = _ := by simp only [boundedCocycle, innerAction, mul_assoc]

theorem bounded_cocycle_derivative_explicit {P : SiteProfile}
    (H V : Operator P) (t : ℝ) :
    HasDerivAt (boundedCocycle H V)
      (evolution (H+V) t * (Complex.I • V) * evolution H (-t)) t := by
  have hc : HasDerivAt (fun z : ℝ => -z) (-1 : ℝ) t := (hasDerivAt_id t).neg
  have hneg := (evolution_derivative_left H (-t)).scomp t hc
  have hp := (evolution_derivative_right (H+V) t).mul hneg
  convert! hp using 1
  simp only [Function.comp_apply, neg_smul, one_smul, smul_add, mul_add, mul_neg]
  noncomm_ring

theorem bounded_cocycle_derivative_right {P : SiteProfile}
    (H V : Operator P) (t : ℝ) :
    HasDerivAt (boundedCocycle H V)
      (boundedCocycle H V t * innerAction H t (Complex.I • V)) t := by
  have he : boundedCocycle H V t * innerAction H t (Complex.I • V) =
      evolution (H+V) t * (Complex.I • V) * evolution H (-t) := by
    calc
      _ = evolution (H+V) t * (evolution H (-t) * evolution H t) *
          (Complex.I • V) * evolution H (-t) := by
        simp only [boundedCocycle, innerAction, mul_assoc]
      _ = _ := by rw [evolution_neg_mul, mul_one]
  rw [he]
  exact bounded_cocycle_derivative_explicit H V t

theorem bounded_cocycle_generator {P : SiteProfile} (H V : Operator P) :
    HasDerivAt (boundedCocycle H V) (Complex.I • V) 0 := by
  simpa only [bounded_cocycle_zero, inner_action_zero, one_mul] using
    bounded_cocycle_derivative_right H V 0

/-- Background-independent continuity with respect to a noncommuting potential. -/
theorem bounded_cocycle_perturbation_bound {P : SiteProfile} (H V W : Operator P)
    (hH : IsSelfAdjoint H) (hV : IsSelfAdjoint V) (hW : IsSelfAdjoint W) (t : ℝ) :
    ‖boundedCocycle H V t - boundedCocycle H W t‖ ≤ ‖V-W‖ * |t| := by
  have he : boundedCocycle H V t - boundedCocycle H W t =
      (evolution (H+V) t - evolution (H+W) t) * evolution H (-t) := by
    simp only [boundedCocycle, sub_mul]
  rw [he, CStarRing.norm_mul_mem_unitary _ (evolution_unitary H hH (-t))]
  have h := unitary_duhamel_bound (H+V) (H+W) (hH.add hV) (hH.add hW) t
  simpa only [add_sub_add_left_eq_sub] using h

theorem bounded_cocycle_distance_from_one {P : SiteProfile} (H V : Operator P)
    (hH : IsSelfAdjoint H) (hV : IsSelfAdjoint V) (t : ℝ) :
    ‖boundedCocycle H V t - 1‖ ≤ ‖V‖ * |t| := by
  simpa only [bounded_cocycle_no_perturbation, sub_zero] using
    bounded_cocycle_perturbation_bound H V 0 hH hV (by change star (0 : Operator P) = 0; simp) t

#print axioms innerAction
#print axioms boundedCocycle
#print axioms inner_action_zero
#print axioms inner_action_group
#print axioms inner_action_norm
#print axioms bounded_cocycle_zero
#print axioms bounded_cocycle_no_perturbation
#print axioms bounded_cocycle_unitary
#print axioms bounded_cocycle_continuous
#print axioms bounded_cocycle_twisted
#print axioms bounded_cocycle_derivative_explicit
#print axioms bounded_cocycle_derivative_right
#print axioms bounded_cocycle_generator
#print axioms bounded_cocycle_perturbation_bound
#print axioms bounded_cocycle_distance_from_one
end
end ChatgptAudit.BoundedPerturbation
