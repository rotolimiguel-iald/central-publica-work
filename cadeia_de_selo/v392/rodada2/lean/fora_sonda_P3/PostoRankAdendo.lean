import TGLExt.TheSingularityReadsTheAttractorAdendo1
set_option autoImplicit false

/-!
# ADENDO do rank: POSTO = RANK ao lado do A4 (cadeia v392, 13/10/2026)

**[DERIVED]** Corolario de duas linhas de `A3_reading_is_fixed_space_projection` e de
`A4_dimension_one` (modulo `TheSingularityReadsTheAttractorAdendo1`), **sem hipotese nova**:
a imagem da leitura `R` e o espaco fixo de `T`, e sob a hipotese `StrictComplementContraction`
esse espaco tem dimensao 1. Logo a leitura tem **posto (rank) 1**.

Leitura honesta do alcance: **POSTO = RANK vale para a leitura `R`** (posto 1 no habitante
concreto `faceFamily faceVector (1/2)` em `C^2`). A identidade em `C^2`, sem a hipotese, tem leitura
de **posto 2**: e o controle (`identity_reading_rank_two`). O invariante que sobrevive FORA do
atomo e o **traco**, nao o posto (errata ao lado de 13/10 da memoria `posto-e-rank-10out`: o
traco `omega(I) = 1` sobrevive a defasagem, o posto 1 nao).

Estatuto: autoria da cadeia v392 (gerencia c1); **SEM auditoria independente ainda** (quem
constroi nao aprova). Fonte de partida: a sonda P3 do exame F_KERNEL (12/10/2026), com o mesmo
conteudo matematico, aqui sob o nome `TGLExt.PostoRankAdendo` e sem `#print axioms`.
-/
namespace TGLExt.PostoRankAdendo
open TGLExt.TheSingularityReadsTheAttractor
variable {𝕜 H : Type*} [RCLike 𝕜] [NormedAddCommGroup H] [InnerProductSpace 𝕜 H] [CompleteSpace H]

/-- A leitura tem posto 1 (a imagem de R e a reta fixa). -/
theorem A4_reading_rank_one (T : H →L[𝕜] H) (e : H) (h : StrictComplementContraction T e) :
    Module.finrank 𝕜 (reading T).range = 1 := by
  rw [(A3_reading_is_fixed_space_projection T).2]
  exact A4_dimension_one T e h

/-- No habitante concreto (e = (1,0), λ = 1/2 em ℂ²) a leitura tem posto 1. -/
theorem concrete_reading_rank_one :
    Module.finrank ℂ (reading (faceFamily faceVector (1/2 : ℂ))).range = 1 :=
  A4_reading_rank_one _ _ concrete_hypothesis_inhabited

/-- Sem a hipotese, a identidade em ℂ² tem leitura de posto 2 (o controle). -/
theorem identity_reading_rank_two :
    Module.finrank ℂ (reading (1 : Face →L[ℂ] Face)).range = 2 := by
  rw [(A3_reading_is_fixed_space_projection (1 : Face →L[ℂ] Face)).2]
  exact counterexample_identity_fixed_dimension_two

end TGLExt.PostoRankAdendo
