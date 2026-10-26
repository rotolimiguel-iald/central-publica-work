import TGLExt.ContratoQG_v31_Teoremas
import Lean
#print axioms TGLExt.ContratoQGv31.ContratoH2.Δit_determined
#print axioms TGLExt.ContratoQGv31.ContratoH2.Δit_index_free
#print axioms TGLExt.ContratoQGv31.ContratoH2.boostMat_det_isUnit
#print axioms TGLExt.ContratoQGv31.ContratoH2.feeds_finite_face
#print axioms TGLExt.ContratoQGv31.ContratoH2.det_unit_along_orbit
#print axioms TGLExt.ContratoQGv31.curvedFrame_not_dragged
#print axioms TGLExt.ContratoQGv31.curvedFrame_fiducial_not_modular
#print axioms TGLExt.ContratoQGv31.ContratoH2.frame_ne_curvedFrame_by_drag
#print axioms TGLExt.ContratoQGv31.ContratoH2.frame_ne_curvedFrame_by_fiducial


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
