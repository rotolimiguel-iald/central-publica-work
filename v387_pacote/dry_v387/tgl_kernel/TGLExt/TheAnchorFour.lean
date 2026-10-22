import TGLExt.HilbertHome

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 400000

/-!
# A ÂNCORA 4 VIRA `iff` — a isotonia de fibras nos DOIS sentidos
  [BANCADA — 24/08/2026 · frente 4 da derivação do operador]

## A derivação do operador

> *"A versão fiberwise iff fecha sem nova física: `P_{ker D₂}(ιx) = ιx ⟺ x ∈ ker D₁`,
> porque `P(ιx) = ιx ⟺ D₂(ιx) = 0` e, pelo entrelaçamento, `D₂(ιx) = V(D₁x)`; como `V`
> é isometria (injetiva), `V(D₁x) = 0 ⟺ D₁x = 0`."*

`starProjection_ker_isotone` (HilbertHome, já selada) dá a direção `⟸`. Aqui a recíproca:
**o canto da região maior fixa a imagem SOMENTE do núcleo menor** — o `⟹` que faltava.
A âncora deixa de ser monotonia e vira EQUIVALÊNCIA pontual.

## ⚠ O que fica declarado

A **Âncora 4 FORTE global** (`O₁ ≤ O₂ ⟺ P_F(O₁) ≤ P_F(O₂)` — o order EMBEDDING da rede
de regiões nos projetores) **NÃO decorre da isotonia**: exige representação fiel/
order-reflecting das regiões — fica NOMEADA como alvo (`[OPEN]`), não provada aqui.
Sem sorry, sem axiom. β jamais entra. Nada aqui move o gate.
-/

namespace TGLExt

noncomputable section

variable {H₁ H₂ W₁ W₂ : Type}
  [NormedAddCommGroup H₁] [InnerProductSpace ℂ H₁] [CompleteSpace H₁]
  [NormedAddCommGroup H₂] [InnerProductSpace ℂ H₂] [CompleteSpace H₂]
  [NormedAddCommGroup W₁] [NormedSpace ℂ W₁]
  [NormedAddCommGroup W₂] [NormedSpace ℂ W₂]

/-- ★★★ **A ÂNCORA 4 COMO `iff`** (fiberwise): sob o entrelaçamento `D₂∘ι = V∘D₁` com
    `ι` inclusão isométrica e `V` isometria, o canto da região maior fixa `ιx` SE E
    SOMENTE SE `x` está no núcleo da menor. A monotonia era metade; esta é a âncora
    inteira. -/
theorem starProjection_ker_isotone_iff (ι : H₁ →ₗᵢ[ℂ] H₂) (D₁ : H₁ →L[ℂ] W₁)
    (D₂ : H₂ →L[ℂ] W₂) (V : W₁ →ₗᵢ[ℂ] W₂)
    (h : ∀ x, D₂ (ι x) = V (D₁ x)) (x : H₁) :
    D₂.ker.starProjection (ι x) = ι x ↔ x ∈ D₁.ker := by
  constructor
  · intro hP
    have hmem : (ι x) ∈ D₂.ker := by
      rw [← hP]
      exact Submodule.starProjection_apply_mem _ _
    have h2 : D₂ (ι x) = 0 := hmem
    rw [h x] at h2
    have h1 : D₁ x = 0 := V.injective (by simpa using h2)
    exact h1
  · intro hx
    exact starProjection_ker_isotone ι D₁ D₂ V h hx

/-- ★ a leitura de posição: fixar-se no canto maior é EXATAMENTE pertencer ao núcleo
    menor — nenhum vetor de fora se disfarça (a metade nova), nenhum de dentro se perde
    (a metade velha). -/
theorem no_disguise_in_the_larger_corner (ι : H₁ →ₗᵢ[ℂ] H₂) (D₁ : H₁ →L[ℂ] W₁)
    (D₂ : H₂ →L[ℂ] W₂) (V : W₁ →ₗᵢ[ℂ] W₂)
    (h : ∀ x, D₂ (ι x) = V (D₁ x)) (x : H₁) (hx : x ∉ D₁.ker) :
    D₂.ker.starProjection (ι x) ≠ ι x := by
  intro hP
  exact hx ((starProjection_ker_isotone_iff ι D₁ D₂ V h x).mp hP)

end

end TGLExt
