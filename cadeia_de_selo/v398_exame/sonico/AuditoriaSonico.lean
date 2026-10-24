import TGLExt.Sonico

/-! Exame independente (gerência c1, modelo forte, 23/10/2026) da pedra candidata `TGLExt.Sonico` (v398).
    Só lê o ambiente do sandbox k398: (1) toda constante do módulo, o tipo e os axiomas (`collectAxioms`); (2) as constantes
    que o TIPO de cada declaração usa (homônimos: qual `rhoOut`, `projPlus`, `rereading_adds_nothing`...), com o módulo que as
    define; (3) as constantes de fora do módulo que cada PROVA usa; (4) os homônimos de `rereading_adds_nothing` no ambiente;
    (5) os axiomas de `proposedCollapseCost` (o habitante da lei de custo). Depois, exemplos: a composição instanciada num espaço
    concreto com um vetor concreto e `proposedCollapseCost`, e as hipóteses internas descarregadas em θ = π/4 (não-vacuidade).
    Nada é declarado além dos `example`. -/

open Lean Elab Command

run_cmd do
  let env ← getEnv
  let some idx := env.getModuleIdx? `TGLExt.Sonico | throwError "modulo TGLExt.Sonico ausente"
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
    IO.println ("SON_AX\t" ++ n.toString ++ "\t" ++ kind ++ "\t" ++ toString n.isInternal ++ "\t" ++ String.intercalate "," (axs.toList.map Name.toString))
    -- as constantes do TIPO (o enunciado): e' aqui que um homonimo se esconderia
    for c in ci.type.getUsedConstants do
      let r := c.getRoot
      if r == `TGL || r == `TGLExt || r == `ChatgptAudit then
        IO.println ("SON_TIPO_USA\t" ++ n.toString ++ "\t" ++ c.toString ++ "\t" ++ modOf c)
    let cs := (match ci with
      | .thmInfo tv => tv.value.getUsedConstants
      | .defnInfo dv => dv.value.getUsedConstants
      | _ => #[])
    for c in cs do
      if env.getModuleIdxFor? c != some idx then
        let r := c.getRoot
        if r == `TGL || r == `TGLExt || r == `ChatgptAudit then
          usadosProva := usadosProva.insert c
  IO.println ("SON_TOTAL\tdecl=" ++ toString nTot ++ "\tthm=" ++ toString nThm ++ "\tfora_do_trio=" ++ toString nFora ++ "\tsorryAx=" ++ toString nSorry)
  for c in usadosProva.toList.toArray.qsort (fun a b => a.toString < b.toString) do
    IO.println ("SON_PROVA_USA\t" ++ c.toString ++ "\t" ++ modOf c)
  -- homonimos de rereading_adds_nothing e de rhoOut/diagExpect/projPlus/angFamily/select/post no ambiente
  for (n, ci) in env.constants.map₁.toList do
    let s := n.getString!
    if (s == "rereading_adds_nothing" || s == "rhoOut" || s == "diagExpect" || s == "projPlus" || s == "angFamily" || s == "select" || s == "post" || s == "ialdSelector" || s == "inscriptions" || s == "collapseEntropy" || s == "rhoParity") && !(n.isInternal) then
      let r := n.getRoot
      if r == `TGL || r == `TGLExt || r == `ChatgptAudit then
        IO.println ("SON_HOMONIMO\t" ++ n.toString ++ "\t" ++ modOf n ++ "\t" ++ toString ci.type.getForallBinderNames.length)
  -- o habitante da lei de custo
  let axsP ← liftCoreM (collectAxioms `ChatgptAudit.Collapse057.proposedCollapseCost)
  IO.println ("SON_HABITANTE\tChatgptAudit.Collapse057.proposedCollapseCost\t" ++ String.intercalate "," (axsP.toList.map Name.toString))
  -- a ponte ialdSelector = post (inscriptions 0): ja' existe como lema no ambiente?
  for (n, ci) in env.constants.map₁.toList do
    if !(n.isInternal) && env.getModuleIdxFor? n != some idx then
      let cs := ci.type.getUsedConstants
      if cs.contains `TGLExt.ialdSelector && cs.contains `TGLExt.TheVerbSelectsTheAction.post then
        IO.println ("SON_PONTE_EXISTENTE\t" ++ n.toString ++ "\t" ++ modOf n)

open ChatgptAudit.Collapse057 in
/-- a lei de custo e' habitada e os campos a determinam: o habitante paga ln 2 por oitava e 1/2 local -/
example : proposedCollapseCost.octaveNats 1 = Real.log 2 ∧ proposedCollapseCost.localNats = 1 / 2 :=
  ⟨by rw [proposedCollapseCost.per_octave 1]; simp, proposedCollapseCost.local_half⟩

open ChatgptAudit.Collapse057 in
/-- a composicao instanciada num espaco concreto (ℂ²), num vetor concreto e no habitante da lei de custo: nao e' vacua -/
example := TGLExt.Sonico.sonico_the_verb_pins_the_octave_and_the_cost_is_the_memory
  (H := EuclideanSpace ℂ (Fin 2)) (EuclideanSpace.single 0 1) proposedCollapseCost

open ChatgptAudit.Collapse057 in
/-- as hipoteses INTERNAS da composicao sao satisfativeis: em θ = π/4, cos² = sin² e sin(2θ) = 1 ≠ 0; logo a entropia do colapso
    do psibit nesse angulo E' o pedagio de uma oitava, e a paridade troca de sinal com θ ↦ -θ (consequencias extraidas da composicao) -/
example : TGLExt.Psibit.collapseEntropy (Real.pi / 4) = proposedCollapseCost.octaveNats 1 ∧
    ((TGLExt.Psibit.rhoParity (Real.pi / 4) = 1 ∧ TGLExt.Psibit.rhoParity (-(Real.pi / 4)) = -1)
      ∨ (TGLExt.Psibit.rhoParity (Real.pi / 4) = -1 ∧ TGLExt.Psibit.rhoParity (-(Real.pi / 4)) = 1)) := by
  have h := TGLExt.Sonico.sonico_the_verb_pins_the_octave_and_the_cost_is_the_memory
    (H := EuclideanSpace ℂ (Fin 2)) (EuclideanSpace.single 0 1) proposedCollapseCost
  obtain ⟨_, _, _, _, _, _, hbit, hbal, _, _, _⟩ := h
  have hcs : Real.cos (Real.pi / 4) ^ 2 = Real.sin (Real.pi / 4) ^ 2 := by
    rw [Real.cos_pi_div_four, Real.sin_pi_div_four]
  have hs : Real.sin (2 * (Real.pi / 4)) ≠ 0 := by
    have : 2 * (Real.pi / 4) = Real.pi / 2 := by ring
    rw [this, Real.sin_pi_div_two]; exact one_ne_zero
  exact ⟨hbal _ hcs, hbit _ hs⟩

open ChatgptAudit.Collapse057 in
/-- a oitava e' o dobro, lido no habitante: exp (ln 2) = 2 -/
example : Real.exp (proposedCollapseCost.octaveNats 1) = 2 :=
  TGLExt.Sonico.the_octave_is_a_doubling proposedCollapseCost

/-- o seletor pina num vetor concreto de ℂ² -/
example : TGLExt.TheVerbSelectsTheAction.select (EuclideanSpace.single (0 : Fin 2) (1 : ℂ)) (EuclideanSpace.single 0 1)
    = EuclideanSpace.single 0 1 :=
  (TGLExt.Sonico.the_selector_pins (EuclideanSpace.single 0 1)).2

#print axioms TGLExt.Sonico.sonico_the_verb_pins_the_octave_and_the_cost_is_the_memory
#print axioms ChatgptAudit.Collapse057.proposedCollapseCost
