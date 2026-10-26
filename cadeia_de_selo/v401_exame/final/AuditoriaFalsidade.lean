import TGLExt.FalsidadeDaInercia

/-! Revisao independente (gerência c1, modelo forte, 25/10/2026) da pedra `TGLExt.FalsidadeDaInercia` (v401). Só lê o ambiente do sandbox k401c
    (`lake env lean` sobre este arquivo, fora da árvore): (1) toda constante do módulo, o tipo e os axiomas (`collectAxioms`); (2) as constantes
    que o TIPO de cada declaração usa, com o módulo que as define; (3) as constantes de fora do módulo que as provas usam; (4) os enunciados dos
    termos citados, impressos; (5) `example`s: a falsidade dá `False` no modelo concreto com o Um posto; a ponte é `rfl`; nada é declarado além. -/

open Lean Elab Command

run_cmd do
  let env ← getEnv
  let some idx := env.getModuleIdx? `TGLExt.FalsidadeDaInercia | throwError "modulo TGLExt.FalsidadeDaInercia ausente"
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
    IO.println ("FDI_AX\t" ++ n.toString ++ "\t" ++ kind ++ "\t" ++ toString n.isInternal ++ "\t" ++ String.intercalate "," (axs.toList.map Name.toString))
    IO.println ("FDI_BINDERS\t" ++ n.toString ++ "\t" ++ String.intercalate "," (ci.type.getForallBinderNames.map Name.toString))
    for c in ci.type.getUsedConstants do
      let r := c.getRoot
      if r == `TGL || r == `TGLExt || r == `ChatgptAudit then
        IO.println ("FDI_TIPO_USA\t" ++ n.toString ++ "\t" ++ c.toString ++ "\t" ++ modOf c)
    let cs := (match ci with
      | .thmInfo tv => tv.value.getUsedConstants
      | .defnInfo dv => dv.value.getUsedConstants
      | _ => #[])
    for c in cs do
      if env.getModuleIdxFor? c != some idx then
        let r := c.getRoot
        if r == `TGL || r == `TGLExt || r == `ChatgptAudit then
          usadosProva := usadosProva.insert c
  IO.println ("FDI_TOTAL\tdecl=" ++ toString nTot ++ "\tthm=" ++ toString nThm ++ "\tfora_do_trio=" ++ toString nFora ++ "\tsorryAx=" ++ toString nSorry)
  for c in usadosProva.toList.toArray.qsort (fun a b => a.toString < b.toString) do
    IO.println ("FDI_PROVA_USA\t" ++ c.toString ++ "\t" ++ modOf c)

-- os enunciados citados, impressos (para confrontar com a docstring da pedra)
#check @TGLExt.DualScalingData.fixed_tau_zero
#check @TGLExt.DualScalingData.scaling
#check @TGLExt.Fundacao.nothing_above_bears_a_post
#check @TGLExt.Fundacao.the_floor_fixes_the_cut
#check @TGLExt.Fundacao.the_fall_never_lands
#check @TGLExt.Fundacao.abismo
#check @TGLExt.Fundacao.oneScaling
#check @TGLExt.beta_forbids_full_static_witness
#check @TGLExt.leakage_strictly_loses
#check @TGLExt.diagFlow
#check @TGLExt.permanent
#check @TGLExt.observerProj
#check @TGLExt.um_is_the_great_attractor
#check @TGLExt.the_observer_is_unique
#print TGLExt.Fundacao.oneScaling
#print TGLExt.diagFlow
#check @TGLExt.FalsidadeDaInercia.the_inertia_of_a_post_is_false
#check @TGLExt.FalsidadeDaInercia.a_post_is_not_inertial
#check @TGLExt.FalsidadeDaInercia.inertia_is_not_its_own_cause
#check @TGLExt.FalsidadeDaInercia.the_zero_is_the_consequence_of_the_pruning
#check @TGLExt.FalsidadeDaInercia.the_tension_is_projected_onto_the_attractor
#check @TGLExt.FalsidadeDaInercia.diagFlow_coordinate_is_the_scaling
#check @TGLExt.FalsidadeDaInercia.falsidade_da_inercia_derivada

open TGLExt TGLExt.Fundacao TGLExt.FalsidadeDaInercia in
/-- a falsidade dá FALSE no modelo concreto com o Um posto em 1 -/
example : ¬ Inertial oneScaling (1 : ℝ) := a_post_is_not_inertial oneScaling rfl
open TGLExt TGLExt.Fundacao TGLExt.FalsidadeDaInercia in
/-- e `(1:ℝ) = 0` a partir da hipótese inercial (a conclusão é literalmente 1 = 0) -/
example (h : Inertial oneScaling (1 : ℝ)) : (1 : ℝ) = 0 := the_inertia_of_a_post_is_false oneScaling rfl h
open TGLExt TGLExt.Fundacao TGLExt.FalsidadeDaInercia in
/-- controle: a hipótese Inertial é necessária — o posto 1 move na escala 1 (não é vácuo) -/
example : oneScaling.theta 1 (1 : ℝ) ≠ 1 := (the_post_exists_and_moves).2 1 one_ne_zero
open TGLExt TGLExt.Fundacao TGLExt.FalsidadeDaInercia in
/-- a ponte é definicional: a coordenada do fluxo diagonal É a escala do modelo concreto (rfl, sem hipótese) -/
example (β : ℝ) (d : Fin 2 → ℝ) (t : ℝ) (x : Fin 2 → ℝ) (i : Fin 2) :
    diagFlow β d t x i = Real.exp (-(t * β * d i)) * x i := rfl
open TGLExt TGLExt.Fundacao TGLExt.FalsidadeDaInercia in
/-- fixo em todas as escalas negativas ⟹ peso zero, no modelo concreto -/
example (m : ℝ) (h : ∀ s : ℝ, s < 0 → oneScaling.theta s m = m) : oneScaling.tau m = 0 :=
  (inertia_is_not_its_own_cause oneScaling).1 m h

#print axioms TGLExt.FalsidadeDaInercia.falsidade_da_inercia_derivada
#print axioms TGLExt.FalsidadeDaInercia.the_inertia_of_a_post_is_false
