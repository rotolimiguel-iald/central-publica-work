import Lean
import TGLExt.O16.OrbitalRapidityMeasure_v4
import TGLExt.O16.OrbitTranslationFaithfulness_v2
import Mathlib.MeasureTheory.Measure.OpenPos
import Mathlib.Tactic

set_option autoImplicit false
set_option maxHeartbeats 1000000
noncomputable section
open MeasureTheory Set Filter
open scoped ENNReal
namespace ChatgptAudit.WignerRapidityMeasure016
open ChatgptAudit.WignerOrbit016

theorem orbitalWeight_pos_ae (m : ℝ) :
    ∀ᵐ y ∂momentumMeasure, orbitalWeight m y ≠ 0 := by
  have hq : ∀ᵐ y ∂momentumMeasure, y.1 ≠ (0 : Transverse) := by
    rw [ae_iff]
    have hs : {y : MomentumCoordinates | ¬ y.1 ≠ (0 : Transverse)} =
        ({0} : Set Transverse) ×ˢ (Set.univ : Set ℝ) := by
      ext y
      simp
    rw [hs]
    exact exceptional_axis_null
  filter_upwards [hq] with y hy
  have hr := transverseMass_pos_of_ne_zero m y.1 hy
  have he : 0 < energy (transverseMass m y.1) y.2 := by
    unfold energy
    apply Real.sqrt_pos.mpr
    nlinarith [sq_pos_of_pos hr, sq_nonneg y.2]
  exact ne_of_gt (ENNReal.ofReal_pos.mpr (one_div_pos.mpr he))

theorem momentum_absolutelyContinuous_orbital (m : ℝ) :
    momentumMeasure ≪ orbitalMeasure m :=
  withDensity_absolutelyContinuous' (orbitalWeight_measurable m).aemeasurable
    (orbitalWeight_pos_ae m)

theorem orbitalMeasure_sigmaFinite (m : ℝ) : SigmaFinite (orbitalMeasure m) := by
  unfold orbitalMeasure orbitalWeight momentumMeasure
  infer_instance

theorem orbitalMeasure_openPos (m : ℝ) : (orbitalMeasure m).IsOpenPosMeasure := by
  letI : momentumMeasure.IsOpenPosMeasure := by unfold momentumMeasure; infer_instance
  exact (momentum_absolutelyContinuous_orbital m).isOpenPosMeasure

/-- Coordinates (q₂,q₃,p₁) with positive-energy root; the vertex is included
in the coordinate domain but has zero orbital measure in the massless case. -/
def shellMomentum (m : ℝ) (y : MomentumCoordinates) : Fin 4 → ℝ :=
  ![energy (transverseMass m y.1) y.2, y.2, y.1 0, y.1 1]

theorem shellMomentum_continuous (m : ℝ) : Continuous (shellMomentum m) := by
  unfold shellMomentum energy transverseMass
  fun_prop

theorem shellMomentum_covers_shell (m : ℝ) (p : Fin 4 → ℝ)
    (hp : p ∈ futureMassShell m) : ∃ y, shellMomentum m y = p := by
  refine ⟨(![p 2, p 3], p 1), ?_⟩
  have he2 : energy (transverseMass m ![p 2, p 3]) (p 1) ^ 2 = (p 0)^2 := by
    rw [energy, Real.sq_sqrt (by positivity), transverseMass_sq]
    simp only [Matrix.cons_val_zero, Matrix.cons_val_one, Matrix.head_cons]
    have hh := hp.2
    nlinarith
  have he : energy (transverseMass m ![p 2, p 3]) (p 1) = p 0 := by
    have hn := Real.sqrt_nonneg ((transverseMass m ![p 2, p 3])^2+(p 1)^2)
    have hh := hp.1
    unfold energy at he2 ⊢
    nlinarith
  ext i
  fin_cases i <;> simp [shellMomentum, he]

def orbitalPhase (m : ℝ) (a : Fin 4 → ℝ) (y : MomentumCoordinates) : ℂ :=
  phase (orbitPairing a (shellMomentum m y))

theorem orbitalPhase_continuous (m : ℝ) (a : Fin 4 → ℝ) :
    Continuous (orbitalPhase m a) := by
  unfold orbitalPhase phase orbitPairing shellMomentum energy transverseMass
  fun_prop

theorem orbitalPhase_norm (m : ℝ) (a : Fin 4 → ℝ) (y : MomentumCoordinates) :
    ‖orbitalPhase m a y‖ = 1 := Complex.norm_exp_ofReal_mul_I _

theorem orbitalPhase_ae_to_shell (m : ℝ) (a : Fin 4 → ℝ)
    (h : orbitalPhase m a =ᵐ[orbitalMeasure m] fun _ => 1) :
    ∀ p ∈ futureMassShell m, phase (orbitPairing a p) = 1 := by
  letI := orbitalMeasure_openPos m
  have he : orbitalPhase m a = fun _ => 1 :=
    ((orbitalPhase_continuous m a).ae_eq_iff_eq (orbitalMeasure m) continuous_const).mp h
  intro p hp
  obtain ⟨y, hy⟩ := shellMomentum_covers_shell m p hp
  have hh := congrFun he y
  simpa only [orbitalPhase, hy] using hh

#print axioms orbitalWeight_pos_ae
#print axioms momentum_absolutelyContinuous_orbital
#print axioms orbitalMeasure_sigmaFinite
#print axioms orbitalMeasure_openPos
#print axioms shellMomentum_continuous
#print axioms shellMomentum_covers_shell
#print axioms orbitalPhase_continuous
#print axioms orbitalPhase_norm
#print axioms orbitalPhase_ae_to_shell
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
