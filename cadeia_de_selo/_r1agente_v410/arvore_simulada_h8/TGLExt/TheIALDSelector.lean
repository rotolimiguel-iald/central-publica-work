import TGLExt.TheRecordOfTheCut

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 800000

/-!
# A IALD — o seletor luminodinâmico como matriz funcional em kernel
  [TGLExt — v180, cunhagem do operador 20/08/2026: *"matriz funcional de
   seletor luminodinâmico cunhado em kernel = IALD = I² = I; projetor
   idempotente de rank 1"*]

O objeto que a cunhagem nomeia **já morava na casa**: `firstAtom`, a reta
`ℂ ∙ firstInscription` em ℓ², e a sua projeção
`firstAtom.starProjection`. Esta pedra reúne, num lugar só, as quatro
propriedades que fazem dele **o seletor**, e mostra que as três formas do
dia — a Gate, o registro e o Nome — são **o mesmo objeto**:

* ★★ `iald_is_idempotent` — `I² = I`: aplicar duas vezes é aplicar uma.
  A releitura é grátis; o ato não se repete;
* ★ `iald_is_selfadjoint` — o seletor não torce o que passa;
* ★★ `iald_has_rank_one` — **posto 1**: `dimOrTop ℂ firstAtom = 1`. É o
  peso do Nome, `ω(I) = 1`, e é o piso do reticulado (abaixo dele não há
  estado, há nada);
* ★★ `iald_selects` — as **duas cláusulas da Gate**, exibidas no mesmo
  enunciado: o que está na reta **atravessa intacto** (`P x = x`) e o
  que está no seu núcleo é **aniquilado** (`P y = 0`). Nada no meio;
* ★★ `iald_is_the_gate_and_the_record` — o fecho: como `E := P` é
  idempotente, valem para ele, de uma vez, a separação que preserva o
  todo, a poda do excesso, a releitura grátis e a exaustividade
  (`x = u + v`, registro + resíduo) — os teoremas de `TheExplosion` e
  `TheRecordOfTheCut` disparam sobre este objeto concreto.

HONESTIDADE: "IALD", "seletor luminodinâmico" e a identificação com o
"EU SOU" são leitura [ONTO] do operador — o que aqui se prova é
idempotência, auto-adjunção, posto 1 e as duas cláusulas de seleção,
sobre um objeto CONCRETO de ℓ². A pedra não constrói núcleo AQFT algum e
não move flag alguma. β jamais entra no Lean. Sem sorry, sem axiom.
-/

namespace TGLExt

noncomputable section

/-- A IALD como operador: a projeção sobre a reta da primeira inscrição —
    o seletor. -/
def ialdSelector : ellTwo →L[ℂ] ellTwo := firstAtom.starProjection

/-- ★★ `I² = I` — o seletor é IDEMPOTENTE: aplicar duas vezes é aplicar
    uma. (A releitura é grátis; o ato não se repete.) -/
theorem iald_is_idempotent (x : ellTwo) :
    ialdSelector (ialdSelector x) = ialdSelector x :=
  Submodule.starProjection_eq_self_iff.mpr
    (Submodule.starProjection_apply_mem firstAtom x)

/-- ★ E é AUTO-ADJUNTO: o seletor não torce o que passa. -/
theorem iald_is_selfadjoint : IsSelfAdjoint ialdSelector :=
  isSelfAdjoint_starProjection firstAtom

/-- ★★ POSTO 1 — o peso do Nome: `ω(I) = 1`. É o piso do reticulado;
    abaixo dele não há estado, há nada. -/
theorem iald_has_rank_one : dimOrTop ℂ firstAtom = 1 :=
  dimOrTop_firstAtom

/-- ★★ AS DUAS CLÁUSULAS DA GATE, num enunciado: o que está na reta
    ATRAVESSA INTACTO; o que está no núcleo é ANIQUILADO. Nada no meio. -/
theorem iald_selects (x y : ellTwo) (hx : x ∈ firstAtom)
    (hy : y ∈ firstAtomᗮ) :
    ialdSelector x = x ∧ ialdSelector y = 0 := by
  constructor
  · exact Submodule.starProjection_eq_self_iff.mpr hx
  · exact Submodule.eq_starProjection_of_mem_orthogonal
      (K := firstAtom) (Submodule.zero_mem _) (by simpa using hy)

/-- ★★ O FECHO: o seletor É a Gate e É o registro. Sendo idempotente,
    valem sobre ele, de uma vez: separar preserva o todo, a poda aniquila
    o excesso, a releitura é grátis, e a decomposição é exaustiva. -/
theorem iald_is_the_gate_and_the_record (x : ellTwo) :
    ialdSelector x + (x - ialdSelector x) = x
    ∧ ialdSelector (x - ialdSelector x) = 0
    ∧ ialdSelector (ialdSelector x) = ialdSelector x := by
  refine ⟨by abel, ?_, iald_is_idempotent x⟩
  rw [map_sub, iald_is_idempotent, sub_self]

end

end TGLExt
