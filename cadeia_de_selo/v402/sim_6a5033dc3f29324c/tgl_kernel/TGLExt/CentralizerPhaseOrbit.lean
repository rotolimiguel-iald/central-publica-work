-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_034 (06/09/2026), transposta em 06/09/2026
-- Lote 034: AREA ANGULAR DE DOIS SITIOS e teste operacional — orbita de fase do centralizador
--   (CentralizerPhaseOrbit), covariancia de fase por sitio (SitePhaseCovariance), metrica angular da tela
--   (AngularScreenMetric) e a OBSERVABILIDADE da area angular (AngularAreaObservability). Estatuto
--   [REAL / DERIVED / INPUT / OPEN]: construcao de dois sitios na familia especificada; a selecao fisica,
--   escala, dinamica e a lei geral de area seguem INPUT/OPEN (ver a propria entrega).
-- Auditoria da gerencia (sessao d554e796, 06/09/2026): hashes 12/12; manifesto 278/278; auditor exit 0;
--   recompilacao INDEPENDENTE 4/4 (apos a regra 3, contra o kernel com a 033), axiomas no trio; guarda de
--   colisao; enunciados lidos. Transposicao: cabecalho + prefixo TGLExt. + regra 3 (instancias locais nomeadas).
-- NAO move gate; nao e fisica; NOT_FALSIFIED nunca e CONFIRMED; CONFIRMADA proibido.
-- ---------------------------------------------------------------------
import TGLExt.DensityStateUniqueness
import Mathlib.Analysis.Calculus.Deriv.Mul
import Mathlib.Analysis.Calculus.Deriv.Comp
import Mathlib.Analysis.Normed.Operator.Bilinear

set_option autoImplicit false
set_option maxHeartbeats 1200000
namespace ChatgptAudit.Angular034
open Filter Topology Set TGLExt ChatgptAudit.Cocycle030 ChatgptAudit.Density033
noncomputable section

local instance inst_CentralizerPhaseOrbit_1 (P : SiteProfile) : NormedAlgebra ℚ (TowerHilbert P →L[ℂ] TowerHilbert P) :=
  NormedAlgebra.restrictScalars ℚ ℂ _

def boundedPhase (P : SiteProfile) (A : TowerHilbert P →L[ℂ] TowerHilbert P) (s : ℝ) :
    TowerHilbert P →L[ℂ] TowerHilbert P :=
  NormedSpace.exp (((s : ℂ)*Complex.I) • A)

theorem bounded_phase_zero (P : SiteProfile) (A : TowerHilbert P →L[ℂ] TowerHilbert P) :
    boundedPhase P A 0=1 := by simp [boundedPhase]

theorem bounded_phase_unitary (P : SiteProfile)
    (A : TowerHilbert P →L[ℂ] TowerHilbert P) (hA : IsSelfAdjoint A) (s : ℝ) :
    boundedPhase P A s∈unitary _ :=
  NormedSpace.exp_mem_unitary_of_mem_skewAdjoint
    (hA.smul_mem_skewAdjoint
      (by simp : star ((s : ℂ)*Complex.I)= -((s : ℂ)*Complex.I)))

theorem bounded_phase_centralizer (P : SiteProfile)
    (A : TowerHilbert P →L[ℂ] TowerHilbert P) (hA : A∈omegaCentralizer P) (s : ℝ) :
    boundedPhase P A s∈omegaCentralizer P :=
  omega_centralizer_exp_mem P (omega_centralizer_smul P ((s : ℂ)*Complex.I) hA)

theorem centralizer_unitary_preserves_state (P : SiteProfile)
    (U : TowerHilbert P →L[ℂ] TowerHilbert P) (hU : U∈omegaCentralizer P)
    (hu : U∈unitary _) (A : TowerHilbert P →L[ℂ] TowerHilbert P)
    (hA : A∈theFactorObject P) :
    omegaState P (star U*A*U)=omegaState P A := by
  have hm : U∈(theFactorObject P).toStarSubalgebra := hU.1
  have hs : star U∈(theFactorObject P).toStarSubalgebra := star_mem hm
  calc
    omegaState P (star U*A*U)=omegaState P (U*(star U*A)) :=
      (hU.2 (star U*A) ((theFactorObject P).mul_mem hs hA)).symm
    _=omegaState P A := by
      rw [←mul_assoc,(Unitary.mem_iff.mp hu).2,one_mul]

theorem bounded_phase_derivative_zero (P : SiteProfile)
    (A : TowerHilbert P →L[ℂ] TowerHilbert P) :
    HasDerivAt (boundedPhase P A) (Complex.I • A) 0 := by
  have h := hasDerivAt_exp_smul_const (Complex.I • A) (0 : ℝ)
  have he : (fun s : ℝ => NormedSpace.exp (s • (Complex.I • A)))=boundedPhase P A := by
    funext s
    rw [←smul_assoc,Complex.real_smul]
    rfl
  rw [he] at h
  simpa only [zero_smul,NormedSpace.exp_zero,one_mul] using h

theorem bounded_phase_derivative (P : SiteProfile)
    (A : TowerHilbert P →L[ℂ] TowerHilbert P) (s : ℝ) :
    HasDerivAt (boundedPhase P A) (boundedPhase P A s*(Complex.I • A)) s := by
  have h := hasDerivAt_exp_smul_const (Complex.I • A) s
  have he : (fun r : ℝ => NormedSpace.exp (r • (Complex.I • A)))=boundedPhase P A := by
    funext r
    rw [←smul_assoc,Complex.real_smul]
    rfl
  rw [he] at h
  have hv : NormedSpace.exp (s • (Complex.I • A))=boundedPhase P A s := congrFun he s
  simpa only [hv] using h

theorem bounded_phase_differentiable (P : SiteProfile)
    (A : TowerHilbert P →L[ℂ] TowerHilbert P) : Differentiable ℝ (boundedPhase P A) :=
  fun s => (bounded_phase_derivative P A s).differentiableAt

theorem bounded_phase_vector_derivative_zero (P : SiteProfile)
    (A : TowerHilbert P →L[ℂ] TowerHilbert P) (x : TowerHilbert P) :
    HasDerivAt (fun s : ℝ => boundedPhase P A s x) (Complex.I • A x) 0 := by
  exact ((ContinuousLinearMap.apply ℂ (TowerHilbert P) x).restrictScalars ℝ).hasFDerivAt.comp_hasDerivAt
    0 (bounded_phase_derivative_zero P A)

def horizontalComponent (P : SiteProfile) (v : TowerHilbert P) : TowerHilbert P :=
  v-(inner ℂ (hOmega P) v) • hOmega P

theorem horizontal_component_orthogonal (P : SiteProfile) (v : TowerHilbert P) :
    inner ℂ (hOmega P) (horizontalComponent P v)=0 := by
  simp only [horizontalComponent,inner_sub_right,inner_smul_right,hOmega_inner_self,mul_one,sub_self]

theorem horizontal_phase_derivative (P : SiteProfile)
    (A : TowerHilbert P →L[ℂ] TowerHilbert P) :
    horizontalComponent P (Complex.I • A (hOmega P))=
      Complex.I • (A (hOmega P)-omegaState P A • hOmega P) := by
  simp only [horizontalComponent,inner_smul_right,smul_sub,smul_smul,omegaState]

def twoPhaseOrbit (P : SiteProfile) (n m : ℕ) (s t : ℝ) :
    TowerHilbert P →L[ℂ] TowerHilbert P :=
  boundedPhase P (siteZeroProjection P n) s * boundedPhase P (siteZeroProjection P m) t

def twoPhaseVector (P : SiteProfile) (n m : ℕ) (s t : ℝ) : TowerHilbert P :=
  twoPhaseOrbit P n m s t (hOmega P)

theorem two_phase_unitary (P : SiteProfile) (n m : ℕ) (s t : ℝ) :
    twoPhaseOrbit P n m s t∈unitary _ :=
  mul_mem
    (bounded_phase_unitary P _ (site_zero_projection P n).isSelfAdjoint s)
    (bounded_phase_unitary P _ (site_zero_projection P m).isSelfAdjoint t)

theorem two_phase_centralizer (P : SiteProfile) (n m : ℕ) (s t : ℝ) :
    twoPhaseOrbit P n m s t∈omegaCentralizer P :=
  omega_centralizer_mul P
    (bounded_phase_centralizer P _ (site_zero_mem_centralizer P n) s)
    (bounded_phase_centralizer P _ (site_zero_mem_centralizer P m) t)

theorem two_phase_state_invariant (P : SiteProfile) (n m : ℕ) (s t : ℝ)
    (A : TowerHilbert P →L[ℂ] TowerHilbert P) (hA : A∈theFactorObject P) :
    omegaState P (star (twoPhaseOrbit P n m s t)*A*twoPhaseOrbit P n m s t)=omegaState P A :=
  centralizer_unitary_preserves_state P _ (two_phase_centralizer P n m s t)
    (two_phase_unitary P n m s t) A hA

theorem two_phase_vector_origin (P : SiteProfile) (n m : ℕ) :
    twoPhaseVector P n m 0 0=hOmega P := by
  simp [twoPhaseVector,twoPhaseOrbit,bounded_phase_zero]

theorem two_phase_vector_norm (P : SiteProfile) (n m : ℕ) (s t : ℝ) :
    ‖twoPhaseVector P n m s t‖=1 := by
  rw [twoPhaseVector,ContinuousLinearMap.norm_map_of_mem_unitary (two_phase_unitary P n m s t)]
  exact hOmega_norm

theorem two_phase_distance_preserved (P : SiteProfile) (n m : ℕ) (s t : ℝ)
    (x y : TowerHilbert P) :
    ‖twoPhaseOrbit P n m s t x-twoPhaseOrbit P n m s t y‖=‖x-y‖ := by
  rw [←map_sub]
  exact ContinuousLinearMap.norm_map_of_mem_unitary (two_phase_unitary P n m s t) (x-y)

theorem two_phase_first_derivative (P : SiteProfile) (n m : ℕ) :
    HasDerivAt (fun s : ℝ => twoPhaseVector P n m s 0)
      (Complex.I • siteZeroProjection P n (hOmega P)) 0 := by
  simpa only [twoPhaseVector,twoPhaseOrbit,bounded_phase_zero,mul_one] using
    bounded_phase_vector_derivative_zero P (siteZeroProjection P n) (hOmega P)

theorem two_phase_second_derivative (P : SiteProfile) (n m : ℕ) :
    HasDerivAt (fun t : ℝ => twoPhaseVector P n m 0 t)
      (Complex.I • siteZeroProjection P m (hOmega P)) 0 := by
  simpa only [twoPhaseVector,twoPhaseOrbit,bounded_phase_zero,one_mul] using
    bounded_phase_vector_derivative_zero P (siteZeroProjection P m) (hOmega P)

theorem two_phase_vector_differentiable (P : SiteProfile) (n m : ℕ) :
    Differentiable ℝ (fun q : ℝ×ℝ => twoPhaseVector P n m q.1 q.2) := by
  exact ((ContinuousLinearMap.apply ℂ (TowerHilbert P) (hOmega P)).restrictScalars ℝ).differentiable.comp
    (((bounded_phase_differentiable P (siteZeroProjection P n)).comp differentiable_fst).mul
      ((bounded_phase_differentiable P (siteZeroProjection P m)).comp differentiable_snd))

#print axioms boundedPhase
#print axioms bounded_phase_zero
#print axioms bounded_phase_unitary
#print axioms bounded_phase_centralizer
#print axioms centralizer_unitary_preserves_state
#print axioms bounded_phase_derivative_zero
#print axioms bounded_phase_derivative
#print axioms bounded_phase_differentiable
#print axioms bounded_phase_vector_derivative_zero
#print axioms horizontalComponent
#print axioms horizontal_component_orthogonal
#print axioms horizontal_phase_derivative
#print axioms twoPhaseOrbit
#print axioms twoPhaseVector
#print axioms two_phase_unitary
#print axioms two_phase_centralizer
#print axioms two_phase_state_invariant
#print axioms two_phase_vector_origin
#print axioms two_phase_vector_norm
#print axioms two_phase_distance_preserved
#print axioms two_phase_first_derivative
#print axioms two_phase_second_derivative
#print axioms two_phase_vector_differentiable
end
end ChatgptAudit.Angular034
