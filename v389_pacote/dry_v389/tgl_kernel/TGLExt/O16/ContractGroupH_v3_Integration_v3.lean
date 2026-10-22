-- predecessor SHA256 dd5249fa3dd2c17f58afd02519456e4f2ec37ba11a4f813007dd9d4d2fac8809
import TGLExt.ContratoQG_v31_Teoremas
import Lean
#print axioms TGLExt.ContratoQGv31.shift_point
#print axioms TGLExt.ContratoQGv31.nullPlaneCharge_of_zero
#print axioms TGLExt.ContratoQGv31.nullEnergy_vac
#print axioms TGLExt.ContratoQGv31.nullEnergy_covariant
#print axioms TGLExt.ContratoQGv31.areaDensity_smul
#print axioms TGLExt.ContratoQGv31.ContratoH3.response_vac
#print axioms TGLExt.ContratoQGv31.ContratoH3.response_covariant_v31
#print axioms TGLExt.ContratoQGv31.ContratoH3.same_source_same_geometry
#print axioms TGLExt.ContratoQGv31.ContratoH3.theta_along
#print axioms TGLExt.ContratoQGv31.ContratoH3.theta_deriv_along
#print axioms TGLExt.ContratoQGv31.ContratoH3.first_law_window
#print axioms TGLExt.ContratoQGv31.ContratoH3.bekenstein_hawking_window
#print axioms TGLExt.ContratoQGv31.ContratoH3.clausius_window
#print axioms TGLExt.ContratoQGv31.ContratoH3.einstein_coefficient_window
#print axioms TGLExt.ContratoQGv31.ContratoH3.kappa_cancels_window
#print axioms TGLExt.ContratoQGv31.ContratoH3.nontrivial_null_energy
#print axioms TGLExt.ContratoQGv31.ContratoH3.expansion_not_constant
#print axioms TGLExt.ContratoQGv31.ContratoH3.response_not_identically_zero
#print axioms TGLExt.ContratoQGv31.ContratoH3.slope_response_excluded
#print axioms TGLExt.ContratoQGv31.ContratoH3.exp_response_excluded
#print axioms TGLExt.ContratoQGv31.ContratoH3.slope_propagator_excluded
#print axioms TGLExt.ContratoQGv31.ContratoH3.exp_propagator_excluded
#print axioms TGLExt.ContratoQGv31.ContratoH3.rescaleG
#print axioms TGLExt.ContratoQGv31.ContratoH3.G_not_predicted


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
