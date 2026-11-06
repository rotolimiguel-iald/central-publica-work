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
import TGLExt.PlaneWaveConnection

set_option autoImplicit false
set_option maxHeartbeats 12000000
set_option maxRecDepth 4096
namespace ChatgptAudit.Wave029
open Matrix Filter Topology Set TGLExt ChatgptAudit.Coherent023 ChatgptAudit.Response028
open scoped ContDiff Matrix.Norms.Elementwise
noncomputable section

theorem wave_connection_linear (a c : ℝ) (x : Coordinate4) (i r j : Fin 4) :
    waveConnection a c x i r j=
      waveConnection a c (Pi.single 1 1) i r j*x 1+
      waveConnection a c (Pi.single 2 1) i r j*x 2 := by
  fin_cases i <;> fin_cases r <;> fin_cases j <;>
    norm_num [waveConnection,waveTransverse,waveCovector,waveRaised,Pi.single_apply,
      Matrix.cons_val_two,Matrix.cons_val_three,Fin.isValue] <;> norm_num [Fin.ext_iff]

theorem wave_connection_jet (a c : ℝ) (x : Coordinate4) (k i : Fin 4) :
    connectionFirstJet (waveConnection a c) x k i=
      waveConnection a c (Pi.single k 1) i := by
  ext r j
  have he : (fun y => waveConnection a c y i r j)=
      fun y => waveConnection a c (Pi.single 1 1) i r j*y 1+
        waveConnection a c (Pi.single 2 1) i r j*y 2 := by
    funext y
    exact wave_connection_linear a c y i r j
  have hf := ((hasFDerivAt_apply (𝕜 := ℝ) 1 x).const_mul
    (waveConnection a c (Pi.single 1 1) i r j)).add
    ((hasFDerivAt_apply (𝕜 := ℝ) 2 x).const_mul (waveConnection a c (Pi.single 2 1) i r j))
  change HasFDerivAt (fun y : Coordinate4 =>
    waveConnection a c (Pi.single 1 1) i r j*y 1+
    waveConnection a c (Pi.single 2 1) i r j*y 2) _ x at hf
  change fderiv ℝ (fun y => waveConnection a c y i r j) x (Pi.single k 1)=_
  rw [he,hf.fderiv,wave_connection_linear a c (Pi.single k 1) i r j]
  simp only [_root_.add_apply,_root_.smul_apply,smul_eq_mul,ContinuousLinearMap.proj_apply]

theorem wave_connection_commute (a c : ℝ) (x : Coordinate4) (i j : Fin 4) :
    waveConnection a c x i*waveConnection a c x j=
      waveConnection a c x j*waveConnection a c x i := by
  ext r s
  fin_cases i <;> fin_cases j <;> fin_cases r <;> fin_cases s <;>
    norm_num [Matrix.mul_apply,Fin.sum_univ_four,waveConnection,waveTransverse,
      waveCovector,waveRaised,Matrix.cons_val_two,Matrix.cons_val_three,Fin.isValue]

theorem wave_curvature_formula (a c : ℝ) (x : Coordinate4) (i j : Fin 4) :
    coordinateCurvature (waveConnection a c) x i j=
      waveConnection a c (Pi.single i 1) j-waveConnection a c (Pi.single j 1) i := by
  unfold coordinateCurvature connectionCurvatureJet
  rw [wave_connection_jet,wave_connection_jet,wave_connection_commute a c x i j]
  abel

theorem wave_ricci (a c : ℝ) (x : Coordinate4) :
    coordinateRicci (frameLeviCivita (waveSolder a c) (waveInverseSolder a c)) x=
      (a+c) • Matrix.vecMulVec waveCovector waveCovector := by
  rw [wave_levi_civita]
  ext i j
  simp only [coordinateRicci,wave_curvature_formula]
  fin_cases i <;> fin_cases j <;>
    norm_num [Fin.sum_univ_four,waveConnection,waveTransverse,waveCovector,waveRaised,
      Pi.single_apply,Matrix.vecMulVec,Matrix.cons_val_two,Matrix.cons_val_three,Fin.isValue]

theorem wave_scalar_curvature (a c : ℝ) (x : Coordinate4) :
    coordinateScalarCurvature (inverseFrameMetricField (waveInverseSolder a c))
      (frameLeviCivita (waveSolder a c) (waveInverseSolder a c)) x=0 := by
  simp only [coordinateScalarCurvature,wave_ricci,wave_inverse_metric_formula]
  norm_num [Fin.sum_univ_four,eta4,Matrix.vecMulVec,waveCovector,waveRaised,
    Matrix.cons_val_two,Matrix.cons_val_three,Matrix.diagonal_apply,Fin.isValue]
  norm_num [Fin.ext_iff]
  ring

theorem wave_einstein (a c : ℝ) (x : Coordinate4) :
    frameEinsteinTensor (waveSolder a c) (waveInverseSolder a c) x=
      (a+c) • Matrix.vecMulVec waveCovector waveCovector := by
  unfold frameEinsteinTensor geometricEinsteinTensor
  rw [wave_scalar_curvature,wave_ricci]
  simp only [zero_div,zero_smul,sub_zero]

theorem wave_first_curvature (a c : ℝ) (x : Coordinate4) :
    coordinateCurvature (frameLeviCivita (waveSolder a c) (waveInverseSolder a c)) x 1 0 1 0=a := by
  rw [wave_levi_civita,wave_curvature_formula]
  norm_num [waveConnection,waveTransverse,waveCovector,waveRaised,Pi.single_apply,
    Matrix.cons_val_two,Matrix.cons_val_three,Fin.isValue]

theorem wave_second_curvature (a c : ℝ) (x : Coordinate4) :
    coordinateCurvature (frameLeviCivita (waveSolder a c) (waveInverseSolder a c)) x 2 0 2 0=c := by
  rw [wave_levi_civita,wave_curvature_formula]
  norm_num [waveConnection,waveTransverse,waveCovector,waveRaised,Pi.single_apply,
    Matrix.cons_val_two,Matrix.cons_val_three,Fin.isValue]

theorem wave_curvature_nonzero (a c : ℝ) (ha : a≠0) (x : Coordinate4) :
    coordinateCurvature (frameLeviCivita (waveSolder a c) (waveInverseSolder a c)) x 1 0≠0 := by
  intro h
  have hh := congrArg (fun M : Tensor4 => M 1 0) h
  apply ha
  simpa only [wave_first_curvature,Matrix.zero_apply] using hh

#print axioms wave_connection_linear
#print axioms wave_connection_jet
#print axioms wave_connection_commute
#print axioms wave_curvature_formula
#print axioms wave_ricci
#print axioms wave_scalar_curvature
#print axioms wave_einstein
#print axioms wave_first_curvature
#print axioms wave_second_curvature
#print axioms wave_curvature_nonzero
end
end ChatgptAudit.Wave029
