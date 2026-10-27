import TGLExt.PonteDaEscalaDual

/-! Exame independente (gerência c1, modelo forte, 26/10/2026) da entrega do Codex à ORDEM 025: `TGLExt.PonteDaEscalaDual` (sha16 0e55b6e448adbd91),
    recompilada no sandbox k402x (cópia do kernel v401). Só lê o ambiente: (1) toda constante do módulo, o tipo e os axiomas (`collectAxioms`);
    (2) as constantes do kernel que o TIPO de cada declaração usa, com o módulo de origem; (3) as constantes de fora do módulo que as PROVAS usam
    (quem usa a pedra FalsidadeDaInercia; quem usa o kernel; quem não usa nada do kernel); (4) os enunciados; (5) `example`s: a instância é a
    estrutura REAL `TGLExt.DualScalingData` (GlobalLiftLadder); «inercial» aqui é o vetor nulo (fixo por todo boost ⟹ v = 0); o lift em τ = 0 é 0. -/

open Lean Elab Command

run_cmd do
  let env ← getEnv
  let some idx := env.getModuleIdx? `TGLExt.PonteDaEscalaDual | throwError "modulo TGLExt.PonteDaEscalaDual ausente"
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
  let mut nDef := 0
  let mut nFora := 0
  let mut nSorry := 0
  let mut nInt := 0
  for n in nomesOrd do
    let some ci := env.find? n | continue
    let kind := match ci with
      | .axiomInfo _ => "axiom" | .defnInfo _ => "def" | .thmInfo _ => "theorem" | .opaqueInfo _ => "opaque"
      | .quotInfo _ => "quot" | .inductInfo _ => "inductive" | .ctorInfo _ => "ctor" | .recInfo _ => "rec"
    let axs ← liftCoreM (collectAxioms n)
    nTot := nTot + 1
    if n.isInternal then nInt := nInt + 1
    if kind == "theorem" && !n.isInternal then nThm := nThm + 1
    if kind == "def" && !n.isInternal then nDef := nDef + 1
    unless axs.all (fun a => a == `propext || a == `Classical.choice || a == `Quot.sound) do nFora := nFora + 1
    if axs.contains `sorryAx then nSorry := nSorry + 1
    IO.println ("O25_AX\t" ++ n.toString ++ "\t" ++ kind ++ "\t" ++ toString n.isInternal ++ "\t" ++ String.intercalate "," (axs.toList.map Name.toString))
    for c in ci.type.getUsedConstants do
      let r := c.getRoot
      if r == `TGL || r == `TGLExt || r == `ChatgptAudit || r == `TGLV351 || r == `F12Completion then
        IO.println ("O25_TIPO_USA\t" ++ n.toString ++ "\t" ++ c.toString ++ "\t" ++ modOf c)
    let cs := (match ci with
      | .thmInfo tv => tv.value.getUsedConstants
      | .defnInfo dv => dv.value.getUsedConstants
      | _ => #[])
    let mut usados : Array String := #[]
    for c in cs do
      if env.getModuleIdxFor? c != some idx then
        let r := c.getRoot
        if r == `TGL || r == `TGLExt || r == `ChatgptAudit || r == `TGLV351 || r == `F12Completion then
          usados := usados.push (c.toString ++ "@" ++ modOf c)
    IO.println ("O25_PROVA_USA\t" ++ n.toString ++ "\t" ++ String.intercalate ";" (usados.qsort (fun a b => a < b)).toList)
  IO.println ("O25_TOTAL\tdecl=" ++ toString nTot ++ "\tthm_nomeados=" ++ toString nThm ++ "\tdef_nomeados=" ++ toString nDef ++ "\tinternos=" ++ toString nInt ++ "\tfora_do_trio=" ++ toString nFora ++ "\tsorryAx=" ++ toString nSorry)

#check @TGLExt.PonteDaEscalaDual.momentumScaling
#print TGLExt.PonteDaEscalaDual.momentumScaling
#check @TGLExt.DualScalingData.scaling
#check @TGLExt.PonteDaEscalaDual.inertial_momentum_is_zero
#check @TGLExt.PonteDaEscalaDual.invariant_weight_is_zero
#check @TGLExt.PonteDaEscalaDual.rest_energy_eq_mc2
#check @TGLExt.PonteDaEscalaDual.lift_rest_energy
#check @TGLExt.PonteDaEscalaDual.lift_mass_not_selected
#check @TGLExt.PonteDaEscalaDual.positive_weight_cannot_be_invariant_mass
#check @TGLExt.PonteDaEscalaDual.core_positive_realization_exists
#check @TGLExt.PonteDaEscalaDual.coreLift
#check @TGLV351.regularCoreDualScalingData
#print TGLExt.PonteDaEscalaDual.theta
#print TGLExt.boost

open TGLExt TGLExt.PonteDaEscalaDual in
/-- a instância é a estrutura REAL do kernel: o campo `scaling` de `momentumScaling` é `pPlus_scaling` -/
example : momentumScaling.scaling = pPlus_scaling := rfl
open TGLExt TGLExt.PonteDaEscalaDual in
example : momentumScaling.tau = pPlus := rfl
open TGLExt TGLExt.PonteDaEscalaDual in
/-- o referente de «inercial» nesta ponte: um vetor fixo por TODO boost é o vetor ZERO (p⁺ = 0 E p⁻ = 0) -/
example (v : Momentum) (h : FalsidadeDaInercia.Inertial momentumScaling v) : v = 0 := by
  have h1 : theta 1 v = v := h 1
  have hp : pPlus v = 0 := inertial_momentum_is_zero h
  have hm : pMinus v = 0 := by
    have := pMinus_scaling 1 v
    rw [h1] at this
    have hne : Real.exp (1 : ℝ) ≠ 1 := by
      intro h0; have := (Real.exp_eq_one_iff (1 : ℝ)).mp h0; norm_num at this
    have h2 : (Real.exp 1 - 1) * pMinus v = 0 := by linarith
    rcases mul_eq_zero.mp h2 with h3 | h3
    · exact absurd (sub_eq_zero.mp h3) hne
    · exact h3
  have h0p : pPlus (0 : Momentum) = 0 := by simp [pPlus, energy, momentum]
  have h0m : pMinus (0 : Momentum) = 0 := by simp [pMinus, energy, momentum]
  apply null_coordinates_injective
  · rw [h0p]; exact hp
  · rw [h0m]; exact hm
open TGLExt TGLExt.PonteDaEscalaDual in
/-- o lift em τ = 0 é o vetor zero (divisão totalizada): fora de τ ≠ 0 a identidade da massa não vale -/
example {M : Type} (D : DualScalingData M) (mu2 : ℝ) (a : M) (h : D.tau a = 0) : lift D mu2 a = 0 := by
  funext i; fin_cases i <;> simp [lift, h]
open TGLExt TGLExt.PonteDaEscalaDual in
/-- `rest_energy_eq_mc2` é álgebra real pura: instancia-se sem nada do kernel -/
example : (2 : ℝ) = 2 * 1 ^ 2 := rest_energy_eq_mc2 2 0 2 1 one_pos (by norm_num) (by norm_num) (by norm_num) rfl
open TGLExt TGLExt.PonteDaEscalaDual in
/-- a massa não é selecionada: no mesmo `a` com τ a = 1, μ² = 1 e μ² = 4 dão vetores distintos, ambos com p⁺ = 1 -/
example : lift Fundacao.oneScaling (1 : ℝ) (1 : ℝ) ≠ lift Fundacao.oneScaling (4 : ℝ) (1 : ℝ) :=
  lift_mass_not_selected Fundacao.oneScaling 1 (by simp [Fundacao.oneScaling]) 1 4 (by norm_num)

#print axioms TGLExt.PonteDaEscalaDual.inertial_momentum_is_zero
#print axioms TGLExt.PonteDaEscalaDual.core_positive_realization_exists
