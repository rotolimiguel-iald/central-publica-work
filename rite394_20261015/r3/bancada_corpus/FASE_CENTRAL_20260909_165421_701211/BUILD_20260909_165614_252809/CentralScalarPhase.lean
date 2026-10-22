import TGLExt.UnitaryDuhamel
import TGLExt.CanonicalCocycleDerivative
import Mathlib.Analysis.Complex.RealDeriv
import Mathlib.Analysis.SpecialFunctions.Pow.Complex

set_option autoImplicit false
set_option maxHeartbeats 1000000
namespace ChatgptAudit.CentralPhase
open TGLExt Filter Topology ChatgptAudit.UnitaryDuhamel ChatgptAudit.CocycleDerivative
noncomputable section

def scalarPhase (a t : ℝ) : ℂ := Complex.exp (((-t*a : ℝ) : ℂ)*Complex.I)

def shifted {P : SiteProfile} (u : ℝ → Operator P) (a t : ℝ) : Operator P :=
  scalarPhase a t • u t

def normalizedShift {P : SiteProfile} (u : ℝ → Operator P) (Z t : ℝ) : Operator P :=
  shifted u (Real.log Z) t

theorem scalar_phase_zero (a : ℝ) : scalarPhase a 0 = 1 := by simp [scalarPhase]

theorem scalar_phase_add (a s t : ℝ) :
    scalarPhase a (s+t) = scalarPhase a s * scalarPhase a t := by
  unfold scalarPhase
  rw [← Complex.exp_add]
  congr 1
  push_cast
  ring

theorem scalar_phase_star (a t : ℝ) :
    star (scalarPhase a t) = scalarPhase a (-t) := by
  unfold scalarPhase
  simp only [Complex.star_def,← Complex.exp_conj,map_mul,Complex.conj_ofReal,Complex.conj_I]
  congr 1
  push_cast
  ring

theorem scalar_phase_unitary (a t : ℝ) : scalarPhase a t ∈ unitary ℂ := by
  rw [Unitary.mem_iff,scalar_phase_star]
  constructor
  · rw [← scalar_phase_add,neg_add_cancel,scalar_phase_zero]
  · rw [← scalar_phase_add,add_neg_cancel,scalar_phase_zero]

theorem scalar_phase_continuous (a : ℝ) : Continuous (scalarPhase a) := by
  unfold scalarPhase
  fun_prop

theorem scalar_phase_derivative (a t : ℝ) :
    HasDerivAt (scalarPhase a)
      (scalarPhase a t * (-(a : ℂ)*Complex.I)) t := by
  have h := ((((hasDerivAt_id t).neg.mul_const a).ofReal_comp).mul_const Complex.I).cexp
  simpa only [scalarPhase,neg_mul,one_mul,Complex.ofReal_neg] using h

theorem shifted_zero {P : SiteProfile} (u : ℝ → Operator P) (a : ℝ)
    (h0 : u 0 = 1) : shifted u a 0 = 1 := by
  simp only [shifted,scalar_phase_zero,h0,one_smul]

theorem shifted_unitary {P : SiteProfile} (u : ℝ → Operator P) (a t : ℝ)
    (hu : u t ∈ unitary _) : shifted u a t ∈ unitary _ :=
  Unitary.smul_mem_of_mem (scalar_phase_unitary a t) hu

theorem shifted_continuous {P : SiteProfile} (u : ℝ → Operator P) (a : ℝ)
    (hu : Continuous u) : Continuous (shifted u a) :=
  (scalar_phase_continuous a).smul hu

theorem shifted_twisted (P : SiteProfile) (u : ℝ → Operator P) (a : ℝ)
    (hu : ∀ s t : ℝ, u (s+t) = u s * modularConjugation P s (u t)) (s t : ℝ) :
    shifted u a (s+t) =
      shifted u a s * modularConjugation P s (shifted u a t) := by
  simp only [shifted,scalar_phase_add,hu s t,map_smul,smul_mul_assoc,
    mul_smul_comm,smul_smul]
  rw [mul_comm (scalarPhase a s) (scalarPhase a t)]

theorem shifted_adjoint_action {P : SiteProfile} (u : ℝ → Operator P) (a t : ℝ)
    (A : Operator P) :
    shifted u a t * A * star (shifted u a t) = u t * A * star (u t) := by
  have h := (Unitary.mem_iff.mp (scalar_phase_unitary a t)).1
  simp only [shifted,star_smul,smul_mul_assoc,mul_smul_comm,smul_smul,h,one_smul]

theorem shifted_modular_action (P : SiteProfile) (u : ℝ → Operator P)
    (a t : ℝ) (A : Operator P) :
    shifted u a t * modularConjugation P t A * star (shifted u a t) =
      u t * modularConjugation P t A * star (u t) :=
  shifted_adjoint_action u a t _

theorem shifted_generator {P : SiteProfile} (u : ℝ → Operator P)
    (V : Operator P) (a : ℝ) (h0 : u 0 = 1)
    (hd : HasDerivAt u (Complex.I • V) 0) :
    HasDerivAt (shifted u a) (Complex.I • (V-(a : ℂ) • 1)) 0 := by
  have h := (scalar_phase_derivative a 0).smul hd
  have he : Complex.I • V + (-(a : ℂ)*Complex.I) • (1 : Operator P) =
      Complex.I • (V-(a : ℂ) • 1) := by
    simp only [smul_sub,smul_smul,neg_mul,neg_smul]
    rw [mul_comm (a : ℂ) Complex.I]
    abel
  simpa only [shifted,scalar_phase_zero,h0,one_mul,one_smul,he] using h

theorem shifted_generator_equation (P : SiteProfile) (u : ℝ → Operator P)
    (V : Operator P) (a : ℝ) (h0 : u 0 = 1)
    (hu : ∀ s t : ℝ, u (s+t) = u s * modularConjugation P s (u t))
    (hd : HasDerivAt u (Complex.I • V) 0) (t : ℝ) :
    HasDerivAt (shifted u a)
      (shifted u a t * (Complex.I • modularConjugation P t (V-(a : ℂ) • 1))) t :=
  canonical_cocycle_generator_equation P (shifted u a) (V-(a : ℂ) • 1)
    (shifted_twisted P u a hu) (shifted_generator u V a h0 hd) t

theorem scalar_phase_log_cpow (Z : ℝ) (hZ : 0 < Z) (t : ℝ) :
    scalarPhase (Real.log Z) t = (Z : ℂ)^(-(t : ℂ)*Complex.I) := by
  rw [Complex.cpow_def_of_ne_zero (Complex.ofReal_ne_zero.mpr (ne_of_gt hZ)),
    ← Complex.ofReal_log (le_of_lt hZ)]
  unfold scalarPhase
  congr 1
  push_cast
  ring

theorem normalized_shift_formula {P : SiteProfile} (u : ℝ → Operator P)
    (Z : ℝ) (hZ : 0 < Z) (t : ℝ) :
    normalizedShift u Z t = (Z : ℂ)^(-(t : ℂ)*Complex.I) • u t := by
  rw [normalizedShift,shifted,scalar_phase_log_cpow Z hZ t]

theorem normalized_shift_generator {P : SiteProfile} (u : ℝ → Operator P)
    (V : Operator P) (Z : ℝ) (h0 : u 0 = 1)
    (hd : HasDerivAt u (Complex.I • V) 0) :
    HasDerivAt (normalizedShift u Z)
      (Complex.I • (V-(Real.log Z : ℂ) • 1)) 0 :=
  shifted_generator u V (Real.log Z) h0 hd

theorem normalized_shift_modular_action (P : SiteProfile) (u : ℝ → Operator P)
    (Z t : ℝ) (A : Operator P) :
    normalizedShift u Z t * modularConjugation P t A * star (normalizedShift u Z t) =
      u t * modularConjugation P t A * star (u t) :=
  shifted_modular_action P u (Real.log Z) t A

#print axioms scalarPhase
#print axioms shifted
#print axioms normalizedShift
#print axioms scalar_phase_zero
#print axioms scalar_phase_add
#print axioms scalar_phase_star
#print axioms scalar_phase_unitary
#print axioms scalar_phase_continuous
#print axioms scalar_phase_derivative
#print axioms shifted_zero
#print axioms shifted_unitary
#print axioms shifted_continuous
#print axioms shifted_twisted
#print axioms shifted_adjoint_action
#print axioms shifted_modular_action
#print axioms shifted_generator
#print axioms shifted_generator_equation
#print axioms scalar_phase_log_cpow
#print axioms normalized_shift_formula
#print axioms normalized_shift_generator
#print axioms normalized_shift_modular_action
end
end ChatgptAudit.CentralPhase
