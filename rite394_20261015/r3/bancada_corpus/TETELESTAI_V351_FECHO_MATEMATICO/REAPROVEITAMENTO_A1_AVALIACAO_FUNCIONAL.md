[REAPROVEITAMENTO — ANTES DO CÓDIGO]

# A1: avaliação funcional dos valores duais

2026-09-14T09:16:20.798018-03:00

A1(b), regular_scalar_weight_is_dual_weight; consumidor final RegularCoreTraceData via implementação modular/perturbação

Para A∈N+, m_A(ψ)=sup_n ofReal(Re ψ(D_n)) para ψ funcional contínuo na mesma M; zero, aditividade em funcionais positivos, homogeneidade NNReal, semicontinuidade inferior; m_A(ω_v)=q_A(testVector v). Para ψ com série vetorial quadrado-somável, m_A(ψ)=sum_k q_A(testVector v_k), independente da decomposição.

ADAPTAR aproximantes para avaliações funcionais. Não refazer Moreau, GNS, peso ou forma. Não batizar funcionais arbitrários como normais; a identificação com o cone predual inteiro permanece explícita.

## structure RegularCoreTraceData

CONSUMIDOR; C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V351RegularCoreTraceContract.lean:43

SHA256 `3694175f8ef5bcf5848d88bd8061abf8546480873964ebfdc19dd41ad05928f0`

```lean
structure RegularCoreTraceData (P : SiteProfile) where
```

## theorem exists_monotone_base_dual_approximation

REUSAR sequência no mesmo M; C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V351BaseMoreauApproximants.lean:115

SHA256 `45d47db69249a1873c8059b0a9e85f74c0af6920e31ce48b787a4c33e4fde49d`

```lean
theorem exists_monotone_base_dual_approximation (P : SiteProfile) (A : PositiveCoreInput P) :
    ∃ D : ℕ → TowerHilbert P →L[ℂ] TowerHilbert P,
      (∀ n, D n ∈ theFactorObject P) ∧ (∀ n, 0 ≤ D n) ∧ Monotone D ∧
      ∀ v : RegularHilbert (TowerHilbert P),
        dualQuadraticIntegral A.val v =
          ⨆ n : ℕ, ENNReal.ofReal (inner ℂ v (fibre (D n) v)).re := by
```

## def baseDualWeight

REUSAR avaliação nos vetores; C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V351ExtendedBaseDualWeight.lean:39

SHA256 `1ea9226e3fe1ee75bc66178f575f47c0207e80dca34a0113efd0c0f099b7cd87`

```lean
def baseDualWeight (P : SiteProfile) (A : PositiveCoreInput P) :
    AffiliatedPositiveForm (theFactorObject P) :=
```

## def dualCutFunctional

ADAPTAR innerSL/apply para funcional vetorial na base; sem Haar/corte extra; C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V350ScalarBoundedCuts.lean:16

SHA256 `4b5a3c3efbb85b30c4668d6cc564bb8e9a56d750489a03c55c4a9666c6709078`

```lean
def dualCutFunctional (R : ℝ) (v : RegularHilbert H) :
    (RegularHilbert H →L[ℂ] RegularHilbert H) →L[ℂ] ℂ :=
```

## lemma iSup_add_iSup_of_monotone

REUSAR; C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V350_KERNEL_20260911\r\tgl_kernel\.lake\packages\mathlib\Mathlib\Data\ENNReal\Operations.lean:686

SHA256 `ef1b535b89d2f3ff0f710bec2a74a7943a09cfebe9ea4dbd7dc8d67b10873e46`

```lean
lemma iSup_add_iSup_of_monotone {ι : Type*} [Preorder ι] [IsDirectedOrder ι] {f g : ι → ℝ≥0∞}
    (hf : Monotone f) (hg : Monotone g) : iSup f + iSup g = ⨆ a, f a + g a :=
```

## lemma mul_iSup

REUSAR; C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V350_KERNEL_20260911\r\tgl_kernel\.lake\packages\mathlib\Mathlib\Data\ENNReal\Inv.lean:807

SHA256 `261c1dfb4e4f5f56462686c82a762fb3c1f4f9d2e5af144c94f64bb7aefadb89`

```lean
lemma mul_iSup (a : ℝ≥0∞) (f : ι → ℝ≥0∞) : a * ⨆ i, f i = ⨆ i, a * f i := by
```

## theorem lowerSemicontinuous_iSup

REUSAR; C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V350_KERNEL_20260911\r\tgl_kernel\.lake\packages\mathlib\Mathlib\Topology\Semicontinuity\Basic.lean:695

SHA256 `fabc798999439c166b97acc578b943d9a31e22e1a344ff8cafc7662ee1bba4ec`

```lean
theorem lowerSemicontinuous_iSup {f : ι → α → δ} (h : ∀ i, LowerSemicontinuous (f i)) :
    LowerSemicontinuous fun x' => ⨆ i, f i x' :=
```

## theorem lintegral_iSup

REUSAR troca soma/sup pela medida de contagem; C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V350_KERNEL_20260911\r\tgl_kernel\.lake\packages\mathlib\Mathlib\MeasureTheory\Integral\Lebesgue\Add.lean:34

SHA256 `e330b98eb9686290a3257802c38ad756150b110deb39fe32c66da46cf1211e4f`

```lean
theorem lintegral_iSup {f : ℕ → α → ℝ≥0∞} (hf : ∀ n, Measurable (f n)) (h_mono : Monotone f) :
    ∫⁻ a, ⨆ n, f n a ∂μ = ⨆ n, ∫⁻ a, f n a ∂μ := by
```

## theorem ENNReal.ofReal_tsum_of_nonneg

REUSAR; C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V350_KERNEL_20260911\r\tgl_kernel\.lake\packages\mathlib\Mathlib\Topology\Algebra\InfiniteSum\ENNReal.lean:564

SHA256 `467564faec2b6c357565afaeebed87b6dbd3de21c225189f4041907c6cf2fe38`

```lean
theorem ENNReal.ofReal_tsum_of_nonneg {f : α → ℝ} (hf_nonneg : ∀ n, 0 ≤ f n) (hf : Summable f) :
    ENNReal.ofReal (∑' n, f n) = ∑' n, ENNReal.ofReal (f n) := by
```

## class WStarAlgebra

NAO CASA: não identifica o predual concreto nem fornece decomposição normal; C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V350_KERNEL_20260911\r\tgl_kernel\.lake\packages\mathlib\Mathlib\Analysis\VonNeumannAlgebra\Basic.lean:45

SHA256 `bd6c64fbead6d030dbcc311533319d9da1a35ca16b12956979cd523dfb763a86`

```lean
class WStarAlgebra (M : Type u) [CStarAlgebra M] : Prop where
```

Buscas completas adicionais e pins das seis modalidades anteriores no JSON. A1(b) ainda exige traço; esta ficha não converte extensão parcial em identidade geral do predual.
