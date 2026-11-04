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
import TGLExt.CentralizerPhaseOrbit
import TGLExt.AngularScreenMetric

set_option autoImplicit false
set_option maxHeartbeats 1000000
namespace ChatgptAudit.Angular034
open Matrix TGLExt ChatgptAudit ChatgptAudit.Cocycle030 ChatgptAudit.Thermal025
noncomputable section

theorem first_horizontal_tangent (P : SiteProfile) (n m : ℕ) :
    horizontalComponent P (deriv (fun s : ℝ => twoPhaseVector P n m s 0) 0)=
      phaseSiteVector P n := by
  rw [(two_phase_first_derivative P n m).deriv,horizontal_phase_derivative,site_zero_state]
  rfl

theorem second_horizontal_tangent (P : SiteProfile) (n m : ℕ) :
    horizontalComponent P (deriv (fun t : ℝ => twoPhaseVector P n m 0 t) 0)=
      phaseSiteVector P m := by
  rw [(two_phase_second_derivative P n m).deriv,horizontal_phase_derivative,site_zero_state]
  rfl

theorem phase_vector_state_form (P : SiteProfile) (n m : ℕ) (s t : ℝ)
    (A : TowerHilbert P →L[ℂ] TowerHilbert P) :
    inner ℂ (twoPhaseVector P n m s t) (A (twoPhaseVector P n m s t))=
      omegaState P (star (twoPhaseOrbit P n m s t)*A*twoPhaseOrbit P n m s t) := by
  rw [mul_assoc,omega_product_inner,star_star]
  rfl

def phaseRestrictedState (P : SiteProfile) (n m : ℕ) (s t : ℝ) :
    (theFactorObject P) → ℂ :=
  fun A => inner ℂ (twoPhaseVector P n m s t) ((A : TowerHilbert P →L[ℂ] TowerHilbert P)
    (twoPhaseVector P n m s t))

theorem phase_restricted_state_eq (P : SiteProfile) (n m : ℕ) (s t : ℝ) :
    phaseRestrictedState P n m s t=
      (fun A : theFactorObject P => omegaState P (A : TowerHilbert P →L[ℂ] TowerHilbert P)) := by
  funext A
  exact (phase_vector_state_form P n m s t A.val).trans
    (two_phase_state_invariant P n m s t A.val A.property)

def phaseReading (P : SiteProfile) (n m : ℕ) (A : theFactorObject P) (s t : ℝ) : ℝ :=
  (phaseRestrictedState P n m s t A).re

theorem phase_reading_constant (P : SiteProfile) (n m : ℕ) (A : theFactorObject P) (s t : ℝ) :
    phaseReading P n m A s t=(omegaState P A.val).re := by
  exact congrArg Complex.re (congrFun (phase_restricted_state_eq P n m s t) A)

theorem phase_reading_first_derivative (P : SiteProfile) (n m : ℕ)
    (A : theFactorObject P) (s t : ℝ) :
    HasDerivAt (fun r : ℝ => phaseReading P n m A r t) 0 s := by
  have hf : (fun r : ℝ => phaseReading P n m A r t)=fun _ => (omegaState P A.val).re :=
    funext (fun r => phase_reading_constant P n m A r t)
  rw [hf]
  exact hasDerivAt_const s _

theorem phase_reading_second_derivative (P : SiteProfile) (n m : ℕ)
    (A : theFactorObject P) (s t : ℝ) :
    HasDerivAt (fun r : ℝ => phaseReading P n m A s r) 0 t := by
  have hf : (fun r : ℝ => phaseReading P n m A s r)=fun _ => (omegaState P A.val).re :=
    funext (fun r => phase_reading_constant P n m A s r)
  rw [hf]
  exact hasDerivAt_const t _

def observablePhaseJacobian (P : SiteProfile) (n m : ℕ) {k : ℕ}
    (A : Fin k → theFactorObject P) (s t : ℝ) : Matrix (Fin k) (Fin 2) ℝ :=
  fun i j => if j=0 then deriv (fun r : ℝ => phaseReading P n m (A i) r t) s
    else deriv (fun r : ℝ => phaseReading P n m (A i) s r) t

theorem observable_phase_jacobian_zero (P : SiteProfile) (n m : ℕ) {k : ℕ}
    (A : Fin k → theFactorObject P) (s t : ℝ) :
    observablePhaseJacobian P n m A s t=0 := by
  ext i j
  dsimp [observablePhaseJacobian]
  split
  · exact (phase_reading_first_derivative P n m (A i) s t).deriv
  · exact (phase_reading_second_derivative P n m (A i) s t).deriv

def observablePhaseGram (P : SiteProfile) (n m : ℕ) {k : ℕ}
    (A : Fin k → theFactorObject P) (G : Matrix (Fin k) (Fin k) ℝ) (s t : ℝ) : ScreenMatrix :=
  (observablePhaseJacobian P n m A s t)ᵀ*G*observablePhaseJacobian P n m A s t

theorem observable_phase_gram_zero (P : SiteProfile) (n m : ℕ) {k : ℕ}
    (A : Fin k → theFactorObject P) (G : Matrix (Fin k) (Fin k) ℝ) (s t : ℝ) :
    observablePhaseGram P n m A G s t=0 := by
  simp only [observablePhaseGram,observable_phase_jacobian_zero,Matrix.transpose_zero,
    Matrix.zero_mul,Matrix.mul_zero]

theorem observable_phase_area_zero (P : SiteProfile) (n m : ℕ) {k : ℕ}
    (A : Fin k → theFactorObject P) (G : Matrix (Fin k) (Fin k) ℝ) (s t : ℝ) :
    screenArea (observablePhaseGram P n m A G s t)=0 := by
  rw [observable_phase_gram_zero,screenArea,Matrix.det_fin_two]
  norm_num

theorem observable_phase_area_not_angular (P : SiteProfile) {n m : ℕ} (h : n≠m) {k : ℕ}
    (A : Fin k → theFactorObject P) (G : Matrix (Fin k) (Fin k) ℝ) :
    screenArea (observablePhaseGram P n m A G 0 0)≠angularScreenArea P n m := by
  rw [observable_phase_area_zero]
  exact ne_of_lt (angular_screen_area_positive P h)

theorem observable_phase_gram_not_angular (P : SiteProfile) {n m : ℕ} (h : n≠m) {k : ℕ}
    (A : Fin k → theFactorObject P) (G : Matrix (Fin k) (Fin k) ℝ) :
    observablePhaseGram P n m A G 0 0≠angularScreenGram P n m := by
  intro he
  exact observable_phase_area_not_angular P h A G (congrArg screenArea he)

theorem reference_phase_area_split {k : ℕ} (A : Fin k → theFactorObject thirdThermalReference)
    (G : Matrix (Fin k) (Fin k) ℝ) :
    angularScreenArea thirdThermalReference 0 1=2/9 ∧
    angularScreenArea thirdThermalReference 0 0=0 ∧
    screenArea (observablePhaseGram thirdThermalReference 0 1 A G 0 0)=0 :=
  ⟨reference_angular_screen_area,reference_repeated_angular_screen_area,
    observable_phase_area_zero thirdThermalReference 0 1 A G 0 0⟩

#print axioms first_horizontal_tangent
#print axioms second_horizontal_tangent
#print axioms phase_vector_state_form
#print axioms phaseRestrictedState
#print axioms phase_restricted_state_eq
#print axioms phaseReading
#print axioms phase_reading_constant
#print axioms phase_reading_first_derivative
#print axioms phase_reading_second_derivative
#print axioms observablePhaseJacobian
#print axioms observable_phase_jacobian_zero
#print axioms observablePhaseGram
#print axioms observable_phase_gram_zero
#print axioms observable_phase_area_zero
#print axioms observable_phase_area_not_angular
#print axioms observable_phase_gram_not_angular
#print axioms reference_phase_area_split
end
end ChatgptAudit.Angular034
