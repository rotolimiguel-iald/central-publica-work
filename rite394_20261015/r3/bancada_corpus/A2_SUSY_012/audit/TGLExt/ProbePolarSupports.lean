import TGLExt.V354BoundedPolar
set_option autoImplicit false
namespace TGLV354.Probes
noncomputable section
private theorem zeroPolar : boundedPolar (0 : ℂ →L[ℂ] ℂ)=0 := by
  ext x
  exact (boundedPolar_apply_eq_zero_iff _ _).mpr rfl

theorem zero_initial_is_zero :
    star (boundedPolar (0 : ℂ →L[ℂ] ℂ))*boundedPolar 0=0 := by
  rw [zeroPolar,star_zero,zero_mul]

/-- A formal counterexample to replacing the initial support by the identity. -/
theorem zero_initial_is_not_identity :
    star (boundedPolar (0 : ℂ →L[ℂ] ℂ))*boundedPolar 0 ≠ 1 := by
  rw [zero_initial_is_zero]
  exact zero_ne_one
#print axioms zero_initial_is_zero
#print axioms zero_initial_is_not_identity
end
end TGLV354.Probes
