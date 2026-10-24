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
import TGLExt.LikelihoodStateCovariance
import TGLExt.SummableGravityControls
import Mathlib.Analysis.InnerProductSpace.Positive
import Mathlib.Analysis.SpecialFunctions.Exponential
import Mathlib.Analysis.Calculus.Deriv.Slope
import Mathlib.Analysis.Calculus.MeanValue

set_option autoImplicit false
set_option maxHeartbeats 600000
namespace ChatgptAudit.Cocycle030
open Matrix Filter Topology Set TGLExt ChatgptAudit ChatgptAudit.Response028
  ChatgptAudit.Micro021 ChatgptAudit.Profile026 ChatgptAudit.Transport027 ChatgptAudit.Thermal025
noncomputable section

local instance (P : SiteProfile) : NormedAlgebra ℚ (TowerHilbert P →L[ℂ] TowerHilbert P) :=
  NormedAlgebra.restrictScalars ℚ ℂ _

theorem amplitude_state_norm_continuous (b : SummableAmplitude) (t : ℝ) :
    Continuous (amplitudeState b t) := by
  unfold amplitudeState globalProfileState
  fun_prop

theorem likelihood_prefix_entropy (b : SummableAmplitude) (t : ℝ) (N : ℕ) :
    amplitudeState b t (likelihoodPrefix b t N)=
      (prefixRelativeEntropy thirdThermalReference (amplitudeProfile b t) N : ℂ) := by
  rw [likelihood_prefix_local,amplitude_state_local]
  simp only [tState,matrixLogRatio,Matrix.diagonal_apply_eq,prefixRelativeEntropy,
    diagonalRelativeEntropy,Complex.ofReal_sum,Complex.ofReal_mul]

theorem likelihood_generator_entropy (b : SummableAmplitude) (t : ℝ) :
    amplitudeState b t (likelihoodGenerator b t)=(amplitudeRelativeEntropy b t : ℂ) := by
  have ht := (amplitude_state_norm_continuous b t).continuousAt.tendsto.comp
    (likelihood_prefix_tendsto b t)
  have hr := Complex.continuous_ofReal.continuousAt.tendsto.comp (amplitude_relative_tendsto b t)
  have h : Tendsto (fun N => (prefixRelativeEntropy thirdThermalReference
      (amplitudeProfile b t) N : ℂ)) atTop
        (𝓝 (amplitudeState b t (likelihoodGenerator b t))) := by
    simpa only [Function.comp_def,likelihood_prefix_entropy] using ht
  exact tendsto_nhds_unique h hr

theorem likelihood_entropy_nonnegative (b : SummableAmplitude) (t : ℝ) :
    0≤(amplitudeState b t (likelihoodGenerator b t)).re := by
  rw [likelihood_generator_entropy,Complex.ofReal_re]
  exact amplitude_relative_nonnegative b t

theorem likelihood_entropy_bound (b : SummableAmplitude) (t : ℝ) :
    (amplitudeState b t (likelihoodGenerator b t)).re≤
      (9/2)*(regularParameter t)^2*amplitudeSquareMass b := by
  rw [likelihood_generator_entropy,Complex.ofReal_re]
  exact amplitude_relative_bound b t

theorem likelihood_filter_positive (b : SummableAmplitude) (t : ℝ) :
    (likelihoodFilter b t).IsPositive := by
  let Q := NormedSpace.exp ((1/4 : ℂ) • likelihoodGenerator b t)
  have hQ : star Q=Q := by
    simp [Q,NormedSpace.star_exp,star_smul,(likelihood_generator_selfadjoint b t).star_eq]
  have he : star Q*Q=likelihoodFilter b t := by
    rw [hQ]
    dsimp [Q,likelihoodFilter]
    rw [←NormedSpace.exp_add_of_commute (Commute.refl _),←add_smul]
    norm_num
  rw [←he]
  exact ContinuousLinearMap.isPositive_adjoint_comp_self Q

theorem likelihood_filter_invertible (b : SummableAmplitude) (t : ℝ) :
    IsUnit (likelihoodFilter b t) :=
  NormedSpace.isUnit_exp _

theorem zero_amplitude_generator (t : ℝ) : likelihoodGenerator zeroAmplitude t=0 := by
  simp [likelihoodGenerator,likelihoodTerm,zeroAmplitude,site_likelihood_zero]

theorem zero_amplitude_cocycle (t s : ℝ) : likelihoodCocycle zeroAmplitude t s=1 := by
  simp [likelihoodCocycle,zero_amplitude_generator]

theorem generator_zero_forces_reference (b : SummableAmplitude) (t : ℝ)
    (h : likelihoodGenerator b t=0) : amplitudeState b t=omegaState thirdThermalReference := by
  funext A
  rw [likelihood_filter_state]
  have hr : likelihoodFilter b t=1 := by simp [likelihoodFilter,h]
  rw [hr,one_mul,mul_one]

theorem geometric_generator_nonzero (t : ℝ) (ht : t≠0) :
    likelihoodGenerator geometricAmplitude t≠0 := by
  intro h
  exact geometric_state_not_reference t ht (generator_zero_forces_reference _ _ h)


def phaseQuadratic (b : SummableAmplitude) (t s : ℝ) :
    TowerHilbert thirdThermalReference →L[ℂ] TowerHilbert thirdThermalReference :=
  star (likelihoodCocycle b t s-1)*(likelihoodCocycle b t s-1)

theorem phase_quadratic_positive (b : SummableAmplitude) (t s : ℝ) :
    (phaseQuadratic b t s).IsPositive :=
  ContinuousLinearMap.isPositive_adjoint_comp_self _

theorem phase_quadratic_formula (b : SummableAmplitude) (t s : ℝ) :
    phaseQuadratic b t s=2*1-likelihoodCocycle b t s-star (likelihoodCocycle b t s) := by
  have h := (Unitary.mem_iff.mp (likelihood_cocycle_unitary b t s)).1
  rw [two_mul]
  simp only [phaseQuadratic,star_sub,star_one,sub_mul,mul_sub,one_mul,mul_one,h]
  abel

theorem phase_quadratic_read (b : SummableAmplitude) (t s : ℝ)
    (x : TowerHilbert thirdThermalReference) :
    (inner ℂ x (phaseQuadratic b t s x)).re=‖(likelihoodCocycle b t s-1) x‖^2 := by
  rw [phaseQuadratic,mul_apply_eq_comp,ContinuousLinearMap.star_eq_adjoint,
    ContinuousLinearMap.adjoint_inner_right]
  exact (norm_sq_eq_re_inner (𝕜 := ℂ) ((likelihoodCocycle b t s-1) x)).symm

theorem phase_quadratic_zero (b : SummableAmplitude) (t : ℝ) : phaseQuadratic b t 0=0 := by
  simp [phaseQuadratic,likelihood_cocycle_zero]

theorem phase_quadratic_reference (b : SummableAmplitude) (s : ℝ) : phaseQuadratic b 0 s=0 := by
  simp [phaseQuadratic,likelihood_cocycle_reference]

theorem likelihood_cocycle_derivative_zero (b : SummableAmplitude) (t : ℝ) :
    HasDerivAt (likelihoodCocycle b t) (Complex.I • likelihoodGenerator b t) 0 := by
  have h := hasDerivAt_exp_smul_const
    (Complex.I • likelihoodGenerator b t) (0 : ℝ)
  have he : (fun s : ℝ => NormedSpace.exp (s • (Complex.I • likelihoodGenerator b t)))=
      likelihoodCocycle b t := by
    funext s
    rw [←smul_assoc,Complex.real_smul]
    rfl
  rw [he] at h
  simpa only [zero_smul,NormedSpace.exp_zero,one_mul] using h

theorem phase_quadratic_modular_limit (b : SummableAmplitude) (t : ℝ) :
    Tendsto (fun s : ℝ => (s^2)⁻¹ • phaseQuadratic b t s) (𝓝[≠] 0)
      (𝓝 (likelihoodGenerator b t*likelihoodGenerator b t)) := by
  have h : Tendsto (fun s : ℝ => s⁻¹ • (likelihoodCocycle b t s-1)) (𝓝[≠] 0)
      (𝓝 (Complex.I • likelihoodGenerator b t)) := by
    have he : (fun s : ℝ => s⁻¹ • (likelihoodCocycle b t s-1))=
        slope (likelihoodCocycle b t) 0 := by
      funext s
      simp [slope,likelihood_cocycle_zero]
    rw [he]
    exact hasDerivAt_iff_tendsto_slope.mp (likelihood_cocycle_derivative_zero b t)
  have hh := h.star.mul h
  have he (s : ℝ) :
      star (s⁻¹ • (likelihoodCocycle b t s-1))*(s⁻¹ • (likelihoodCocycle b t s-1))=
        (s^2)⁻¹ • phaseQuadratic b t s := by
    simp [phaseQuadratic,star_smul,smul_smul,pow_two,_root_.mul_inv_rev]
  have hz : star (Complex.I • likelihoodGenerator b t)*(Complex.I • likelihoodGenerator b t)=
      likelihoodGenerator b t*likelihoodGenerator b t := by
    simp [star_smul,(likelihood_generator_selfadjoint b t).star_eq,smul_smul,Complex.I_mul_I]
  simpa only [he,hz] using hh


theorem likelihood_cocycle_derivative (b : SummableAmplitude) (t s : ℝ) :
    HasDerivAt (likelihoodCocycle b t)
      (likelihoodCocycle b t s*(Complex.I • likelihoodGenerator b t)) s := by
  have h := hasDerivAt_exp_smul_const (Complex.I • likelihoodGenerator b t) s
  have he : (fun r : ℝ => NormedSpace.exp (r • (Complex.I • likelihoodGenerator b t)))=
      likelihoodCocycle b t := by
    funext r
    rw [←smul_assoc,Complex.real_smul]
    rfl
  rw [he,congrFun he s] at h
  exact h

theorem likelihood_phase_norm_bound (b : SummableAmplitude) (t s : ℝ) :
    ‖likelihoodCocycle b t s-1‖≤‖likelihoodGenerator b t‖*|s| := by
  have hd (r : ℝ) (_ : r∈(Set.univ : Set ℝ)) :=
    (likelihood_cocycle_derivative b t r).hasDerivWithinAt (s := Set.univ)
  have hn (r : ℝ) (_ : r∈(Set.univ : Set ℝ)) :
      ‖likelihoodCocycle b t r*(Complex.I • likelihoodGenerator b t)‖≤
        ‖likelihoodGenerator b t‖ := by
    rw [CStarRing.norm_mem_unitary_mul _ (likelihood_cocycle_unitary b t r),
      norm_smul,Complex.norm_I,one_mul]
  have h := Convex.norm_image_sub_le_of_norm_hasDerivWithin_le hd hn (convex_univ : Convex ℝ (Set.univ : Set ℝ))
    (Set.mem_univ (0 : ℝ)) (Set.mem_univ s)
  simpa only [likelihood_cocycle_zero,sub_zero,Real.norm_eq_abs] using h

theorem phase_quadratic_norm_bound (b : SummableAmplitude) (t s : ℝ) :
    ‖phaseQuadratic b t s‖ ≤ s^2*‖likelihoodGenerator b t‖^2 := by
  have h := likelihood_phase_norm_bound b t s
  calc
    ‖phaseQuadratic b t s‖=‖likelihoodCocycle b t s-1‖^2 := by
      simpa only [phaseQuadratic,pow_two] using
        (CStarRing.norm_star_mul_self (x := likelihoodCocycle b t s-1))
    _≤(‖likelihoodGenerator b t‖*|s|)^2 := by
      nlinarith [norm_nonneg (likelihoodCocycle b t s-1),
        mul_nonneg (norm_nonneg (likelihoodGenerator b t)) (abs_nonneg s)]
    _=s^2*‖likelihoodGenerator b t‖^2 := by rw [mul_pow,sq_abs]; ring

theorem phase_quadratic_fourth_order_bound (b : SummableAmplitude) (t s : ℝ) :
    ‖phaseQuadratic b t s‖≤36*s^2*(amplitudeMass b)^2*t^4 := by
  have hL : ‖likelihoodGenerator b t‖≤6*t^2*amplitudeMass b :=
    (likelihood_generator_bound b t).trans
      (mul_le_mul_of_nonneg_right
        (mul_le_mul_of_nonneg_left (regular_parameter_le_square t) (by norm_num))
          (amplitude_mass_nonnegative b))
  calc
    ‖phaseQuadratic b t s‖ ≤ s^2*‖likelihoodGenerator b t‖^2 := phase_quadratic_norm_bound b t s
    _ ≤ s^2*(6*t^2*amplitudeMass b)^2 := by
      apply mul_le_mul_of_nonneg_left _ (sq_nonneg s)
      nlinarith [norm_nonneg (likelihoodGenerator b t),
        mul_nonneg (mul_nonneg (by norm_num : (0 : ℝ)≤6) (sq_nonneg t))
          (amplitude_mass_nonnegative b)]
    _=36*s^2*(amplitudeMass b)^2*t^4 := by ring

#print axioms likelihood_cocycle_derivative
#print axioms likelihood_phase_norm_bound
#print axioms phase_quadratic_norm_bound
#print axioms phase_quadratic_fourth_order_bound

#print axioms phaseQuadratic
#print axioms phase_quadratic_positive
#print axioms phase_quadratic_formula
#print axioms phase_quadratic_read
#print axioms phase_quadratic_zero
#print axioms phase_quadratic_reference
#print axioms likelihood_cocycle_derivative_zero
#print axioms phase_quadratic_modular_limit

#print axioms amplitude_state_norm_continuous
#print axioms likelihood_prefix_entropy
#print axioms likelihood_generator_entropy
#print axioms likelihood_entropy_nonnegative
#print axioms likelihood_entropy_bound
#print axioms likelihood_filter_positive
#print axioms likelihood_filter_invertible
#print axioms zero_amplitude_generator
#print axioms zero_amplitude_cocycle
#print axioms generator_zero_forces_reference
#print axioms geometric_generator_nonzero
end
end ChatgptAudit.Cocycle030
