import Lean
import TGLExt.O16.ProductOrbitalSpectrum_v3

set_option autoImplicit false
noncomputable section
open MeasureTheory Filter
open scoped ENNReal
namespace ChatgptAudit.WignerRapidityMeasure016
variable {E : Type*} [NormedAddCommGroup E] [NormedSpace ℂ E]

/-- Norm preservation suffices; no trivialization of a helicity cocycle is assumed.
The hypothesis specifies a candidate eigenvector through its almost-everywhere action.
It does not construct the physical helicity representation or its measurability. -/
theorem isometric_fiber_shift_no_eigen
    (C : ℝ → MomentumCoordinates → (E →ₗᵢ[ℂ] E))
    (f : Lp E 2 momentumMeasure)
    (h : ∀ s : ℝ, ∃ c : ℂ, ‖c‖=1 ∧
      (fun y => C s y (f (coordinateShift (-s) y))) =ᵐ[momentumMeasure]
        (fun y => c • f y)) : f=0 := by
  apply product_norm_periodic_zero f
  intro n
  obtain ⟨c,hc,he⟩ := h (-(n : ℝ))
  filter_upwards [he] with y hy
  have hn := congrArg (fun z : E => ‖z‖) hy
  simp only [LinearIsometry.norm_map, norm_smul, hc, one_mul,
    coordinateShift, neg_neg] at hn
  simpa only [← ofReal_norm] using congrArg ENNReal.ofReal hn

/-- Integer shifts alone already rule out a nonzero finite-norm eigenvector. -/
theorem integer_isometric_fiber_shift_no_eigen
    (C : ℤ → MomentumCoordinates → (E →ₗᵢ[ℂ] E))
    (f : Lp E 2 momentumMeasure)
    (h : ∀ n : ℤ, ∃ c : ℂ, ‖c‖=1 ∧
      (fun y => C n y (f (y.1,y.2+n))) =ᵐ[momentumMeasure]
        (fun y => c • f y)) : f=0 := by
  apply product_norm_periodic_zero f
  intro n
  obtain ⟨c,hc,he⟩ := h n
  filter_upwards [he] with y hy
  have hn := congrArg (fun z : E => ‖z‖) hy
  simp only [LinearIsometry.norm_map, norm_smul, hc, one_mul] at hn
  simpa only [← ofReal_norm] using congrArg ENNReal.ofReal hn

#print axioms isometric_fiber_shift_no_eigen
#print axioms integer_isometric_fiber_shift_no_eigen
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
