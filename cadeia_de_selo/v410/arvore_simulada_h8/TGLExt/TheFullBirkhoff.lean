import TGLExt.TheCoordinateBridge

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 800000

/-!
# O BIRKHOFF PLENO — a dependência temporal é eliminada, e o estático emerge
  [BANCADA — 25/08/2026 · a extensão nomeada nas v208/v210, agora cunhada]

## O enunciado clássico e a divisão de selos

Birkhoff pleno: *esfericamente simétrico + vácuo ⟹ estático + Schwarzschild*. As ondas
anteriores selaram a metade estática (`STATIC_SPHERICAL_VACUUM_IFF_SCHWARZSCHILD_CLASS`);
esta pedra elimina a dependência temporal: com `A(t,r), B(t,r)`, a componente cruzada do
tensor de Einstein da classe é `G_tr ∝ ∂ₜB/(r·B)` [KNOWN, forma padrão — construída à mão,
como as componentes mistas da v210], logo **vácuo ⟹ `∂ₜB = 0` ⟹ `B` é ESTÁTICA** (constância
em convexo, a mesma ferramenta); a cadeia da v210 dá Schwarzschild EM CADA FATIA de tempo; e
a estática de `B` COLA o `r_s` entre as fatias — **`r_s` é uma constante única**. O que resta
livre é exatamente o que DEVE restar: o gauge temporal `C(t)` (removível por `dt′ = √C·dt`,
reparametrização [KNOWN, declarada — não suprimida]).

## O que se prova

* ★★ `birkhoff_B_is_static` — `G_tr = 0` (i.e. `∂ₜB = 0`) num intervalo convexo aberto ⟹
  `B(t,r) = B(t₀,r)`: a fatia radial não depende do tempo;
* ★★★ **`the_full_birkhoff_class`** — a CADEIA PLENA: `G_tr = G^t_t = G^r_r = 0` em
  `I × s` (convexos abertos, domínio regular) ⟹ **∃ um único `r_s` constante e um gauge
  temporal `C(t)`** com `(B t r)⁻¹ = 1 − r_s/r` e `A t r = C(t)·(1 − r_s/r)` em todo o
  domínio. *Esfericamente simétrico + vácuo ⟹ estático (a menos do gauge) + Schwarzschild.*

## ⚠ Delimitações

`G_tr ∝ ∂ₜB` é a forma padrão [KNOWN] da classe, definida à mão na MESMA estação das
componentes mistas (v210) e do `AnsatzEinstein` da casa; a derivação Christoffel→Ricci em
kernel segue NOMEADA. O gauge `C(t)` fica DECLARADO: vácuo não o normaliza (a lição do `C`
constante, agora na face temporal). β jamais entra. Sem sorry, sem axiom. Nada aqui move o
gate.
-/

namespace TGLExt

noncomputable section

/-- ★★ **A ESTÁTICA DERIVADA**: `∂ₜB = 0` num intervalo convexo aberto ⟹ a fatia não
    depende do tempo — `B(t,r) = B(t₀,r)`. (O conteúdo de `G_tr = 0` [KNOWN].) -/
theorem birkhoff_B_is_static (B : ℝ → ℝ → ℝ) (I : Set ℝ)
    (hIconv : Convex ℝ I) (hIopen : IsOpen I) (r : ℝ)
    (hstatic : ∀ t ∈ I, HasDerivAt (fun τ => B τ r) 0 t)
    (t₀ t : ℝ) (ht₀ : t₀ ∈ I) (ht : t ∈ I) : B t r = B t₀ r :=
  const_of_hasDerivAt_zero (fun τ => B τ r) I hIconv hIopen hstatic t t₀ ht ht₀

/-- ★★★ **O BIRKHOFF PLENO DA CLASSE**: `G_tr = G^t_t = G^r_r = 0` em `I × s` ⟹ existe
    UM `r_s` constante (o mesmo em todas as fatias de tempo) e um gauge temporal `C(t)`
    com `(B t r)⁻¹ = 1 − r_s/r` e `A t r = C(t)·(1 − r_s/r)`. *Esférico + vácuo ⟹
    estático (a menos do gauge declarado) + Schwarzschild.* -/
theorem the_full_birkhoff_class (A B : ℝ → ℝ → ℝ) (I s : Set ℝ)
    (hIconv : Convex ℝ I) (hIopen : IsOpen I)
    (hsconv : Convex ℝ s) (hsopen : IsOpen s)
    (hpos : ∀ r ∈ s, 0 < r)
    (hAne : ∀ t ∈ I, ∀ r ∈ s, A t r ≠ 0) (hBne : ∀ t ∈ I, ∀ r ∈ s, B t r ≠ 0)
    (hAdiff : ∀ t ∈ I, ∀ r ∈ s, DifferentiableAt ℝ (A t) r)
    (hBdiff : ∀ t ∈ I, ∀ r ∈ s, DifferentiableAt ℝ (B t) r)
    (hGtr : ∀ r ∈ s, ∀ t ∈ I, HasDerivAt (fun τ => B τ r) 0 t)
    (hTT : ∀ t ∈ I, ∀ r ∈ s, einsteinTT (B t) r = 0)
    (hRR : ∀ t ∈ I, ∀ r ∈ s, einsteinRR (A t) (B t) r = 0)
    (t₀ : ℝ) (ht₀ : t₀ ∈ I) (r₀ : ℝ) (hr₀ : r₀ ∈ s) :
    ∃ rs : ℝ, ∃ CF : ℝ → ℝ, ∀ t ∈ I, ∀ r ∈ s,
      (B t r)⁻¹ = 1 - rs / r ∧ A t r = CF t * (1 - rs / r) := by
  have chain : ∀ t ∈ I, ∃ rst Ct : ℝ, ∀ r ∈ s,
      (B t r)⁻¹ = 1 - rst / r ∧ A t r = Ct * (1 - rst / r) := fun t ht =>
    einstein_vacuum_implies_schwarzschild (A t) (B t) s hsconv hsopen hpos
      (hAne t ht) (hBne t ht) (hAdiff t ht) (hBdiff t ht) (hTT t ht) (hRR t ht) r₀ hr₀
  choose! rsF CF hF using chain
  refine ⟨rsF t₀, CF, fun t ht r hr => ?_⟩
  have hrne : r ≠ 0 := ne_of_gt (hpos r hr)
  have hstat : B t r = B t₀ r :=
    birkhoff_B_is_static B I hIconv hIopen r (hGtr r hr) t₀ t ht₀ ht
  have h1 := (hF t ht r hr).1
  have h2 := (hF t₀ ht₀ r hr).1
  have heq : 1 - rsF t / r = 1 - rsF t₀ / r := by
    rw [← h1, hstat, h2]
  have hdiv : rsF t / r = rsF t₀ / r := by linarith [heq]
  have hrs : rsF t = rsF t₀ := by
    have h3 : rsF t / r * r = rsF t₀ / r * r := by rw [hdiv]
    rwa [div_mul_cancel₀ _ hrne, div_mul_cancel₀ _ hrne] at h3
  constructor
  · rw [(hF t ht r hr).1, hrs]
  · rw [(hF t ht r hr).2, hrs]

end

end TGLExt
