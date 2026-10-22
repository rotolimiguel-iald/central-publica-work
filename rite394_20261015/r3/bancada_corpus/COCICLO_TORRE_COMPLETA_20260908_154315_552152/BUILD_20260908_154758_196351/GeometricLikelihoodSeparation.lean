import TGLExt.LikelihoodDensityLog
import TGLExt.SummableGravityControls
import Mathlib.Tactic

set_option autoImplicit false
set_option maxHeartbeats 2400000
namespace ChatgptAudit.CocycleRealization
open Filter Topology Set TGLExt ChatgptAudit.Response028 ChatgptAudit.Cocycle030
  ChatgptAudit.Density033 ChatgptAudit.Thermal025
noncomputable section

def logContrast (x : ℝ) : ℝ := logOneRatio x - logZeroRatio x

def geometricArgument (t : ℝ) (n : ℕ) : ℝ :=
  geometricAmplitude.value n * regularParameter t

def geometricContrast (t : ℝ) (n : ℕ) : ℝ :=
  logContrast (geometricArgument t n)

theorem contrast_nonnegative {x : ℝ} (hx : 0 ≤ x) (hb : x ≤ 1/12) :
    0 ≤ logContrast x := by
  have h0 := (log_zero_ratio_bounds x hx hb).2
  have h1 := (log_one_ratio_bounds x hx).1
  dsimp [logContrast]
  linarith

theorem contrast_upper {x : ℝ} (hx : 0 ≤ x) (hb : x ≤ 1/12) :
    logContrast x ≤ 6*x := by
  have h := log_ratio_abs_bound x hx hb
  have h0 := (log_zero_ratio_bounds x hx hb).2
  have h1 := (log_one_ratio_bounds x hx).1
  rw [abs_of_nonpos h0, abs_of_nonneg h1] at h
  dsimp [logContrast]
  linarith

theorem contrast_log_ratio {x : ℝ} (hx : 0 ≤ x) (hb : x ≤ 1/12) :
    logContrast x = Real.log ((1+(3/2)*x)/(1-3*x)) := by
  have h0 : 0 < 1-3*x := by linarith
  have h1 : 0 < 1+(3/2)*x := by positivity
  rw [Real.log_div (ne_of_gt h1) (ne_of_gt h0)]
  rfl

theorem contrast_strict_dyadic {x : ℝ} (hx : 0 < x) (hb : x ≤ 1/12) :
    2*logContrast (x/2) < logContrast x := by
  have h0 : 0 < 1-3*x := by linarith
  have hh : 0 < 1-3*(x/2) := by linarith
  have hp : 0 < 1+(3/2)*(x/2) := by positivity
  have hbhalf : x/2 ≤ (1:ℝ)/12 := by linarith
  have hratio :
      ((1+(3/2)*(x/2))/(1-3*(x/2)))^2 <
        (1+(3/2)*x)/(1-3*x) := by
    rw [div_pow]
    apply (div_lt_div_iff₀ (sq_pos_of_pos hh) h0).mpr
    apply sub_pos.mp
    have he :
        (1+(3/2)*x)*(1-3*(x/2))^2 -
          (1+(3/2)*(x/2))^2*(1-3*x) = (27/16)*x^2*(1+3*x) := by ring
    rw [he]
    positivity
  have hl := Real.log_lt_log (sq_pos_of_pos (div_pos hp hh)) hratio
  rw [Real.log_pow] at hl
  rw [contrast_log_ratio (by positivity : 0 ≤ x/2) hbhalf,
    contrast_log_ratio hx.le hb]
  simpa using hl

theorem contrast_dyadic {x : ℝ} (hx : 0 ≤ x) (hb : x ≤ 1/12) :
    2*logContrast (x/2) ≤ logContrast x := by
  by_cases hz : x=0
  · subst x
    norm_num [logContrast,logOneRatio,logZeroRatio]
  · exact (contrast_strict_dyadic (lt_of_le_of_ne hx (Ne.symm hz)) hb).le

theorem geometric_argument_bounds (t : ℝ) (n : ℕ) :
    0 ≤ geometricArgument t n ∧ geometricArgument t n ≤ 1/12 :=
  likelihood_argument_bounds geometricAmplitude t n

theorem geometric_argument_positive {t : ℝ} (ht : t≠0) (n : ℕ) :
    0 < geometricArgument t n :=
  mul_pos (geometric_amplitude_positive n) (regular_parameter_positive t ht)

theorem geometric_argument_succ (t : ℝ) (n : ℕ) :
    geometricArgument t (n+1) = geometricArgument t n/2 := by
  change (1/24)*(1/2 : ℝ)^(n+1)*regularParameter t =
    ((1/24)*(1/2 : ℝ)^n*regularParameter t)/2
  rw [pow_succ]
  ring

theorem geometric_contrast_nonnegative (t : ℝ) (n : ℕ) :
    0 ≤ geometricContrast t n :=
  contrast_nonnegative (geometric_argument_bounds t n).1 (geometric_argument_bounds t n).2

theorem geometric_contrast_summable (t : ℝ) : Summable (geometricContrast t) := by
  apply Summable.of_nonneg_of_le (geometric_contrast_nonnegative t)
    (fun n => ?_) (geometricAmplitude.summable.mul_left (6*regularParameter t))
  have h := contrast_upper (geometric_argument_bounds t n).1 (geometric_argument_bounds t n).2
  simpa only [geometricContrast,geometricArgument,mul_comm,mul_left_comm,mul_assoc] using h

theorem geometric_contrast_succ_le (t : ℝ) (n : ℕ) :
    geometricContrast t (n+1) ≤ geometricContrast t n/2 := by
  have h := contrast_dyadic (geometric_argument_bounds t n).1 (geometric_argument_bounds t n).2
  change logContrast (geometricArgument t (n+1)) ≤ _
  rw [geometric_argument_succ]
  change logContrast (geometricArgument t n/2) ≤ logContrast (geometricArgument t n)/2
  linarith

theorem geometric_contrast_strict_succ {t : ℝ} (ht : t≠0) (n : ℕ) :
    2*geometricContrast t (n+1) < geometricContrast t n := by
  have h := contrast_strict_dyadic (geometric_argument_positive ht n)
    (geometric_argument_bounds t n).2
  simpa only [geometricContrast,geometric_argument_succ] using h

theorem geometric_contrast_shift_bound (t : ℝ) (n k : ℕ) :
    geometricContrast t (n+1+k) ≤ geometricContrast t (n+1)*(1/2 : ℝ)^k := by
  induction k with
  | zero => simp
  | succ k ih =>
    have hh := geometric_contrast_succ_le t (n+1+k)
    have hle := div_le_div_of_nonneg_right ih (by norm_num : (0:ℝ)≤2)
    rw [pow_succ]
    have he : n+1+(k+1)=(n+1+k)+1 := by omega
    rw [he]
    nlinarith

theorem geometric_contrast_tail_summable (t : ℝ) (n : ℕ) :
    Summable (fun k => geometricContrast t (n+1+k)) :=
  (geometric_contrast_summable t).comp_injective (fun _ _ h => Nat.add_left_cancel h)

theorem geometric_contrast_tail_le (t : ℝ) (n : ℕ) :
    (∑' k, geometricContrast t (n+1+k)) ≤ 2*geometricContrast t (n+1) := by
  calc
    (∑' k, geometricContrast t (n+1+k)) ≤
        ∑' k, geometricContrast t (n+1)*(1/2 : ℝ)^k :=
      tsum_le_tsum (geometric_contrast_shift_bound t n)
        (geometric_contrast_tail_summable t n)
        ((summable_geometric_of_lt_one (by norm_num : (0:ℝ)≤1/2) (by norm_num)).mul_left _)
    _ = 2*geometricContrast t (n+1) := by
      rw [tsum_mul_left,tsum_geometric_of_lt_one (by norm_num : (0:ℝ)≤1/2) (by norm_num)]
      ring

theorem geometric_contrast_dominates_entire_tail {t : ℝ} (ht : t≠0) (n : ℕ) :
    (∑' k, geometricContrast t (n+1+k)) < geometricContrast t n :=
  lt_of_le_of_lt (geometric_contrast_tail_le t n) (geometric_contrast_strict_succ ht n)

theorem existing_global_generator_bound (t : ℝ) :
    ‖likelihoodGenerator geometricAmplitude t‖ ≤ regularParameter t/2 := by
  have h := likelihood_generator_bound geometricAmplitude t
  rw [geometric_amplitude_mass] at h
  convert h using 1 <;> ring

theorem existing_global_density_normalized (t : ℝ) :
    omegaState thirdThermalReference (likelihoodDensity geometricAmplitude t)=1 :=
  likelihood_density_normalized geometricAmplitude t

theorem existing_global_cocycle_limit (t s : ℝ) :
    Tendsto (likelihoodPrefixCocycle geometricAmplitude t s) atTop
      (𝓝 (likelihoodCocycle geometricAmplitude t s)) :=
  likelihood_prefix_cocycle_limit geometricAmplitude t s

#print axioms logContrast
#print axioms geometricArgument
#print axioms geometricContrast
#print axioms contrast_nonnegative
#print axioms contrast_upper
#print axioms contrast_log_ratio
#print axioms contrast_strict_dyadic
#print axioms contrast_dyadic
#print axioms geometric_argument_bounds
#print axioms geometric_argument_positive
#print axioms geometric_argument_succ
#print axioms geometric_contrast_nonnegative
#print axioms geometric_contrast_summable
#print axioms geometric_contrast_succ_le
#print axioms geometric_contrast_strict_succ
#print axioms geometric_contrast_shift_bound
#print axioms geometric_contrast_tail_summable
#print axioms geometric_contrast_tail_le
#print axioms geometric_contrast_dominates_entire_tail
#print axioms existing_global_generator_bound
#print axioms existing_global_density_normalized
#print axioms existing_global_cocycle_limit

end
end ChatgptAudit.CocycleRealization
