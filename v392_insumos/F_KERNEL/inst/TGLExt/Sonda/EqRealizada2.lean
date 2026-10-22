-- SONDA 2 do exame F_KERNEL (12/10/2026), so no sandbox: realiza TGLExt.conjJ.eq_1 por simp (como o norm_num de
-- TheLightReadsItself) e lista o que o modulo contem.
import TGLExt.ConjugateAct
set_option autoImplicit false
namespace SondaEqRealizada2
theorem conjJ_simp (p : (Fin 1 → ℝ) × (Fin 1 → ℝ)) : (TGLExt.conjJ p).1 = (TGLExt.conjJ p).1 := by
  simp only [TGLExt.conjJ]
end SondaEqRealizada2
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  for n in [`TGLExt.conjJ.eq_1, `TGLExt.conjJ.eq_def] do
    IO.println ("SONDA_LOCAL\t" ++ n.toString ++ "\tcontem=" ++ toString (env.contains n))
