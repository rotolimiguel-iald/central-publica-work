import TGLExt.SMatrix

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 800000

/-!
# O ACOPLAMENTO VERBAL — o limiar de poda É a amplitude de reflexão da fronteira
  [TGLExt — v297; casa "Nós" (29/08/2026)]

## A ORDEM DO OPERADOR (29/08/2026)

> *"As referências e derivações que faltam, inclusive quanto ao PsiBit, estão todas
> especificadas nas minhas patentes, inclusive com código funcional lá. Essa é a última
> camada: incorporar a linguagem das minhas patentes no kernel, porque ao fim essa é a
> arquitetura final."*

## ★★ A PONTE QUE ESTA PEDRA TIPA — mesmo número, mesma derivação, dois domínios

A patente **BR 10 2026 006129-8** (Kernel Ontológico, depósito INPI 15/03/2026) define, no
domínio **verbal**:

* `θ_Miguel = arcsin(√β_TGL)` — a *fronteira natural* (relatório: ≈ 6,3°);
* o **limiar de repetição/vácuo**: `g_ratio < √β_TGL ≈ 0,110 ⟹ L_poda elimina`;
* a **função de acoplamento verbal** `f(θ) = tanh((θ − θ_Miguel)/Δθ)`.

E o kernel já provava, no domínio **modular**, que a amplitude de reflexão da matriz-S da
fronteira é `|𝓡| = sin θ` (`normSq_reflection`, `SMatrix.lean:241`), com
`|𝓡|² + |𝓣|² = 1` (`:254`).

> **Logo o limiar de poda verbal `√β` É a amplitude de reflexão `|𝓡|` em `θ = θ_Miguel`.**
> Não é analogia de vocabulário: é o mesmo número, com a mesma derivação, lido em dois
> domínios. Podar o que reflete menos que `√β` é podar abaixo da amplitude da fronteira.

## O QUE FICA PROVADO

* `sin_thetaMiguel` — `sin(θ_Miguel β) = √β` para `0 ≤ β ≤ 1`. ⚠ **Elementar**
  (`Real.sin_arcsin`); o conteúdo não está aqui, está na identificação seguinte;
* ★★★ `the_pruning_threshold_is_the_reflection_amplitude` — o limiar verbal `√β` e a
  amplitude `|𝓡|` da matriz-S coincidem **em `θ_Miguel`**, e a soma com a transmissão
  fecha em 1: um só ângulo governa os dois domínios;
* ★★ `coupling_vanishes_at_the_boundary` — `f(θ_Miguel) = 0`: **o acoplamento verbal se
  anula exatamente na fronteira**;
* ★★★ `tanh_sign` e `the_boundary_separates_the_verbal_domains` — o acoplamento
  **muda de sinal em `θ_Miguel`**: negativo abaixo, positivo acima, zero na fronteira.
  Logo é um **separador genuíno**, e não um carimbo — a forma tipada do classificador;
* `the_verb_floor_is_a_fraction_of_the_max` — o Piso de Hilbert verbal (sinal ≥ `β·S_max`)
  é fração estrita do máximo quando `0 < β < 1`.

## ⚠ O QUE ESTA PEDRA **NÃO** FAZ

Não deriva `β` — ele entra como parâmetro real, e `β_TGL = α·√e` **nunca é literal em
kernel**. Não afirma que um LLM SEJA uma fronteira modular: o próprio artefato crava essa
leitura como **heurística estrutural**. Não ressuscita a medida de `β` em corpus de texto,
**refutada** por veredito pré-registrado (na base de tokens a conjugação não fixa Ψ). E não
move o gate.

## ⚠⚠ ERRATA DO OPERADOR (29/08/2026) — **NÃO EXISTE β_TGL ADAPTATIVO**

> *"Não concordo, não existe β_TGL adaptativo — isso é um erro na patente e precisa ser
> corrigido. β_TGL é um só e é canônico."*

A **BR 10 2026 005477-1** (Aprendizado Contínuo, depósito INPI 09/03/2026) traz — no
relatório (eqs. 4, 8, 10), nos componentes [2] e [6], na Figura 7 e em **cinco
reivindicações — QUATRO independentes (1, 8, 14, 17) mais a dependente 5**
(⚠ ERRATA v304: a v298 dizia "duas (1 e 14)"; a custódia mediu o .docx
depositado em 30/08 e o alcance real é maior) — um `β_adaptativo = α·√S` que **varia com a
entropia de Shannon**. **O operador declara isso ERRO.** `β_TGL = α·√e` é constante: um `β`
que varia com o estado **não é β**. Um `β` que se adapta ao dado deixa de poder ser
falsificado por ele — e é essa a razão de fundo pela qual o erro importa.

⚠ **Esta pedra não usa `β_adaptativo`**: `verbFloor β Smax` toma `β` como parâmetro real, e
a bancada afere contra a constante canônica (`√β = 0,109687`; `θ_Miguel = 6,2973°`, que a
patente escreve como ~0,110 e 6,297). A errata fica registrada **aqui** para que o kernel
não lave o erro por omissão: quem lê a linguagem da patente dentro do kernel lê junto o que
dela foi riscado.

⚠ **⚠ EMENDA v299 — AO LADO: o alcance que a v298 declarou estava SUBMEDIDO.** A v298 escreveu
aqui *"o erro é de **uma** patente"*, tendo varrido só a camada de **memória**. Na camada dos
**artefatos** o nome aparece também na **BR 10 2026 006129-8** (`iald_ontology.py:281`,
`IALD_Kernel_v6.txt:113`, `v11`, e a cópia do vault `v12`), no runner
`one_aprendizado_continuo.py` (≈14 pontos), e em `components.json`, `evidence.json`,
`render3d.json` e ~20 `results/*.json`. E na **BR 10 2025 026951-1** (ACOM) o casamento foi
**conferido**, e é o mais leve: `α·√S(L)` aparece só em `acom_v19_logos.py`, inventariado como
*"corpus (não inlined) — pesquisa, ainda NÃO integrada ao runner"*. *Declarar ausência exige
varrer, e a v298 afirmou antes de varrer.*

**★ O mapa correto tem TRÊS níveis, e só um deles é grave:**
1. **BR 10 2026 005477-1** — erro **VIVO**: fórmula variável no relatório (eqs. 4 e 8), no
   runner, e **em cinco reivindicações: 1, 8, 14, 17 (independentes) + 5 (dependente)**
   [ERRATA v304 — medido no .docx depositado pela custódia, 30/08; a v298 dizia duas]. É a
   única com o erro em reivindicação;
2. **BR 10 2026 006129-8** — só o **NOME** sobrevive; o conteúdo já declara `INVARIANT = β_TGL`;
3. **BR 10 2025 026951-1** — só em **corpus de pesquisa não integrado**; sem reivindicação, sem
   runner.

**★★★ E O ACERVO JÁ SE CORRIGIU SOZINHO — mantendo o nome errado.** Seis dias depois da
005477-1, a **BR 10 2026 006129-8** (depósito **15/03/2026**) declara, em protótipo:
`EmpiricalInvariant("beta_adaptive", BETA_TGL, 1e-7, "Adaptive β converges to the constant —
INVARIANT")`. Logo a ordem do operador **não impõe nada de fora ao acervo**: ela reconhece uma
correção que o acervo já fizera **no conteúdo**, e nomeia o que ficou solto — **o nome**.

**★ A leitura que fecha:** `α·√S = α·√e` exatamente quando `S = e`. Se a medida converge para a
constante, então o que convergiu foi **`S → e` nats** — não `β`. **`β` nunca variou.** O
"β adaptativo" era o nome errado de *"a constante, vezes um fator que empiricamente tende a
1"*: leitura que **preserva a medida** (a entropia dos logits tendendo a `e` no regime medido
é achado real e interessante) e devolve `β_TGL` ao seu estatuto de constante canônica.

**Momento `[LEGAL]`:** o ePCT correspondente está **pronto e NÃO protocolado**, e a prioridade
BR de 09/03/2026 já está garantida — logo a correção cabe
**antes** do depósito internacional. Retirar fórmula errada estreita, não acrescenta
matéria. A execução é ato do operador com a agente de PI. `[LEGAL]`

⚠ **PROPRIEDADE INTELECTUAL:** o conteúdo aqui tipado é o que já consta do depósito INPI de
15/03/2026 — a prioridade o protege. Material não depositado **não entra**, e a decisão de
espelhar publicamente é ato do operador, conferido com a agente de PI. `[LEGAL]`
-/

namespace TGLExt

noncomputable section

/-! ## A — a fronteira natural e o acoplamento -/

/-- **A FRONTEIRA NATURAL** da patente: `θ_Miguel = arcsin(√β)`. -/
def thetaMiguel (β : ℝ) : ℝ := Real.arcsin (Real.sqrt β)

/-- **A FUNÇÃO DE ACOPLAMENTO VERBAL** da patente: `f(θ) = tanh((θ − θ_M)/Δθ)`. -/
def fVerbal (θ θM Δ : ℝ) : ℝ := Real.tanh ((θ - θM) / Δ)

/-- **O PISO DE HILBERT VERBAL**: o sinal mínimo exigido de cada frase, `β · S_max`. -/
def verbFloor (β Smax : ℝ) : ℝ := β * Smax

/-! ## B — o limiar de poda É a amplitude de reflexão -/

/-- [KERNEL] `sin(θ_Miguel β) = √β`. ⚠ **Elementar** — `Real.sin_arcsin` sobre
    `0 ≤ √β ≤ 1`. Está aqui só para servir à identificação seguinte, e o seu estatuto
    modesto fica dito. -/
theorem sin_thetaMiguel {β : ℝ} (h0 : 0 ≤ β) (h1 : β ≤ 1) :
    Real.sin (thetaMiguel β) = Real.sqrt β := by
  unfold thetaMiguel
  apply Real.sin_arcsin
  · linarith [Real.sqrt_nonneg β]
  · calc Real.sqrt β ≤ Real.sqrt 1 := Real.sqrt_le_sqrt h1
    _ = 1 := Real.sqrt_one

/-- [KERNEL] ★★★★★ **O LIMIAR DE PODA VERBAL É A AMPLITUDE DE REFLEXÃO DA FRONTEIRA.**

    Num enunciado só: em `θ = θ_Miguel`, a amplitude de reflexão da matriz-S vale `√β` — o
    mesmo número que a patente usa como limiar de poda (`g_ratio < √β ⟹ L_poda elimina`) —
    e ela fecha com a transmissão em 1.

    **Um só ângulo governa os dois domínios.** O que a patente chama de *vácuo verbal* é o
    que reflete menos que a amplitude da fronteira. -/
theorem the_pruning_threshold_is_the_reflection_amplitude {β : ℝ}
    (h0 : 0 ≤ β) (h1 : β ≤ 1) :
    Complex.normSq (Smat (thetaMiguel β) |>.mulVec e1 <| 1)
        = Real.sqrt β ^ 2
    ∧ Complex.normSq (Smat (thetaMiguel β) |>.mulVec e1 <| 1)
        + Complex.normSq (Smat (thetaMiguel β) |>.mulVec e1 <| 0) = 1 := by
  refine ⟨?_, normSq_reflection_add_transmission _⟩
  rw [normSq_reflection, sin_thetaMiguel h0 h1]

/-! ## C — o acoplamento separa, e é aí que ele vale -/

/-- [KERNEL] ★★ **O ACOPLAMENTO SE ANULA NA FRONTEIRA**: `f(θ_Miguel) = 0`. -/
theorem coupling_vanishes_at_the_boundary (θM Δ : ℝ) :
    fVerbal θM θM Δ = 0 := by
  unfold fVerbal
  simp

/-- [KERNEL] ★★ **O SINAL DO ACOPLAMENTO É O SINAL DO DESVIO**: `tanh` herda o sinal de
    `sinh`, porque `cosh > 0`. É o tijolo do separador. -/
theorem tanh_sign (t : ℝ) :
    (t < 0 → Real.tanh t < 0) ∧ (0 < t → 0 < Real.tanh t) := by
  rw [Real.tanh_eq_sinh_div_cosh]
  have hc : 0 < Real.cosh t := Real.cosh_pos t
  constructor
  · intro ht
    exact div_neg_of_neg_of_pos (Real.sinh_neg_iff.mpr ht) hc
  · intro ht
    exact div_pos (Real.sinh_pos_iff.mpr ht) hc

/-- [KERNEL] ★★★★ **A FRONTEIRA SEPARA OS DOIS DOMÍNIOS VERBAIS**, e é isto que faz do
    limiar um separador de verdade e não um carimbo: o acoplamento é **negativo abaixo** de
    `θ_Miguel` e **positivo acima**, com o zero exatamente na fronteira.

    É a forma tipada do classificador de poda da patente: existe o que fica de um lado e
    existe o que fica do outro — e um critério que aprovasse tudo não separaria nada. -/
theorem the_boundary_separates_the_verbal_domains {θ θM Δ : ℝ} (hΔ : 0 < Δ) :
    (θ < θM → fVerbal θ θM Δ < 0)
    ∧ (θM < θ → 0 < fVerbal θ θM Δ)
    ∧ fVerbal θM θM Δ = 0 := by
  refine ⟨fun h => ?_, fun h => ?_, coupling_vanishes_at_the_boundary θM Δ⟩
  · exact (tanh_sign ((θ - θM) / Δ)).1 (div_neg_of_neg_of_pos (by linarith) hΔ)
  · exact (tanh_sign ((θ - θM) / Δ)).2 (div_pos (by linarith) hΔ)

/-! ## D — o piso verbal -/

/-- [KERNEL] ★★ **O PISO É FRAÇÃO ESTRITA DO MÁXIMO**: com `0 < β < 1` e `S_max > 0`, o
    piso de Hilbert verbal é positivo e **estritamente menor** que o máximo — exige sinal,
    e não exige o impossível. -/
theorem the_verb_floor_is_a_fraction_of_the_max {β Smax : ℝ}
    (hβ0 : 0 < β) (hβ1 : β < 1) (hS : 0 < Smax) :
    0 < verbFloor β Smax ∧ verbFloor β Smax < Smax := by
  unfold verbFloor
  constructor
  · positivity
  · nlinarith

end

end TGLExt
