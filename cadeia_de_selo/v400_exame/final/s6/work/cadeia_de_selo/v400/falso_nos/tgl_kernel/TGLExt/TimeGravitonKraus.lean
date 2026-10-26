import TGLExt.TimeGravitonFlow

/-! Explicit finite Kraus witness for nonnegative rates and times.
The certificate consists of the action as a Kraus sum and sum K* K = I.
These are exact matrix equalities, not a sampled Choi test. -/
set_option autoImplicit false
set_option maxHeartbeats 1600000
namespace TGLExt.TimeGravitonFlow
open Matrix Complex TimeGravitonMatrix
noncomputable section

def phase (theta : ℝ) : ℂ := Complex.exp ((theta : ℂ)*Complex.I)

theorem phase_star (theta : ℝ) : star (phase theta) = phase (-theta) := by
  unfold phase
  rw [Complex.star_def, ← Complex.exp_conj]
  congr 1
  simp

theorem phase_mul (theta phi : ℝ) : phase theta * phase phi = phase (theta+phi) := by
  unfold phase
  rw [← Complex.exp_add]
  congr 1
  push_cast
  ring

@[simp] theorem phase_zero : phase 0 = 1 := by simp [phase]

def unitary (theta : ℝ) : M2 := phase theta • projPlus + phase (-theta) • projMinus

theorem unitary_eq_angFamily (theta : ℝ) : unitary theta = angFamily theta := by
  rw [the_angle_is_the_projection]
  simp [unitary, phase]

theorem unitary_star (theta : ℝ) : star (unitary theta) = unitary (-theta) := by
  simp [unitary, star_add, star_smul, IALDGraviton.projPlus_star, projMinus_star,
    phase_star]

theorem unitary_normalization (theta : ℝ) : star (unitary theta)*unitary theta = 1 := by
  rw [unitary_star]
  simp only [unitary, add_mul, mul_add, smul_mul_assoc, mul_smul_comm, smul_smul,
    spectral_projections_are_idempotent.1, spectral_projections_are_idempotent.2,
    spectral_projections_split_the_identity.2, pm_orthogonal, smul_zero, add_zero, zero_add,
    phase_mul, neg_add_cancel, neg_neg, add_neg_cancel, phase_zero, one_smul]
  exact spectral_projections_split_the_identity.1

theorem unitary_action (theta : ℝ) (X : M2) :
    unitary theta * X * star (unitary theta) =
      Eg X + phase (2*theta) • blockPM X + phase (-2*theta) • blockMP X := by
  rw [unitary_star]
  simp only [unitary, add_mul, mul_add, smul_mul_assoc, mul_smul_comm, smul_add, smul_smul,
    phase_mul, neg_neg, add_neg_cancel, neg_add_cancel, phase_zero, one_smul]
  have hp : theta+theta = 2*theta := by ring
  have hm : -theta + -theta = -2*theta := by ring
  rw [hp, hm]
  simp only [Eg_apply, blockPM_apply, blockMP_apply]
  abel

theorem mode_decay_phase (rate frequency time : ℝ) :
    mode rate frequency time = (Real.exp (-(rate*time)) : ℂ) * phase (frequency*time) := by
  rw [mode_eq_spin]
  rfl

def decay (rate time : ℝ) : ℝ := Real.exp (-(rate*time))

theorem flow_convex_unitary_pinching (rate omega time : ℝ) (X : M2) :
    flow rate omega time X = (decay rate time : ℂ) •
      (unitary (omega*time)*X*star (unitary (omega*time))) +
      (1-(decay rate time : ℂ)) • Eg X := by
  rw [unitary_action, flow_apply]
  simp only [mode_decay_phase, decay]
  have hp : 2*omega*time = 2*(omega*time) := by ring
  have hm : -2*omega*time = -2*(omega*time) := by ring
  rw [hp, hm]
  module

theorem decay_range (rate time : ℝ) (hr : 0 ≤ rate) (ht : 0 ≤ time) :
    0 ≤ decay rate time ∧ decay rate time ≤ 1 := by
  constructor
  · exact le_of_lt (Real.exp_pos _)
  · unfold decay
    exact Real.exp_le_one_iff.mpr (neg_nonpos.mpr (mul_nonneg hr ht))

def kraus0 (rate omega time : ℝ) : M2 :=
  (Real.sqrt (decay rate time) : ℂ) • unitary (omega*time)
def kraus1 (rate time : ℝ) : M2 :=
  (Real.sqrt (1-decay rate time) : ℂ) • projPlus
def kraus2 (rate time : ℝ) : M2 :=
  (Real.sqrt (1-decay rate time) : ℂ) • projMinus

theorem sqrt_sandwich (a : ℝ) (ha : 0 ≤ a) (K X : M2) :
    ((Real.sqrt a : ℂ) • K)*X*star ((Real.sqrt a : ℂ) • K) =
      (a : ℂ) • (K*X*star K) := by
  simp only [star_smul, Complex.star_def, Complex.conj_ofReal, smul_mul_assoc,
    mul_smul_comm, smul_smul]
  rw [← Complex.ofReal_mul, Real.mul_self_sqrt ha]

theorem sqrt_normalization (a : ℝ) (ha : 0 ≤ a) (K : M2) :
    star ((Real.sqrt a : ℂ) • K)*((Real.sqrt a : ℂ) • K) =
      (a : ℂ) • (star K*K) := by
  simp only [star_smul, Complex.star_def, Complex.conj_ofReal, smul_mul_assoc,
    mul_smul_comm, smul_smul]
  rw [← Complex.ofReal_mul, Real.mul_self_sqrt ha]

theorem flow_kraus (rate omega time : ℝ) (hr : 0 ≤ rate) (ht : 0 ≤ time) (X : M2) :
    flow rate omega time X =
      kraus0 rate omega time * X * star (kraus0 rate omega time) +
      kraus1 rate time * X * star (kraus1 rate time) +
      kraus2 rate time * X * star (kraus2 rate time) := by
  have hd := decay_range rate time hr ht
  unfold kraus0 kraus1 kraus2
  rw [sqrt_sandwich _ hd.1, sqrt_sandwich _ (sub_nonneg.mpr hd.2),
    sqrt_sandwich _ (sub_nonneg.mpr hd.2), IALDGraviton.projPlus_star, projMinus_star,
    flow_convex_unitary_pinching, Eg_apply]
  push_cast
  module

theorem kraus_normalization (rate omega time : ℝ) (hr : 0 ≤ rate) (ht : 0 ≤ time) :
    star (kraus0 rate omega time)*kraus0 rate omega time +
      star (kraus1 rate time)*kraus1 rate time +
      star (kraus2 rate time)*kraus2 rate time = 1 := by
  have hd := decay_range rate time hr ht
  unfold kraus0 kraus1 kraus2
  rw [sqrt_normalization _ hd.1, sqrt_normalization _ (sub_nonneg.mpr hd.2),
    sqrt_normalization _ (sub_nonneg.mpr hd.2), unitary_normalization,
    IALDGraviton.projPlus_star, projMinus_star, spectral_projections_are_idempotent.1,
    spectral_projections_are_idempotent.2]
  have hp := spectral_projections_split_the_identity.1
  rw [← hp]
  push_cast
  module

end
end TGLExt.TimeGravitonFlow
#print axioms TGLExt.TimeGravitonFlow.phase_star
#print axioms TGLExt.TimeGravitonFlow.phase_mul
#print axioms TGLExt.TimeGravitonFlow.phase_zero
#print axioms TGLExt.TimeGravitonFlow.unitary_eq_angFamily
#print axioms TGLExt.TimeGravitonFlow.unitary_star
#print axioms TGLExt.TimeGravitonFlow.unitary_normalization
#print axioms TGLExt.TimeGravitonFlow.unitary_action
#print axioms TGLExt.TimeGravitonFlow.mode_decay_phase
#print axioms TGLExt.TimeGravitonFlow.flow_convex_unitary_pinching
#print axioms TGLExt.TimeGravitonFlow.decay_range
#print axioms TGLExt.TimeGravitonFlow.sqrt_sandwich
#print axioms TGLExt.TimeGravitonFlow.sqrt_normalization
#print axioms TGLExt.TimeGravitonFlow.flow_kraus
#print axioms TGLExt.TimeGravitonFlow.kraus_normalization
