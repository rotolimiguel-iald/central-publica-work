-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_030 (06/09/2026), transposta em 06/09/2026
-- Lote 030: o COCICLO GLOBAL — gerador de log-verossimilhanca somavel (auto-adjunto, no fator), o cociclo
--   unitario u(t,s) com a identidade TORCIDA u(s+r) = u(s)·sigma_s(u(r)) (Connes, para a perturbacao
--   comutante), cortes efetivos e limite dos prefixos, estado preparado reproduzido (filtro positivo e
--   invertivel), covariancia no fator inteiro (duplo comutante, sem postular WOT), leitura entropica no
--   limite dos prefixos, e a LEITURA ANGULAR QUADRATICA (objeto positivo; coeficiente de ordem t² nulo;
--   cota de 4a ordem). ERRATA NOMINAL 001 (ao lado): `likelihood_terms_summable` le-se `likelihood_summable`.
--   Estatuto [REAL / INPUT / OPEN]: familia comutante especificada (referencia 1/3,2/3; b somavel), nao
--   teorema sobre todo par de estados fieis; operador de Tomita RELATIVO nao limitado, Connes-RN e
--   entropia de Araki gerais NAO reclamados; area geometrica e H3 geral seguem OPEN.
-- Auditoria da gerencia (sessao d554e796, 06/09/2026): hashes 16/16; manifesto 260/260; auditor da
--   bancada exit 0; recompilacao INDEPENDENTE 6/6, axiomas no trio; guarda de colisao estatica no ROOT;
--   enunciados lidos. Transposicao MECANICA (cabecalho + prefixo TGLExt.).
-- NAO move gate; nao e fisica; NOT_FALSIFIED nunca e CONFIRMED; CONFIRMADA proibido.
-- ---------------------------------------------------------------------
import TGLExt.SummableLikelihoodGenerator

set_option autoImplicit false
set_option maxHeartbeats 1600000
namespace ChatgptAudit.Cocycle030
open Matrix Filter Topology Set TGLExt ChatgptAudit.Response028
  ChatgptAudit.Profile026 ChatgptAudit.Transport027 ChatgptAudit.Thermal025
noncomputable section

local instance (P : SiteProfile) : NormedAlgebra ℚ (TowerHilbert P →L[ℂ] TowerHilbert P) :=
  NormedAlgebra.restrictScalars ℚ ℂ _

local instance (P : SiteProfile) : IsScalarTower ℚ ℂ (TowerHilbert P →L[ℂ] TowerHilbert P) :=
  IsScalarTower.restrictScalars ℚ ℂ _

def likelihoodCocycle (b : SummableAmplitude) (t s : ℝ) :
    TowerHilbert thirdThermalReference →L[ℂ] TowerHilbert thirdThermalReference :=
  NormedSpace.exp (((s : ℂ)*Complex.I) • likelihoodGenerator b t)

def likelihoodPrefixCocycle (b : SummableAmplitude) (t s : ℝ) (N : ℕ) :
    TowerHilbert thirdThermalReference →L[ℂ] TowerHilbert thirdThermalReference :=
  NormedSpace.exp (((s : ℂ)*Complex.I) • likelihoodPrefix b t N)

def likelihoodFilter (b : SummableAmplitude) (t : ℝ) :
    TowerHilbert thirdThermalReference →L[ℂ] TowerHilbert thirdThermalReference :=
  NormedSpace.exp ((1/2 : ℂ) • likelihoodGenerator b t)

theorem likelihood_prefix_selfadjoint (b : SummableAmplitude) (t : ℝ) (N : ℕ) :
    IsSelfAdjoint (likelihoodPrefix b t N) := by
  change star (∑ n∈Finset.range (N+1), likelihoodTerm b t n)=_
  simp only [star_sum,(likelihood_term_selfadjoint b t _).star_eq]
  rfl

theorem likelihood_cocycle_unitary (b : SummableAmplitude) (t s : ℝ) :
    likelihoodCocycle b t s∈unitary _ :=
  NormedSpace.exp_mem_unitary_of_mem_skewAdjoint
    ((likelihood_generator_selfadjoint b t).smul_mem_skewAdjoint
      (by simp : star ((s : ℂ)*Complex.I)= -((s : ℂ)*Complex.I)))

theorem likelihood_cocycle_zero (b : SummableAmplitude) (t : ℝ) :
    likelihoodCocycle b t 0=1 := by simp [likelihoodCocycle]

theorem likelihood_cocycle_reference (b : SummableAmplitude) (s : ℝ) :
    likelihoodCocycle b 0 s=1 := by simp [likelihoodCocycle,likelihood_generator_zero]

theorem likelihood_cocycle_group (b : SummableAmplitude) (t s r : ℝ) :
    likelihoodCocycle b t (s+r)=likelihoodCocycle b t s*likelihoodCocycle b t r := by
  have h : Commute (((s : ℂ)*Complex.I) • likelihoodGenerator b t)
      (((r : ℂ)*Complex.I) • likelihoodGenerator b t) :=
    ((Commute.refl _).smul_left _).smul_right _
  unfold likelihoodCocycle
  rw [←NormedSpace.exp_add_of_commute h,←add_smul]
  congr 2
  push_cast
  ring

theorem likelihood_cocycle_star (b : SummableAmplitude) (t s : ℝ) :
    star (likelihoodCocycle b t s)=likelihoodCocycle b t (-s) := by
  simp only [likelihoodCocycle,NormedSpace.star_exp,star_smul,
    (likelihood_generator_selfadjoint b t).star_eq,star_mul,Complex.star_def,
    Complex.conj_ofReal,Complex.conj_I,Complex.ofReal_neg,neg_mul]
  congr 1
  congr 1
  ring

theorem likelihood_cocycle_inverse (b : SummableAmplitude) (t s : ℝ) :
    likelihoodCocycle b t s*likelihoodCocycle b t (-s)=1 := by
  rw [←likelihood_cocycle_group,add_neg_cancel,likelihood_cocycle_zero]

theorem likelihood_cocycle_continuous (b : SummableAmplitude) (t : ℝ) :
    Continuous (likelihoodCocycle b t) := by
  unfold likelihoodCocycle
  fun_prop

theorem likelihood_cocycle_mem_factor (b : SummableAmplitude) (t s : ℝ) :
    likelihoodCocycle b t s∈theFactorObject thirdThermalReference := by
  apply NormedSpace.exp_mem (R := ℂ) (s := (theFactorObject thirdThermalReference).toStarSubalgebra)
    (factor_norm_closed _)
  exact (theFactorObject thirdThermalReference).toStarSubalgebra.smul_mem
    (likelihood_generator_mem_factor b t) _

theorem likelihood_cocycle_modular_fixed (b : SummableAmplitude) (t s r : ℝ) :
    modularConjugation thirdThermalReference r (likelihoodCocycle b t s)=likelihoodCocycle b t s := by
  unfold likelihoodCocycle
  rw [NormedSpace.map_exp (modularConjugation thirdThermalReference r)
    (modular_conjugation_continuous _ r),map_smul,likelihood_generator_modular_fixed]

theorem likelihood_cocycle_twisted (b : SummableAmplitude) (t s r : ℝ) :
    likelihoodCocycle b t (s+r)=likelihoodCocycle b t s*
      modularConjugation thirdThermalReference s (likelihoodCocycle b t r) := by
  rw [likelihood_cocycle_modular_fixed,likelihood_cocycle_group]

theorem likelihood_prefix_cocycle_limit (b : SummableAmplitude) (t s : ℝ) :
    Tendsto (likelihoodPrefixCocycle b t s) atTop (𝓝 (likelihoodCocycle b t s)) := by
  exact NormedSpace.exp_continuous.continuousAt.tendsto.comp
    (tendsto_const_nhds.smul (likelihood_prefix_tendsto b t))

theorem likelihood_filter_selfadjoint (b : SummableAmplitude) (t : ℝ) :
    IsSelfAdjoint (likelihoodFilter b t) := by
  change star (likelihoodFilter b t)=likelihoodFilter b t
  simp [likelihoodFilter,NormedSpace.star_exp,star_smul,(likelihood_generator_selfadjoint b t).star_eq]

theorem likelihood_filter_mem_factor (b : SummableAmplitude) (t : ℝ) :
    likelihoodFilter b t∈theFactorObject thirdThermalReference := by
  apply NormedSpace.exp_mem (R := ℂ) (s := (theFactorObject thirdThermalReference).toStarSubalgebra)
    (factor_norm_closed _)
  exact (theFactorObject thirdThermalReference).toStarSubalgebra.smul_mem
    (likelihood_generator_mem_factor b t) _

theorem likelihood_filter_modular_fixed (b : SummableAmplitude) (t s : ℝ) :
    modularConjugation thirdThermalReference s (likelihoodFilter b t)=likelihoodFilter b t := by
  unfold likelihoodFilter
  rw [NormedSpace.map_exp (modularConjugation thirdThermalReference s)
    (modular_conjugation_continuous _ s),map_smul,likelihood_generator_modular_fixed]

theorem likelihood_filter_prefix_limit (b : SummableAmplitude) (t : ℝ) :
    Tendsto (fun N => NormedSpace.exp ((1/2 : ℂ) • likelihoodPrefix b t N)) atTop
      (𝓝 (likelihoodFilter b t)) :=
  NormedSpace.exp_continuous.continuousAt.tendsto.comp
    (tendsto_const_nhds.smul (likelihood_prefix_tendsto b t))

theorem likelihood_filter_square (b : SummableAmplitude) (t : ℝ) :
    likelihoodFilter b t*likelihoodFilter b t=NormedSpace.exp (likelihoodGenerator b t) := by
  unfold likelihoodFilter
  rw [←NormedSpace.exp_add_of_commute (Commute.refl _),←add_smul]
  norm_num

theorem likelihood_filter_zero (b : SummableAmplitude) : likelihoodFilter b 0=1 := by
  simp [likelihoodFilter,likelihood_generator_zero]

#print axioms likelihoodCocycle
#print axioms likelihoodFilter
#print axioms likelihood_prefix_selfadjoint
#print axioms likelihood_cocycle_unitary
#print axioms likelihood_cocycle_zero
#print axioms likelihood_cocycle_reference
#print axioms likelihood_cocycle_group
#print axioms likelihood_cocycle_star
#print axioms likelihood_cocycle_inverse
#print axioms likelihood_cocycle_continuous
#print axioms likelihood_cocycle_mem_factor
#print axioms likelihood_cocycle_modular_fixed
#print axioms likelihood_cocycle_twisted
#print axioms likelihood_prefix_cocycle_limit
#print axioms likelihood_filter_selfadjoint
#print axioms likelihood_filter_mem_factor
#print axioms likelihood_filter_modular_fixed
#print axioms likelihood_filter_prefix_limit
#print axioms likelihood_filter_square
#print axioms likelihood_filter_zero
end
end ChatgptAudit.Cocycle030
