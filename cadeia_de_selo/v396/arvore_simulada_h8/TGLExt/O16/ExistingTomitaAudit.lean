import Lean
import TGLExt.ContinuousModularReconstruction
import TGLExt.O16.KMSStripConditional

/- Consumer only: the response's proposed closed-Tomita lemma already exists.
No duplicate theorem, new assumption, regional algebra, or chosen partition. -/
#print axioms ChatgptAudit.Continuous049.continuous_tomita_domain_dense
#print axioms ChatgptAudit.Continuous049.continuous_tomita_closed
#print axioms ChatgptAudit.Continuous049.continuous_tomita_involutive
#print axioms ChatgptAudit.Continuous049.continuous_J_tomita_eq_modular
#print axioms ChatgptAudit.Continuous050.continuous_delta_graph_iff_tomita_comp
#print axioms ChatgptAudit.KMSStrip016.kms_rescale_existing
#print axioms ChatgptAudit.KMSStrip016.boost_rapidity_kms_from_modular
#print axioms ChatgptAudit.KMSStrip016.killing_kms_from_modular


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
