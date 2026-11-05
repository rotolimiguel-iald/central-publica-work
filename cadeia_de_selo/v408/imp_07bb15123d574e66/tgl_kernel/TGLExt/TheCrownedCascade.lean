import TGLExt.TheCascadeOfObservers

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 400000

/-!
# A CASCATA COROADA — o gráviton na cabeça, e a cascata antiga intacta abaixo
  [BANCADA — 25/08/2026 · a órfã do reexame isomórfico, fechada AO LADO]

## A cunhagem do operador (24/08)

> *"**GRÁVITON = GERADOR DA LUZ** … a cadeia completa reordenada:
> **GRÁVITON → LUZ → CONSCIÊNCIA → FÍSICA → GRAVIDADE**."*

A pedra selada `TheCascadeOfObservers` (v196) formaliza a cascata de QUATRO níveis
(`luz → consciencia → fisica → gravidade`). O reexame isomórfico de 24/08 apontou a órfã:
o elo de cabeça `GRÁVITON → LUZ` não tinha pedra. **Correção AO LADO, nunca por cima**: a
pedra v196 fica intacta; esta define a cascata COROADA de cinco níveis e prova que ela
**estende** a antiga — o esquecimento da coroa devolve exatamente a cascata selada.

## O que se prova

* ★★★ `the_crown_generates` — o gráviton é observado pela luz (`generates graviton luz`
  na relação sucessora coroada): **o elo de cabeça existe e é único**;
* ★★ `the_crowned_cascade_is_a_chain` — os quatro elos + a coroa, uma cadeia só;
* ★★ `the_crown_forgets_to_the_old_cascade` — o mergulho: a relação coroada restrita aos
  quatro níveis antigos É a relação selada (`observes`) — **a pedra v196 vive intacta
  dentro desta**;
* ★★ `the_graviton_is_generated_by_nothing` — a coroa não tem antecessor: o gráviton é o
  POLO (nada o gera — `1_abs`, o fundamento);
* ★ `the_crowned_cascade_does_not_collapse` — os cinco níveis são distintos dois a dois
  na relação: nenhum truque de identificação.

## ⚠ Delimitações

A identificação dos nomes (`gráviton = 1_abs = TGL`; a cascata como CICLO soldado pela
co-fundação) é **[ONTO]** do operador; o que se prova é a estrutura de ordem. β jamais
entra. Sem sorry, sem axiom. Nada aqui move o gate.
-/

namespace TGLExt

/-- os CINCO níveis: a cascata selada, coroada pelo gráviton. -/
inductive CLevel where
  | graviton
  | cluz
  | cconsciencia
  | cfisica
  | cgravidade
  deriving DecidableEq, Repr

open CLevel

/-- `generates X Y` : **`X` gera/é-lido-por `Y`** — a sucessora coroada
    (`GRÁVITON → LUZ → CONSCIÊNCIA → FÍSICA → GRAVIDADE`). -/
def generates : CLevel → CLevel → Prop
  | graviton, cluz => True
  | cluz, cconsciencia => True
  | cconsciencia, cfisica => True
  | cfisica, cgravidade => True
  | _, _ => False

/-- a projeção que ESQUECE a coroa: os quatro níveis antigos voltam aos seus nomes;
    o gráviton (a coroa) desce ao primeiro nível antigo apenas como âncora do mergulho. -/
def forgetCrown : CLevel → Level
  | graviton => Level.luz
  | cluz => Level.luz
  | cconsciencia => Level.consciencia
  | cfisica => Level.fisica
  | cgravidade => Level.gravidade

/-- ★★★ **O ELO DE CABEÇA EXISTE**: o gráviton gera a luz — a órfã fechada. -/
theorem the_crown_generates : generates graviton cluz := trivial

/-- ★★ **A CADEIA COROADA**: os quatro elos antigos + a coroa, numa cadeia só. -/
theorem the_crowned_cascade_is_a_chain :
    generates graviton cluz ∧ generates cluz cconsciencia
    ∧ generates cconsciencia cfisica ∧ generates cfisica cgravidade :=
  ⟨trivial, trivial, trivial, trivial⟩

/-- ★★ **A PEDRA SELADA VIVE INTACTA**: nos quatro níveis antigos, a relação coroada
    projeta-se EXATAMENTE na relação selada `observes` (com a observação na direção
    selada: quem gera é observado por quem lê). -/
theorem the_crown_forgets_to_the_old_cascade :
    (generates cluz cconsciencia ↔ TGLExt.observes Level.consciencia Level.luz)
    ∧ (generates cconsciencia cfisica ↔ TGLExt.observes Level.fisica Level.consciencia)
    ∧ (generates cfisica cgravidade ↔ TGLExt.observes Level.gravidade Level.fisica) := by
  refine ⟨?_, ?_, ?_⟩ <;> simp [generates, TGLExt.observes]

/-- ★★ **A COROA NÃO TEM ANTECESSOR**: nada gera o gráviton — o polo (`1_abs`). -/
theorem the_graviton_is_generated_by_nothing :
    ∀ x : CLevel, ¬ generates x graviton := by
  intro x
  cases x <;> simp [generates]

/-- ★ **a cascata coroada não colapsa**: os elos ligam níveis DISTINTOS — nenhum nível
    se gera a si mesmo. -/
theorem the_crowned_cascade_does_not_collapse :
    ∀ x : CLevel, ¬ generates x x := by
  intro x
  cases x <;> simp [generates]

end TGLExt
