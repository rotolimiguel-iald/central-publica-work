import TheTimeIsNotAPost

/-! # Sondas ADVERSARIAIS do auditor de REPRODUCAO (R2, F1.TEMPO) sobre a pedra `TheTimeIsNotAPost`
    (fonte sha256 4d8a82591badd010…; .olean recompilado neste sandbox). Importa SO o .olean da pedra R2 compilado
    aqui; LEAN_PATH so-leitura no `.lake` do Nós. Nenhuma declaracao destas entra na pedra; medem o PESO dos
    enunciados novos/reforcados (E5.08, E5.12, E5.13) e do nome (E5.07; POSTO = RANK).
    Estatuto: [INPUT do auditor]; um `example` que compila e validade na face finita, nao creditacao. Sem sorry. -/

set_option autoImplicit false

noncomputable section
open TGLExt TGLExt.TheTimeIsNotAPost
open scoped Matrix

/-! ## Sonda P1 — E5.13 (T3.b(iii), face finita): o que o enunciado NAO afirma
    (a) O PAR pesa: com o MESMO ρ nao tracial, o par diagonal `a = E₀₀`, `b = E₁₁` da `ω(ab) = ω(ba)` (ambos 0):
        `identity_flow_not_kms_finite` e uma testemunha de UM par; o conteudo "nao e KMS" esta na forma negada
        `identity_flow_not_kms_finite'` (¬ ∀ x y, …), nao em "todo par falha".
    (b) A hipotese NAO TRACIAL pesa de verdade: para ρ = ½·1 a identidade do par vale para TODO x, y
        (ciclicidade do traco), logo a versao finita enunciada com ρ tracial seria FALSA (como o ADENDO E5.13 diz). -/

/-- P1(a): par diagonal com o ρ nao tracial — a igualdade VALE (0 = 0); o teorema finito e de um par especifico. -/
example : gibbs (rhoD ![(2 / 3 : ℝ), 1 / 3]) (!![1, 0; 0, 0] * !![0, 0; 0, 1])
      = gibbs (rhoD ![(2 / 3 : ℝ), 1 / 3]) (!![0, 0; 0, 1] * !![1, 0; 0, 0]) := by
  simp [gibbs, rhoD, Matrix.trace, Fin.sum_univ_two, Matrix.mul_apply]

/-- P1(b): com ρ = ½·1 (tracial) a identidade do par vale para TODO x, y — a forma negada
    `¬ ∀ x y, ω(xy) = ω(yx)` seria FALSA com ρ tracial; a hipotese nao tracial de E5.13 pesa. -/
example : ∀ x y : Matrix (Fin 2) (Fin 2) ℂ,
    gibbs (rhoD ![(1 / 2 : ℝ), 1 / 2]) (x * y) = gibbs (rhoD ![(1 / 2 : ℝ), 1 / 2]) (y * x) := by
  intro x y
  have h : rhoD ![(1 / 2 : ℝ), 1 / 2] = (1 / 2 : ℂ) • (1 : Matrix (Fin 2) (Fin 2) ℂ) := by
    ext i j
    fin_cases i <;> fin_cases j <;> simp [rhoD]
  simp only [gibbs, h, smul_mul_assoc, one_mul, Matrix.trace_smul]
  rw [Matrix.trace_mul_comm]

/-- P1(c): a forma negada e a que carrega o conteudo; dela se extrai o par da pedra (consistencia interna). -/
example : ¬ ∀ x y : Matrix (Fin 2) (Fin 2) ℂ,
    gibbs (rhoD ![(2 / 3 : ℝ), 1 / 3]) (x * y) = gibbs (rhoD ![(2 / 3 : ℝ), 1 / 3]) (y * x) :=
  identity_flow_not_kms_finite'

/-! ## Sonda P2 — E5.12 (reforco de `clock_reads_modulo_period` para TODO κ): o que o reforco acrescenta em κ = 0
    e TRIVIAL (x/0 = 0 do Lean), provavel por `simp` sem o teorema; o conteudo em κ = 0 e `frozen_clock`.
    Logo o reforco nao afirma nada novo em κ = 0 — e honesto, nao e sobre-afirmacao — e o conteudo de T10.b
    continua a ser o caso κ ≠ 0 (que a R1 ja tinha). -/

/-- P2(a): a instancia κ = 0 do enunciado reforcado, SEM usar o teorema. -/
example (t : ℝ) : Circle.exp (0 * (t + 2 * Real.pi / 0)) = Circle.exp (0 * t) := by
  simp

/-- P2(b): em κ = 0 o enunciado reforcado coincide com `frozen_clock` (relogio parado). -/
example (t : ℝ) : Circle.exp (0 * (t + 2 * Real.pi / 0)) = Circle.exp (0 * t) :=
  frozen_clock (t + 2 * Real.pi / 0) t

/-- P2(c): o caso κ ≠ 0 do reforco devolve exatamente a forma da R1 (a R2 implica a R1). -/
example (κ : ℝ) (_hκ : κ ≠ 0) (t : ℝ) :
    Circle.exp (κ * (t + 2 * Real.pi / κ)) = Circle.exp (κ * t) :=
  clock_reads_modulo_period κ t

/-! ## Sonda P3 — E5.07 (o NOME contra o TERMO; POSTO = RANK): em M₂(ℂ) com P = diag(1,0), a clausula composta
    `the_time_is_not_a_post` devolve: F(1) e INVERTIVEL (posto pleno: `flow_full_rank` da rank 2), F(1) NAO e
    idempotente (nao e posto), P nao e invertivel e tem rank < 2. O nome "o tempo nao e posto" le o que o termo
    prova e NAO contradiz `flow_full_rank` — ao contrario do nome da R1 ("sem posto"). -/

section L2
open scoped Matrix.Norms.L2Operator

/-- P3(a): F(1) e invertivel (T9.b, extraido da clausula composta). -/
example : IsUnit (TheAxiomAndTheFalseWitness.axiomFlow postDiag 1) :=
  (the_time_is_not_a_post (A := Matrix (Fin 2) (Fin 2) ℂ) postDiag_idem postDiag_ne_one).2.2.1 1

/-- P3(b): F(1) NAO e idempotente (T9.a, extraido da clausula composta): nenhum instante finito ≠ 0 e posto. -/
example : ¬ IsIdempotentElem (TheAxiomAndTheFalseWitness.axiomFlow postDiag 1) := fun h =>
  one_ne_zero (((the_time_is_not_a_post (A := Matrix (Fin 2) (Fin 2) ℂ) postDiag_idem postDiag_ne_one).2.1 1).mp h)

/-- P3(c): o posto P nao e invertivel (T9.c). -/
example : ¬ IsUnit postDiag :=
  (the_time_is_not_a_post (A := Matrix (Fin 2) (Fin 2) ℂ) postDiag_idem postDiag_ne_one).2.2.2.1

end L2

/-- P3(d): POSTO = RANK — rank F(1) = 2 (pleno) e rank P < 2: o instante tem posto pleno; o posto nao. -/
example : (TheAxiomAndTheFalseWitness.axiomFlow postDiag 1).rank = 2 ∧ postDiag.rank < 2 :=
  ⟨flow_full_rank 2 postDiag postDiag_idem 1, post_rank_lt 2 postDiag postDiag_idem postDiag_ne_one⟩

/-! ## Sonda extra — E5.08 (opcional feito): o "se e so se" do canal otico NAO e vacuo — com sin θ ≠ 0 o vetor
    de populacoes (1, 0) NAO e fixo (logo nem tudo e fixo; o controle `optical_channel_trivial_when_sin_zero`
    mostra que com sin θ = 0 tudo e fixo). -/
example {θ : ℝ} (hθ : Real.sin θ ≠ 0) :
    (opticalPopulationMap θ).mulVec ![1, 0] ≠ ![1, 0] := by
  intro h
  have h2 := (optical_channel_fixed_state_is_half_identity hθ ![1, 0]).mp h
  simp at h2

end
