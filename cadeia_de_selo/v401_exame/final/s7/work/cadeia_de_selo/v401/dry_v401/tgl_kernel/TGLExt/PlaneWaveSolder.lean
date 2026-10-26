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
import TGLExt.SummableGravityControls

set_option autoImplicit false
set_option maxHeartbeats 8000000
set_option maxRecDepth 4096
namespace ChatgptAudit.Wave029
open Matrix Filter Topology Set TGLExt ChatgptAudit.Coherent023 ChatgptAudit.Response028
open scoped ContDiff Matrix.Norms.Elementwise
noncomputable section

def waveCovector : Coordinate4 := ![1,0,0,1]
def waveRaised : Coordinate4 := ![1,0,0,-1]
def waveNilpotent : Tensor4 := Matrix.vecMulVec waveRaised waveCovector
def waveProfile (a c : ℝ) (x : Coordinate4) : ℝ := a*(x 1)^2+c*(x 2)^2
def waveSolder (a c : ℝ) (x : Coordinate4) : Tensor4 :=
  1+(waveProfile a c x/2) • waveNilpotent
def waveInverseSolder (a c : ℝ) (x : Coordinate4) : Tensor4 :=
  1-(waveProfile a c x/2) • waveNilpotent

theorem wave_covector_nonzero : waveCovector ≠ 0 := by
  intro h
  have hh := congrArg (fun v : Coordinate4 => v 0) h
  norm_num [Matrix.cons_val_two,Matrix.cons_val_three,Matrix.diagonal_apply,Matrix.one_apply,Fin.isValue,waveCovector] at hh

theorem wave_nilpotent_square : waveNilpotent*waveNilpotent=0 := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    norm_num [Matrix.cons_val_two,Matrix.cons_val_three,Matrix.diagonal_apply,Matrix.one_apply,Fin.isValue,waveNilpotent,waveCovector,waveRaised,Matrix.vecMulVec,Matrix.mul_apply,Fin.sum_univ_four]

theorem wave_solder_inverse (a c : ℝ) (x : Coordinate4) :
    waveSolder a c x*waveInverseSolder a c x=1 := by
  unfold waveSolder waveInverseSolder
  rw [add_mul,mul_sub,one_mul,one_mul,mul_sub,mul_one,Matrix.smul_mul,Matrix.mul_smul,
    wave_nilpotent_square,smul_zero,smul_zero,sub_zero]
  abel

theorem wave_inverse_solder (a c : ℝ) (x : Coordinate4) :
    waveInverseSolder a c x*waveSolder a c x=1 := by
  unfold waveSolder waveInverseSolder
  rw [sub_mul,one_mul,mul_add,mul_one,Matrix.smul_mul,Matrix.mul_smul,
    wave_nilpotent_square,smul_zero,smul_zero,add_zero]
  abel

theorem wave_metric_formula (a c : ℝ) (x : Coordinate4) :
    frameMetricField (waveSolder a c) x=
      eta4+waveProfile a c x • Matrix.vecMulVec waveCovector waveCovector := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    norm_num [Matrix.cons_val_two,Matrix.cons_val_three,Matrix.diagonal_apply,Matrix.one_apply,Fin.isValue,frameMetricField,waveSolder,waveNilpotent,waveCovector,waveRaised,
      eta4,Matrix.mul_apply,Fin.sum_univ_four,Matrix.vecMulVec] <;> norm_num [Fin.ext_iff] <;> ring

theorem wave_inverse_metric_formula (a c : ℝ) (x : Coordinate4) :
    inverseFrameMetricField (waveInverseSolder a c) x=
      eta4-waveProfile a c x • Matrix.vecMulVec waveRaised waveRaised := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    norm_num [Matrix.cons_val_two,Matrix.cons_val_three,Matrix.diagonal_apply,Matrix.one_apply,Fin.isValue,inverseFrameMetricField,waveInverseSolder,waveNilpotent,waveCovector,waveRaised,
      eta4,Matrix.mul_apply,Fin.sum_univ_four,Matrix.vecMulVec] <;> norm_num [Fin.ext_iff] <;> ring

theorem wave_profile_smooth (a c : ℝ) : ContDiff ℝ ∞ (waveProfile a c) := by
  unfold waveProfile
  fun_prop

theorem wave_solder_smooth (a c : ℝ) : SmoothMatrixOn univ (waveSolder a c) := by
  intro i j
  change ContDiffOn ℝ ∞ (fun x => (1 : Tensor4) i j+
    waveProfile a c x/2*waveNilpotent i j) univ
  have h : ContDiffOn ℝ ∞ (waveProfile a c) univ := (wave_profile_smooth a c).contDiffOn
  fun_prop

theorem wave_inverse_solder_smooth (a c : ℝ) : SmoothMatrixOn univ (waveInverseSolder a c) := by
  intro i j
  change ContDiffOn ℝ ∞ (fun x => (1 : Tensor4) i j-
    waveProfile a c x/2*waveNilpotent i j) univ
  have h : ContDiffOn ℝ ∞ (waveProfile a c) univ := (wave_profile_smooth a c).contDiffOn
  fun_prop

theorem wave_profile_partial (a c : ℝ) (x : Coordinate4) (i : Fin 4) :
    coordinatePartial (waveProfile a c) x i=
      2*a*x 1*(Pi.single i (1:ℝ) : Coordinate4) 1+
      2*c*x 2*(Pi.single i (1:ℝ) : Coordinate4) 2 := by
  have hf := (((hasFDerivAt_apply (𝕜 := ℝ) 1 x).pow 2).const_mul a).add
    (((hasFDerivAt_apply (𝕜 := ℝ) 2 x).pow 2).const_mul c)
  change HasFDerivAt (fun y : Coordinate4 => a*(y 1)^2+c*(y 2)^2) _ x at hf
  unfold coordinatePartial waveProfile
  rw [hf.fderiv]
  simp only [_root_.add_apply,_root_.smul_apply,smul_eq_mul,
    ContinuousLinearMap.proj_apply]
  norm_num
  ring

theorem wave_metric_at_origin (a c : ℝ) :
    frameMetricField (waveSolder a c) 0=eta4 := by
  rw [wave_metric_formula]
  simp [waveProfile]

theorem wave_inverse_metric_null (a c : ℝ) (x : Coordinate4) :
    tensorQuad (inverseFrameMetricField (waveInverseSolder a c) x) waveCovector=0 := by
  rw [wave_inverse_metric_formula]
  norm_num [Matrix.cons_val_two,Matrix.cons_val_three,Matrix.diagonal_apply,Matrix.one_apply,Fin.isValue,tensorQuad,Matrix.mulVec,dotProduct,Fin.sum_univ_four,eta4,
    Matrix.vecMulVec,waveCovector,waveRaised]
  norm_num [Fin.ext_iff]

#print axioms waveCovector
#print axioms waveRaised
#print axioms waveSolder
#print axioms waveInverseSolder
#print axioms wave_covector_nonzero
#print axioms wave_nilpotent_square
#print axioms wave_solder_inverse
#print axioms wave_inverse_solder
#print axioms wave_metric_formula
#print axioms wave_inverse_metric_formula
#print axioms wave_profile_smooth
#print axioms wave_solder_smooth
#print axioms wave_inverse_solder_smooth
#print axioms wave_profile_partial
#print axioms wave_metric_at_origin
#print axioms wave_inverse_metric_null
end
end ChatgptAudit.Wave029
