-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_036 (06/09/2026), transposta em 06/09/2026
-- Lote 035..037 (processo da ORDEM_008 cumprido pela bancada: zero instancias anonimas, lote compilado junto
--   num diretorio limpo). 035: DEFORMACOES OBSERVAVEIS e AREA DE FISHER — derivadas da conjugacao unitaria e
--   do estado, observaveis de Pauli por sitio na torre real, duas leituras independentes (jacobiano nao
--   degenerado), medicao conjunta efetiva (sitios distintos), probabilidades normalizadas e suas derivadas,
--   matriz de Fisher na origem, densidade de area de Fisher (4/9 como area de coordenadas). 036: AREA OPTICA e
--   LIBERDADE RADIATIVA — a area induzida dos campos de Jacobi da metrica 029 ligada a curvatura real
--   (A2(0) = -Ric(d,d); A4(0) = 2(tr K)^2 - 2 tr(K_TF^T K_TF)); germes de area distintos para shears
--   distintos. 037: QUARTA ORDEM, AREA e RELOGIO — limites entropicos e de area em 4a ordem; NEGATIVO
--   MEDIDO: o casamento adicional em 4a ordem com parametro comum fixo FALHA (delta4 >= (7/48) B > 0);
--   a reparametrizacao do relogio t + lambda t^3 cancela o defeito ate 4a ordem (controle do relogio relativo).
--   Estatuto [REAL / DERIVED / INPUT / OPEN]: X, Y, sitios e normalizacao sao INPUT; a familia optica
--   lorentziana e INPUT; identificacao da inscricao angular com area fisica, retorno estabilizador, ponte
--   regiao-algebra, escala, assinatura, dinamica gravitacional e H3 geral NAO pagos.
-- Auditoria da gerencia (sessao d554e796, 06/09/2026): hashes 14/14, 8/8 (via manifesto), 10/10; manifestos
--   1051/977; 3/3 auditores exit 0; recompilacao INDEPENDENTE 15/15, axiomas no trio; guarda de colisao;
--   enunciados lidos. Transposicao: cabecalho + prefixo TGLExt. (+ regra 3, sem efeito: zero anonimas).
-- NAO move gate; nao e fisica; NOT_FALSIFIED nunca e CONFIRMED; CONFIRMADA proibido.
-- ---------------------------------------------------------------------
import TGLExt.PlaneWaveCurvature

set_option autoImplicit false
set_option maxHeartbeats 8000000
set_option maxRecDepth 4096

namespace ChatgptAudit.Optical036
open Matrix TGLExt ChatgptAudit ChatgptAudit.Wave029 ChatgptAudit.Screen015
noncomputable section

/-- The affine normalization is waveCovector(d) = 1. -/
def centralNullDirection : Coordinate4 := ![1/2,0,0,1/2]

def centralNullCurve (t : ℝ) : Coordinate4 := t • centralNullDirection

def transverseScreenVector (i : Fin 2) : Coordinate4 :=
  ![![0,1,0,0], ![0,0,1,0]] i

def transverseScreenColumns : ScreenVectors :=
  fun r i => transverseScreenVector i r

/-- R(u,v)w, with R_ij = partial_i Gamma_j - partial_j Gamma_i + [Gamma_i,Gamma_j]. -/
def curvatureAction (Gamma : ConnectionField4) (x u v w : Coordinate4) : Coordinate4 :=
  ∑ i, ∑ j, (u i * v j) • ((coordinateCurvature Gamma x i j).mulVec w)

/-- K(e_j) = R(e_j,d)d. The minus sign uses the positive metric on the spacelike screen.
The associated Jacobi equation has the convention J'' + K J = 0. -/
def opticalTidalMatrix (a c : ℝ) (x : Coordinate4) : ScreenMatrix :=
  fun i j => -tensorPair (frameMetricField (waveSolder a c) x)
    (transverseScreenVector i)
    (curvatureAction (frameLeviCivita (waveSolder a c) (waveInverseSolder a c)) x
      (transverseScreenVector j) centralNullDirection centralNullDirection)

def opticalTidalTraceFree (a c : ℝ) (x : Coordinate4) : ScreenMatrix :=
  opticalTidalMatrix a c x - (Matrix.trace (opticalTidalMatrix a c x)/2) • 1

/-- Squared Frobenius norm in the displayed orthonormal screen. -/
def opticalTidalTraceFreeNormSq (a c : ℝ) (x : Coordinate4) : ℝ :=
  Matrix.trace ((opticalTidalTraceFree a c x)ᵀ * opticalTidalTraceFree a c x)

theorem central_direction_frequency :
    dotProduct waveCovector centralNullDirection = 1 := by
  norm_num [waveCovector,centralNullDirection,dotProduct,Fin.sum_univ_four,
    Matrix.cons_val_two,Matrix.cons_val_three]

theorem central_direction_nonzero : centralNullDirection ≠ 0 := by
  intro h
  have hh := congrArg (fun v : Coordinate4 => v 0) h
  norm_num [centralNullDirection] at hh

theorem central_curve_metric (a c t : ℝ) :
    frameMetricField (waveSolder a c) (centralNullCurve t) = eta4 := by
  rw [wave_metric_formula]
  simp [waveProfile,centralNullCurve,centralNullDirection,Matrix.cons_val_two]

theorem central_curve_null (a c t : ℝ) :
    tensorQuad (frameMetricField (waveSolder a c) (centralNullCurve t))
      centralNullDirection = 0 := by
  rw [central_curve_metric]
  norm_num [tensorQuad,centralNullDirection,eta4,Matrix.mulVec,dotProduct,
    Fin.sum_univ_four,Matrix.cons_val_two,Matrix.cons_val_three,Matrix.diagonal_apply,
    Fin.isValue]

theorem central_curve_derivative (t : ℝ) :
    HasDerivAt centralNullCurve centralNullDirection t := by
  change HasDerivAt (fun s : ℝ => s • centralNullDirection) centralNullDirection t
  simpa only [one_smul,id_eq] using
    (hasDerivAt_id t).smul_const centralNullDirection

theorem central_curve_connection_zero (a c t : ℝ) :
    frameLeviCivita (waveSolder a c) (waveInverseSolder a c) (centralNullCurve t) = 0 := by
  rw [wave_levi_civita]
  ext i r j
  fin_cases i <;> fin_cases r <;> fin_cases j <;>
    norm_num [waveConnection,waveTransverse,waveCovector,waveRaised,
      centralNullCurve,centralNullDirection,Matrix.cons_val_two,Matrix.cons_val_three,
      Fin.isValue]

theorem central_curve_acceleration_zero (a c t : ℝ) :
    sprayAcceleration (frameLeviCivita (waveSolder a c) (waveInverseSolder a c))
      (centralNullCurve t) centralNullDirection = 0 := by
  simp [sprayAcceleration,connectionAlong,central_curve_connection_zero]

/-- The actual position and velocity equations for the Levi-Civita geodesic. -/
theorem central_curve_geodesic (a c t : ℝ) :
    HasDerivAt centralNullCurve centralNullDirection t ∧
    HasDerivAt (fun _ : ℝ => centralNullDirection)
      (sprayAcceleration (frameLeviCivita (waveSolder a c) (waveInverseSolder a c))
        (centralNullCurve t) centralNullDirection) t := by
  constructor
  · exact central_curve_derivative t
  · rw [central_curve_acceleration_zero]
    exact hasDerivAt_const t centralNullDirection

theorem transverse_screen_null_orthogonal (a c t : ℝ) (i : Fin 2) :
    tensorPair (frameMetricField (waveSolder a c) (centralNullCurve t))
      centralNullDirection (transverseScreenVector i) = 0 := by
  rw [central_curve_metric]
  fin_cases i <;>
    norm_num [tensorPair,centralNullDirection,transverseScreenVector,eta4,
      Matrix.mulVec,dotProduct,Fin.sum_univ_four,Matrix.cons_val_two,
      Matrix.cons_val_three,Matrix.diagonal_apply,Fin.isValue]

theorem transverse_screen_gram (a c : ℝ) (x : Coordinate4) :
    screenGram (frameMetricField (waveSolder a c) x) transverseScreenColumns =
      -(1 : ScreenMatrix) := by
  rw [wave_metric_formula]
  ext i j
  fin_cases i <;> fin_cases j <;>
    norm_num [screenGram,transverseScreenColumns,transverseScreenVector,
      eta4,waveCovector,Matrix.vecMulVec,Matrix.mul_apply,Fin.sum_univ_four,
      Matrix.cons_val_two,Matrix.cons_val_three,Matrix.diagonal_apply,
      Matrix.one_apply,Fin.isValue]

/-- The contraction uses the full Riemann tensor of the existing Levi-Civita connection. -/
theorem optical_tidal_action (a c : ℝ) (x : Coordinate4) (i : Fin 2) :
    curvatureAction (frameLeviCivita (waveSolder a c) (waveInverseSolder a c)) x
      (transverseScreenVector i) centralNullDirection centralNullDirection =
        (if i=0 then a else c) • transverseScreenVector i := by
  rw [wave_levi_civita]
  ext r
  fin_cases i <;> fin_cases r <;>
    norm_num [curvatureAction,wave_curvature_formula,transverseScreenVector,
      centralNullDirection,Matrix.mulVec,dotProduct,Fin.sum_univ_four,
      waveConnection,waveTransverse,waveCovector,waveRaised,Pi.single_apply,
      Matrix.cons_val_two,Matrix.cons_val_three,Fin.isValue] <;>
    norm_num [Fin.ext_iff] <;> ring

theorem optical_tidal_diagonal (a c : ℝ) (x : Coordinate4) :
    opticalTidalMatrix a c x = !![a,0;0,c] := by
  ext i j
  simp only [opticalTidalMatrix,optical_tidal_action,wave_metric_formula]
  fin_cases i <;> fin_cases j <;>
    norm_num [tensorPair,transverseScreenVector,eta4,waveCovector,
      Matrix.vecMulVec,Matrix.mulVec,dotProduct,Fin.sum_univ_four,
      Matrix.cons_val_two,Matrix.cons_val_three,Matrix.diagonal_apply,Fin.isValue]

theorem optical_tidal_trace (a c : ℝ) (x : Coordinate4) :
    Matrix.trace (opticalTidalMatrix a c x) = a+c := by
  rw [optical_tidal_diagonal]
  simp [Matrix.trace]

/-- The trace is the Ricci contraction in the same normalized null direction. -/
theorem optical_tidal_trace_eq_ricci (a c : ℝ) (x : Coordinate4) :
    Matrix.trace (opticalTidalMatrix a c x) =
      tensorQuad (coordinateRicci
        (frameLeviCivita (waveSolder a c) (waveInverseSolder a c)) x)
        centralNullDirection := by
  rw [optical_tidal_trace,wave_ricci]
  norm_num [tensorQuad,centralNullDirection,waveCovector,Matrix.vecMulVec,
    Matrix.mulVec,dotProduct,Fin.sum_univ_four,Matrix.cons_val_two,Matrix.cons_val_three]
  ring

theorem optical_tidal_tracefree_diagonal (a c : ℝ) (x : Coordinate4) :
    opticalTidalTraceFree a c x = !![(a-c)/2,0;0,(c-a)/2] := by
  unfold opticalTidalTraceFree
  rw [optical_tidal_trace,optical_tidal_diagonal]
  ext i j
  fin_cases i <;> fin_cases j <;>
    norm_num [Matrix.one_apply,Matrix.diagonal_apply,Fin.isValue] <;> ring

theorem optical_tidal_tracefree_norm_sq (a c : ℝ) (x : Coordinate4) :
    opticalTidalTraceFreeNormSq a c x = (a-c)^2/2 := by
  unfold opticalTidalTraceFreeNormSq
  rw [optical_tidal_tracefree_diagonal]
  norm_num [Matrix.trace,Matrix.mul_apply,Fin.sum_univ_two]
  ring

theorem optical_tidal_tracefree_norm_sq_nonnegative (a c : ℝ) (x : Coordinate4) :
    0 ≤ opticalTidalTraceFreeNormSq a c x := by
  rw [optical_tidal_tracefree_norm_sq]
  positivity

theorem optical_tidal_tracefree_norm_sq_zero_iff (a c : ℝ) (x : Coordinate4) :
    opticalTidalTraceFreeNormSq a c x = 0 ↔ a=c := by
  rw [optical_tidal_tracefree_norm_sq]
  constructor
  · intro h
    nlinarith [sq_nonneg (a-c)]
  · intro h
    simp [h]

#print axioms centralNullDirection
#print axioms centralNullCurve
#print axioms transverseScreenVector
#print axioms transverseScreenColumns
#print axioms curvatureAction
#print axioms opticalTidalMatrix
#print axioms opticalTidalTraceFree
#print axioms opticalTidalTraceFreeNormSq
#print axioms central_direction_frequency
#print axioms central_direction_nonzero
#print axioms central_curve_metric
#print axioms central_curve_null
#print axioms central_curve_derivative
#print axioms central_curve_connection_zero
#print axioms central_curve_acceleration_zero
#print axioms central_curve_geodesic
#print axioms transverse_screen_null_orthogonal
#print axioms transverse_screen_gram
#print axioms optical_tidal_action
#print axioms optical_tidal_diagonal
#print axioms optical_tidal_trace
#print axioms optical_tidal_trace_eq_ricci
#print axioms optical_tidal_tracefree_diagonal
#print axioms optical_tidal_tracefree_norm_sq
#print axioms optical_tidal_tracefree_norm_sq_nonnegative
#print axioms optical_tidal_tracefree_norm_sq_zero_iff

end
end ChatgptAudit.Optical036
