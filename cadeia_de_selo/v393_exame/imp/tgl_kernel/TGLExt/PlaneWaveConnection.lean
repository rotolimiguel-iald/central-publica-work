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
import TGLExt.PlaneWaveSolder

set_option autoImplicit false
set_option maxHeartbeats 8000000
set_option maxRecDepth 4096
namespace ChatgptAudit.Wave029
open Matrix Filter Topology Set TGLExt ChatgptAudit.Coherent023 ChatgptAudit.Response028
open scoped ContDiff Matrix.Norms.Elementwise
noncomputable section

def waveTransverse (a c : ℝ) (x : Coordinate4) : Coordinate4 := ![0,a*x 1,c*x 2,0]
def waveConnection (a c : ℝ) (x : Coordinate4) : ConnectionMatrix4 :=
  fun i r j => waveRaised r*(waveCovector j*waveTransverse a c x i+
    waveCovector i*waveTransverse a c x j)+
    waveTransverse a c x r*waveCovector i*waveCovector j

theorem wave_metric_jet (a c : ℝ) (x : Coordinate4) (i : Fin 4) :
    tensorFieldJet (frameMetricField (waveSolder a c)) x i=
      (2*waveTransverse a c x i) • Matrix.vecMulVec waveCovector waveCovector := by
  have he : frameMetricField (waveSolder a c)=
      fun y => eta4+waveProfile a c y • Matrix.vecMulVec waveCovector waveCovector := by
    funext y
    exact wave_metric_formula a c y
  rw [he]
  have hf : DifferentiableAt ℝ (waveProfile a c) x :=
    (wave_profile_smooth a c).differentiable (by simp) x
  rw [tensorFieldJet_add (fun _ => eta4)
    (fun y => waveProfile a c y • Matrix.vecMulVec waveCovector waveCovector) x
    (fun j k => differentiableAt_const (eta4 j k))
    (fun j k => hf.mul_const (Matrix.vecMulVec waveCovector waveCovector j k)),
    tensorFieldJet_smul (waveProfile a c) (fun _ => Matrix.vecMulVec waveCovector waveCovector)
      x hf (fun j k => differentiableAt_const (Matrix.vecMulVec waveCovector waveCovector j k))]
  have hz (M : Tensor4) : tensorFieldJet (fun _ => M) x=0 := by
    ext i j k
    simp [tensorFieldJet,coordinatePartial]
  simp only [hz,zero_add]
  rw [wave_profile_partial]
  fin_cases i <;> norm_num [Matrix.cons_val_two,Matrix.cons_val_three,Matrix.diagonal_apply,Matrix.one_apply,Fin.isValue,waveTransverse,Pi.single_apply] <;> norm_num [Fin.ext_iff] <;> ring

theorem wave_levi_civita (a c : ℝ) :
    frameLeviCivita (waveSolder a c) (waveInverseSolder a c)=waveConnection a c := by
  funext x i r j
  change (inverseFrameMetricField (waveInverseSolder a c) x *
    lowerChristoffelJet (tensorFieldJet (frameMetricField (waveSolder a c)) x) i) r j=_
  simp only [wave_inverse_metric_formula,Matrix.mul_apply,lowerChristoffelJet,wave_metric_jet]
  fin_cases i <;> fin_cases r <;> fin_cases j <;>
    norm_num [Matrix.cons_val_two,Matrix.cons_val_three,Matrix.diagonal_apply,Matrix.one_apply,Fin.isValue,waveConnection,waveTransverse,waveCovector,waveRaised,
      eta4,Matrix.vecMulVec,Fin.sum_univ_four] <;> norm_num [Fin.ext_iff] <;> ring

theorem wave_connection_smooth (a c : ℝ) : SmoothConnectionOn univ (waveConnection a c) := by
  intro i r j
  unfold waveConnection waveTransverse
  fin_cases i <;> fin_cases r <;> fin_cases j <;> dsimp <;> fun_prop

theorem wave_connection_torsion_free (a c : ℝ) (x : Coordinate4) (i j r : Fin 4) :
    waveConnection a c x i r j=waveConnection a c x j r i := by
  unfold waveConnection
  ring

theorem wave_transverse_partial (a c : ℝ) (x : Coordinate4) (i j : Fin 4) :
    coordinatePartial (fun y => waveTransverse a c y j) x i=
      if i=j then (if j=1 then a else if j=2 then c else 0) else 0 := by
  fin_cases j
  · simp [waveTransverse,coordinatePartial]
  · have hf := (hasFDerivAt_apply (𝕜 := ℝ) 1 x).const_mul a
    change fderiv ℝ (fun y : Coordinate4 => a*y 1) x (Pi.single i 1)=_
    rw [hf.fderiv]
    fin_cases i <;> norm_num [Matrix.cons_val_two,Matrix.cons_val_three,Matrix.diagonal_apply,Matrix.one_apply,Fin.isValue,Pi.single_apply]
  · have hf := (hasFDerivAt_apply (𝕜 := ℝ) 2 x).const_mul c
    change fderiv ℝ (fun y : Coordinate4 => c*y 2) x (Pi.single i 1)=_
    rw [hf.fderiv]
    fin_cases i <;> norm_num [Matrix.cons_val_two,Matrix.cons_val_three,Matrix.diagonal_apply,Matrix.one_apply,Fin.isValue,Pi.single_apply] <;> norm_num [Fin.ext_iff]
  · simp [waveTransverse,coordinatePartial]

#print axioms waveConnection
#print axioms wave_metric_jet
#print axioms wave_levi_civita
#print axioms wave_connection_smooth
#print axioms wave_connection_torsion_free
#print axioms wave_transverse_partial
end
end ChatgptAudit.Wave029
