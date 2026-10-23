import Lean
import TGLExt.ContratoQG_v31_Teoremas
import TGLExt.O16.PolarMinimalPeriod_v2
set_option autoImplicit false
set_option maxHeartbeats 1000000
noncomputable section
namespace TGLExt.ContratoQGv31
open TGL.SpecificAQFT TGL.ModularRealization
open MeasureTheory Matrix Complex Filter Topology
open scoped InnerProductSpace
namespace ContratoH3
variable {W : TGLSpecificAQFTWitness} {R : TGLModularRealization W}
  {N : KillingNormalization} {T : StressTensorData W}
/-- The exported data uses exactly this H3 contract's H2 horizon. -/
theorem data_fields_same_horizon (C : ContratoH3 W R N T)
    {psi : W.H} (hpsi : psi ∈ C.admissible) (x : Fin 4 → ℝ)
    (c d : ℝ) (htheta : C.theta psi (x+d • nullDir)=0) :
    (C.toHorizonData hpsi x c d htheta).kappa=C.H2.kappa ∧
    (C.toHorizonData hpsi x c d htheta).G=C.G ∧
    (C.toHorizonData hpsi x c d htheta).dS=2*Real.pi*windowCharge T psi x c d :=
  ⟨rfl,rfl,rfl⟩

theorem data_temperature_from_same_period (C : ContratoH3 W R N T)
    {psi : W.H} (hpsi : psi ∈ C.admissible) (x : Fin 4 → ℝ)
    (c d period : ℝ) (htheta : C.theta psi (x+d • nullDir)=0)
    (hp : 0 < period)
    (hperiod : ChatgptAudit.PolarPeriod016.AngularQuotientFaithful C.H2.kappa period) :
    (C.toHorizonData hpsi x c d htheta).kappa/(2*Real.pi)=1/period :=
  (ChatgptAudit.PolarPeriod016.reciprocal_temperature C.H2.kappa_pos hp hperiod).symm

#print axioms theta_along
#print axioms theta_deriv_along
#print axioms first_law_window
#print axioms bekenstein_hawking_window
#print axioms clausius_window
#print axioms einstein_coefficient_window
#print axioms toHorizonData
#print axioms feeds_the_master
#print axioms data_fields_same_horizon
#print axioms data_temperature_from_same_period
end ContratoH3
#print axioms shift_point
end TGLExt.ContratoQGv31


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
