-- SONDA P3 (exame F_KERNEL, 12/10/2026, so sandbox; NAO e pedra -- quem constroi nao aprova): «POSTO = RANK ao lado do A4».
-- Pergunta: o A4 do F1.ATRATOR ja da, por termo, que a LEITURA R tem posto (rank) 1? Corolario de duas linhas sobre
-- A3_reading_is_fixed_space_projection e A4_dimension_one, sem hipotese nova.
import TGLExt.TheSingularityReadsTheAttractorAdendo1
set_option autoImplicit false
namespace SondaPostoRank
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

end SondaPostoRank
#print axioms SondaPostoRank.A4_reading_rank_one
#print axioms SondaPostoRank.concrete_reading_rank_one
#print axioms SondaPostoRank.identity_reading_rank_two
