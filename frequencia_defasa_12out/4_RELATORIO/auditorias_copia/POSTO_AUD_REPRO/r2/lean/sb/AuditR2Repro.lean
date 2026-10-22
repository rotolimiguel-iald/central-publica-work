import TheUnitIsTheRank

/-!
# Auditoria REPRO r2 (auditor independente) — enumeracao PELO AMBIENTE, nao por regex no fonte.
Para CADA constante que o modulo `TheUnitIsTheRank` acrescentou ao ambiente (inclusive auxiliares geradas pelo
elaborador): axiomas coletados por `Lean.collectAxioms`; acusa qualquer axioma fora de {propext, Classical.choice,
Quot.sound} (sorryAx inclusive), qualquer `axiom` declarado, constante `unsafe`/`partial`, `implemented_by` e `extern`.
-/

open Lean Elab Command

#eval show CommandElabM Unit from do
  let env ← getEnv
  let some idx := env.getModuleIdx? `TheUnitIsTheRank | throwError "modulo TheUnitIsTheRank nao achado"
  let names := env.header.moduleData[idx.toNat]!.constNames
  let trio : Array Name := #[``propext, ``Classical.choice, ``Quot.sound]
  let mut fora : Array (Name × Array Name) := #[]
  let mut axiomasDecl : Array Name := #[]
  let mut inseguras : Array Name := #[]
  let mut implBy : Array Name := #[]
  let mut externs : Array Name := #[]
  let mut nThm := 0
  let mut nDef := 0
  let mut nOutro := 0
  let mut nUser := 0
  let mut usados : Array Name := #[]
  for n in names do
    let some ci := env.find? n | throwError m!"constante sumiu: {n}"
    match ci with
    | .axiomInfo _ => axiomasDecl := axiomasDecl.push n
    | _ => pure ()
    if ci.isUnsafe || ci.isPartial then inseguras := inseguras.push n
    if (Compiler.implementedByAttr.getParam? env n).isSome then implBy := implBy.push n
    if isExtern env n then externs := externs.push n
    let axs ← liftCoreM (Lean.collectAxioms n)
    for a in axs do
      if !usados.contains a then usados := usados.push a
    let extra := axs.filter (fun a => !trio.contains a)
    if extra.size > 0 then fora := fora.push (n, extra)
    -- declaracoes "de usuario": nome sem componente interno (_proof, eq_, match_, _aux, _sunfold, ...)
    let interno := n.isInternal || n.components.any (fun c => c.toString.startsWith "eq_" ||
      c.toString.startsWith "match_" || c.toString == "eq_def" || c.toString.startsWith "_")
    if !interno then
      nUser := nUser + 1
      match ci with
      | .thmInfo _ => nThm := nThm + 1
      | .defnInfo _ => nDef := nDef + 1
      | _ => nOutro := nOutro + 1
  logInfo m!"AUDIT_CONSTANTES_NO_MODULO {names.size}"
  logInfo m!"AUDIT_DECLARACOES_DE_USUARIO {nUser} (theorem {nThm}, def {nDef}, outras {nOutro})"
  logInfo m!"AUDIT_AXIOMAS_USADOS_NO_MODULO {usados}"
  logInfo m!"AUDIT_FORA_DO_TRIO {fora.size} {fora}"
  logInfo m!"AUDIT_AXIOMAS_DECLARADOS {axiomasDecl.size} {axiomasDecl}"
  logInfo m!"AUDIT_UNSAFE_OU_PARTIAL {inseguras.size} {inseguras}"
  logInfo m!"AUDIT_IMPLEMENTED_BY {implBy.size} {implBy}"
  logInfo m!"AUDIT_EXTERN {externs.size} {externs}"

-- Os enunciados centrais com nomes COMPLETOS (fidelidade: Matrix.rank e a da Mathlib; dephase/diagExpect/rhoOut/
-- Smat/thetaMiguel/TGLCoupling sao os do kernel do Nos)
set_option pp.fullNames true
open TGLExt.TheUnitIsTheRank in
section
#check @pure_iff_rank_one
#check @pure_iff_rank_one_fin_two
#check @rankOne_density
#check @rank_add_nullity
#check @trace_eq_rank_of_projection
#check @name_meets_rank_only_at_the_atom
#check @rhoStar_unit
#check @range_rhoStar
#check @compression_by_rank_one
#check @reading_of_the_attractor_state
#check @anticomm_zero_iff
#check @anticomm_at_thetaMiguel
#check @leak_eq
#check @leak_at_thetaMiguel
#check @ad_rank
#check @fractal_one_is_rank_one
#check @endpoint_rank_two_iff
#check @endpoint_at_thetaMiguel
#check @dephased_rank_two_iff
#check @rank_not_preserved_by_dephasing
#check @leak_survives_dephasing
#check @anticomm_dephased_zero_iff
#check @Smat_pow
#check @angular_leak_no_limit
#check @dephasing_trivial_iff
#check @literal_transmission_does_not_force_dephasing
#check @literal_leak_does_not_force_dephasing
#check @dephasing_acts_iff_transmits_and_leaks
#check @inscription_at_thetaMiguel
#check @dephasingActs_iff_forward
#check @one_sub_rhoOut_eq_Qtheta_neg
#print rhoStar
#print Qtheta
#print dephasingActs
#print nullity
end
