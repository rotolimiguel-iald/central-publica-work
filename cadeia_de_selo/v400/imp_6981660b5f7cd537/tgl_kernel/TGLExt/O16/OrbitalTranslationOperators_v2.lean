import Lean
import TGLExt.O16.UnitMultiplierIdentity
import TGLExt.O16.OrbitalMeasureSupport_v2

set_option autoImplicit false
set_option maxHeartbeats 1000000
noncomputable section
open MeasureTheory Filter
open scoped ENNReal
namespace ChatgptAudit.WignerRapidityMeasure016
open ChatgptAudit.WignerOrbit016 ChatgptAudit.UnitMultiplier016

variable {E : Type*} [NormedAddCommGroup E] [NormedSpace ℂ E]

/-- Actual translation operator on the weighted mass-shell L² space.
The same scalar phase acts on every complex fiber, including ℂ × ℂ. -/
def orbitalTranslation (m : ℝ) (a : Fin 4 → ℝ) :
    Lp E 2 (orbitalMeasure m) →L[ℂ] Lp E 2 (orbitalMeasure m) :=
  unitMultiplier (orbitalMeasure m) (orbitalPhase m a)
    (orbitalPhase_continuous m a).measurable (orbitalPhase_norm m a)

theorem orbitalTranslation_ae (m : ℝ) (a : Fin 4 → ℝ)
    (f : Lp E 2 (orbitalMeasure m)) :
    orbitalTranslation m a f =ᵐ[orbitalMeasure m] fun y => orbitalPhase m a y • f y :=
  unitMultiplier_ae _ _ _ _ f

theorem orbitalTranslation_norm (m : ℝ) (a : Fin 4 → ℝ)
    (f : Lp E 2 (orbitalMeasure m)) : ‖orbitalTranslation m a f‖ = ‖f‖ :=
  unitMultiplier_norm _ _ _ _ f

theorem orbitalPhase_add (m : ℝ) (a b : Fin 4 → ℝ) (y : MomentumCoordinates) :
    orbitalPhase m (a+b) y = orbitalPhase m a y * orbitalPhase m b y := by
  have hp (p : Fin 4 → ℝ) : orbitPairing (a+b) p = orbitPairing a p + orbitPairing b p := by
    simp only [orbitPairing, Pi.add_apply]
    ring
  simp only [orbitalPhase, phase, hp, Complex.ofReal_add, add_mul, Complex.exp_add]

theorem orbitalTranslation_zero (m : ℝ) (f : Lp E 2 (orbitalMeasure m)) :
    orbitalTranslation m 0 f = f := by
  apply Lp.ext
  filter_upwards [orbitalTranslation_ae m 0 f] with y hy
  simpa [orbitalPhase, phase, orbitPairing] using hy

theorem orbitalTranslation_add (m : ℝ) (a b : Fin 4 → ℝ)
    (f : Lp E 2 (orbitalMeasure m)) :
    orbitalTranslation m (a+b) f = orbitalTranslation m a (orbitalTranslation m b f) := by
  apply Lp.ext
  filter_upwards [orbitalTranslation_ae m (a+b) f,
    orbitalTranslation_ae m a (orbitalTranslation m b f), orbitalTranslation_ae m b f]
      with y h1 h2 h3
  rw [h1, h2, h3, orbitalPhase_add, mul_smul]

theorem orbitalTranslation_inverse (m : ℝ) (a : Fin 4 → ℝ)
    (f : Lp E 2 (orbitalMeasure m)) :
    orbitalTranslation m (-a) (orbitalTranslation m a f) = f := by
  rw [← orbitalTranslation_add, neg_add_cancel, orbitalTranslation_zero]

def orbitalTranslationIsometry (m : ℝ) (a : Fin 4 → ℝ) :
    Lp E 2 (orbitalMeasure m) →ₗᵢ[ℂ] Lp E 2 (orbitalMeasure m) where
  toLinearMap := (orbitalTranslation m a).toLinearMap
  norm_map' := orbitalTranslation_norm m a

def orbitalTranslationEquiv (m : ℝ) (a : Fin 4 → ℝ) :
    Lp E 2 (orbitalMeasure m) ≃ₗᵢ[ℂ] Lp E 2 (orbitalMeasure m) :=
  LinearIsometryEquiv.ofLinearIsometry (orbitalTranslationIsometry m a)
    (orbitalTranslation m (-a)).toLinearMap
    (by
      apply LinearMap.ext
      intro f
      change orbitalTranslation m a (orbitalTranslation m (-a) f) = f
      simpa only [neg_neg] using orbitalTranslation_inverse m (-a) f)
    (by
      apply LinearMap.ext
      intro f
      change orbitalTranslation m (-a) (orbitalTranslation m a f) = f
      exact orbitalTranslation_inverse m a f)

theorem orbitalTranslationEquiv_apply (m : ℝ) (a : Fin 4 → ℝ)
    (f : Lp E 2 (orbitalMeasure m)) :
    orbitalTranslationEquiv m a f = orbitalTranslation m a f := rfl

/-- Kernel faithfulness for all nonnegative masses and every nontrivial complex fiber.
The a.e. multiplier is upgraded by full support and continuity before using the
already compiled pointwise character theorems. -/
theorem orbitalTranslation_faithful [Nontrivial E] (m : ℝ) (hm : 0 ≤ m)
    (a : Fin 4 → ℝ)
    (h : ∀ f : Lp E 2 (orbitalMeasure m), orbitalTranslation m a f = f) : a = 0 := by
  letI := orbitalMeasure_sigmaFinite m
  have hae : orbitalPhase m a =ᵐ[orbitalMeasure m] fun _ => 1 :=
    (unitMultiplier_identity_iff (E := E) (orbitalMeasure m) (orbitalPhase m a)
      (orbitalPhase_continuous m a).measurable (orbitalPhase_norm m a)).mp h
  have hp := orbitalPhase_ae_to_shell m a hae
  rcases eq_or_lt_of_le hm with hz | hpos
  · subst m
    exact null_orbit_faithful a hp
  · exact massive_orbit_faithful m hpos a hp

theorem orbitalTranslation_injective [Nontrivial E] (m : ℝ) (hm : 0 ≤ m) :
    Function.Injective (orbitalTranslation (E := E) m) := by
  intro a b hab
  have hzero : a-b=0 := by
    apply orbitalTranslation_faithful (E := E) m hm
    intro f
    rw [sub_eq_add_neg, orbitalTranslation_add, hab,
      ← orbitalTranslation_add, add_neg_cancel, orbitalTranslation_zero]
  exact sub_eq_zero.mp hzero

#print axioms orbitalTranslation_ae
#print axioms orbitalTranslation_norm
#print axioms orbitalPhase_add
#print axioms orbitalTranslation_zero
#print axioms orbitalTranslation_add
#print axioms orbitalTranslation_inverse
#print axioms orbitalTranslationEquiv_apply
#print axioms orbitalTranslation_faithful
#print axioms orbitalTranslation_injective
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
