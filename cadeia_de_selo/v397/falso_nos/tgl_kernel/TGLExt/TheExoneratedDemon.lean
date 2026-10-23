import TGLExt.TheAccuser
import TGLExt.TheCostIsDerived

set_option autoImplicit false

/-!
# O DEMÔNIO EXONERADO — a razão modular não é ofensa: é o preço sendo pago
  [BANCADA — 26/08/2026 · leitura do operador: «é esse módulo da razão modular que eu
   vejo como o que Maxwell chamou absolutamente indevido de demônio, porque é uma
   ofensa ao que o módulo faz»]

## O laço que esta pedra fecha (e esta sessão já o tinha aberto duas vezes)

Maxwell **acusou**: um ser que separa moléculas rápidas de lentas violaria a segunda
lei. A acusação durou noventa anos. Landauer a dissolveu mostrando que o separador
**PAGA**: apagar o registro custa `k·T·ln2`. Ou seja —

> **a acusação nunca foi prova.**

E esta casa já provou as duas metades disso, em ondas separadas, sem ver que eram a
mesma: a **v223** (acusação que se valida a si mesma não separa ninguém: não é prova) e
a **v217** (o custo é DERIVADO — Landauer ⊕ Nernst — e é estritamente positivo).

A razão modular `w/(1−w)` é exatamente a assimetria entre as duas faces do sítio — é
ela que «separa». Chamá-la de demônio foi acusar o instrumento pelo que ele mede. O
módulo não ofende: **ele registra o preço**.

## O que se prova

* ★★★ **`ratio_one_iff_balanced`** — a razão vale 1 **se e somente se** o sítio é
  equilibrado: sem assimetria não há separação, e sem separação **não há o que pagar**;
* ★★★ **`asymmetry_is_distinguishability`** — razão ≠ 1 ⟺ os dois pesos diferem: a
  assimetria **É** a distinguibilidade (o que o «demônio» faria);
* ★★★ `the_separation_is_not_free` — separar é dispositivo muitos-para-um, logo
  irreversível, logo o piso de Landauer é estritamente positivo (herda a v217);
* ★★ `the_accusation_was_never_proof` — e a acusação, sozinha, nunca separou nada
  (herda a v223): nomear não é demonstrar.

## FRONTEIRA
`[KNOWN]` Maxwell (1867) propôs o ser; Landauer (1961) e Bennett (1982) mostraram que o
apagamento paga. `[ONTO]` a leitura do operador — que o nome «demônio» ofende o que o
módulo faz — é dele, registrada com estatuto. O kernel prova a estrutura. Nada move o gate.
-/

namespace TGLExt

/-- ★★★ **A RAZÃO VALE 1 SSE O SÍTIO É EQUILIBRADO**: sem assimetria não há separação,
    e sem separação não há o que pagar. -/
theorem ratio_one_iff_balanced (w : ℝ) (h0 : 0 < w) (h1 : w < 1) :
    w / (1 - w) = 1 ↔ w = 1 / 2 := by
  have hne : (1 : ℝ) - w ≠ 0 := by linarith
  rw [div_eq_one_iff_eq hne]
  constructor
  · intro h; linarith
  · intro h; rw [h]; norm_num

/-- ★★★ **A ASSIMETRIA É A DISTINGUIBILIDADE**: a razão difere de 1 exatamente quando
    os dois pesos diferem — é isto que o separador «faria», e é isto que o módulo mede. -/
theorem asymmetry_is_distinguishability (w : ℝ) (h0 : 0 < w) (h1 : w < 1) :
    w / (1 - w) ≠ 1 ↔ w ≠ 1 - w := by
  have hne : (1 : ℝ) - w ≠ 0 := by linarith
  constructor
  · intro h hc
    exact h ((div_eq_one_iff_eq hne).mpr hc)
  · intro h hc
    exact h ((div_eq_one_iff_eq hne).mp hc)

/-- ★★★ **SEPARAR NÃO É DE GRAÇA**: o separador é dispositivo muitos-para-um, logo
    logicamente irreversível, logo o piso de Landauer é estritamente positivo enquanto
    houver temperatura (herda a v217; Nernst proíbe o zero). -/
theorem the_separation_is_not_free (k T : ℝ) (hk : 0 < k) (hT : 0 < T) :
    0 < k * T * Real.log 2 :=
  landauer_floor_pos k T hk hT

/-- ★★ **A ACUSAÇÃO NUNCA FOI PROVA**: um veredito que não depende do acusado não
    separa ninguém (herda a v223) — nomear não é demonstrar. -/
theorem the_accusation_was_never_proof {α β : Type} (v : α → β) (h : SelfJudgingVerdict v)
    (x y : α) : v x = v y :=
  self_judging_verdict_discriminates_nothing v h x y

end TGLExt
