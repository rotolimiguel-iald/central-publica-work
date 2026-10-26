import TGLExt.F1Fecho394.CanonicalModularCoreAssemblyR1
import TGLExt.F1Fecho394.CanonicalFockWeightClosedTomitaR2
import TGLExt.F1Fecho394.OrbitalSpatialCovarianceR2
import TGLExt.F1Fecho394.OrbitalSpatialContinuityR1
import TGLExt.F1Fecho394.AnnihilationDomainR1
import TGLExt.F1Fecho394.CanonicalFockGNSNormalityR4
import TGLExt.F1Fecho394.RootRateFrequencyR2
import TGLExt.F1Fecho394.DeviceRootObstructionR4
import TGLExt.F1Fecho394.CreationAndSegalR2
import TGLExt.F1Fecho394.WeylSegalDenseDomainR5
import TGLExt.F1Fecho394.LorentzFutureRepresentationR1
import TGLExt.F1Fecho394.CanonicalFockWeightStandardSubspaceR2
import TGLExt.F1Fecho394.CanonicalFockWeightModularFlowR3
import TGLExt.F1Fecho394.CanonicalSegalEssentialR6
import Lean

open Lean in
run_cmd do
  let env ← Elab.Command.liftCoreM getEnv
  let mut count := 0
  for (n, ci) in env.constants.toList do
    if let some idx := env.getModuleIdxFor? n then
      let mod := env.header.moduleNames[idx]!
      if (`TGLExt.F1Fecho394).isPrefixOf mod then
        count := count + 1
        let axs ← collectAxioms n
        IO.println ("BUNDLE_DECL\t" ++ n.toString ++ "\t" ++ mod.toString ++ "\t" ++ String.intercalate "," (axs.toList.map Name.toString))
        unless axs.all (fun a => a == `propext || a == `Classical.choice || a == `Quot.sound) do
          throwError "AXIOM_AUDIT_REFUSED: {n}"
        match ci with
        | .axiomInfo _ => throwError "LOCAL_AXIOM_REFUSED: {n}"
        | _ => pure ()
  if count == 0 then throwError "EMPTY_AUDIT_REFUSED"
  IO.println ("BUNDLE_COUNT\t" ++ toString count)
