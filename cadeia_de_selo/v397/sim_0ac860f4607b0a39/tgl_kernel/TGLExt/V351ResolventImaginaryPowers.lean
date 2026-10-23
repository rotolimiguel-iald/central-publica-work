import TGLExt.V351ResolventPhaseCalculus

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1500000

namespace TGLV350.Regular
open Filter
open scoped Topology
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
variable (T : H →L[ℂ] H) (hT : 0 ≤ T) (h1 : T ≤ 1)
variable (hi : Function.Injective T) (hj : Function.Injective (1-T : H →L[ℂ] H))

include hi hj in
theorem resolventDampingOperator_injective : Function.Injective (resolventDampingOperator T) :=
  hi.comp hj

include hT h1 hi hj in
theorem resolventDampingOperator_denseRange : DenseRange (resolventDampingOperator T) :=
  ChatgptAudit.Continuous049.bounded_graph_domain_dense (resolventDampingOperator T) 0
    (resolventDampingOperator_injective T hi hj)
    (IsSelfAdjoint.of_nonneg (resolventDampingOperator_nonneg T hT h1))

include hT h1 hi hj in
theorem resolventPhaseOperator_denseRange (t : ℝ) : DenseRange (resolventPhaseOperator T t) := by
  have hd := resolventDampingOperator_denseRange T hT h1 hi hj
  have hdd := hd.comp hd (resolventDampingOperator T).continuous
  apply hdd.mono
  rintro _ ⟨x,rfl⟩
  refine ⟨resolventPhaseOperator T (-t) x,?_⟩
  have he := resolventPhaseOperator_mul T (IsSelfAdjoint.of_nonneg hT) t (-t)
  simp only [add_neg_cancel,resolventPhaseOperator_zero T (IsSelfAdjoint.of_nonneg hT)] at he
  exact congrArg (fun A : H →L[ℂ] H => A x) he

/-- The unitary determined by continuous calculus on a dense damped range.
It represents the imaginary power of the positive graph operator `(1-T)/T`. -/
def resolventImaginaryPower (t : ℝ) : H ≃ₗᵢ[ℂ] H :=
  denseLinearEquiv (resolventPhaseOperator T t).toLinearMap
    (resolventDampingOperator T).toLinearMap
    (resolventDampingOperator_denseRange T hT h1 hi hj)
    (resolventPhaseOperator_norm T hT h1 t)
    (resolventPhaseOperator_denseRange T hT h1 hi hj t)

theorem resolventImaginaryPower_damping (t : ℝ) (x : H) :
    resolventImaginaryPower T hT h1 hi hj t (resolventDampingOperator T x)=
      resolventPhaseOperator T t x :=
  denseLinearEquiv_apply _ _ _ _ _ x

theorem resolventImaginaryPower_zero (x : H) :
    resolventImaginaryPower T hT h1 hi hj 0 x = x := by
  refine (resolventDampingOperator_denseRange T hT h1 hi hj).induction ?_
    (isClosed_eq (by fun_prop) continuous_id) x
  rintro _ ⟨y,rfl⟩
  rw [resolventImaginaryPower_damping,resolventPhaseOperator_zero T (IsSelfAdjoint.of_nonneg hT)]

include hT in
theorem resolventPhaseOperator_commutes_damping (t : ℝ) :
    Commute (resolventPhaseOperator T t) (resolventDampingOperator T) := by
  change resolventPhaseOperator T t * resolventDampingOperator T = _
  have ha := resolventPhaseOperator_mul T (IsSelfAdjoint.of_nonneg hT) t 0
  simpa only [add_zero,resolventPhaseOperator_zero T (IsSelfAdjoint.of_nonneg hT)] using ha

theorem resolventImaginaryPower_commutes_damping (t : ℝ) (x : H) :
    resolventImaginaryPower T hT h1 hi hj t (resolventDampingOperator T x) =
      resolventDampingOperator T (resolventImaginaryPower T hT h1 hi hj t x) := by
  refine (resolventDampingOperator_denseRange T hT h1 hi hj).induction ?_
    (isClosed_eq (by fun_prop) (by fun_prop)) x
  rintro _ ⟨y,rfl⟩
  rw [resolventImaginaryPower_damping,resolventImaginaryPower_damping]
  exact congrArg (fun A : H →L[ℂ] H => A y)
    (resolventPhaseOperator_commutes_damping T hT t).eq

theorem resolventImaginaryPower_add (s t : ℝ) (x : H) :
    resolventImaginaryPower T hT h1 hi hj s
        (resolventImaginaryPower T hT h1 hi hj t x) =
      resolventImaginaryPower T hT h1 hi hj (s+t) x := by
  have hd := resolventDampingOperator_denseRange T hT h1 hi hj
  refine (hd.comp hd (resolventDampingOperator T).continuous).induction ?_
    (isClosed_eq (by fun_prop) (by fun_prop)) x
  rintro _ ⟨y,rfl⟩
  simp only [Function.comp_apply]
  change resolventImaginaryPower T hT h1 hi hj s
    (resolventImaginaryPower T hT h1 hi hj t
      (resolventDampingOperator T (resolventDampingOperator T y))) = _
  rw [resolventImaginaryPower_commutes_damping T hT h1 hi hj t,
    resolventImaginaryPower_damping]
  rw [resolventImaginaryPower_damping,resolventImaginaryPower_damping]
  exact congrArg (fun A : H →L[ℂ] H => A y)
    ((resolventPhaseOperator_mul T (IsSelfAdjoint.of_nonneg hT) s t).trans
      (resolventPhaseOperator_commutes_damping T hT (s+t)).eq.symm)

#print axioms resolventDampingOperator_injective
#print axioms resolventDampingOperator_denseRange
#print axioms resolventPhaseOperator_denseRange
#print axioms resolventImaginaryPower
#print axioms resolventImaginaryPower_damping
#print axioms resolventImaginaryPower_zero
#print axioms resolventPhaseOperator_commutes_damping
#print axioms resolventImaginaryPower_commutes_damping
#print axioms resolventImaginaryPower_add
end
end TGLV350.Regular
