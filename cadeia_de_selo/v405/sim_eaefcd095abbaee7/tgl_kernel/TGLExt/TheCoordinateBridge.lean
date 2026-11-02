import TGLExt.TheSchwarzschildUniqueness

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 800000

/-!
# A PONTE COORDENADA — o tensor de Einstein fala com as integrais primeiras
  [BANCADA — 25/08/2026 · o elo declarado da v208, agora provado]

## O que esta pedra fecha

A v208 provou `vácuo ⟺ classe de Schwarzschild` sobre os numeradores `(E_t, E_r)`, com a
ponte `G_μν → (E_t, E_r)` DECLARADA `[KNOWN]`. Aqui a ponte vira TEOREMA: nas componentes
MISTAS do tensor de Einstein da classe `ds² = A·dt² − B·dr² − r²dΩ²` [KNOWN, forma padrão
estática esférica — construída à mão, na MESMA estatura do `AnsatzEinstein` da casa]:

    G^t_t = 1/r² − 1/(B·r²) + B′/(r·B²)        G^r_r = 1/r² − 1/(B·r²) − A′/(r·A·B)

valem as REDUÇÕES EXATAS (álgebra de corpo, uma linha cada):

    G^t_t · (r²·B²)  =  E_t          G^r_r · (r²·A·B)  =  −E_r

## O que se prova

* ★★★ `einsteinTT_reduces` / `einsteinRR_reduces` — as duas identidades exatas;
* ★★★ `einstein_vacuum_iff_first_integral_equations` — `G^t_t = 0 ∧ G^r_r = 0 ⟺
  E_t = 0 ∧ E_r = 0` no domínio regular;
* ★★★ **`einstein_vacuum_implies_schwarzschild`** — a CADEIA COMPLETA: componentes de
  Einstein anulam num domínio convexo aberto ⟹ a classe de Schwarzschild emerge com o
  gauge `C` declarado — **o iff da v208 fala agora DIRETAMENTE com o tensor de Einstein**.

## ⚠ Delimitações

As fórmulas `G^t_t, G^r_r` são o resultado padrão [KNOWN] — aqui DEFINIDAS à mão (como o
`AnsatzEinstein` da casa) e amarradas por redução exata; a derivação
Christoffel→Riemann→Ricci DENTRO do kernel segue NOMEADA como o elo mais profundo. As
componentes angulares anulam pela primeira integral (`the_angular_component_is_free`,
v208). β jamais entra. Sem sorry, sem axiom. Nada aqui move o gate.
-/

namespace TGLExt

noncomputable section

/-- `G^t_t` da classe estática esférica [KNOWN, construída à mão]. -/
def einsteinTT (B : ℝ → ℝ) (r : ℝ) : ℝ :=
  1 / r ^ 2 - 1 / (B r * r ^ 2) + deriv B r / (r * B r ^ 2)

/-- `G^r_r` da classe estática esférica [KNOWN, construída à mão]. -/
def einsteinRR (A B : ℝ → ℝ) (r : ℝ) : ℝ :=
  1 / r ^ 2 - 1 / (B r * r ^ 2) - deriv A r / (r * A r * B r)

/-- ★★★ **A REDUÇÃO TEMPORAL É EXATA**: `G^t_t · (r²·B²) = E_t`. -/
theorem einsteinTT_reduces (B : ℝ → ℝ) (r : ℝ) (hr : r ≠ 0) (hB : B r ≠ 0) :
    einsteinTT B r * (r ^ 2 * B r ^ 2) = vacuumT B r := by
  unfold einsteinTT vacuumT
  field_simp
  ring

/-- ★★★ **A REDUÇÃO RADIAL É EXATA**: `G^r_r · (r²·A·B) = −E_r`. -/
theorem einsteinRR_reduces (A B : ℝ → ℝ) (r : ℝ) (hr : r ≠ 0)
    (hA : A r ≠ 0) (hB : B r ≠ 0) :
    einsteinRR A B r * (r ^ 2 * A r * B r) = -vacuumR A B r := by
  unfold einsteinRR vacuumR
  field_simp
  ring

/-- ★★★ **A PONTE**: no domínio regular, o vácuo de Einstein (componentes mistas) é
    EXATAMENTE o sistema das integrais primeiras. -/
theorem einstein_vacuum_iff_first_integral_equations (A B : ℝ → ℝ) (r : ℝ)
    (hr : r ≠ 0) (hA : A r ≠ 0) (hB : B r ≠ 0) :
    (einsteinTT B r = 0 ∧ einsteinRR A B r = 0)
      ↔ (vacuumT B r = 0 ∧ vacuumR A B r = 0) := by
  have hd1 : r ^ 2 * B r ^ 2 ≠ 0 :=
    mul_ne_zero (pow_ne_zero 2 hr) (pow_ne_zero 2 hB)
  have hd2 : r ^ 2 * A r * B r ≠ 0 :=
    mul_ne_zero (mul_ne_zero (pow_ne_zero 2 hr) hA) hB
  constructor
  · rintro ⟨h1, h2⟩
    constructor
    · have hred := einsteinTT_reduces B r hr hB
      rw [h1, zero_mul] at hred
      exact hred.symm
    · have hred := einsteinRR_reduces A B r hr hA hB
      rw [h2, zero_mul] at hred
      linarith [hred]
  · rintro ⟨h1, h2⟩
    constructor
    · have hred := einsteinTT_reduces B r hr hB
      rw [h1] at hred
      exact (mul_eq_zero.mp hred).resolve_right hd1
    · have hred := einsteinRR_reduces A B r hr hA hB
      rw [h2, neg_zero] at hred
      exact (mul_eq_zero.mp hred).resolve_right hd2

/-- ★★★ **A CADEIA COMPLETA**: Einstein-vácuo num domínio convexo aberto ⟹ a classe de
    Schwarzschild com o gauge `C` declarado. *O tensor de Einstein, a solda de duas
    funções e as integrais primeiras — um só teorema.* -/
theorem einstein_vacuum_implies_schwarzschild (A B : ℝ → ℝ) (s : Set ℝ)
    (hconv : Convex ℝ s) (hopen : IsOpen s)
    (hpos : ∀ r ∈ s, 0 < r) (hAne : ∀ r ∈ s, A r ≠ 0) (hBne : ∀ r ∈ s, B r ≠ 0)
    (hA : ∀ r ∈ s, DifferentiableAt ℝ A r) (hB : ∀ r ∈ s, DifferentiableAt ℝ B r)
    (hTT : ∀ r ∈ s, einsteinTT B r = 0) (hRR : ∀ r ∈ s, einsteinRR A B r = 0)
    (r₀ : ℝ) (hr₀ : r₀ ∈ s) :
    ∃ rs C : ℝ, ∀ r ∈ s,
      (B r)⁻¹ = 1 - rs / r ∧ A r = C * (1 - rs / r) := by
  apply vacuum_implies_schwarzschild_class A B s hconv hopen hpos hBne hA hB ?_ ?_ r₀ hr₀
  · intro r hr
    exact ((einstein_vacuum_iff_first_integral_equations A B r
      (ne_of_gt (hpos r hr)) (hAne r hr) (hBne r hr)).mp ⟨hTT r hr, hRR r hr⟩).1
  · intro r hr
    exact ((einstein_vacuum_iff_first_integral_equations A B r
      (ne_of_gt (hpos r hr)) (hAne r hr) (hBne r hr)).mp ⟨hTT r hr, hRR r hr⟩).2

end

end TGLExt
