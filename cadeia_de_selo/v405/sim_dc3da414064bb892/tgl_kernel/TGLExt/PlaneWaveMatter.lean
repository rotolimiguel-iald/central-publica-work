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
import TGLExt.PlaneWaveCurvature

set_option autoImplicit false
set_option maxHeartbeats 8000000
set_option maxRecDepth 4096
namespace ChatgptAudit.Wave029
open Matrix Filter Topology Set TGLExt ChatgptAudit.Coherent023 ChatgptAudit.Response028
open scoped ContDiff Matrix.Norms.Elementwise
noncomputable section

def waveCovectorField (_x : Coordinate4) : Coordinate4 := waveCovector
def waveMatter (a c coupling : ℝ) : TensorField4 :=
  frameCovectorStress (waveSolder a c) (waveInverseSolder a c) waveCovectorField coupling

theorem wave_covector_smooth : SmoothVectorOn univ waveCovectorField :=
  fun _ => contDiffOn_const

theorem wave_covector_closed : ClosedCovectorOn univ waveCovectorField := by
  intro x _ i j
  simp [waveCovectorField,coordinatePartial]

theorem wave_covector_parallel (a c : ℝ) (x : Coordinate4) (i : Fin 4) :
    covectorDerivative (frameLeviCivita (waveSolder a c) (waveInverseSolder a c))
      waveCovectorField x i=0 := by
  rw [wave_levi_civita]
  ext j
  simp only [covectorDerivative,vectorPartial,waveCovectorField,Pi.sub_apply]
  simp only [coordinatePartial]
  fin_cases i <;> fin_cases j <;>
    norm_num [Matrix.mulVec,dotProduct,Fin.sum_univ_four,Matrix.transpose_apply,
      waveConnection,waveTransverse,waveCovector,waveRaised,
      Matrix.cons_val_two,Matrix.cons_val_three,Fin.isValue]

theorem wave_covector_wave (a c : ℝ) :
    CovectorWaveOn univ (inverseFrameMetricField (waveInverseSolder a c))
      (frameLeviCivita (waveSolder a c) (waveInverseSolder a c)) waveCovectorField := by
  intro x _
  simp only [covectorDivergence,wave_covector_parallel,Pi.zero_apply,mul_zero,
    Finset.sum_const_zero]

theorem wave_matter_formula (a c coupling : ℝ) (x : Coordinate4) :
    waveMatter a c coupling x=coupling • Matrix.vecMulVec waveCovector waveCovector := by
  change coupling • (Matrix.vecMulVec waveCovector waveCovector-
    (tensorQuad (inverseFrameMetricField (waveInverseSolder a c) x) waveCovector/2) •
      frameMetricField (waveSolder a c) x)=_
  rw [wave_inverse_metric_null]
  simp only [zero_div,zero_smul,sub_zero]

theorem wave_matter_smooth (a c coupling : ℝ) :
    SmoothMatrixOn univ (waveMatter a c coupling) := by
  have he : waveMatter a c coupling=
      fun _ => coupling • Matrix.vecMulVec waveCovector waveCovector := by
    funext x
    exact wave_matter_formula a c coupling x
  rw [he]
  exact fun _ _ => contDiffOn_const

theorem wave_matter_conserved (a c coupling : ℝ) :
    ∀ x∈(univ : Set Coordinate4), ∀ j,
      tensorFieldDivergence (inverseFrameMetricField (waveInverseSolder a c))
        (frameLeviCivita (waveSolder a c) (waveInverseSolder a c)) (waveMatter a c coupling) x j=0 :=
  frame_covector_stress_conserved univ isOpen_univ (waveSolder a c) (waveInverseSolder a c)
    waveCovectorField coupling
    (fun x _ => wave_solder_inverse a c x) (fun x _ => wave_inverse_solder a c x)
    (wave_solder_smooth a c) (wave_inverse_solder_smooth a c) wave_covector_smooth
    wave_covector_closed (wave_covector_wave a c)

theorem wave_matter_independent (a c a' c' coupling : ℝ) :
    waveMatter a c coupling=waveMatter a' c' coupling := by
  funext x
  rw [wave_matter_formula,wave_matter_formula]

theorem wave_matter_nonzero (a c coupling : ℝ) (hc : coupling≠0) (x : Coordinate4) :
    waveMatter a c coupling x≠0 := by
  intro h
  have hh := congrArg (fun M : Tensor4 => M 0 0) h
  rw [wave_matter_formula] at hh
  apply hc
  simpa [Matrix.vecMulVec,waveCovector] using hh

theorem wave_covector_potential :
    potentialCovector (fun x : Coordinate4 => x 0+x 3)=waveCovectorField := by
  funext x i
  have hf := (hasFDerivAt_apply (𝕜 := ℝ) 0 x).add (hasFDerivAt_apply (𝕜 := ℝ) 3 x)
  change HasFDerivAt (fun y : Coordinate4 => y 0+y 3) _ x at hf
  change fderiv ℝ (fun y : Coordinate4 => y 0+y 3) x (Pi.single i 1)=_
  rw [hf.fderiv]
  fin_cases i <;>
    norm_num [waveCovectorField,waveCovector,_root_.add_apply,ContinuousLinearMap.proj_apply,
      Pi.single_apply,Matrix.cons_val_two,Matrix.cons_val_three,Fin.isValue] <;> norm_num [Fin.ext_iff]

#print axioms waveCovectorField
#print axioms waveMatter
#print axioms wave_covector_smooth
#print axioms wave_covector_closed
#print axioms wave_covector_parallel
#print axioms wave_covector_wave
#print axioms wave_matter_formula
#print axioms wave_matter_smooth
#print axioms wave_matter_conserved
#print axioms wave_matter_independent
#print axioms wave_matter_nonzero
#print axioms wave_covector_potential
end
end ChatgptAudit.Wave029
