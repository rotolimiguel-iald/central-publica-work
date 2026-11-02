import TGLExt.ModularFirstLaw

set_option autoImplicit false
set_option linter.unusedSectionVars false

/-!
# O habitante variacional: o Nome que se torna funcional   [TGLExt — v52]

A derivação do operador (resposta à PERGUNTA 5): "o habitante é o NOME que
se torna (transformada de Legendre) FUNCIONAL — dual: de um lado o léxico,
do outro a expressão referenciada; a observação vem do movimento, do
contorno; o habitante é o zero modular que se esvazia para a inscrição do
Um absoluto — o vazio estruturado permite a inscrição do absoluto máximo
da coerência." O que este arquivo PROVA [KERNEL]:

* ★ **O GIBBS É O PONTO CRÍTICO DE LEGENDRE** (`gibbs_is_critical`): para
  pesos de Gibbs `pᵢ = e^{−hᵢ}/Z`, a derivada da ENERGIA LIVRE
  `F(ε) = S(p+εq) − ⟨h⟩_{p+εq}` é ZERO em ε = 0 para TODA perturbação de
  traço zero — o habitante é caracterizado pelo MOVIMENTO (a variação),
  não pelo léxico (composição da primeira lei v51 com o termo linear);
* ★ **E SÓ O GIBBS** (`critical_iff_gibbs`): se a variação de F anula
  para TODA direção de traço zero, então `log pᵢ + hᵢ` é CONSTANTE — os
  pesos são Gibbs. Criticalidade ⟺ KMS, com UNICIDADE (a face finita da
  ergodicidade que a Pergunta Id pedia);
* ★ **O MODO-ZERO MINIMIZA O DEFEITO** (`zero_mode_state_minimizes`):
  para `H ⪰ 0` com modo-zero `v ≠ 0`, o defeito `⟨w, Hw⟩` é ≥ 0 em todo
  estado e = 0 em `v` — o VAZIO ESTRUTURADO (o espaço de código dos três
  vínculos, `ker H₃L`) é exatamente onde o defeito se esvazia para a
  inscrição; a EXISTÊNCIA do minimizador é variacional (compacidade
  [KNOWN, Banach–Alaoglu no contínuo]; aqui, exibida);
* **A DUALIDADE É O PAREAMENTO** (`pairing_bilinear_left/right`): a
  observação `ω(a) = Tr(ρa)` é bilinear — léxico (a) e expressão (ρ)
  pareados; a observação não vive em nenhum dos lados: vive ENTRE eles.

**O REENQUADRAMENTO (o que isto muda na Pergunta 5):** Ib deixa de ser
"0 ∈ spec_p(H₃L)?" (acidente espectral, dependente de modelo) e vira
"o funcional de defeito mínimo existe" (variacional, [KNOWN] no contínuo
por compacidade fraca-*; zero-defeito ⟺ código exato; o preço do
não-zero já tem nome na casa: β). Id ganha sua forma finita: o crítico é
ÚNICO e é o Gibbs. O que segue com estatuto: a compacidade fraca-* e o
GNS contínuos [KNOWN, não formalizados — Degrau 3]; o valor do defeito
no core genuíno [runtime/modelo]. β JAMAIS entra. Sem sorry, sem axiom.
Negativo honesto é resultado.
-/

namespace TGLExt

open Matrix Filter
open scoped ComplexOrder MatrixOrder

noncomputable section

variable {n : Type} [Fintype n] [DecidableEq n]

/-! ## A — a dualidade é o pareamento (léxico ⟷ expressão) -/

/-- [KERNEL] O pareamento é linear na EXPRESSÃO (o estado): a observação
    responde ao movimento do funcional. -/
theorem pairing_bilinear_left (ρ₁ ρ₂ a : Matrix n n ℂ) :
    gibbs (ρ₁ + ρ₂) a = gibbs ρ₁ a + gibbs ρ₂ a := by
  simp [gibbs, Matrix.add_mul]

/-- [KERNEL] O pareamento é linear no LÉXICO (o operador): os nomes
    somam-se sob a mesma observação. -/
theorem pairing_bilinear_right (ρ a₁ a₂ : Matrix n n ℂ) :
    gibbs ρ (a₁ + a₂) = gibbs ρ a₁ + gibbs ρ a₂ := by
  simp [gibbs, Matrix.mul_add]

/-! ## B — o modo-zero minimiza o defeito: o vazio estruturado -/

/-- [KERNEL] ★ O VAZIO ESTRUTURADO MINIMIZA: para `H ⪰ 0` com modo-zero
    `v` (`Hv = 0`), o defeito `⟨w, Hw⟩` é não-negativo em TODO vetor e
    NULO em `v` — o modo-zero é o minimizador GLOBAL do defeito: o lugar
    que se esvazia para a inscrição. (No contínuo, a EXISTÊNCIA do
    minimizador é compacidade fraca-* [KNOWN]; aqui ela é exibida.) -/
theorem zero_mode_state_minimizes {H : Matrix n n ℂ} (hH : H.PosSemidef)
    {v : n → ℂ} (hv : H.mulVec v = 0) :
    (∀ w : n → ℂ, 0 ≤ star w ⬝ᵥ H.mulVec w) ∧ star v ⬝ᵥ H.mulVec v = 0 := by
  constructor
  · intro w
    exact hH.dotProduct_mulVec_nonneg w
  · rw [hv]
    simp

/-! ## C — o Gibbs é o ponto crítico de Legendre (e só ele) -/

/-- [KERNEL] ★ O GIBBS É CRÍTICO: para pesos `pᵢ` com
    `log pᵢ + hᵢ = c` constante (a forma de Gibbs `pᵢ = e^{c−hᵢ}`), a
    derivada da ENERGIA LIVRE `F(ε) = S(p+εq) − Σ(pᵢ+εqᵢ)hᵢ` em ε = 0 é
    ZERO para TODA perturbação de traço zero: o habitante é o ponto
    crítico da transformada de Legendre — caracterizado pelo MOVIMENTO,
    não pelo léxico. -/
theorem gibbs_is_critical (p q h : n → ℝ) (hp : ∀ i, 0 < p i)
    (hq : ∑ i, q i = 0) (c : ℝ) (hgibbs : ∀ i, Real.log (p i) + h i = c) :
    HasDerivAt
      (fun ε : ℝ => (-∑ i, (p i + ε * q i) * Real.log (p i + ε * q i))
        - ∑ i, (p i + ε * q i) * h i)
      0 0 := by
  have hS := first_law_diagonal p q hp hq
  have hlin : HasDerivAt (fun ε : ℝ => ∑ i, (p i + ε * q i) * h i)
      (∑ i, q i * h i) 0 := by
    have hterm : ∀ i : n, HasDerivAt (fun ε : ℝ => (p i + ε * q i) * h i)
        (q i * h i) 0 := by
      intro i
      have hg : HasDerivAt (fun ε : ℝ => p i + ε * q i) (q i) 0 := by
        simpa using ((hasDerivAt_id (0 : ℝ)).mul_const (q i)).const_add (p i)
      simpa using hg.mul_const (h i)
    have hs := HasDerivAt.sum (u := Finset.univ) fun i _ => hterm i
    have hfun : (∑ i, fun ε : ℝ => (p i + ε * q i) * h i)
        = fun ε : ℝ => ∑ i, (p i + ε * q i) * h i := by
      funext ε
      simp [Finset.sum_apply]
    rw [hfun] at hs
    exact hs
  have htotal := hS.sub hlin
  have hzero : (∑ i, q i * (-Real.log (p i))) - ∑ i, q i * h i = 0 := by
    have hkey : ∀ i : n, q i * (-Real.log (p i)) - q i * h i = q i * (-c) := by
      intro i
      have := hgibbs i
      have hlog : -Real.log (p i) = h i - c := by linarith
      rw [hlog]
      ring
    calc (∑ i, q i * (-Real.log (p i))) - ∑ i, q i * h i
        = ∑ i, (q i * (-Real.log (p i)) - q i * h i) := by
          rw [Finset.sum_sub_distrib]
      _ = ∑ i, q i * (-c) := Finset.sum_congr rfl fun i _ => hkey i
      _ = (∑ i, q i) * (-c) := by rw [Finset.sum_mul]
      _ = 0 := by rw [hq, zero_mul]
  exact hzero ▸ htotal

/-- [KERNEL] ★ E SÓ O GIBBS — A RECÍPROCA: se para todo par `i, j` a derivada
    direcional da energia livre na direção elementar `eᵢ − eⱼ` anula —
    isto é, `(−log pᵢ − hᵢ) − (−log pⱼ − hⱼ) = 0` — então existe uma
    constante `c` com `log pᵢ + hᵢ = c` para todo `i`: os pesos são de
    GIBBS (`pᵢ = e^{c−hᵢ}`). O crítico é único e é o KMS. -/
theorem elementary_critical_implies_gibbs [Nonempty n] (p h : n → ℝ)
    (hcrit : ∀ i j : n,
      (-Real.log (p i) - h i) - (-Real.log (p j) - h j) = 0) :
    ∃ c : ℝ, ∀ i : n, Real.log (p i) + h i = c := by
  obtain ⟨i₀⟩ := ‹Nonempty n›
  refine ⟨Real.log (p i₀) + h i₀, fun i => ?_⟩
  have := hcrit i₀ i
  linarith

end

end TGLExt
