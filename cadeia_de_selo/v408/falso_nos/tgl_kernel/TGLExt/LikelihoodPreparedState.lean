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
import TGLExt.LikelihoodCocycle
import TGLExt.Cocycle
import TGLExt.ChainPrefix

set_option autoImplicit false
set_option maxHeartbeats 4000000
namespace ChatgptAudit.Cocycle030
open Matrix Filter Topology Set TGLExt ChatgptAudit ChatgptAudit.Response028
  ChatgptAudit.Profile026 ChatgptAudit.Transport027 ChatgptAudit.Thermal025
open scoped Matrix.Norms.Operator Kronecker
noncomputable section

local instance (P : SiteProfile) : NormedAlgebra ℚ (TowerHilbert P →L[ℂ] TowerHilbert P) :=
  NormedAlgebra.restrictScalars ℚ ℂ _

def towerPiAlgHom (P : SiteProfile) (N : ℕ) :
    Matrix (chainIdx N) (chainIdx N) ℂ →ₐ[ℂ]
      (TowerHilbert P →L[ℂ] TowerHilbert P) where
  toFun := towerPi P
  map_one' := towerPi_one N
  map_mul' := towerPi_mul N
  map_zero' := (towerPiLinear P N).map_zero
  map_add' := towerPi_add
  commutes' := by
    intro c
    simp only [Algebra.algebraMap_eq_smul_one,towerPi_smul,towerPi_one]

theorem tower_pi_exp (P : SiteProfile) (N : ℕ) (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    towerPi P (NormedSpace.exp a)=NormedSpace.exp (towerPi P a) :=
  NormedSpace.map_exp (towerPiAlgHom P N)
    (towerPiAlgHom P N).toLinearMap.continuous_of_finiteDimensional a

def lastSiteLinear (n : ℕ) :
    Matrix (Fin 2) (Fin 2) ℂ →ₗ[ℂ] Matrix (chainIdx n) (chainIdx n) ℂ where
  toFun := lastSiteMatrix n
  map_add' := by
    intro a b
    cases n with
    | zero => rfl
    | succ n =>
      ext i j
      simp [lastSiteMatrix,mul_add]
  map_smul' := by
    intro c a
    cases n with
    | zero => rfl
    | succ n =>
      ext i j
      simp only [lastSiteMatrix,Matrix.kroneckerMap_apply,Matrix.smul_apply,smul_eq_mul,RingHom.id_apply]
      ring

theorem last_site_add (n : ℕ) (a b : Matrix (Fin 2) (Fin 2) ℂ) :
    lastSiteMatrix n (a+b)=lastSiteMatrix n a+lastSiteMatrix n b :=
  (lastSiteLinear n).map_add a b

theorem last_site_sub (n : ℕ) (a b : Matrix (Fin 2) (Fin 2) ℂ) :
    lastSiteMatrix n (a-b)=lastSiteMatrix n a-lastSiteMatrix n b :=
  (lastSiteLinear n).map_sub a b

theorem last_site_smul (n : ℕ) (c : ℂ) (a : Matrix (Fin 2) (Fin 2) ℂ) :
    lastSiteMatrix n (c • a)=c • lastSiteMatrix n a :=
  (lastSiteLinear n).map_smul c a

def matrixLogRatio {ι : Type} [DecidableEq ι] (p q : ι → ℝ) : Matrix ι ι ℂ :=
  Matrix.diagonal (fun i => ((Real.log (q i)-Real.log (p i) : ℝ) : ℂ))

theorem binary_log_matrix (p q : ℝ) :
    matrixLogRatio (siteW p) (siteW q)=
      ((Real.log q-Real.log p : ℝ) : ℂ) • (Matrix.single 0 0 1 : Matrix (Fin 2) (Fin 2) ℂ)+
      ((Real.log (1-q)-Real.log (1-p) : ℝ) : ℂ) • (1-Matrix.single 0 0 1) := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    norm_num [matrixLogRatio,siteW,Matrix.diagonal_apply,Matrix.single_apply,Matrix.one_apply]

theorem third_log_coefficients (x : ℝ) (hx : 0 ≤ x) (hb : x≤1/12) :
    Real.log (1/3-x)-Real.log (1/3)=logZeroRatio x ∧
      Real.log (1-(1/3-x))-Real.log (1-1/3)=logOneRatio x := by
  have hp : (1/3-x : ℝ)≠0 := ne_of_gt (by linarith)
  constructor
  · rw [←Real.log_div hp (by norm_num : (1/3 : ℝ)≠0)]
    unfold logZeroRatio
    congr 1
    ring
  · have he : (1 : ℝ)-(1/3-x)=2/3+x := by ring
    rw [he,show (1 : ℝ)-1/3=2/3 by norm_num]
    rw [←Real.log_div (by positivity : (2/3+x : ℝ)≠0) (by norm_num : (2/3 : ℝ)≠0)]
    unfold logOneRatio
    congr 1
    ring

theorem likelihood_term_local (b : SummableAmplitude) (t : ℝ) (n : ℕ) :
    likelihoodTerm b t n=siteOperator thirdThermalReference n
      (matrixLogRatio (siteW (1/3)) (siteW ((amplitudeProfile b t).w n))) := by
  have hh := third_log_coefficients (b.value n*regularParameter t)
    (likelihood_argument_bounds b t n).1 (likelihood_argument_bounds b t n).2
  rw [binary_log_matrix]
  change likelihoodTerm b t n=siteOperator thirdThermalReference n
    (((Real.log (1/3-b.value n*regularParameter t)-Real.log (1/3) : ℝ) : ℂ) • Matrix.single 0 0 1+
      ((Real.log (1-(1/3-b.value n*regularParameter t))-Real.log (1-1/3) : ℝ) : ℂ) • (1-Matrix.single 0 0 1))
  rw [hh.1,hh.2]
  unfold siteOperator
  rw [last_site_add,last_site_smul,last_site_smul,last_site_sub,last_site_one,
    towerPi_add,towerPi_smul,towerPi_smul]
  have hs : towerPi thirdThermalReference (1-lastSiteMatrix n (Matrix.single 0 0 1))=
      towerPi thirdThermalReference (1 : Matrix (chainIdx n) (chainIdx n) ℂ)-
        towerPi thirdThermalReference (lastSiteMatrix n (Matrix.single 0 0 1)) :=
    (towerPiLinear thirdThermalReference n).map_sub _ _
  rw [hs,towerPi_one]
  rfl

theorem matrix_log_product {ι κ : Type} [Fintype ι] [Fintype κ]
    [DecidableEq ι] [DecidableEq κ] (p q : ι → ℝ) (r z : κ → ℝ)
    (hp : ∀ i, 0<p i) (hq : ∀ i, 0<q i) (hr : ∀ j, 0<r j) (hz : ∀ j, 0<z j) :
    matrixLogRatio (productWeights p r) (productWeights q z)=
      matrixLogRatio p q ⊗ₖ 1+1 ⊗ₖ matrixLogRatio r z := by
  unfold matrixLogRatio
  rw [←Matrix.diagonal_one,←Matrix.diagonal_one,
    Matrix.diagonal_kronecker_diagonal,Matrix.diagonal_kronecker_diagonal]
  rw [Matrix.diagonal_add]
  congr 1
  funext i
  simp only [productWeights,Real.log_mul (ne_of_gt (hp _)) (ne_of_gt (hr _)),
    Real.log_mul (ne_of_gt (hq _)) (ne_of_gt (hz _)),mul_one,one_mul]
  push_cast
  ring

theorem likelihood_prefix_local (b : SummableAmplitude) (t : ℝ) (N : ℕ) :
    likelihoodPrefix b t N=towerPi thirdThermalReference
      (matrixLogRatio (towerW thirdThermalReference N) (towerW (amplitudeProfile b t) N)) := by
  induction N with
  | zero =>
    simpa [likelihoodPrefix,towerW,siteOperator,lastSiteMatrix,thirdThermalReference] using
      likelihood_term_local b t 0
  | succ N ih =>
    rw [likelihoodPrefix,Finset.sum_range_succ]
    rw [show (∑ x∈Finset.range (N+1), likelihoodTerm b t x)=likelihoodPrefix b t N from rfl]
    rw [ih,likelihood_term_local]
    have hp : towerW thirdThermalReference (N+1)=
        productWeights (towerW thirdThermalReference N) (siteW (1/3)) := rfl
    have hq : towerW (amplitudeProfile b t) (N+1)=
        productWeights (towerW (amplitudeProfile b t) N) (siteW ((amplitudeProfile b t).w (N+1))) := rfl
    rw [hp,hq]
    rw [matrix_log_product _ _ _ _ (towerW_pos _ _) (towerW_pos _ _)
      (siteW_pos (by norm_num) (by norm_num))
      (siteW_pos ((amplitudeProfile b t).pos _) ((amplitudeProfile b t).lt_one _)),towerPi_add]
    change _=towerPi thirdThermalReference (towerStep _)+
      siteOperator thirdThermalReference (N+1) _
    rw [towerPi_step]

theorem matrix_half_log_filter {ι : Type} [Fintype ι] [DecidableEq ι]
    (p q : ι → ℝ) (hp : ∀ i, 0<p i) (hq : ∀ i, 0<q i) :
    NormedSpace.exp ((1/2 : ℂ) • matrixLogRatio p q)=relativeFilter p q := by
  rw [matrixLogRatio,←Matrix.diagonal_smul,Matrix.exp_diagonal,relativeFilter]
  congr 1
  funext i
  simp only [Pi.coe_exp,Pi.smul_apply,smul_eq_mul,←Complex.exp_eq_exp_ℂ]
  have he : (1/2 : ℂ)*((Real.log (q i)-Real.log (p i) : ℝ) : ℂ)=
      ((Real.log (q i/p i)/2 : ℝ) : ℂ) := by
    rw [Real.log_div (ne_of_gt (hq i)) (ne_of_gt (hp i))]
    push_cast
    ring
  rw [he,←Complex.ofReal_exp,←Real.log_sqrt (div_pos (hq i) (hp i)).le,
    Real.exp_log (Real.sqrt_pos.mpr (div_pos (hq i) (hp i)))]

theorem likelihood_prefix_filter (b : SummableAmplitude) (t : ℝ) (N : ℕ) :
    NormedSpace.exp ((1/2 : ℂ) • likelihoodPrefix b t N)=
      towerPi thirdThermalReference
        (relativeFilter (towerW thirdThermalReference N) (towerW (amplitudeProfile b t) N)) := by
  rw [likelihood_prefix_local,←towerPi_smul,←tower_pi_exp,
    matrix_half_log_filter _ _ (towerW_pos _ _) (towerW_pos _ _)]


theorem likelihood_filter_vector (b : SummableAmplitude) (t : ℝ) :
    likelihoodFilter b t (hOmega thirdThermalReference)=amplitudeVector b t := by
  have hc : Continuous (fun A : TowerHilbert thirdThermalReference →L[ℂ] TowerHilbert thirdThermalReference =>
      A (hOmega thirdThermalReference)) := by fun_prop
  have ht := hc.continuousAt.tendsto.comp (likelihood_filter_prefix_limit b t)
  have hp : Tendsto (profileVector thirdThermalReference (amplitudeProfile b t)) atTop
      (𝓝 (likelihoodFilter b t (hOmega thirdThermalReference))) := by
    change Tendsto (fun N => towerPi thirdThermalReference
      (relativeFilter (towerW thirdThermalReference N) (towerW (amplitudeProfile b t) N))
        (hOmega thirdThermalReference)) atTop _
    simpa only [Function.comp_def,likelihood_prefix_filter] using ht
  exact tendsto_nhds_unique hp
    (global_profile_vector_tendsto _ _ (amplitude_profile_affinity_positive b t))

theorem likelihood_filter_state (b : SummableAmplitude) (t : ℝ)
    (A : TowerHilbert thirdThermalReference →L[ℂ] TowerHilbert thirdThermalReference) :
    amplitudeState b t A=omegaState thirdThermalReference
      (likelihoodFilter b t*A*likelihoodFilter b t) := by
  have hs : ContinuousLinearMap.adjoint (likelihoodFilter b t)=likelihoodFilter b t :=
    (likelihood_filter_selfadjoint b t).star_eq
  change inner ℂ (amplitudeVector b t) (A (amplitudeVector b t))=
    inner ℂ (hOmega thirdThermalReference)
      (likelihoodFilter b t (A (likelihoodFilter b t (hOmega thirdThermalReference))))
  rw [←likelihood_filter_vector b t]
  conv_rhs => rw [←hs]
  rw [ContinuousLinearMap.adjoint_inner_right,hs]

theorem likelihood_exponential_normalized (b : SummableAmplitude) (t : ℝ) :
    omegaState thirdThermalReference (NormedSpace.exp (likelihoodGenerator b t))=1 := by
  have h := (likelihood_filter_state b t 1).symm
  have h1 : amplitudeState b t 1=1 := global_profile_state_one _ _ _
  simpa only [h1,mul_one,likelihood_filter_square] using h

#print axioms likelihood_filter_vector
#print axioms likelihood_filter_state
#print axioms likelihood_exponential_normalized

#print axioms towerPiAlgHom
#print axioms tower_pi_exp
#print axioms last_site_add
#print axioms last_site_sub
#print axioms last_site_smul
#print axioms binary_log_matrix
#print axioms third_log_coefficients
#print axioms likelihood_term_local
#print axioms matrix_log_product
#print axioms likelihood_prefix_local
#print axioms matrix_half_log_filter
#print axioms likelihood_prefix_filter
end
end ChatgptAudit.Cocycle030
