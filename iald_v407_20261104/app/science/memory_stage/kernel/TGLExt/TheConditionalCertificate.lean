import TGLExt.FrontierCertificate
import TGLExt.TheConjugationOfOperators
import TGLExt.TheIsometryOnWH
import TGLExt.TheCarrierBridge
import TGLExt.WedgeNet

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

/-!
# O CERTIFICADO CONDICIONADO — a montagem feita, e a dívida isolada num item só
  [BANCADA — 27/08/2026 · marco M4 · tarefa (d), a MONTAGEM]

## O que esta pedra faz

Das oito cláusulas do `ModularRealizationCertificate`, **sete já estão provadas** nesta
árvore: a função, a aditividade, a antilinearidade, a isometria, a involução, o vácuo
fixo, e `J M J ⊆ M′`. A oitava — `J M J ⊇ M′` — depende do **teorema de comutação**,
cujo obstáculo foi localizado com exatidão (v250) e cuja rota falsa foi eliminada
(entrelaçamento ≠ conjunção).

Esta pedra **monta o certificado CONDICIONADO** a essa única hipótese. O ganho é
preciso: a dívida do item deixa de ser «faltam cláusulas» e passa a ser **«falta UM
enunciado nomeado»** — e qualquer um pode conferir, lendo o kernel, que é só ele.

## ⚠ O QUE ISTO NÃO É
Isto **NÃO habita** o certificado. Uma instância condicionada a uma hipótese não
provada **não acende bandeira**, e o nome reservado do razonete **continua escuro**.
Montar não é pagar — do mesmo modo que precificar não é pagar (v245) e nomear o
obstáculo não é removê-lo (v250). β jamais entra; nada move o gate.

## O que se prova

* ★★ `commAlg_carrier` — o portador do COMUTANTE é o comutante da imagem da torre;
* ★★★ **`certificate_modulo_commutation`** — **SE** vale o teorema de comutação,
  **ENTÃO** as oito cláusulas valem: a montagem, feita.
-/

namespace TGLExt

/-- ★★ **O PORTADOR DO COMUTANTE** é o comutante da imagem da torre. -/
theorem commAlg_carrier :
    (commAlg : Set WCLM) = commutantSet (towerImage mixProfile) := by
  show (StarSubalgebra.centralizer ℂ
      ((theFactorObject mixProfile : Set WCLM)) : Set WCLM) = _
  rw [StarSubalgebra.coe_centralizer, StarMemClass.star_coe_eq, Set.union_self,
      theFactorObject_carrier, ← commutantSet_eq_centralizer, commutant_triple]

/-- ★★★ **A MONTAGEM, CONDICIONADA**: se vale o teorema de comutação, as oito
    cláusulas do certificado valem. A dívida fica isolada num enunciado só. -/
theorem certificate_modulo_commutation
    (hComm : commutantSet (towerImage mixProfile)
      ⊆ conjByJ mixProfile '' (commutantSet (commutantSet (towerImage mixProfile)))) :
    (∀ v w : WH, towerJ mixProfile (v + w)
        = towerJ mixProfile v + towerJ mixProfile w)
    ∧ (∀ (c : ℂ) (v : WH), towerJ mixProfile (c • v)
        = (starRingEnd ℂ) c • towerJ mixProfile v)
    ∧ (∀ v : WH, ‖towerJ mixProfile v‖ = ‖v‖)
    ∧ (∀ v : WH, towerJ mixProfile (towerJ mixProfile v) = v)
    ∧ (towerJ mixProfile (hOmega mixProfile) = hOmega mixProfile)
    ∧ (conjByJ mixProfile '' (theFactorObject mixProfile : Set WCLM)
        ⊆ (commAlg : Set WCLM))
    ∧ ((commAlg : Set WCLM)
        ⊆ conjByJ mixProfile '' (theFactorObject mixProfile : Set WCLM)) := by
  refine ⟨towerJ_add mixProfile, towerJ_conj_smul mixProfile,
    towerJ_norm mixProfile, towerJ_involutive mixProfile,
    towerJ_fixes_hOmega mixProfile, ?_, ?_⟩
  · rw [theFactorObject_carrier, commAlg_carrier]
    exact J_M_J_in_commutant mixProfile
  · rw [theFactorObject_carrier, commAlg_carrier]
    exact hComm

end TGLExt
