-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_029 (06/09/2026), transposta em 06/09/2026
-- Lote 029: GEOMETRIA CURVA CONSTRUIDA — familia de soldas de onda plana (metrica e inversa reais,
--   Levi-Civita e curvatura CALCULADAS: wave_ricci, wave_einstein = (a+c) w (x) w), materia escalar
--   conservada, habitante CURVO do casamento de area na familia (matched_wave_area; matched_wave_einstein
--   _from_area) e a LIBERDADE RESIDUAL: a soma dos coeficientes transversais e escolhida para casar a area;
--   a diferenca (shear) fica LIVRE — entropia, Ricci e materia iguais NAO selecionam a coordenada de
--   curvatura (matched_curvature_distinguishes; state_alone_not_curvature_coordinate); controles:
--   wave_wrong_trace_refused, zero_eta_nonzero_source_refused, zero_wave_vacuum/nonflat.
--   Estatuto [REAL / INPUT / OPEN]: construcao de EXISTENCIA dentro de um ansatz — nao e derivacao da
--   geometria geral a partir de omega(I)=1; lei de area geral e selecao da liberdade radiativa OPEN.
-- Auditoria da gerencia (sessao d554e796, 06/09/2026): hashes 16/16; manifesto conferido; auditor da
--   bancada exit 0; recompilacao INDEPENDENTE 6/6, axiomas no trio; guarda de colisao estatica no ROOT;
--   enunciados lidos. Transposicao MECANICA (cabecalho + prefixo TGLExt.).
-- NAO move gate; nao e fisica; NOT_FALSIFIED nunca e CONFIRMED; CONFIRMADA proibido.
-- ---------------------------------------------------------------------
import TGLExt.PlaneWaveMatter

set_option autoImplicit false
set_option maxHeartbeats 8000000
set_option maxRecDepth 4096
namespace ChatgptAudit.Wave029
open Matrix Filter Topology Set TGLExt ChatgptAudit.Coherent023 ChatgptAudit.Response028
  ChatgptAudit.Flow019 ChatgptAudit.Flow020 ChatgptAudit.Micro021 ChatgptAudit.Profile026 ChatgptAudit.Thermal025
open scoped ContDiff Matrix.Norms.Elementwise
noncomputable section

def waveRicciScale (b : SummableAmplitude) (eta : ℝ) : ℝ :=
  2*Real.pi*amplitudeCoupling b/eta
def matchedLeft (b : SummableAmplitude) (eta shear : ℝ) : ℝ := waveRicciScale b eta/2+shear
def matchedRight (b : SummableAmplitude) (eta shear : ℝ) : ℝ := waveRicciScale b eta/2-shear
def matchedSolder (b : SummableAmplitude) (eta shear : ℝ) : TensorField4 :=
  waveSolder (matchedLeft b eta shear) (matchedRight b eta shear)
def matchedInverseSolder (b : SummableAmplitude) (eta shear : ℝ) : TensorField4 :=
  waveInverseSolder (matchedLeft b eta shear) (matchedRight b eta shear)

theorem matched_parameter_sum (b : SummableAmplitude) (eta shear : ℝ) :
    matchedLeft b eta shear+matchedRight b eta shear=waveRicciScale b eta := by
  unfold matchedLeft matchedRight
  ring

theorem wave_ricci_quad (a c : ℝ) (x d : Coordinate4) :
    tensorQuad (coordinateRicci (frameLeviCivita (waveSolder a c) (waveInverseSolder a c)) x) d=
      (a+c)*(covectorRead waveCovector d)^2 := by
  rw [wave_ricci]
  simp only [tensorQuad,Matrix.smul_mulVec,dotProduct_smul,smul_eq_mul]
  change (a+c)*tensorQuad (Matrix.vecMulVec waveCovector waveCovector) d=_
  rw [outer_tensor_quad]

theorem wave_matter_quad (a c coupling : ℝ) (x d : Coordinate4) :
    tensorQuad (waveMatter a c coupling x) d=coupling*(covectorRead waveCovector d)^2 := by
  rw [wave_matter_formula]
  simp only [tensorQuad,Matrix.smul_mulVec,dotProduct_smul,smul_eq_mul]
  change coupling*tensorQuad (Matrix.vecMulVec waveCovector waveCovector) d=_
  rw [outer_tensor_quad]

theorem wave_area_matching_of_sum (a c : ℝ) (b : SummableAmplitude) (eta : ℝ)
    (heta : eta≠0) (hac : a+c=waveRicciScale b eta) (x d : Coordinate4)
    (P : EquilibriumScreenData univ (frameMetricField (waveSolder a c))
      (frameLeviCivita (waveSolder a c) (waveInverseSolder a c)) x d)
    (hn : tensorQuad (frameMetricField (waveSolder a c) x) d=0) :
    Tendsto (fun t => amplitudeAreaDefect b (covectorRead waveCovector d) eta
      (inducedArea (frameMetricField (waveSolder a c)) P.curve P.screen.vectors) t/t^2)
      (𝓝[<] 0) (𝓝 0) := by
  have hG : SmoothConnectionOn univ (frameLeviCivita (waveSolder a c) (waveInverseSolder a c)) := by
    rw [wave_levi_civita]
    exact wave_connection_smooth a c
  have ht : ∀ i j k, frameLeviCivita (waveSolder a c) (waveInverseSolder a c) x i k j=
      frameLeviCivita (waveSolder a c) (waveInverseSolder a c) x j k i := by
    rw [wave_levi_civita]
    exact wave_connection_torsion_free a c x
  apply (amplitude_area_matching_iff_ricci P
    (inverseFrameMetricField (waveInverseSolder a c)) waveCovectorField b eta isOpen_univ
    (frame_metric_smooth univ _ (wave_solder_smooth a c)) hG ht hn).2
  change eta*tensorQuad (coordinateRicci
    (frameLeviCivita (waveSolder a c) (waveInverseSolder a c)) x) d=
      2*Real.pi*tensorQuad (waveMatter a c (amplitudeCoupling b) x) d
  rw [wave_ricci_quad,wave_matter_quad,hac]
  unfold waveRicciScale
  field_simp [heta]

theorem matched_wave_area (b : SummableAmplitude) (eta shear : ℝ) (heta : eta≠0)
    (x d : Coordinate4)
    (P : EquilibriumScreenData univ (frameMetricField (matchedSolder b eta shear))
      (frameLeviCivita (matchedSolder b eta shear) (matchedInverseSolder b eta shear)) x d)
    (hn : tensorQuad (frameMetricField (matchedSolder b eta shear) x) d=0) :
    Tendsto (fun t => amplitudeAreaDefect b (covectorRead waveCovector d) eta
      (inducedArea (frameMetricField (matchedSolder b eta shear)) P.curve P.screen.vectors) t/t^2)
      (𝓝[<] 0) (𝓝 0) :=
  wave_area_matching_of_sum _ _ b eta heta (matched_parameter_sum b eta shear) x d P hn

def matchedScreen (b : SummableAmplitude) (eta shear : ℝ) (x d : Coordinate4) (hd : d≠0)
    (hn : tensorQuad (frameMetricField (matchedSolder b eta shear) x) d=0) :
    EquilibriumScreenData univ (frameMetricField (matchedSolder b eta shear))
      (frameLeviCivita (matchedSolder b eta shear) (matchedInverseSolder b eta shear)) x d :=
  localEquilibriumScreen univ isOpen_univ _ _
    (fun y _ => wave_solder_inverse _ _ y) (fun y _ => wave_inverse_solder _ _ y)
    (wave_solder_smooth _ _) (wave_inverse_solder_smooth _ _) x d (mem_univ _) hd hn

theorem matched_constructed_area (b : SummableAmplitude) (eta shear : ℝ) (heta : eta≠0)
    (x d : Coordinate4) (hd : d≠0)
    (hn : tensorQuad (frameMetricField (matchedSolder b eta shear) x) d=0) :
    let P := matchedScreen b eta shear x d hd hn
    Tendsto (fun t => amplitudeAreaDefect b (covectorRead waveCovector d) eta
      (inducedArea (frameMetricField (matchedSolder b eta shear)) P.curve P.screen.vectors) t/t^2)
      (𝓝[<] 0) (𝓝 0) :=
  matched_wave_area b eta shear heta x d (matchedScreen b eta shear x d hd hn) hn

theorem wave_heat_matching (a c : ℝ) (b : SummableAmplitude) (rate : ℝ) (x d : Coordinate4)
    (P : EquilibriumScreenData univ (frameMetricField (waveSolder a c))
      (frameLeviCivita (waveSolder a c) (waveInverseSolder a c)) x d)
    (hn : tensorQuad (frameMetricField (waveSolder a c) x) d=0) :
    Tendsto (fun t => amplitudeHeatDefect b (covectorRead waveCovector d) rate
      (constructedHeat P (waveMatter a c (amplitudeCoupling b)) rate isOpen_univ
        (frame_metric_smooth univ _ (wave_solder_smooth a c))
        (fun i j => (wave_matter_smooth a c (amplitudeCoupling b) i j).differentiableOn (by simp))) t/t^2)
      (𝓝[<] 0) (𝓝 0) :=
  amplitude_heat_matching P (inverseFrameMetricField (waveInverseSolder a c)) waveCovectorField b rate
    isOpen_univ (frame_metric_smooth univ _ (wave_solder_smooth a c))
    (fun i j => (wave_matter_smooth a c (amplitudeCoupling b) i j).differentiableOn (by simp)) hn

theorem matched_wave_einstein (b : SummableAmplitude) (eta shear : ℝ) (x : Coordinate4) :
    frameEinsteinTensor (matchedSolder b eta shear) (matchedInverseSolder b eta shear) x=
      (2*Real.pi/eta) • frameCovectorStress (matchedSolder b eta shear)
        (matchedInverseSolder b eta shear) waveCovectorField (amplitudeCoupling b) x := by
  change frameEinsteinTensor (waveSolder _ _) (waveInverseSolder _ _) x=
    (2*Real.pi/eta) • waveMatter _ _ (amplitudeCoupling b) x
  rw [wave_einstein,wave_matter_formula,matched_parameter_sum,smul_smul]
  congr 1
  unfold waveRicciScale
  ring

theorem matched_wave_einstein_from_area (b : SummableAmplitude) (eta shear : ℝ) (heta : eta≠0) :
    ∃ cosmological : ℝ, ∀ x∈(univ : Set Coordinate4),
      frameEinsteinTensor (matchedSolder b eta shear) (matchedInverseSolder b eta shear) x+
        cosmological • frameMetricField (matchedSolder b eta shear) x=
      (2*Real.pi/eta) • frameCovectorStress (matchedSolder b eta shear)
        (matchedInverseSolder b eta shear) waveCovectorField (amplitudeCoupling b) x := by
  apply einstein_from_summable_area_matching univ isOpen_univ isPreconnected_univ
    (matchedSolder b eta shear) (matchedInverseSolder b eta shear) waveCovectorField b
    1 eta one_ne_zero heta
    (fun x _ => wave_solder_inverse _ _ x) (fun x _ => wave_inverse_solder _ _ x)
    (wave_solder_smooth _ _) (wave_inverse_solder_smooth _ _) wave_covector_smooth
    wave_covector_closed (wave_covector_wave _ _)
  intro x hx d hd hn
  exact matched_constructed_area b eta shear heta x d hd hn

theorem wave_read_entropy_joint {α : Type} {l : Filter α}
    (b : SummableAmplitude) (d : Coordinate4) (cutoff : α → ℕ) (time : α → ℝ)
    (hN : Tendsto cutoff l atTop) (ht : Tendsto time l (𝓝 0)) (hne : ∀ᶠ y in l, time y≠0) :
    Tendsto (fun y =>
      (finiteEntropy (amplitudeReadWeights b (covectorRead waveCovector d*time y) (cutoff y))-
        finiteEntropy (towerW thirdThermalReference (cutoff y)))/(time y)^2) l
      (𝓝 (amplitudeResponse b (covectorRead waveCovector d))) := by
  simpa only [amplitude_read_entropy] using
    amplitude_prefix_entropy_joint b (covectorRead waveCovector d) cutoff time hN ht hne

theorem matched_read_area_joint {α : Type} {l : Filter α}
    (b : SummableAmplitude) (eta shear : ℝ) (heta : eta≠0) (x d : Coordinate4)
    (P : EquilibriumScreenData univ (frameMetricField (matchedSolder b eta shear))
      (frameLeviCivita (matchedSolder b eta shear) (matchedInverseSolder b eta shear)) x d)
    (hn : tensorQuad (frameMetricField (matchedSolder b eta shear) x) d=0)
    (cutoff : α → ℕ) (time : α → ℝ) (hN : Tendsto cutoff l atTop)
    (ht : Tendsto time l (𝓝[<] 0)) :
    Tendsto (fun y =>
      (finiteEntropy (amplitudeReadWeights b (covectorRead waveCovector d*time y) (cutoff y))-
        finiteEntropy (towerW thirdThermalReference (cutoff y))-
        eta*(inducedArea (frameMetricField (matchedSolder b eta shear)) P.curve P.screen.vectors (time y)-
          inducedArea (frameMetricField (matchedSolder b eta shear)) P.curve P.screen.vectors 0))/
        (time y)^2) l (𝓝 0) := by
  have hread := wave_read_entropy_joint b d cutoff time hN (ht.mono_right nhdsWithin_le_nhds)
    (ht.eventually past_time_nonzero)
  have hglobal := (amplitude_entropy_quadratic_limit b (covectorRead waveCovector d)).comp ht
  have harea := (matched_wave_area b eta shear heta x d P hn).comp ht
  have h := (hread.sub hglobal).add harea
  simp only [sub_self,add_zero] at h
  convert h using 1
  funext y
  simp only [Function.comp_apply,amplitudeAreaDefect]
  ring

#print axioms matched_read_area_joint

#print axioms waveRicciScale
#print axioms matchedSolder
#print axioms matchedInverseSolder
#print axioms matchedScreen
#print axioms matched_parameter_sum
#print axioms wave_ricci_quad
#print axioms wave_matter_quad
#print axioms wave_area_matching_of_sum
#print axioms matched_wave_area
#print axioms matched_constructed_area
#print axioms wave_heat_matching
#print axioms matched_wave_einstein
#print axioms matched_wave_einstein_from_area
#print axioms wave_read_entropy_joint
end
end ChatgptAudit.Wave029
