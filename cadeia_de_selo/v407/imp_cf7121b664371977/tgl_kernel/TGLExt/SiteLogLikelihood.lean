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
import TGLExt.SummableStateThermodynamics
import TGLExt.CentralizerLocal
import Mathlib.Analysis.CStarAlgebra.Exponential

set_option autoImplicit false
set_option maxHeartbeats 1600000
namespace ChatgptAudit.Cocycle030
open Matrix Filter Topology Set TGLExt ChatgptAudit.Response028
  ChatgptAudit.Profile026 ChatgptAudit.Transport027 ChatgptAudit.Thermal025
noncomputable section

def siteZeroProjection (P : SiteProfile) (n : ℕ) :
    TowerHilbert P →L[ℂ] TowerHilbert P :=
  siteOperator P n (Matrix.single 0 0 1)

theorem last_site_mul (n : ℕ) (a b : Matrix (Fin 2) (Fin 2) ℂ) :
    lastSiteMatrix n (a*b)=lastSiteMatrix n a*lastSiteMatrix n b := by
  cases n with
  | zero => rfl
  | succ n => simp only [lastSiteMatrix,←Matrix.mul_kronecker_mul,one_mul]

theorem last_site_one (n : ℕ) :
    lastSiteMatrix n (1 : Matrix (Fin 2) (Fin 2) ℂ)=1 := by
  cases n with
  | zero => rfl
  | succ n => simp [lastSiteMatrix]

theorem site_zero_projection (P : SiteProfile) (n : ℕ) :
    IsStarProjection (siteZeroProjection P n) := by
  constructor
  · change siteOperator P n (Matrix.single 0 0 1)*siteOperator P n (Matrix.single 0 0 1)=_
    unfold siteOperator
    rw [←towerPi_mul,←last_site_mul]
    congr 2
    ext i j
    fin_cases i <;> fin_cases j <;> norm_num [Matrix.mul_apply,Matrix.single_apply,Fin.sum_univ_two]
  · change star (siteOperator P n (Matrix.single 0 0 1))=siteOperator P n (Matrix.single 0 0 1)
    rw [←siteOperator_star]
    simp [Matrix.conjTranspose_single]

theorem site_zero_norm (P : SiteProfile) (n : ℕ) : ‖siteZeroProjection P n‖≤1 :=
  IsStarProjection.norm_le _ (site_zero_projection P n)

theorem site_one_norm (P : SiteProfile) (n : ℕ) : ‖1-siteZeroProjection P n‖≤1 :=
  IsStarProjection.norm_le _ (site_zero_projection P n).one_sub

theorem site_zero_commute (P : SiteProfile) (n m : ℕ) :
    Commute (siteZeroProjection P n) (siteZeroProjection P m) := by
  by_cases h : n=m
  · subst m; exact Commute.refl _
  · exact siteOperators_commute h _ _

theorem last_site_diagonal (n : ℕ) (d : Fin 2 → ℂ) :
    ∃ v : chainIdx n → ℂ, lastSiteMatrix n (Matrix.diagonal d)=Matrix.diagonal v := by
  cases n with
  | zero => exact ⟨d,rfl⟩
  | succ n =>
    refine ⟨fun i => d i.2,?_⟩
    simp only [lastSiteMatrix,←Matrix.diagonal_one,Matrix.diagonal_kronecker_diagonal,one_mul]

theorem site_zero_modular_fixed (P : SiteProfile) (n : ℕ) (s : ℝ) :
    modularConjugation P s (siteZeroProjection P n)=siteZeroProjection P n := by
  have hdiag : (Matrix.single 0 0 (1 : ℂ) : Matrix (Fin 2) (Fin 2) ℂ)=
      Matrix.diagonal ![1,0] := by
    ext i j
    fin_cases i <;> fin_cases j <;> norm_num [Matrix.single_apply,Matrix.diagonal_apply]
  unfold siteZeroProjection siteOperator
  rw [modularConjugation_local,hdiag]
  obtain ⟨v,hv⟩ := last_site_diagonal n ![1,0]
  rw [hv]
  congr 1
  ext i j
  by_cases h : i=j
  · subst j
    simp [flowLevel,modularPhase]
  · simp [flowLevel,Matrix.diagonal_apply_ne _ h]

theorem site_zero_mem_centralizer (P : SiteProfile) (n : ℕ) :
    siteZeroProjection P n∈omegaCentralizer P := by
  have hdiag : (Matrix.single 0 0 (1 : ℂ) : Matrix (Fin 2) (Fin 2) ℂ)=
      Matrix.diagonal ![1,0] := by
    ext i j
    fin_cases i <;> fin_cases j <;> norm_num [Matrix.single_apply,Matrix.diagonal_apply]
  unfold siteZeroProjection siteOperator
  rw [hdiag]
  obtain ⟨v,hv⟩ := last_site_diagonal n ![1,0]
  rw [hv]
  apply density_commuting_local_is_global_centralizer
  change Matrix.diagonal _*Matrix.diagonal _=Matrix.diagonal _*Matrix.diagonal _
  simp only [Matrix.diagonal_mul_diagonal]
  congr 1
  funext i
  exact mul_comm _ _

def logZeroRatio (x : ℝ) : ℝ := Real.log (1-3*x)
def logOneRatio (x : ℝ) : ℝ := Real.log (1+(3/2)*x)

theorem log_zero_ratio_bounds (x : ℝ) (hx : 0 ≤ x) (hb : x≤1/12) :
    -4*x≤logZeroRatio x ∧ logZeroRatio x≤0 := by
  have hy : 0<1-3*x := by linarith
  have hi : (1-3*x)⁻¹≤1+4*x := by
    rw [inv_eq_one_div,div_le_iff₀ hy]
    nlinarith [mul_nonneg hx (sub_nonneg.mpr hb)]
  constructor
  · have h := Real.one_sub_inv_le_log_of_pos hy
    change -4*x≤Real.log (1-3*x)
    linarith
  · have h := Real.log_le_sub_one_of_pos hy
    change Real.log (1-3*x)≤0
    linarith

theorem log_one_ratio_bounds (x : ℝ) (hx : 0 ≤ x) :
    0 ≤ logOneRatio x ∧ logOneRatio x≤2*x := by
  constructor
  · change 0 ≤ Real.log (1+(3/2)*x)
    exact Real.log_nonneg (by linarith)
  · have h := Real.log_le_sub_one_of_pos (by positivity : 0<1+(3/2)*x)
    change Real.log (1+(3/2)*x)≤2*x
    linarith

theorem log_ratio_abs_bound (x : ℝ) (hx : 0 ≤ x) (hb : x≤1/12) :
    |logZeroRatio x|+|logOneRatio x|≤6*x := by
  obtain ⟨h0l,h0u⟩ := log_zero_ratio_bounds x hx hb
  obtain ⟨h1l,h1u⟩ := log_one_ratio_bounds x hx
  rw [abs_of_nonpos h0u,abs_of_nonneg h1l]
  linarith

def siteLikelihood (P : SiteProfile) (n : ℕ) (x : ℝ) :
    TowerHilbert P →L[ℂ] TowerHilbert P :=
  (logZeroRatio x : ℂ) • siteZeroProjection P n+
    (logOneRatio x : ℂ) • (1-siteZeroProjection P n)

theorem site_likelihood_selfadjoint (P : SiteProfile) (n : ℕ) (x : ℝ) :
    IsSelfAdjoint (siteLikelihood P n x) := by
  change star (siteLikelihood P n x)=siteLikelihood P n x
  simp only [siteLikelihood,star_add,star_smul,star_sub,star_one,
    (site_zero_projection P n).isSelfAdjoint.star_eq,Complex.star_def,Complex.conj_ofReal]

theorem site_likelihood_bound (P : SiteProfile) (n : ℕ) (x : ℝ)
    (hx : 0 ≤ x) (hb : x≤1/12) : ‖siteLikelihood P n x‖≤6*x := by
  calc
    ‖siteLikelihood P n x‖≤
        ‖(logZeroRatio x : ℂ) • siteZeroProjection P n‖+
        ‖(logOneRatio x : ℂ) • (1-siteZeroProjection P n)‖ := norm_add_le _ _
    _≤|logZeroRatio x|+|logOneRatio x| := by
      simp only [norm_smul,Complex.norm_real,Real.norm_eq_abs]
      exact add_le_add (mul_le_of_le_one_right (abs_nonneg _) (site_zero_norm P n))
        (mul_le_of_le_one_right (abs_nonneg _) (site_one_norm P n))
    _≤6*x := log_ratio_abs_bound x hx hb

theorem site_likelihood_modular_fixed (P : SiteProfile) (n : ℕ) (x s : ℝ) :
    modularConjugation P s (siteLikelihood P n x)=siteLikelihood P n x := by
  simp only [siteLikelihood,map_add,map_smul,map_sub,map_one,site_zero_modular_fixed]

theorem site_likelihood_mem_factor (P : SiteProfile) (n : ℕ) (x : ℝ) :
    siteLikelihood P n x∈theFactorObject P := by
  have hp := (site_zero_mem_centralizer P n).1
  exact add_mem ((theFactorObject P).toStarSubalgebra.smul_mem hp _)
    ((theFactorObject P).toStarSubalgebra.smul_mem (sub_mem (one_mem _) hp) _)

theorem site_likelihood_zero (P : SiteProfile) (n : ℕ) : siteLikelihood P n 0=0 := by
  simp [siteLikelihood,logZeroRatio,logOneRatio]

#print axioms last_site_mul
#print axioms last_site_one
#print axioms site_zero_projection
#print axioms site_zero_norm
#print axioms site_one_norm
#print axioms site_zero_commute
#print axioms last_site_diagonal
#print axioms site_zero_modular_fixed
#print axioms site_zero_mem_centralizer
#print axioms log_zero_ratio_bounds
#print axioms log_one_ratio_bounds
#print axioms log_ratio_abs_bound
#print axioms site_likelihood_selfadjoint
#print axioms site_likelihood_bound
#print axioms site_likelihood_modular_fixed
#print axioms site_likelihood_mem_factor
#print axioms site_likelihood_zero
end
end ChatgptAudit.Cocycle030
