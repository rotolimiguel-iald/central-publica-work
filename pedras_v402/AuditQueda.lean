import TGLExt.QuedaSemGeometria

-- Audit incremental v402: axioma de TODA constante do modulo TGLExt.QuedaSemGeometria (formato do Audit.lean)
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  let mut n_decl := 0
  let mut n_thm := 0
  let mut n_fora := 0
  let mut n_sorry := 0
  for (n, ci) in env.constants.map₁.toList do
    match env.getModuleIdxFor? n with
    | none => pure ()
    | some idx =>
      let m := env.header.moduleNames[idx.toNat]!
      if m == `TGLExt.QuedaSemGeometria then
        let axs ← liftCoreM (collectAxioms n)
        n_decl := n_decl + 1
        if ci matches .thmInfo _ then n_thm := n_thm + 1
        unless axs.all (fun a => a == `propext || a == `Classical.choice || a == `Quot.sound) do n_fora := n_fora + 1
        if axs.contains `sorryAx then n_sorry := n_sorry + 1
        IO.println ("'" ++ n.toString ++ "' depends on axioms: [" ++ String.intercalate ", " (axs.toList.map Name.toString) ++ "]")
  IO.println ("QUEDA_AXIOM_COVERAGE decl=" ++ toString n_decl ++ " thm=" ++ toString n_thm ++ " fora_do_trio=" ++ toString n_fora ++ " sorry=" ++ toString n_sorry)
