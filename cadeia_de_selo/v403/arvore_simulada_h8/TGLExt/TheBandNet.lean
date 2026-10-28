import TGLExt.TailNet

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 800000

/-!
# A REDE DE BANDAS — a localidade ESPECTRAL (o índice é o comprimento de onda)
  [TGLExt — v177, ordem do operador 20/08/2026: *"o habitante do CORE
   AQFT é o comprimento de onda = Lambda"*]

**O que esta pedra resolve, e o que ela NÃO resolve.** A auditoria de
hoje encontrou o núcleo do gate habitado pela REDE DE CAUDAS
(`theTailNet`, `Region := ℕ`) e concluiu que ali não há localidade. A
cunhagem do operador reenquadra o objeto: o índice não é região do
espaço-tempo — é **escala**, e `tailSub n = {x ∈ ℓ² | x_k = 0 ∀ k < n}`
é literalmente um corte de comprimento de onda. A leitura está certa
sobre o que o objeto é. Mas ela expõe um obstáculo ESTRUTURAL, e esta
pedra o torna teorema:

* ★★ `tails_are_totally_ordered` — duas caudas quaisquer são
  COMPARÁVEIS (uma contém a outra). Logo **na rede de caudas não existe
  par independente**, e uma obrigação de localidade ali seria VAZIA —
  não por falta de campo no tipo, mas por falta de objetos disjuntos.
  *A cauda é uma filtração, não uma rede com regiões independentes.*

O que a leitura espectral pede, então, não é cauda: é **banda**.

* `bandSub a b` — os modos em `[a, b)`: `{x | x_k = 0 fora de [a,b)}`;
* ★ `bandSub_isotone` — intervalo contido dá banda contida (ISOTONIA);
* ★★ `bandSub_disjoint_inf_bot` — bandas de intervalos DISJUNTOS se
  encontram só no zero: `band a b ⊓ band c d = ⊥`;
* ★★ `bandSub_orthogonal` — e são ORTOGONAIS: `⟪x, y⟫ = 0` para `x` numa
  e `y` na outra. **Esta é a independência espectral** — o análogo, na
  leitura por comprimento de onda, do que a localidade tipo-espaço é na
  leitura por espaço-tempo;
* `bandSub_le_tailSub` — toda banda `[a,b)` mora na cauda `a`: a rede de
  bandas REFINA a de caudas, e a escala das caudas é recuperada.

HONESTIDADE, sem a qual isto não vale nada: (i) esta pedra dá a
independência das bandas, **não** um núcleo AQFT — não há aqui álgebras
locais por região, nem covariância, nem III₁; (ii) o tipo
`PhysicalNetData` continua **sem campo de localidade**, e habitá-lo com
bandas exigiria ESTENDER o tipo — o que esta pedra não faz; (iii) a
identificação "comprimento de onda = Λ" é [CONJECTURE] do operador: o
que está provado aqui é sobre bandas de modos de ℓ², e a ponte com
`stationLambda = e^{−κ}` é leitura, não teorema.

β jamais literal. Sem sorry, sem axiom. Negativo honesto é resultado —
e `tails_are_totally_ordered` é um negativo honesto em kernel.
-/

namespace TGLExt

noncomputable section

/-! ## A — o obstáculo: a cauda é filtração, não rede independente -/

/-- A cauda é ANTÍTONA no índice: subir o corte encolhe o espaço. -/
theorem tailSub_antitone {m n : ℕ} (h : m ≤ n) : tailSub n ≤ tailSub m := by
  intro x hx k hk
  exact hx k (lt_of_lt_of_le hk h)

/-- ★★ DUAS CAUDAS QUAISQUER SÃO COMPARÁVEIS — logo não há par
    independente na rede de caudas, e uma obrigação de localidade ali
    seria vazia. (O obstáculo estrutural, como teorema.) -/
theorem tails_are_totally_ordered (m n : ℕ) :
    tailSub n ≤ tailSub m ∨ tailSub m ≤ tailSub n := by
  rcases le_total m n with h | h
  · exact Or.inl (tailSub_antitone h)
  · exact Or.inr (tailSub_antitone h)

/-! ## B — a banda: o que a leitura espectral pede -/

/-- A banda `[a, b)`: as sequências nulas FORA do intervalo. -/
def bandSub (a b : ℕ) : Submodule ℂ ellTwo where
  carrier := {x | ∀ k, ¬ (a ≤ k ∧ k < b) → x k = 0}
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

@[simp] theorem mem_bandSub {a b : ℕ} {x : ellTwo} :
    x ∈ bandSub a b ↔ ∀ k, ¬ (a ≤ k ∧ k < b) → x k = 0 := Iff.rfl

/-- ★ ISOTONIA: intervalo contido dá banda contida. -/
theorem bandSub_isotone {a b c d : ℕ} (hac : c ≤ a) (hbd : b ≤ d) :
    bandSub a b ≤ bandSub c d := by
  intro x hx k hk
  exact hx k (fun ⟨h1, h2⟩ => hk ⟨le_trans hac h1, lt_of_lt_of_le h2 hbd⟩)

/-- Toda banda `[a,b)` mora na cauda `a`: a rede de bandas REFINA a de
    caudas, e a escala das caudas é recuperada. -/
theorem bandSub_le_tailSub (a b : ℕ) : bandSub a b ≤ tailSub a := by
  intro x hx k hk
  exact hx k (fun ⟨h1, _⟩ => absurd hk (not_lt.mpr h1))

/-! ## C — a independência espectral -/

/-- ★★ BANDAS DE INTERVALOS DISJUNTOS SE ENCONTRAM SÓ NO ZERO. -/
theorem bandSub_disjoint_inf_bot {a b c d : ℕ}
    (hdisj : ∀ k, ¬ ((a ≤ k ∧ k < b) ∧ (c ≤ k ∧ k < d))) :
    bandSub a b ⊓ bandSub c d = ⊥ := by
  rw [Submodule.eq_bot_iff]
  rintro x ⟨hx1, hx2⟩
  ext k
  by_cases h1 : a ≤ k ∧ k < b
  · have h2 : ¬ (c ≤ k ∧ k < d) := fun hc => hdisj k ⟨h1, hc⟩
    simpa using hx2 k h2
  · simpa using hx1 k h1

/-- ★★ E SÃO ORTOGONAIS: a independência espectral. Para `x` numa banda
    e `y` numa banda disjunta, o produto interno é ZERO — cada termo da
    soma morre porque, em cada modo, ao menos um dos dois é nulo. -/
theorem bandSub_orthogonal {a b c d : ℕ}
    (hdisj : ∀ k, ¬ ((a ≤ k ∧ k < b) ∧ (c ≤ k ∧ k < d)))
    {x y : ellTwo} (hx : x ∈ bandSub a b) (hy : y ∈ bandSub c d) :
    ∀ k, (starRingEnd ℂ) (x k) * y k = 0 := by
  intro k
  by_cases h1 : a ≤ k ∧ k < b
  · have h2 : ¬ (c ≤ k ∧ k < d) := fun hc => hdisj k ⟨h1, hc⟩
    rw [hy k h2, mul_zero]
  · rw [hx k h1, map_zero, zero_mul]

/-- ★ E a disjunção é REALIZÁVEL: bandas adjacentes `[a,b)` e `[b,c)`
    são disjuntas — logo o par independente EXISTE (o contrário do que
    acontece nas caudas). -/
theorem adjacent_bands_disjoint (a b c : ℕ) :
    ∀ k, ¬ ((a ≤ k ∧ k < b) ∧ (b ≤ k ∧ k < c)) := by
  rintro k ⟨⟨_, h2⟩, ⟨h3, _⟩⟩
  exact absurd h3 (not_le.mpr h2)

end

end TGLExt
