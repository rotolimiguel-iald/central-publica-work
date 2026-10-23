import TGLExt.F1Fecho394.RegularCoreAverageR2
import TGLExt.V350DualSemifiniteIdeal
/-! Plancherel evaluation of actual generic regular averages. This is the
same V350 Fourier argument on H, without substituting a different core. -/
set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 2500000
noncomputable section
namespace F1Fecho.RegularCoreFiniteWeight
open MeasureTheory Filter FourierTransform TGLV350 TGLV350.Regular
open F1Fecho.RegularCovariantCore F1Fecho.RegularCoreAverage
open scoped FourierTransform ENNReal NNReal Topology
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
/-- The actual Hilbert-valued regular orbit restricted to a finite interval. -/
def regularOrbitCut (B : UnitaryFlow H) (h : ℝ)
    (v : RegularHilbert H) :
    ℝ → RegularHilbert H :=
  (Set.Ioc 0 h).indicator (fun t => regularUnitary B t v)

theorem regularOrbitCut_memLp (B : UnitaryFlow H) (h : ℝ)
    (v : RegularHilbert H) (p : ℝ≥0∞) :
    MemLp (regularOrbitCut B h v) p := by
  have hc := memLp_indicator_const p measurableSet_Ioc ‖v‖
    (Or.inr (show volume (Set.Ioc 0 h) ≠ ⊤ by simp [Real.volume_Ioc]))
  apply hc.congr_norm
    ((regular_strongly_continuous B v).stronglyMeasurable.indicator measurableSet_Ioc).aestronglyMeasurable
  filter_upwards [] with t
  by_cases ht : t ∈ Set.Ioc 0 h
  · simp [ht, F1Fecho.RegularCoreAverage.regular_norm_map B]
  · simp [ht]

theorem regularOrbitCut_integrable (B : UnitaryFlow H) (h : ℝ)
    (v : RegularHilbert H) :
    Integrable (regularOrbitCut B h v) :=
  memLp_one_iff_integrable.mp (regularOrbitCut_memLp B h v 1)

theorem regularOrbitCut_integral_norm_sq (B : UnitaryFlow H) (h : ℝ) (hh : 0 < h)
    (v : RegularHilbert H) :
    (∫ t : ℝ, ‖regularOrbitCut B h v t‖ ^ 2) = h * ‖v‖ ^ 2 := by
  have heq : (fun t => ‖regularOrbitCut B h v t‖ ^ 2) =
      (Set.Ioc 0 h).indicator (fun _ => ‖v‖ ^ 2) := by
    funext t
    by_cases ht : t ∈ Set.Ioc 0 h <;> simp [regularOrbitCut, ht, F1Fecho.RegularCoreAverage.regular_norm_map B]
  rw [heq, integral_indicator measurableSet_Ioc, setIntegral_const]
  simp [Measure.real, Real.volume_Ioc, ENNReal.toReal_ofReal hh.le]

theorem regularAverage_dual_fourier (B : UnitaryFlow H) (s h : ℝ) (hh : 0 < h)
    (v : RegularHilbert H) :
    dualAmbient s (regularAverage B h) v =
      h⁻¹ • (𝓕 (regularOrbitCut B h v)) (s / (2 * Real.pi)) := by
  rw [F1Fecho.RegularCoreAverage.regularAverage_dual_apply B, Real.fourier_real_eq_integral_exp_smul]
  congr 1
  rw [intervalIntegral.integral_of_le hh.le]
  have heq : (fun t : ℝ => Complex.exp (↑(-2 * Real.pi * t * (s / (2 * Real.pi))) * Complex.I) •
      regularOrbitCut B h v t) =
      (Set.Ioc 0 h).indicator (fun t => characterPhase s t • regularUnitary B t v) := by
    funext t
    by_cases ht : t ∈ Set.Ioc 0 h
    · simp only [regularOrbitCut, Set.indicator_of_mem ht]
      congr 2
      push_cast
      field_simp
    · simp [regularOrbitCut, ht]
  rw [heq, integral_indicator measurableSet_Ioc]
  rfl

theorem regularAverage_dual_sq_integrable (B : UnitaryFlow H) (h : ℝ) (hh : 0 < h)
    (v : RegularHilbert H) :
    Integrable (fun s : ℝ => ‖dualAmbient s (regularAverage B h) v‖ ^ 2) := by
  have hf := Fourier.fourier_integral_memLp_two _
    (regularOrbitCut_integrable B h v) (regularOrbitCut_memLp B h v 2)
  have hi := ((memLp_two_iff_integrable_sq_norm hf.1).mp hf).comp_div
    (show (2 * Real.pi : ℝ) ≠ 0 by positivity)
  simpa only [regularAverage_dual_fourier B _ h hh v, norm_smul, Real.norm_eq_abs, mul_pow]
    using hi.const_mul (|h⁻¹| ^ 2)

theorem regularAverage_dual_integral_norm_sq (B : UnitaryFlow H) (h : ℝ) (hh : 0 < h)
    (v : RegularHilbert H) :
    (∫ s : ℝ, ‖dualAmbient s (regularAverage B h) v‖ ^ 2) =
      (2 * Real.pi) * h⁻¹ * ‖v‖ ^ 2 := by
  simp_rw [regularAverage_dual_fourier B _ h hh v, norm_smul, Real.norm_eq_abs, mul_pow]
  let g : ℝ → ℝ := fun x => ‖(𝓕 (regularOrbitCut B h v)) x‖ ^ 2
  have hd := Measure.integral_comp_div g (2 * Real.pi)
  change (∫ x : ℝ, ‖(𝓕 (regularOrbitCut B h v)) (x / (2 * Real.pi))‖ ^ 2) =
    |2 * Real.pi| • (∫ x : ℝ, ‖(𝓕 (regularOrbitCut B h v)) x‖ ^ 2) at hd
  rw [integral_const_mul, hd,
    Fourier.fourier_integral_norm_sq _ (regularOrbitCut_integrable B h v)
      (regularOrbitCut_memLp B h v 2), regularOrbitCut_integral_norm_sq B h hh v]
  rw [abs_of_pos (inv_pos.mpr hh), abs_of_pos (by positivity : 0 < 2 * Real.pi)]
  simp only [smul_eq_mul]
  field_simp

/-- Uniform finite form for the square of the averaging operator. The coefficient
is 1/h with the already fixed dual Haar convention, not an imposed normalization. -/
theorem regularAverage_dualQuadraticIntegral (B : UnitaryFlow H) (h : ℝ) (hh : 0 < h)
    (v : RegularHilbert H) :
    dualQuadraticIntegral (star (regularAverage B h) * regularAverage B h) v =
      ENNReal.ofReal (h⁻¹ * ‖v‖ ^ 2) := by
  simp only [dualQuadraticIntegral, dualQuadraticIntegrand_star_mul]
  rw [← ofReal_integral_eq_lintegral_ofReal (regularAverage_dual_sq_integrable B h hh v)
    (Filter.Eventually.of_forall (fun s => sq_nonneg _)),
    regularAverage_dual_integral_norm_sq B h hh v,
    ← ENNReal.ofReal_mul dualHaarFactor_pos.le]
  congr 1
  unfold dualHaarFactor
  field_simp

theorem regularAverage_dualQuadraticIntegral_lt_top (B : UnitaryFlow H)
    (h : ℝ) (hh : 0 < h) (v : RegularHilbert H) :
    dualQuadraticIntegral (star (regularAverage B h) * regularAverage B h) v < ⊤ := by
  rw [regularAverage_dualQuadraticIntegral B h hh v]
  exact ENNReal.ofReal_lt_top


theorem regularAverage_hasFiniteDualSquare (B : UnitaryFlow H)
    (h : ℝ) (hh : 0 < h) : HasFiniteDualSquare (regularAverage B h) := by
  let C : ℝ≥0 := ⟨h⁻¹, (inv_pos.mpr hh).le⟩
  have hC : ENNReal.ofReal h⁻¹ = (C : ℝ≥0∞) := ENNReal.ofReal_coe_nnreal (p := C)
  refine ⟨C, fun v => ?_⟩
  rw [regularAverage_dualQuadraticIntegral B h hh v,
    ENNReal.ofReal_mul (inv_pos.mpr hh).le]
  rw [hC]

theorem finiteDualLeftIdeal_strong_approximation (B : UnitaryFlow H) (M : VonNeumannAlgebra H)
    (A : (core B M).toStarSubalgebra) :
    (∀ h : ℝ, 0 < h → HasFiniteDualSquare (A.val * regularAverage B h)) ∧
    (∀ h : ℝ, A.val * regularAverage B h ∈ core B M) ∧
    (∀ v, Tendsto (fun h : ℝ => (A.val * regularAverage B h) v) (𝓝[>] 0) (𝓝 (A.val v))) := by
  refine ⟨fun h hh => HasFiniteDualSquare.left_mul _ _
    (regularAverage_hasFiniteDualSquare B h hh),
    fun h => (core B M).toStarSubalgebra.mul_mem A.property (regularAverage_mem B M h),
    fun v => (regularAverage_mul_tendsto B A.val v).mono_left ?_⟩
  exact nhdsWithin_mono _ (by intro h hh; exact ne_of_gt hh)

end F1Fecho.RegularCoreFiniteWeight
open Lean in
run_cmd do
  let env ← Elab.Command.liftCoreM getEnv
  for (n, ci) in env.constants.map₂.toList do
    if (`F1Fecho.RegularCoreFiniteWeight).isPrefixOf n then
      let axs ← collectAxioms n
      IO.println ("LOCAL_DECL\t" ++ n.toString ++ "\t" ++ String.intercalate "," (axs.toList.map Name.toString))
      unless axs.all (fun a => a == `propext || a == `Classical.choice || a == `Quot.sound) do
        throwError "AXIOM_AUDIT_REFUSED: {n}"
      match ci with
      | .axiomInfo _ => throwError "LOCAL_AXIOM_REFUSED: {n}"
      | _ => pure ()
