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
import TGLExt.SiteLogLikelihood
import Mathlib.Analysis.Normed.Group.InfiniteSum

set_option autoImplicit false
set_option maxHeartbeats 1600000
namespace ChatgptAudit.Cocycle030
open Matrix Filter Topology Set TGLExt ChatgptAudit.Response028
  ChatgptAudit.Profile026 ChatgptAudit.Transport027 ChatgptAudit.Thermal025
noncomputable section

theorem factor_norm_closed (P : SiteProfile) :
    IsClosed (theFactorObject P : Set (TowerHilbert P →L[ℂ] TowerHilbert P)) := by
  have he : Set.centralizer (Set.centralizer (theFactorObject P : Set (TowerHilbert P →L[ℂ] TowerHilbert P)))=
      (theFactorObject P : Set (TowerHilbert P →L[ℂ] TowerHilbert P)) :=
    (theFactorObject P).centralizer_centralizer'
  rw [←he]
  exact Set.isClosed_centralizer _

theorem modular_conjugation_continuous (P : SiteProfile) (s : ℝ) :
    Continuous (modularConjugation P s) := by
  change Continuous (fun A : TowerHilbert P →L[ℂ] TowerHilbert P =>
    (modularFlowUnitary P s).toContinuousLinearEquiv.toContinuousLinearMap.comp
      (A.comp (modularFlowUnitary P s).symm.toContinuousLinearEquiv.toContinuousLinearMap))
  fun_prop

theorem state_norm_continuous (P : SiteProfile) : Continuous (omegaState P) := by
  unfold omegaState
  fun_prop

theorem centralizer_norm_closed (P : SiteProfile) :
    IsClosed (omegaCentralizer P) := by
  have hz : IsClosed (⋂ B : TowerHilbert P →L[ℂ] TowerHilbert P,
      ⋂ (_ : B∈theFactorObject P), {A | omegaState P (A*B)=omegaState P (B*A)}) := by
    apply isClosed_iInter
    intro B
    apply isClosed_iInter
    intro _
    exact isClosed_eq ((state_norm_continuous P).comp (continuous_id.mul continuous_const))
      ((state_norm_continuous P).comp (continuous_const.mul continuous_id))
  convert (factor_norm_closed P).inter hz using 1
  ext A
  simp [omegaCentralizer]

theorem site_likelihood_mem_centralizer (P : SiteProfile) (n : ℕ) (x : ℝ) :
    siteLikelihood P n x∈omegaCentralizer P := by
  refine ⟨site_likelihood_mem_factor P n x,?_⟩
  intro B hB
  have h := (site_zero_mem_centralizer P n).2 B hB
  simp only [siteLikelihood,add_mul,mul_add,smul_mul_assoc,mul_smul_comm,sub_mul,mul_sub,one_mul,mul_one]
  simp only [omegaState,_root_.add_apply,_root_.sub_apply,
    _root_.smul_apply,inner_add_right,inner_sub_right,inner_smul_right]
  change inner ℂ (hOmega P) ((siteZeroProjection P n*B) (hOmega P))=
    inner ℂ (hOmega P) ((B*siteZeroProjection P n) (hOmega P)) at h
  rw [h]

def likelihoodTerm (b : SummableAmplitude) (t : ℝ) (n : ℕ) :
    TowerHilbert thirdThermalReference →L[ℂ] TowerHilbert thirdThermalReference :=
  siteLikelihood thirdThermalReference n (b.value n*regularParameter t)

def likelihoodPrefix (b : SummableAmplitude) (t : ℝ) (N : ℕ) :
    TowerHilbert thirdThermalReference →L[ℂ] TowerHilbert thirdThermalReference :=
  ∑ n∈Finset.range (N+1), likelihoodTerm b t n

def likelihoodGenerator (b : SummableAmplitude) (t : ℝ) :
    TowerHilbert thirdThermalReference →L[ℂ] TowerHilbert thirdThermalReference :=
  ∑' n, likelihoodTerm b t n

theorem likelihood_argument_bounds (b : SummableAmplitude) (t : ℝ) (n : ℕ) :
    0 ≤ b.value n*regularParameter t ∧ b.value n*regularParameter t≤1/12 :=
  ⟨mul_nonneg (b.nonnegative n) (regular_parameter_nonnegative t),
    (mul_le_of_le_one_right (b.nonnegative n) (regular_parameter_lt_one t).le).trans (b.bound n)⟩

theorem likelihood_term_bound (b : SummableAmplitude) (t : ℝ) (n : ℕ) :
    ‖likelihoodTerm b t n‖≤(6*regularParameter t)*b.value n := by
  have h := site_likelihood_bound thirdThermalReference n (b.value n*regularParameter t)
    (likelihood_argument_bounds b t n).1 (likelihood_argument_bounds b t n).2
  simpa only [likelihoodTerm,mul_comm,mul_left_comm,mul_assoc] using h

theorem likelihood_norm_summable (b : SummableAmplitude) (t : ℝ) :
    Summable (fun n => ‖likelihoodTerm b t n‖) :=
  Summable.of_nonneg_of_le (fun _ => norm_nonneg _) (likelihood_term_bound b t)
    (b.summable.mul_left (6*regularParameter t))

theorem likelihood_summable (b : SummableAmplitude) (t : ℝ) :
    Summable (likelihoodTerm b t) :=
  (likelihood_norm_summable b t).of_norm

theorem likelihood_prefix_tendsto (b : SummableAmplitude) (t : ℝ) :
    Tendsto (likelihoodPrefix b t) atTop (𝓝 (likelihoodGenerator b t)) :=
  (likelihood_summable b t).hasSum.tendsto_sum_nat.comp (tendsto_add_atTop_nat 1)

theorem likelihood_generator_bound (b : SummableAmplitude) (t : ℝ) :
    ‖likelihoodGenerator b t‖≤6*regularParameter t*amplitudeMass b :=
  tsum_of_norm_bounded (b.summable.hasSum.mul_left (6*regularParameter t)) (likelihood_term_bound b t)

theorem likelihood_term_selfadjoint (b : SummableAmplitude) (t : ℝ) (n : ℕ) :
    IsSelfAdjoint (likelihoodTerm b t n) := site_likelihood_selfadjoint _ _ _

theorem likelihood_generator_selfadjoint (b : SummableAmplitude) (t : ℝ) :
    IsSelfAdjoint (likelihoodGenerator b t) := by
  change star (∑' n, likelihoodTerm b t n)=_
  rw [tsum_star]
  simp only [(likelihood_term_selfadjoint b t _).star_eq]
  rfl

theorem likelihood_prefix_mem_factor (b : SummableAmplitude) (t : ℝ) (N : ℕ) :
    likelihoodPrefix b t N∈theFactorObject thirdThermalReference :=
  sum_mem (fun n _ => site_likelihood_mem_factor _ n _)

theorem likelihood_generator_mem_factor (b : SummableAmplitude) (t : ℝ) :
    likelihoodGenerator b t∈theFactorObject thirdThermalReference :=
  tsum_mem (factor_norm_closed _) (fun n => site_likelihood_mem_factor _ n _)

theorem likelihood_term_modular_fixed (b : SummableAmplitude) (t s : ℝ) (n : ℕ) :
    modularConjugation thirdThermalReference s (likelihoodTerm b t n)=likelihoodTerm b t n :=
  site_likelihood_modular_fixed _ _ _ _

theorem likelihood_prefix_modular_fixed (b : SummableAmplitude) (t s : ℝ) (N : ℕ) :
    modularConjugation thirdThermalReference s (likelihoodPrefix b t N)=likelihoodPrefix b t N := by
  simp only [likelihoodPrefix,map_sum,likelihood_term_modular_fixed]

theorem likelihood_generator_modular_fixed (b : SummableAmplitude) (t s : ℝ) :
    modularConjugation thirdThermalReference s (likelihoodGenerator b t)=likelihoodGenerator b t := by
  apply tendsto_nhds_unique
    ((modular_conjugation_continuous _ s).tendsto _ |>.comp (likelihood_prefix_tendsto b t))
  simpa only [Function.comp_def,likelihood_prefix_modular_fixed] using likelihood_prefix_tendsto b t

theorem likelihood_generator_zero (b : SummableAmplitude) : likelihoodGenerator b 0=0 := by
  simp [likelihoodGenerator,likelihoodTerm,regular_parameter_zero,site_likelihood_zero]

#print axioms factor_norm_closed
#print axioms modular_conjugation_continuous
#print axioms state_norm_continuous
#print axioms centralizer_norm_closed
#print axioms site_likelihood_mem_centralizer
#print axioms likelihood_argument_bounds
#print axioms likelihood_term_bound
#print axioms likelihood_norm_summable
#print axioms likelihood_summable
#print axioms likelihood_prefix_tendsto
#print axioms likelihood_generator_bound
#print axioms likelihood_term_selfadjoint
#print axioms likelihood_generator_selfadjoint
#print axioms likelihood_prefix_mem_factor
#print axioms likelihood_generator_mem_factor
#print axioms likelihood_term_modular_fixed
#print axioms likelihood_prefix_modular_fixed
#print axioms likelihood_generator_modular_fixed
#print axioms likelihood_generator_zero
end
end ChatgptAudit.Cocycle030
