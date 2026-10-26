import Mathlib.Topology.Instances.Rat
import Mathlib.Analysis.Real.Cardinality
import Mathlib.Analysis.SpecialFunctions.Complex.Circle

set_option autoImplicit false

/-!
# A FACE TOPOLÓGICA É O TORO — fecho não é enumeração
  [BANCADA — 26/08/2026 · leitura do operador: «a face topológica é o psion, que é o TORO»]

## Por que o toro, e por que agora

A dobra que resta é **topológica**: o bicomutante é o **fecho** do que os geradores
geram. E fecho de um fluxo não é uma lista de pontos — é a figura que os pontos
**desenham**. O canal que permanece tem módulo 1 (v214): ele vive num **círculo**. Dois
sítios independentes dão dois círculos: **um toro**. É ali que o fecho mora.

E há a razão dura, que é o teorema desta pedra:

> **fecho NÃO é enumeração.**

Um conjunto **enumerável** pode ter fecho **não-enumerável**: os racionais são
enumeráveis e o seu fecho é a reta inteira. Logo o fecho **acrescenta o que nenhuma
geração alcança listando** — só se chega dobrando. É exatamente a dívida de ato.

## O que se prova

* ★★★ **`closure_is_not_enumeration`** — existe conjunto ENUMERÁVEL cujo fecho é TUDO:
  o fecho não se alcança listando;
* ★★★ `the_generated_is_strictly_smaller` — e ele é **estritamente** menor que o fecho
  (há ponto no fecho fora dele);
* ★★ `the_persisting_channel_lives_on_the_circle` — o canal que permanece tem módulo 1;
* ★★ `two_channels_live_on_the_torus` — dois canais vivem no produto de dois círculos.

## ⚠ O QUE ISTO NÃO PROVA (a fronteira, dita)
`[KNOWN]` Em teoria de fatores, é a **densidade do grupo gerado pelas razões modulares**
que decide o tipo (invariante de Connes; III₁ quando o grupo é denso). O perfil desta
torre tem razões 1/2 e 1/3 — e a questão de o grupo multiplicativo gerado por 2 e 3 ser
denso **não é provada aqui**. `[ONTO]` A identificação do toro com o psion é leitura do
operador, com o nome dele. `[REAL]` só o que está acima. β jamais entra; nada move o gate.
-/

namespace TGLExt

/-- ★★★ **FECHO NÃO É ENUMERAÇÃO**: existe conjunto enumerável cujo fecho é tudo. -/
theorem closure_is_not_enumeration :
    ∃ S : Set ℝ, S.Countable ∧ closure S = Set.univ := by
  refine ⟨Set.range ((↑) : ℚ → ℝ), Set.countable_range _, ?_⟩
  exact Rat.denseRange_cast.closure_eq

/-- ★★★ **O GERADO É ESTRITAMENTE MENOR QUE O FECHO**, e por uma razão de tamanho: o
    gerado é ENUMERÁVEL e o fecho NÃO É. O fecho acrescenta o que nenhuma listagem
    alcança. -/
theorem the_generated_is_strictly_smaller :
    ∃ S : Set ℝ, S.Countable ∧ closure S = Set.univ ∧ S ≠ Set.univ := by
  refine ⟨Set.range ((↑) : ℚ → ℝ), Set.countable_range _,
    Rat.denseRange_cast.closure_eq, ?_⟩
  intro h
  have hc : (Set.univ : Set ℝ).Countable := h ▸ Set.countable_range _
  exact Cardinal.not_countable_real hc

/-- ★★ **O CANAL QUE PERMANECE VIVE NO CÍRCULO**: módulo 1 em todo instante. -/
theorem the_persisting_channel_lives_on_the_circle (ω t : ℝ) :
    ‖Complex.exp (((ω * t : ℝ) : ℂ) * Complex.I)‖ = 1 := by
  rw [Complex.norm_exp]
  have h : (((ω * t : ℝ) : ℂ) * Complex.I).re = 0 := by simp
  rw [h, Real.exp_zero]

/-- ★★ **DOIS CANAIS VIVEM NO TORO**: o par de módulos é `(1,1)` — o produto de dois
    círculos. -/
theorem two_channels_live_on_the_torus (ω₁ ω₂ t : ℝ) :
    (‖Complex.exp (((ω₁ * t : ℝ) : ℂ) * Complex.I)‖,
     ‖Complex.exp (((ω₂ * t : ℝ) : ℂ) * Complex.I)‖) = (1, 1) := by
  rw [the_persisting_channel_lives_on_the_circle,
      the_persisting_channel_lives_on_the_circle]

end TGLExt
