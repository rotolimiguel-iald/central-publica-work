-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_024 (06/09/2026), transposta em 06/09/2026
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
import TGLExt.GibbsMatterBridge

set_option autoImplicit false
set_option maxHeartbeats 12000000
namespace ChatgptAudit.Thermal024
open Matrix Filter Topology Set TGLExt ChatgptAudit.Micro021 ChatgptAudit.Coherent023
  ChatgptAudit.Flow019 ChatgptAudit.Flow020 ChatgptAudit.Screen014
open scoped ContDiff Matrix.Norms.Elementwise
noncomputable section
variable {ι : Type} [Fintype ι] [Nonempty ι]

omit [Nonempty ι] in
theorem gibbs_weights_tracial (p : ι → ℝ) (hs : ∑ i, p i=1)
    (ht : ∀ i j, p i=p j) (s : ℝ) (i : ι) : gibbsWeights p s i=p i := by
  have he : ∀ j, modularScore p j=modularScore p i :=
    fun j => congrArg (fun r => -Real.log r) (ht j i)
  have hZ : gibbsPartition p s=Real.exp (-s*modularScore p i) := by
    simp only [gibbsPartition,gibbsAtom,he,←Finset.sum_mul,hs,one_mul]
  unfold gibbsWeights gibbsAtom
  rw [hZ]
  exact mul_div_cancel_right₀ _ (Real.exp_ne_zero _)

theorem binary_gibbs_variance_positive (q : ℝ) (h0 : 0<q) (h1 : q<1) (hne : q≠1/2) :
    0 < modularVariance (siteW q) := by
  apply modular_variance_positive _ (siteW_pos h0 h1) (siteW_sum q)
  refine ⟨0,1,?_⟩
  change q≠1-q
  intro he
  apply hne
  linarith

theorem tower_first_site_variance_positive (P : SiteProfile) (hne : P.w 0≠1/2) :
    0 < modularVariance (towerW P 0) :=
  binary_gibbs_variance_positive (P.w 0) (P.pos 0) (P.lt_one 0) hne

def towerGibbsReadWeights (P : SiteProfile) (N : ℕ) (s : ℝ) (i : chainIdx N) : ℝ :=
  (towerGibbsState P N s (towerPi P (Matrix.diagonal (Pi.single i (1:ℂ))))).re

theorem tower_gibbs_read_weights (P : SiteProfile) (N : ℕ) (s : ℝ) :
    towerGibbsReadWeights P N s=gibbsWeights (towerW P N) s := by
  funext i
  simp only [towerGibbsReadWeights,tower_gibbs_local_projection,Complex.ofReal_re]

theorem tower_gibbs_entropy_quadratic (P : SiteProfile) (N : ℕ) (frequency : ℝ) :
    Tendsto (fun t => (finiteEntropy (towerGibbsReadWeights P N ((frequency*t)^2))-
      finiteEntropy (towerGibbsReadWeights P N 0))/t^2) (𝓝[<] 0)
      (𝓝 (-frequency^2*modularVariance (towerW P N))) := by
  have h0 : gibbsWeights (towerW P N) 0=towerW P N := funext (gibbs_weights_zero _ (towerW_sum P N))
  simpa only [tower_gibbs_read_weights,h0,quadraticGibbsWeights] using
    quadratic_gibbs_entropy_limit (towerW P N) (towerW_pos P N) (towerW_sum P N) frequency

theorem tower_gibbs_modular_quadratic (P : SiteProfile) (N : ℕ) (frequency : ℝ) :
    Tendsto (fun t =>
      ((towerGibbsState P N ((frequency*t)^2) (towerPi P (diagonalModularGenerator (towerW P N)))).re-
       (towerGibbsState P N 0 (towerPi P (diagonalModularGenerator (towerW P N)))).re)/t^2)
      (𝓝[<] 0) (𝓝 (-frequency^2*modularVariance (towerW P N))) := by
  have he : ∀ s, gibbsMean (towerW P N) s-gibbsMean (towerW P N) 0=
      modularIncrement (towerW P N) (gibbsWeights (towerW P N) s) := by
    intro s
    rw [gibbs_mean_zero _ (towerW_sum P N)]
    simp only [gibbsMean,modularMean,modularIncrement,modularScore,sub_mul,Finset.sum_sub_distrib]
  simpa only [tower_gibbs_local_generator,Complex.ofReal_re,he,quadraticGibbsWeights] using
    quadratic_gibbs_modular_limit (towerW P N) (towerW_pos P N) (towerW_sum P N) frequency

theorem gibbs_weights_not_modular_orbit (P : SiteProfile) (N : ℕ) (frequency : ℝ)
    (hf : frequency≠0) (hv : 0 < modularVariance (towerW P N)) :
    ¬∀ t, quadraticGibbsWeights (towerW P N) frequency t=modularLocalWeights P N t := by
  intro he
  have hl := quadratic_gibbs_entropy_limit (towerW P N) (towerW_pos P N) (towerW_sum P N) frequency
  simp only [he,modular_local_weights_eq,sub_self,zero_div] at hl
  have hz : -frequency^2*modularVariance (towerW P N)=0 :=
    tendsto_nhds_unique hl tendsto_const_nhds
  exact (mul_ne_zero (neg_ne_zero.mpr (pow_ne_zero 2 hf)) (ne_of_gt hv)) hz

theorem tower_gibbs_not_modular_orbit (P : SiteProfile) (N : ℕ) (frequency : ℝ)
    (hf : frequency≠0) (hv : 0 < modularVariance (towerW P N)) :
    ¬∀ t (a : Matrix (chainIdx N) (chainIdx N) ℂ),
      towerGibbsState P N ((frequency*t)^2) (towerPi P a)=modularLocalState P N t a := by
  intro he
  apply gibbs_weights_not_modular_orbit P N frequency hf hv
  intro t
  funext i
  have hh := congrArg Complex.re (he t (Matrix.diagonal (Pi.single i (1:ℂ))))
  simpa only [tower_gibbs_local_projection,Complex.ofReal_re,modularLocalWeights,
    quadraticGibbsWeights] using hh

def gibbsFlatMatter (p : ι → ℝ) : TensorField4 :=
  frameCovectorStress flatSolder flatSolder constantTimeCovector (gibbsCoupling p)

omit [Nonempty ι] in
theorem gibbs_flat_matter_smooth (p : ι → ℝ) : SmoothMatrixOn univ (gibbsFlatMatter p) :=
  frame_covector_stress_smooth univ flatSolder flatSolder constantTimeCovector (gibbsCoupling p)
    flat_solder_smooth flat_solder_smooth constant_time_smooth

omit [Nonempty ι] in
theorem gibbs_flat_matter_conserved (p : ι → ℝ) : ∀ x∈(univ : Set Coordinate4), ∀ j,
    tensorFieldDivergence (inverseFrameMetricField flatSolder) (frameLeviCivita flatSolder flatSolder)
      (gibbsFlatMatter p) x j=0 :=
  frame_covector_stress_conserved univ isOpen_univ flatSolder flatSolder constantTimeCovector
    (gibbsCoupling p) flat_solder_inverse flat_solder_inverse flat_solder_smooth
    flat_solder_smooth constant_time_smooth constant_time_closed constant_time_wave

omit [Nonempty ι] in
theorem gibbs_flat_null_value (p : ι → ℝ) :
    tensorQuad (gibbsFlatMatter p 0) horizonControlDirection=gibbsCoupling p := by
  change tensorQuad (covectorStress _ _ _ _) horizonControlDirection=_
  rw [covector_stress_null _ _ _ _ _ flat_control_null]
  norm_num [covectorRead,constantTimeCovector,timeCovector,horizonControlDirection,dotProduct,
    Fin.sum_univ_four,Matrix.cons_val_two,Matrix.cons_val_three]

theorem gibbs_flat_heat_matching (p : ι → ℝ) (hp : ∀ i, 0<p i) (hs : ∑ i, p i=1) :
    Tendsto (fun t => microscopicHeatError
      (quadraticGibbsCurve p hp hs (covectorRead (constantTimeCovector 0) horizonControlDirection))
      1 (constructedHeat flatConstructedScreen (gibbsFlatMatter p) 1 isOpen_univ
        (frame_metric_smooth univ flatSolder flat_solder_smooth)
        (fun i j => (gibbs_flat_matter_smooth p i j).differentiableOn (by simp))) t/t^2)
      (𝓝[<] 0) (𝓝 0) :=
  gibbs_heat_matching flatConstructedScreen (inverseFrameMetricField flatSolder) constantTimeCovector
    p hp hs 1 isOpen_univ (frame_metric_smooth univ flatSolder flat_solder_smooth)
    (fun i j => (gibbs_flat_matter_smooth p i j).differentiableOn (by simp)) flat_control_null

theorem gibbs_flat_area_not_matching (p : ι → ℝ) (hp : ∀ i, 0<p i) (hs : ∑ i, p i=1)
    (hv : 0 < modularVariance p) (eta : ℝ) :
    ¬Tendsto (fun t => microscopicAreaError
      (quadraticGibbsCurve p hp hs (covectorRead (constantTimeCovector 0) horizonControlDirection))
      eta (inducedArea (frameMetricField flatSolder) flatConstructedScreen.curve
        flatConstructedScreen.screen.vectors) t/t^2) (𝓝[<] 0) (𝓝 0) := by
  have hG : SmoothConnectionOn univ (frameLeviCivita flatSolder flatSolder) := by
    rw [flat_connection_zero]
    exact fun _ _ _ => contDiffOn_const
  have ht : ∀ i j k, frameLeviCivita flatSolder flatSolder 0 i k j=
      frameLeviCivita flatSolder flatSolder 0 j k i := by
    simp only [flat_connection_zero,Matrix.zero_apply,implies_true]
  intro hh
  have he := (gibbs_area_matching_iff_ricci flatConstructedScreen
    (inverseFrameMetricField flatSolder) constantTimeCovector p hp hs eta isOpen_univ
    (frame_metric_smooth univ flatSolder flat_solder_smooth) hG ht flat_control_null).mp hh
  change eta*tensorQuad (coordinateRicci (frameLeviCivita flatSolder flatSolder) 0)
    horizonControlDirection=2*Real.pi*tensorQuad (gibbsFlatMatter p 0) horizonControlDirection at he
  rw [flat_ricci_zero,gibbs_flat_null_value] at he
  have hpC : 0<gibbsCoupling p := div_pos hv Real.pi_pos
  have hpos : 0<2*Real.pi*gibbsCoupling p := by positivity
  have hz : tensorQuad (0 : Tensor4) horizonControlDirection=0 := by simp [tensorQuad]
  rw [hz,mul_zero] at he
  linarith

#print axioms gibbs_weights_tracial
#print axioms binary_gibbs_variance_positive
#print axioms tower_first_site_variance_positive
#print axioms tower_gibbs_read_weights
#print axioms tower_gibbs_entropy_quadratic
#print axioms tower_gibbs_modular_quadratic
#print axioms gibbs_weights_not_modular_orbit
#print axioms tower_gibbs_not_modular_orbit
#print axioms gibbs_flat_matter_smooth
#print axioms gibbs_flat_matter_conserved
#print axioms gibbs_flat_null_value
#print axioms gibbs_flat_heat_matching
#print axioms gibbs_flat_area_not_matching
end
end ChatgptAudit.Thermal024
