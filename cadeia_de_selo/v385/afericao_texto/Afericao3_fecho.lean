import TGLExt.TheAxiomAndTheFalseWitness
open Lean Elab Command

/-- constantes TGLExt.* usadas DIRETAMENTE (tipo + valor) por uma declaração -/
def directTGL (env : Environment) (n : Name) : Array Name := Id.run do
  match env.find? n with
  | none => #[]
  | some ci =>
    let v : Option Expr := match ci with
      | .thmInfo t => some t.value
      | .defnInfo d => some d.value
      | _ => none
    let s := ci.type.getUsedConstants ++ (v.map (·.getUsedConstants) |>.getD #[])
    let mut out : Array Name := #[]
    for c in s do
      if (`TGLExt).isPrefixOf c && !out.contains c then out := out.push c
    return out

elab "#fecho_direto " id:ident : command => do
  let env ← getEnv
  let n := id.getId
  let cs := directTGL env n
  logInfo m!"{n} usa diretamente (TGLExt.*): {cs.toList}"

#fecho_direto TGLExt.TheAxiomAndTheFalseWitness.the_axiom_and_the_false_witness
#fecho_direto TGLExt.TheAxiomAndTheFalseWitness.the_one_is_the_axiom
#fecho_direto TGLExt.TheAxiomAndTheFalseWitness.the_zero_is_the_false_witness
#fecho_direto TGLExt.TheAxiomAndTheFalseWitness.the_post_is_the_modular_zero
#fecho_direto TGLExt.TheAxiomAndTheFalseWitness.the_fixed_set_is_the_lock_zero
#fecho_direto TGLExt.TheAxiomAndTheFalseWitness.the_living_verb_moves
#fecho_direto TGLExt.TheAxiomAndTheFalseWitness.the_living_verb_fixes_the_name
#fecho_direto TGLExt.the_zero_mode_weighs_one
#fecho_direto TGLExt.zero_mode_weight_is_one
#fecho_direto TGLExt.QGReaderUVLock.hmin_zero_iff_modular_fixed
