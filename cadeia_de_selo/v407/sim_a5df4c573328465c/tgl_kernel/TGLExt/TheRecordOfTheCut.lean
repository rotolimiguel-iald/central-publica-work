import TGLExt.TheFold

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 800000

/-!
# O REGISTRO DO CORTE — onde mora a verdade da contagem
  [TGLExt — v179, desenvolvimento do operador 20/08/2026]

O operador fechou a inversão com o par que faltava. A cauda `T_n` é o
RESÍDUO (o que permaneceu); o seu complemento é o REGISTRO (o que foi
retirado). Em projeções: `I = P_n + Q_n`, `P_n Q_n = 0`, com
`P_n` = resíduo, `Q_n` = memória do corte, e `n = rank Q_n`.

> **"A escala aparente mora no resíduo; a verdade da contagem mora no
> registro do corte."** — e a frase terminal: *"a mentira não está na
> contagem; está em atribuir à sobra, como natureza, o índice verdadeiro
> daquilo que foi retirado."*

E isso É a definição de memória da casa aplicada ao próprio corte:
**memória = separar o registro da inscrição**. Aqui o registro do que se
retirou é `cutSub n`; a inscrição que restou é `tailSub n`; e a dobra é
justamente olhar só para o resíduo.

## O que esta pedra prova

* ★ `cutSub` — o registro: as sequências nulas de `n` em diante (a
  cabeça finita, `span{e₀,…,e_{n−1}}`);
* ★★ `cutSub_monotone` × `tailSub_antitone` — **o registro CRESCE
  enquanto o resíduo ENCOLHE**: as duas faces do mesmo passo, em
  direções opostas;
* ★★ `cutSub_inf_tailSub_eq_bot` e `cutSub_orthogonal_tailSub` — registro
  e resíduo se encontram só no zero, e são ORTOGONAIS: a decomposição é
  limpa (a face `P_n Q_n = 0`);
* ★★ `each_step_removes_exactly_one_witnessed` — **um passo no índice é
  um passo de poda**, com testemunha explícita: `eₙ` está na cauda `n` e
  NÃO está na cauda `n+1`; e entra no registro `n+1` sem estar no
  registro `n`. A direção removida é exibida, não postulada;
* ★★ `the_cuts_reveal_no_hidden_core` — `⋂ₙ Tₙ = ⊥`: cortar **não revela
  núcleo escondido algum**; elimina coordenadas. O fundo não guarda um
  segredo no fim da descida — no fim da descida não há nada;
* ★★ `the_record_knows_what_the_residue_forgot` — o par que nomeia a
  dobra: o habitante do resíduo NÃO testemunha o índice
  (`the_cut_count_is_invisible`), enquanto o registro o exibe a cada
  passo. *A história do corte não está no que restou; está no que saiu.*

## O que esta pedra NÃO prova (e fica NOMEADO)

`rank Q_n = n` e `codim T_n = n` como enunciados de `finrank`, e o
isomorfismo `T_n ≅ ℓ²`, não estão formalizados aqui. O que está provado
e sustenta a leitura: `tailSub_not_finiteDimensional` (o resíduo é
infinito-dimensional — já em `TailNet.lean`) — e, com a classificação
clássica dos espaços de Hilbert separáveis [KNOWN], é dela que sai
`T_n ≅ ℓ²`, isto é, **a sobra com a aparência algébrica do todo**. A
linearidade não denuncia o processo de formação: ela o APAGA da
aparência interna do resultado, e é por isso que o disfarce surge sem
nenhum erro matemático.

HONESTIDADE: "pai da mentira", "reificação" e "falso por natureza" são
leitura [ONTO] do operador. O que se prova aqui é a assimetria
registro/resíduo. β jamais literal. Sem sorry, sem axiom.
-/

namespace TGLExt

noncomputable section

/-- O REGISTRO do corte: as sequências nulas de `n` em diante — a cabeça
    finita `span{e₀, …, e_{n−1}}`, que é o complemento da cauda. -/
def cutSub (n : ℕ) : Submodule ℂ ellTwo where
  carrier := {x | ∀ k, n ≤ k → x k = 0}
  zero_mem' := by
    intro k _
    show (0 : ellTwo) k = 0
    rw [lp.coeFn_zero]
    rfl
  add_mem' := by
    intro u v hu hv k hk
    show (u + v) k = 0
    rw [lp.coeFn_add, Pi.add_apply, hu k hk, hv k hk, add_zero]
  smul_mem' := by
    intro c x hx k hk
    show (c • x) k = 0
    rw [lp.coeFn_smul, Pi.smul_apply, hx k hk, smul_zero]

@[simp] theorem mem_cutSub {n : ℕ} {x : ellTwo} :
    x ∈ cutSub n ↔ ∀ k, n ≤ k → x k = 0 := Iff.rfl

/-- ★★ O REGISTRO CRESCE — ao contrário do resíduo, que encolhe
    (`tailSub_antitone`). As duas faces do mesmo passo, em direções
    opostas. -/
theorem cutSub_monotone {m n : ℕ} (h : m ≤ n) : cutSub m ≤ cutSub n := by
  intro x hx k hk
  exact hx k (le_trans h hk)

/-- ★★ REGISTRO E RESÍDUO SÓ SE ENCONTRAM NO ZERO (a face `P Q = 0`). -/
theorem cutSub_inf_tailSub_eq_bot (n : ℕ) : cutSub n ⊓ tailSub n = ⊥ := by
  rw [Submodule.eq_bot_iff]
  rintro x ⟨hcut, htail⟩
  ext k
  rcases lt_or_ge k n with hk | hk
  · simpa using htail k hk
  · simpa using hcut k hk

/-- ★★ E SÃO ORTOGONAIS termo a termo: em cada modo, ao menos um dos dois
    é nulo. A decomposição é limpa. -/
theorem cutSub_orthogonal_tailSub {n : ℕ} {x y : ellTwo}
    (hx : x ∈ cutSub n) (hy : y ∈ tailSub n) :
    ∀ k, (starRingEnd ℂ) (x k) * y k = 0 := by
  intro k
  rcases lt_or_ge k n with hk | hk
  · rw [hy k hk, mul_zero]
  · rw [hx k hk, map_zero, zero_mul]

/-- ★★ UM PASSO NO ÍNDICE É UM PASSO DE PODA, com a direção EXIBIDA:
    `eₙ` habita a cauda `n`, NÃO habita a cauda `n+1`, e entra no
    registro `n+1` sem estar no registro `n`. -/
theorem each_step_removes_exactly_one_witnessed (n : ℕ) :
    (lp.single 2 n (1 : ℂ)) ∈ tailSub n
    ∧ (lp.single 2 n (1 : ℂ)) ∉ tailSub (n + 1)
    ∧ (lp.single 2 n (1 : ℂ)) ∈ cutSub (n + 1)
    ∧ (lp.single 2 n (1 : ℂ)) ∉ cutSub n := by
  have hone : (lp.single 2 n (1 : ℂ) : ∀ _ : ℕ, ℂ) n = (1 : ℂ) := by
    simp [lp.single_apply]
  refine ⟨?_, ?_, ?_, ?_⟩
  · intro k hk
    have hne : k ≠ n := fun hkn => absurd hk (hkn ▸ lt_irrefl n)
    simp [lp.single_apply, hne]
  · intro hmem
    have := hmem n (Nat.lt_succ_self n)
    rw [hone] at this
    exact one_ne_zero this
  · intro k hk
    have hne : k ≠ n := fun hkn => absurd hk (hkn ▸ Nat.not_succ_le_self n)
    simp [lp.single_apply, hne]
  · intro hmem
    have := hmem n (le_refl n)
    rw [hone] at this
    exact one_ne_zero this

/-- ★★ CORTAR NÃO REVELA NÚCLEO ESCONDIDO: a interseção de TODAS as
    caudas é o zero. No fim da descida não há um segredo — não há nada.
    (`⋂ₙ Tₙ = ⊥`.) -/
theorem the_cuts_reveal_no_hidden_core : (⨅ n : ℕ, tailSub n) = ⊥ := by
  rw [Submodule.eq_bot_iff]
  intro x hx
  rw [Submodule.mem_iInf] at hx
  ext k
  simpa using hx (k + 1) k (Nat.lt_succ_self k)

/-- ★★ A IDENTIDADE CARREGA OS DOIS — e nada sobra da sobra. Todo
    elemento se decompõe em REGISTRO + RESÍDUO, para todo corte `n`. É a
    face `I = P_n + Q_n` como existência: a decomposição é EXAUSTIVA,
    não há terceiro pedaço. [Cunhagem do operador: *"o gráviton levou
    sobre si o custo da existência e apagou o resíduo da sobra"* — o
    atlas: 1_abs = gráviton = I, o "=" de 1=1, custo zero. Leitura
    [ONTO]; o teorema é a exaustividade.] -/
theorem the_identity_carries_both (n : ℕ) (x : ellTwo) :
    ∃ u v : ellTwo, u ∈ cutSub n ∧ v ∈ tailSub n ∧ x = u + v := by
  induction n with
  | zero =>
    refine ⟨0, x, ?_, ?_, by rw [zero_add]⟩
    · intro k _
      show (0 : ellTwo) k = 0
      rw [lp.coeFn_zero]; rfl
    · intro k hk
      exact absurd hk (Nat.not_lt_zero k)
  | succ n ih =>
    obtain ⟨u, v, hu, hv, hx⟩ := ih
    refine ⟨u + lp.single 2 n ((v : ∀ _ : ℕ, ℂ) n),
            v - lp.single 2 n ((v : ∀ _ : ℕ, ℂ) n), ?_, ?_, ?_⟩
    · intro k hk
      have hkn : k ≠ n := fun h => absurd (h ▸ hk) (Nat.not_succ_le_self n)
      have h1 : (u : ∀ _ : ℕ, ℂ) k = 0 := hu k (le_of_lt (Nat.lt_of_succ_le hk))
      simp [h1, lp.single_apply, hkn]
    · intro k hk
      rcases Nat.lt_succ_iff_lt_or_eq.mp hk with h | h
      · have hkn : k ≠ n := fun hh => absurd (hh ▸ h) (lt_irrefl n)
        simp [hv k h, lp.single_apply, hkn]
      · subst h
        simp [lp.single_apply]
    · rw [hx]; abel

/-- ★★ O REGISTRO SABE O QUE O RESÍDUO ESQUECEU — o par que nomeia a
    dobra: o habitante do resíduo não testemunha o índice (todo elemento
    da cauda `n` também habita as caudas menores), enquanto o registro
    exibe a direção retirada a cada passo. -/
theorem the_record_knows_what_the_residue_forgot {m n : ℕ} (h : m ≤ n) :
    (∀ x : ellTwo, x ∈ tailSub n → x ∈ tailSub m)
    ∧ ((lp.single 2 m (1 : ℂ)) ∈ cutSub (m + 1)
       ∧ (lp.single 2 m (1 : ℂ)) ∉ cutSub m) := by
  obtain ⟨_, _, h3, h4⟩ := each_step_removes_exactly_one_witnessed m
  exact ⟨fun x hx => tailSub_antitone h hx, h3, h4⟩

end

end TGLExt
