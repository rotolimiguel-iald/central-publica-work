-- COB v392 (cadeia v392, 13/10/2026): enumera as declaracoes das pedras de STONES (14 na rodada 2) e a cobertura de axiomas (collectAxioms). Instrumento de medida; so no sandbox.
import TGL
import TGLExt
import TGLExt.Palavra
import TGLExt.LiganteLeiCampoCurvo
import TGLExt.LiganteLeiCampoCurvoTestemunha
import TGLExt.V351DualScalingBridge
import TGLExt.AgapeNonVacuity
import TGLExt.TheSingularityReadsTheAttractorAdendo1
import TGLExt.OpticalPopulationBridgeR2
import TGLExt.TheLightReadsItself
import TGLExt.LightNetStandardWedgeDataBGL
import TGLExt.Posto
import TGLExt.PostoAdendo
import TGLExt.Santo
import TGLExt.IALD
import TGLExt.Verdade

open Lean Elab Command

run_cmd do
  let env ← getEnv
  let alvo : List Name := [`TGLExt.Palavra, `TGLExt.LiganteLeiCampoCurvo, `TGLExt.LiganteLeiCampoCurvoTestemunha, `TGLExt.V351DualScalingBridge, `TGLExt.AgapeNonVacuity, `TGLExt.TheSingularityReadsTheAttractorAdendo1, `TGLExt.OpticalPopulationBridgeR2, `TGLExt.TheLightReadsItself, `TGLExt.LightNetStandardWedgeDataBGL, `TGLExt.Posto, `TGLExt.PostoAdendo, `TGLExt.Santo, `TGLExt.IALD, `TGLExt.Verdade]
  let mut n_decl := 0
  let mut n_thm := 0
  let mut n_fora := 0
  for (n, ci) in env.constants.map₁.toList do
    match env.getModuleIdxFor? n with
    | none => pure ()
    | some idx =>
      let m := env.header.moduleNames[idx.toNat]!
      if alvo.contains m then
        let axs ← liftCoreM (collectAxioms n)
        let kind : String := match ci with
          | .thmInfo _ => "thm" | .defnInfo _ => "def" | .axiomInfo _ => "AXIOM"
          | .opaqueInfo _ => "opaque" | .quotInfo _ => "quot" | .inductInfo _ => "induct"
          | .ctorInfo _ => "ctor" | .recInfo _ => "rec"
        n_decl := n_decl + 1
        if kind == "thm" then n_thm := n_thm + 1
        let ok := axs.all (fun a => a == `propext || a == `Classical.choice || a == `Quot.sound)
        unless ok do n_fora := n_fora + 1
        IO.println ("COB	" ++ m.toString ++ "	" ++ n.toString ++ "	" ++ kind ++ "	" ++ (if ok then "TRIO" else "FORA") ++ "	" ++ String.intercalate "," (axs.toList.map Name.toString))
  IO.println ("COB_TOTAL	decl=" ++ toString n_decl ++ "	thm=" ++ toString n_thm ++ "	fora_do_trio=" ++ toString n_fora)
