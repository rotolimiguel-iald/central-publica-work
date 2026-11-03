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
import TGLExt.TowerThermalOverlap

set_option autoImplicit false
set_option maxHeartbeats 14000000
namespace ChatgptAudit.Thermal025
open Matrix Filter Topology Set TGLExt ChatgptAudit.Thermal024 ChatgptAudit.Micro021
noncomputable section

def cutoffSize (N : ℕ) : ℝ := (N:ℝ)+1
def cutoffFrequency (frequency : ℝ) (N : ℕ) : ℝ := frequency/Real.sqrt (cutoffSize N)
def cutoffParameter (frequency t : ℝ) (N : ℕ) : ℝ := (frequency*t)^2/cutoffSize N

theorem cutoff_size_positive (N : ℕ) : 0<cutoffSize N := by unfold cutoffSize; positivity

theorem cutoff_frequency_square (frequency : ℝ) (N : ℕ) :
    (cutoffFrequency frequency N)^2=frequency^2/cutoffSize N := by
  rw [cutoffFrequency,div_pow,Real.sq_sqrt (cutoff_size_positive N).le]

theorem cutoff_parameter_matches (frequency t : ℝ) (N : ℕ) :
    (cutoffFrequency frequency N*t)^2=cutoffParameter frequency t N := by
  rw [mul_pow,cutoff_frequency_square]
  unfold cutoffParameter
  ring

theorem cutoff_size_tends_infinity : Tendsto cutoffSize atTop atTop := by
  change Tendsto (fun N : ℕ => (N:ℝ)+1) atTop atTop
  have ht : Tendsto (fun N : ℕ => ((N+1:ℕ):ℝ)) atTop atTop :=
    tendsto_natCast_atTop_atTop.comp (tendsto_add_atTop_nat 1)
  simpa only [Nat.cast_add,Nat.cast_one] using ht

theorem cutoff_parameter_tends_zero (frequency t : ℝ) :
    Tendsto (cutoffParameter frequency t) atTop (𝓝 0) := by
  change Tendsto (fun N : ℕ => (frequency*t)^2/((N:ℝ)+1)) atTop (𝓝 0)
  have ht := (tendsto_one_div_add_atTop_nhds_zero_nat (𝕜 := ℝ)).const_mul ((frequency*t)^2)
  simpa only [mul_one_div,mul_zero] using ht

theorem tower_coupling_uniform (P : SiteProfile) (q : ℝ) (hP : ∀ n, P.w n=q) (N : ℕ) :
    gibbsCoupling (towerW P N)=cutoffSize N*gibbsCoupling (siteW q) := by
  unfold gibbsCoupling cutoffSize
  rw [tower_variance_uniform P q hP]
  ring

theorem stationary_site_variance_positive (P : SiteProfile) (q : ℝ) (hP : ∀ n, P.w n=q) (hq : q≠1/2) :
    0 < modularVariance (siteW q) := by
  have h0 : 0<q := by rw [←hP 0]; exact P.pos 0
  have h1 : q<1 := by rw [←hP 0]; exact P.lt_one 0
  exact binary_gibbs_variance_positive q h0 h1 hq

theorem tower_coupling_unbounded (P : SiteProfile) (q : ℝ) (hP : ∀ n, P.w n=q) (hq : q≠1/2) :
    Tendsto (fun N : ℕ => gibbsCoupling (towerW P N)) atTop atTop := by
  have hc : 0<gibbsCoupling (siteW q) := div_pos (stationary_site_variance_positive P q hP hq) Real.pi_pos
  have ht := Tendsto.const_mul_atTop hc cutoff_size_tends_infinity
  simpa only [tower_coupling_uniform P q hP,mul_comm] using ht

theorem cutoff_response_equals_site (P : SiteProfile) (q : ℝ) (hP : ∀ n, P.w n=q) (frequency : ℝ) (N : ℕ) :
    gibbsResponse (towerW P N) (cutoffFrequency frequency N)=gibbsResponse (siteW q) frequency := by
  unfold gibbsResponse
  rw [cutoff_frequency_square,tower_variance_uniform P q hP]
  change -(frequency^2/cutoffSize N)*(cutoffSize N*modularVariance (siteW q))=_
  field_simp [ne_of_gt (cutoff_size_positive N)]

theorem cutoff_modular_limit (P : SiteProfile) (q : ℝ) (hP : ∀ n, P.w n=q) (frequency : ℝ) (N : ℕ) :
    Tendsto (fun t => modularIncrement (towerW P N)
      (gibbsWeights (towerW P N) (cutoffParameter frequency t N))/t^2) (𝓝[<] 0)
      (𝓝 (-frequency^2*modularVariance (siteW q))) := by
  have ht := quadratic_gibbs_modular_limit (towerW P N) (towerW_pos P N) (towerW_sum P N) (cutoffFrequency frequency N)
  change Tendsto _ _ (𝓝 (gibbsResponse (towerW P N) (cutoffFrequency frequency N))) at ht
  rw [cutoff_response_equals_site P q hP] at ht
  simpa only [quadraticGibbsWeights,cutoff_parameter_matches,gibbsResponse] using ht

theorem cutoff_entropy_limit (P : SiteProfile) (q : ℝ) (hP : ∀ n, P.w n=q) (frequency : ℝ) (N : ℕ) :
    Tendsto (fun t => (finiteEntropy (gibbsWeights (towerW P N) (cutoffParameter frequency t N))-
      finiteEntropy (towerW P N))/t^2) (𝓝[<] 0) (𝓝 (-frequency^2*modularVariance (siteW q))) := by
  have ht := quadratic_gibbs_entropy_limit (towerW P N) (towerW_pos P N) (towerW_sum P N) (cutoffFrequency frequency N)
  change Tendsto _ _ (𝓝 (gibbsResponse (towerW P N) (cutoffFrequency frequency N))) at ht
  rw [cutoff_response_equals_site P q hP] at ht
  simpa only [quadraticGibbsWeights,cutoff_parameter_matches,gibbsResponse] using ht

theorem cutoff_relative_entropy_limit (P : SiteProfile) (frequency : ℝ) (N : ℕ) :
    Tendsto (fun t => diagonalRelativeEntropy
      (gibbsWeights (towerW P N) (cutoffParameter frequency t N)) (towerW P N)/t^2) (𝓝[<] 0) (𝓝 0) := by
  simpa only [quadraticGibbsWeights,cutoff_parameter_matches] using
    quadratic_gibbs_relative_entropy_zero (towerW P N) (towerW_pos P N) (towerW_sum P N) (cutoffFrequency frequency N)

theorem cutoff_state_entropy_limit (P : SiteProfile) (q : ℝ) (hP : ∀ n, P.w n=q) (frequency : ℝ) (N : ℕ) :
    Tendsto (fun t => (finiteEntropy (towerGibbsReadWeights P N (cutoffParameter frequency t N))-
      finiteEntropy (towerW P N))/t^2) (𝓝[<] 0) (𝓝 (-frequency^2*modularVariance (siteW q))) := by
  simpa only [tower_gibbs_read_weights] using cutoff_entropy_limit P q hP frequency N

theorem thermal_local_state_continuous (P : SiteProfile) (L : ℕ) (a : Matrix (chainIdx L) (chainIdx L) ℂ) :
    Continuous (fun s => towerGibbsState P L s (towerPi P a)) := by
  have he : (fun s => towerGibbsState P L s (towerPi P a))=
      (fun s => ∑ i, (gibbsWeights (towerW P L) s i:ℂ)*a i i) := by
    funext s
    exact tower_gibbs_local_state P L s a
  rw [he]
  apply continuous_finsetSum
  intro i _
  exact (Complex.continuous_ofReal.comp (gibbs_weights_continuous _ (towerW_pos P L) i)).mul continuous_const

theorem cutoff_local_state_returns_reference (P : SiteProfile) (L : ℕ)
    (a : Matrix (chainIdx L) (chainIdx L) ℂ) (frequency t : ℝ) :
    Tendsto (fun N : ℕ => towerGibbsState P N (cutoffParameter frequency t N) (towerPi P a))
      atTop (𝓝 (omegaState P (towerPi P a))) := by
  have ht := ((thermal_local_state_continuous P L a).continuousAt (x := 0)).tendsto.comp
    (cutoff_parameter_tends_zero frequency t)
  rw [tower_gibbs_state_zero] at ht
  have he : (fun N : ℕ => towerGibbsState P N (cutoffParameter frequency t N) (towerPi P a))=ᶠ[atTop]
      (fun N : ℕ => towerGibbsState P L (cutoffParameter frequency t N) (towerPi P a)) := by
    filter_upwards [eventually_ge_atTop L] with N hN
    exact thermal_tower_marginal P _ hN a
  exact ht.congr' he.symm

#print axioms cutoff_size_positive
#print axioms cutoff_frequency_square
#print axioms cutoff_parameter_matches
#print axioms cutoff_size_tends_infinity
#print axioms cutoff_parameter_tends_zero
#print axioms tower_coupling_uniform
#print axioms stationary_site_variance_positive
#print axioms tower_coupling_unbounded
#print axioms cutoff_response_equals_site
#print axioms cutoff_modular_limit
#print axioms cutoff_entropy_limit
#print axioms cutoff_relative_entropy_limit
#print axioms cutoff_state_entropy_limit
#print axioms thermal_local_state_continuous
#print axioms cutoff_local_state_returns_reference
end
end ChatgptAudit.Thermal025
