-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_025 (06/09/2026), transposta em 06/09/2026
-- Lote 024..026: a perturbacao de GIBBS realizada no mesmo Hilbert da torre (estado fiel,
--   normalizado, distinto da orbita modular; resposta quadratica; calor/fonte por normalizacao);
--   o LIMITE TERMICO: para perfil constante nao tracial a preparacao NAO tem limite em norma
--   (nao-Cauchy) e o acoplamento da torre e ilimitado; corte com escala escolhida; AFINIDADE:
--   criterio exato (Cauchy <=> afinidade-limite > 0), estado global no Hilbert original, fiel e
--   ciclico; perfil gradual (muda em infinitos sitios, ainda fiel). Estatuto [REAL / INPUT / OPEN]:
--   selecao fisica, area, H3 dinamico, dimensao/assinatura, globalizacao e a classificacao geral
--   dos estados normais (disjuncao) seguem INPUT/OPEN — a bancada NAO promoveu nao-Cauchy a teorema
--   geral de disjuncao nem importou Kakutani.
-- Auditoria da gerencia (sessao d554e796, 06/09/2026): hashes 100%; manifestos 202/206/220;
--   3/3 auditores da bancada exit 0; recompilacao INDEPENDENTE 22/22, axiomas no trio; guarda de
--   colisao estatica no ROOT; enunciados lidos. Transposicao MECANICA (cabecalho + prefixo TGLExt.).
-- NAO move gate; nao e fisica; NOT_FALSIFIED nunca e CONFIRMED; CONFIRMADA proibido.
-- ---------------------------------------------------------------------
import TGLExt.GibbsAffinity

set_option autoImplicit false
set_option maxHeartbeats 16000000
namespace ChatgptAudit.Thermal025
open Matrix Filter Topology Set TGLExt ChatgptAudit.Thermal024
noncomputable section

theorem tower_gibbs_omega_overlap (P : SiteProfile) (N : ℕ) (s : ℝ) :
    inner ℂ (hOmega P) (towerGibbsVector P N s)=(gibbsAffinity (towerW P N) s:ℂ) := by
  change omegaState P (towerPi P (gibbsFilter (towerW P N) s))=_
  rw [omegaState_pi]
  simp only [tState,gibbsFilter,Matrix.diagonal_apply_eq,←Complex.ofReal_mul,←Complex.ofReal_sum,
    gibbs_filter_affinity _ (towerW_pos P N)]

theorem tower_gibbs_affinity_uniform (P : SiteProfile) (q : ℝ) (hP : ∀ n, P.w n=q) (s : ℝ) (N : ℕ) :
    gibbsAffinity (towerW P N) s=(gibbsAffinity (siteW q) s)^(N+1) := by
  induction N with
  | zero =>
    change gibbsAffinity (siteW (P.w 0)) s=(gibbsAffinity (siteW q) s)^1
    rw [hP,pow_one]
  | succ N ih =>
    change gibbsAffinity (productWeights (towerW P N) (siteW (P.w (N+1)))) s=_
    rw [gibbs_affinity_product _ _ (towerW_pos P N) (siteW_pos (P.pos _) (P.lt_one _)),
      ih,hP]
    exact (pow_succ _ (N+1)).symm

theorem tower_gibbs_uniform_overlap (P : SiteProfile) (q : ℝ) (hP : ∀ n, P.w n=q) (s : ℝ) (N : ℕ) :
    inner ℂ (hOmega P) (towerGibbsVector P N s)=(((gibbsAffinity (siteW q) s)^(N+1):ℝ):ℂ) := by
  rw [tower_gibbs_omega_overlap,tower_gibbs_affinity_uniform P q hP]

theorem tower_step_diagonal {N : ℕ} (f : chainIdx N → ℂ) :
    towerStep (Matrix.diagonal f)=Matrix.diagonal (fun x : chainIdx (N+1) => f x.1) := by
  unfold towerStep
  rw [←Matrix.diagonal_one,Matrix.diagonal_kronecker_diagonal]
  simp only [mul_one]

theorem tower_local_vectors_inner (P : SiteProfile) {L N : ℕ} (hLN : L≤N)
    (a : Matrix (chainIdx L) (chainIdx L) ℂ) (b : Matrix (chainIdx N) (chainIdx N) ℂ) :
    inner ℂ (towerPi P a (hOmega P)) (towerPi P b (hOmega P))=
      tInner P N (tPush hLN a) b := by
  rw [towerPi_omega,towerPi_omega,UniformSpace.Completion.inner_coe,towerPre_inner_def,
    innerPre_tof_at hLN (le_refl N),tPush_self]

theorem tower_gibbs_successive_overlap (P : SiteProfile) (N : ℕ) (s : ℝ) :
    inner ℂ (towerGibbsVector P N s) (towerGibbsVector P (N+1) s)=
      (gibbsAffinity (siteW (P.w (N+1))) s:ℂ) := by
  unfold towerGibbsVector
  rw [tower_local_vectors_inner P (Nat.le_succ N),tPush_succ (le_refl N) (Nat.le_succ N),tPush_self]
  rw [tInner,←towerStep_star,gibbs_filter_self_adjoint]
  simp only [tState,gibbsFilter,tower_step_diagonal,Matrix.diagonal_mul_diagonal,
    Matrix.diagonal_apply_eq,Fintype.sum_prod_type]
  have hamp : ∀ i j,
      Real.sqrt (gibbsWeights (towerW P (N+1)) s (i,j)/towerW P (N+1) (i,j))=
        Real.sqrt (gibbsWeights (towerW P N) s i/towerW P N i)*
        Real.sqrt (gibbsWeights (siteW (P.w (N+1))) s j/siteW (P.w (N+1)) j) := by
    intro i j
    exact gibbs_amplitude_product _ _ (towerW_pos P N) (siteW_pos (P.pos _) (P.lt_one _)) s i j
  have he : ∀ i j,
      (towerW P (N+1) (i,j):ℂ)*
        ((Real.sqrt (gibbsWeights (towerW P N) s i/towerW P N i):ℂ)*
          (Real.sqrt (gibbsWeights (towerW P (N+1)) s (i,j)/towerW P (N+1) (i,j)):ℂ))=
      (((towerW P N i*(Real.sqrt (gibbsWeights (towerW P N) s i/towerW P N i))^2)*
        (siteW (P.w (N+1)) j*Real.sqrt
          (gibbsWeights (siteW (P.w (N+1))) s j/siteW (P.w (N+1)) j)):ℝ):ℂ) := by
    intro i j
    rw [hamp]
    rw [show towerW P (N+1) (i,j)=towerW P N i*siteW (P.w (N+1)) j from rfl]
    push_cast
    ring
  simp only [he,gibbs_filter_weighted_square _ (towerW_pos P N),←Complex.ofReal_sum,
    ←Finset.mul_sum,←Finset.sum_mul,gibbs_weights_normalized _ (towerW_pos P N),one_mul,
    gibbs_filter_affinity _ (siteW_pos (P.pos _) (P.lt_one _))]

theorem tower_gibbs_successive_distance (P : SiteProfile) (N : ℕ) (s : ℝ) :
    ‖towerGibbsVector P N s-towerGibbsVector P (N+1) s‖^2=
      2-2*gibbsAffinity (siteW (P.w (N+1))) s := by
  rw [norm_sub_sq (𝕜 := ℂ),tower_gibbs_vector_norm,tower_gibbs_vector_norm,tower_gibbs_successive_overlap]
  change (1:ℝ)^2-2*gibbsAffinity (siteW (P.w (N+1))) s+1^2=_
  ring

theorem nontracial_site_affinity_lt_one (P : SiteProfile) (q : ℝ) (hP : ∀ n, P.w n=q)
    (s : ℝ) (hS : s≠0) (hq : q≠1/2) : gibbsAffinity (siteW q) s<1 := by
  have h0 : 0<q := by rw [←hP 0]; exact P.pos 0
  have h1 : q<1 := by rw [←hP 0]; exact P.lt_one 0
  apply gibbs_affinity_lt_one _ (siteW_pos h0 h1) (siteW_sum q) s hS
  refine ⟨0,1,?_⟩
  change q≠1-q
  intro he
  apply hq
  linarith

theorem thermal_uniform_overlap_tends_zero (P : SiteProfile) (q : ℝ) (hP : ∀ n, P.w n=q)
    (s : ℝ) (hS : s≠0) (hq : q≠1/2) :
    Tendsto (fun N : ℕ => (inner ℂ (hOmega P) (towerGibbsVector P N s)).re) atTop (𝓝 0) := by
  have h0 : 0<q := by rw [←hP 0]; exact P.pos 0
  have h1 : q<1 := by rw [←hP 0]; exact P.lt_one 0
  have hp := gibbs_affinity_positive (siteW q) (siteW_pos h0 h1) s
  have hl := nontracial_site_affinity_lt_one P q hP s hS hq
  have ht := (tendsto_pow_atTop_nhds_zero_of_lt_one hp.le hl).comp (tendsto_add_atTop_nat 1)
  simpa only [tower_gibbs_uniform_overlap P q hP,Complex.ofReal_re,Function.comp_def] using ht

theorem thermal_vectors_no_norm_limit (P : SiteProfile) (q : ℝ) (hP : ∀ n, P.w n=q)
    (s : ℝ) (hS : s≠0) (hq : q≠1/2) (v : TowerHilbert P) :
    ¬Tendsto (fun N : ℕ => towerGibbsVector P N s) atTop (𝓝 v) := by
  intro ht
  have hsuc := ht.comp (tendsto_add_atTop_nat 1)
  have hd := (ht.sub hsuc).norm.pow 2
  have hz : Tendsto (fun _N : ℕ => 2-2*gibbsAffinity (siteW q) s) atTop (𝓝 0) := by
    simpa only [Function.comp_def,tower_gibbs_successive_distance,hP,sub_self,norm_zero,zero_pow (by decide : 2≠0)] using hd
  have he : 2-2*gibbsAffinity (siteW q) s=0 := tendsto_nhds_unique tendsto_const_nhds hz
  have hlt := nontracial_site_affinity_lt_one P q hP s hS hq
  linarith

theorem thermal_vectors_not_cauchy (P : SiteProfile) (q : ℝ) (hP : ∀ n, P.w n=q)
    (s : ℝ) (hS : s≠0) (hq : q≠1/2) :
    ¬CauchySeq (fun N : ℕ => towerGibbsVector P N s) := by
  intro hc
  obtain ⟨v,hv⟩ := cauchySeq_tendsto_of_complete hc
  exact thermal_vectors_no_norm_limit P q hP s hS hq v hv

#print axioms tower_gibbs_omega_overlap
#print axioms tower_gibbs_affinity_uniform
#print axioms tower_gibbs_uniform_overlap
#print axioms tower_step_diagonal
#print axioms tower_local_vectors_inner
#print axioms tower_gibbs_successive_overlap
#print axioms tower_gibbs_successive_distance
#print axioms nontracial_site_affinity_lt_one
#print axioms thermal_uniform_overlap_tends_zero
#print axioms thermal_vectors_no_norm_limit
#print axioms thermal_vectors_not_cauchy
end
end ChatgptAudit.Thermal025
