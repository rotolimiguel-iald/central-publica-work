/- SONDA ADVERSARIAL do auditor REPRO (sandbox; nao e pedra): «prova que nao usa as hipoteses».
   Para cada TEOREMA da pedra (namespace TGLExt.TheUnitIsTheRank, nomes nao internos), abre o termo de prova
   (lambdaTelescope) e lista as hipoteses Prop do telescopio que o corpo NAO menciona (nem os tipos dos binders
   seguintes). Hipotese nao mencionada = hipotese sem peso no termo. -/
import TheUnitIsTheRank

open Lean Meta Elab Command

run_meta do
  let env ← getEnv
  let pre := `TGLExt.TheUnitIsTheRank
  let names := env.constants.fold
    (fun (acc : Array Name) n _ => if pre.isPrefixOf n && !n.isInternal then acc.push n else acc) #[]
  let names := names.qsort (fun a b => a.toString < b.toString)
  let mut nThm := 0
  let mut nHyp := 0
  let mut nDef := 0
  let mut semValor := 0
  let mut achados : Array (Name × Array Name) := #[]
  for nm in names do
    match env.find? nm with
    | some (.thmInfo v) =>
      nThm := nThm + 1
      let r ← lambdaTelescope v.value fun xs body => do
        let mut un : Array Name := #[]
        let mut k := 0
        for i in [0:xs.size] do
          let x := xs[i]!
          let ty ← inferType x
          if ← isProp ty then
            k := k + 1
            let fv := x.fvarId!
            let mut usadoDepois := false
            for j in [i+1:xs.size] do
              if (← inferType xs[j]!).containsFVar fv then
                usadoDepois := true
            if !(body.containsFVar fv) && !usadoDepois then
              un := un.push (← fv.getUserName)
        return (k, un)
      nHyp := nHyp + r.1
      if r.2.size > 0 then
        achados := achados.push (nm, r.2)
    | some (.defnInfo _) => nDef := nDef + 1
    | some _ => pure ()
    | none => semValor := semValor + 1
  logInfo m!"SONDA_HIPOTESES teoremas={nThm} defs={nDef} hipoteses_Prop_no_telescopio={nHyp} teoremas_com_hipotese_nao_mencionada={achados.size} sem_constante={semValor}"
  for (nm, un) in achados do
    logInfo m!"NAO_MENCIONADA {nm} : {un}"
