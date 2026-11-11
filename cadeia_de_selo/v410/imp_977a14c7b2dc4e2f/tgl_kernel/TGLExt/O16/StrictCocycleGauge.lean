import Lean
import TGLExt.O16.OrbitTranslationFaithfulness_v2

set_option autoImplicit false
set_option maxHeartbeats 800000
noncomputable section
open Complex
namespace ChatgptAudit.CocycleGauge016
open ChatgptAudit.WignerOrbit016

/-- Pointwise law: no almost-everywhere substitution is hidden here. -/
theorem strict_cocycle_is_coboundary {G : Type*} [Group G]
    (C : ℝ → ℝ → G)
    (hc : ∀ s t x : ℝ, C (s+t) x = C s x * C t (x-s)) (s x : ℝ) :
    C s x = C x x * (C (x-s) (x-s))⁻¹ := by
  have h := hc s (x-s) x
  rw [add_sub_cancel] at h
  rw [h,mul_assoc,mul_inv_cancel, mul_one]

def phaseCoboundary (chi : ℝ → ℝ) (s x : ℝ) : ℂ :=
  phase (chi x - chi (x-s))

theorem phaseCoboundary_cocycle (chi : ℝ → ℝ) (s t x : ℝ) :
    phaseCoboundary chi (s+t) x =
      phaseCoboundary chi s x * phaseCoboundary chi t (x-s) := by
  unfold phaseCoboundary phase
  rw [← Complex.exp_add]
  congr 1
  rw [show x-(s+t) = x-s-t by ring]
  push_cast
  ring

theorem phaseCoboundary_unit (chi : ℝ → ℝ) (s x : ℝ) :
    ‖phaseCoboundary chi s x‖ = 1 := by
  simp [phaseCoboundary,phase,Complex.norm_exp]

theorem linear_phaseCoboundary (a s x : ℝ) :
    phaseCoboundary (fun y => a*y) s x = phase (a*s) := by
  unfold phaseCoboundary
  congr 1
  ring

theorem gauge_changes_boost_phase :
    phaseCoboundary (fun y => y) Real.pi 0 = -1 := by
  simpa [phase,phaseCoboundary] using Complex.exp_pi_mul_I

#print axioms strict_cocycle_is_coboundary
#print axioms phaseCoboundary_cocycle
#print axioms phaseCoboundary_unit
#print axioms linear_phaseCoboundary
#print axioms gauge_changes_boost_phase
end ChatgptAudit.CocycleGauge016


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
