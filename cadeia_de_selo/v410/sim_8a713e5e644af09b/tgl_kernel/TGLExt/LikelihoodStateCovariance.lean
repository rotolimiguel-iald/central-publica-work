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
import TGLExt.LikelihoodPreparedState
import TGLExt.Ergodicity

set_option autoImplicit false
set_option maxHeartbeats 2400000
namespace ChatgptAudit.Cocycle030
open Matrix Filter Topology Set TGLExt ChatgptAudit ChatgptAudit.Response028
  ChatgptAudit.Profile026 ChatgptAudit.Transport027 ChatgptAudit.Thermal025
open scoped Matrix.Norms.Operator
noncomputable section

local instance (P : SiteProfile) : NormedAlgebra ℚ (TowerHilbert P →L[ℂ] TowerHilbert P) :=
  NormedAlgebra.restrictScalars ℚ ℂ _

theorem matrix_cocycle_log {ι : Type} [Fintype ι] [DecidableEq ι]
    (p q : ι → ℝ) (hp : ∀ i, 0<p i) (hq : ∀ i, 0<q i) (s : ℝ) :
    cocycle (rhoD q) (rhoD p) s=NormedSpace.exp (((s : ℂ)*Complex.I) • matrixLogRatio p q) := by
  rw [cocycle_of_commute _ _ (by
    rw [logRho_diagonal q hq,logRho_diagonal p hp]
    exact Matrix.commute_diagonal _ _) s,logRho_diagonal q hq,logRho_diagonal p hp]
  congr 2
  ext i j
  by_cases hij : i=j
  · subst j; simp [matrixLogRatio]
  · simp [matrixLogRatio,hij]

theorem likelihood_prefix_is_finite_cocycle (b : SummableAmplitude) (t s : ℝ) (N : ℕ) :
    likelihoodPrefixCocycle b t s N=towerPi thirdThermalReference
      (cocycle (rhoD (towerW (amplitudeProfile b t) N)) (rhoD (towerW thirdThermalReference N)) s) := by
  rw [likelihoodPrefixCocycle,likelihood_prefix_local,←towerPi_smul,←tower_pi_exp,
    ←matrix_cocycle_log _ _ (towerW_pos _ _) (towerW_pos _ _)]

theorem finite_cocycle_intertwines {ι : Type} [Fintype ι] [DecidableEq ι]
    (q p a : Matrix ι ι ℂ) (s : ℝ) :
    cocycle q p s*sigma p s a*star (cocycle q p s)=sigma q s a := by
  change cocycle q p s*sigma p s a*(cocycle q p s)ᴴ=sigma q s a
  rw [cocycle_conjTranspose]
  simp only [cocycle,sigma]
  calc
    modPow q s*modPow p (-s)*(modPow p s*a*modPow p (-s))*
        (modPow p s*modPow q (-s))=
      modPow q s*((modPow p (-s)*modPow p s)*a*
        (modPow p (-s)*modPow p s))*modPow q (-s) := by simp only [mul_assoc]
    _=modPow q s*a*modPow q (-s) := by simp only [modPow_neg_mul,one_mul,mul_one]

theorem flow_level_is_sigma (P : SiteProfile) (s : ℝ) (N : ℕ)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    flowLevel P s N a=sigma (rhoD (towerW P N)) s a := by
  ext i j
  rw [sigma_diagonal_apply _ (towerW_pos _ _)]
  unfold flowLevel modularPhase
  congr 2
  push_cast
  ring

theorem likelihood_prefix_local_covariance (b : SummableAmplitude) (t s : ℝ)
    {L N : ℕ} (h : L≤N) (a : Matrix (chainIdx L) (chainIdx L) ℂ) :
    likelihoodPrefixCocycle b t s N*
      modularConjugation thirdThermalReference s (towerPi thirdThermalReference a)*
        star (likelihoodPrefixCocycle b t s N)=
      towerPi thirdThermalReference (flowLevel (amplitudeProfile b t) s L a) := by
  rw [←towerPi_compat (P := thirdThermalReference) h a,modularConjugation_local,
    likelihood_prefix_is_finite_cocycle,flow_level_is_sigma]
  change towerPi thirdThermalReference _*towerPi thirdThermalReference _*
    ContinuousLinearMap.adjoint (towerPi thirdThermalReference _)=_
  rw [←towerPi_star,←towerPi_mul,←towerPi_mul]
  change towerPi thirdThermalReference
    (cocycle _ _ s*sigma _ s (tPush h a)*star (cocycle _ _ s))=_
  rw [finite_cocycle_intertwines,←flow_level_is_sigma,flowLevel_push,towerPi_compat]

theorem likelihood_local_covariance (b : SummableAmplitude) (t s : ℝ)
    (L : ℕ) (a : Matrix (chainIdx L) (chainIdx L) ℂ) :
    likelihoodCocycle b t s*
      modularConjugation thirdThermalReference s (towerPi thirdThermalReference a)*
        star (likelihoodCocycle b t s)=
      towerPi thirdThermalReference (flowLevel (amplitudeProfile b t) s L a) := by
  have hc := likelihood_prefix_cocycle_limit b t s
  have ht := (hc.mul (tendsto_const_nhds
    (x := modularConjugation thirdThermalReference s (towerPi thirdThermalReference a)))).mul hc.star
  have he : (fun N => likelihoodPrefixCocycle b t s N*
      modularConjugation thirdThermalReference s (towerPi thirdThermalReference a)*
        star (likelihoodPrefixCocycle b t s N)) =ᶠ[atTop]
      fun _ => towerPi thirdThermalReference (flowLevel (amplitudeProfile b t) s L a) := by
    filter_upwards [eventually_ge_atTop L] with N hN
    exact likelihood_prefix_local_covariance b t s hN a
  exact tendsto_nhds_unique ht (tendsto_const_nhds.congr' he.symm)

theorem conjugations_eq_on_factor (P : SiteProfile)
    (U Ui V Vi : TowerHilbert P →L[ℂ] TowerHilbert P)
    (hUUi : U*Ui=1) (hUiU : Ui*U=1)
    (hVVi : V*Vi=1) (hViV : Vi*V=1)
    (hloc : ∀ (N : ℕ) (a : Matrix (chainIdx N) (chainIdx N) ℂ),
      U*towerPi P a*Ui=V*towerPi P a*Vi)
    (x : TowerHilbert P →L[ℂ] TowerHilbert P) (hx : x∈theFactorObject P) :
    U*x*Ui=V*x*Vi := by
  have hc (y : TowerHilbert P →L[ℂ] TowerHilbert P) (hy : y∈towerImage P) :
      y*(Vi*U)=(Vi*U)*y := by
    obtain ⟨N,a,rfl⟩ := hy
    symm
    calc
      Vi*U*towerPi P a=Vi*(U*towerPi P a*Ui)*U := by
        simp only [mul_assoc,hUiU,mul_one]
      _=Vi*(V*towerPi P a*Vi)*U := by rw [hloc]
      _=towerPi P a*(Vi*U) := by simp only [←mul_assoc,hViV,one_mul]
  have hm : Vi*U∈StarSubalgebra.centralizer ℂ (towerImage P) := by
    rw [StarSubalgebra.mem_centralizer_iff]
    intro y hy
    exact ⟨hc y hy,hc (star y) (towerImage_star_closed hy)⟩
  have hx' : x∈StarSubalgebra.centralizer ℂ
      ((StarSubalgebra.centralizer ℂ (towerImage P) :
        StarSubalgebra ℂ (TowerHilbert P →L[ℂ] TowerHilbert P)) :
          Set (TowerHilbert P →L[ℂ] TowerHilbert P)) := hx
  rw [StarSubalgebra.mem_centralizer_iff] at hx'
  have he : (Vi*U)*x=x*(Vi*U) := (hx' (Vi*U) hm).1
  calc
    U*x*Ui=V*((Vi*U)*x)*Ui := by simp only [←mul_assoc,hVVi,one_mul]
    _=V*(x*(Vi*U))*Ui := by rw [he]
    _=V*x*Vi := by simp only [mul_assoc,hUUi,mul_one]


theorem isometry_conjugation_mul (P : SiteProfile)
    (e : TowerHilbert P ≃ₗᵢ[ℂ] TowerHilbert P)
    (A : TowerHilbert P →L[ℂ] TowerHilbert P) :
    e.conjStarAlgEquiv A=e.toContinuousLinearEquiv.toContinuousLinearMap*A*
      e.symm.toContinuousLinearEquiv.toContinuousLinearMap := rfl

theorem conjugations_eq_on_factor_unitary (P : SiteProfile)
    (e f : TowerHilbert P ≃ₗᵢ[ℂ] TowerHilbert P)
    (u : TowerHilbert P →L[ℂ] TowerHilbert P) (hu : u∈unitary _)
    (hloc : ∀ (N : ℕ) (a : Matrix (chainIdx N) (chainIdx N) ℂ),
      u*e.conjStarAlgEquiv (towerPi P a)*star u=f.conjStarAlgEquiv (towerPi P a))
    (A : TowerHilbert P →L[ℂ] TowerHilbert P) (hA : A∈theFactorObject P) :
    u*e.conjStarAlgEquiv A*star u=f.conjStarAlgEquiv A := by
  let E := e.toContinuousLinearEquiv.toContinuousLinearMap
  let Ei := e.symm.toContinuousLinearEquiv.toContinuousLinearMap
  let F := f.toContinuousLinearEquiv.toContinuousLinearMap
  let Fi := f.symm.toContinuousLinearEquiv.toContinuousLinearMap
  have hEEi : E*Ei=1 := by
    ext x
    exact e.apply_symm_apply x
  have hEiE : Ei*E=1 := by
    ext x
    exact e.symm_apply_apply x
  have hFFi : F*Fi=1 := by
    ext x
    exact f.apply_symm_apply x
  have hFiF : Fi*F=1 := by
    ext x
    exact f.symm_apply_apply x
  have hu1 : star u*u=1 := (Unitary.mem_iff.mp hu).1
  have hu2 : u*star u=1 := (Unitary.mem_iff.mp hu).2
  have hleft : (u*E)*(Ei*star u)=1 := by
    calc
      (u*E)*(Ei*star u)=u*(E*Ei)*star u := by simp only [mul_assoc]
      _=1 := by rw [hEEi,mul_one,hu2]
  have hright : (Ei*star u)*(u*E)=1 := by
    calc
      (Ei*star u)*(u*E)=Ei*(star u*u)*E := by simp only [mul_assoc]
      _=1 := by rw [hu1,mul_one,hEiE]
  have hl (N : ℕ) (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
      (u*E)*towerPi P a*(Ei*star u)=F*towerPi P a*Fi := by
    have h := hloc N a
    simp only [isometry_conjugation_mul,mul_assoc] at h
    exact h
  have h := conjugations_eq_on_factor P (u*E) (Ei*star u) F Fi
    hleft hright hFFi hFiF hl A hA
  simpa only [isometry_conjugation_mul,mul_assoc] using h

theorem likelihood_global_covariance (b : SummableAmplitude) (t s : ℝ)
    (A : TowerHilbert thirdThermalReference →L[ℂ] TowerHilbert thirdThermalReference)
    (hA : A∈theFactorObject thirdThermalReference) :
    likelihoodCocycle b t s*modularConjugation thirdThermalReference s A*
      star (likelihoodCocycle b t s)=
    profileFlowConjugation thirdThermalReference (amplitudeProfile b t)
      (amplitude_profile_affinity_positive b t) s A := by
  apply conjugations_eq_on_factor_unitary thirdThermalReference
    (modularFlowUnitary thirdThermalReference s)
    (profileModularFlow thirdThermalReference (amplitudeProfile b t)
      (amplitude_profile_affinity_positive b t) s)
    (likelihoodCocycle b t s) (likelihood_cocycle_unitary b t s) _ A hA
  intro N a
  change likelihoodCocycle b t s*
      modularConjugation thirdThermalReference s (towerPi thirdThermalReference a)*
        star (likelihoodCocycle b t s)=
    profileFlowConjugation thirdThermalReference (amplitudeProfile b t)
      (amplitude_profile_affinity_positive b t) s (towerPi thirdThermalReference a)
  rw [likelihood_local_covariance,profile_flow_local_conjugation]

#print axioms isometry_conjugation_mul
#print axioms conjugations_eq_on_factor_unitary
#print axioms likelihood_global_covariance

#print axioms matrix_cocycle_log
#print axioms likelihood_prefix_is_finite_cocycle
#print axioms finite_cocycle_intertwines
#print axioms flow_level_is_sigma
#print axioms likelihood_prefix_local_covariance
#print axioms likelihood_local_covariance
#print axioms conjugations_eq_on_factor
end
end ChatgptAudit.Cocycle030
