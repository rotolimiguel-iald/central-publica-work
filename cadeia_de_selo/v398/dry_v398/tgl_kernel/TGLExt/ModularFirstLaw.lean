import TGLExt.Ergodicity

set_option autoImplicit false
set_option linter.unusedSectionVars false

/-!
# A primeira lei modular δS = δ⟨K⟩ — o elo que faltava do gate 5   [TGLExt — v51]

O gate 5 (derivar Einstein, não admitir Einstein) é uma COMPOSIÇÃO cujos
elos do lado-TGL agora estão TODOS em kernel:

* **δS = δ⟨K⟩** — A PRIMEIRA LEI MODULAR (`first_law_diagonal`, ESTE
  arquivo): a variação de primeira ordem da entropia de von Neumann sob
  uma perturbação de traço zero é EXATAMENTE o valor esperado da
  perturbação no hamiltoniano modular K = −log ρ. O que o form-check v5
  media a 1e-15, agora é TEOREMA (face diagonal, derivada genuína
  HasDerivAt);
* **T = 1/2π** — a temperatura modular (v47, `modPow_gibbs_boost`:
  o fluxo percorre K a velocidade 2π);
* **δQ = T·δS ⟹ δQ = (1/2π)·δ⟨K⟩** — a composição de Clausius TIPADA
  (`clausius_composition`);
* **a normalização 8πG** — `TGL.AreaScale.newtonPlanck_equivalence`
  (kernel desde as primeiras pedras: 2π/η = 8πG ⟺ κ = 2G) e
  `face_area_eq_G`;
* **a fonte é simétrica** — `gaugeSym_symmetric` (v48).

**O QUE RESTA da composição (a lista encolheu — a leitura do operador):**
(i) unicidade de Lovelock 4D [KNOWN — teorema clássico citável; fora do
alcance da mathlib hoje]; (ii) vetores de Killing APROXIMADOS para
regiões locais não-ideais [resíduo NOMEADO — compartilhado com Jacobson
1995 desde sempre; o estatuto E7 da casa]; (iii) conservação ∇^μ𝒫_μν = 0
no contínuo [o form-check v5 a verifica na sombra; contínuo OPEN].
NADA aqui afirma "provamos Einstein": afirma que TODO elo do lado
modular-TGL da cadeia de Jacobson–Clausius é agora teorema de kernel, e
os elos restantes são clássicos citáveis ou resíduos nomeados.
β JAMAIS entra. Sem sorry, sem axiom. Negativo honesto é resultado.
-/

namespace TGLExt

open Filter

noncomputable section

variable {n : Type} [Fintype n] [DecidableEq n]

/-! ## A — a primeira lei modular, com derivada genuína -/

/-- [KERNEL] ★ A PRIMEIRA LEI MODULAR δS = δ⟨K⟩ (face diagonal): para
    pesos `p > 0` e perturbação `q` de TRAÇO ZERO, a derivada em ε = 0 de
    `S(ε) = −Σ (pᵢ + ε·qᵢ)·log(pᵢ + ε·qᵢ)` é `Σ qᵢ·Kᵢ` com
    `Kᵢ = −log pᵢ` — a variação da entropia É o valor esperado da
    perturbação no hamiltoniano modular. O elo central da cadeia de
    Jacobson (δQ = TδS), que o form-check v5 media a 1e-15, como teorema. -/
theorem first_law_diagonal (p q : n → ℝ) (hp : ∀ i, 0 < p i)
    (hq : ∑ i, q i = 0) :
    HasDerivAt (fun ε : ℝ => -∑ i, (p i + ε * q i) * Real.log (p i + ε * q i))
      (∑ i, q i * (-Real.log (p i))) 0 := by
  have hterm : ∀ i : n, HasDerivAt
      (fun ε : ℝ => (p i + ε * q i) * Real.log (p i + ε * q i))
      ((Real.log (p i) + 1) * q i) 0 := by
    intro i
    have hg : HasDerivAt (fun ε : ℝ => p i + ε * q i) (q i) 0 := by
      simpa using ((hasDerivAt_id (0 : ℝ)).mul_const (q i)).const_add (p i)
    have hg0 : p i + (0 : ℝ) * q i = p i := by ring
    have hml : HasDerivAt (fun x : ℝ => x * Real.log x)
        (Real.log (p i + (0 : ℝ) * q i) + 1) (p i + (0 : ℝ) * q i) := by
      rw [hg0]
      exact Real.hasDerivAt_mul_log (hp i).ne'
    have hcomp := hml.comp (0 : ℝ) hg
    rw [hg0] at hcomp
    exact hcomp
  have hsum' := HasDerivAt.sum (u := Finset.univ) fun i _ => hterm i
  have hfun : (∑ i, fun ε : ℝ => (p i + ε * q i) * Real.log (p i + ε * q i))
      = fun ε : ℝ => ∑ i, (p i + ε * q i) * Real.log (p i + ε * q i) := by
    funext ε
    simp [Finset.sum_apply]
  rw [hfun] at hsum'
  have hsum : HasDerivAt
      (fun ε : ℝ => ∑ i, (p i + ε * q i) * Real.log (p i + ε * q i))
      (∑ i, (Real.log (p i) + 1) * q i) 0 := hsum'
  have hD : -(∑ i, (Real.log (p i) + 1) * q i)
      = ∑ i, q i * (-Real.log (p i)) := by
    have hsplit : ∑ i, (Real.log (p i) + 1) * q i
        = (∑ i, q i * Real.log (p i)) + ∑ i, q i := by
      rw [← Finset.sum_add_distrib]
      exact Finset.sum_congr rfl fun i _ => by ring
    rw [hsplit, hq, add_zero]
    simp only [mul_neg]
    rw [← Finset.sum_neg_distrib]
  exact hD ▸ hsum.neg

/-! ## B — a composição de Clausius, tipada -/

/-- [KERNEL] A COMPOSIÇÃO DE CLAUSIUS: dados a primeira lei (δS = δ⟨K⟩),
    a temperatura modular de Unruh (T = 1/2π, v47) e a relação de
    Clausius (δQ = T·δS), segue `δQ = (1/2π)·δ⟨K⟩` — o lado
    termodinâmico-modular da cadeia de Jacobson, com cada hipótese
    apontando para seu teorema de kernel (v51/v47) ou seu estatuto. -/
theorem clausius_composition (T dS dK dQ : ℝ)
    (hT : T = (2 * Real.pi)⁻¹)
    (hfirst : dS = dK)
    (hclausius : dQ = T * dS) :
    dQ = (2 * Real.pi)⁻¹ * dK := by
  rw [hclausius, hT, hfirst]

end

end TGLExt
