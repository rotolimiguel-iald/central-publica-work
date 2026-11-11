import TGLExt.BisognanoWichmann

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 400000

/-!
# A MUDANÇA DE HORIZONTE FÍSICA É O BOOST — e o defeito ganha VALOR
  [BANCADA — 24/08/2026 · a parede, frentes 1 e 2 da derivação do operador]

## A derivação do operador

> *"A física seleciona o U: `U_phys = U(Λ_W(χ))` — o boost de Lorentz que preserva a cunha…
> o fluxo modular não é apenas parecido com uma mudança de horizonte: na cunha ele é
> implementado pelo boost físico (Bisognano–Wichmann [KNOWN])… `U_phys` escolhe qual
> horizonte/canal é físico; `β_input` calibra o valor do defeito nesse canal. Nenhuma
> expressão para κ foi necessária."*

## O que se prova

* **`PhysicalHorizonChange`** — o predicado que SELECIONA o `U`: existe rapidez `χ` com
  `U = boost χ`. Deixa de ser unitário genérico: os teoremas geométricos já selados
  (grupo, `η`, cunha, `e^{±χ}` nas nulas) transferem-se por composição;
* ★★★ **`the_defect_has_a_value`** — com `|s|² = β` (reflexão) e `|c|² = 1−β` (transmissão)
  da matriz-S selada: **`‖c‖·‖s‖ = √(β(1−β))`** — o defeito de amplitude FECHA em valor, e
  o seu QUADRADO é `β(1−β)` — exatamente o defeito de transporte (`Var = β(1−β)`, v26) que
  a arquitetura já carregava: *o defeito de transporte é a POTÊNCIA do defeito de amplitude.*

## ⚠ Delimitações

A identificação `U(Λ_W(χ)) = Δ_W^{−iχ/2π}` é **Bisognano–Wichmann [KNOWN, externa]** — o
kernel prova a face geométrica (aqui composta) e a face Gibbs-modular
(`sigma_gibbs_boost`, já selada); a identificação na rede CONTÍNUA segue no ledger externo.
β jamais literal (o teorema é genérico em β; o runtime instancia). Sem sorry, sem axiom.
Nada aqui move o gate.
-/

namespace TGLExt

open Matrix

/-- ★ O PREDICADO FÍSICO: `U` é mudança de horizonte física ⟺ é um boost da cunha. -/
def PhysicalHorizonChange (U : Matrix (Fin 2) (Fin 2) ℝ) : Prop :=
  ∃ χ : ℝ, U = boost χ

/-- todo boost é físico (a testemunha canônica). -/
theorem boost_is_physical (χ : ℝ) : PhysicalHorizonChange (boost χ) := ⟨χ, rfl⟩

/-- ★★ o físico FORMA GRUPO: composição de mudanças físicas é física (adição de rapidez). -/
theorem physical_horizon_group {U V : Matrix (Fin 2) (Fin 2) ℝ}
    (hU : PhysicalHorizonChange U) (hV : PhysicalHorizonChange V) :
    PhysicalHorizonChange (U * V) := by
  obtain ⟨χ, rfl⟩ := hU
  obtain ⟨ξ, rfl⟩ := hV
  exact ⟨χ + ξ, boost_add χ ξ⟩

/-- ★★ o físico PRESERVA A CAUSALIDADE: `Uᵀ·η·U = η`. -/
theorem physical_horizon_preserves_eta {U : Matrix (Fin 2) (Fin 2) ℝ}
    (hU : PhysicalHorizonChange U) : Uᵀ * minkEta * U = minkEta := by
  obtain ⟨χ, rfl⟩ := hU
  exact boost_preserves_eta χ

/-- ★★ o físico PRESERVA A CUNHA: o horizonte não vaza. -/
theorem physical_horizon_preserves_wedge {U : Matrix (Fin 2) (Fin 2) ℝ}
    (hU : PhysicalHorizonChange U) (x t : ℝ) (h : |t| < x) :
    |U.mulVec ![x, t] 1| < U.mulVec ![x, t] 0 := by
  obtain ⟨χ, rfl⟩ := hU
  exact boost_preserves_wedge χ x t h

/-- ★★★ **O DEFEITO TEM VALOR.** Com `s² = β` e `c² = 1−β` (a matriz-S da fronteira),
    o defeito de amplitude fecha: `(c·s)² = β(1−β)` e `c·s = √(β(1−β))`.
    *O defeito de transporte da arquitetura (`Var = β(1−β)`, v26) é a POTÊNCIA deste.* -/
theorem the_defect_has_a_value (β c s : ℝ) (hc : 0 ≤ c) (hs : 0 ≤ s)
    (hs2 : s ^ 2 = β) (hc2 : c ^ 2 = 1 - β) :
    (c * s) ^ 2 = β * (1 - β) ∧ c * s = Real.sqrt (β * (1 - β)) := by
  have h1 : (c * s) ^ 2 = β * (1 - β) := by
    rw [mul_pow, hs2, hc2]; ring
  refine ⟨h1, ?_⟩
  rw [← h1, Real.sqrt_sq (mul_nonneg hc hs)]

/-- ★ o fecho: a seleção física + o valor do defeito, num enunciado — `U_phys` escolhe o
    canal; `β` calibra o defeito nele; e κ NÃO apareceu. -/
theorem the_wall_gains_a_value (χ β c s : ℝ) (hc : 0 ≤ c) (hs : 0 ≤ s)
    (hs2 : s ^ 2 = β) (hc2 : c ^ 2 = 1 - β) :
    PhysicalHorizonChange (boost χ) ∧ c * s = Real.sqrt (β * (1 - β)) :=
  ⟨boost_is_physical χ, (the_defect_has_a_value β c s hc hs hs2 hc2).2⟩

end TGLExt
