import Lean
import TGLExt.O16.OrbitalStateAnalytic
import TGLExt.O16.ContratoQG_v31_Minimal

set_option autoImplicit false
noncomputable section
open MeasureTheory
open scoped InnerProductSpace
namespace ChatgptAudit.WignerRapidityMeasure016
open TGLExt.ContratoQGv31 TGL.SpecificAQFT

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℂ E]

/-- Matches the analytic conclusion of PositiveEnergy, with the actual orbital
translations and the existing forwardCone/upperHalf. It does not insert a
one-particle vector into the reserved AQFT witness or fabricate a vacuum. -/
theorem orbital_positive_energy_v31_shape (m : ℝ) (a : Fin 4 → ℝ)
    (ha : a ∈ forwardCone) (f : Lp E 2 (orbitalMeasure m)) : ∃ F : ℂ → ℂ,
      DiffContOnCl ℂ F upperHalf ∧
      (∃ M : ℝ, ∀ z : ℂ, 0 ≤ z.im → ‖F z‖ ≤ M) ∧
      (∀ t : ℝ, F t = ⟪f, orbitalTranslation m (t • a) f⟫_ℂ) := by
  have ha' : a 1^2+a 2^2+a 3^2 ≤ a 0^2 := by
    have h := ha.2
    unfold minkowskiSq at h
    linarith
  exact orbital_positive_energy_analytic m a ha.1 ha' f

#print axioms orbital_positive_energy_v31_shape
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
