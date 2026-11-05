-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_031 (06/09/2026), transposta em 06/09/2026
-- Lote 031..032: o OPERADOR MODULAR RELATIVO com dominio e fecho — S^0_{psi|omega}(A Omega) = A* Psi,
--   grafico relativo fechado por homeomorfismo dos graficos algebricos, dominio denso, adjunto antilinear
--   maximal, congruencia limitada (auto-adjunta, positiva) e Delta_rel = S*S com dominio, fecho,
--   auto-adjunticidade e positividade; e a COMUTACAO MODULAR: separacao de frequencias reais, reconhecimento
--   do grafico de Delta por testes fracos, B limitado auto-adjunto comutando com o fluxo preserva o dominio
--   de Delta e comuta; o filtro e o inverso preservam o dominio; IGUALDADE dos dominios de Delta relativo e
--   de referencia e igualdade dos operadores parciais (Delta_rel = produto de verossimilhanca x Delta_omega
--   como LinearPMap), positivo, auto-adjunto, fechado. Estatuto [REAL / INPUT / OPEN]: familia comutante
--   especificada (referencia 1/3,2/3; b somavel); calculo funcional/potencias relativas, identificacao
--   Connes/Araki completa, area geometrica e reconstrucao geral NAO pagos.
-- Auditoria da gerencia (sessao d554e796, 06/09/2026): hashes 12/12 + 12/12; manifestos 254/259; 2/2
--   auditores exit 0; recompilacao INDEPENDENTE 8/8, axiomas no trio; guarda de colisao estatica no ROOT;
--   enunciados lidos. Transposicao MECANICA (cabecalho + prefixo TGLExt.).
-- NAO move gate; nao e fisica; NOT_FALSIFIED nunca e CONFIRMED; CONFIRMADA proibido.
-- ---------------------------------------------------------------------
import TGLExt.LikelihoodCocycleControls

set_option autoImplicit false
set_option maxHeartbeats 1000000
namespace ChatgptAudit.Relative031
open Matrix Filter Topology Set TGLExt ChatgptAudit ChatgptAudit.Cocycle030
  ChatgptAudit.Response028 ChatgptAudit.Profile026 ChatgptAudit.Transport027 ChatgptAudit.Thermal025
noncomputable section

local instance (P : SiteProfile) : NormedAlgebra ℚ (TowerHilbert P →L[ℂ] TowerHilbert P) :=
  NormedAlgebra.restrictScalars ℚ ℂ _
local instance (P : SiteProfile) : IsScalarTower ℚ ℂ (TowerHilbert P →L[ℂ] TowerHilbert P) :=
  IsScalarTower.restrictScalars ℚ ℂ _

def inverseLikelihoodFilter (b : SummableAmplitude) (t : ℝ) :
    TowerHilbert thirdThermalReference →L[ℂ] TowerHilbert thirdThermalReference :=
  NormedSpace.exp ((-1/2 : ℂ) • likelihoodGenerator b t)

theorem filter_mul_inverse (b : SummableAmplitude) (t : ℝ) :
    likelihoodFilter b t*inverseLikelihoodFilter b t=1 := by
  have h : Commute ((1/2 : ℂ) • likelihoodGenerator b t)
      ((-1/2 : ℂ) • likelihoodGenerator b t) :=
    ((Commute.refl _).smul_left _).smul_right _
  unfold likelihoodFilter inverseLikelihoodFilter
  rw [←NormedSpace.exp_add_of_commute h,←add_smul]
  norm_num

theorem inverse_mul_filter (b : SummableAmplitude) (t : ℝ) :
    inverseLikelihoodFilter b t*likelihoodFilter b t=1 := by
  have h : Commute ((-1/2 : ℂ) • likelihoodGenerator b t)
      ((1/2 : ℂ) • likelihoodGenerator b t) :=
    ((Commute.refl _).smul_left _).smul_right _
  unfold likelihoodFilter inverseLikelihoodFilter
  rw [←NormedSpace.exp_add_of_commute h,←add_smul]
  norm_num

theorem inverse_filter_selfadjoint (b : SummableAmplitude) (t : ℝ) :
    IsSelfAdjoint (inverseLikelihoodFilter b t) := by
  change star (inverseLikelihoodFilter b t)=inverseLikelihoodFilter b t
  simp [inverseLikelihoodFilter,NormedSpace.star_exp,star_smul,
    (likelihood_generator_selfadjoint b t).star_eq]

theorem inverse_filter_mem_factor (b : SummableAmplitude) (t : ℝ) :
    inverseLikelihoodFilter b t∈theFactorObject thirdThermalReference := by
  apply NormedSpace.exp_mem (R := ℂ) (s := (theFactorObject thirdThermalReference).toStarSubalgebra)
    (factor_norm_closed _)
  exact (theFactorObject thirdThermalReference).toStarSubalgebra.smul_mem
    (likelihood_generator_mem_factor b t) _

def likelihoodFilterEquiv (b : SummableAmplitude) (t : ℝ) :
    TowerHilbert thirdThermalReference ≃L[ℂ] TowerHilbert thirdThermalReference where
  toLinearEquiv :=
    { toFun := likelihoodFilter b t
      invFun := inverseLikelihoodFilter b t
      map_add' := (likelihoodFilter b t).map_add
      map_smul' := (likelihoodFilter b t).map_smul
      left_inv := by
        intro x
        change (inverseLikelihoodFilter b t*likelihoodFilter b t) x=x
        rw [inverse_mul_filter]
        rfl
      right_inv := by
        intro x
        change (likelihoodFilter b t*inverseLikelihoodFilter b t) x=x
        rw [filter_mul_inverse]
        rfl }
  continuous_toFun := (likelihoodFilter b t).continuous
  continuous_invFun := (inverseLikelihoodFilter b t).continuous

theorem filter_equiv_apply (b : SummableAmplitude) (t : ℝ)
    (x : TowerHilbert thirdThermalReference) :
    likelihoodFilterEquiv b t x=likelihoodFilter b t x := rfl

theorem inverse_filter_equiv_apply (b : SummableAmplitude) (t : ℝ)
    (x : TowerHilbert thirdThermalReference) :
    (likelihoodFilterEquiv b t).symm x=inverseLikelihoodFilter b t x := rfl

theorem inverse_filter_vector (b : SummableAmplitude) (t : ℝ) :
    inverseLikelihoodFilter b t (amplitudeVector b t)=hOmega thirdThermalReference := by
  rw [←likelihood_filter_vector b t,←mul_apply_eq_comp,inverse_mul_filter]
  rfl

#print axioms inverseLikelihoodFilter
#print axioms likelihoodFilterEquiv
#print axioms filter_mul_inverse
#print axioms inverse_mul_filter
#print axioms inverse_filter_selfadjoint
#print axioms inverse_filter_mem_factor
#print axioms filter_equiv_apply
#print axioms inverse_filter_equiv_apply
#print axioms inverse_filter_vector
end
end ChatgptAudit.Relative031
