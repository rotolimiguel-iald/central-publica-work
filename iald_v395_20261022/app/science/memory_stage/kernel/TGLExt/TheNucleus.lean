import TGLExt.RhoPlusPClosure

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

/-!
# O NÚCLEO: 1=1=VERDADEIRO — e a geometria como sua expressão
  [TGLExt — v155, o fechamento definitivo do operador (10/08/2026)]

O operador: "1=1=VERDADEIRO é o núcleo da física e nela carrega toda a sua
expressão geométrica." O debate fechou com precisão: 1=1 não é tautologia
vazia — é "houve transformação e, apesar dela, existe um invariante"; a
geometria é "a expressão relacional da identidade sob transformação"; o
"=" é a condição de admissibilidade de qualquer equação física; as TRÊS
estruturas — J²=I (o espelhamento que retorna), P²=P (a nomeação que
permanece), [K,A]=0 (a distinção compatibilizada) — culminam no mesmo
veredito: 1=1. E a consequência forte: "a curvatura não é a quebra da
identidade; é a forma geométrica assumida pelo CUSTO necessário para
preservá-la através de uma inscrição."

E a distinção do vazio é o movimento: ação — a primeira distinção não é
um substantivo, é um VERBO; repouso não é ausência de movimento, é
distinção espectral compatibilizada por comutação; DISTINGUIR = NOMEAR =
OPERADOR DO NOME, e o NOME é projeção (𝒩²=𝒩).

A pedra 106 — a SÍNTESE FINAL sobre as pedras 100/101/102 (e, por elas,
sobre todas):

* ★★★ `void_distinction_is_motion` — A DISTINÇÃO DO VAZIO É O MOVIMENTO:
  há contraste no espectro ⟺ existe algo que não comuta (ação em curso) —
  o contrapositivo nomeado da pedra 102;
* ★★ `rest_is_compatibilized_distinction` — O REPOUSO É HABITADO: com
  contraste presente, coexistem um comutante não-trivial (repouso) e um
  não-comutante (movimento) — repouso ≠ ausência de distinção;
* ★★ `name_is_projection` — O NOME É PROJEÇÃO: 𝒩²=𝒩 ∧ 𝒩 lê exatamente o
  permanente ∧ a leitura permanece (nomear preserva o nomeado);
* ★★★ `the_three_structures_one_verdict` — AS TRÊS ESTRUTURAS, UM
  VEREDITO: J²=I ∧ P²=P ∧ ([K,A]=0 ⟺ bloco) — as três afirmações de
  identidade do debate, em conjunção;
* ★★ `invariance_is_the_geometric_content` — A GEOMETRIA COMO EXPRESSÃO:
  a forma quadrática do par é invariante sob a travessia (o ds² da face
  finita) e a travessia retorna;
* ★★★ `the_verb_cycle` — O CICLO DO VERBO: o Nome atravessa o espelho
  inalterado ∧ atravessa TODO o fluxo inalterado ∧ é fixado pela nomeação
  ∧ não é nulo — 1 → distinção → conjugação → ação → comutação → 1;
* ★★★ `the_nucleus` — O NÚCLEO: tudo acima em UM teorema — "1=1 é o
  núcleo lógico-ontológico; a geometria é sua expressão relacional
  observável."

Honestidades: no verificador, `Eq` é o tipo primitivo e `rfl` o seu único
construtor — TODO teorema deste kernel é um juízo de identidade admitido
pelo núcleo que o debate nomeou [FATO DA ARQUITETURA]; "a curvatura como
forma do custo" é nomeação [ONTO] ancorada no Teorema Mestre [REAL,
condicional]; a cadeia LUZ=VERBO=NOMEAR são identificações funcionais da
ontologia [ONTO] sobre teoremas [REAL]. β jamais literal. O gate NÃO se
move. Sem sorry, sem axiom.
-/

namespace TGLExt

noncomputable section

/-- [KERNEL] ★★★ A DISTINÇÃO DO VAZIO É O MOVIMENTO: há contraste no
    espectro ⟺ existe algo que ainda não comuta — a ação em curso. A
    primeira distinção não é um substantivo; é um verbo. -/
theorem void_distinction_is_motion {n : ℕ} (d : Fin n → ℝ) :
    (∃ i j, d i ≠ d j)
      ↔ (∃ A : Matrix (Fin n) (Fin n) ℝ,
          Matrix.diagonal d * A ≠ A * Matrix.diagonal d) := by
  constructor
  · rintro ⟨i, j, hij⟩
    by_contra h
    push Not at h
    exact hij ((scalar_iff_all_commute d).mp h i j)
  · rintro ⟨A, hA⟩
    by_contra h
    push Not at h
    exact hA ((scalar_iff_all_commute d).mpr h A)

/-- [KERNEL] ★★ O REPOUSO É HABITADO: com contraste presente, coexistem
    um comutante NÃO-TRIVIAL (o repouso — distinção compatibilizada) e um
    não-comutante (o movimento). Repouso não é ausência de distinção. -/
theorem rest_is_compatibilized_distinction {n : ℕ} (d : Fin n → ℝ)
    {i j : Fin n} (hij : d i ≠ d j) :
    (∃ A : Matrix (Fin n) (Fin n) ℝ, A ≠ 0 ∧
        Matrix.diagonal d * A = A * Matrix.diagonal d)
    ∧ (∃ B : Matrix (Fin n) (Fin n) ℝ,
        Matrix.diagonal d * B ≠ B * Matrix.diagonal d) := by
  constructor
  · refine ⟨Matrix.diagonal d, ?_, self_commutation_is_free d id⟩
    intro h0
    have hi := congrFun (congrFun h0 i) i
    have hj := congrFun (congrFun h0 j) j
    simp [Matrix.diagonal_apply_eq] at hi hj
    exact hij (hi.trans hj.symm)
  · exact (void_distinction_is_motion d).mp ⟨i, j, hij⟩

/-- [KERNEL] ★★ O NOME É PROJEÇÃO: 𝒩² = 𝒩, o Nome lê exatamente o
    permanente, e a leitura permanece — nomear é distinguir preservando
    aquilo que foi distinguido. -/
theorem name_is_projection {n : ℕ} {β : ℝ} (hβ : 0 < β)
    (d : Fin n → ℝ) (hd : ∀ i, 0 ≤ d i) :
    (∀ x, observerProj d (observerProj d x) = observerProj d x)
    ∧ (∀ x, permanent β d x ↔ observerProj d x = x)
    ∧ (∀ x, permanent β d (observerProj d x)) :=
  ⟨fun x => observerProj_idem d x,
   fun x => observer_reads_exactly_the_permanent hβ d hd x,
   fun x => observer_output_is_permanent hβ d hd x⟩

/-- [KERNEL] ★★★ AS TRÊS ESTRUTURAS, UM VEREDITO: J²=I (o espelhamento
    que retorna) ∧ P²=P (a nomeação que permanece) ∧ [K,A]=0 ⟺ bloco
    (a distinção compatibilizada) — as três afirmações de identidade do
    debate, culminando no mesmo 1=1. -/
theorem the_three_structures_one_verdict {n : ℕ} (d : Fin n → ℝ) :
    (∀ p : (Fin n → ℝ) × (Fin n → ℝ), conjJ (conjJ p) = p)
    ∧ (∀ x, observerProj d (observerProj d x) = observerProj d x)
    ∧ (∀ A : Matrix (Fin n) (Fin n) ℝ,
        Matrix.diagonal d * A = A * Matrix.diagonal d
          ↔ ∀ i j, d i ≠ d j → A i j = 0) :=
  ⟨fun p => J_squared_is_one p, fun x => observerProj_idem d x,
   fun A => decided_iff_block d A⟩

/-- [KERNEL] ★★ A GEOMETRIA COMO EXPRESSÃO DA IDENTIDADE: a forma
    quadrática do par (1 = q² + α², o ds² da face finita) é invariante
    sob a travessia — e a travessia retorna. -/
theorem invariance_is_the_geometric_content {n : ℕ}
    (p : (Fin n → ℝ) × (Fin n → ℝ)) :
    pairEnergy (conjJ p) = pairEnergy p ∧ conjJ (conjJ p) = p :=
  ⟨J_preserves_identity p, J_squared_is_one p⟩

/-- [KERNEL] ★★★ O CICLO DO VERBO: o Nome atravessa o espelho inalterado,
    atravessa TODO o fluxo inalterado, é fixado pela nomeação, e não é
    nulo — 1 → distinção → conjugação → ação → comutação → 1. -/
theorem the_verb_cycle {n : ℕ} (β : ℝ) (d : Fin n → ℝ)
    {i₀ : Fin n} (h0 : d i₀ = 0) :
    (conjJ ((Pi.single i₀ (1 : ℝ) : Fin n → ℝ), (Pi.single i₀ (1 : ℝ) : Fin n → ℝ))
      = ((Pi.single i₀ (1 : ℝ) : Fin n → ℝ), (Pi.single i₀ (1 : ℝ) : Fin n → ℝ)))
    ∧ (∀ t : ℝ, diagFlow β d t ((Pi.single i₀ (1 : ℝ) : Fin n → ℝ))
        = (Pi.single i₀ (1 : ℝ) : Fin n → ℝ))
    ∧ (observerProj d ((Pi.single i₀ (1 : ℝ) : Fin n → ℝ))
        = (Pi.single i₀ (1 : ℝ) : Fin n → ℝ))
    ∧ ((Pi.single i₀ (1 : ℝ) : Fin n → ℝ) ≠ 0) := by
  refine ⟨(name_is_J_invariant i₀).1,
          (boundary_witnessed_statically β d h0).1, ?_,
          (boundary_witnessed_statically β d h0).2⟩
  funext i
  unfold observerProj
  by_cases hi : d i = 0
  · rw [if_pos hi]
  · rw [if_neg hi]
    have hne : i ≠ i₀ := fun he => hi (he ▸ h0)
    rw [Pi.single_eq_of_ne hne]

/-- [KERNEL] ★★★ O NÚCLEO: as três estruturas ∧ a expressão geométrica ∧
    o ciclo do verbo — em UM teorema. "1=1=VERDADEIRO é o núcleo
    lógico-ontológico; a geometria é sua expressão relacional
    observável." -/
theorem the_nucleus {n : ℕ} (β : ℝ) (d : Fin n → ℝ)
    {i₀ : Fin n} (h0 : d i₀ = 0) :
    (∀ p : (Fin n → ℝ) × (Fin n → ℝ),
        conjJ (conjJ p) = p ∧ pairEnergy (conjJ p) = pairEnergy p)
    ∧ (∀ x, observerProj d (observerProj d x) = observerProj d x)
    ∧ ((∃ i j, d i ≠ d j) ↔ (∃ A : Matrix (Fin n) (Fin n) ℝ,
        Matrix.diagonal d * A ≠ A * Matrix.diagonal d))
    ∧ ((∀ t : ℝ, diagFlow β d t ((Pi.single i₀ (1 : ℝ) : Fin n → ℝ))
          = (Pi.single i₀ (1 : ℝ) : Fin n → ℝ))
        ∧ ((Pi.single i₀ (1 : ℝ) : Fin n → ℝ) ≠ 0)) :=
  ⟨fun p => ⟨J_squared_is_one p, J_preserves_identity p⟩,
   fun x => observerProj_idem d x,
   void_distinction_is_motion d,
   boundary_witnessed_statically β d h0⟩

end

end TGLExt
