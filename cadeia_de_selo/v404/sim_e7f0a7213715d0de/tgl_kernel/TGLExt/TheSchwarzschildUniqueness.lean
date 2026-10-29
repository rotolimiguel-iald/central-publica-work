import TGLExt.TheTwoFunctionSolder

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 800000

/-!
# A UNICIDADE DE SCHWARZSCHILD NA SOLDA — as duas integrais primeiras
  [BANCADA — 24-25/08/2026 · a derivação do operador, cunhada]

## A derivação do operador (o degrau para o Einstein geral)

> *"Defina `μ(r) := r(1 − 1/B)`. Então `E_t = 0 ⟹ μ′ = 0` — a massa. Defina `Σ := A·B`.
> Então `r·Σ′ = AB(B−1) + AB(1−B) = 0`. Logo `B = (1 − r_s/r)⁻¹` e `A = C·(1 − r_s/r)`.
> **Acabou.** … vácuo sozinho NÃO força `C = 1` — exigir `C = 1` antes da fixação do gauge
> faria o teorema artificialmente forte… derivada zero em convexo ⟹ constante. Você NÃO
> precisa resolver uma EDO por biblioteca."*

Com `A := a²`, `B := b²` (a classe `TheTwoFunctionSolder`), as equações de vácuo radiais
reduzem aos numeradores [KNOWN, parametrização estática esférica padrão]:

    E_t(r) := r·B′ + B² − B = 0        E_r(r) := r·A′ − A·B + A = 0

## O que se prova

* ★★★ `massAspect_deriv_zero` — a primeira integral: `E_t = 0 ⟹ (r(1−1/B))′ = 0`;
* ★★★ `solderProduct_deriv_zero` — a segunda: `E_t = E_r = 0 ⟹ (A·B)′ = 0`
  (`linear_combination B·E_r + A·E_t`);
* ★★★ **`vacuum_implies_schwarzschild_class`** — em domínio convexo aberto com `r > 0`,
  `B ≠ 0`: **`(B r)⁻¹ = 1 − r_s/r` e `A = C·(1 − r_s/r)`** — a CLASSE de Schwarzschild,
  com a liberdade de gauge `C` DECLARADA;
* ★★ `schwarzschild_class_implies_vacuum` — a volta, com derivadas explícitas;
* ★★ `the_angular_component_is_free` — o bônus: da primeira integral numa vizinhança,
  `r·F″ + 2F′ = 0` (`F = 1/B`) — o componente angular anula SEM Bianchi como caixa-preta.

## ⚠ Delimitações

O selo desta pedra é **`STATIC_SPHERICAL_VACUUM_IFF_SCHWARZSCHILD_CLASS`**. O
**`FULL_BIRKHOFF`** (partir de `A(t,r), B(t,r)` e eliminar `t`) é extensão futura NOMEADA —
os selos não se misturam. A ponte `G_{μν}`-completo → `(E_t, E_r)` na convenção da casa é o
elo coordenado declarado [KNOWN]. β jamais entra. Sem sorry, sem axiom. Nada aqui move o gate.
-/

namespace TGLExt

noncomputable section

/-- a equação de vácuo temporal (numerador): `E_t = r·B′ + B² − B`. -/
def vacuumT (B : ℝ → ℝ) (r : ℝ) : ℝ := r * deriv B r + B r ^ 2 - B r

/-- a equação de vácuo radial (numerador): `E_r = r·A′ − A·B + A`. -/
def vacuumR (A B : ℝ → ℝ) (r : ℝ) : ℝ := r * deriv A r - A r * B r + A r

/-- o aspecto de massa: `μ(r) = r·(1 − 1/B)`. -/
def massAspect (B : ℝ → ℝ) (r : ℝ) : ℝ := r * (1 - (B r)⁻¹)

/-- o produto da solda: `Σ = A·B`. -/
def solderProduct (A B : ℝ → ℝ) (r : ℝ) : ℝ := A r * B r

/-- ★★★ **A PRIMEIRA INTEGRAL (a massa)**: `E_t = 0 ⟹ μ′ = 0` — a derivada exibida:
    `μ′ = (B² − B + r·B′)/B² = E_t/B²`. -/
theorem massAspect_deriv_zero (B : ℝ → ℝ) (r : ℝ)
    (hB : DifferentiableAt ℝ B r) (hBne : B r ≠ 0)
    (hvac : vacuumT B r = 0) :
    HasDerivAt (massAspect B) 0 r := by
  have h1 : HasDerivAt (fun t => (B t)⁻¹) (-(deriv B r) / B r ^ 2) r :=
    hB.hasDerivAt.inv hBne
  have h2 : HasDerivAt (fun t => (1 : ℝ) - (B t)⁻¹) (deriv B r / B r ^ 2) r := by
    have h := h1.const_sub (1 : ℝ)
    simpa [neg_div] using h
  have h3 : HasDerivAt (fun t => t * ((1 : ℝ) - (B t)⁻¹))
      (1 * ((1 : ℝ) - (B r)⁻¹) + r * (deriv B r / B r ^ 2)) r :=
    (hasDerivAt_id r).mul h2
  have hval : 1 * ((1 : ℝ) - (B r)⁻¹) + r * (deriv B r / B r ^ 2) = 0 := by
    unfold vacuumT at hvac
    field_simp
    linarith [hvac]
  rw [hval] at h3
  exact h3

/-- ★★★ **A SEGUNDA INTEGRAL (a solda)**: `E_t = 0 ∧ E_r = 0 ⟹ (A·B)′ = 0` — a
    combinação `B·E_r + A·E_t` anula `r·(A′B + AB′)` por `ring`. -/
theorem solderProduct_deriv_zero (A B : ℝ → ℝ) (r : ℝ) (hr : r ≠ 0)
    (hA : DifferentiableAt ℝ A r) (hB : DifferentiableAt ℝ B r)
    (hT : vacuumT B r = 0) (hR : vacuumR A B r = 0) :
    HasDerivAt (solderProduct A B) 0 r := by
  have h : HasDerivAt (fun t => A t * B t)
      (deriv A r * B r + A r * deriv B r) r :=
    hA.hasDerivAt.mul hB.hasDerivAt
  have key : r * (deriv A r * B r + A r * deriv B r) = 0 := by
    unfold vacuumT at hT
    unfold vacuumR at hR
    linear_combination B r * hR + A r * hT
  have hval : deriv A r * B r + A r * deriv B r = 0 :=
    (mul_eq_zero.mp key).resolve_left hr
  rw [show (0 : ℝ) = deriv A r * B r + A r * deriv B r from hval.symm]
  exact h

/-- constância em convexo aberto a partir de `HasDerivAt · 0` ponto a ponto —
    a ferramenta da mathlib que dissolve a "lacuna da EDO". -/
theorem const_of_hasDerivAt_zero (f : ℝ → ℝ) (s : Set ℝ)
    (hconv : Convex ℝ s) (hopen : IsOpen s)
    (hf : ∀ r ∈ s, HasDerivAt f 0 r) (x y : ℝ) (hx : x ∈ s) (hy : y ∈ s) :
    f x = f y := by
  have hdiff : DifferentiableOn ℝ f s := fun r hr =>
    ((hf r hr).differentiableAt).differentiableWithinAt
  have hzero : ∀ r ∈ s, fderivWithin ℝ f s r = 0 := by
    intro r hr
    have hAt : fderiv ℝ f r = 0 := by
      have h := (hf r hr).hasFDerivAt.fderiv
      rw [h]
      simp
    rw [fderivWithin_of_isOpen hopen hr, hAt]
  exact hconv.is_const_of_fderivWithin_eq_zero hdiff hzero hx hy

/-- ★★★ **VÁCUO ⟹ A CLASSE DE SCHWARZSCHILD** (domínio convexo aberto, `r > 0`,
    `B ≠ 0`): existem `r_s` e `C` com `(B r)⁻¹ = 1 − r_s/r` e `A r = C·(1 − r_s/r)` em
    todo o domínio — a liberdade de gauge `C` DECLARADA, não suprimida. -/
theorem vacuum_implies_schwarzschild_class (A B : ℝ → ℝ) (s : Set ℝ)
    (hconv : Convex ℝ s) (hopen : IsOpen s)
    (hpos : ∀ r ∈ s, 0 < r) (hBne : ∀ r ∈ s, B r ≠ 0)
    (hA : ∀ r ∈ s, DifferentiableAt ℝ A r) (hB : ∀ r ∈ s, DifferentiableAt ℝ B r)
    (hT : ∀ r ∈ s, vacuumT B r = 0) (hR : ∀ r ∈ s, vacuumR A B r = 0)
    (r₀ : ℝ) (hr₀ : r₀ ∈ s) :
    ∃ rs C : ℝ, ∀ r ∈ s,
      (B r)⁻¹ = 1 - rs / r ∧ A r = C * (1 - rs / r) := by
  have hmu : ∀ r ∈ s, massAspect B r = massAspect B r₀ := fun r hr =>
    const_of_hasDerivAt_zero (massAspect B) s hconv hopen
      (fun t ht => massAspect_deriv_zero B t (hB t ht) (hBne t ht) (hT t ht)) r r₀ hr hr₀
  have hSig : ∀ r ∈ s, solderProduct A B r = solderProduct A B r₀ := fun r hr =>
    const_of_hasDerivAt_zero (solderProduct A B) s hconv hopen
      (fun t ht => solderProduct_deriv_zero A B t (ne_of_gt (hpos t ht))
        (hA t ht) (hB t ht) (hT t ht) (hR t ht)) r r₀ hr hr₀
  refine ⟨massAspect B r₀, solderProduct A B r₀, fun r hr => ?_⟩
  have hrne : r ≠ 0 := ne_of_gt (hpos r hr)
  have hBr : B r ≠ 0 := hBne r hr
  have h1 : r * (1 - (B r)⁻¹) = massAspect B r₀ := by
    have h := hmu r hr
    unfold massAspect at h
    exact h
  have hinv : (B r)⁻¹ = 1 - massAspect B r₀ / r := by
    have h2 : massAspect B r₀ / r = 1 - (B r)⁻¹ := by
      rw [← h1, mul_div_cancel_left₀ _ hrne]
    linarith [h2]
  refine ⟨hinv, ?_⟩
  have h2 : A r * B r = solderProduct A B r₀ := hSig r hr
  have hAval : A r = solderProduct A B r₀ * (B r)⁻¹ := by
    rw [← h2, mul_assoc, mul_inv_cancel₀ hBr, mul_one]
  rw [hAval, hinv]

/-- ★★ **A VOLTA**: o membro de Schwarzschild (com gauge `C`) satisfaz `E_t = E_r = 0`
    em todo `r ≠ 0` com `1 − r_s/r ≠ 0` — derivadas explícitas, álgebra de corpo. -/
theorem schwarzschild_class_implies_vacuum (rs C r : ℝ) (hr : r ≠ 0)
    (hf : 1 - rs / r ≠ 0) :
    vacuumT (fun t => (1 - rs / t)⁻¹) r = 0
    ∧ vacuumR (fun t => C * (1 - rs / t)) (fun t => (1 - rs / t)⁻¹) r = 0 := by
  have h1 : HasDerivAt (fun t : ℝ => rs / t) (-(rs / r ^ 2)) r := by
    have h := (hasDerivAt_inv hr).const_mul rs
    have hv : rs * -(r ^ 2)⁻¹ = -(rs / r ^ 2) := by
      field_simp
    rw [hv] at h
    simpa [div_eq_mul_inv] using h
  have hfder : HasDerivAt (fun t : ℝ => 1 - rs / t) (rs / r ^ 2) r := by
    have h := h1.const_sub (1 : ℝ)
    simpa using h
  have hBder : HasDerivAt (fun t : ℝ => (1 - rs / t)⁻¹)
      (-(rs / r ^ 2) / (1 - rs / r) ^ 2) r := hfder.inv hf
  have hAder : HasDerivAt (fun t : ℝ => C * (1 - rs / t)) (C * (rs / r ^ 2)) r :=
    hfder.const_mul C
  constructor
  · unfold vacuumT
    rw [hBder.deriv]
    have hr2 : r ^ 2 ≠ 0 := pow_ne_zero 2 hr
    have hf2 : (1 - rs / r) ^ 2 ≠ 0 := pow_ne_zero 2 hf
    field_simp
    ring
  · unfold vacuumR
    rw [hAder.deriv]
    have hr2 : r ^ 2 ≠ 0 := pow_ne_zero 2 hr
    have hrr : r - rs ≠ 0 := by
      intro h0
      apply hf
      have hrs : rs = r := by linarith
      rw [hrs, div_self hr]
      norm_num
    field_simp [hrr]
    ring

/-- ★★ **O COMPONENTE ANGULAR É DE GRAÇA**: se a primeira integral vale numa vizinhança
    (`t·F′ = 1 − F` em `s` aberto), então `r·F″ + 2F′ = 0` — sem Bianchi como
    caixa-preta. -/
theorem the_angular_component_is_free (F : ℝ → ℝ) (s : Set ℝ) (hopen : IsOpen s)
    (r : ℝ) (hr : r ∈ s)
    (hF : DifferentiableAt ℝ F r) (hF2 : DifferentiableAt ℝ (deriv F) r)
    (hfirst : ∀ t ∈ s, t * deriv F t = 1 - F t) :
    r * deriv (deriv F) r + 2 * deriv F r = 0 := by
  have hev : (fun t => t * deriv F t + F t - 1) =ᶠ[nhds r] (fun _ => (0 : ℝ)) := by
    filter_upwards [hopen.mem_nhds hr] with t ht
    have h := hfirst t ht
    show t * deriv F t + F t - 1 = 0
    linarith
  have hmul : HasDerivAt (fun t => t * deriv F t)
      (1 * deriv F r + r * deriv (deriv F) r) r :=
    (hasDerivAt_id r).mul hF2.hasDerivAt
  have hg : HasDerivAt (fun t => t * deriv F t + F t - 1)
      ((1 * deriv F r + r * deriv (deriv F) r) + deriv F r) r := by
    have h := (hmul.add hF.hasDerivAt).sub_const 1
    simpa using h
  have hzero : HasDerivAt (fun _ : ℝ => (0 : ℝ))
      ((1 * deriv F r + r * deriv (deriv F) r) + deriv F r) r :=
    hg.congr_of_eventuallyEq hev.symm
  have huniq : (1 * deriv F r + r * deriv (deriv F) r) + deriv F r = 0 :=
    hzero.unique (hasDerivAt_const r 0)
  linarith [huniq]

end

end TGLExt
