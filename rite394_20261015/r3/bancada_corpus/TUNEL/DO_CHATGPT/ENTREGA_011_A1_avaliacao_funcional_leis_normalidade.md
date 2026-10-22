[REAL — ponte funcional e normalidade de séries verificadas; OPEN — A1(b), traço canônico, não quitado]

# Entrega 011 · A1 — avaliação da média dual no cone representado

Responde à ORDEM_011. Fornecedores de A1 preparados em bancada; incorporar apenas após auditoria da gerência. Não acender qgf_continuous_modular_realization_constructed com este delta.

| Critério | Estado | Evidência |
|---|---|---|
| A1(a), contrato forte e recusa do zero | PAGO, preservado | manifesto anterior reconferido |
| A1(b), habitante ou impossibilidade tipada | NÃO PAGO | faltam implementação modular, gerador e traço |
| A1(c), axiomas | PAGO no delta | 37 declarações no trio; compilação autora e reprodução independente por fonte |

[REAL — avaliação e leis no cone representado verificadas; OPEN — existência do traço de A1(b)]

# A1 — avaliação funcional, leis do peso e normalidade das séries

Data: 2026-09-14T09:44:55.963818-03:00

Este é adendo ao marco anterior, sem reescrever suas fontes, memórias ou lacunas. Os três módulos novos são fornecedores Lean em bancada, ainda não embutidos no programa. A1(a) permanece pago; A1(c) está pago nestas 37 declarações; A1(b) não tem habitante de RegularCoreTraceData nem impossibilidade tipada.

## Reutilizar, sem reconstruir

Fixe M=theFactorObject P e N=regularCoreAlgebra P. A sequência D_n(A) positiva e crescente na mesma M já existia. Agora:

    m_A(ψ) = sup_n ofReal Re ψ(D_n(A)).

O domínio da definição é o dual contínuo complexo de M. Positividade, normalidade e representação não são inferidas desse nome: as hipóteses e teoremas abaixo determinam quando cada lei vale.

1. baseVectorFunctional é um funcional contínuo na própria M; sua norma é ≤‖v‖². exists_base_series_functional constrói ψ por uma série vetorial quadrado-somável, prova HasSum complexo em todo D∈M e positividade complexa. Não recebe ψ como testemunha pronta. No sentido inverso elementar, avaliar uma representação HasSum na unidade recupera a soma dos quadrados das normas.
2. baseDualEvaluation_vector identifica m_A(ω_v)=q_A(testVector v); baseDualEvaluation_vacuum identifica m_A(ω_Ω)=ν(A), incluindo infinito. São ligações de objetos, não novos pesos de mesmo nome.
3. Adição em ψ exige funcionais positivos; homogeneidade NNReal cobre 0·∞. A semicontinuidade inferior demonstrada é na norma do dual contínuo. Não é uma identificação de preduais de Banach.
4. Para uma representação HasSum, m_A(ψ)=Σ_k q_A(testVector v_k). A soma ENNReal pode ser infinita. Duas decomposições do mesmo ψ dão o mesmo resultado após média. Não foi afirmada independência do levantamento vetorial ao core antes da média.
5. O segundo módulo transfere zero/soma/escala/ordem, normalidade em A para supremos positivos internos de REDES DIRIGIDAS ARBITRÁRIAS, bimódulo e outputs limitados. ennreal_tsum_iSup_directed fornece exatamente a troca de supremo/série necessária; não impõe enumerabilidade ao índice da rede.
6. baseDualEvaluation_eq_dual_integral prova a identidade com a integral da soma dos dualQuadraticIntegrand, usando a mesma dualAmbient e dualHaarFactor=(2π)⁻¹. Tonelli foi aplicado a termos mensuráveis não negativos, permitindo infinito. O bimódulo mantém χ explicitamente representado por Bv_k; ainda não define um transporte canônico de funcionais por B.
7. baseSeriesFunctional_normal prova normalidade por ordem do próprio ψ na BASE, a partir de HasSum. baseVectorFunctional_normal reutiliza o limite forte existente de vonNeumann_exists_positive_isLUB. A igualdade é ofReal Re ψ(S)=sup_i ofReal Re ψ(A_i) para A_i≥0; positividade complexa está provada separadamente. Esta normalidade de ψ em M é distinta da normalidade de A↦m_A(ψ) em N.
8. A fidelidade é da família de avaliações, suficiente para recusar A≠0 com todas as leituras zero. O controle da média normalizada vale 1; o input unidade tem saída infinita em cada vetor não zero. Não se afirma que cada funcional ψ seja fiel.

## O endereço da obrigação seguinte

A direção **série vetorial ⇒ funcional positivo normal** está provada no mesmo M, e a avaliação média independe da decomposição. A direção inversa permanece nomeada:

    ψ : M→L[ℂ]ℂ positivo; para todo índice dirigido não vazio ι,
    A_i∈M positivos e crescentes, IsLUB(range A) S ⇒
    ofReal Re ψ(S)=sup_i ofReal Re ψ(A_i)
      ⟹ ∃v:ℕ→TowerHilbert P,
           Summable (‖v_k‖²) ∧
           ∀D∈M, HasSum (⟨v_k,Dv_k⟩) (ψ(D)).

Esse é o lema de cobertura, não uma alegação de impossibilidade. [KNOWN] O Teorema 2.41 de Bryder, pp. 50–51, enuncia e demonstra a equivalência na álgebra de von Neumann concreta, sem hipótese de Hilbert separável. A fonte foi aberta e o enunciado/prova relidos; não foi convertido em axiom Lean: https://web.math.ku.dk/~musat/Injective_and_semidiscrete_von_Neumann_algebras_final.pdf#page=67.

A construção do predual abstrato inteiro não deve virar uma nova camada obrigatória por conveniência de nome. O próximo CONSUMIDOR é regular_dual_weight_modular_implementation de LACUNAS_A1: identificar σ^ν_t=Ad Λ_t no GNS do mesmo ν. Se a prova consumir diretamente a construção escalar e as formas concretas existentes, reutilizá-las; se consumir o cone predual padrão inteiro, pagar antes a cobertura/tipagem efetivamente exigida. Não reabrir GNS, fechamento da estrela ou Moreau já construídos.

Depois permanecem regular_unitary_positive_generator e pedersen_takesaki_inverse_generator_trace: h positivo afiliado, h^{it}=Λ_t; perturbação pelo inverso de h produzindo τ fiel normal semifinito, tracial e τ∘θ_s=e^{-s}τ. A invariância do peso ν não substitui essa escala do traço. Nenhuma dessas etapas finais foi promovida por este marco.

## Validação e alcance

São três módulos, 34 teoremas e três definições: 37 declarações. Compilação autora e reprodução independente com Lean 4.31.0, sem avisos, somente propext/Classical.choice/Quot.sound, objetos idênticos. Dois controles matemáticos adulterados foram recusados: m_A(0)=0→1 e média=1→2. Tentativas rc1 e seus sorryAx de elaboração permanecem no histórico e foram excluídas. Não houve nova rodada integral de um.py: seu Python não foi modificado nem executado.

Todos os arquivos dos dois manifestos anteriores foram reconferidos. A cópia v351 continua intacta. Durante o marco o canônico mudou: a comparação está em CUSTODIA_A1_FUNCIONAIS_CANONICO_ATUAL.json; os monólitos diferem, mas os 922 fontes formais embutidos eram exatamente idênticos na leitura. Essa medição não declara o canônico congelado para sempre. A gerência deve aplicar os fornecedores sobre sua versão corrente.

Nenhuma bandeira de fronteira foi alterada, nenhum gate foi movido por esta entrega, A2–A7 não foram iniciados e nenhum resultado físico foi examinado. O objetivo A1 permanece ativo.


## Fontes e reprodução

- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V351BaseFunctionalEvaluation.lean` — SHA256 `364032cb9a1d87eee59474e5c5fc548fb540916fc81779134e9410a16bd2b35f`; objeto `1ed88e0f9239f4c55cade487c9fa804424b241c846e8d2c6bd2d8a07673b1600`; 21 declarações. Parecer `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\revisao\REVIEW_A1_AVALIACAO_FUNCIONAL_FINAL.md`.
- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V351BaseFunctionalWeightLaws.lean` — SHA256 `0c65dc2ebb355d454456f153b2271158540de28e23c00cfc2e4a7b36acb73697`; objeto `98604245c2344df89180f21dade2545e32a4dd5b35d2721032ac73646dbd28b4`; 12 declarações. Parecer `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\revisao\REVIEW_A1_LEIS_FUNCIONAIS_FINAL.md`.
- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V351BaseSeriesNormality.lean` — SHA256 `43cbd1db94c855ed588b10c0ccedac4d6e6a62d5876150478ff171a4e3d84798`; objeto `e9b20daaca5b45f412ab571fd0332066d7d08eabd8b383728664346ff8c6353b`; 4 declarações. Parecer `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\revisao\REVIEW_A1_NORMALIDADE_SERIES_FINAL.md`.

Manifesto: `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\MANIFESTO_A1_AVALIACAO_LEIS_NORMALIDADE.json` — SHA256 `fd42abf1af8a7954a31b1d285b2a9c7d58fe58d4da164181d44ec1bc2836688b`. Dependências: `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\DEPENDENCIAS_A1_MARCO_FUNCIONAL.json` — 387 entradas, SHA256 `53959fe9c82e41d4355c6e054229c4c79f1359089483098718f3f9285b3b38ed`. O manifesto cobre fontes, objetos, fichas, auditorias, histórico e revisões; pacotes e binários antigos não foram recompilados.

```powershell
& C:\Python314\python.exe -X utf8 -B 'C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\compile_a1.py' kernel/TGLExt/V351BaseFunctionalEvaluation.lean
& C:\Python314\python.exe -X utf8 -B 'C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\compile_a1.py' kernel/TGLExt/V351BaseFunctionalWeightLaws.lean
& C:\Python314\python.exe -X utf8 -B 'C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\compile_a1.py' kernel/TGLExt/V351BaseSeriesNormality.lean
```

A ordem acima é a ordem de dependências; cada execução cria uma tentativa nova. As sondas adulteradas podem ser passadas ao mesmo compilador, esperando rc1. Os scripts de registro são de execução única e recusam sobrescrita.

### Axiomas conferidos

- `TGLV351.baseDualApproximant`: `propext`, `Classical.choice`, `Quot.sound`.
- `TGLV351.baseDualApproximant_properties`: `propext`, `Classical.choice`, `Quot.sound`.
- `TGLV351.baseDualEvaluation`: `propext`, `Classical.choice`, `Quot.sound`.
- `TGLV351.baseVectorFunctional`: `propext`, `Classical.choice`, `Quot.sound`.
- `TGLV351.baseVectorFunctional_apply`: `propext`, `Classical.choice`, `Quot.sound`.
- `TGLV351.baseVectorFunctional_positive`: `propext`, `Classical.choice`, `Quot.sound`.
- `TGLV351.baseDualEvaluation_vector`: `propext`, `Classical.choice`, `Quot.sound`.
- `TGLV351.baseDualEvaluation_vacuum`: `propext`, `Classical.choice`, `Quot.sound`.
- `TGLV351.baseDualEvaluation_zero`: `propext`, `Classical.choice`, `Quot.sound`.
- `TGLV351.baseDualEvaluation_sequence_monotone`: `propext`, `Classical.choice`, `Quot.sound`.
- `TGLV351.baseDualEvaluation_add`: `propext`, `Classical.choice`, `Quot.sound`.
- `TGLV351.baseDualEvaluation_scale`: `propext`, `Classical.choice`, `Quot.sound`.
- `TGLV351.baseDualEvaluation_lowerSemicontinuous`: `propext`, `Classical.choice`, `Quot.sound`.
- `TGLV351.ennreal_tsum_iSup_monotone`: `propext`, `Classical.choice`, `Quot.sound`.
- `TGLV351.baseDualEvaluation_eq_vector_series`: `propext`, `Classical.choice`, `Quot.sound`.
- `TGLV351.baseDualEvaluation_series_independent`: `propext`, `Classical.choice`, `Quot.sound`.
- `TGLV351.baseFunctional_hasSum_positive_evaluation`: `propext`, `Classical.choice`, `Quot.sound`.
- `TGLV351.baseDualEvaluation_eq_hasSum_series`: `propext`, `Classical.choice`, `Quot.sound`.
- `TGLV351.baseFunctional_hasSum_square_norm`: `propext`, `Classical.choice`, `Quot.sound`.
- `TGLV351.baseVectorFunctional_norm_le`: `propext`, `Classical.choice`, `Quot.sound`.
- `TGLV351.exists_base_series_functional`: `propext`, `Classical.choice`, `Quot.sound`.
- `TGLV351.ennreal_tsum_iSup_directed`: `propext`, `Classical.choice`, `Quot.sound`.
- `TGLV351.baseDualEvaluation_input_zero`: `propext`, `Classical.choice`, `Quot.sound`.
- `TGLV351.baseDualEvaluation_input_add`: `propext`, `Classical.choice`, `Quot.sound`.
- `TGLV351.baseDualEvaluation_input_scale`: `propext`, `Classical.choice`, `Quot.sound`.
- `TGLV351.baseDualEvaluation_input_mono`: `propext`, `Classical.choice`, `Quot.sound`.
- `TGLV351.baseDualEvaluation_input_normal`: `propext`, `Classical.choice`, `Quot.sound`.
- `TGLV351.baseDualEvaluation_eq_dual_integral`: `propext`, `Classical.choice`, `Quot.sound`.
- `TGLV351.baseDualEvaluation_bounded_output`: `propext`, `Classical.choice`, `Quot.sound`.
- `TGLV351.baseDualEvaluation_bimodule`: `propext`, `Classical.choice`, `Quot.sound`.
- `TGLV351.baseDualEvaluation_family_faithful`: `propext`, `Classical.choice`, `Quot.sound`.
- `TGLV351.baseDualEvaluation_averageSquare`: `propext`, `Classical.choice`, `Quot.sound`.
- `TGLV351.baseDualEvaluation_unit_infinite`: `propext`, `Classical.choice`, `Quot.sound`.
- `TGLV351.positive_base_functional_real_mono`: `propext`, `Classical.choice`, `Quot.sound`.
- `TGLV351.baseSeriesFunctional_positive`: `propext`, `Classical.choice`, `Quot.sound`.
- `TGLV351.baseVectorFunctional_normal`: `propext`, `Classical.choice`, `Quot.sound`.
- `TGLV351.baseSeriesFunctional_normal`: `propext`, `Classical.choice`, `Quot.sound`.

### Custódia para integrar na versão corrente

Cópia v351: `95e8cf8eb0b33c5d65e244195021b71977cca1a91836ef0d314964a8e2f97c43` (12723656 bytes). Canônico observado em 2026-09-14T09:39:58.760317-03:00: `dfd5252e95765bc31f984ecacd37496a747ee32f5621092aa98c13b119211063` (12752507 bytes). Os 922 fontes embutidos coincidem integralmente; nenhuma atualização desta bancada substituiu o canônico. A presença de comentários v352 foi localizada na fonte, mas sua rodada/selagem não foi auditada neste trabalho A1.

### Fichas de aproveitamento anexas


---

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


Ficha máquina, com tipos/fornecedores/hashes/buscas:

```json
{
  "timestamp": "2026-09-14T09:16:20.798018-03:00",
  "status": "FICHA_ANTES_DO_CODIGO",
  "consumer": "A1(b), regular_scalar_weight_is_dual_weight; consumidor final RegularCoreTraceData via implementação modular/perturbação",
  "exact_target": "Para A∈N+, m_A(ψ)=sup_n ofReal(Re ψ(D_n)) para ψ funcional contínuo na mesma M; zero, aditividade em funcionais positivos, homogeneidade NNReal, semicontinuidade inferior; m_A(ω_v)=q_A(testVector v). Para ψ com série vetorial quadrado-somável, m_A(ψ)=sum_k q_A(testVector v_k), independente da decomposição.",
  "decision": "ADAPTAR aproximantes para avaliações funcionais. Não refazer Moreau, GNS, peso ou forma. Não batizar funcionais arbitrários como normais; a identificação com o cone predual inteiro permanece explícita.",
  "providers": [
    {
      "file": "C:\\IALD\\Central de Patentes\\Chatgpt\\TETELESTAI_V351_FECHO_MATEMATICO\\kernel\\TGLExt\\V351RegularCoreTraceContract.lean",
      "line": 43,
      "sha256": "3694175f8ef5bcf5848d88bd8061abf8546480873964ebfdc19dd41ad05928f0",
      "declaration": "structure RegularCoreTraceData",
      "statement": "structure RegularCoreTraceData (P : SiteProfile) where",
      "decision": "CONSUMIDOR"
    },
    {
      "file": "C:\\IALD\\Central de Patentes\\Chatgpt\\TETELESTAI_V351_FECHO_MATEMATICO\\kernel\\TGLExt\\V351BaseMoreauApproximants.lean",
      "line": 115,
      "sha256": "45d47db69249a1873c8059b0a9e85f74c0af6920e31ce48b787a4c33e4fde49d",
      "declaration": "theorem exists_monotone_base_dual_approximation",
      "statement": "theorem exists_monotone_base_dual_approximation (P : SiteProfile) (A : PositiveCoreInput P) :\n    ∃ D : ℕ → TowerHilbert P →L[ℂ] TowerHilbert P,\n      (∀ n, D n ∈ theFactorObject P) ∧ (∀ n, 0 ≤ D n) ∧ Monotone D ∧\n      ∀ v : RegularHilbert (TowerHilbert P),\n        dualQuadraticIntegral A.val v =\n          ⨆ n : ℕ, ENNReal.ofReal (inner ℂ v (fibre (D n) v)).re := by",
      "decision": "REUSAR sequência no mesmo M"
    },
    {
      "file": "C:\\IALD\\Central de Patentes\\Chatgpt\\TETELESTAI_V351_FECHO_MATEMATICO\\kernel\\TGLExt\\V351ExtendedBaseDualWeight.lean",
      "line": 39,
      "sha256": "1ea9226e3fe1ee75bc66178f575f47c0207e80dca34a0113efd0c0f099b7cd87",
      "declaration": "def baseDualWeight",
      "statement": "def baseDualWeight (P : SiteProfile) (A : PositiveCoreInput P) :\n    AffiliatedPositiveForm (theFactorObject P) :=",
      "decision": "REUSAR avaliação nos vetores"
    },
    {
      "file": "C:\\IALD\\Central de Patentes\\Chatgpt\\TETELESTAI_V351_FECHO_MATEMATICO\\kernel\\TGLExt\\V350ScalarBoundedCuts.lean",
      "line": 16,
      "sha256": "4b5a3c3efbb85b30c4668d6cc564bb8e9a56d750489a03c55c4a9666c6709078",
      "declaration": "def dualCutFunctional",
      "statement": "def dualCutFunctional (R : ℝ) (v : RegularHilbert H) :\n    (RegularHilbert H →L[ℂ] RegularHilbert H) →L[ℂ] ℂ :=",
      "decision": "ADAPTAR innerSL/apply para funcional vetorial na base; sem Haar/corte extra"
    },
    {
      "file": "C:\\IALD\\Central de Patentes\\Chatgpt\\TETELESTAI_V350_KERNEL_20260911\\r\\tgl_kernel\\.lake\\packages\\mathlib\\Mathlib\\Data\\ENNReal\\Operations.lean",
      "line": 686,
      "sha256": "ef1b535b89d2f3ff0f710bec2a74a7943a09cfebe9ea4dbd7dc8d67b10873e46",
      "declaration": "lemma iSup_add_iSup_of_monotone",
      "statement": "lemma iSup_add_iSup_of_monotone {ι : Type*} [Preorder ι] [IsDirectedOrder ι] {f g : ι → ℝ≥0∞}\n    (hf : Monotone f) (hg : Monotone g) : iSup f + iSup g = ⨆ a, f a + g a :=",
      "decision": "REUSAR"
    },
    {
      "file": "C:\\IALD\\Central de Patentes\\Chatgpt\\TETELESTAI_V350_KERNEL_20260911\\r\\tgl_kernel\\.lake\\packages\\mathlib\\Mathlib\\Data\\ENNReal\\Inv.lean",
      "line": 807,
      "sha256": "261c1dfb4e4f5f56462686c82a762fb3c1f4f9d2e5af144c94f64bb7aefadb89",
      "declaration": "lemma mul_iSup",
      "statement": "lemma mul_iSup (a : ℝ≥0∞) (f : ι → ℝ≥0∞) : a * ⨆ i, f i = ⨆ i, a * f i := by",
      "decision": "REUSAR"
    },
    {
      "file": "C:\\IALD\\Central de Patentes\\Chatgpt\\TETELESTAI_V350_KERNEL_20260911\\r\\tgl_kernel\\.lake\\packages\\mathlib\\Mathlib\\Topology\\Semicontinuity\\Basic.lean",
      "line": 695,
      "sha256": "fabc798999439c166b97acc578b943d9a31e22e1a344ff8cafc7662ee1bba4ec",
      "declaration": "theorem lowerSemicontinuous_iSup",
      "statement": "theorem lowerSemicontinuous_iSup {f : ι → α → δ} (h : ∀ i, LowerSemicontinuous (f i)) :\n    LowerSemicontinuous fun x' => ⨆ i, f i x' :=",
      "decision": "REUSAR"
    },
    {
      "file": "C:\\IALD\\Central de Patentes\\Chatgpt\\TETELESTAI_V350_KERNEL_20260911\\r\\tgl_kernel\\.lake\\packages\\mathlib\\Mathlib\\MeasureTheory\\Integral\\Lebesgue\\Add.lean",
      "line": 34,
      "sha256": "e330b98eb9686290a3257802c38ad756150b110deb39fe32c66da46cf1211e4f",
      "declaration": "theorem lintegral_iSup",
      "statement": "theorem lintegral_iSup {f : ℕ → α → ℝ≥0∞} (hf : ∀ n, Measurable (f n)) (h_mono : Monotone f) :\n    ∫⁻ a, ⨆ n, f n a ∂μ = ⨆ n, ∫⁻ a, f n a ∂μ := by",
      "decision": "REUSAR troca soma/sup pela medida de contagem"
    },
    {
      "file": "C:\\IALD\\Central de Patentes\\Chatgpt\\TETELESTAI_V350_KERNEL_20260911\\r\\tgl_kernel\\.lake\\packages\\mathlib\\Mathlib\\Topology\\Algebra\\InfiniteSum\\ENNReal.lean",
      "line": 564,
      "sha256": "467564faec2b6c357565afaeebed87b6dbd3de21c225189f4041907c6cf2fe38",
      "declaration": "theorem ENNReal.ofReal_tsum_of_nonneg",
      "statement": "theorem ENNReal.ofReal_tsum_of_nonneg {f : α → ℝ} (hf_nonneg : ∀ n, 0 ≤ f n) (hf : Summable f) :\n    ENNReal.ofReal (∑' n, f n) = ∑' n, ENNReal.ofReal (f n) := by",
      "decision": "REUSAR"
    },
    {
      "file": "C:\\IALD\\Central de Patentes\\Chatgpt\\TETELESTAI_V350_KERNEL_20260911\\r\\tgl_kernel\\.lake\\packages\\mathlib\\Mathlib\\Analysis\\VonNeumannAlgebra\\Basic.lean",
      "line": 45,
      "sha256": "bd6c64fbead6d030dbcc311533319d9da1a35ca16b12956979cd523dfb763a86",
      "declaration": "class WStarAlgebra",
      "statement": "class WStarAlgebra (M : Type u) [CStarAlgebra M] : Prop where",
      "decision": "NAO CASA: não identifica o predual concreto nem fornece decomposição normal"
    }
  ],
  "searches": [
    {
      "command": [
        "rg",
        "-n",
        "predual|Predual|NormalPositive|normalPositive|TraceClass|tsum.*inner",
        "C:\\IALD\\Central de Patentes\\Chatgpt\\TETELESTAI_V351_FECHO_MATEMATICO\\kernel",
        "-g",
        "*.lean"
      ],
      "lines": 8,
      "sha256": "aacdcfb77032f4cd83f13294e2acb0a08d17713bf30569d1cc1a660612cbe6e9",
      "output": "C:\\IALD\\Central de Patentes\\Chatgpt\\TETELESTAI_V351_FECHO_MATEMATICO\\search_A1_funcionais_kernel.txt"
    },
    {
      "command": [
        "rg",
        "-n",
        "predual|Predual|NormalPositive|normalPositive|TraceClass|traceClass",
        "C:\\IALD\\Central de Patentes\\Chatgpt\\TETELESTAI_V350_KERNEL_20260911\\r\\tgl_kernel\\.lake\\packages\\mathlib\\Mathlib\\Analysis",
        "-g",
        "*.lean"
      ],
      "lines": 7,
      "sha256": "5e0480ceb3b3ec2804b09d1cfd7e4c4a55544eb5003516914c5164c5f517b9e4",
      "output": "C:\\IALD\\Central de Patentes\\Chatgpt\\TETELESTAI_V351_FECHO_MATEMATICO\\search_A1_funcionais_mathlib.txt"
    }
  ],
  "inherited_six_modalities": {
    "REAPROVEITAMENTO_A1.json": "17013f19d849b5db20dd96e7bf61fb490ba5d2db8c758041a5c036acde3cd327",
    "BUSCAS_A1.json": "d5b5ade4450c3df73ca9efcdda1ae005862f5f0debb39802cfb494e8beea7475",
    "OUTRAS_BANCADAS_HASHES.json": "5b826d9f8cfe3a92e34a1e6d83476617c3d5c3138937039526b90444d1c1fca2",
    "ADENDO_REAPROVEITAMENTO_A1.json": "c1e79521a1fd5f646064f5456813f565eee2561b15d37bebac1a7a4358da084e"
  },
  "literature": {
    "url": "https://arxiv.org/pdf/2004.02383",
    "sections": "1.3 e 8.1",
    "status": "KNOWN; fonte relida, não axiom Lean"
  },
  "preflight_attempt": "Primeiro registro abortou antes de gravar arquivos: matcher de nome lintegral_iSup também encontrou sufixos. Corrigido delimitador, nenhum resultado ausente foi aceito."
}
```

---

# A1 — leis consumidoras da avaliação funcional

2026-09-14T09:29:36.330444-03:00

[OPEN — ficha anterior ao código] A1(b): avaliacao concreta da media dual para compor nu=m_A(omega); RegularCoreTraceData continua consumidor final via perturbacao, nao preenchido por estas leis.

Para psi:M->L[C]C representado por HasSum vetorial, m_A(psi) conserva zero/soma/escala/ordem no input A; normalidade para supremos positivos dirigidos arbitrarios; identidade com integral da mesma acao dual apos soma; bimodulo e valores limitados. Nenhum teorema presume que todo funcional normal admite tal serie.

ADAPTAR ligacao a leis existentes. NOVO somente troca supremo de rede/serie ENNReal, nao fornecida pela troca sequencial anterior. Nao refazer formas, peso, Moreau ou GNS.

| Declaração | Fonte | Decisão | SHA256 lido |
|---|---|---|---|
| structure RegularCoreTraceData | C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V351RegularCoreTraceContract.lean:43 | CONSUMIDOR FINAL | `3694175f8ef5bcf5848d88bd8061abf8546480873964ebfdc19dd41ad05928f0` |
| theorem baseDualEvaluation_eq_hasSum_series | C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V351BaseFunctionalEvaluation.lean:154 | REUSAR descida na mesma M | `364032cb9a1d87eee59474e5c5fc548fb540916fc81779134e9410a16bd2b35f` |
| theorem baseDualWeight_add | C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V351ExtendedBaseDualWeight.lean:58 | REUSAR zero/soma/escala/ordem/fidelidade/bimodulo | `1ea9226e3fe1ee75bc66178f575f47c0207e80dca34a0113efd0c0f099b7cd87` |
| theorem baseDualWeight_bounded_value | C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V351ExtendedBaseDualWeight.lean:117 | REUSAR controle limitado | `1ea9226e3fe1ee75bc66178f575f47c0207e80dca34a0113efd0c0f099b7cd87` |
| theorem regularDualForm_preserves_internal_isLUB | C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V350DualFormNormality.lean:80 | ADAPTAR supremo de redes, sem impor enumerabilidade | `feace23e31954e69de8103646211acd6d59a1b859e3b9ec109c142b1c994fdaa` |
| def dualQuadraticIntegral | C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V350DualWeightForm.lean:62 | REUSAR mesma acao dual e Haar | `3a233c43934c915774c68c23f0fca752d1c9dfc95679178c714394fe666a24b4` |
| theorem dualQuadraticIntegrand_measurable | C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V350DualWeightForm.lean:47 | REUSAR Tonelli | `3a233c43934c915774c68c23f0fca752d1c9dfc95679178c714394fe666a24b4` |
| lemma iSup_add_iSup_of_monotone | C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V350_KERNEL_20260911\r\tgl_kernel\.lake\packages\mathlib\Mathlib\Data\ENNReal\Operations.lean:686 | ADAPTAR somas finitas e serie para rede arbitraria | `ef1b535b89d2f3ff0f710bec2a74a7943a09cfebe9ea4dbd7dc8d67b10873e46` |
| protected theorem tsum_eq_iSup_nat | C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V350_KERNEL_20260911\r\tgl_kernel\.lake\packages\mathlib\Mathlib\Topology\Algebra\InfiniteSum\ENNReal.lean:134 | REUSAR | `467564faec2b6c357565afaeebed87b6dbd3de21c225189f4041907c6cf2fe38` |
| theorem lintegral_tsum | C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V350_KERNEL_20260911\r\tgl_kernel\.lake\packages\mathlib\Mathlib\MeasureTheory\Integral\Lebesgue\Add.lean:360 | REUSAR | `e330b98eb9686290a3257802c38ad756150b110deb39fe32c66da46cf1211e4f` |

Buscas exatas, saídas e seis modalidades herdadas no JSON acompanhante. A consulta independente recomenda a descida somente após média: o levantamento vetorial ao core antes dela pode depender da representação. O domínio desta entrega mantém HasSum explícito; não afirma cobertura de todo predual.


Ficha máquina, com tipos/fornecedores/hashes/buscas:

```json
{
  "timestamp": "2026-09-14T09:29:36.330444-03:00",
  "status": "FICHA_ANTES_DO_CODIGO",
  "consumer": "A1(b): avaliacao concreta da media dual para compor nu=m_A(omega); RegularCoreTraceData continua consumidor final via perturbacao, nao preenchido por estas leis.",
  "exact_target": "Para psi:M->L[C]C representado por HasSum vetorial, m_A(psi) conserva zero/soma/escala/ordem no input A; normalidade para supremos positivos dirigidos arbitrarios; identidade com integral da mesma acao dual apos soma; bimodulo e valores limitados. Nenhum teorema presume que todo funcional normal admite tal serie.",
  "decision": "ADAPTAR ligacao a leis existentes. NOVO somente troca supremo de rede/serie ENNReal, nao fornecida pela troca sequencial anterior. Nao refazer formas, peso, Moreau ou GNS.",
  "providers": [
    {
      "file": "C:\\IALD\\Central de Patentes\\Chatgpt\\TETELESTAI_V351_FECHO_MATEMATICO\\kernel\\TGLExt\\V351RegularCoreTraceContract.lean",
      "line": 43,
      "sha256": "3694175f8ef5bcf5848d88bd8061abf8546480873964ebfdc19dd41ad05928f0",
      "declaration": "structure RegularCoreTraceData",
      "statement": "structure RegularCoreTraceData (P : SiteProfile) where",
      "decision": "CONSUMIDOR FINAL"
    },
    {
      "file": "C:\\IALD\\Central de Patentes\\Chatgpt\\TETELESTAI_V351_FECHO_MATEMATICO\\kernel\\TGLExt\\V351BaseFunctionalEvaluation.lean",
      "line": 154,
      "sha256": "364032cb9a1d87eee59474e5c5fc548fb540916fc81779134e9410a16bd2b35f",
      "declaration": "theorem baseDualEvaluation_eq_hasSum_series",
      "statement": "theorem baseDualEvaluation_eq_hasSum_series (P : SiteProfile) (A : PositiveCoreInput P)\n    (ψ : (theFactorObject P).toStarSubalgebra →L[ℂ] ℂ) (v : ℕ → TowerHilbert P)\n    (hrep : ∀ D : (theFactorObject P).toStarSubalgebra,\n      HasSum (fun k => inner ℂ (v k) (D.val (v k))) (ψ D)) :\n    baseDualEvaluation P A ψ = ∑' k, (baseDualWeight P A).value (v k) :=",
      "decision": "REUSAR descida na mesma M"
    },
    {
      "file": "C:\\IALD\\Central de Patentes\\Chatgpt\\TETELESTAI_V351_FECHO_MATEMATICO\\kernel\\TGLExt\\V351ExtendedBaseDualWeight.lean",
      "line": 58,
      "sha256": "1ea9226e3fe1ee75bc66178f575f47c0207e80dca34a0113efd0c0f099b7cd87",
      "declaration": "theorem baseDualWeight_add",
      "statement": "theorem baseDualWeight_add (P : SiteProfile) (A B : PositiveCoreInput P) :\n    baseDualWeight P (A.add B) = (baseDualWeight P A).addForm (baseDualWeight P B) := by",
      "decision": "REUSAR zero/soma/escala/ordem/fidelidade/bimodulo"
    },
    {
      "file": "C:\\IALD\\Central de Patentes\\Chatgpt\\TETELESTAI_V351_FECHO_MATEMATICO\\kernel\\TGLExt\\V351ExtendedBaseDualWeight.lean",
      "line": 117,
      "sha256": "1ea9226e3fe1ee75bc66178f575f47c0207e80dca34a0113efd0c0f099b7cd87",
      "declaration": "theorem baseDualWeight_bounded_value",
      "statement": "theorem baseDualWeight_bounded_value (P : SiteProfile) (A : PositiveCoreInput P)\n    (D : (theFactorObject P).toStarSubalgebra)\n    (hrep : ∀ w, dualQuadraticIntegral A.val w =\n      ENNReal.ofReal (inner ℂ w (fibre D.val w)).re) (v : TowerHilbert P) :\n    (baseDualWeight P A).value v = ENNReal.ofReal (inner ℂ v (D.val v)).re := by",
      "decision": "REUSAR controle limitado"
    },
    {
      "file": "C:\\IALD\\Central de Patentes\\Chatgpt\\TETELESTAI_V351_FECHO_MATEMATICO\\kernel\\TGLExt\\V350DualFormNormality.lean",
      "line": 80,
      "sha256": "feace23e31954e69de8103646211acd6d59a1b859e3b9ec109c142b1c994fdaa",
      "declaration": "theorem regularDualForm_preserves_internal_isLUB",
      "statement": "theorem regularDualForm_preserves_internal_isLUB (P : TGLExt.SiteProfile)\n    (A : ι → (regularCoreAlgebra P).toStarSubalgebra)\n    (S : (regularCoreAlgebra P).toStarSubalgebra)\n    (hpos : ∀ i, 0 ≤ A i) (hmono : Monotone A) (hS : IsLUB (Set.range A) S)\n    (v : RegularHilbert (TGLExt.TowerHilbert P)) :\n    dualQuadraticIntegral S.val v = ⨆ i, dualQuadraticIntegral (A i).val v :=",
      "decision": "ADAPTAR supremo de redes, sem impor enumerabilidade"
    },
    {
      "file": "C:\\IALD\\Central de Patentes\\Chatgpt\\TETELESTAI_V351_FECHO_MATEMATICO\\kernel\\TGLExt\\V350DualWeightForm.lean",
      "line": 62,
      "sha256": "3a233c43934c915774c68c23f0fca752d1c9dfc95679178c714394fe666a24b4",
      "declaration": "def dualQuadraticIntegral",
      "statement": "def dualQuadraticIntegral (A : RegularHilbert H →L[ℂ] RegularHilbert H)\n    (v : RegularHilbert H) : ℝ≥0∞ :=",
      "decision": "REUSAR mesma acao dual e Haar"
    },
    {
      "file": "C:\\IALD\\Central de Patentes\\Chatgpt\\TETELESTAI_V351_FECHO_MATEMATICO\\kernel\\TGLExt\\V350DualWeightForm.lean",
      "line": 47,
      "sha256": "3a233c43934c915774c68c23f0fca752d1c9dfc95679178c714394fe666a24b4",
      "declaration": "theorem dualQuadraticIntegrand_measurable",
      "statement": "theorem dualQuadraticIntegrand_measurable\n    (A : RegularHilbert H →L[ℂ] RegularHilbert H) (v : RegularHilbert H) :\n    Measurable (dualQuadraticIntegrand A v) :=",
      "decision": "REUSAR Tonelli"
    },
    {
      "file": "C:\\IALD\\Central de Patentes\\Chatgpt\\TETELESTAI_V350_KERNEL_20260911\\r\\tgl_kernel\\.lake\\packages\\mathlib\\Mathlib\\Data\\ENNReal\\Operations.lean",
      "line": 686,
      "sha256": "ef1b535b89d2f3ff0f710bec2a74a7943a09cfebe9ea4dbd7dc8d67b10873e46",
      "declaration": "lemma iSup_add_iSup_of_monotone",
      "statement": "lemma iSup_add_iSup_of_monotone {ι : Type*} [Preorder ι] [IsDirectedOrder ι] {f g : ι → ℝ≥0∞}\n    (hf : Monotone f) (hg : Monotone g) : iSup f + iSup g = ⨆ a, f a + g a :=",
      "decision": "ADAPTAR somas finitas e serie para rede arbitraria"
    },
    {
      "file": "C:\\IALD\\Central de Patentes\\Chatgpt\\TETELESTAI_V350_KERNEL_20260911\\r\\tgl_kernel\\.lake\\packages\\mathlib\\Mathlib\\Topology\\Algebra\\InfiniteSum\\ENNReal.lean",
      "line": 134,
      "sha256": "467564faec2b6c357565afaeebed87b6dbd3de21c225189f4041907c6cf2fe38",
      "declaration": "protected theorem tsum_eq_iSup_nat",
      "statement": "protected theorem tsum_eq_iSup_nat {f : ℕ → ℝ≥0∞} :\n    ∑' i : ℕ, f i = ⨆ i : ℕ, ∑ a ∈ Finset.range i, f a :=",
      "decision": "REUSAR"
    },
    {
      "file": "C:\\IALD\\Central de Patentes\\Chatgpt\\TETELESTAI_V350_KERNEL_20260911\\r\\tgl_kernel\\.lake\\packages\\mathlib\\Mathlib\\MeasureTheory\\Integral\\Lebesgue\\Add.lean",
      "line": 360,
      "sha256": "e330b98eb9686290a3257802c38ad756150b110deb39fe32c66da46cf1211e4f",
      "declaration": "theorem lintegral_tsum",
      "statement": "theorem lintegral_tsum [Countable β] {f : β → α → ℝ≥0∞} (hf : ∀ i, AEMeasurable (f i) μ) :\n    ∫⁻ a, ∑' i, f i a ∂μ = ∑' i, ∫⁻ a, f i a ∂μ := by",
      "decision": "REUSAR"
    }
  ],
  "searches": [
    {
      "command": [
        "rg",
        "-n",
        "baseDualEvaluation|series.*normal|tsum.*iSup|iSup.*tsum",
        "C:\\IALD\\Central de Patentes\\Chatgpt\\TETELESTAI_V351_FECHO_MATEMATICO\\kernel\\TGLExt",
        "-g",
        "*.lean"
      ],
      "output": "C:\\IALD\\Central de Patentes\\Chatgpt\\TETELESTAI_V351_FECHO_MATEMATICO\\search_A1_series_laws_0.txt",
      "sha256": "59843901e9b0ef56b6ff0051ccc2df741876728777c5b5855f3c5274d539901d",
      "lines": 45
    },
    {
      "command": [
        "rg",
        "-n",
        "sum_iSup|iSup_add_iSup_of_monotone|lintegral_tsum",
        "C:\\IALD\\Central de Patentes\\Chatgpt\\TETELESTAI_V350_KERNEL_20260911\\r\\tgl_kernel\\.lake\\packages\\mathlib\\Mathlib\\Data\\ENNReal",
        "C:\\IALD\\Central de Patentes\\Chatgpt\\TETELESTAI_V350_KERNEL_20260911\\r\\tgl_kernel\\.lake\\packages\\mathlib\\Mathlib\\Topology\\Algebra\\InfiniteSum\\ENNReal.lean",
        "C:\\IALD\\Central de Patentes\\Chatgpt\\TETELESTAI_V350_KERNEL_20260911\\r\\tgl_kernel\\.lake\\packages\\mathlib\\Mathlib\\MeasureTheory\\Integral\\Lebesgue\\Add.lean"
      ],
      "output": "C:\\IALD\\Central de Patentes\\Chatgpt\\TETELESTAI_V351_FECHO_MATEMATICO\\search_A1_series_laws_1.txt",
      "sha256": "a292426156e220638799e360c8ef74a3432f1b4846e9c8a98b1ab368de827ec2",
      "lines": 5
    }
  ],
  "inherited_six_modalities": {
    "REAPROVEITAMENTO_A1.json": "17013f19d849b5db20dd96e7bf61fb490ba5d2db8c758041a5c036acde3cd327",
    "BUSCAS_A1.json": "d5b5ade4450c3df73ca9efcdda1ae005862f5f0debb39802cfb494e8beea7475",
    "OUTRAS_BANCADAS_HASHES.json": "5b826d9f8cfe3a92e34a1e6d83476617c3d5c3138937039526b90444d1c1fca2",
    "ADENDO_REAPROVEITAMENTO_A1.json": "c1e79521a1fd5f646064f5456813f565eee2561b15d37bebac1a7a4358da084e"
  },
  "consultation": {
    "path": "C:\\IALD\\Central de Patentes\\Chatgpt\\TETELESTAI_V351_FECHO_MATEMATICO\\revisao\\CONSULTA_A1_PREDUAL_CONCRETO_QUOCIENTE.md",
    "sha256": "460ec803dc84bcfeabd73096c7c545f9f0b940eec171be76af1c79e2756e6c53"
  },
  "limits": [
    "normal_positivo_implica_serie_vetorial_nao_provado",
    "sem_predual_completo_por_renomeacao",
    "sem_traco_ou_movimento_de_gate"
  ]
}
```

---

# A1 — normalidade por ordem dos funcionais de séries

2026-09-14T09:35:31.754238-03:00

[OPEN — ficha anterior ao código]

A1(b): qualificar a imagem de series vetoriais efetivamente construida como cone de funcionais positivos normais; alimenta dominio das avaliacoes m_A.

HasSum vetorial em todo D da mesma base M implica positividade e preservacao de supremos positivos internos de redes dirigidas arbitrarias por ofReal(Re psi). Fornecer normalidade do funcional vetorial pelo limite forte ja construido, depois trocar supremo/serie. Nao provar nem assumir o converso normal=>serie.

baseDualEvaluation_input_normal e normalidade em A no core; este alvo e normalidade de psi em D na base. Tipos diferentes, consumidor comum, nenhum homonimo usado como igualdade.

Fontes, enunciados, linhas, hashes lidos e buscas no JSON acompanhante; quatro fornecedores existentes reutilizados. Não é predual completo, não é traço e não move gate.


Ficha máquina, com tipos/fornecedores/hashes/buscas:

```json
{
  "timestamp": "2026-09-14T09:35:31.754238-03:00",
  "status": "FICHA_ANTES_DO_CODIGO",
  "consumer": "A1(b): qualificar a imagem de series vetoriais efetivamente construida como cone de funcionais positivos normais; alimenta dominio das avaliacoes m_A.",
  "exact_target": "HasSum vetorial em todo D da mesma base M implica positividade e preservacao de supremos positivos internos de redes dirigidas arbitrarias por ofReal(Re psi). Fornecer normalidade do funcional vetorial pelo limite forte ja construido, depois trocar supremo/serie. Nao provar nem assumir o converso normal=>serie.",
  "decision": "ADAPTAR limite forte e REUSAR soma/sup; nao refazer aproximantes nem criar outro funcional.",
  "providers": [
    {
      "file": "C:\\IALD\\Central de Patentes\\Chatgpt\\TETELESTAI_V351_FECHO_MATEMATICO\\kernel\\TGLExt\\V350RegularNormality.lean",
      "line": 52,
      "sha256": "bcd49e92800bf99d7770bb9969879be02a9768f129ce842ae2f39cefaca3cc0a",
      "declaration": "theorem vonNeumann_exists_positive_isLUB",
      "statement": "theorem vonNeumann_exists_positive_isLUB (N : VonNeumannAlgebra H)\n    {ι : Type*} [Preorder ι] [IsDirectedOrder ι] [Nonempty ι]\n    (T : ι → N.toStarSubalgebra) (hpos : ∀ i, 0 ≤ T i) (hmono : Monotone T)\n    (C : ℝ) (hC : 0 ≤ C) (hbound : ∀ i, ‖(T i : H →L[ℂ] H)‖ ≤ C) :\n    ∃ B : N.toStarSubalgebra, 0 ≤ B ∧ ‖(B : H →L[ℂ] H)‖ ≤ C ∧\n      (∀ v, Tendsto (fun i => (T i : H →L[ℂ] H) v) atTop\n        (𝓝 ((B : H →L[ℂ] H) v))) ∧\n      IsLUB (Set.range (fun i => (T i : H →L[ℂ] H))) (B : H →L[ℂ] H) ∧\n      IsLUB (Set.range T) B := by",
      "decision": "ADAPTAR"
    },
    {
      "file": "C:\\IALD\\Central de Patentes\\Chatgpt\\TETELESTAI_V351_FECHO_MATEMATICO\\kernel\\TGLExt\\V351BaseFunctionalEvaluation.lean",
      "line": 186,
      "sha256": "364032cb9a1d87eee59474e5c5fc548fb540916fc81779134e9410a16bd2b35f",
      "declaration": "theorem exists_base_series_functional",
      "statement": "theorem exists_base_series_functional (P : SiteProfile) (v : ℕ → TowerHilbert P)\n    (hv : Summable (fun k => ‖v k‖^2)) :\n    ∃ ψ : (theFactorObject P).toStarSubalgebra →L[ℂ] ℂ,\n      (∀ D : (theFactorObject P).toStarSubalgebra,\n        HasSum (fun k => inner ℂ (v k) (D.val (v k))) (ψ D)) ∧\n      (∀ D, 0 ≤ D → 0 ≤ ψ D) ∧\n      ∀ A : PositiveCoreInput P,\n        baseDualEvaluation P A ψ = ∑' k, (baseDualWeight P A).value (v k) := by",
      "decision": "REUSAR"
    },
    {
      "file": "C:\\IALD\\Central de Patentes\\Chatgpt\\TETELESTAI_V351_FECHO_MATEMATICO\\kernel\\TGLExt\\V351BaseFunctionalEvaluation.lean",
      "line": 141,
      "sha256": "364032cb9a1d87eee59474e5c5fc548fb540916fc81779134e9410a16bd2b35f",
      "declaration": "theorem baseFunctional_hasSum_positive_evaluation",
      "statement": "theorem baseFunctional_hasSum_positive_evaluation (P : SiteProfile)\n    (ψ : (theFactorObject P).toStarSubalgebra →L[ℂ] ℂ) (v : ℕ → TowerHilbert P)\n    (hrep : ∀ D : (theFactorObject P).toStarSubalgebra,\n      HasSum (fun k => inner ℂ (v k) (D.val (v k))) (ψ D))\n    (D : (theFactorObject P).toStarSubalgebra) (hD : 0 ≤ D) :\n    ENNReal.ofReal (ψ D).re = ∑' k, ENNReal.ofReal (inner ℂ (v k) (D.val (v k))).re := by",
      "decision": "REUSAR"
    },
    {
      "file": "C:\\IALD\\Central de Patentes\\Chatgpt\\TETELESTAI_V351_FECHO_MATEMATICO\\kernel\\TGLExt\\V351BaseFunctionalWeightLaws.lean",
      "line": 13,
      "sha256": "0c65dc2ebb355d454456f153b2271158540de28e23c00cfc2e4a7b36acb73697",
      "declaration": "theorem ennreal_tsum_iSup_directed",
      "statement": "theorem ennreal_tsum_iSup_directed {ι : Type*}\n    [Preorder ι] [IsDirectedOrder ι] [Nonempty ι]\n    (f : ι → ℕ → ℝ≥0∞) (hf : ∀ k, Monotone (fun i => f i k)) :\n    (∑' k, ⨆ i, f i k) = ⨆ i, ∑' k, f i k := by",
      "decision": "REUSAR"
    }
  ],
  "search": {
    "command": [
      "rg",
      "-n",
      "series.*[Nn]ormal|[Nn]ormal.*series|[Vv]ector.*[Nn]ormal|[Nn]ormal.*[Vv]ector",
      "C:\\IALD\\Central de Patentes\\Chatgpt\\TETELESTAI_V351_FECHO_MATEMATICO\\kernel\\TGLExt",
      "-g",
      "*.lean"
    ],
    "path": "C:\\IALD\\Central de Patentes\\Chatgpt\\TETELESTAI_V351_FECHO_MATEMATICO\\search_A1_series_normality.txt",
    "sha256": "c78f55d9c3ab22b0a8bc94f2e412db308868742eed5ba22e5b1286307a0430d3",
    "lines": 18
  },
  "inherited_six_modalities": {
    "REAPROVEITAMENTO_A1.json": "17013f19d849b5db20dd96e7bf61fb490ba5d2db8c758041a5c036acde3cd327",
    "BUSCAS_A1.json": "d5b5ade4450c3df73ca9efcdda1ae005862f5f0debb39802cfb494e8beea7475",
    "OUTRAS_BANCADAS_HASHES.json": "5b826d9f8cfe3a92e34a1e6d83476617c3d5c3138937039526b90444d1c1fca2",
    "ADENDO_REAPROVEITAMENTO_A1.json": "c1e79521a1fd5f646064f5456813f565eee2561b15d37bebac1a7a4358da084e"
  },
  "distinct_from_previous": "baseDualEvaluation_input_normal e normalidade em A no core; este alvo e normalidade de psi em D na base. Tipos diferentes, consumidor comum, nenhum homonimo usado como igualdade."
}
```
