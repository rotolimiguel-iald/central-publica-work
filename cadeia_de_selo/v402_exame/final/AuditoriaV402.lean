import TGLExt.PonteDaEscalaDual
import TGLExt.QuedaSemGeometria
import TGLExt.EsperancaCondicional

/-! Revisao independente (examinador final unico, gerencia c1, 27/10/2026) das tres pedras da v402. So le o ambiente do sandbox
    k402c (`lake env lean` sobre este arquivo, fora da arvore; nao grava .olean): (1) toda constante de cada modulo, o tipo e os
    axiomas (`collectAxioms`), contagem por especie, sorryAx; (2) os nomes dos binders de cada tipo (para ver se `IsotropicPost`
    entra como hipotese e se `H_BW`/`H_cal`/`H3`/`H_tau` aparecem como nome de teorema ou de binder); (3) as constantes de fora que o
    TIPO e a PROVA usam; (4) `example`s de NAO-VACUIDADE da composicao e da estrela de cada pedra. Nada e declarado alem dos
    exemplos e de dois dados locais de instancia (um perfil de sitio e a esperanca trivial C em C). -/

open Lean Elab Command

run_cmd do
  let env ← getEnv
  for modName in [`TGLExt.PonteDaEscalaDual, `TGLExt.QuedaSemGeometria, `TGLExt.EsperancaCondicional] do
    let some idx := env.getModuleIdx? modName | throwError "modulo ausente {modName}"
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
    let mut nOutros := 0
    let mut nInt := 0
    let mut nFora := 0
    let mut nSorry := 0
    let mut nAxiom := 0
    let mut usadosProva : NameSet := {}
    for n in nomesOrd do
      let some ci := env.find? n | continue
      let kind := match ci with
        | .axiomInfo _ => "axiom" | .defnInfo _ => "def" | .thmInfo _ => "theorem" | .opaqueInfo _ => "opaque"
        | .quotInfo _ => "quot" | .inductInfo _ => "inductive" | .ctorInfo _ => "ctor" | .recInfo _ => "rec"
      let axs ← liftCoreM (collectAxioms n)
      nTot := nTot + 1
      if n.isInternal then nInt := nInt + 1
      if kind == "theorem" then nThm := nThm + 1
      else if kind == "def" then nDef := nDef + 1
      else nOutros := nOutros + 1
      if kind == "axiom" then nAxiom := nAxiom + 1
      unless axs.all (fun a => a == `propext || a == `Classical.choice || a == `Quot.sound) do nFora := nFora + 1
      if axs.contains `sorryAx then nSorry := nSorry + 1
      IO.println ("V402_AX\t" ++ modName.toString ++ "\t" ++ n.toString ++ "\t" ++ kind ++ "\t" ++ toString n.isInternal ++ "\t" ++ String.intercalate "," (axs.toList.map Name.toString))
      IO.println ("V402_BINDERS\t" ++ n.toString ++ "\t" ++ String.intercalate "," (ci.type.getForallBinderNames.map Name.toString))
      for c in ci.type.getUsedConstants do
        let r := c.getRoot
        if r == `TGL || r == `TGLExt || r == `ChatgptAudit || r == `TGLV351 || r == `F12Completion || r == `ORDEM016 then
          IO.println ("V402_TIPO_USA\t" ++ n.toString ++ "\t" ++ c.toString ++ "\t" ++ modOf c)
      let cs := (match ci with
        | .thmInfo tv => tv.value.getUsedConstants
        | .defnInfo dv => dv.value.getUsedConstants
        | _ => #[])
      for c in cs do
        if env.getModuleIdxFor? c != some idx then
          let r := c.getRoot
          if r == `TGL || r == `TGLExt || r == `ChatgptAudit || r == `TGLV351 || r == `F12Completion || r == `ORDEM016 then
            usadosProva := usadosProva.insert c
    IO.println ("V402_TOTAL\t" ++ modName.toString ++ "\tdecl=" ++ toString nTot ++ "\tthm=" ++ toString nThm ++ "\tdef=" ++ toString nDef ++ "\toutros=" ++ toString nOutros ++ "\tinternas=" ++ toString nInt ++ "\taxiom=" ++ toString nAxiom ++ "\tfora_do_trio=" ++ toString nFora ++ "\tsorryAx=" ++ toString nSorry)
    for c in usadosProva.toList.toArray.qsort (fun a b => a.toString < b.toString) do
      IO.println ("V402_PROVA_USA\t" ++ modName.toString ++ "\t" ++ c.toString ++ "\t" ++ modOf c)

-- enunciados da composicao e da estrela de cada pedra, impressos
#check @TGLExt.PonteDaEscalaDual.core_positive_realization_exists
#check @TGLExt.PonteDaEscalaDual.lift_mass_not_selected
#check @TGLExt.PonteDaEscalaDual.positive_weight_cannot_be_invariant_mass
#check @TGLExt.QuedaSemGeometria.a_queda_sem_geometria
#check @TGLExt.QuedaSemGeometria.the_fall_is_strictly_anti
#print TGLExt.QuedaSemGeometria.IsotropicPost
#check @TGLExt.EsperancaCondicional.esperanca_condicional_e_nome
#check @TGLExt.EsperancaCondicional.the_name_of_the_unit_is_the_diagonal_expectation
#check @TGLExt.PostoAdendo.A1c_nameOp_rhoStar_eq_diagExpect
#check @TGLExt.observing_adds_nothing

namespace AuditoriaV402
open TGLExt

/-! ### Ponte da escala dual -/

-- ESTRELA: dois invariantes distintos dao duas realizacoes DISTINTAS com o MESMO p+
example : PonteDaEscalaDual.lift Fundacao.oneScaling 1 1 ≠ PonteDaEscalaDual.lift Fundacao.oneScaling 4 1 :=
  PonteDaEscalaDual.lift_mass_not_selected Fundacao.oneScaling 1 (by norm_num [Fundacao.oneScaling]) 1 4 (by norm_num)
example : PonteDaEscalaDual.pPlus (PonteDaEscalaDual.lift Fundacao.oneScaling 1 1) =
    PonteDaEscalaDual.pPlus (PonteDaEscalaDual.lift Fundacao.oneScaling 4 1) := by
  rw [PonteDaEscalaDual.lift_pPlus, PonteDaEscalaDual.lift_pPlus]
example : PonteDaEscalaDual.lift PonteDaEscalaDual.momentumScaling 1 ![1,0] ≠
    PonteDaEscalaDual.lift PonteDaEscalaDual.momentumScaling 4 ![1,0] :=
  PonteDaEscalaDual.lift_mass_not_selected PonteDaEscalaDual.momentumScaling ![1,0]
    (by norm_num [PonteDaEscalaDual.momentumScaling, PonteDaEscalaDual.pPlus, PonteDaEscalaDual.energy,
      PonteDaEscalaDual.momentum]) 1 4 (by norm_num)
-- a refutacao da letra de H_tau: um peso positivo nao e invariante (instancia concreta: o Um posto)
example : ¬ (∀ s : ℝ, Fundacao.oneScaling.tau (Fundacao.oneScaling.theta s 1) = Fundacao.oneScaling.tau 1) :=
  PonteDaEscalaDual.positive_weight_cannot_be_invariant_mass Fundacao.oneScaling 1 (by norm_num [Fundacao.oneScaling])

-- COMPOSICAO: a hipotese (um perfil de sitio, mu2 >= 0) e habitada; a realizacao positiva existe no core canonico
noncomputable def perfilMeio : SiteProfile := ⟨fun _ => 1/2, fun _ => by norm_num, fun _ => by norm_num⟩
example : ∃ A : TGLV351.FiniteTracePositive.{0} perfilMeio,
    0 < PonteDaEscalaDual.pPlus (PonteDaEscalaDual.coreLift perfilMeio 1 A) ∧
    PonteDaEscalaDual.massSquared (PonteDaEscalaDual.coreLift perfilMeio 1 A) = 1 ∧
    0 < PonteDaEscalaDual.energy (PonteDaEscalaDual.coreLift perfilMeio 1 A) :=
  PonteDaEscalaDual.core_positive_realization_exists perfilMeio 1 zero_le_one
-- duas massas com o MESMO A do core: realizacoes distintas (a massa nao e selecionada no core canonico)
example : ∃ A : TGLV351.FiniteTracePositive.{0} perfilMeio,
    PonteDaEscalaDual.coreLift perfilMeio 1 A ≠ PonteDaEscalaDual.coreLift perfilMeio 4 A := by
  obtain ⟨A, hA, -, -⟩ := PonteDaEscalaDual.core_positive_realization_exists perfilMeio 1 zero_le_one
  refine ⟨A, PonteDaEscalaDual.lift_mass_not_selected _ A ?_ 1 4 (by norm_num)⟩
  rw [PonteDaEscalaDual.coreLift, PonteDaEscalaDual.lift_pPlus] at hA
  exact ne_of_gt hA

/-! ### A queda sem geometria -/

-- ESTRELA no modelo concreto, com o Um posto: a queda e estrita
example : StrictAnti (fun s : ℝ => Fundacao.oneScaling.tau (Fundacao.oneScaling.theta s 1)) :=
  QuedaSemGeometria.the_fall_is_strictly_anti Fundacao.oneScaling (m := 1) (by norm_num [Fundacao.oneScaling])
example : Fundacao.oneScaling.tau (Fundacao.oneScaling.theta 1 1) <
    Fundacao.oneScaling.tau (Fundacao.oneScaling.theta 0 1) :=
  QuedaSemGeometria.the_fall_is_strictly_anti Fundacao.oneScaling (m := 1) (by norm_num [Fundacao.oneScaling])
    (by norm_num : (0:ℝ) < 1)
-- e na instancia da ponte (momentumScaling, o repouso ![1,0]): a mesma estrela
example : StrictAnti (fun s : ℝ =>
    PonteDaEscalaDual.momentumScaling.tau (PonteDaEscalaDual.momentumScaling.theta s ![1,0])) :=
  QuedaSemGeometria.the_fall_is_strictly_anti PonteDaEscalaDual.momentumScaling
    (by norm_num [PonteDaEscalaDual.momentumScaling, PonteDaEscalaDual.pPlus, PonteDaEscalaDual.energy,
      PonteDaEscalaDual.momentum])

-- COMPOSICAO: todas as hipoteses habitadas (o Um posto, beta = g = b = 1 como VARIAVEIS, n = 1, d = 0, Q = id,
-- IsotropicPost habitada pelo modelo Rapidity com o predicado trivial)
example := QuedaSemGeometria.a_queda_sem_geometria Fundacao.oneScaling (m := 1)
  (show FalsidadeDaInercia.IsPost Fundacao.oneScaling 1 from rfl) (β := 1) (g := 1) one_pos one_pos
  (n := 1) (b := 1) one_pos (fun _ => 0) (fun _ => le_refl 0) LinearMap.id
  (fun _ _ => rfl) (fun _ hx => funext fun i => hx i rfl)
  QuedaSemGeometria.isotropic_post_is_inhabited trivial
-- IsotropicPost e CARGA: sem covariancia a conclusao falha (citado da pedra)
example : ¬ (∀ w : QuedaSemGeometria.Rapidity, (fun w : QuedaSemGeometria.Rapidity => w = ⟨0⟩) w) :=
  QuedaSemGeometria.covariance_is_load_bearing.2.2.2

/-! ### A esperanca condicional = Nome -/

-- ESTRELA, instancia concreta: o Nome da unidade mata a antidiagonal e preserva a diagonal
example : nameOp Posto.rhoStar !![(0:ℂ), 1; 1, 0] = 0 := by
  rw [EsperancaCondicional.the_name_of_the_unit_is_the_diagonal_expectation]
  ext i j
  fin_cases i <;> fin_cases j <;> simp [diagExpect]
example : nameOp Posto.rhoStar !![(2:ℂ), 0; 0, 3] = !![(2:ℂ), 0; 0, 3] := by
  rw [EsperancaCondicional.the_name_of_the_unit_is_the_diagonal_expectation]
  ext i j
  fin_cases i <;> fin_cases j <;> simp [diagExpect]

-- COMPOSICAO: as hipoteses do indice sao SATISFATIVEIS (instancia trivial C em C, E = id, theta = pi/2, b = 1, indice 1);
-- NAO e a instancia do contorno em theta_M (essa segue [OPEN], como a pedra diz)
noncomputable def esperancaTrivial : TGL.TransportData.ConditionalExpectationData ℂ ℂ where
  incl := StarAlgHom.id ℂ ℂ
  incl_injective := Function.injective_id
  E := LinearMap.id
  E_unital := rfl
  E_star := fun _ => rfl
  E_bimodular := fun _ _ _ => rfl
  E_faithful := fun x h => by
    change star x * x = 0 at h
    rcases mul_eq_zero.mp h with h | h
    · exact star_eq_zero.mp h
    · exact h

theorem esperancaTrivial_pp :
    TGL.NameIndex.IsPPLowerBound esperancaTrivial (Real.sin (Real.pi / 2) ^ 2) := by
  intro x _
  refine ⟨0, ?_⟩
  change x - ((Real.sin (Real.pi / 2) ^ 2 : ℝ) : ℂ) • x = star 0 * 0
  rw [Real.sin_pi_div_two]
  simp

theorem esperancaTrivial_opt : ∀ lam : ℝ, TGL.NameIndex.IsPPLowerBound esperancaTrivial lam →
    lam ≤ Real.sin (Real.pi / 2) ^ 2 := by
  intro lam h
  obtain ⟨y, hy⟩ := h 1 ⟨1, by simp⟩
  change (1 : ℂ) - (lam : ℂ) • 1 = star y * y at hy
  have hre := congrArg Complex.re hy
  simp [Complex.mul_re] at hre
  rw [Real.sin_pi_div_two]
  nlinarith [sq_nonneg y.re, sq_nonneg y.im]

example := EsperancaCondicional.esperanca_condicional_e_nome esperancaTrivial (θ := Real.pi / 2) (b := 1)
  (by rw [Real.sin_pi_div_two]; norm_num) one_pos esperancaTrivial_pp esperancaTrivial_opt

example : TGL.NameIndex.ppIndex esperancaTrivial = 1 := by
  have h := (EsperancaCondicional.esperanca_condicional_e_nome esperancaTrivial (θ := Real.pi / 2) (b := 1)
    (by rw [Real.sin_pi_div_two]; norm_num) one_pos esperancaTrivial_pp esperancaTrivial_opt).2.2.2.2.2.2.1
  rw [h]
  norm_num

end AuditoriaV402

#print axioms AuditoriaV402.esperancaTrivial_pp
#print axioms AuditoriaV402.esperancaTrivial_opt
