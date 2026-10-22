-- KH-N1 proposta v392 (exame F_KERNEL 12/10/2026, so sandbox): o fecho TGL+TGLExt INTEIRO, no formato do #print axioms
import TGL
import TGLExt

open Lean Elab Command in
run_cmd do
  let env ← getEnv
  let mut n_decl := 0
  let mut n_thm := 0
  let mut n_fora := 0
  for (n, ci) in env.constants.map₁.toList do
    match env.getModuleIdxFor? n with
    | none => pure ()
    | some idx =>
      let m := env.header.moduleNames[idx.toNat]!
      if m.getRoot == `TGL || m.getRoot == `TGLExt then
        let axs ← liftCoreM (collectAxioms n)
        n_decl := n_decl + 1
        if ci matches .thmInfo _ then n_thm := n_thm + 1
        unless axs.all (fun a => a == `propext || a == `Classical.choice || a == `Quot.sound) do n_fora := n_fora + 1
        if axs.isEmpty then
          IO.println ("'" ++ n.toString ++ "' does not depend on any axioms")
        else
          IO.println ("'" ++ n.toString ++ "' depends on axioms: [" ++ String.intercalate ", " (axs.toList.map Name.toString) ++ "]")
  IO.println ("TGL_AXIOM_COVERAGE_TOTAL decl=" ++ toString n_decl ++ " thm=" ++ toString n_thm ++ " fora_do_trio=" ++ toString n_fora)
