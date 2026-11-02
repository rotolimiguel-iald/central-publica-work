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
import TGLExt.PlaneWaveEntropyMatching

set_option autoImplicit false
set_option maxHeartbeats 8000000
set_option maxRecDepth 4096
namespace ChatgptAudit.Wave029
open Matrix Filter Topology Set TGLExt ChatgptAudit.Coherent023 ChatgptAudit.Response028
  ChatgptAudit.Flow019 ChatgptAudit.Flow020 ChatgptAudit.Micro021 ChatgptAudit.Profile026 ChatgptAudit.Thermal025
open scoped ContDiff Matrix.Norms.Elementwise
noncomputable section

def waveTestDirection : Coordinate4 := ![1,1,0,0]

theorem wave_test_nonzero : waveTestDirection≠0 := by
  intro h
  have hh := congrArg (fun v : Coordinate4 => v 0) h
  norm_num [waveTestDirection] at hh

theorem wave_test_null (a c : ℝ) :
    tensorQuad (frameMetricField (waveSolder a c) 0) waveTestDirection=0 := by
  rw [wave_metric_at_origin]
  norm_num [waveTestDirection,eta4,tensorQuad,Matrix.mulVec,dotProduct,Fin.sum_univ_four,
    Matrix.cons_val_two,Matrix.cons_val_three,Matrix.diagonal_apply,Fin.isValue]

theorem wave_test_frequency : covectorRead waveCovector waveTestDirection=1 := by
  norm_num [covectorRead,waveCovector,waveTestDirection,dotProduct,Fin.sum_univ_four,
    Matrix.cons_val_two,Matrix.cons_val_three]

def waveOriginScreen (a c : ℝ) :
    EquilibriumScreenData univ (frameMetricField (waveSolder a c))
      (frameLeviCivita (waveSolder a c) (waveInverseSolder a c)) 0 waveTestDirection :=
  localEquilibriumScreen univ isOpen_univ _ _
    (fun x _ => wave_solder_inverse a c x) (fun x _ => wave_inverse_solder a c x)
    (wave_solder_smooth a c) (wave_inverse_solder_smooth a c)
    0 waveTestDirection (mem_univ _) wave_test_nonzero (wave_test_null a c)

theorem wave_origin_area_iff (a c : ℝ) (b : SummableAmplitude) (eta : ℝ) :
    Tendsto (fun t => amplitudeAreaDefect b 1 eta
      (inducedArea (frameMetricField (waveSolder a c)) (waveOriginScreen a c).curve
        (waveOriginScreen a c).screen.vectors) t/t^2) (𝓝[<] 0) (𝓝 0) ↔
      eta*(a+c)=2*Real.pi*amplitudeCoupling b := by
  have hG : SmoothConnectionOn univ (frameLeviCivita (waveSolder a c) (waveInverseSolder a c)) := by
    rw [wave_levi_civita]
    exact wave_connection_smooth a c
  have ht : ∀ i j k, frameLeviCivita (waveSolder a c) (waveInverseSolder a c) 0 i k j=
      frameLeviCivita (waveSolder a c) (waveInverseSolder a c) 0 j k i := by
    rw [wave_levi_civita]
    exact wave_connection_torsion_free a c 0
  have h := amplitude_area_matching_iff_ricci (waveOriginScreen a c)
    (inverseFrameMetricField (waveInverseSolder a c)) waveCovectorField b eta isOpen_univ
    (frame_metric_smooth univ _ (wave_solder_smooth a c)) hG ht (wave_test_null a c)
  change (Tendsto (fun t => amplitudeAreaDefect b (covectorRead waveCovector waveTestDirection) eta
      (inducedArea (frameMetricField (waveSolder a c)) (waveOriginScreen a c).curve
        (waveOriginScreen a c).screen.vectors) t/t^2) (𝓝[<] 0) (𝓝 0) ↔
    eta*tensorQuad (coordinateRicci (frameLeviCivita (waveSolder a c) (waveInverseSolder a c)) 0)
      waveTestDirection=2*Real.pi*tensorQuad (waveMatter a c (amplitudeCoupling b) 0) waveTestDirection) at h
  simpa only [wave_ricci_quad,wave_matter_quad,wave_test_frequency,one_pow,mul_one] using h

theorem wave_wrong_trace_refused (a c : ℝ) (b : SummableAmplitude) (eta : ℝ)
    (hbad : eta*(a+c)≠2*Real.pi*amplitudeCoupling b) :
    ¬Tendsto (fun t => amplitudeAreaDefect b 1 eta
      (inducedArea (frameMetricField (waveSolder a c)) (waveOriginScreen a c).curve
        (waveOriginScreen a c).screen.vectors) t/t^2) (𝓝[<] 0) (𝓝 0) :=
  fun h => hbad ((wave_origin_area_iff a c b eta).mp h)

theorem matched_ricci_independent (b : SummableAmplitude) (eta s s' : ℝ) :
    coordinateRicci (frameLeviCivita (matchedSolder b eta s) (matchedInverseSolder b eta s))=
      coordinateRicci (frameLeviCivita (matchedSolder b eta s') (matchedInverseSolder b eta s')) := by
  funext x
  change coordinateRicci (frameLeviCivita (waveSolder _ _) (waveInverseSolder _ _)) x=
    coordinateRicci (frameLeviCivita (waveSolder _ _) (waveInverseSolder _ _)) x
  rw [wave_ricci,wave_ricci,matched_parameter_sum,matched_parameter_sum]

theorem matched_curvature_difference (b : SummableAmplitude) (eta shear : ℝ) (x : Coordinate4) :
    coordinateCurvature (frameLeviCivita (matchedSolder b eta shear) (matchedInverseSolder b eta shear)) x 1 0 1 0-
      coordinateCurvature (frameLeviCivita (matchedSolder b eta shear) (matchedInverseSolder b eta shear)) x 2 0 2 0=
      2*shear := by
  change coordinateCurvature (frameLeviCivita (waveSolder _ _) (waveInverseSolder _ _)) x 1 0 1 0-
    coordinateCurvature (frameLeviCivita (waveSolder _ _) (waveInverseSolder _ _)) x 2 0 2 0=_
  rw [wave_first_curvature,wave_second_curvature]
  unfold matchedLeft matchedRight
  ring

theorem matched_curvature_distinguishes (b : SummableAmplitude) (eta s s' : ℝ) (hs : s≠s')
    (x : Coordinate4) :
    coordinateCurvature (frameLeviCivita (matchedSolder b eta s) (matchedInverseSolder b eta s)) x 1 0 1 0≠
      coordinateCurvature (frameLeviCivita (matchedSolder b eta s') (matchedInverseSolder b eta s')) x 1 0 1 0 := by
  change coordinateCurvature (frameLeviCivita (waveSolder _ _) (waveInverseSolder _ _)) x 1 0 1 0≠
    coordinateCurvature (frameLeviCivita (waveSolder _ _) (waveInverseSolder _ _)) x 1 0 1 0
  rw [wave_first_curvature,wave_first_curvature]
  unfold matchedLeft
  exact fun h => hs (by linarith)

theorem matched_metrics_agree_at_origin (b : SummableAmplitude) (eta s s' : ℝ) :
    frameMetricField (matchedSolder b eta s) 0=frameMetricField (matchedSolder b eta s') 0 := by
  change frameMetricField (waveSolder _ _) 0=frameMetricField (waveSolder _ _) 0
  rw [wave_metric_at_origin,wave_metric_at_origin]

theorem zero_wave_ricci_scale (eta : ℝ) : waveRicciScale zeroAmplitude eta=0 := by
  simp [waveRicciScale,amplitudeCoupling,amplitudeMass,zeroAmplitude]

theorem zero_wave_vacuum (eta shear : ℝ) (x : Coordinate4) :
    coordinateRicci (frameLeviCivita (matchedSolder zeroAmplitude eta shear)
      (matchedInverseSolder zeroAmplitude eta shear)) x=0 := by
  change coordinateRicci (frameLeviCivita (waveSolder _ _) (waveInverseSolder _ _)) x=0
  rw [wave_ricci,matched_parameter_sum,zero_wave_ricci_scale,zero_smul]

theorem zero_wave_nonflat (eta shear : ℝ) (hs : shear≠0) (x : Coordinate4) :
    coordinateCurvature (frameLeviCivita (matchedSolder zeroAmplitude eta shear)
      (matchedInverseSolder zeroAmplitude eta shear)) x 1 0≠0 := by
  apply wave_curvature_nonzero
  simpa only [matchedLeft,zero_wave_ricci_scale,zero_div,zero_add] using hs

theorem geometric_wave_matter_nonzero (eta shear : ℝ) (x : Coordinate4) :
    frameCovectorStress (matchedSolder geometricAmplitude eta shear)
      (matchedInverseSolder geometricAmplitude eta shear) waveCovectorField
        (amplitudeCoupling geometricAmplitude) x≠0 :=
  wave_matter_nonzero _ _ _ geometric_coupling_positive.ne' x

theorem geometric_wave_curved (eta : ℝ) (heta : eta≠0) (x : Coordinate4) :
    coordinateCurvature (frameLeviCivita (matchedSolder geometricAmplitude eta 0)
      (matchedInverseSolder geometricAmplitude eta 0)) x 1 0≠0 := by
  apply wave_curvature_nonzero
  change waveRicciScale geometricAmplitude eta/2+0≠0
  rw [add_zero]
  apply div_ne_zero
  · exact div_ne_zero
      (mul_ne_zero (mul_ne_zero (by norm_num) Real.pi_ne_zero) geometric_coupling_positive.ne') heta
  · norm_num

theorem state_alone_not_curvature_coordinate (b : SummableAmplitude) (eta t : ℝ) :
    ¬∃ F : ((TowerHilbert thirdThermalReference →L[ℂ] TowerHilbert thirdThermalReference) → ℂ) → ℝ,
      ∀ shear : ℝ, F (amplitudeState b t)=
        coordinateCurvature (frameLeviCivita (matchedSolder b eta shear)
          (matchedInverseSolder b eta shear)) 0 1 0 1 0 := by
  rintro ⟨F,hF⟩
  have h := (hF 0).symm.trans (hF 1)
  exact matched_curvature_distinguishes b eta 0 1 (by norm_num) 0 h

theorem zero_eta_nonzero_source_refused (a c : ℝ) (b : SummableAmplitude)
    (hb : amplitudeCoupling b≠0) :
    ¬Tendsto (fun t => amplitudeAreaDefect b 1 0
      (inducedArea (frameMetricField (waveSolder a c)) (waveOriginScreen a c).curve
        (waveOriginScreen a c).screen.vectors) t/t^2) (𝓝[<] 0) (𝓝 0) := by
  apply wave_wrong_trace_refused
  rw [zero_mul]
  exact Ne.symm (mul_ne_zero (mul_ne_zero (by norm_num) Real.pi_ne_zero) hb)

#print axioms zero_eta_nonzero_source_refused

#print axioms waveOriginScreen
#print axioms wave_test_nonzero
#print axioms wave_test_null
#print axioms wave_test_frequency
#print axioms wave_origin_area_iff
#print axioms wave_wrong_trace_refused
#print axioms matched_ricci_independent
#print axioms matched_curvature_difference
#print axioms matched_curvature_distinguishes
#print axioms matched_metrics_agree_at_origin
#print axioms zero_wave_ricci_scale
#print axioms zero_wave_vacuum
#print axioms zero_wave_nonflat
#print axioms geometric_wave_matter_nonzero
#print axioms geometric_wave_curved
#print axioms state_alone_not_curvature_coordinate
end
end ChatgptAudit.Wave029
