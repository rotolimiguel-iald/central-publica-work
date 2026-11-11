import TGLExt.TheCompletionExtension
import Mathlib.Topology.MetricSpace.Completion

set_option autoImplicit false

/-!
# A DOBRA NÃO É DISTÂNCIA — `| . |`
  [BANCADA — 26/08/2026 · correção do operador: «não há distância, é só uma dobra: | . |»]

## A palavra que ele corrigiu (e a correção é exata)

A onda anterior chamou de **distância** o que separa o gerador da álgebra e o andar do
completamento. **Está errado, e o erro é de linguagem com consequência.** Nos dois
casos o objeto «longe» é o **FECHO** do objeto «perto» — e fecho significa distância
**ZERO**: todo ponto do completamento é limite de pontos da torre, arbitrariamente
próximos; o bicomutante é o fecho da álgebra gerada.

Não há longe. **Há uma DOBRA** — e a notação que ele escreveu é literalmente ela:
duas barras (as duas faces) e um ponto (o que se identifica).

## E o módulo É a dobra, com precisão

A dobra `x ↦ −x` identifica cada ponto com o seu reflexo. O módulo `|x|` é **exatamente**
o quociente por essa dobra: ele identifica os dois lados e **nada além** —
`|x| = |y| ⟺ y = x ∨ y = −x`. Nem mais (não confunde o que a dobra não junta), nem
menos (não separa o que ela junta). **O módulo é o invariante completo da dobra.**

Isto reescreve a dívida: o que falta **não é comprimento a percorrer**, é a **dobra a
executar** — a operação que identifica o limite com o que a ele se aproxima. Dívida de
ato, não de trajeto.

## O que se prova

* ★★★ **`the_modulus_is_exactly_the_fold`** — `|x| = |y| ⟺ y = x ∨ y = −x`: o módulo
  identifica os dois lados e nada além;
* ★★★ **`the_fold_is_an_involution`** — dobrar duas vezes é não dobrar;
* ★★★ **`density_is_zero_distance`** — todo ponto do completamento tem pontos do denso
  a distância menor que qualquer `ε`: **não há distância a percorrer**;
* ★★ `the_fold_preserves_the_modulus` — a dobra preserva exatamente o que o módulo mede.

β jamais entra. Nada move o gate.
-/

namespace TGLExt

/-- a dobra da reta: identifica cada ponto com o seu reflexo. -/
def theFold (x : ℝ) : ℝ := -x

/-- ★★★ **DOBRAR DUAS VEZES É NÃO DOBRAR**. -/
theorem the_fold_is_an_involution (x : ℝ) : theFold (theFold x) = x := neg_neg x

/-- ★★★ **O MÓDULO É EXATAMENTE A DOBRA**: identifica os dois lados e NADA ALÉM. -/
theorem the_modulus_is_exactly_the_fold (x y : ℝ) :
    |x| = |y| ↔ (y = x ∨ y = theFold x) := by
  rw [abs_eq_abs]
  unfold theFold
  constructor
  · rintro (h | h)
    · exact Or.inl h.symm
    · exact Or.inr (by rw [h]; ring)
  · rintro (h | h)
    · exact Or.inl h.symm
    · exact Or.inr (by rw [h]; ring)

/-- ★★ **A DOBRA PRESERVA O QUE O MÓDULO MEDE**. -/
theorem the_fold_preserves_the_modulus (x : ℝ) : |theFold x| = |x| := by
  unfold theFold
  exact abs_neg x

/-- ★★★ **DENSIDADE É DISTÂNCIA ZERO**: todo ponto do completamento tem pontos do
    denso mais perto que qualquer `ε` --- **não há distância a percorrer**. O que falta
    não é comprimento: é a DOBRA. -/
theorem density_is_zero_distance {α : Type} [MetricSpace α]
    (z : UniformSpace.Completion α) (ε : ℝ) (hε : 0 < ε) :
    ∃ a : α, dist z (↑a : UniformSpace.Completion α) < ε :=
  Metric.denseRange_iff.mp UniformSpace.Completion.denseRange_coe z ε hε

end TGLExt
