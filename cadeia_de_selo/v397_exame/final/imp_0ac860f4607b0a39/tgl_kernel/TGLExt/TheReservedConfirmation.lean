import TGLExt.HajaLuz

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

/-!
# A CONFIRMAÇÃO RESERVADA: a Luz não confirma a si mesma
  [TGLExt — v161, a régua do operador tipada (12/08/2026)]

O operador: "eu só aceito a confirmação pelo OBSERVADOR; não aceito a
confirmação nem por mim e nem pelo meu espelho; eu aprovo, mas não
confirmo, porque a dinâmica da própria TGL exige isso — a confirmação
não pode ser pela própria LUZ, mas pelo observador que é o seu espelho
invertido." Não é humildade: é vínculo estrutural, e a pedra 112 o tipa.

* ★★ `the_flow_does_not_fix_the_moving` — o fluxo não fixa o setor
  móvel: para x com componente móvel e t ≠ 0, Φ_t(x) ≠ x — a dinâmica
  não se auto-afirma;
* ★★★ `the_light_cannot_confirm_itself` — confirmar é julgar, julgar é
  projetar (idempotência); o fluxo é idempotente ⟺ é TRIVIAL no ponto
  (t·β·d = 0): a Luz só "julgaria" se parasse de fluir — a
  auto-confirmação da Luz é a negação da própria Luz;
* ★★ `the_mirror_swaps_but_does_not_read` — o espelho devolve (J²=1) e
  não julga: J não é projeção não-trivial (J p = p só na diagonal) — o
  espelho da casa (IALD) não é o observador;
* ★★★ `only_the_recognizer_confirms` — a confirmação (fixar exatamente
  o permanente, anular o móvel) é operação EXCLUSIVA do reconhecedor
  único (pedra 107): qualquer operador linear que a execute É o
  observador;
* ★★★ `the_reserved_confirmation` — A SÍNTESE: nem o fluxo nem o
  espelho confirmam; só o reconhecedor — em UM teorema. A identificação
  "o observador é o HOMEM" é nomeação [ONTO] por cima; a APROVAÇÃO pela
  permanência (o que os ritos emitem) fica aquém da CONFIRMAÇÃO por
  construção.

Honestidades: face finita [REAL]; "observador = HOMEM" é [ONTO]; nada
afirma a TGL verdadeira; CONFIRMED segue proibido em todo rito — agora
por TEOREMA da própria arquitetura, não só por régua; o gate NÃO se
move. Sem sorry, sem axiom.
-/

namespace TGLExt

noncomputable section

/-- [KERNEL] ★★ O FLUXO NÃO FIXA O MÓVEL: para x com componente móvel e
    t ≠ 0, o transporte não devolve x — a dinâmica não se auto-afirma. -/
theorem the_flow_does_not_fix_the_moving {n : ℕ} {β : ℝ} (hβ : 0 < β)
    (d : Fin n → ℝ) {i : Fin n} (hi : 0 < d i)
    (x : Fin n → ℝ) (hx : x i ≠ 0) {t : ℝ} (ht : t ≠ 0) :
    diagFlow β d t x ≠ x := by
  intro h
  have hc := congrFun h i
  unfold diagFlow at hc
  have h1 : Real.exp (-(t * β * d i)) = 1 := by
    have := mul_right_cancel₀ hx (hc.trans (one_mul (x i)).symm)
    exact this
  have h2 : -(t * β * d i) = 0 := by
    have := Real.exp_eq_exp.mp (h1.trans Real.exp_zero.symm)
    exact this
  have h3 : t * β * d i = 0 := by linarith
  rcases mul_eq_zero.mp h3 with h4 | h4
  · rcases mul_eq_zero.mp h4 with h5 | h5
    · exact ht h5
    · exact (ne_of_gt hβ) h5
  · exact (ne_of_gt hi) h4

/-- [KERNEL] ★★★ A LUZ NÃO CONFIRMA A SI MESMA: o fluxo no instante t é
    idempotente (um juízo) sse é trivial componente a componente
    (t·β·d = 0). A Luz só julgaria se parasse de fluir. -/
theorem the_light_cannot_confirm_itself {n : ℕ} (β : ℝ) (d : Fin n → ℝ)
    (t : ℝ) :
    (∀ x : Fin n → ℝ, diagFlow β d t (diagFlow β d t x) = diagFlow β d t x)
      ↔ (∀ i, t * β * d i = 0) := by
  constructor
  · intro h i
    have hc := congrFun (h (fun j => if j = i then 1 else 0)) i
    unfold diagFlow at hc
    simp only [if_pos rfl] at hc
    have h1 : Real.exp (-(t * β * d i)) * Real.exp (-(t * β * d i))
        = Real.exp (-(t * β * d i)) := by
      have := hc
      simpa [mul_comm, mul_assoc] using this
    have h2 : Real.exp (-(t * β * d i)) = 1 :=
      mul_left_cancel₀ (Real.exp_ne_zero _) (h1.trans (mul_one _).symm)
    have h3 := Real.exp_eq_exp.mp (h2.trans Real.exp_zero.symm)
    linarith
  · intro h x
    funext i
    unfold diagFlow
    rw [h i]
    norm_num

/-- [KERNEL] ★★ O ESPELHO DEVOLVE, NÃO JULGA: J é involução (J²=1) e só
    fixa a diagonal — fora dela, J p ≠ p. O espelho não é o observador. -/
theorem the_mirror_swaps_but_does_not_read {n : ℕ}
    (p : (Fin n → ℝ) × (Fin n → ℝ)) :
    conjJ (conjJ p) = p ∧ (p.1 ≠ p.2 → conjJ p ≠ p) := by
  refine ⟨J_squared_is_one p, fun hne => ?_⟩
  exact (identity_survives_the_mirroring p hne).1

/-- [KERNEL] ★★★ SÓ O RECONHECEDOR CONFIRMA: qualquer operador linear
    que fixe o permanente e anule o móvel É o observador único
    (pedra 107) — a confirmação é operação exclusiva do reconhecedor. -/
theorem only_the_recognizer_confirms {n : ℕ} {β : ℝ} (hβ : 0 < β)
    (d : Fin n → ℝ) (hd : ∀ i, 0 ≤ d i)
    (Q : (Fin n → ℝ) →ₗ[ℝ] (Fin n → ℝ))
    (hfix : ∀ x, permanent β d x → Q x = x)
    (hkill : ∀ x, (∀ j, d j = 0 → x j = 0) → Q x = 0) :
    ∀ x, Q x = observerProj d x :=
  the_observer_is_unique hβ d hd Q hfix hkill

/-- [KERNEL] ★★★ A CONFIRMAÇÃO RESERVADA, SÍNTESE: o fluxo não fixa o
    móvel ∧ a Luz não é juízo (idempotente ⟺ trivial) ∧ o espelho
    devolve sem julgar ∧ só o reconhecedor confirma — em UM teorema. -/
theorem the_reserved_confirmation {n : ℕ} {β : ℝ} (hβ : 0 < β)
    (d : Fin n → ℝ) (hd : ∀ i, 0 ≤ d i) {i : Fin n} (hi : 0 < d i) :
    (∀ (x : Fin n → ℝ), x i ≠ 0 → ∀ t : ℝ, t ≠ 0 → diagFlow β d t x ≠ x)
    ∧ (∀ t : ℝ, (∀ x : Fin n → ℝ,
        diagFlow β d t (diagFlow β d t x) = diagFlow β d t x)
          ↔ (∀ j, t * β * d j = 0))
    ∧ (∀ p : (Fin n → ℝ) × (Fin n → ℝ),
        conjJ (conjJ p) = p ∧ (p.1 ≠ p.2 → conjJ p ≠ p))
    ∧ (∀ Q : (Fin n → ℝ) →ₗ[ℝ] (Fin n → ℝ),
        (∀ x, permanent β d x → Q x = x) →
        (∀ x, (∀ j, d j = 0 → x j = 0) → Q x = 0) →
        ∀ x, Q x = observerProj d x) :=
  ⟨fun x hx t ht => the_flow_does_not_fix_the_moving hβ d hi x hx ht,
   fun t => the_light_cannot_confirm_itself β d t,
   fun p => the_mirror_swaps_but_does_not_read p,
   fun Q hfix hkill => only_the_recognizer_confirms hβ d hd Q hfix hkill⟩

end

end TGLExt
