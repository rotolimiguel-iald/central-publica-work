import Lean
import Mathlib.Analysis.Calculus.ParametricIntegral
import Mathlib.Analysis.SpecialFunctions.ExpDeriv
import Mathlib.Analysis.Complex.Trigonometric
import Mathlib.Tactic

set_option autoImplicit false
set_option maxHeartbeats 1000000
noncomputable section
open MeasureTheory Filter Set
open scoped ENNReal Topology
namespace ChatgptAudit.PositiveEnergy016

def spectralPhase (z : ℂ) (r : ℝ) : ℂ := Complex.exp (z * ((r : ℂ) * Complex.I))

theorem spectralPhase_norm (z : ℂ) (r : ℝ) :
    ‖spectralPhase z r‖ = Real.exp (-z.im*r) := by
  simp [spectralPhase, Complex.norm_exp, Complex.mul_re, Complex.mul_im]

theorem spectralPhase_norm_le_one (z : ℂ) (r : ℝ) (hz : 0 ≤ z.im) (hr : 0 ≤ r) :
    ‖spectralPhase z r‖ ≤ 1 := by
  rw [spectralPhase_norm]
  apply Real.exp_le_one_iff.mpr
  nlinarith

theorem spectralPhase_hasDerivAt (z : ℂ) (r : ℝ) :
    HasDerivAt (fun w => spectralPhase w r)
      (((r : ℂ)*Complex.I)*spectralPhase z r) z := by
  have h := (Complex.hasDerivAt_exp (z*((r : ℂ)*Complex.I))).comp z
    ((hasDerivAt_id z).mul_const ((r : ℂ)*Complex.I))
  simpa [spectralPhase, Function.comp_def, mul_comm] using h

/-- Uniform derivative bound on every strict interior sub-half-plane.
No finite first moment of the spectral measure is assumed. -/
theorem spectralPhase_derivative_bound (z : ℂ) (r δ : ℝ)
    (hr : 0 ≤ r) (hδ : 0 < δ) (hz : δ ≤ z.im) :
    ‖((r : ℂ)*Complex.I)*spectralPhase z r‖ ≤ 1/δ := by
  have hnorm : ‖((r : ℂ)*Complex.I)*spectralPhase z r‖ = r*Real.exp (-z.im*r) := by
    simp [norm_mul, spectralPhase_norm, Complex.norm_real, abs_of_nonneg hr]
  rw [hnorm]
  have hmono : r*Real.exp (-z.im*r) ≤ r*Real.exp (-(δ*r)) := by
    apply mul_le_mul_of_nonneg_left _ hr
    apply Real.exp_le_exp.mpr
    nlinarith
  apply hmono.trans
  apply (le_div_iff₀ hδ).mpr
  have hb := Real.mul_exp_neg_le_exp_neg_one (δ*r)
  have hunit : Real.exp (-1) ≤ 1 := Real.exp_le_one_iff.mpr (by norm_num)
  nlinarith

variable {X : Type*} [MeasurableSpace X]

theorem spectralPhase_measurable (freq : X → ℝ) (hfreq : Measurable freq) (z : ℂ) :
    Measurable (fun x => spectralPhase z (freq x)) := by
  unfold spectralPhase
  fun_prop

theorem spectralPhase_integrable (μ : Measure X) [IsFiniteMeasure μ]
    (freq : X → ℝ) (hfreq : Measurable freq) (hpos : ∀ x, 0 ≤ freq x)
    (z : ℂ) (hz : 0 ≤ z.im) : Integrable (fun x => spectralPhase z (freq x)) μ := by
  apply (integrable_const (1 : ℝ)).mono'
    (spectralPhase_measurable freq hfreq z).aestronglyMeasurable
  exact ae_of_all _ fun x => spectralPhase_norm_le_one z (freq x) hz (hpos x)

def spectralIntegral (μ : Measure X) (freq : X → ℝ) (z : ℂ) : ℂ :=
  ∫ x, spectralPhase z (freq x) ∂μ

theorem spectralIntegral_bound (μ : Measure X) [IsFiniteMeasure μ]
    (freq : X → ℝ) (hpos : ∀ x, 0 ≤ freq x) (z : ℂ) (hz : 0 ≤ z.im) :
    ‖spectralIntegral μ freq z‖ ≤ μ.real Set.univ := by
  simpa only [spectralIntegral, one_mul] using (norm_integral_le_of_norm_le_const
    (μ := μ) (ae_of_all _ fun x => spectralPhase_norm_le_one z (freq x) hz (hpos x)))

theorem spectralIntegral_differentiableAt (μ : Measure X) [IsFiniteMeasure μ]
    (freq : X → ℝ) (hfreq : Measurable freq) (hpos : ∀ x, 0 ≤ freq x)
    (z : ℂ) (hz : 0 < z.im) : DifferentiableAt ℂ (spectralIntegral μ freq) z := by
  let δ := z.im/2
  have hd : 0 < δ := by dsimp [δ]; positivity
  have hs : {w : ℂ | δ < w.im} ∈ 𝓝 z := by
    apply (isOpen_lt continuous_const Complex.continuous_im).mem_nhds
    dsimp [δ]
    linarith
  have hmeas : ∀ᶠ w in 𝓝 z, AEStronglyMeasurable (fun x => spectralPhase w (freq x)) μ :=
    Filter.Eventually.of_forall fun w => (spectralPhase_measurable freq hfreq w).aestronglyMeasurable
  have hdmeas : AEStronglyMeasurable
      (fun x => (((freq x : ℝ) : ℂ)*Complex.I)*spectralPhase z (freq x)) μ := by
    apply Measurable.aestronglyMeasurable
    exact ((Complex.continuous_ofReal.measurable.comp hfreq).mul_const Complex.I).mul
      (spectralPhase_measurable freq hfreq z)
  have hb : ∀ᵐ x ∂μ, ∀ w ∈ {w : ℂ | δ < w.im},
      ‖(((freq x : ℝ) : ℂ)*Complex.I)*spectralPhase w (freq x)‖ ≤ 1/δ := by
    exact ae_of_all _ fun x w hw => spectralPhase_derivative_bound w (freq x) δ (hpos x) hd hw.le
  have hh := hasDerivAt_integral_of_dominated_loc_of_deriv_le
    (μ := μ) hs hmeas (spectralPhase_integrable μ freq hfreq hpos z hz.le)
    hdmeas hb (integrable_const (1/δ))
    (ae_of_all _ fun x w _ => spectralPhase_hasDerivAt w (freq x))
  exact hh.2.differentiableAt

theorem spectralIntegral_holomorphic (μ : Measure X) [IsFiniteMeasure μ]
    (freq : X → ℝ) (hfreq : Measurable freq) (hpos : ∀ x, 0 ≤ freq x) :
    DifferentiableOn ℂ (spectralIntegral μ freq) {z : ℂ | 0 < z.im} := by
  intro z hz
  exact (spectralIntegral_differentiableAt μ freq hfreq hpos z hz).differentiableWithinAt

theorem spectralIntegral_continuous_closed (μ : Measure X) [IsFiniteMeasure μ]
    (freq : X → ℝ) (hfreq : Measurable freq) (hpos : ∀ x, 0 ≤ freq x) :
    ContinuousOn (spectralIntegral μ freq) {z : ℂ | 0 ≤ z.im} := by
  apply continuousOn_of_dominated (bound := fun _ => (1 : ℝ))
  · intro z _
    exact (spectralPhase_measurable freq hfreq z).aestronglyMeasurable
  · intro z hz
    exact ae_of_all _ fun x => spectralPhase_norm_le_one z (freq x) hz (hpos x)
  · exact integrable_const 1
  · apply ae_of_all
    intro x
    have hd : Differentiable ℂ (fun z => spectralPhase z (freq x)) :=
      fun z => (spectralPhase_hasDerivAt z (freq x)).differentiableAt
    exact hd.continuous.continuousOn

#print axioms spectralIntegral_continuous_closed
#print axioms spectralPhase_norm
#print axioms spectralPhase_norm_le_one
#print axioms spectralPhase_hasDerivAt
#print axioms spectralPhase_derivative_bound
#print axioms spectralPhase_measurable
#print axioms spectralPhase_integrable
#print axioms spectralIntegral_bound
#print axioms spectralIntegral_differentiableAt
#print axioms spectralIntegral_holomorphic
end ChatgptAudit.PositiveEnergy016


-- Engineering audit: all declarations introduced by this compilation unit.
open Lean in
run_cmd do
  let env ← Elab.Command.liftCoreM getEnv
  for (n, ci) in env.constants.map₂.toList do
    let axs ← collectAxioms n
    let kind := match ci with
      | .axiomInfo _ => "axiom"
      | .thmInfo _ => "theorem"
      | .defnInfo _ => "definition"
      | _ => "generated_or_type"
    IO.println ("BENCH_DECL\t" ++ n.toString ++ "\t" ++ kind ++ "\t" ++
      String.intercalate "," (axs.toList.map Name.toString))
    unless axs.all (fun a => a == `propext || a == `Classical.choice || a == `Quot.sound) do
      throwError "AXIOM_AUDIT_REFUSED: {n}"
    if kind == "axiom" then throwError "NEW_AXIOM_REFUSED: {n}"
