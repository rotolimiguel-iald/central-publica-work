import TGLExt.F1Fecho394.ExponentialTotalityR4
import TGLExt.F1Fecho394.BosonicSectorContinuity
import Mathlib.Analysis.Analytic.IsolatedZeros
import Mathlib.Analysis.Analytic.Constructions
import Mathlib.Analysis.SpecificLimits.Basic
/-! Analytic tools for totality of exponential vectors over a real cyclic subspace.
The tensor bilinear map and completed tensor powers are reused without modification. -/
set_option autoImplicit false
set_option maxHeartbeats 1600000
set_option synthInstance.maxHeartbeats 100000
noncomputable section
open Filter Topology UniformSpace
namespace F1Fecho.WedgeExponential
open TGLExt.ImportedSQ F1Rede.BosonicSectors F1Rede.BosonicFock
open F1Rede.BosonicSectorContinuity F1Fecho.Exponential

theorem ofReal_smul_H1 (t : ℝ) (x : H1) : (t : ℂ) • x = t • x := by
  rw [show (t : ℂ) = t • (1 : ℂ) by simp [Complex.real_smul], smul_assoc, one_smul]

def realSeries (a : ℕ → ℂ) : FormalMultilinearSeries ℝ ℝ ℂ :=
  fun n => ContinuousMultilinearMap.mkPiRing ℝ (Fin n) (a n)

theorem realSeries_coeff (a : ℕ → ℂ) (n : ℕ) : (realSeries a).coeff n = a n := by
  simp [realSeries, FormalMultilinearSeries.coeff]

theorem coefficients_zero_on_real_subspace (K : Submodule ℝ H1) (v : F)
    (hv : ∀ x ∈ K, inner ℂ v (exponential x) = 0) (x : H1) (hx : x ∈ K) (n : ℕ) :
    coefficient v x n = 0 := by
  have hp : HasFPowerSeriesAt (0 : ℝ → ℂ) (realSeries (coefficient v x)) 0 := by
    apply hasFPowerSeriesAt_iff.mpr
    apply Filter.Eventually.of_forall
    intro t
    have hs := scalar_series v x (t : ℂ)
    have hz : inner ℂ v (exponential ((t : ℂ) • x)) = 0 := by
      apply hv
      rw [ofReal_smul_H1]
      exact K.smul_mem t hx
    simpa only [realSeries_coeff, Complex.real_smul, Complex.ofReal_pow, hz, Pi.zero_apply] using hs
  have he := hp.apply_eq_zero n (1 : ℝ)
  simpa [realSeries] using he

theorem pure_inner_zero_on_real_subspace (K : Submodule ℝ H1) (v : F)
    (hv : ∀ x ∈ K, inner ℂ v (exponential x) = 0) (x : H1) (hx : x ∈ K) (n : ℕ) :
    inner ℂ (v n) (pureTensor n x) = 0 := by
  have h := coefficients_zero_on_real_subspace K v hv x hx n
  unfold coefficient component at h
  rw [_root_.inner_smul_right (v n) (pureTensor n x) (weight n : ℂ)] at h
  exact (mul_eq_zero.mp h).resolve_left (by exact_mod_cast (ne_of_gt (weight_pos n)))

theorem analytic_pureAlgebraic (n : ℕ) (x : H1) :
    AnalyticAt ℂ (fun y : H1 => pureAlgebraic y n) x := by
  induction n with
  | zero => exact analyticAt_const
  | succ n ih =>
    change AnalyticAt ℂ (fun y : H1 => tensorBilinear n y (pureAlgebraic y n)) x
    exact ((tensorBilinear n).analyticAt_bilinear _).comp₂ analyticAt_id ih

theorem analytic_pureCompleted (n : ℕ) (x : H1) :
    AnalyticAt ℂ (pureCompleted n) x := by
  exact ((Completion.toComplL (𝕜 := ℂ) (E := Algebraic n)).analyticAt _).comp
    (analytic_pureAlgebraic n x)

theorem zeros_on_real_frequent (f : ℂ → ℂ) (hf : ∀ t : ℝ, f t = 0) :
    ∃ᶠ z in 𝓝[≠] (0 : ℂ), f z = 0 := by
  let a : ℕ → ℂ := fun n => (1 / ((n : ℝ) + 1) : ℝ)
  have ha : Tendsto a atTop (𝓝 (0 : ℂ)) := by
    simpa only [a, Function.comp_def, Complex.ofReal_zero] using
      (Complex.continuous_ofReal.tendsto (0 : ℝ)).comp
        (tendsto_one_div_add_atTop_nhds_zero_nat (𝕜 := ℝ))
  have hn : ∀ n, a n ≠ 0 := by intro n; dsimp [a]; exact_mod_cast (by positivity : (1 / ((n : ℝ)+1)) ≠ 0)
  have ht : Tendsto a atTop (𝓝[≠] (0 : ℂ)) :=
    tendsto_nhdsWithin_iff.mpr ⟨ha, Filter.Eventually.of_forall hn⟩
  exact ht.frequently (Filter.Eventually.of_forall (fun n : ℕ => hf (1 / ((n : ℝ)+1)))).frequently

theorem analytic_zero_from_real (f : ℂ → ℂ) (hf : AnalyticOnNhd ℂ f Set.univ)
    (hr : ∀ t : ℝ, f t = 0) : ∀ z : ℂ, f z = 0 := by
  intro z
  exact hf.eqOn_zero_of_preconnected_of_frequently_eq_zero isPreconnected_univ
    (Set.mem_univ 0) (zeros_on_real_frequent f hr) (Set.mem_univ z)

end F1Fecho.WedgeExponential

#print axioms F1Fecho.WedgeExponential.coefficients_zero_on_real_subspace
#print axioms F1Fecho.WedgeExponential.analytic_pureAlgebraic
#print axioms F1Fecho.WedgeExponential.analytic_pureCompleted
#print axioms F1Fecho.WedgeExponential.analytic_zero_from_real
