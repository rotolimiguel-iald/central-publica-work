import TGLExt.SemifiniteSeed

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

/-!
# A PONTE DA DIMENSÃO: a camada abstrata dispara sobre o kernel concreto
  [TGLExt — v77, o incremento 2 do programa SemifiniteAnalysis]

O v64 tipou a camada abstrata (SemifiniteTraceData/BreuerGapData) e a
habitou no modelo-brinquedo ℝ≥0∞. O v76 provou os axiomas do peso no
traço matricial. Esta pedra constrói a PRIMEIRA INSTÂNCIA GENUÍNA da
camada abstrata — o reticulado REAL de subespaços de ℝⁿ com τ = dimensão
— e faz o teorema abstrato de Breuer DISPARAR pela primeira vez sobre o
kernel de um operador CONCRETO.

O QUE ESTA PEDRA PROVA [KERNEL]:

* `dimTraceData` — τ = dim no reticulado de subespaços: FIEL
  (dim S = 0 ⟹ S = ⊥) e MONÓTONO (S ≤ T ⟹ dim S ≤ dim T) — os campos
  da camada v64 habitados por um reticulado de verdade;
* ★ `dimension_trace_bot` / `dimension_trace_top_finite` — τ(⊥) = 0 e
  τ(⊤) < ∞ (em dimensão finita, o traço total é finito — a semifinitude
  é a finitude);
* ★★ `concrete_kernel_weight_via_abstract_layer` — **A PONTE DISPARA**:
  o pacote de gap (ker = ker(H₀−V), gap = ⊤) instancia BreuerGapData na
  camada da dimensão, e o teorema ABSTRATO `breuer_kernel_weight` (v64)
  conclui 0 < dim ker < ∞ para o operador CONCRETO;
* ★★ `concrete_kernel_full_profile` — O PERFIL COMPLETO DO CANTO
  CONCRETO (v64 × v65 × v77 numa só implicação): com H₀ positivo-definido
  e kernel não-trivial, o peso do canto é POSITIVO, FINITO e LIMITADO
  PELO POSTO DA INSCRIÇÃO (dim ker ≤ posto V).

HONESTIDADE: dimensão finita — o tijolo 2; o contínuo (subespaços
fechados de Hilbert ∞-dim, τ semifinito genuíno, afiliação) segue o
programa. β jamais literal. Sem sorry, sem axiom.
-/

namespace TGLExt

open scoped ENNReal
open Matrix

noncomputable section

variable {n : Type} [Fintype n] [DecidableEq n]

/-- [DATA — a 1ª instância GENUÍNA da camada v64] o reticulado REAL de
    subespaços de ℝⁿ com τ = dimensão: fiel e monótono. -/
def dimTraceData (n : Type) [Fintype n] :
    SemifiniteTraceData (Submodule ℝ (n → ℝ)) where
  tau := fun S => (Module.finrank ℝ S : ℝ≥0∞)
  mono := by
    intro p q hpq
    exact_mod_cast Submodule.finrank_mono hpq
  faithful := by
    intro p hp
    have h0 : Module.finrank ℝ p = 0 := by exact_mod_cast hp
    exact (Submodule.finrank_eq_zero (R := ℝ)).mp h0

/-- [KERNEL] ★ τ(⊥) = 0 — o vazio não pesa. -/
theorem dimension_trace_bot :
    (dimTraceData n).tau ⊥ = 0 := by
  simp [dimTraceData]

/-- [KERNEL] ★ τ(⊤) < ∞ — em dimensão finita o traço total é finito
    (a semifinitude é a finitude). -/
theorem dimension_trace_top_finite :
    (dimTraceData n).tau ⊤ < ⊤ := by
  simp only [dimTraceData]
  exact ENNReal.natCast_lt_top _

/-- [DATA] o pacote de gap CONCRETO: ker = ker(H₀−V) no reticulado da
    dimensão, gap = ⊤ (finito em dimensão finita). -/
def concreteKernelPackage (H0 V : Matrix n n ℝ)
    (hker : LinearMap.ker (H0 - V).mulVecLin ≠ ⊥) :
    BreuerGapData (Submodule ℝ (n → ℝ)) (dimTraceData n) where
  ker := LinearMap.ker (H0 - V).mulVecLin
  gap := ⊤
  ker_le_gap := le_top
  gap_finite := dimension_trace_top_finite
  ker_ne_bot := hker

/-- [KERNEL] ★★ A PONTE DISPARA: o teorema ABSTRATO de Breuer (v64)
    conclui, para o kernel do operador CONCRETO H₀ − V,
    0 < dim(ker) < ∞ — a camada abstrata e o operador real se tocam. -/
theorem concrete_kernel_weight_via_abstract_layer (H0 V : Matrix n n ℝ)
    (hker : LinearMap.ker (H0 - V).mulVecLin ≠ ⊥) :
    0 < (dimTraceData n).tau (LinearMap.ker (H0 - V).mulVecLin) ∧
      (dimTraceData n).tau (LinearMap.ker (H0 - V).mulVecLin) < ⊤ :=
  breuer_kernel_weight (concreteKernelPackage H0 V hker)

/-- [KERNEL] ★★ O PERFIL COMPLETO DO CANTO CONCRETO (v64 × v65 × v77):
    com H₀ positivo-definido e kernel não-trivial, o peso do canto é
    POSITIVO, FINITO e LIMITADO PELO POSTO DA INSCRIÇÃO — as três
    cláusulas do (B3) físico, numa só implicação, sobre o operador real. -/
theorem concrete_kernel_full_profile (H0 V : Matrix n n ℝ)
    (hpd : ∀ x : n → ℝ, x ≠ 0 → 0 < x ⬝ᵥ (H0 *ᵥ x))
    (hker : LinearMap.ker (H0 - V).mulVecLin ≠ ⊥) :
    (0 < (dimTraceData n).tau (LinearMap.ker (H0 - V).mulVecLin) ∧
      (dimTraceData n).tau (LinearMap.ker (H0 - V).mulVecLin) < ⊤) ∧
      Module.finrank ℝ (LinearMap.ker (H0 - V).mulVecLin) ≤
        Module.finrank ℝ (LinearMap.range V.mulVecLin) :=
  ⟨concrete_kernel_weight_via_abstract_layer H0 V hker,
    kernel_dim_le_rank_of_perturbation H0 V hpd⟩

end

end TGLExt
