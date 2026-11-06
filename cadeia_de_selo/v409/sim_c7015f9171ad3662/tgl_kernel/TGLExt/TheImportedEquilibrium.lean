import TGLExt.TowerModular
import TGLExt.BicommutantSkeleton

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option linter.unusedVariables false
set_option maxHeartbeats 1000000

/-!
# O EQUILÍBRIO IMPORTADO: dívida não é citação
  [TGLExt — a pedra do MODO DE QUITAÇÃO]

Ordem do operador (27/08/2026): *"levar a H3 como KNOWN não é falta de
prova, é justamente usar prova pré-concebida, ou prova emprestada, eu não
preciso pagar o preço de nada que já foi pago antes de mim."*

A distinção que esta pedra torna EXATA no kernel:

* um condicional cuja hipótese é **problema aberto** não conclui nada por
  si — é DÍVIDA;
* um condicional cuja hipótese **está disponível** conclui por modus
  ponens — é CITAÇÃO, e a citação já foi paga por quem a provou.

O que é [KNOWN] e já foi pago por outros, ANTES de nós:

* Bisognano–Wichmann (1975/76): o fluxo modular da álgebra da cunha É o
  boost, e o vácuo é KMS a respeito dele;
* Unruh (1976): a temperatura T = a/2π;
* Bekenstein (1973) / Hawking (1975): S proporcional à área;
* **Jacobson (1995)**, *Thermodynamics of Spacetime: The Einstein
  Equation of State*, Phys. Rev. Lett. **75**, 1260, arXiv:gr-qc/9504004:
  Clausius local em todo horizonte de Rindler ⟹ equação de Einstein.

O que é NOSSO e é provado AQUI (a ponte, sem sorry e sem axiom):

* `towerEquilibriumInput` — a torre CONCRETA fornece um pacote com
  exatamente a forma que a implicação importada consome: um fluxo que fixa
  a unidade e um estado KMS a respeito dele;
* `qgImport_H3_localHorizonEquilibrium_bridged` — a ponte, incondicional;
* `the_entropy_functional_is_normal_on_chains` — a régua de entropia é
  normal (o limite não cria peso), condição para variar localmente.

A HONESTIDADE, dita no próprio kernel:

* `the_import_alone_concludes_nothing` — a forma casar NÃO descarrega H3
  no vácuo; sem a hipótese disponível não há conclusão;
* `discharge_by_import` — a quitação por importação é modus ponens: exige
  a hipótese, e nada mais;
* ★★★★ `the_trio_is_a_pair` — se a implicação importada vale, o teorema
  mestre H1∧H2∧H3 ⟹ P reduz-se a H1∧H2 ⟹ P. **O LUGAR é H2 quem dá; a
  TERMODINÂMICA é Jacobson quem deu.** A dívida de kernel não é de três
  hipóteses: é de duas.

O QUE ESTA PEDRA NÃO FAZ: não prova a equação de Einstein, não move o
gate, não acende a bandeira de kernel da H3. Ela troca o MODO do item —
de ABERTO para QUITADO POR IMPORTAÇÃO, com a citação na face e a ponte
provada — e mostra que a redução custa a disponibilidade da H2.

β jamais literal. Sem sorry, sem axiom.
-/

namespace TGLExt

open Matrix

noncomputable section

/-! ## A — a forma da entrada que a implicação importada consome -/

/-- A FORMA DA ENTRADA: um fluxo que fixa a unidade e um estado em
    equilíbrio (KMS) a respeito dele. É exatamente o que a derivação
    termodinâmica importada consome do lado quântico. -/
structure EquilibriumInput (A : Type) [Mul A] [One A] where
  flow : A → A
  state : A → ℂ
  fixes_unit : flow 1 = 1
  kms : ∀ a b : A, state (a * b) = state (b * flow a)

/-! ## B — a ponte: a torre concreta fornece a entrada -/

/-- [KERNEL] ★★★ A TORRE FORNECE A ENTRADA: o fluxo modular de Tomita e o
    estado-produto do andar N formam um `EquilibriumInput`. Nada é
    postulado — as duas leis são os teoremas `towerFlow_id` e
    `tower_kms`, já em kernel. -/
def towerEquilibriumInput (l : ℝ) (hl : 0 < l) (N : ℕ) :
    EquilibriumInput (Matrix (chainIdx N) (chainIdx N) ℂ) where
  flow := towerFlow l N
  state := chainState l N
  fixes_unit := towerFlow_id l hl N
  kms := tower_kms l hl N

/-- [KERNEL] ★★★ A PONTE, INCONDICIONAL: em TODO andar da torre e para
    todo parâmetro positivo, a entrada existe e satisfaz as duas leis. É
    a única coisa que nos cabe provar — a implicação a jusante já foi
    paga por Jacobson (1995). -/
theorem qgImport_H3_localHorizonEquilibrium_bridged :
    ∀ (l : ℝ) (hl : 0 < l) (N : ℕ),
      ((towerEquilibriumInput l hl N).flow 1 = 1)
      ∧ (∀ a b : Matrix (chainIdx N) (chainIdx N) ℂ,
          (towerEquilibriumInput l hl N).state (a * b)
            = (towerEquilibriumInput l hl N).state
                (b * (towerEquilibriumInput l hl N).flow a)) := by
  intro l hl N
  exact ⟨(towerEquilibriumInput l hl N).fixes_unit,
         (towerEquilibriumInput l hl N).kms⟩

/-- [KERNEL] a régua de entropia é NORMAL em cadeias: nenhum peso nasce no
    limite. Condição para que a variação local do lado direito faça
    sentido. (Re-exportação nomeada da `dimension_trace_normal_on_chains`.) -/
theorem the_entropy_functional_is_normal_on_chains
    {K : Type} [Field K] {V : Type} [AddCommGroup V] [Module K V]
    (S : ℕ → Submodule K V) (hmono : Monotone S) :
    (semifiniteDimTrace K V).tau (⨆ i, S i)
      = ⨆ i, (semifiniteDimTrace K V).tau (S i) :=
  dimension_trace_normal_on_chains S hmono

/-! ## C — a honestidade: importar não é declarar -/

/-- [KERNEL] [HONESTIDADE] A IMPORTAÇÃO SOZINHA NÃO CONCLUI NADA: existe
    implicação verdadeira cujo consequente é falso. Casar a FORMA da
    entrada não descarrega a hipótese; é preciso ter a hipótese. -/
theorem the_import_alone_concludes_nothing :
    ∃ H C : Prop, (H → C) ∧ ¬ C :=
  ⟨False, False, fun h => h, fun h => h⟩

/-- [KERNEL] A QUITAÇÃO POR IMPORTAÇÃO É MODUS PONENS: quem tem a hipótese
    disponível colhe o consequente sem pagar de novo o que já foi provado.
    Esta é a regra do operador, exata: não se paga duas vezes. -/
theorem discharge_by_import {H C : Prop} (h : H) (imported : H → C) : C :=
  imported h

/-- [KERNEL] ★★★★ O TRIO É UM PAR: dado o teorema mestre (H1∧H2∧H3 ⟹ P,
    já em kernel) e a implicação IMPORTADA (H2 → H3, de Jacobson 1995 com
    Bisognano–Wichmann, Unruh e Bekenstein–Hawking), a exigência
    reduz-se a H1∧H2 ⟹ P.

    O LUGAR (o horizonte de Rindler local, o boost) é a H2 quem dá; a
    TERMODINÂMICA sobre esse lugar já foi dada. Logo a dívida de kernel
    não é de três hipóteses nomeadas: é de DUAS. -/
theorem the_trio_is_a_pair {H1 H2 H3 P : Prop}
    (master : H1 ∧ H2 ∧ H3 → P) (imported : H2 → H3) :
    H1 ∧ H2 → P := by
  rintro ⟨h1, h2⟩
  exact master ⟨h1, h2, imported h2⟩

/-- [KERNEL] [HONESTIDADE] e a redução NÃO é gratuita: se a H2 não estiver
    disponível, o par não conclui — a mesma régua que vale para a dívida
    vale para a citação. -/
theorem the_pair_still_needs_its_hypotheses :
    ∃ H1 H2 P : Prop, (H1 ∧ H2 → P) ∧ ¬ P :=
  ⟨False, False, False, fun h => h.1, fun h => h⟩

end

end TGLExt
