import TGLExt.AfinacaoDasCordas

/-! Exame independente (gerência c1, modelo forte, 23/10/2026) da pedra candidata `TGLExt.AfinacaoDasCordas` (v398).
    Só lê o ambiente do sandbox k398b: (1) TODA constante do módulo (inclusive as internas geradas pelo Lean), o tipo e os
    axiomas (`collectAxioms`); (2) as constantes que o TIPO de cada declaração nomeada usa, com o módulo que as define (homônimos);
    (3) as constantes de fora do módulo que as PROVAS usam, com o módulo; (4) os homônimos, no ambiente, dos nomes citados
    (`faithful_period_iff`, `reciprocal_temperature`, `AngularQuotientFaithful`, `abismo`, `the_floor_fixes_the_cut`,
    `station_never_closes`, `the_face_does_not_close`, `the_read_face_closes`, `boost`). Depois, `example`s de não-vacuidade e de
    controle (meus, independentes do probe do preparador). Nada é declarado além dos `example`. -/

open Lean Elab Command

run_cmd do
  let env ← getEnv
  let some idx := env.getModuleIdx? `TGLExt.AfinacaoDasCordas | throwError "modulo TGLExt.AfinacaoDasCordas ausente"
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
  let mut nAx := 0
  let mut nFora := 0
  let mut nSorry := 0
  let mut nInt := 0
  let mut usadosProva : NameSet := {}
  for n in nomesOrd do
    let some ci := env.find? n | continue
    let kind := match ci with
      | .axiomInfo _ => "axiom" | .defnInfo _ => "def" | .thmInfo _ => "theorem" | .opaqueInfo _ => "opaque"
      | .quotInfo _ => "quot" | .inductInfo _ => "inductive" | .ctorInfo _ => "ctor" | .recInfo _ => "rec"
    let axs ← liftCoreM (collectAxioms n)
    nTot := nTot + 1
    if kind == "theorem" then nThm := nThm + 1
    if kind == "def" then nDef := nDef + 1
    if kind == "axiom" then nAx := nAx + 1
    if n.isInternal then nInt := nInt + 1
    unless axs.all (fun a => a == `propext || a == `Classical.choice || a == `Quot.sound) do nFora := nFora + 1
    if axs.contains `sorryAx then nSorry := nSorry + 1
    IO.println ("AFI_AX\t" ++ n.toString ++ "\t" ++ kind ++ "\t" ++ toString n.isInternal ++ "\t" ++ String.intercalate "," (axs.toList.map Name.toString))
    unless n.isInternal do
      for c in ci.type.getUsedConstants do
        let r := c.getRoot
        if r == `TGL || r == `TGLExt || r == `ChatgptAudit || r == `HurwitzZeta || c == `riemannZeta then
          IO.println ("AFI_TIPO_USA\t" ++ n.toString ++ "\t" ++ c.toString ++ "\t" ++ modOf c)
    let cs := (match ci with
      | .thmInfo tv => tv.value.getUsedConstants
      | .defnInfo dv => dv.value.getUsedConstants
      | _ => #[])
    for c in cs do
      if env.getModuleIdxFor? c != some idx then
        let r := c.getRoot
        if r == `TGL || r == `TGLExt || r == `ChatgptAudit || r == `HurwitzZeta || c == `riemannZeta || c == `riemannZeta_neg_nat_eq_bernoulli || c == `bernoulli_two || c == `bernoulli_one then
          usadosProva := usadosProva.insert c
  IO.println ("AFI_TOTAL\tdecl=" ++ toString nTot ++ "\tthm=" ++ toString nThm ++ "\tdef=" ++ toString nDef ++ "\taxiom=" ++ toString nAx ++ "\tinternas=" ++ toString nInt ++ "\tfora_do_trio=" ++ toString nFora ++ "\tsorryAx=" ++ toString nSorry)
  for c in usadosProva.toList.toArray.qsort (fun a b => a.toString < b.toString) do
    IO.println ("AFI_PROVA_USA\t" ++ c.toString ++ "\t" ++ modOf c)
  for (n, ci) in env.constants.map₁.toList do
    let s := n.getString!
    if (s == "faithful_period_iff" || s == "reciprocal_temperature" || s == "AngularQuotientFaithful" || s == "positive_faithful_period" || s == "abismo" || s == "the_floor_fixes_the_cut" || s == "station_never_closes" || s == "the_face_does_not_close" || s == "the_read_face_closes" || s == "boost" || s == "matsubara" || s == "DualScalingData" || s == "oneScaling") && !(n.isInternal) then
      let r := n.getRoot
      if r == `TGL || r == `TGLExt || r == `ChatgptAudit then
        IO.println ("AFI_HOMONIMO\t" ++ n.toString ++ "\t" ++ modOf n ++ "\t" ++ toString ci.type.getForallBinderNames.length)

open TGLExt.AfinacaoDasCordas ChatgptAudit.PolarPeriod016

-- os enunciados de Mathlib que a aritmetica usa, impressos
#check @riemannZeta_neg_nat_eq_bernoulli
#check @HurwitzZeta.hurwitzZeta_neg_nat
#check @ChatgptAudit.PolarPeriod016.faithful_period_iff
#check @ChatgptAudit.PolarPeriod016.reciprocal_temperature
#check @ChatgptAudit.PolarPeriod016.positive_faithful_period
#print ChatgptAudit.PolarPeriod016.AngularQuotientFaithful
#check @TGLExt.Fundacao.abismo
#check @TGLExt.Fundacao.the_floor_fixes_the_cut
#check @TGLExt.station_never_closes
#check @TGLExt.Palavra.the_face_does_not_close
#check @TGLExt.Palavra.the_read_face_closes

/-- MEU controle do polinomio de Bernoulli em ℚ: B₂(1/2) = 1/4 − 1/2 + 1/6 = −1/12 (convencao B₁ = −1/2 do Mathlib) -/
example : (Polynomial.bernoulli 2).eval (1 / 2 : ℚ) = -1 / 12 := by
  simp [Polynomial.bernoulli_def, Finset.sum_range_succ, bernoulli_one, bernoulli_two]
  norm_num

/-- MEU controle: ζ(−1, 1/2) = (2^{−1} − 1)·ζ(−1) = (−1/2)(−1/12) = 1/24, pela identidade da pedra -/
example : HurwitzZeta.hurwitzZeta (↑(1 / 2 : ℝ)) (-1) = ((1 / 2 : ℂ) - 1) * riemannZeta (-1) := by
  rw [hurwitz_zeta_neg_one_half, zeta_neg_one]; norm_num

/-- nao-vacuidade do circulo fiel: κ = 1, P = 2π e' fiel (κ·P = 2π) -/
example : AngularQuotientFaithful 1 (2 * Real.pi) := by
  rw [faithful_period_iff one_ne_zero]; left; ring

/-- e nele a torre e' n·κ: ω_1 = 1 -/
example : matsubara (2 * Real.pi) 1 = 1 := by
  have h := (faithful_iff_fundamental_mode (κ := 1) (P := 2 * Real.pi) one_pos (by positivity)).mp
    (by rw [faithful_period_iff one_ne_zero]; left; ring)
  exact h

/-- a divergencia e' genuina: as somas parciais de Σ n passam de qualquer cota (consequencia extraida do teorema) -/
example : ∀ C : ℝ, ∃ N : ℕ, C < ∑ n ∈ Finset.range N, (n : ℝ) := by
  intro C
  have h := the_tower_is_infinite.2.1
  obtain ⟨N, hN⟩ := (Filter.tendsto_atTop_atTop.mp h) (C + 1)
  exact ⟨N, by have := hN N le_rfl; linarith⟩

/-- os numeros fecham onde a docstring diz, e so' ai -/
example : bosonZeroPoint 26 = -1 := (bosonic_critical_dimension 26).1.mpr rfl
example : nsZeroPoint 10 = -1 / 2 := (superstring_critical_dimension 10).1.mpr rfl
example : ¬ (nsZeroPoint 26 = -1 / 2) := fun h => by have := (superstring_critical_dimension 26).1.mp h; omega
example : ¬ (bosonZeroPoint 10 = -1) := fun h => by have := (bosonic_critical_dimension 10).1.mp h; omega

/-- MEU controle do sinal de Fermi: com +1/48 por direcao (sinal trocado) a equacao −1/2 fecha em D = 26, nao em 10 -/
example (D : ℕ) : (((D : ℂ) - 2) * (bosonDirection - nsFermionDirection) = -1 / 2) ↔ D = 26 := by
  have e : ((D : ℂ) - 2) * (bosonDirection - nsFermionDirection) = -((D : ℂ) - 2) / 48 := by
    rw [bosonDirection_eq, nsFermionDirection_eq]; ring
  rw [e]; constructor
  · intro h; have h' : (D : ℂ) = 26 := by linear_combination (-48 : ℂ) * h
    exact_mod_cast h'
  · rintro rfl; norm_num

/-- a hipotese nomeada e' uma definicao proposicional habitada e refutavel: vale em (1, 1) e falha em (1, 2) -/
example : MasslessFirstLevel 1 1 := by unfold MasslessFirstLevel; ring
example : ¬ MasslessFirstLevel 1 2 := by unfold MasslessFirstLevel; norm_num

/-- a clausula do abismo da composicao dispara no modelo concreto `Fundacao.oneScaling` -/
example : ∃ s : ℝ, (TGLExt.Fundacao.oneScaling).tau ((TGLExt.Fundacao.oneScaling).theta s 1) < (1 / 10 : ℝ) := by
  obtain ⟨-, -, -, -, -, -, -, -, -, -, -, hab, -⟩ :=
    the_strings_close_the_face_from_outside_the_tgl_closes_the_reading
  exact hab ℝ TGLExt.Fundacao.oneScaling 1 (by show (0 : ℝ) < id 1; norm_num) (1 / 10) (by norm_num)

#print axioms TGLExt.AfinacaoDasCordas.the_strings_close_the_face_from_outside_the_tgl_closes_the_reading
#print axioms TGLExt.AfinacaoDasCordas.MasslessFirstLevel
