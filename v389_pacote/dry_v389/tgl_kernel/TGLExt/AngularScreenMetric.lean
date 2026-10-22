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
import TGLExt.SitePhaseCovariance
import TGLExt.ScreenAreaCalculus

set_option autoImplicit false
set_option maxHeartbeats 800000

namespace ChatgptAudit.Angular034
open Matrix TGLExt ChatgptAudit ChatgptAudit.Thermal025
noncomputable section

/-- The centered phase direction in the GNS Hilbert space. -/
def phaseSiteVector (P : SiteProfile) (n : ℕ) : TowerHilbert P :=
  Complex.I • centeredSiteVector P n

/-- Real Gram matrix of two centered phase directions; no spacetime identification. -/
def angularScreenGram (P : SiteProfile) (n m : ℕ) : ScreenMatrix :=
  !![(inner ℂ (phaseSiteVector P n) (phaseSiteVector P n)).re,
      (inner ℂ (phaseSiteVector P n) (phaseSiteVector P m)).re;
     (inner ℂ (phaseSiteVector P m) (phaseSiteVector P n)).re,
      (inner ℂ (phaseSiteVector P m) (phaseSiteVector P m)).re]

/-- The area density of the specified pair of GNS phase directions. -/
def angularScreenArea (P : SiteProfile) (n m : ℕ) : ℝ :=
  screenArea (angularScreenGram P n m)

theorem phase_site_inner (P : SiteProfile) (n m : ℕ) :
    inner ℂ (phaseSiteVector P n) (phaseSiteVector P m)=
      inner ℂ (centeredSiteVector P n) (centeredSiteVector P m) := by
  simp [phaseSiteVector,inner_smul_left,inner_smul_right,←mul_assoc]

theorem phase_site_omega_inner (P : SiteProfile) (n : ℕ) :
    inner ℂ (hOmega P) (phaseSiteVector P n)=0 := by
  simp only [phaseSiteVector,inner_smul_right,centered_site_omega_inner,mul_zero]

theorem angular_screen_gram_distinct (P : SiteProfile) {n m : ℕ} (h : n≠m) :
    angularScreenGram P n m=
      !![P.w n*(1-P.w n),0;0,P.w m*(1-P.w m)] := by
  simp only [angularScreenGram,phase_site_inner,centered_site_inner_self,
    centered_site_inner_distinct P h,centered_site_inner_distinct P h.symm,
    Complex.ofReal_re,Complex.zero_re]

theorem angular_screen_determinant (P : SiteProfile) {n m : ℕ} (h : n≠m) :
    (angularScreenGram P n m).det=
      (P.w n*(1-P.w n))*(P.w m*(1-P.w m)) := by
  rw [angular_screen_gram_distinct P h,Matrix.det_fin_two]
  simp

theorem angular_screen_determinant_positive (P : SiteProfile) {n m : ℕ} (h : n≠m) :
    0<(angularScreenGram P n m).det := by
  rw [angular_screen_determinant P h]
  exact mul_pos (centered_site_variance_pos P n) (centered_site_variance_pos P m)

theorem angular_screen_area_positive (P : SiteProfile) {n m : ℕ} (h : n≠m) :
    0<angularScreenArea P n m :=
  screen_area_positive _ (angular_screen_determinant_positive P h)

theorem angular_screen_gram_repeated (P : SiteProfile) (n : ℕ) :
    angularScreenGram P n n=
      !![P.w n*(1-P.w n),P.w n*(1-P.w n);
         P.w n*(1-P.w n),P.w n*(1-P.w n)] := by
  simp only [angularScreenGram,phase_site_inner,centered_site_inner_self,Complex.ofReal_re]

theorem angular_screen_determinant_repeated (P : SiteProfile) (n : ℕ) :
    (angularScreenGram P n n).det=0 := by
  rw [angular_screen_gram_repeated,Matrix.det_fin_two]
  simp

theorem angular_screen_area_repeated (P : SiteProfile) (n : ℕ) :
    angularScreenArea P n n=0 := by
  simp only [angularScreenArea,screenArea,angular_screen_determinant_repeated,Real.sqrt_zero]

theorem reference_angular_screen_area :
    angularScreenArea thirdThermalReference 0 1=2/9 := by
  rw [angularScreenArea,screenArea,angular_screen_determinant thirdThermalReference (by decide)]
  norm_num [thirdThermalReference,Real.sqrt_div]

theorem reference_repeated_angular_screen_area :
    angularScreenArea thirdThermalReference 0 0=0 :=
  angular_screen_area_repeated thirdThermalReference 0

#print axioms phaseSiteVector
#print axioms angularScreenGram
#print axioms angularScreenArea
#print axioms phase_site_inner
#print axioms phase_site_omega_inner
#print axioms angular_screen_gram_distinct
#print axioms angular_screen_determinant
#print axioms angular_screen_determinant_positive
#print axioms angular_screen_area_positive
#print axioms angular_screen_gram_repeated
#print axioms angular_screen_determinant_repeated
#print axioms angular_screen_area_repeated
#print axioms reference_angular_screen_area
#print axioms reference_repeated_angular_screen_area

end
end ChatgptAudit.Angular034
