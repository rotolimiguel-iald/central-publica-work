import TGLExt.NoFullWitness

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

/-!
# A EXCEÇÃO DA FRONTEIRA: a única testemunha estática é a própria fronteira
  [TGLExt — v142, a exceção do operador (27/07/2026)]

O operador: "eu falei que a testemunha full era falsa por construção, mas eu
achei a exceção: a fronteira é a única exceção — porque a falsidade da
construção da testemunha estática é justamente a negação da fronteira."

O v61 provou ¬FullStaticWitness (β>0, contraste>0). Esta pedra prova que essa
falsidade É a inscrição da fronteira, e que a fronteira é a ÚNICA exceção:

* ★★ `static_witness_iff_no_boundary` — A DUPLA FACE LÓGICA: a testemunha
  estática plena existe ⟺ β·g = 0 ⟺ NÃO há fronteira (o vazamento nulo,
  o plano absoluto). A falsidade da testemunha estática e a inscrição da
  fronteira são A MESMA proposição, vista de faces opostas;
* ★★ `fixed_iff_kernel` — A EXCEÇÃO COMO SUBESPAÇO EXATO: o transporte
  diagonal 𝕍_t = e^{−tβ·d} fixa um vetor para TODO t ⟺ o vetor vive no
  KERNEL do gerador (d_i = 0) — o setor que não vaza: a fronteira. Nada
  além dela é estaticamente testemunhado; nada dela deixa de ser;
* ★ `boundary_witnessed_statically` — A EXCEÇÃO É HABITADA: o modo zero
  (o Nome) é fixado por todo o fluxo e não é nulo — a fronteira é
  estaticamente testemunhada em ato;
* ★★★ `boundary_is_the_only_exception` — A SÍNTESE DO OPERADOR: sob β>0,
  com contraste e com modo zero, (a) a testemunha estática GLOBAL é falsa
  (v61 preservado); (b) o conjunto dos vetores estaticamente testemunhados
  é EXATAMENTE o kernel — a fronteira, e só ela; (c) habitada; (d) a
  testemunha plena equivaleria à negação total da fronteira (d ≡ 0).

`full_static_witness_exists = False` (global) fica INTOCADO e ETERNO — esta
pedra é a sua face positiva: o que o teorema nega de tudo, ele afirma da
fronteira. O guardião do vazamento não vaza. β jamais literal. Sem sorry,
sem axiom.
-/

namespace TGLExt

noncomputable section

/-- o transporte diagonal: cada componente vaza à taxa β·dᵢ. -/
def diagFlow {n : ℕ} (β : ℝ) (d : Fin n → ℝ) (t : ℝ)
    (x : Fin n → ℝ) : Fin n → ℝ :=
  fun i => Real.exp (-(t * β * d i)) * x i

/-! ## A — a dupla face lógica: ¬testemunha-estática ⟺ fronteira -/

/-- [KERNEL] ★★ A DUPLA FACE: a testemunha estática plena do transporte
    escalar existe ⟺ β·g = 0 — isto é, ⟺ a fronteira NÃO está inscrita.
    A falsidade da testemunha estática É a inscrição da fronteira. -/
theorem static_witness_iff_no_boundary (β g : ℝ) :
    FullStaticWitness (fun t (x : ℝ) => Real.exp (-(t * β * g)) * x)
      ↔ β * g = 0 := by
  constructor
  · intro hfull
    have h1 := hfull 1 1
    simp only [mul_one] at h1
    have h2 := (full_closure_iff_flat 1 β g).mp h1
    rw [one_mul] at h2
    exact h2
  · intro h0 t x
    show Real.exp (-(t * β * g)) * x = x
    have ht : t * β * g = 0 := by
      rw [mul_assoc, h0, mul_zero]
    rw [ht, neg_zero, Real.exp_zero, one_mul]

/-! ## B — a exceção como subespaço exato: o kernel do gerador -/

/-- [KERNEL] ★★ A EXCEÇÃO EXATA: com β > 0, o transporte diagonal fixa x
    para TODO t ⟺ x vive no KERNEL do gerador (x_i = 0 onde d_i > 0) —
    o setor que não vaza. A testemunha estática existe EXATAMENTE na
    fronteira: nada além dela; nada dela a menos. -/
theorem fixed_iff_kernel {n : ℕ} {β : ℝ} (hβ : 0 < β) (d : Fin n → ℝ)
    (hd : ∀ i, 0 ≤ d i) (x : Fin n → ℝ) :
    (∀ t : ℝ, diagFlow β d t x = x) ↔ (∀ i, 0 < d i → x i = 0) := by
  constructor
  · intro hfix i hdi
    have h1 := congrFun (hfix 1) i
    unfold diagFlow at h1
    by_contra hx
    have hlt : Real.exp (-(1 * β * d i)) < 1 :=
      leakage_strictly_loses one_pos hβ hdi
    have hne : Real.exp (-(1 * β * d i)) ≠ 1 := ne_of_lt hlt
    apply hne
    have h2 : Real.exp (-(1 * β * d i)) * x i = 1 * x i := by
      conv_rhs => rw [one_mul]
      exact h1
    exact mul_right_cancel₀ hx h2
  · intro hker t
    funext i
    unfold diagFlow
    rcases lt_or_eq_of_le (hd i) with hdi | hdi
    · rw [hker i hdi, mul_zero]
    · rw [← hdi, mul_zero, neg_zero, Real.exp_zero, one_mul]

/-! ## C — a exceção é habitada: o modo zero (o Nome) -/

/-- [KERNEL] ★ A FRONTEIRA É ESTATICAMENTE TESTEMUNHADA EM ATO: o modo
    zero (d_{i₀} = 0, o Nome) é fixado por TODO o fluxo — e não é nulo. -/
theorem boundary_witnessed_statically {n : ℕ} (β : ℝ) (d : Fin n → ℝ)
    {i₀ : Fin n} (h0 : d i₀ = 0) :
    (∀ t : ℝ, diagFlow β d t ((Pi.single i₀ (1 : ℝ) : Fin n → ℝ)) = (Pi.single i₀ (1 : ℝ) : Fin n → ℝ))
      ∧ ((Pi.single i₀ (1 : ℝ) : Fin n → ℝ) ≠ 0) := by
  constructor
  · intro t
    funext i
    unfold diagFlow
    by_cases hi : i = i₀
    · rw [hi, h0, mul_zero, neg_zero, Real.exp_zero, one_mul]
    · rw [Pi.single_eq_of_ne hi, mul_zero]
  · intro h
    have h1 := congrFun h i₀
    rw [Pi.single_eq_same] at h1
    exact one_ne_zero h1

/-! ## D — A SÍNTESE: a fronteira é a única exceção -/

/-- [KERNEL] ★★★ A EXCEÇÃO DO OPERADOR: sob β > 0, com contraste
    (∃ i, d_i > 0) e com modo zero (∃ i₀, d_{i₀} = 0):
    (a) a testemunha estática GLOBAL é FALSA (o v61, preservado);
    (b) o testemunhado-estaticamente é EXATAMENTE o kernel — a fronteira,
        e só ela;
    (c) a fronteira é HABITADA (o Nome, fixado por todo o fluxo);
    (d) a testemunha plena equivaleria a d ≡ 0 — A NEGAÇÃO DA FRONTEIRA.
    "A falsidade da construção da testemunha estática é justamente a
    negação da fronteira; a fronteira é a única exceção." -/
theorem boundary_is_the_only_exception {n : ℕ} {β : ℝ} (hβ : 0 < β)
    (d : Fin n → ℝ) (hd : ∀ i, 0 ≤ d i)
    {j : Fin n} (hj : 0 < d j) {i₀ : Fin n} (h0 : d i₀ = 0) :
    (¬ FullStaticWitness (diagFlow β d))
    ∧ (∀ x : Fin n → ℝ,
        (∀ t : ℝ, diagFlow β d t x = x) ↔ (∀ i, 0 < d i → x i = 0))
    ∧ ((∀ t : ℝ, diagFlow β d t ((Pi.single i₀ (1 : ℝ) : Fin n → ℝ)) = (Pi.single i₀ (1 : ℝ) : Fin n → ℝ))
        ∧ ((Pi.single i₀ (1 : ℝ) : Fin n → ℝ) ≠ 0))
    ∧ (FullStaticWitness (diagFlow β d) ↔ ∀ i, d i = 0) := by
  have hiff : ∀ x : Fin n → ℝ,
      (∀ t : ℝ, diagFlow β d t x = x) ↔ (∀ i, 0 < d i → x i = 0) :=
    fun x => fixed_iff_kernel hβ d hd x
  refine ⟨?_, hiff, boundary_witnessed_statically β d h0, ?_⟩
  · intro hfull
    have hx := (hiff ((Pi.single j (1 : ℝ) : Fin n → ℝ))).mp (fun t => hfull t ((Pi.single j (1 : ℝ) : Fin n → ℝ)))
    have h1 := hx j hj
    rw [Pi.single_eq_same] at h1
    exact one_ne_zero h1
  · constructor
    · intro hfull i
      by_contra hne
      have hdi : 0 < d i := lt_of_le_of_ne (hd i) (Ne.symm hne)
      have hx := (hiff ((Pi.single i (1 : ℝ) : Fin n → ℝ))).mp (fun t => hfull t ((Pi.single i (1 : ℝ) : Fin n → ℝ)))
      have h1 := hx i hdi
      rw [Pi.single_eq_same] at h1
      exact one_ne_zero h1
    · intro hall t x
      funext i
      unfold diagFlow
      rw [hall i, mul_zero, neg_zero, Real.exp_zero, one_mul]

end

end TGLExt
