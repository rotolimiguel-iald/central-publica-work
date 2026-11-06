import Lean
import TGLExt.O16.OrbitalPositiveEnergy_v3
import TGLExt.O16.OrbitalTranslationOperators_v2
import Mathlib.MeasureTheory.Integral.Bochner.ContinuousLinearMap
import Mathlib.Analysis.Calculus.DiffContOnCl
import Mathlib.Analysis.Complex.ReImTopology

set_option autoImplicit false
set_option maxHeartbeats 1000000
noncomputable section
open MeasureTheory Filter Set
open scoped ENNReal InnerProductSpace
namespace ChatgptAudit.WignerRapidityMeasure016
open ChatgptAudit.WignerOrbit016 ChatgptAudit.PositiveEnergy016 ChatgptAudit.UnitMultiplier016

variable {X E : Type*} [MeasurableSpace X] [NormedAddCommGroup E] [InnerProductSpace ℂ E]

def stateDensityMeasure (μ : Measure X) (f : Lp E 2 μ) : Measure X :=
  μ.withDensity (fun x => ENNReal.ofReal (‖f x‖^2))

theorem stateDensityMeasure_finite (μ : Measure X) (f : Lp E 2 μ) :
    IsFiniteMeasure (stateDensityMeasure μ f) := by
  apply isFiniteMeasure_withDensity
  have hi := (memLp_two_iff_integrable_sq_norm (Lp.aestronglyMeasurable f)).mp (Lp.memLp f)
  exact (lintegral_ofReal_ne_top_iff_integrable hi.aestronglyMeasurable
    (ae_of_all _ fun x => sq_nonneg ‖f x‖)).mpr hi

theorem stateDensity_integral_multiplier (μ : Measure X) (f : Lp E 2 μ)
    (u : X → ℂ) (hu : Measurable u) (hn : ∀ x, ‖u x‖=1) :
    (∫ x, u x ∂stateDensityMeasure μ f) = ⟪f, unitMultiplier μ u hu hn f⟫_ℂ := by
  have hw : AEMeasurable (fun x => ENNReal.ofReal (‖f x‖^2)) μ :=
    ((Lp.aestronglyMeasurable f).norm.aemeasurable.pow_const 2).ennreal_ofReal
  rw [stateDensityMeasure, integral_withDensity_eq_integral_toReal_smul₀ hw
    (ae_of_all _ fun _ => ENNReal.ofReal_lt_top) u, L2.inner_def]
  apply integral_congr_ae
  filter_upwards [unitMultiplier_ae μ u hu hn f] with x hx
  rw [hx, inner_smul_right, inner_self_eq_norm_sq_to_K]
  simp [ENNReal.toReal_ofReal, sq_nonneg, Complex.real_smul, mul_comm]

theorem orbitalPhase_real_parameter (m t : ℝ) (a : Fin 4 → ℝ) (y : MomentumCoordinates) :
    spectralPhase (t : ℂ) (orbitPairing a (shellMomentum m y)) =
      orbitalPhase m (t • a) y := by
  have hp (p : Fin 4 → ℝ) : orbitPairing (t • a) p = t*orbitPairing a p := by
    simp only [orbitPairing, Pi.smul_apply, smul_eq_mul]
    ring
  unfold spectralPhase orbitalPhase phase
  rw [hp, Complex.ofReal_mul]
  congr 1
  ring

theorem orbitalStateIntegral_boundary (m t : ℝ) (a : Fin 4 → ℝ)
    (f : Lp E 2 (orbitalMeasure m)) :
    spectralIntegral (stateDensityMeasure (orbitalMeasure m) f)
      (fun y => orbitPairing a (shellMomentum m y)) (t : ℂ) =
        ⟪f, orbitalTranslation m (t • a) f⟫_ℂ := by
  unfold spectralIntegral
  simp_rw [orbitalPhase_real_parameter]
  exact stateDensity_integral_multiplier (orbitalMeasure m) f (orbitalPhase m (t • a))
    (orbitalPhase_continuous m (t • a)).measurable (orbitalPhase_norm m (t • a))

/-- The analytic positive-energy conclusion for the actual orbital translations,
including the real boundary coefficient of every L² vector. -/
theorem orbital_positive_energy_analytic (m : ℝ) (a : Fin 4 → ℝ)
    (ha0 : 0 ≤ a 0) (ha : a 1^2+a 2^2+a 3^2 ≤ a 0^2)
    (f : Lp E 2 (orbitalMeasure m)) : ∃ F : ℂ → ℂ,
      DiffContOnCl ℂ F {z : ℂ | 0 < z.im} ∧
      (∃ M : ℝ, ∀ z : ℂ, 0 ≤ z.im → ‖F z‖ ≤ M) ∧
      (∀ t : ℝ, F t = ⟪f, orbitalTranslation m (t • a) f⟫_ℂ) := by
  let ν := stateDensityMeasure (orbitalMeasure m) f
  letI : IsFiniteMeasure ν := stateDensityMeasure_finite (orbitalMeasure m) f
  refine ⟨spectralIntegral ν (fun y => orbitPairing a (shellMomentum m y)), ?_, ?_, ?_⟩
  · constructor
    · exact orbitalSpectralIntegral_holomorphic m a ha0 ha ν
    · rw [Complex.closure_setOf_lt_im]
      exact spectralIntegral_continuous_closed ν _ (orbitalEnergy_measurable m a)
        (orbitalEnergy_nonnegative m a ha0 ha)
  · exact ⟨ν.real univ, fun z hz => orbitalSpectralIntegral_bound m a ha0 ha ν z hz⟩
  · intro t
    exact orbitalStateIntegral_boundary m t a f

#print axioms stateDensityMeasure_finite
#print axioms stateDensity_integral_multiplier
#print axioms orbitalPhase_real_parameter
#print axioms orbitalStateIntegral_boundary
#print axioms orbital_positive_energy_analytic
end ChatgptAudit.WignerRapidityMeasure016


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
