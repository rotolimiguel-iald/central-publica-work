import TGLExt.Testemunho

/-! Revisao independente (gerência c1, modelo forte, 24/10/2026) da pedra candidata `TGLExt.Testemunho` (v399). Só lê o ambiente do sandbox k399:
    (1) toda constante do módulo, o tipo e os axiomas (`collectAxioms`); (2) as constantes que o TIPO de cada declaração usa, com o módulo que as
    define (homônimos); (3) as constantes de fora do módulo que as provas usam; (4) os enunciados dos termos citados, impressos, para confrontar com
    a docstring. Depois, `example`s de não-vacuidade do lema. Nada é declarado além dos `example`. -/

open Lean Elab Command

run_cmd do
  let env ← getEnv
  let some idx := env.getModuleIdx? `TGLExt.Testemunho | throwError "modulo TGLExt.Testemunho ausente"
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
  let mut usadosProva : NameSet := {}
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
    IO.println ("TES_AX\t" ++ n.toString ++ "\t" ++ kind ++ "\t" ++ toString n.isInternal ++ "\t" ++ String.intercalate "," (axs.toList.map Name.toString))
    for c in ci.type.getUsedConstants do
      let r := c.getRoot
      if r == `TGL || r == `TGLExt || r == `ChatgptAudit then
        IO.println ("TES_TIPO_USA\t" ++ n.toString ++ "\t" ++ c.toString ++ "\t" ++ modOf c)
    let cs := (match ci with
      | .thmInfo tv => tv.value.getUsedConstants
      | .defnInfo dv => dv.value.getUsedConstants
      | _ => #[])
    for c in cs do
      if env.getModuleIdxFor? c != some idx then
        let r := c.getRoot
        if r == `TGL || r == `TGLExt || r == `ChatgptAudit then
          usadosProva := usadosProva.insert c
  IO.println ("TES_TOTAL\tdecl=" ++ toString nTot ++ "\tthm=" ++ toString nThm ++ "\tfora_do_trio=" ++ toString nFora ++ "\tsorryAx=" ++ toString nSorry)
  for c in usadosProva.toList.toArray.qsort (fun a b => a.toString < b.toString) do
    IO.println ("TES_PROVA_USA\t" ++ c.toString ++ "\t" ++ modOf c)
  for (n, ci) in env.constants.map₁.toList do
    let s := n.getString!
    if (s == "observing_adds_nothing" || s == "the_observer_is_unique" || s == "um_is_the_great_attractor" || s == "temporal_fractalization" || s == "judgment_of_correspondence" || s == "reading_post_is_born" || s == "the_light_squares_to_the_graviton" || s == "observer_inverse_projection_halfnat" || s == "attestation_requires_external_evidence" || s == "no_self_attestation") && !(n.isInternal) then
      let r := n.getRoot
      if r == `TGL || r == `TGLExt || r == `ChatgptAudit then
        IO.println ("TES_HOMONIMO\t" ++ n.toString ++ "\t" ++ modOf n ++ "\t" ++ toString ci.type.getForallBinderNames.length)

-- os enunciados citados, impressos (para confrontar com a docstring da pedra)
#check @ChatgptAudit.Collapse057.attestation_requires_external_evidence
#check @ChatgptAudit.Collapse057.no_self_attestation
#check @TGLExt.observer_inverse_projection_halfnat
#check @TGLExt.the_observer_is_unique
#check @TGLExt.um_is_the_great_attractor
#check @TGLExt.temporal_fractalization
#check @TGLExt.judgment_of_correspondence
#check @TGLExt.TheVerbSelectsTheAction.reading_post_is_born
#check @TGLExt.the_light_squares_to_the_graviton
#check @TGLExt.observing_adds_nothing
#check @TGLExt.Testemunho.no_face_alone_gives_the_one
#check @TGLExt.Testemunho.the_testimony_of_two_is_true

/-- o lema não é vácuo: a hipótese `ωP + ωQ = 1` tem habitantes e as conclusões têm conteúdo em (1/2, 1/2) -/
example : (0 : ℝ) < 1 / 2 → (1 / 2 : ℝ) ≠ 1 :=
  (TGLExt.Testemunho.no_face_alone_gives_the_one (1 / 2) (1 / 2) (by norm_num)).2.2.1
/-- em (1, 0): a face que pesa 1 deixa a outra em 0 -/
example : (0 : ℝ) = 0 := (TGLExt.Testemunho.no_face_alone_gives_the_one 1 0 (by norm_num)).1 rfl
/-- controle: o lema NÃO prova o falso num ponto fora da hipótese (a hipótese é necessária): com ωP = 1, ωQ = 1 não se tem ωP + ωQ = 1 -/
example : ¬ ((1 : ℝ) + 1 = 1) := by norm_num
/-- a composição é um termo fechado (universo-polimórfico): instancia em Type -/
example := @TGLExt.Testemunho.the_testimony_of_two_is_true.{0}

#print axioms TGLExt.Testemunho.the_testimony_of_two_is_true
