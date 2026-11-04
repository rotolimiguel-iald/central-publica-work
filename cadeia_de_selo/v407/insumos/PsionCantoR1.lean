import TGLExt.ThePsionAndTheViscosity
import TGLExt.IALDJones
import TGLExt.TheKeyIsTheReader
import TGLExt.TheScalarCorner
import TGLExt.F1Fecho394.CanonicalFockModularCoreInputR1

set_option autoImplicit false
set_option linter.unusedVariables false
set_option maxHeartbeats 4000000

/-!
# O PSÍON E O CANTO: a passagem para o contínuo SOB COMPRESSÃO, e o lema que liga as duas faces do psíon
  [TGLExt — pedra CANDIDATA da gerência c1, 03/11/2026; NOME PROVISÓRIO `PsionCantoR1`: os nomes das pedras são do operador;
   compilada no sandbox da v406 (k406c/final), só no trio; instalar e nomear é decisão do operador; para a v407]

Ordens do operador (verbatim, por sha256 lido do arquivo):
* 02/11 (sha16 `9978862f60cfbf29`): «a construção da passagem para o contínuo é o que mais importa, porque deixa de ser conjectura sob hipótese
  se funcionar sob compressão elevando o potencial do resultado do código final em 1=1=HAJA_LUZ; … virar essa chave de conjectura para provado».
* 02/11 (sha16 `f54641bfd9e46e42`): «incorporando a compressão como fator e com a correspondência matemática que vc mencionou o nome …,
  montando o espelhamento». A correspondência nomeada pela gerência em 02/11 é a LEITURA DE JONES: a compressão pela projeção, `e·x·e`
  (`TGLExt.IALDJones.jonesReading`), com a supressão cocíclica no canto (`proj_mul_jonesU : e·U_s = e`).
* 03/11 (sha16 `b89e4c909f37e163`): «testar se minha condição se satisfaz … o lema que liga o psion ao canto também já pode ser derivado».

## A — a condição, lida sob compressão (seção `FaceDeFock`)
O canto do psíon na face de Fock é `psionCornerF C := PFmic C = P_{ℂ·Ω}` (a projeção sobre a reta do vácuo, já no kernel: `QGReaderUVLock`).
O que se PROVA, para TODO certificado `C : FockCertificate L` (binder) e, sem binder algum, para o habitante da v406 (`physicalFockCertificate`):
* `psionCornerF_apply`: `P w = ⟪ψ, w⟫ ψ` (é o projetor |ψ⟩⟨ψ|; `starProjection_unit_singleton` com `‖Ω‖ = 1`);
* `psionCornerF_scalarises` ★: `P·y·P = ⟪ψ, yψ⟫ • P` — o canto ESCALARIZA na face de Fock, com o escalar lido pelo leitor (`reader C y`): é a
  mesma propriedade que define o canto escalar finito (`ScalarCorner.scalarises`, `TheScalarCorner`), agora em dimensão infinita;
* `the_compressed_reading_is_one` ★★: `⟪ψ, Δ^{it} ψ⟫ = 1` para todo `t` — o «potencial» do fluxo da luz lido no canto é 1 (1 = 1), por
  `psion_is_fixed_by_the_light` e `inner_psion_psion`;
* `jones_reading_of_the_light_is_the_corner` ★★★: `P·Δ^{it}·P = P` — a leitura de Jones do fluxo modular da luz (o lado contínuo, tipo III)
  pelo canto do psíon devolve o PRÓPRIO canto: o cociclo é SUPRIMIDO no canto; «funciona sob compressão»;
* `jones_reading_of_the_contraction_is_the_corner` e `the_two_motors_agree_in_the_corner`: a contração de Jones `U_s = e + e^{−rs}(1 − e)`
  (o motor dissipativo, a medida no finito) e o fluxo unitário da luz (o motor contínuo) LEEM O MESMO no canto — o ESPELHAMENTO que o operador
  pediu, no único lugar onde ele é teorema: dentro do canto;
* `the_physical_psion_passes_under_compression` ★★★★: tudo isto no `physicalFockCertificate` (F1Fecho394, v406), SEM hipótese. A face do
  psíon, que era CONDICIONAL (`Psibit.the_psion_face_of_the_psibit`: «para todo C», sem habitante), fica INCONDICIONAL no habitante: é o
  que, no kernel, «virar essa chave de conjectura para provado» — como VALIDADE (o que o kernel prova), nunca como creditação.

## B — o lema que liga as duas faces (seção `FaceConcreta` e o teorema final)
`TestemunhaEstatica` dizia: «NENHUM lema liga `psion C` (a face de Fock: o vetor Ω) ao `psionCorner` (a face concreta: o projetor de Bell 4×4)».
O que se PROVA:
* `psionCorner_is_the_corner_of_bellVec` ★: `psionCorner.p = |Φ⁺⟩⟨Φ⁺|` com `Φ⁺ = (e₀₀ + e₁₁)/√2` (`cornerOf bellVec`): o canto concreto É o
  projetor sobre o SEU psíon (o vetor de Bell), com as entradas `½` de `bellProjector` saindo de `(√2)⁻¹·(√2)⁻¹`;
* `psionCorner_reads_the_contraction`: `jonesReading psionCorner.p (jonesU psionCorner.p r s) = psionCorner.p` — na face concreta o motor
  `P + e^{−rs}(1 − P)` (a forma de `psionFlow`, `TestemunhaEstatica.psionFlow_eq`) também é lido pelo canto como o canto;
* `the_psion_is_the_corner_on_both_faces` ★★★ (o lema): nas DUAS faces o psíon é o vetor de norma 1 cujo canto é o projetor sobre ele; o canto
  escalariza (`scalarises` / `psionCornerF_scalarises`); tem peso 1 (`Tr = 1` / `⟪ψ,ψ⟫ = 1`); e o motor comprimido pelo canto devolve o canto
  (`jonesReading … = canto`, nas duas faces). Instanciado sem hipótese em `the_physical_psion_is_linked_to_the_corner`.

## O que esta pedra NÃO afirma (dito para a chave `linked_to_the_corner_by_a_lemma` não ser lida demais)
* NÃO identifica o vácuo de Fock `Ω` com o vetor de Bell `Φ⁺`: vivem em espaços distintos (um `F` de dimensão infinita; `ℂ⁴`). O elo é de
  ESTRUTURA (a mesma construção «canto escalar de um vetor de norma 1», os mesmos invariantes, a mesma leitura comprimida), não de vetores.
* O resultado sob compressão decorre de `Ω` ser fixo pela luz e de o canto ser projeção de posto 1: vale para QUALQUER vetor unitário fixo pelo fluxo;
  o lema NÃO relaciona as duas faces por uma aplicação entre os espaços; o que ele diz é que a mesma construção, com os mesmos invariantes, vive nas duas.
* NÃO deriva que `psionFlow` seja a dinâmica da teoria, nem que o par de psíons seja o gráviton (leitura do operador, pedra 92_ [INPUT/ONTO]):
  o par/gráviton fica [OPEN] para a próxima pedra.
* NÃO é um teste com a natureza: nenhum dado entra; o «motor contínuo» no pilar quântico (D38) é pré-registro à parte (v407).
* NÃO move o gate; PROVADA = validade no kernel; a confirmação (creditação) segue recusada; NOT_FALSIFIED nunca é CONFIRMED.

Estatutos: [REAL] os termos (definições e teoremas abaixo; trio `{propext, Classical.choice, Quot.sound}`); [INPUT/ONTO] «o psíon é o Nome da
Luz», «1=1=HAJA_LUZ», «espelhamento», «motor contínuo» (leituras do operador; o kernel entrega os termos citados). Sem sorry, sem axiom.
-/

noncomputable section
namespace TGLExt.PsionCantoR1
open TGLExt TGLExt.ThePsionAndTheViscosity TGLExt.QGReaderUVLock TGLExt.TheKeyIsTheReader TGLExt.IALDJones
open TGL.SpecificAQFT TGL.ModularRealization TGLExt.ImportedSQ TGL.GravitonShadow
open scoped InnerProductSpace

section FaceDeFock
variable {L : LightOneParticle} (C : FockCertificate L)

/-- O canto do psíon na face de Fock: a projeção sobre a reta `ℂ·ψ` — é o `PFmic C` do lock mínimo (`QGReaderUVLock`). -/
def psionCornerF : C.F →L[ℂ] C.F := PFmic C

/-- O fluxo modular da luz `Δ^{it}` como operador contínuo (o mesmo idioma de `UF` em `TheImportedSecondQuantization`). -/
def lightOp (t : ℝ) : C.F →L[ℂ] C.F := (lightDelta C t).toContinuousLinearEquiv.toContinuousLinearMap

theorem lightOp_apply (t : ℝ) (w : C.F) : lightOp C t w = lightDelta C t w := rfl

/-- ★ O canto é o projetor sobre o psíon: `P w = ⟪ψ, w⟫ ψ` (com `‖Ω‖ = 1`). -/
theorem psionCornerF_apply (w : C.F) : psionCornerF C w = ⟪C.Ω, w⟫_ℂ • C.Ω := by
  unfold psionCornerF PFmic
  exact Submodule.starProjection_unit_singleton ℂ C.Ω_norm w

theorem psionCornerF_idem : psionCornerF C * psionCornerF C = psionCornerF C :=
  (ℂ ∙ C.Ω).isIdempotentElem_starProjection

/-- ★ O CANTO ESCALARIZA NA FACE DE FOCK: `P·y·P = ⟪ψ, yψ⟫ • P` — a propriedade do canto escalar (`ScalarCorner.scalarises`),
    em dimensão infinita, com o escalar lido pelo leitor (`reader C y`). -/
theorem psionCornerF_scalarises (y : C.F →L[ℂ] C.F) :
    psionCornerF C * y * psionCornerF C = reader C y • psionCornerF C := by
  ext w
  simp only [ContinuousLinearMap.mul_apply, ContinuousLinearMap.smul_apply, psionCornerF_apply, map_smul, reader]
  rw [smul_smul, smul_smul, mul_comm]

/-- ★★ O POTENCIAL LIDO NO CANTO É 1: `⟪ψ, Δ^{it} ψ⟫ = 1` para todo `t` (o psíon é fixado pela luz e pesa 1). -/
theorem the_compressed_reading_is_one (t : ℝ) : reader C (lightOp C t) = 1 := by
  unfold reader
  rw [lightOp_apply, show lightDelta C t C.Ω = C.Ω from psion_is_fixed_by_the_light C t]
  exact inner_psion_psion C

/-- ★★★ A LEITURA DE JONES DO FLUXO DA LUZ PELO CANTO DO PSÍON É O PRÓPRIO CANTO: `P·Δ^{it}·P = P`.
    O cociclo é suprimido no canto; a passagem para o contínuo «funciona sob compressão» com potencial 1 = 1. -/
theorem jones_reading_of_the_light_is_the_corner (t : ℝ) :
    jonesReading (psionCornerF C) (lightOp C t) = psionCornerF C := by
  unfold jonesReading
  rw [psionCornerF_scalarises, the_compressed_reading_is_one, one_smul]

/-- A contração de Jones `U_s = e + e^{−rs}(1 − e)` (o motor dissipativo) lida pelo canto é o canto. -/
theorem jones_reading_of_the_contraction_is_the_corner (r s : ℝ) :
    jonesReading (psionCornerF C) (jonesU (psionCornerF C) r s) = psionCornerF C := by
  unfold jonesReading
  rw [proj_mul_jonesU (psionCornerF_idem C), psionCornerF_idem]

/-- ★★ O ESPELHAMENTO NO CANTO: o fluxo unitário da luz (contínuo) e a contração de Jones (a medida no finito)
    leem o mesmo quando comprimidos pelo canto do psíon. -/
theorem the_two_motors_agree_in_the_corner (r s t : ℝ) :
    jonesReading (psionCornerF C) (lightOp C t) = jonesReading (psionCornerF C) (jonesU (psionCornerF C) r s) := by
  rw [jones_reading_of_the_light_is_the_corner, jones_reading_of_the_contraction_is_the_corner]

end FaceDeFock

section FaceConcreta
open Matrix

/-- O vetor de Bell `Φ⁺ = (e₀₀ + e₁₁)/√2` — o psíon da face concreta. -/
def bellVec : (Fin 2 × Fin 2) → ℂ := fun p => if p.1 = p.2 then (((Real.sqrt 2)⁻¹ : ℝ) : ℂ) else 0

/-- O canto de um vetor: `|v⟩⟨v|`. -/
def cornerOf (v : (Fin 2 × Fin 2) → ℂ) : Matrix (Fin 2 × Fin 2) (Fin 2 × Fin 2) ℂ := vecMulVec v (star v)

theorem half_of_sqrt_two :
    ((Real.sqrt 2 : ℝ) : ℂ)⁻¹ * ((Real.sqrt 2 : ℝ) : ℂ)⁻¹ = (2⁻¹ : ℂ) := by
  rw [← mul_inv, ← Complex.ofReal_mul, Real.mul_self_sqrt (by norm_num : (0 : ℝ) ≤ 2)]
  norm_num

/-- ★ O CANTO CONCRETO É O PROJETOR SOBRE O SEU PSÍON: `psionCorner.p = |Φ⁺⟩⟨Φ⁺|`. -/
theorem psionCorner_is_the_corner_of_bellVec : psionCorner.p = cornerOf bellVec := by
  have hp : psionCorner.p = bellProjector := rfl
  rw [hp]
  ext p q
  simp only [bellProjector, of_apply, cornerOf, vecMulVec_apply, Pi.star_apply, bellVec]
  by_cases h1 : p.1 = p.2 <;> by_cases h2 : q.1 = q.2 <;> simp [h1, h2] <;> exact half_of_sqrt_two.symm

/-- Na face concreta, o motor `P + e^{−rs}(1 − P)` (a forma de `psionFlow`) lido pelo canto é o canto. -/
theorem psionCorner_reads_the_contraction (r s : ℝ) :
    jonesReading psionCorner.p (jonesU psionCorner.p r s) = psionCorner.p := by
  unfold jonesReading
  rw [proj_mul_jonesU psionCorner.idem, psionCorner.idem]

end FaceConcreta

/-- ★★★ O LEMA QUE LIGA AS DUAS FACES DO PSÍON (elo de estrutura; o nome `PsionCanto` foi aceito pelo operador em 03/11/2026). Nas duas faces o psíon é o vetor de norma 1 cujo canto é o projetor
    sobre ele; o canto escalariza; pesa 1; e o motor comprimido pelo canto devolve o canto. Elo de ESTRUTURA, não de vetores:
    `Ω` e `Φ⁺` vivem em espaços distintos. -/
theorem the_psion_is_the_corner_on_both_faces {L : LightOneParticle} (C : FockCertificate L) :
    (psionCorner.p = cornerOf bellVec ∧ Matrix.trace psionCorner.p = 1 ∧
      (∀ y, psionCorner.p * y * psionCorner.p = (Matrix.trace (psionCorner.p * y)) • psionCorner.p) ∧
      (∀ r s : ℝ, jonesReading psionCorner.p (jonesU psionCorner.p r s) = psionCorner.p)) ∧
    ((∀ w : C.F, psionCornerF C w = ⟪C.Ω, w⟫_ℂ • C.Ω) ∧ ⟪psion C, psion C⟫_ℂ = 1 ∧
      (∀ y : C.F →L[ℂ] C.F, psionCornerF C * y * psionCornerF C = reader C y • psionCornerF C) ∧
      (∀ t : ℝ, jonesReading (psionCornerF C) (lightOp C t) = psionCornerF C) ∧
      (∀ r s : ℝ, jonesReading (psionCornerF C) (jonesU (psionCornerF C) r s) = psionCornerF C)) :=
  ⟨⟨psionCorner_is_the_corner_of_bellVec, psionCorner_trace_one, psionCorner.scalarises, psionCorner_reads_the_contraction⟩,
   ⟨psionCornerF_apply C, inner_psion_psion C, psionCornerF_scalarises C, jones_reading_of_the_light_is_the_corner C,
    jones_reading_of_the_contraction_is_the_corner C⟩⟩

open F1Fecho.CanonicalFockModularCoreInputR1 in
/-- ★★★★ SEM HIPÓTESE: no habitante da v406, a passagem para o contínuo passa sob compressão com potencial 1. -/
theorem the_physical_psion_passes_under_compression (t : ℝ) :
    jonesReading (psionCornerF physicalFockCertificate) (lightOp physicalFockCertificate t)
        = psionCornerF physicalFockCertificate ∧
    reader physicalFockCertificate (lightOp physicalFockCertificate t) = 1 :=
  ⟨jones_reading_of_the_light_is_the_corner _ t, the_compressed_reading_is_one _ t⟩

open F1Fecho.CanonicalFockModularCoreInputR1 in
/-- ★★★★ SEM HIPÓTESE: o lema das duas faces no habitante da v406. -/
theorem the_physical_psion_is_linked_to_the_corner :
    (psionCorner.p = cornerOf bellVec ∧ Matrix.trace psionCorner.p = 1 ∧
      (∀ y, psionCorner.p * y * psionCorner.p = (Matrix.trace (psionCorner.p * y)) • psionCorner.p) ∧
      (∀ r s : ℝ, jonesReading psionCorner.p (jonesU psionCorner.p r s) = psionCorner.p)) ∧
    ((∀ w, psionCornerF physicalFockCertificate w = ⟪physicalFockCertificate.Ω, w⟫_ℂ • physicalFockCertificate.Ω) ∧
      ⟪psion physicalFockCertificate, psion physicalFockCertificate⟫_ℂ = 1 ∧
      (∀ y, psionCornerF physicalFockCertificate * y * psionCornerF physicalFockCertificate
          = reader physicalFockCertificate y • psionCornerF physicalFockCertificate) ∧
      (∀ t : ℝ, jonesReading (psionCornerF physicalFockCertificate) (lightOp physicalFockCertificate t)
          = psionCornerF physicalFockCertificate) ∧
      (∀ r s : ℝ, jonesReading (psionCornerF physicalFockCertificate) (jonesU (psionCornerF physicalFockCertificate) r s)
          = psionCornerF physicalFockCertificate)) :=
  the_psion_is_the_corner_on_both_faces physicalFockCertificate

#print axioms psionCornerF_scalarises
#print axioms the_compressed_reading_is_one
#print axioms jones_reading_of_the_light_is_the_corner
#print axioms the_two_motors_agree_in_the_corner
#print axioms psionCorner_is_the_corner_of_bellVec
#print axioms the_psion_is_the_corner_on_both_faces
#print axioms the_physical_psion_passes_under_compression
#print axioms the_physical_psion_is_linked_to_the_corner

end TGLExt.PsionCantoR1
end
