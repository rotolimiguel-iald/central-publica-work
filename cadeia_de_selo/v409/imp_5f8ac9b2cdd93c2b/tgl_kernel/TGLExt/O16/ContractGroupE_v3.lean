import TGLExt.ContratoQG_v31_Teoremas
import Lean
#print axioms TGLExt.ContratoQGv31.ContratoH2.modular_is_boost_at_two_pi
#print axioms TGLExt.ContratoQGv31.ContratoH2.unruh_is_kms
#print axioms TGLExt.ContratoQGv31.ContratoH2.unruh_is_kms_temperature
#print axioms TGLExt.ContratoQGv31.ContratoH2.kms_product_is_two_pi
#print axioms TGLExt.ContratoQGv31.ContratoH2.refRadius
#print axioms TGLExt.ContratoQGv31.ContratoH2.refRadius_pos
#print axioms TGLExt.ContratoQGv31.ContratoH2.kappa_mul_radius
#print axioms TGLExt.ContratoQGv31.ContratoH2.kappa_eq_inv_radius
#print axioms TGLExt.ContratoQGv31.ContratoH2.kappa_fixed
#print axioms TGLExt.ContratoQGv31.ContratoH2.no_rekappa
#print axioms TGLExt.ContratoQGv31.ContratoH2.observer_unit_of_index
#print axioms TGLExt.ContratoQGv31.ContratoH2.reindex
#print axioms TGLExt.ContratoQGv31.ContratoH2.kappa_is_input
#print axioms TGLExt.ContratoQGv31.ContratoH2.killingFlow_add
#print axioms TGLExt.ContratoQGv31.ContratoH2.killingFlow_zero
#print axioms TGLExt.ContratoQGv31.ContratoH2.modularEnergy_of_boostEnergy
#print axioms TGLExt.ContratoQGv31.ContratoH2.modularEnergy_unique
#print axioms TGLExt.ContratoQGv31.ContratoH2.vac_modularEnergy
#print axioms TGLExt.ContratoQGv31.ContratoH2.vac_boostEnergy
#print axioms TGLExt.ContratoQGv31.ContratoH2.inner_vac_Δit
#print axioms TGLExt.ContratoQGv31.ContratoH2.bilateral_no_first_order


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
