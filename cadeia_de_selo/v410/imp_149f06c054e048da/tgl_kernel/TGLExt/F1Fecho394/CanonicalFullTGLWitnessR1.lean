import TGLExt.F1Fecho394.CanonicalFockModularCoreInputR1
set_option autoImplicit false

/-!
Candidata da gerencia c1 (02/11/2026): a TESTEMUNHA CANONICA PLENA como termo. Nome provisorio; o nome e do operador.

`TGL/ModularRealization.lean` anuncia desde a v24, em comentario, «def canonicalFullTGLWitness : FullTGLWitness := ... -- TERMO
(nao construido)»; o `um.py` le a chave `witness_layers.canonical_full_witness_term_constructed` pela presenca de
`TGL.ModularRealization.canonicalFullTGLWitness` no `axiom_report`. Com o certificado de Fock fisico habitado pela bancada
(`physicalFockCertificate`, F1.FECHO 16/10/2026, recompilado no sandbox em 02/11/2026), o termo e a montagem de duas pecas
que o kernel ja tem: a rede da luz `lightNet C` e a sua realizacao modular `lightRealization C`
(`TheImportedSecondQuantization.lean`). `FullTGLWitness := Σ W : TGLSpecificAQFTWitness, TGLModularRealization W`.

O que NAO e afirmado: nada da natureza; nenhuma confirmacao; o gate nao se move; as ressalvas da ratificacao R10 (K(O) ≠ ⊥ so
na cunha; «nucleo II_∞» como [KNOWN]; traco ENNReal ciclico, nao linear) valem aqui por heranca.
-/

namespace TGL.ModularRealization

open TGLExt.ImportedSQ F1Fecho.CanonicalFockModularCoreInputR1

/-- a testemunha canonica plena: a rede da luz sobre o certificado de Fock fisico, com a sua realizacao modular. -/
noncomputable def canonicalFullTGLWitness : FullTGLWitness :=
  ⟨lightNet physicalFockCertificate, lightRealization physicalFockCertificate⟩

/-- o tipo-Sigma esta habitado pelo termo canonico (nao so pelo regular da torre, `regularFullWitness`). -/
theorem canonical_full_witness_inhabited : Nonempty FullTGLWitness := ⟨canonicalFullTGLWitness⟩

/-- a primeira componente e a rede da luz fisica: o nome e a leitura, o conteudo e a definicao (rfl). -/
theorem canonicalFullTGLWitness_fst : canonicalFullTGLWitness.1 = lightNet physicalFockCertificate := rfl

end TGL.ModularRealization

#print axioms TGL.ModularRealization.canonicalFullTGLWitness
#print axioms TGL.ModularRealization.canonical_full_witness_inhabited
#print axioms TGL.ModularRealization.canonicalFullTGLWitness_fst
