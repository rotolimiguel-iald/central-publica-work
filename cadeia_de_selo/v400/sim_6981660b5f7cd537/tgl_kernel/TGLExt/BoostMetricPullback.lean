-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_044 (06/09/2026), transposta em 06/09/2026
-- Lote 044..045 (ORDEM_008 cumprida). 044: BOOST APROXIMADO e orientacao do calor — o peso -kappa t realizado
--   por um campo de boost chi = -kappa u d_u + kappa v d_v e seu fluxo (grupo, inversa, jacobiano); pullback da
--   metrica e defeito de Lie -2kappa(aX^2+cY^2)du^2 (zera com o 1o jato na central); controle negativo: nao e
--   Killing em aberto se kappa != 0 e (a,c) != 0; T(chi,d) = -kappa t T(d,d); Q_boost = opticalHeat041 globalmente,
--   = opticalScreenHeat043 como germe; orientacao do passado certificada (calor e area invertem sinal juntos).
--   045 (resposta a ORDEM_010): swapHorizon P p hp i j — troca de sitios no perfil estacionario e um TowerHorizon
--   por prova (unitario, normaliza M, preserva omega); permutacoes finitas com lei de grupo e covariancia das
--   esperancas estacionaria/tracial (horizontes algebricos; identificacao fisica OPEN); shift unilateral NAO
--   construido; aperiodico OPEN (rota Cesaro nomeada); StateClock: classe cinematica (origem, derivada 1, jato) —
--   DICOTOMIA: para todo relogio comum g alguma tela falha (duas telas sigma = 0, r/4, mesmo estado e Ricci:
--   diferenca dos residuos/t^4 -> +eta r^2/96), cada tela isolada admite relogio que cancela a 4a ordem;
--   area: covariancia por horizontes NAO fixa a normalizacao (h e alpha h ambos invariantes; area x alpha).
--   Estatuto [REAL / DERIVED / INPUT / OPEN]: familia, carta e kappa sao INPUT; kappa/(2pi) e normalizacao
--   herdada (sem Unruh/KMS); H3 fisico, lei finita geral, ponte regiao-algebra, shift e aperiodico OPEN.
-- Auditoria da gerencia (sessao d554e796, 06/09/2026): hashes 10/10 + 8/8; 2/2 auditores exit 0;
--   recompilacao INDEPENDENTE 8/8, axiomas no trio; guarda de colisao; enunciados lidos.
--   Transposicao: cabecalho + prefixo TGLExt. (+ regra 3, sem efeito). As fontes v329 (gerencia) NAO sao
--   reincorporadas: a bancada as recompilou como dependencia, sem novidade contada.
-- NAO move gate; nao e fisica; NOT_FALSIFIED nunca e CONFIRMED; CONFIRMADA proibido.
-- ---------------------------------------------------------------------
import TGLExt.ApproximateBoostFlow

set_option autoImplicit false
set_option maxHeartbeats 12000000
set_option maxRecDepth 4096

namespace ChatgptAudit.Boost044
open Matrix Filter Set TGLExt ChatgptAudit ChatgptAudit.Wave029
  ChatgptAudit.Optical036 ChatgptAudit.Optical043
open scoped Topology ContDiff Matrix.Norms.Elementwise
noncomputable section

/-- Pullback by the actual linear boost flow and its certified spatial Jacobian. -/
def boostMetricPullback (a c rate s : ℝ) (x : Coordinate4) : Tensor4 :=
  (boostMatrix rate s)ᵀ *
    frameMetricField (waveSolder a c) (boostFlow rate s x) * boostMatrix rate s

/-- The coordinate Lie derivative uses the actual scalar and vector partial derivatives. -/
def coordinateMetricLie (g : TensorField4) (V : VectorField4) : TensorField4 :=
  fun x i j =>
    scalarAlong V (fun y => g y i j) x +
    (∑ k, g x k j * vectorPartial V x i k) +
    ∑ k, g x i k * vectorPartial V x j k

theorem boost_wave_profile (a c rate s : ℝ) (x : Coordinate4) :
    waveProfile a c (boostFlow rate s x)=waveProfile a c x := by
  simp only [waveProfile,boost_flow_one,boost_flow_two]

theorem boost_wave_covector_pullback (rate s : ℝ) :
    (boostMatrix rate s)ᵀ * Matrix.vecMulVec waveCovector waveCovector *
      boostMatrix rate s =
      Real.exp (-2*rate*s) • Matrix.vecMulVec waveCovector waveCovector := by
  have hv : waveCovector ᵥ* boostMatrix rate s =
      Real.exp (-rate*s) • waveCovector := by
    calc
      waveCovector ᵥ* boostMatrix rate s =
          (boostMatrix rate s)ᵀ *ᵥ waveCovector := by
        simpa only [Matrix.transpose_transpose] using
          (Matrix.vecMul_transpose (boostMatrix rate s)ᵀ waveCovector)
      _ = _ := boost_matrix_covector rate s
  rw [Matrix.mul_vecMulVec,Matrix.vecMulVec_mul,boost_matrix_covector,hv]
  have he : Real.exp (-rate*s)*Real.exp (-rate*s)=Real.exp (-2*rate*s) := by
    rw [← Real.exp_add]
    congr 1
    ring
  ext i j
  simp only [Matrix.vecMulVec_apply,Pi.smul_apply,smul_eq_mul]
  calc
    (Real.exp (-rate*s)*waveCovector i)*(Real.exp (-rate*s)*waveCovector j) =
        (Real.exp (-rate*s)*Real.exp (-rate*s))*(waveCovector i*waveCovector j) := by ring
    _ = Real.exp (-2*rate*s)*(waveCovector i*waveCovector j) := by rw [he]

/-- Exact pullback identity for arbitrary real profile coefficients. -/
theorem boost_metric_pullback_formula (a c rate s : ℝ) (x : Coordinate4) :
    boostMetricPullback a c rate s x =
      frameMetricField (waveSolder a c) x +
        ((Real.exp (-2*rate*s)-1)*waveProfile a c x) •
          Matrix.vecMulVec waveCovector waveCovector := by
  rw [boostMetricPullback,wave_metric_formula,boost_wave_profile,mul_add,add_mul,
    Matrix.mul_smul,Matrix.smul_mul,boost_matrix_flat_preserving,
    boost_wave_covector_pullback,wave_metric_formula]
  ext i j
  simp only [Matrix.add_apply,Matrix.smul_apply,smul_eq_mul]
  ring

theorem boost_metric_scalar_along (a c rate : ℝ) (x : Coordinate4) (i j : Fin 4) :
    scalarAlong (boostField rate)
      (fun y => frameMetricField (waveSolder a c) y i j) x=0 := by
  change (∑ k, boostField rate x k *
    tensorFieldJet (frameMetricField (waveSolder a c)) x k i j)=0
  simp only [Fin.sum_univ_four,wave_metric_jet]
  norm_num [boostField,waveTransverse,Matrix.smul_apply,
    Matrix.cons_val_two,Matrix.cons_val_three]

/-- The Lie defect is computed from derivatives, independently of its pullback description. -/
theorem boost_metric_lie_formula (a c rate : ℝ) (x : Coordinate4) :
    coordinateMetricLie (frameMetricField (waveSolder a c)) (boostField rate) x =
      (-2*rate*waveProfile a c x) • Matrix.vecMulVec waveCovector waveCovector := by
  ext i j
  unfold coordinateMetricLie
  rw [boost_metric_scalar_along,zero_add]
  simp only [boost_field_partial,wave_metric_formula,Fin.sum_univ_four]
  fin_cases i <;> fin_cases j <;>
    norm_num [boostGenerator,eta4,waveCovector,Matrix.vecMulVec,
      Matrix.diagonal_apply,Matrix.cons_val_two,Matrix.cons_val_three,Fin.ext_iff]
  all_goals ring

/-- Differentiating the actual pullback at zero gives the coordinate Lie derivative. -/
theorem boost_metric_pullback_derivative_zero (a c rate : ℝ) (x : Coordinate4) :
    HasMatrixDerivAt (fun s => boostMetricPullback a c rate s x)
      (coordinateMetricLie (frameMetricField (waveSolder a c)) (boostField rate) x) 0 := by
  intro i j
  have he : HasDerivAt (fun s : ℝ => Real.exp (-2*rate*s)) (-2*rate) 0 := by
    simpa using ((hasDerivAt_id (0:ℝ)).const_mul (-2*rate)).exp
  have hd := ((he.sub_const 1).mul_const
    (waveProfile a c x*Matrix.vecMulVec waveCovector waveCovector i j)).const_add
      (frameMetricField (waveSolder a c) x i j)
  have hf : (fun s => boostMetricPullback a c rate s x i j) =
      (fun s => frameMetricField (waveSolder a c) x i j +
        (Real.exp (-2*rate*s)-1)*
          (waveProfile a c x*Matrix.vecMulVec waveCovector waveCovector i j)) := by
    funext s
    rw [boost_metric_pullback_formula]
    simp only [Matrix.add_apply,Matrix.smul_apply,smul_eq_mul]
    ring
  rw [hf,boost_metric_lie_formula]
  apply hd.congr_deriv
  simp only [Matrix.smul_apply,smul_eq_mul]
  ring

#print axioms boostMetricPullback
#print axioms coordinateMetricLie
#print axioms boost_wave_profile
#print axioms boost_wave_covector_pullback
#print axioms boost_metric_pullback_formula
#print axioms boost_metric_scalar_along
#print axioms boost_metric_lie_formula
#print axioms boost_metric_pullback_derivative_zero
end
end ChatgptAudit.Boost044
