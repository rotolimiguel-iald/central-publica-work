import TGLExt.Cocycle
import Mathlib.Analysis.InnerProductSpace.LinearMap
import Mathlib.Analysis.Normed.Module.Normalize
import Mathlib.Analysis.SpecialFunctions.Exponential

set_option autoImplicit false
set_option maxHeartbeats 800000

namespace ModularRemainderDensity
open Matrix NormedSpace TGLExt
open scoped ComplexOrder MatrixOrder Matrix.Norms.L2Operator
noncomputable section

variable {n : Type} [Fintype n] [DecidableEq n]

/-- Regulated remainder, with reference and vacuum densities specified. -/
def remainder (rho reference : Matrix n n ℂ) : Matrix n n ℂ :=
  logRho reference - logRho rho

theorem remainder_isSelfAdjoint (rho reference : Matrix n n ℂ) :
    IsSelfAdjoint (remainder rho reference) :=
  (logRho_isSelfAdjoint reference).sub (logRho_isSelfAdjoint rho)

theorem modular_generator_decomposition (rho reference : Matrix n n ℂ) :
    -logRho rho = -logRho reference + remainder rho reference := by
  unfold remainder
  abel

/-- Faithfulness makes equality of logarithms imply equality of states. -/
theorem remainder_zero_iff (rho reference : Matrix n n ℂ)
    (hrho : rho.PosDef) (href : reference.PosDef) :
    remainder rho reference = 0 ↔ rho = reference := by
  constructor
  · intro h
    have he : logRho reference = logRho rho := sub_eq_zero.mp h
    have hh := congrArg NormedSpace.exp he
    simpa only [exp_logRho _ hrho, exp_logRho _ href] using hh.symm
  · rintro rfl
    exact sub_self _

/-- Reference dependence is explicit; there is no unique remainder before
choosing the candidate geometric reference. -/
theorem remainder_change_reference (rho a b : Matrix n n ℂ) :
    remainder rho b - remainder rho a = logRho b - logRho a := by
  unfold remainder
  abel

theorem remainder_antisymmetric (rho reference : Matrix n n ℂ) :
    remainder reference rho = -remainder rho reference := by
  unfold remainder
  abel

/-- Intertwining of the actual matrix flows, without a commutativity premise. -/
theorem cocycle_intertwines (rho reference x : Matrix n n ℂ) (t : ℝ) :
    cocycle rho reference t * sigma reference t x *
      (cocycle rho reference t)ᴴ = sigma rho t x := by
  rw [cocycle_conjTranspose]
  simp only [cocycle, sigma]
  calc
    _ = modPow rho t * ((modPow reference (-t) * modPow reference t) * x *
      (modPow reference (-t) * modPow reference t)) * modPow rho (-t) := by
        noncomm_ring
    _ = _ := by rw [modPow_neg_mul]; simp

/-- Differentiation of the existing modular power, in its real time parameter. -/
theorem modular_power_derivative (rho : Matrix n n ℂ) (t : ℝ) :
    HasDerivAt (modPow rho)
      (modPow rho t * (Complex.I • logRho rho)) t := by
  have h := hasDerivAt_exp_smul_const (Complex.I • logRho rho) t
  have he : (fun r : ℝ => NormedSpace.exp (r • (Complex.I • logRho rho))) =
      modPow rho := by
    funext r
    rw [← smul_assoc, Complex.real_smul]
    rfl
  rw [he, congrFun he t] at h
  exact h

/-- The relative modular correction is i times the derivative of the actual
cocycle at zero; no commuting-density hypothesis is used. -/
theorem cocycle_derivative_remainder (rho reference : Matrix n n ℂ) :
    HasDerivAt (cocycle rho reference)
      ((-Complex.I) • remainder rho reference) 0 := by
  have hn := (modular_power_derivative reference (-(0 : ℝ))).scomp (0 : ℝ)
    (hasDerivAt_id (0 : ℝ)).neg
  have hp := (modular_power_derivative rho 0).mul hn
  convert! hp using 1
  simp only [Function.comp_apply, neg_zero, modPow_zero, one_mul, mul_one,
    neg_smul, one_smul, remainder, smul_sub]
  abel

/-- Exact Gibbs normalization for any positive normalizing scalar. Choosing Z
as the partition function gives the normalized reference density. -/
theorem gibbs_reference_log (Q : Matrix n n ℂ) (hQ : IsSelfAdjoint Q)
    (Z : ℝ) (hZ : 0 < Z) :
    -logRho (Z⁻¹ • NormedSpace.exp (-Q)) =
      Q + (Real.log Z) • (1 : Matrix n n ℂ) := by
  have he : IsStrictlyPositive (NormedSpace.exp (-Q)) := by
    rw [← CFC.real_exp_eq_normedSpace_exp hQ.neg]
    exact (cfc_isStrictlyPositive_iff Real.exp (-Q)).mpr (fun x _ => Real.exp_pos x)
  change -CFC.log (Z⁻¹ • NormedSpace.exp (-Q)) = _
  rw [CFC.log_smul' _ (inv_pos.mpr hZ) he, CFC.log_exp _ hQ.neg, Real.log_inv]
  simp only [map_neg, Algebra.algebraMap_eq_smul_one, neg_add_rev, neg_neg]

def entropy (rho : Matrix n n ℂ) : ℂ := -trace (rho * logRho rho)
def relativeEntropy (rho reference : Matrix n n ℂ) : ℂ :=
  trace (rho * (logRho rho - logRho reference))

/-- Exact noncommuting matrix entropy balance. Positivity is not needed for
this algebraic identity, but is needed for the entropy interpretation. -/
theorem relative_entropy_balance (rho reference : Matrix n n ℂ) :
    relativeEntropy rho reference =
      trace ((rho-reference)*(-logRho reference)) -
        (entropy rho - entropy reference) := by
  simp only [relativeEntropy, entropy, mul_sub, sub_mul, mul_neg,
    trace_sub, trace_neg]
  ring

/-- Scalar normalization cancels in expectation differences of normalized states. -/
theorem scalar_normalization_cancels (rho reference : Matrix n n ℂ) (c : ℂ)
    (hrho : trace rho = 1) (href : trace reference = 1) :
    trace ((rho-reference)*(c • (1 : Matrix n n ℂ))) = 0 := by
  simp only [mul_smul_comm, mul_one, trace_smul, trace_sub, hrho, href, sub_self,
    smul_zero]

theorem residual_entropy_balance (rho vacuum Q : Matrix n n ℂ) (c : ℂ)
    (hrho : trace rho = 1) (hvac : trace vacuum = 1) :
    trace ((rho-vacuum)*(-logRho vacuum-Q-c • (1 : Matrix n n ℂ))) =
      relativeEntropy rho vacuum + (entropy rho-entropy vacuum) -
        trace ((rho-vacuum)*Q) := by
  rw [relative_entropy_balance, mul_sub, mul_sub, trace_sub, trace_sub,
    scalar_normalization_cancels rho vacuum c hrho hvac]
  ring

section Expectations
variable {H : Type*} [NormedAddCommGroup H] [InnerProductSpace ℂ H]

/-- Polarization criterion, valid even without finite dimension. The scalar is
real because it is an expectation of a selfadjoint remainder in the application.
Testing all quadratic forms is essential; a single vacuum vector does not suffice. -/
theorem all_quadratic_forms_constant_iff (R : H →ₗ[ℂ] H) (c : ℝ) :
    (∀ v : H, inner ℂ (R v) v = (c : ℂ) * inner ℂ v v) ↔
      R = (c : ℂ) • LinearMap.id := by
  rw [← ext_inner_map]
  constructor <;> intro h v <;>
    simpa only [LinearMap.smul_apply, LinearMap.id_apply, inner_smul_left,
      Complex.conj_ofReal] using h v

/-- It suffices to test unit vectors, i.e. pure normalized vector states. -/
theorem all_unit_expectations_constant_iff (R : H →ₗ[ℂ] H) (c : ℝ) :
    (∀ v : H, ‖v‖=1 → inner ℂ (R v) v=(c : ℂ)) ↔
      R=(c : ℂ) • LinearMap.id := by
  constructor
  · intro h
    apply (all_quadratic_forms_constant_iff R c).mp
    intro v
    by_cases hv : v=0
    · simp [hv]
    have hw := h (NormedSpace.normalize v) (NormedSpace.norm_normalize hv)
    have he : (‖v‖ : ℂ) • NormedSpace.normalize v=v := by
      simpa only [Complex.coe_smul] using NormedSpace.norm_smul_normalize v
    have hinner : inner ℂ (R v) v=(‖v‖ : ℂ)*(‖v‖ : ℂ)*(c : ℂ) := by
      calc
        _ = inner ℂ (R ((‖v‖ : ℂ) • NormedSpace.normalize v))
              ((‖v‖ : ℂ) • NormedSpace.normalize v) := by rw [he]
        _ = _ := by simp only [map_smul, inner_smul_left, inner_smul_right,
              Complex.conj_ofReal, hw]; ring
    rw [hinner, inner_self_eq_norm_sq_to_K]
    change (‖v‖ : ℂ)*(‖v‖ : ℂ)*(c : ℂ)=(c : ℂ)*(‖v‖ : ℂ)^2
    ring
  · rintro rfl v hv
    simp [inner_self_eq_norm_sq_to_K, hv]

end Expectations

#print axioms remainder_isSelfAdjoint
#print axioms modular_generator_decomposition
#print axioms remainder_zero_iff
#print axioms remainder_change_reference
#print axioms remainder_antisymmetric
#print axioms cocycle_intertwines
#print axioms modular_power_derivative
#print axioms cocycle_derivative_remainder
#print axioms gibbs_reference_log
#print axioms relative_entropy_balance
#print axioms scalar_normalization_cancels
#print axioms residual_entropy_balance
#print axioms all_quadratic_forms_constant_iff
#print axioms all_unit_expectations_constant_iff
end
end ModularRemainderDensity
