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
import TGLExt.TailNotCyclic
import TGLExt.CentralizerDensity

set_option autoImplicit false
set_option maxHeartbeats 1200000

namespace ChatgptAudit.Angular034
open TGLExt ChatgptAudit ChatgptAudit.Cocycle030
noncomputable section

theorem site_zero_eq_site_mark (P : SiteProfile) (n : ℕ) :
    siteZeroProjection P n = siteMark P n := rfl

theorem site_zero_state (P : SiteProfile) (n : ℕ) :
    omegaState P (siteZeroProjection P n) = (P.w n : ℂ) := by
  rw [site_zero_eq_site_mark, siteMark_state]

theorem site_mark_mem_tail (P : SiteProfile) (N m : ℕ) (h : N ≤ m) :
    siteMark P m ∈ chainTailClosure P N := by
  have hlocal : siteMark P m ∈ chainLocalAlgebra P (Set.Ici N) := by
    apply StarAlgebra.subset_adjoin
    exact ⟨m, h, Matrix.single (0 : Fin 2) 0 (1 : ℂ), rfl⟩
  change siteMark P m ∈ StarSubalgebra.centralizer ℂ
    ((StarSubalgebra.centralizer ℂ
      (chainLocalAlgebra P (Set.Ici N) : Set (TowerHilbert P →L[ℂ] TowerHilbert P))) :
      Set (TowerHilbert P →L[ℂ] TowerHilbert P))
  rw [StarSubalgebra.mem_centralizer_iff]
  intro A hA
  have hstarA : star A ∈ StarSubalgebra.centralizer ℂ
      (chainLocalAlgebra P (Set.Ici N) : Set (TowerHilbert P →L[ℂ] TowerHilbert P)) :=
    star_mem hA
  change A ∈ StarSubalgebra.centralizer ℂ
    (chainLocalAlgebra P (Set.Ici N) : Set (TowerHilbert P →L[ℂ] TowerHilbert P)) at hA
  rw [StarSubalgebra.mem_centralizer_iff] at hA hstarA
  exact ⟨(hA _ hlocal).1.symm, (hstarA _ hlocal).1.symm⟩

theorem site_mark_tail_factorization (P : SiteProfile) (n : ℕ)
    (A : TowerHilbert P →L[ℂ] TowerHilbert P)
    (hA : A ∈ chainTailClosure P (n + 1)) :
    omegaState P (siteMark P n * A) = (P.w n : ℂ) * omegaState P A := by
  have he := expectation_bimodular n
    (lastSiteMatrix n (Matrix.single (0 : Fin 2) 0 (1 : ℂ))) 1 A
    (chain_tail_mem_factor _ hA)
  simp only [towerPi_one, mul_one] at he
  change towerExpectation P n (siteMark P n * A) =
    siteMark P n * towerExpectation P n A at he
  rw [← expectation_preserves_state n (siteMark P n * A), he,
    tail_prefix_expectation_scalar n A hA, mul_smul_comm, mul_one]
  change inner ℂ (hOmega P) (omegaState P A • siteMark P n (hOmega P)) = _
  rw [inner_smul_right]
  change omegaState P A * omegaState P (siteMark P n) = _
  rw [siteMark_state, mul_comm]

theorem site_zero_product_state_lt (P : SiteProfile) {n m : ℕ} (h : n < m) :
    omegaState P (siteZeroProjection P n * siteZeroProjection P m) =
      (P.w n : ℂ) * (P.w m : ℂ) := by
  rw [site_zero_eq_site_mark, site_zero_eq_site_mark,
    site_mark_tail_factorization P n (siteMark P m)
      (site_mark_mem_tail P (n + 1) m (Nat.succ_le_of_lt h)), siteMark_state]

theorem site_zero_product_state (P : SiteProfile) {n m : ℕ} (h : n ≠ m) :
    omegaState P (siteZeroProjection P n * siteZeroProjection P m) =
      (P.w n : ℂ) * (P.w m : ℂ) := by
  rcases lt_or_gt_of_ne h with hlt | hgt
  · exact site_zero_product_state_lt P hlt
  · rw [(site_zero_commute P n m).eq, site_zero_product_state_lt P hgt, mul_comm]

def centeredSiteVector (P : SiteProfile) (n : ℕ) : TowerHilbert P :=
  siteZeroProjection P n (hOmega P) - (P.w n : ℂ) • hOmega P

theorem site_zero_omega_inner (P : SiteProfile) (n : ℕ) :
    inner ℂ (siteZeroProjection P n (hOmega P)) (hOmega P) = (P.w n : ℂ) := by
  rw [site_zero_eq_site_mark]
  have h := omega_product_inner (P := P) (siteMark P n) 1
  simp only [mul_one, siteMark_star, one_apply_eq_self] at h
  rw [← h, siteMark_state]

theorem centered_site_omega_inner (P : SiteProfile) (n : ℕ) :
    inner ℂ (hOmega P) (centeredSiteVector P n) = 0 := by
  have he : inner ℂ (hOmega P) (siteZeroProjection P n (hOmega P)) = (P.w n : ℂ) :=
    site_zero_state P n
  simp only [centeredSiteVector, inner_sub_right, inner_smul_right,
    he, hOmega_inner_self, mul_one, sub_self]

theorem centered_site_inner_self (P : SiteProfile) (n : ℕ) :
    inner ℂ (centeredSiteVector P n) (centeredSiteVector P n) =
      ((P.w n * (1 - P.w n) : ℝ) : ℂ) := by
  have hee : inner ℂ (siteZeroProjection P n (hOmega P))
      (siteZeroProjection P n (hOmega P)) = (P.w n : ℂ) := by
    rw [site_zero_eq_site_mark]
    have h := omega_product_inner (P := P) (siteMark P n) (siteMark P n)
    rw [siteMark_square, siteMark_star, siteMark_state] at h
    exact h.symm
  have heo := site_zero_omega_inner P n
  have hoe : inner ℂ (hOmega P) (siteZeroProjection P n (hOmega P)) = (P.w n : ℂ) :=
    site_zero_state P n
  simp only [centeredSiteVector, inner_sub_left, inner_sub_right,
    inner_smul_left, inner_smul_right, Complex.conj_ofReal,
    hee, heo, hoe, hOmega_inner_self]
  push_cast
  ring

theorem centered_site_inner_distinct (P : SiteProfile) {n m : ℕ} (h : n ≠ m) :
    inner ℂ (centeredSiteVector P n) (centeredSiteVector P m) = 0 := by
  have hem : inner ℂ (siteZeroProjection P n (hOmega P))
      (siteZeroProjection P m (hOmega P)) = (P.w n : ℂ) * (P.w m : ℂ) := by
    have hp := omega_product_inner (P := P)
      (siteZeroProjection P n) (siteZeroProjection P m)
    rw [(site_zero_projection P n).isSelfAdjoint.star_eq,
      site_zero_product_state P h] at hp
    exact hp.symm
  have hno := site_zero_omega_inner P n
  have hom : inner ℂ (hOmega P) (siteZeroProjection P m (hOmega P)) = (P.w m : ℂ) :=
    site_zero_state P m
  simp only [centeredSiteVector, inner_sub_left, inner_sub_right,
    inner_smul_left, inner_smul_right, Complex.conj_ofReal,
    hem, hno, hom, hOmega_inner_self]
  ring

theorem centered_site_norm_sq (P : SiteProfile) (n : ℕ) :
    ‖centeredSiteVector P n‖ ^ 2 = P.w n * (1 - P.w n) := by
  rw [norm_sq_eq_re_inner (𝕜 := ℂ), centered_site_inner_self]
  rfl

theorem centered_site_variance_pos (P : SiteProfile) (n : ℕ) :
    0 < P.w n * (1 - P.w n) :=
  mul_pos (P.pos n) (sub_pos.mpr (P.lt_one n))

theorem centered_site_ne_zero (P : SiteProfile) (n : ℕ) :
    centeredSiteVector P n ≠ 0 := by
  intro h
  have hn := centered_site_norm_sq P n
  rw [h, norm_zero, zero_pow (by decide : 2 ≠ 0)] at hn
  have hp := centered_site_variance_pos P n
  linarith

#print axioms site_zero_eq_site_mark
#print axioms site_zero_state
#print axioms site_mark_mem_tail
#print axioms site_mark_tail_factorization
#print axioms site_zero_product_state_lt
#print axioms site_zero_product_state
#print axioms centeredSiteVector
#print axioms site_zero_omega_inner
#print axioms centered_site_omega_inner
#print axioms centered_site_inner_self
#print axioms centered_site_inner_distinct
#print axioms centered_site_norm_sq
#print axioms centered_site_variance_pos
#print axioms centered_site_ne_zero
end
end ChatgptAudit.Angular034
