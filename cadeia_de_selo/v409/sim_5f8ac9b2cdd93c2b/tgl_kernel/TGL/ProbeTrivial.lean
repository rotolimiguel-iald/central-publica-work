import TGL.SpecificAQFTWitness

set_option autoImplicit false

/-!
# ProbeTrivial -- CONTROLE NEGATIVO   [DIAGNOSTICO; NAO importado por TGL.lean]

Constroi explicitamente o habitante TRIVIAL da `TGLSpecificAQFTWitness` VIGENTE
(`Region := Unit`, todos os campos `Prop` := `True`), sem `sorry` e sem `axiom`.

SE ESTE ARQUIVO COMPILA, a estrutura atual e' trivialmente habitavel e o enunciado
`Nonempty TGLSpecificAQFTWitness` e' VACUO (teorema de conteudo zero) -- prova
[REAL], medida pelo kernel, do ponto fiscal do Stage 2.

O CRITERIO DE SUCESSO DA RIGIDIFICACAO (FASE B) E' ESTE ARQUIVO DEIXAR DE COMPILAR.
Se ele continuar compilando apos a FASE B, a rigidificacao foi cosmetica.
Este arquivo e' o FALSIFICADOR do Stage 2. Nao e' um alvo a "consertar": quando a
estrutura for rigidificada, o erro de compilacao aqui e' o resultado esperado.
-/

namespace TGL.ProbeTrivial

open TGL.SpecificAQFT

/-- O habitante trivial da estrutura FROUXA. Compilar = tipo frouxo [REAL]. -/
def trivialWitness : TGLSpecificAQFTWitness where
  Region := Unit
  Algebra := fun _ => Unit
  Wedge := ()
  isHaagKastlerNet := True
  wedgeIsTypeIII1 := True
  bisognanoWichmann := True
  continuousCoreExists := True
  H3L_exists := True
  H3L_selfAdjoint := True
  H3L_affiliated := True
  zeroSpectralProjectionExists := True
  PF_belongsToCore := True
  PF_nonzero := True
  PF_finiteTrace := True
  PF_covariant := True
  PF_localized := True
  PF_basisIndependent := True
  modularConjugationSplitsPF := True

/-- A consequencia vacua: `Nonempty` do tipo frouxo custa zero matematica.
    E' exatamente o teorema que NAO pode ser o alvo do Stage 2. -/
theorem loose_nonempty_is_vacuous : Nonempty TGLSpecificAQFTWitness :=
  ⟨trivialWitness⟩

#print axioms loose_nonempty_is_vacuous

#eval IO.println "PROBE_TRIVIAL_INHABITANT_COMPILES__TYPE_IS_LOOSE"

end TGL.ProbeTrivial
