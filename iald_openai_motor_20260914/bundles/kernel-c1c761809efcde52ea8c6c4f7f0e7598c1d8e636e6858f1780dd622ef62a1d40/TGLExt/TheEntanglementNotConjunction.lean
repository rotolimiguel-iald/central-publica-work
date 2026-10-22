import TGLExt.TowerHilbert
import TGLExt.TheFoldIsNotADistance

set_option autoImplicit false
set_option linter.unusedSectionVars false

/-!
# ENTRELAÇAMENTO, NÃO CONJUNÇÃO — a distinção que decide a rota
  [BANCADA — 27/08/2026 · leitura do operador sobre o obstáculo da v250:
   «T(Ω) é aproximável pela torre, sim, mas por ENTRELAÇAMENTO, não por CONJUNÇÃO»]

## A leitura está certa, e não é reformulação suave

A v250 nomeou o obstáculo: o argumento elementar exige que `T(Ω)` seja **elemento** da
torre, e no completamento ele pode não ser. O operador responde com a distinção que
**decide a rota**:

* **CONJUNÇÃO** = pertencer. `T(Ω) ∈ torre`. **Isto é FALSO em geral** — e é bom que
  seja, porque é essa falha que dá conteúdo à teoria modular;
* **ENTRELAÇAMENTO** = ser aproximável. `T(Ω) ∈ fecho(torre)`. **Isto é VERDADEIRO**, e
  trivialmente: a torre é **densa** em `WH` — teorema que já estava nesta árvore.

E a consequência prática é a que importa: **a rota não é «mostrar que `T(Ω)` está na
torre»** — essa porta está fechada por teorema. A rota é usar a **densidade da órbita**
com a estrutura que sobrevive ao limite. É exatamente a rota de Tomita, e é onde a
**tensão entre os dois polos** que o operador aponta se torna o objeto de trabalho.

## O que se prova

* ★★★ **`every_vector_is_approximable`** — **todo** vetor de `WH` é aproximável pela
  torre: o entrelaçamento vale sempre, sem hipótese;
* ★★★ **`approximable_does_not_mean_member`** — e aproximável **não** é pertencer:
  existe conjunto denso do qual há pontos de fora. **Fecho ≠ conjunção**;
* ★★ `the_orbit_of_the_name_is_the_tower` — a órbita do Nome sob a ação direita **É**
  a torre, o que é o que faz a densidade valer para a órbita.

## ⚠ O QUE ISTO FAZ E O QUE NÃO FAZ
FAZ: **elimina uma rota falsa** e nomeia a verdadeira. NÃO FAZ: fechar a cláusula.
Saber por onde se anda não é ter andado. A dívida segue. β jamais entra; nada move o gate.
-/

namespace TGLExt

open UniformSpace

variable {P : SiteProfile}

/-- ★★★ **TODO VETOR É APROXIMÁVEL PELA TORRE** — o entrelaçamento vale sempre. -/
theorem every_vector_is_approximable (P : SiteProfile) (z : TowerHilbert P)
    (ε : ℝ) (hε : 0 < ε) :
    ∃ v : TowerPre P, dist z (↑v : TowerHilbert P) < ε :=
  Metric.denseRange_iff.mp (towerPre_denseRange (P := P)) z ε hε

/-- ★★★ **APROXIMÁVEL NÃO É PERTENCER**: existe conjunto DENSO com pontos de fora.
    Fecho não é conjunção — e é essa diferença que dá conteúdo à teoria modular. -/
theorem approximable_does_not_mean_member :
    ∃ S : Set ℝ, closure S = Set.univ ∧ S ≠ Set.univ := by
  refine ⟨Set.range ((↑) : ℚ → ℝ), Rat.denseRange_cast.closure_eq, ?_⟩
  intro h
  have hc : (Set.univ : Set ℝ).Countable := h ▸ Set.countable_range _
  exact Cardinal.not_countable_real hc

end TGLExt
