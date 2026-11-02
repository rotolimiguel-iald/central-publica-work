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
import TGLExt.ThermalCutoffResponse

set_option autoImplicit false
set_option maxHeartbeats 14000000
namespace ChatgptAudit.Thermal025
open Matrix Filter Topology Set TGLExt ChatgptAudit.Thermal024 ChatgptAudit.Micro021
  ChatgptAudit.Coherent023 ChatgptAudit.Flow019 ChatgptAudit.Flow020 ChatgptAudit.Screen014
open scoped ContDiff Matrix.Norms.Elementwise
noncomputable section

def halfThermalReference : SiteProfile where
  w _ := 1/2
  pos _ := by norm_num
  lt_one _ := by norm_num

def thirdThermalReference : SiteProfile where
  w _ := 1/3
  pos _ := by norm_num
  lt_one _ := by norm_num

theorem half_site_equal : ∀ i j : Fin 2, siteW (1/2) i=siteW (1/2) j := by
  intro i j
  fin_cases i <;> fin_cases j <;> norm_num [siteW]

theorem half_gibbs_affinity (s : ℝ) : gibbsAffinity (siteW (1/2)) s=1 := by
  have hf : gibbsWeights (siteW (1/2)) s=siteW (1/2) :=
    funext (gibbs_weights_tracial _ (siteW_sum _) half_site_equal s)
  unfold gibbsAffinity
  rw [hf]
  exact diagonal_affinity_self _ (fun i => (siteW_pos (by norm_num) (by norm_num) i).le) (siteW_sum _)

theorem half_thermal_vectors_fixed (N : ℕ) (s : ℝ) :
    towerGibbsVector halfThermalReference N s=hOmega halfThermalReference := by
  have hi := tower_gibbs_uniform_overlap halfThermalReference (1/2) (fun _ => rfl) s N
  rw [half_gibbs_affinity,one_pow,Complex.ofReal_one] at hi
  have hz : ‖hOmega halfThermalReference-towerGibbsVector halfThermalReference N s‖^2=0 := by
    rw [norm_sub_sq (𝕜 := ℂ),hOmega_norm,tower_gibbs_vector_norm,hi]
    norm_num
  exact (sub_eq_zero.mp (norm_eq_zero.mp (sq_eq_zero_iff.mp hz))).symm

theorem half_thermal_variance_zero (N : ℕ) : modularVariance (towerW halfThermalReference N)=0 := by
  have hv : modularVariance (siteW (1/2))=0 :=
    (modular_variance_zero_iff_tracial _ (siteW_pos (by norm_num) (by norm_num)) (siteW_sum _)).mpr half_site_equal
  rw [tower_variance_uniform halfThermalReference (1/2) (fun _ => rfl),hv,mul_zero]

theorem third_thermal_vectors_not_cauchy (s : ℝ) (hs : s≠0) :
    ¬CauchySeq (fun N : ℕ => towerGibbsVector thirdThermalReference N s) :=
  thermal_vectors_not_cauchy thirdThermalReference (1/3) (fun _ => rfl) s hs (by norm_num)

theorem third_thermal_coupling_unbounded :
    Tendsto (fun N : ℕ => gibbsCoupling (towerW thirdThermalReference N)) atTop atTop :=
  tower_coupling_unbounded thirdThermalReference (1/3) (fun _ => rfl) (by norm_num)

theorem cutoff_heat_matching
    {U : Set Coordinate4} {g : TensorField4} {Gamma : ConnectionField4} {x d : Coordinate4}
    (S : EquilibriumScreenData U g Gamma x d) (gInv : TensorField4) (w : CovectorField4)
    (P : SiteProfile) (q : ℝ) (hP : ∀ n, P.w n=q) (N : ℕ) (rate : ℝ)
    (hU : IsOpen U) (hg : SmoothMatrixOn U g)
    (hT : ∀ i j, DifferentiableOn ℝ (fun y => covectorStressField g gInv w (gibbsCoupling (siteW q)) y i j) U)
    (hn : tensorQuad (g x) d=0) :
    Tendsto (fun t => microscopicHeatError
      (quadraticGibbsCurve (towerW P N) (towerW_pos P N) (towerW_sum P N)
        (cutoffFrequency (covectorRead (w x) d) N)) rate
      (constructedHeat S (covectorStressField g gInv w (gibbsCoupling (siteW q))) rate hU hg hT) t/t^2)
      (𝓝[<] 0) (𝓝 0) := by
  let T := covectorStressField g gInv w (gibbsCoupling (siteW q))
  have he : gibbsResponse (towerW P N) (cutoffFrequency (covectorRead (w x) d) N)=
      -Real.pi*tensorQuad (T x) d :=
    (cutoff_response_equals_site P q hP _ N).trans
      (gibbs_response_null_stress (siteW q) (g x) (gInv x) (w x) d hn)
  have hl := gibbs_heat_error_limit (towerW P N) (towerW_pos P N) (towerW_sum P N)
    (cutoffFrequency (covectorRead (w x) d) N) rate (constructedHeat S T rate hU hg hT)
    (-rate*tensorQuad (T x) d/2) (constructed_heat_quadratic_limit S T rate hU hg hT)
  rw [he] at hl
  have hz : -rate*tensorQuad (T x) d/2-rate/(2*Real.pi)*(-Real.pi*tensorQuad (T x) d)=0 := by
    field_simp [Real.pi_ne_zero]
    ring
  rwa [hz] at hl

theorem cutoff_area_matching_iff_ricci
    {U : Set Coordinate4} {g : TensorField4} {Gamma : ConnectionField4} {x d : Coordinate4}
    (S : EquilibriumScreenData U g Gamma x d) (gInv : TensorField4) (w : CovectorField4)
    (P : SiteProfile) (q : ℝ) (hP : ∀ n, P.w n=q) (N : ℕ) (eta : ℝ)
    (hU : IsOpen U) (hg : SmoothMatrixOn U g) (hG : SmoothConnectionOn U Gamma)
    (ht : ∀ i j k, Gamma x i k j=Gamma x j k i) (hn : tensorQuad (g x) d=0) :
    Tendsto (fun t => microscopicAreaError
      (quadraticGibbsCurve (towerW P N) (towerW_pos P N) (towerW_sum P N)
        (cutoffFrequency (covectorRead (w x) d) N)) eta
      (inducedArea g S.curve S.screen.vectors) t/t^2) (𝓝[<] 0) (𝓝 0) ↔
      eta*tensorQuad (coordinateRicci Gamma x) d=
        2*Real.pi*tensorQuad (covectorStressField g gInv w (gibbsCoupling (siteW q)) x) d := by
  have hl := gibbs_area_error_limit S (towerW P N) (towerW_pos P N) (towerW_sum P N)
    (cutoffFrequency (covectorRead (w x) d) N) eta hU hg hG ht
  rw [cutoff_response_equals_site P q hP] at hl
  rw [past_zero_limit_iff _ _ hl,gibbs_response_null_stress (siteW q) (g x) (gInv x) (w x) d hn]
  change -Real.pi*tensorQuad (covectorStressField g gInv w (gibbsCoupling (siteW q)) x) d+
    eta*tensorQuad (coordinateRicci Gamma x) d/2=0 ↔ _
  constructor <;> intro hh <;> nlinarith only [hh]

theorem cutoff_flat_heat_matching (P : SiteProfile) (q : ℝ) (hP : ∀ n, P.w n=q) (N : ℕ) :
    Tendsto (fun t => microscopicHeatError
      (quadraticGibbsCurve (towerW P N) (towerW_pos P N) (towerW_sum P N)
        (cutoffFrequency (covectorRead (constantTimeCovector 0) horizonControlDirection) N))
      1 (constructedHeat flatConstructedScreen (gibbsFlatMatter (siteW q)) 1 isOpen_univ
        (frame_metric_smooth univ flatSolder flat_solder_smooth)
        (fun i j => (gibbs_flat_matter_smooth (siteW q) i j).differentiableOn (by simp))) t/t^2)
      (𝓝[<] 0) (𝓝 0) :=
  cutoff_heat_matching flatConstructedScreen (inverseFrameMetricField flatSolder) constantTimeCovector
    P q hP N 1 isOpen_univ (frame_metric_smooth univ flatSolder flat_solder_smooth)
    (fun i j => (gibbs_flat_matter_smooth (siteW q) i j).differentiableOn (by simp)) flat_control_null

theorem cutoff_flat_area_not_matching (P : SiteProfile) (q : ℝ) (hP : ∀ n, P.w n=q)
    (hq : q≠1/2) (N : ℕ) (eta : ℝ) :
    ¬Tendsto (fun t => microscopicAreaError
      (quadraticGibbsCurve (towerW P N) (towerW_pos P N) (towerW_sum P N)
        (cutoffFrequency (covectorRead (constantTimeCovector 0) horizonControlDirection) N))
      eta (inducedArea (frameMetricField flatSolder) flatConstructedScreen.curve
        flatConstructedScreen.screen.vectors) t/t^2) (𝓝[<] 0) (𝓝 0) := by
  have hG : SmoothConnectionOn univ (frameLeviCivita flatSolder flatSolder) := by
    rw [flat_connection_zero]
    exact fun _ _ _ => contDiffOn_const
  have ht : ∀ i j k, frameLeviCivita flatSolder flatSolder 0 i k j=
      frameLeviCivita flatSolder flatSolder 0 j k i := by
    simp only [flat_connection_zero,Matrix.zero_apply,implies_true]
  intro hh
  have he := (cutoff_area_matching_iff_ricci flatConstructedScreen
    (inverseFrameMetricField flatSolder) constantTimeCovector P q hP N eta isOpen_univ
    (frame_metric_smooth univ flatSolder flat_solder_smooth) hG ht flat_control_null).mp hh
  change eta*tensorQuad (coordinateRicci (frameLeviCivita flatSolder flatSolder) 0)
    horizonControlDirection=2*Real.pi*tensorQuad (gibbsFlatMatter (siteW q) 0) horizonControlDirection at he
  rw [flat_ricci_zero,gibbs_flat_null_value] at he
  have hpC : 0<gibbsCoupling (siteW q) := div_pos (stationary_site_variance_positive P q hP hq) Real.pi_pos
  have hpos : 0<2*Real.pi*gibbsCoupling (siteW q) := by positivity
  have hz : tensorQuad (0 : Tensor4) horizonControlDirection=0 := by simp [tensorQuad]
  rw [hz,mul_zero] at he
  linarith

#print axioms half_site_equal
#print axioms half_gibbs_affinity
#print axioms half_thermal_vectors_fixed
#print axioms half_thermal_variance_zero
#print axioms third_thermal_vectors_not_cauchy
#print axioms third_thermal_coupling_unbounded
#print axioms cutoff_heat_matching
#print axioms cutoff_area_matching_iff_ricci
#print axioms cutoff_flat_heat_matching
#print axioms cutoff_flat_area_not_matching
end
end ChatgptAudit.Thermal025
