import Mathlib.Tactic
theorem x_sorry : False := by sorry
theorem y_ok : 1 + 1 = 2 := by norm_num

-- RODAPE B (v392; conserto B da PROPOSTA_V392): o axioma de TODA declaracao deste modulo, no formato do #print axioms
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  let mut n_decl := 0
  let mut n_fora := 0
  for (n, _) in env.constants.map₂.toList do
    let axs ← liftCoreM (collectAxioms n)
    n_decl := n_decl + 1
    unless axs.all (fun a => a == `propext || a == `Classical.choice || a == `Quot.sound) do n_fora := n_fora + 1
    if axs.isEmpty then
      IO.println ("'" ++ n.toString ++ "' does not depend on any axioms")
    else
      IO.println ("'" ++ n.toString ++ "' depends on axioms: [" ++ String.intercalate ", " (axs.toList.map Name.toString) ++ "]")
  IO.println ("TGL_FOOTER_B_TOTAL decl=" ++ toString n_decl ++ " fora_do_trio=" ++ toString n_fora)
