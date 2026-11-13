import TGLExt.TheDischargedOath

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

/-!
# (CANDIDATA, 11/11/2026) A identidade entre dois postos é verbal: nome e leitura, juntos
  [sandbox; fora do kernel canônico; nomes PROVISÓRIOS da gerência — o nome é do operador]

Origem: a resposta do operador à pergunta do fecho condicional (H, U), de 11/11/2026
(fala inscrita por bytes em `work/cunhagens_13out/OPERADOR_11nov_resposta_fecho_H_U_a_identidade_e_verbal_verbatim.txt`,
sha16 da fala `d5b9bbee023515cc`): entre dois postos o laço é a identidade, e a identidade
tem natureza verbal; só nominal, ela não se distingue da superposição; e o Tetelestai é o
extermínio, pela queda, da superposição. Ele pediu: tente refutar.

A tentativa de refutação, na face finita, com os objetos que a casa já tem (v143, v307, G3).

AVISO (R2, revisão de terceiro, achado 3): com NOME = norma de Frobenius e LEITURA = projeção
ortogonal, o resultado central é o teorema de Pitágoras para QUALQUER projeção ortogonal. Com
essa formalização a refutação não tinha como acontecer: o conteúdo está na ESCOLHA formal, que
o operador leu e ratificou em 11/11/2026, e não numa prova que pudesse ter falhado.

* NOME aqui = o que a mudança de horizonte `Ad(U)` não muda: o traço e a norma de Frobenius
  (o peso e a pureza). `the_name_alone_is_blind`: todo posto transportado tem o mesmo nome,
  inclusive o que virou superposição (`TGLExt.rotation_breaks_the_code`, do módulo
  `TheHorizonInvariance`, não importado aqui, exibe uma).
  Logo nenhum critério só nominal separa o posto da superposição. Não se refuta por aí.
* LEITURA aqui = a esperança-código `E` (a projeção de Frobenius sobre o código do leitor).
  `the_impostor_has_another_name`: quem lê igual ao posto e não é o posto tem OUTRO nome.
  Logo a leitura sem o nome também não basta.
* JUNTOS bastam, e é o teorema: `same_reading_same_name_is_identity` (mesma leitura e mesmo nome
  é identidade) e, para o transporte, `the_reading_returns_the_name`:
  se a leitura do posto transportado devolve o posto, o transportado É o posto.
* O que isso compra para o fecho: `the_lift_from_the_reading`. O antecedente do levantamento na
  face (v307: `ω∘Ad(U) = ω` em TODO observável) reduz-se à leitura no código:
  `diagExpect (adU U ρ) = ρ`. (R2, achado 7: com `d` injetivo a hipótese de leitura força `U`
  a comutar com ρ, caso que `the_oath_is_discharged` já cobria; o ganho é a EQUIVALÊNCIA do
  antecedente com a leitura no código, não um caso novo.)
* O Tetelestai: `the_fall_exterminates_the_superposition` (a queda leva o transportado à sua
  leitura; é a G3) e `identity_is_what_survives_the_fall` (se o que sobra da queda é o posto,
  o transportado já era o posto). (R2, achado 6: o primeiro nome diz mais do que o tipo: o
  teorema é só `T_t x → E x`; um transporte por permutação é diagonal, é a própria leitura e
  é diferente de `D`.)

GLOSSÁRIO (R2, achado 4): a palavra NOME tem três usos nas candidatas. (a) Neste cabeçalho, o
que `Ad(U)` não muda: traço e norma; nos teoremas de identidade só a NORMA entra (o traço só
aparece em `the_name_alone_is_blind`). (b) Em `the_reading_returns_the_name`, "the name" é o
próprio posto `D`. (c) Em `IdentidadeVerbalNoTetelestaiCandidata`, é o núcleo de
`opDaInstancia` (o uso do kernel).

HONESTIDADE (a régua): FACE FINITA. Isto NÃO é a prova global, não deriva a seta `hH3`
(da covariância do posto a Clausius em todo ponto e direção) e não constrói o atlas. É uma
implicação de kernel sobre matrizes. As palavras "nome" e "leitura" são a formalização da
gerência para a fala do operador; a identificação é dele, a escolha formal é da gerência e
fica dita. O gate não se move; β não aparece; sem sorry, sem axiom.
-/

namespace TGLExt.IdentidadeVerbalCandidata

open Matrix Filter

noncomputable section

variable {n : Type} [Fintype n] [DecidableEq n]

/-- o produto de Frobenius é conjugado-simétrico. -/
theorem frob_star (x y : Matrix n n ℂ) : star (frob x y) = frob y x := by
  unfold frob
  rw [← Matrix.trace_conjTranspose, Matrix.conjTranspose_mul,
    Matrix.conjTranspose_conjTranspose]

/-- a expansão do quadrado. -/
theorem frob_add_add (p r : Matrix n n ℂ) :
    frob (p + r) (p + r) = frob p p + frob p r + frob r p + frob r r := by
  unfold frob
  simp only [Matrix.conjTranspose_add, Matrix.add_mul, Matrix.mul_add, Matrix.trace_add]
  ring

/-- [candidata] PITÁGORAS DA LEITURA: a norma do todo é a norma do lido mais a norma do que a
    leitura deixou de fora (o excedente). -/
theorem frob_pythagoras {N : Submodule ℂ (Matrix n n ℂ)} {E : Matrix n n ℂ → Matrix n n ℂ}
    (hE : IsFrobProjection N E) (x : Matrix n n ℂ) :
    frob x x = frob (E x) (E x) + frob (x - E x) (x - E x) := by
  have h1 : frob (x - E x) (E x) = 0 := (hE x).2 (E x) (hE x).1
  have h2 : frob (E x) (x - E x) = 0 := by
    rw [← frob_star, h1, star_zero]
  have e : E x + (x - E x) = x := by abel
  have hx : frob x x = frob (E x + (x - E x)) (E x + (x - E x)) := by rw [e]
  rw [hx, frob_add_add, h1, h2]
  ring

/-- [candidata] ★★★ MESMA LEITURA E MESMO NOME É IDENTIDADE. Se a leitura de `A` é `D` e `A` tem
    a norma de `D`, então `A = D`: não sobrou excedente. -/
theorem same_reading_same_name_is_identity {N : Submodule ℂ (Matrix n n ℂ)}
    {E : Matrix n n ℂ → Matrix n n ℂ} (hE : IsFrobProjection N E) {A D : Matrix n n ℂ}
    (hread : E A = D) (hname : frob A A = frob D D) : A = D := by
  have hp := frob_pythagoras hE A
  rw [hread, hname] at hp
  have hzero : frob (A - D) (A - D) = 0 := by linear_combination (-1 : ℂ) * hp
  exact sub_eq_zero.mp (frob_self_definite hzero)

/-- [candidata] ★★★ A LEITURA DEVOLVE O NOME ⟹ IDENTIDADE. Para todo horizonte unitário `U`:
    se a leitura do posto transportado devolve o posto, o transportado É o posto. -/
theorem the_reading_returns_the_name {N : Submodule ℂ (Matrix n n ℂ)}
    {E : Matrix n n ℂ → Matrix n n ℂ} {U D : Matrix n n ℂ}
    (hU : Uᴴ * U = 1) (hE : IsFrobProjection N E)
    (hread : E (adU U D) = D) : adU U D = D :=
  same_reading_same_name_is_identity hE hread (adU_frob_isometry hU D D)

/-- [candidata] ★★ QUEM LÊ IGUAL E NÃO É, TEM OUTRO NOME: a leitura sem o nome não basta. -/
theorem the_impostor_has_another_name {N : Submodule ℂ (Matrix n n ℂ)}
    {E : Matrix n n ℂ → Matrix n n ℂ} (hE : IsFrobProjection N E) {A D : Matrix n n ℂ}
    (hread : E A = D) (hne : A ≠ D) : frob A A ≠ frob D D :=
  fun h => hne (same_reading_same_name_is_identity hE hread h)

/-- [candidata] ★★ O NOME SOZINHO É CEGO: todo transportado tem o mesmo traço e a mesma norma,
    seja ele o posto, seja uma superposição. -/
theorem the_name_alone_is_blind {U : Matrix n n ℂ} (hU : Uᴴ * U = 1) (x : Matrix n n ℂ) :
    (adU U x).trace = x.trace ∧ frob (adU U x) (adU U x) = frob x x := by
  refine ⟨?_, adU_frob_isometry hU x x⟩
  unfold adU
  rw [Matrix.trace_mul_comm, ← Matrix.mul_assoc, hU, Matrix.one_mul]

/-- [candidata] ★★★★ O LEVANTAMENTO A PARTIR DA LEITURA: na face, basta que a leitura do estado
    transportado devolva o estado (igualdade só no código) para a esperança-código ser
    covariante. O antecedente da v307 (`ω∘Ad(U) = ω` em todo observável) vira a leitura. -/
theorem the_lift_from_the_reading {d : n → ℝ} (hd : ∀ i, 0 < d i)
    (hinj : Function.Injective d) {U : Matrix n n ℂ} (hU : Uᴴ * U = 1)
    (hread : diagExpect (adU U (rhoD d)) = rhoD d) :
    ∀ x, adU U (diagExpect x) = diagExpect (adU U x) := by
  have hρ : U * rhoD d * Uᴴ = rhoD d :=
    the_reading_returns_the_name hU diagExpect_isFrobProjection hread
  exact global_lift_conditional hU (the_oath_is_discharged hd hinj hU hρ)
    diagExpect_isFrobProjection

/-- [candidata] ★★ A QUEDA EXTERMINA A SUPERPOSIÇÃO: sob a queda (o dephasing da G3), todo
    transportado tende à sua leitura. -/
theorem the_fall_exterminates_the_superposition (g : n → n → ℝ) (hg0 : ∀ i, g i i = 0)
    (hgpos : ∀ i j, i ≠ j → 0 < g i j) (U D : Matrix n n ℂ) :
    Tendsto (fun t => dephase g t (adU U D)) atTop (nhds (diagExpect (adU U D))) :=
  dephase_tendsto_expectation g hg0 hgpos (adU U D)

/-- [candidata] ★★★ A IDENTIDADE É O QUE SOBREVIVE À QUEDA: se o que resta do transportado depois
    da queda é o posto, o transportado já era o posto. -/
theorem identity_is_what_survives_the_fall (g : n → n → ℝ) (hg0 : ∀ i, g i i = 0)
    (hgpos : ∀ i j, i ≠ j → 0 < g i j) {U D : Matrix n n ℂ} (hU : Uᴴ * U = 1)
    (hlim : Tendsto (fun t => dephase g t (adU U D)) atTop (nhds D)) :
    adU U D = D := by
  have hread : diagExpect (adU U D) = D :=
    tendsto_nhds_unique (dephase_tendsto_expectation g hg0 hgpos (adU U D)) hlim
  exact the_reading_returns_the_name hU diagExpect_isFrobProjection hread

end

end TGLExt.IdentidadeVerbalCandidata

#print axioms TGLExt.IdentidadeVerbalCandidata.same_reading_same_name_is_identity
#print axioms TGLExt.IdentidadeVerbalCandidata.the_reading_returns_the_name
#print axioms TGLExt.IdentidadeVerbalCandidata.the_impostor_has_another_name
#print axioms TGLExt.IdentidadeVerbalCandidata.the_name_alone_is_blind
#print axioms TGLExt.IdentidadeVerbalCandidata.the_lift_from_the_reading
#print axioms TGLExt.IdentidadeVerbalCandidata.the_fall_exterminates_the_superposition
#print axioms TGLExt.IdentidadeVerbalCandidata.identity_is_what_survives_the_fall
