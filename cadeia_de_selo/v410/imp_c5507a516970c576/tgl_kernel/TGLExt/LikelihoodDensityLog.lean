-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_033 (06/09/2026), transposta em 06/09/2026
-- Lote 033: DENSIDADE CENTRALIZANTE, logaritmo e cociclo canonico — a algebra do centralizador de omega
--   definida sem o fluxo (fechada, soma, produto, exponencial); L, R, H e u no centralizador; densidade
--   positiva, auto-adjunta, invertivel, no fator e NORMALIZADA; logaritmo genuino e unico (CFC.log_exp);
--   potencia imaginaria limitada = cociclo, unitaria; estado da densidade e UNICIDADE da densidade no fator
--   (H, K no fator; sem supor positividade das concorrentes); controle da leitura angular (par no tempo;
--   estado de referencia invariante pelo cociclo). Estatuto [REAL / KNOWN / DERIVED / INPUT / OPEN]:
--   a identificacao de Connes e especializacao explicita de Hiai 9.4(2) [KNOWN/DERIVED], nao teorema novo
--   do kernel; Pedersen-Takesaki geral, area, retorno estabilizante e gravidade geral NAO pagos.
-- Auditoria da gerencia (sessao d554e796, 06/09/2026): hashes 10/10; manifesto 265/265; auditor exit 0;
--   recompilacao INDEPENDENTE 3/3 apos a REGRA 3, axiomas no trio; guarda de colisao; enunciados lidos.
-- TRANSPOSICAO: cabecalho + prefixo TGLExt. + REGRA 3 (instancias LOCAIS anonimas nomeadas
--   inst_<Modulo>_<k>): Lean gerava o MESMO nome automatico (Density033.instNormedAlgebraRat...) em
--   CentralizerDensity e LikelihoodDensityLog e o ROOT nao os importa juntos; so o NOME da declaracao muda,
--   nenhuma prova. Os oleans da bancada traziam sufixos de arquivo que um compilador limpo nao gera
--   (ambiente da bancada com oleans reaproveitados) — ORDEM_008 pede instancias NOMEADAS daqui em diante.
-- NAO move gate; nao e fisica; NOT_FALSIFIED nunca e CONFIRMED; CONFIRMADA proibido.
-- ---------------------------------------------------------------------
import TGLExt.RelativeModularProduct
import Mathlib.Analysis.SpecialFunctions.ContinuousFunctionalCalculus.ExpLog.Basic
import Mathlib.Analysis.CStarAlgebra.ContinuousLinearMap

set_option autoImplicit false
set_option maxHeartbeats 1200000
namespace ChatgptAudit.Density033
open Filter Topology Set TGLExt ChatgptAudit.Cocycle030 ChatgptAudit.Response028
  ChatgptAudit.Profile026 ChatgptAudit.Transport027 ChatgptAudit.Thermal025
noncomputable section

local instance inst_LikelihoodDensityLog_1 (P : SiteProfile) : NormedAlgebra ℚ (TowerHilbert P →L[ℂ] TowerHilbert P) :=
  NormedAlgebra.restrictScalars ℚ ℂ _

def likelihoodDensity (b : SummableAmplitude) (t : ℝ) :
    TowerHilbert thirdThermalReference →L[ℂ] TowerHilbert thirdThermalReference :=
  NormedSpace.exp (likelihoodGenerator b t)

def boundedDensityPower (b : SummableAmplitude) (t s : ℝ) :
    TowerHilbert thirdThermalReference →L[ℂ] TowerHilbert thirdThermalReference :=
  NormedSpace.exp (((s : ℂ)*Complex.I) • CFC.log (likelihoodDensity b t))

theorem likelihood_density_square (b : SummableAmplitude) (t : ℝ) :
    likelihoodDensity b t=likelihoodFilter b t*likelihoodFilter b t :=
  (likelihood_filter_square b t).symm

theorem likelihood_density_positive (b : SummableAmplitude) (t : ℝ) :
    (likelihoodDensity b t).IsPositive := by
  rw [likelihood_density_square]
  have h := ContinuousLinearMap.isPositive_adjoint_comp_self (likelihoodFilter b t)
  change (star (likelihoodFilter b t)*likelihoodFilter b t).IsPositive at h
  rwa [(likelihood_filter_selfadjoint b t).star_eq] at h

theorem likelihood_density_selfadjoint (b : SummableAmplitude) (t : ℝ) :
    IsSelfAdjoint (likelihoodDensity b t) := by
  change star (NormedSpace.exp (likelihoodGenerator b t))=_
  rw [NormedSpace.star_exp,(likelihood_generator_selfadjoint b t).star_eq]
  rfl

theorem likelihood_density_invertible (b : SummableAmplitude) (t : ℝ) :
    IsUnit (likelihoodDensity b t) := NormedSpace.isUnit_exp _

theorem likelihood_density_mem_factor (b : SummableAmplitude) (t : ℝ) :
    likelihoodDensity b t∈theFactorObject thirdThermalReference := by
  rw [likelihood_density_square]
  exact (theFactorObject thirdThermalReference).mul_mem
    (likelihood_filter_mem_factor b t) (likelihood_filter_mem_factor b t)

theorem likelihood_density_normalized (b : SummableAmplitude) (t : ℝ) :
    omegaState thirdThermalReference (likelihoodDensity b t)=1 :=
  likelihood_exponential_normalized b t

theorem likelihood_density_log (b : SummableAmplitude) (t : ℝ) :
    CFC.log (likelihoodDensity b t)=likelihoodGenerator b t :=
  CFC.log_exp (likelihoodGenerator b t) (likelihood_generator_selfadjoint b t)

theorem likelihood_filter_log (b : SummableAmplitude) (t : ℝ) :
    CFC.log (likelihoodFilter b t)=(1/2 : ℂ) • likelihoodGenerator b t := by
  apply CFC.log_exp
  change star ((1/2 : ℂ) • likelihoodGenerator b t)=_
  simp [star_smul,(likelihood_generator_selfadjoint b t).star_eq]

theorem likelihood_density_log_unique (b : SummableAmplitude) (t : ℝ)
    (K : TowerHilbert thirdThermalReference →L[ℂ] TowerHilbert thirdThermalReference)
    (hK : IsSelfAdjoint K) (he : NormedSpace.exp K=likelihoodDensity b t) :
    K=likelihoodGenerator b t := by
  calc
    K=CFC.log (NormedSpace.exp K) := (CFC.log_exp K hK).symm
    _=CFC.log (likelihoodDensity b t) := congrArg CFC.log he
    _=likelihoodGenerator b t := likelihood_density_log b t

theorem bounded_density_power_eq_cocycle (b : SummableAmplitude) (t s : ℝ) :
    boundedDensityPower b t s=likelihoodCocycle b t s := by
  simp only [boundedDensityPower,likelihood_density_log,likelihoodCocycle]

theorem bounded_density_power_unitary (b : SummableAmplitude) (t s : ℝ) :
    boundedDensityPower b t s∈unitary _ := by
  rw [bounded_density_power_eq_cocycle]
  exact likelihood_cocycle_unitary b t s

theorem likelihood_density_reference (b : SummableAmplitude) :
    likelihoodDensity b 0=1 := by
  simp [likelihoodDensity,likelihood_generator_zero]

theorem phase_quadratic_time_even (b : SummableAmplitude) (t s : ℝ) :
    phaseQuadratic b t (-s)=phaseQuadratic b t s := by
  simp only [phase_quadratic_formula,likelihood_cocycle_star,neg_neg]
  abel

#print axioms likelihoodDensity
#print axioms boundedDensityPower
#print axioms likelihood_density_square
#print axioms likelihood_density_positive
#print axioms likelihood_density_selfadjoint
#print axioms likelihood_density_invertible
#print axioms likelihood_density_mem_factor
#print axioms likelihood_density_normalized
#print axioms likelihood_density_log
#print axioms likelihood_filter_log
#print axioms likelihood_density_log_unique
#print axioms bounded_density_power_eq_cocycle
#print axioms bounded_density_power_unitary
#print axioms likelihood_density_reference
#print axioms phase_quadratic_time_even
end
end ChatgptAudit.Density033
