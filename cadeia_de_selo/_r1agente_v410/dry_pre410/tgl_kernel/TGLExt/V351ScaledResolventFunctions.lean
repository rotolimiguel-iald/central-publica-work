import TGLExt.V351ResolventPhaseFunctions
import TGLExt.ModularFlowAlgebra

set_option autoImplicit false
set_option maxHeartbeats 1000000

namespace TGLV350.Regular
open ChatgptAudit
noncomputable section

def scaledResolventCoordinate (r x : ℝ) : ℝ := x/(r+(1-r)*x)
def scaledResolventDampingFactor (r x : ℝ) : ℝ := r/(r+(1-r)*x)^2

theorem scaledResolventDenominator_scalar_pos (r : ℝ) (hr : 0<r) (x : ℝ)
    (hx : x ∈ Set.Icc (0 : ℝ) 1) : 0<r+(1-r)*x := by
  by_cases h : x=1
  · simp [h]
  · have hh : 0<r*(1-x) := mul_pos hr (sub_pos.mpr (lt_of_le_of_ne hx.2 h))
    nlinarith [hx.1]

theorem scaledResolventCoordinate_complement (r x : ℝ) (hd : r+(1-r)*x ≠ 0) :
    1-scaledResolventCoordinate r x = r*(1-x)/(r+(1-r)*x) := by
  unfold scaledResolventCoordinate
  apply (eq_div_iff hd).mpr
  rw [sub_mul,one_mul,div_mul_cancel₀ _ hd]
  ring

theorem scaledResolventCoordinate_ratio (r x : ℝ) (hx : x≠0) (hd : r+(1-r)*x ≠ 0) :
    (1-scaledResolventCoordinate r x)/scaledResolventCoordinate r x = r*((1-x)/x) := by
  rw [scaledResolventCoordinate_complement r x hd]
  unfold scaledResolventCoordinate
  field_simp [hd,hx]
  have hd' : r+x*(1-r)≠0 := by simpa only [mul_comm] using hd
  exact mul_div_cancel_right₀ _ hd'

theorem scaledResolventCoordinate_damping (r x : ℝ) (hd : r+(1-r)*x ≠ 0) :
    resolventDamping (scaledResolventCoordinate r x)=
      resolventDamping x * scaledResolventDampingFactor r x := by
  unfold resolventDamping
  rw [scaledResolventCoordinate_complement r x hd]
  unfold scaledResolventCoordinate scaledResolventDampingFactor
  simp only [div_eq_mul_inv,← inv_pow]
  ring

theorem scaledResolventCoordinate_phase (r : ℝ) (hr : 0<r) (t x : ℝ)
    (hd : r+(1-r)*x ≠ 0) :
    resolventPhaseFunction t (scaledResolventCoordinate r x)=
      modularPhase t (Real.log r) * resolventPhaseFunction t x *
        (scaledResolventDampingFactor r x : ℂ) := by
  by_cases hx : x=0
  · subst x
    simp [scaledResolventCoordinate,resolventPhaseFunction,resolventDamping]
  by_cases h1 : x=1
  · subst x
    simp [scaledResolventCoordinate,resolventPhaseFunction,resolventDamping]
  have hl : Real.log ((1-scaledResolventCoordinate r x)/scaledResolventCoordinate r x)=
      Real.log r + Real.log ((1-x)/x) := by
    rw [scaledResolventCoordinate_ratio r x hx hd,
      Real.log_mul hr.ne' (div_ne_zero (sub_ne_zero.mpr (Ne.symm h1)) hx)]
  have hp : modularPhase t (Real.log r + Real.log ((1-x)/x)) =
      modularPhase t (Real.log r)*modularPhase t (Real.log ((1-x)/x)) := by
    simpa only [add_sub_cancel_right,sub_zero] using
      (modularPhase_cocycle t (Real.log r+Real.log ((1-x)/x)) (Real.log ((1-x)/x)) 0).symm
  unfold resolventPhaseFunction
  rw [scaledResolventCoordinate_damping r x hd,hl,hp]
  push_cast
  ring

#print axioms scaledResolventCoordinate
#print axioms scaledResolventDampingFactor
#print axioms scaledResolventDenominator_scalar_pos
#print axioms scaledResolventCoordinate_complement
#print axioms scaledResolventCoordinate_ratio
#print axioms scaledResolventCoordinate_damping
#print axioms scaledResolventCoordinate_phase
end
end TGLV350.Regular
