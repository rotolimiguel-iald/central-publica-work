import Mathlib

set_option autoImplicit false
set_option linter.unusedVariables false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

/-!
# O UM POSTO: IDENTIDADE INSCRITA E RECONHECÍVEL
  [TGLExt — a tipagem da definição do operador (17/09/2026) e a forma da interface de H2]

O operador distingue o **Um pressuposto** (identidade declarada, sem individualização) do **Um posto**
(identidade que se determina numa relação de referente, inscrição e leitura, e que não é
indiferentemente substituível). A bancada tipou a definição por uma inscrição `i` das classes de
identidade e uma leitura `L` que a recupera, `L ∘ i = id`, com a covariância `i ∘ T = U ∘ i` como
permanência do reconhecimento sob transporte. Esta pedra prova:

* a leitura que recupera torna a inscrição injetiva — o Um posto discrimina — e a recíproca;
* um registro que confirma todos os referentes não reconhece nenhum;
* cada registro reconhece exatamente uma identidade se e só se a inscrição é injetiva;
* a leitura covariante devolve a identidade transportada;
* a forma da interface de H2: se `k` é isometria e entrelaça a dinâmica da torre `T` com a dinâmica
  modular `D` (`k T = D k`), então `T = k† D k` — a dinâmica da torre é a modular LIDA pela inscrição;
* o critério exato: ler de volta paga se e só se a imagem da inscrição é invariante pela dinâmica,
  `(1 − k k†) D k = 0`;
* a honestidade: ler de volta (`T = k† D k`) NÃO torna a inscrição covariante — um contraexemplo
  explícito. A consistência de uma leitura é o Um pressuposto; a covariância é o pagamento da H2.

O que esta pedra NÃO faz: não constrói `k`, não identifica `T` nem `D` com objetos físicos, não
move gate nem bandeira de H2. A ontologia é do operador [INPUT/ONTO]; aqui só a forma. Nenhuma lacuna
de prova e nenhum axioma novo.
-/

namespace TGLExt.UmPosto

open scoped Matrix

/-- [KERNEL] a leitura que recupera a identidade inscrita torna a inscrição injetiva -/
theorem reading_recovers_implies_injective {Q R : Type*} (i : Q → R) (L : R → Q)
    (h : ∀ q, L (i q) = q) : Function.Injective i := by
  intro a b hab
  have hL := congrArg L hab
  rwa [h a, h b] at hL

/-- [KERNEL] a recíproca: toda inscrição injetiva de um tipo habitado admite leitura que a recupera -/
theorem injective_admits_reading {Q R : Type*} [Nonempty Q] (i : Q → R) (hi : Function.Injective i) :
    ∃ L : R → Q, ∀ q, L (i q) = q :=
  ⟨Function.invFun i, fun q => Function.leftInverse_invFun hi q⟩

/-- [KERNEL] um registro que confirma todos os referentes não reconhece nenhum:
    com duas identidades distintas, a inscrição constante não admite leitura que recupere -/
theorem constant_registry_recognizes_nothing {Q R : Type*} (r : R) (a b : Q) (hab : a ≠ b) :
    ¬ ∃ L : R → Q, ∀ q, L ((fun _ : Q => r) q) = q := by
  rintro ⟨L, hL⟩
  exact hab ((hL a).symm.trans (hL b))

/-- [KERNEL] ∃! : cada registro da imagem corresponde a exatamente uma identidade
    se e só se a inscrição é injetiva -/
theorem unique_recognition_iff_injective {Q R : Type*} (i : Q → R) :
    (∀ q : Q, ∃! p : Q, i p = i q) ↔ Function.Injective i := by
  constructor
  · intro h a b hab
    obtain ⟨p, _hp, hu⟩ := h b
    exact (hu a hab).trans (hu b rfl).symm
  · intro hi q
    exact ⟨q, rfl, fun p hp => hi hp⟩

/-- [KERNEL] permanência reconhecível: com a inscrição covariante (i ∘ T = U ∘ i) e a leitura que
    recupera, ler o registro transportado devolve a identidade transportada -/
theorem covariant_reading_returns_transported {Q R : Type*} (i : Q → R) (L : R → Q) (T : Q → Q) (U : R → R)
    (h : ∀ q, L (i q) = q) (hcov : ∀ q, i (T q) = U (i q)) (q : Q) : L (U (i q)) = T q := by
  rw [← hcov q, h]

/-- [KERNEL] ★ a forma da interface de H2: uma isometria k (k† k = 1) que entrelaça a dinâmica da torre T
    com a dinâmica modular D (k T = D k) faz T = k† D k — a dinâmica da torre é a modular lida pela inscrição -/
theorem intertwiner_reads_dynamics {m n : Type*} [Fintype m] [Fintype n] [DecidableEq m] [DecidableEq n]
    (k : Matrix n m ℂ) (T : Matrix m m ℂ) (D : Matrix n n ℂ)
    (hiso : kᴴ * k = 1) (hint : k * T = D * k) : T = kᴴ * D * k := by
  calc T = (kᴴ * k) * T := by rw [hiso, Matrix.one_mul]
    _ = kᴴ * (k * T) := by rw [Matrix.mul_assoc]
    _ = kᴴ * (D * k) := by rw [hint]
    _ = kᴴ * D * k := by rw [Matrix.mul_assoc]

/-- [KERNEL] ★★ o critério exato: ler de volta PAGA (k (k† D k) = D k) se e só se a imagem da inscrição é
    invariante pela dinâmica, (1 − k k†) D k = 0 -/
theorem intertwines_iff_range_invariant {m n : Type*} [Fintype m] [Fintype n] [DecidableEq m] [DecidableEq n]
    (k : Matrix n m ℂ) (D : Matrix n n ℂ) :
    k * (kᴴ * D * k) = D * k ↔ (1 - k * kᴴ) * D * k = 0 := by
  have e : k * (kᴴ * D * k) = k * kᴴ * D * k := by simp only [Matrix.mul_assoc]
  rw [e, Matrix.sub_mul, Matrix.sub_mul, Matrix.one_mul, sub_eq_zero]
  exact eq_comm

/-- [KERNEL] ★ a honestidade: ler de volta não é pagar. Existe uma isometria k e uma dinâmica D tais que
    a leitura T := k† D k é consistente, mas k NÃO entrelaça T com D. O Um pressuposto não é o Um posto. -/
theorem reading_back_does_not_make_covariant :
    ∃ (k : Matrix (Fin 2) (Fin 1) ℂ) (D : Matrix (Fin 2) (Fin 2) ℂ),
      kᴴ * k = 1 ∧ ¬ (k * (kᴴ * D * k) = D * k) := by
  refine ⟨!![1; 0], !![0, 1; 1, 0], ?_, ?_⟩
  · ext i j
    fin_cases i; fin_cases j
    simp [Matrix.mul_apply, Fin.sum_univ_two, Matrix.conjTranspose_apply]
  · intro h
    have h10 := congrFun (congrFun h 1) 0
    simp [Matrix.mul_apply, Fin.sum_univ_two, Matrix.conjTranspose_apply] at h10

end TGLExt.UmPosto
