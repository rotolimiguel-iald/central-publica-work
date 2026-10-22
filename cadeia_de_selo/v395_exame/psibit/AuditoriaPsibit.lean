import TGLExt.Psibit

/-! Exame independente (gerência c1, modelo forte, 21/10/2026) da pedra candidata `TGLExt.Psibit`.
    Só lê o ambiente: (1) toda constante do módulo, o tipo e os axiomas (`collectAxioms`); (2) as constantes de FORA do módulo que
    cada declaração usa diretamente, com o módulo que as define (citações e homônimos); (3) quem, no ambiente, devolve um
    `FockCertificate` (para saber se a hipótese da composição é habitada). Nada é declarado. -/

open Lean Elab Command

run_cmd do
  let env ← getEnv
  let some idx := env.getModuleIdx? `TGLExt.Psibit | throwError "modulo TGLExt.Psibit ausente"
  let modOf : Name → String := fun n =>
    match env.getModuleIdxFor? n with
    | some i => (env.header.moduleNames[i.toNat]!).toString
    | none => "<este arquivo>"
  let mut nomes : Array Name := #[]
  for (n, _) in env.constants.map₁.toList do
    if env.getModuleIdxFor? n == some idx then
      nomes := nomes.push n
  let nomesOrd := nomes.qsort (fun a b => a.toString < b.toString)
  let mut nTot := 0
  let mut nThm := 0
  let mut nFora := 0
  let mut nSorry := 0
  let mut usados : NameSet := {}
  for n in nomesOrd do
    let some ci := env.find? n | continue
    let kind := match ci with
      | .axiomInfo _ => "axiom" | .defnInfo _ => "def" | .thmInfo _ => "theorem" | .opaqueInfo _ => "opaque"
      | .quotInfo _ => "quot" | .inductInfo _ => "inductive" | .ctorInfo _ => "ctor" | .recInfo _ => "rec"
    let axs ← liftCoreM (collectAxioms n)
    nTot := nTot + 1
    if kind == "theorem" then nThm := nThm + 1
    unless axs.all (fun a => a == `propext || a == `Classical.choice || a == `Quot.sound) do nFora := nFora + 1
    if axs.contains `sorryAx then nSorry := nSorry + 1
    IO.println ("PSIBIT_AX\t" ++ n.toString ++ "\t" ++ kind ++ "\t" ++ toString n.isInternal ++ "\t" ++ String.intercalate "," (axs.toList.map Name.toString))
    let cs := ci.type.getUsedConstants ++ (match ci with
      | .thmInfo tv => tv.value.getUsedConstants
      | .defnInfo dv => dv.value.getUsedConstants
      | _ => #[])
    for c in cs do
      if env.getModuleIdxFor? c != some idx then
        let r := c.getRoot
        if r == `TGL || r == `TGLExt || r == `ChatgptAudit then
          usados := usados.insert c
  IO.println ("PSIBIT_TOTAL\tdecl=" ++ toString nTot ++ "\tthm=" ++ toString nThm ++ "\tfora_do_trio=" ++ toString nFora ++ "\tsorryAx=" ++ toString nSorry)
  for c in usados.toList.toArray.qsort (fun a b => a.toString < b.toString) do
    IO.println ("PSIBIT_USA\t" ++ c.toString ++ "\t" ++ modOf c)
  -- quem devolve um FockCertificate (a hipótese da composição)
  let alvo := `TGLExt.ImportedSQ.FockCertificate
  IO.println ("PSIBIT_FOCK_EXISTE\t" ++ toString (env.contains alvo))
  for (n, ci) in env.constants.map₁.toList do
    let concl := ci.type.getForallBody
    if concl.getAppFn.constName? == some alvo && !(n.isInternal) then
      let kind := match ci with | .defnInfo _ => "def" | .thmInfo _ => "theorem" | .opaqueInfo _ => "opaque" | .axiomInfo _ => "axiom" | .ctorInfo _ => "ctor" | _ => "outro"
      IO.println ("PSIBIT_FOCK_PRODUTOR\t" ++ n.toString ++ "\t" ++ kind ++ "\t" ++ modOf n ++ "\t" ++ toString (ci.type.getForallBinderNames.length))

  -- habitantes: algum termo do ambiente cujo TIPO mencione FockCertificate dentro de Nonempty / Inhabited / Exists?
  for (n, ci) in env.constants.map₁.toList do
    let concl := ci.type.getForallBody
    let h := concl.getAppFn.constName?
    if (h == some ``Nonempty || h == some ``Inhabited || h == some ``Exists) && (concl.getUsedConstants.contains alvo) && !(n.isInternal) then
      IO.println ("PSIBIT_FOCK_HABITANTE	" ++ n.toString ++ "	" ++ modOf n)
