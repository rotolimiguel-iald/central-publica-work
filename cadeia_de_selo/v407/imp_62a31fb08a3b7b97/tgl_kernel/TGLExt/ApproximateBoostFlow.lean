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
import TGLExt.OpticalConstructedHeat

set_option autoImplicit false
set_option maxHeartbeats 8000000
set_option maxRecDepth 4096

namespace ChatgptAudit.Boost044
open Matrix Filter Set TGLExt ChatgptAudit ChatgptAudit.Wave029
  ChatgptAudit.Optical036 ChatgptAudit.Optical043
open scoped Topology ContDiff Matrix.Norms.Elementwise
noncomputable section

/-- The affine boost field in the original plane-wave coordinates. -/
def boostField (rate : ℝ) (x : Coordinate4) : Coordinate4 :=
  ![-rate * x 3, 0, 0, -rate * x 0]

def boostGenerator (rate : ℝ) : Tensor4 :=
  !![0,0,0,-rate; 0,0,0,0; 0,0,0,0; -rate,0,0,0]

def boostEven (rate s : ℝ) : ℝ :=
  (Real.exp (-rate*s) + Real.exp (rate*s))/2

def boostOdd (rate s : ℝ) : ℝ :=
  (Real.exp (-rate*s) - Real.exp (rate*s))/2

/-- The actual differential of the finite boost map. -/
def boostMatrix (rate s : ℝ) : Tensor4 :=
  !![boostEven rate s,0,0,boostOdd rate s;
    0,1,0,0; 0,0,1,0;
    boostOdd rate s,0,0,boostEven rate s]

def boostFlow (rate s : ℝ) (x : Coordinate4) : Coordinate4 :=
  (boostMatrix rate s).mulVec x

/-- Matrix action as a continuous linear map on the same coordinate space. -/
def boostMatrixAction (M : Tensor4) : Coordinate4 →L[ℝ] Coordinate4 :=
  ContinuousLinearMap.pi (fun i =>
    ∑ j : Fin 4, M i j •
      (ContinuousLinearMap.proj j : Coordinate4 →L[ℝ] ℝ))

theorem boost_matrix_action_apply (M : Tensor4) (x : Coordinate4) :
    boostMatrixAction M x = M.mulVec x := by
  ext i
  simp [boostMatrixAction, Matrix.mulVec, dotProduct]

theorem boost_even_add_odd (rate s : ℝ) :
    boostEven rate s + boostOdd rate s = Real.exp (-rate*s) := by
  unfold boostEven boostOdd
  ring

theorem boost_even_sub_odd (rate s : ℝ) :
    boostEven rate s - boostOdd rate s = Real.exp (rate*s) := by
  unfold boostEven boostOdd
  ring

theorem boost_exponential_product (rate s : ℝ) :
    Real.exp (-rate*s) * Real.exp (rate*s) = 1 := by
  rw [← Real.exp_add]
  have he : -rate*s + rate*s = 0 := by ring
  rw [he, Real.exp_zero]

theorem boost_coeff_hyperbolic (rate s : ℝ) :
    boostEven rate s ^ 2 - boostOdd rate s ^ 2 = 1 := by
  calc
    boostEven rate s ^ 2 - boostOdd rate s ^ 2 =
        Real.exp (-rate*s) * Real.exp (rate*s) := by
      unfold boostEven boostOdd
      ring
    _ = 1 := boost_exponential_product rate s

theorem boost_even_add (rate s t : ℝ) :
    boostEven rate (s+t) =
      boostEven rate s * boostEven rate t + boostOdd rate s * boostOdd rate t := by
  unfold boostEven boostOdd
  rw [show -rate*(s+t) = -rate*s + -rate*t by ring,
    show rate*(s+t) = rate*s + rate*t by ring, Real.exp_add, Real.exp_add]
  ring

theorem boost_odd_add (rate s t : ℝ) :
    boostOdd rate (s+t) =
      boostEven rate s * boostOdd rate t + boostOdd rate s * boostEven rate t := by
  unfold boostEven boostOdd
  rw [show -rate*(s+t) = -rate*s + -rate*t by ring,
    show rate*(s+t) = rate*s + rate*t by ring, Real.exp_add, Real.exp_add]
  ring

theorem boost_even_hasDerivAt (rate s : ℝ) :
    HasDerivAt (boostEven rate) (-rate * boostOdd rate s) s := by
  have hm := ((hasDerivAt_id s).const_mul (-rate)).exp
  have hp := ((hasDerivAt_id s).const_mul rate).exp
  have h := (hm.add hp).div_const 2
  convert h using 1
  all_goals first | rfl | (dsimp [boostEven, boostOdd]; ring)

theorem boost_odd_hasDerivAt (rate s : ℝ) :
    HasDerivAt (boostOdd rate) (-rate * boostEven rate s) s := by
  have hm := ((hasDerivAt_id s).const_mul (-rate)).exp
  have hp := ((hasDerivAt_id s).const_mul rate).exp
  have h := (hm.sub hp).div_const 2
  convert h using 1
  all_goals first | rfl | (dsimp [boostEven, boostOdd]; ring)

theorem boost_field_smooth (rate : ℝ) :
    SmoothVectorOn Set.univ (boostField rate) := by
  intro i
  fin_cases i <;> dsimp [boostField] <;> fun_prop

theorem boost_field_origin (rate : ℝ) : boostField rate 0 = 0 := by
  ext i
  fin_cases i <;> simp [boostField]

theorem boost_field_central (rate t : ℝ) :
    boostField rate (centralNullCurve t) = (-rate*t) • centralNullDirection := by
  ext i
  fin_cases i <;>
    simp [boostField, centralNullCurve, centralNullDirection] <;> ring

theorem boost_field_future_central (rate t : ℝ) (hrate : 0 < rate) (ht : t < 0) :
    0 < boostField rate (centralNullCurve t) 0 := by
  rw [boost_field_central]
  change 0 < (-rate*t) * (1/2 : ℝ)
  nlinarith [mul_pos hrate (neg_pos.mpr ht)]

theorem boost_field_frequency (rate : ℝ) (x : Coordinate4) :
    dotProduct waveCovector (boostField rate x) = -rate * opticalPhaseCoordinate x := by
  norm_num [dotProduct, Fin.sum_univ_four, waveCovector, boostField,
    opticalPhaseCoordinate, Matrix.cons_val_two, Matrix.cons_val_three]
  ring

theorem boost_field_as_linear (rate : ℝ) :
    boostField rate = (boostMatrixAction (boostGenerator rate) : Coordinate4 → Coordinate4) := by
  funext x
  rw [boost_matrix_action_apply]
  ext i
  fin_cases i <;>
    simp [boostField, boostGenerator, Matrix.mulVec, dotProduct, Fin.sum_univ_four]

theorem boost_field_hasFDerivAt (rate : ℝ) (x : Coordinate4) :
    HasFDerivAt (boostField rate) (boostMatrixAction (boostGenerator rate)) x := by
  rw [boost_field_as_linear]
  exact (boostMatrixAction (boostGenerator rate)).hasFDerivAt

theorem boost_field_partial (rate : ℝ) (x : Coordinate4) (i : Fin 4) :
    vectorPartial (boostField rate) x i = (fun j => boostGenerator rate j i) := by
  ext j
  have h := hasFDerivAt_pi'.mp (boost_field_hasFDerivAt rate x) j
  change fderiv ℝ (fun y : Coordinate4 => boostField rate y j) x (Pi.single i 1) =
    boostGenerator rate j i
  rw [h.fderiv]
  change (boostMatrixAction (boostGenerator rate) (Pi.single i 1)) j =
    boostGenerator rate j i
  rw [boost_matrix_action_apply, Matrix.mulVec_single_one]
  rfl

theorem boost_matrix_zero (rate : ℝ) : boostMatrix rate 0 = 1 := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    norm_num [boostMatrix, boostEven, boostOdd, Matrix.one_apply]

theorem boost_matrix_add (rate s t : ℝ) :
    boostMatrix rate (s+t) = boostMatrix rate s * boostMatrix rate t := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    norm_num [boostMatrix, Matrix.mul_apply, Fin.sum_univ_four,
      boost_even_add, boost_odd_add, Matrix.cons_val_two, Matrix.cons_val_three] <;> ring

theorem boost_matrix_mul_neg (rate s : ℝ) :
    boostMatrix rate s * boostMatrix rate (-s) = 1 := by
  rw [← boost_matrix_add, add_neg_cancel, boost_matrix_zero]

theorem boost_matrix_neg_mul (rate s : ℝ) :
    boostMatrix rate (-s) * boostMatrix rate s = 1 := by
  rw [← boost_matrix_add, neg_add_cancel, boost_matrix_zero]

theorem boost_matrix_hasDerivAt (rate s : ℝ) :
    HasDerivAt (boostMatrix rate) (boostGenerator rate * boostMatrix rate s) s := by
  apply hasDerivAt_pi.2
  intro i
  apply hasDerivAt_pi.2
  intro j
  fin_cases i <;> fin_cases j <;>
    norm_num [boostMatrix, boostGenerator, Matrix.mul_apply, Fin.sum_univ_four,
      Matrix.cons_val_two, Matrix.cons_val_three] <;>
    first
    | simpa only [neg_mul] using boost_even_hasDerivAt rate s
    | simpa only [neg_mul] using boost_odd_hasDerivAt rate s
    | exact hasDerivAt_const s (0 : ℝ)
    | exact hasDerivAt_const s (1 : ℝ)

theorem boost_matrix_hasDerivAt_zero (rate : ℝ) :
    HasDerivAt (boostMatrix rate) (boostGenerator rate) 0 := by
  simpa only [boost_matrix_zero, mul_one] using boost_matrix_hasDerivAt rate 0

theorem boost_flow_coordinates (rate s : ℝ) (x : Coordinate4) :
    boostFlow rate s x =
      ![boostEven rate s * x 0 + boostOdd rate s * x 3,
        x 1, x 2, boostOdd rate s * x 0 + boostEven rate s * x 3] := by
  ext i
  fin_cases i <;> simp [boostFlow, boostMatrix, Matrix.mulVec, dotProduct, Fin.sum_univ_four]

theorem boost_flow_zero (rate : ℝ) (x : Coordinate4) : boostFlow rate 0 x = x := by
  simp [boostFlow, boost_matrix_zero]

theorem boost_flow_add (rate s t : ℝ) (x : Coordinate4) :
    boostFlow rate (s+t) x = boostFlow rate s (boostFlow rate t x) := by
  unfold boostFlow
  rw [boost_matrix_add, Matrix.mulVec_mulVec]

theorem boost_flow_neg_left (rate s : ℝ) (x : Coordinate4) :
    boostFlow rate (-s) (boostFlow rate s x) = x := by
  rw [← boost_flow_add, neg_add_cancel, boost_flow_zero]

theorem boost_flow_neg_right (rate s : ℝ) (x : Coordinate4) :
    boostFlow rate s (boostFlow rate (-s) x) = x := by
  rw [← boost_flow_add, add_neg_cancel, boost_flow_zero]

theorem boost_flow_hasDerivAt (rate s : ℝ) (x : Coordinate4) :
    HasDerivAt (fun q => boostFlow rate q x)
      (boostField rate (boostFlow rate s x)) s := by
  simp only [boost_flow_coordinates]
  apply hasDerivAt_pi.2
  intro i
  fin_cases i
  · change HasDerivAt (fun q : ℝ => boostEven rate q * x 0 + boostOdd rate q * x 3)
      (-rate * (boostOdd rate s * x 0 + boostEven rate s * x 3)) s
    convert ((boost_even_hasDerivAt rate s).mul_const (x 0)).add
      ((boost_odd_hasDerivAt rate s).mul_const (x 3)) using 1
    all_goals first | rfl | ring
  · change HasDerivAt (fun _ : ℝ => x 1) 0 s
    exact hasDerivAt_const s _
  · change HasDerivAt (fun _ : ℝ => x 2) 0 s
    exact hasDerivAt_const s _
  · change HasDerivAt (fun q : ℝ => boostOdd rate q * x 0 + boostEven rate q * x 3)
      (-rate * (boostEven rate s * x 0 + boostOdd rate s * x 3)) s
    convert ((boost_odd_hasDerivAt rate s).mul_const (x 0)).add
      ((boost_even_hasDerivAt rate s).mul_const (x 3)) using 1
    all_goals first | rfl | ring

theorem boost_flow_hasFDerivAt (rate s : ℝ) (x : Coordinate4) :
    HasFDerivAt (boostFlow rate s) (boostMatrixAction (boostMatrix rate s)) x := by
  have he : boostFlow rate s =
      (boostMatrixAction (boostMatrix rate s) : Coordinate4 → Coordinate4) := by
    funext y
    exact (boost_matrix_action_apply (boostMatrix rate s) y).symm
  rw [he]
  exact (boostMatrixAction (boostMatrix rate s)).hasFDerivAt

/-- The spatial Jacobian is certified independently of the time derivative. -/
theorem boost_flow_fderiv (rate s : ℝ) (x : Coordinate4) :
    fderiv ℝ (boostFlow rate s) x = boostMatrixAction (boostMatrix rate s) :=
  (boost_flow_hasFDerivAt rate s x).fderiv

theorem boost_flow_one (rate s : ℝ) (x : Coordinate4) :
    boostFlow rate s x 1 = x 1 := by
  rw [boost_flow_coordinates]
  rfl

theorem boost_flow_two (rate s : ℝ) (x : Coordinate4) :
    boostFlow rate s x 2 = x 2 := by
  rw [boost_flow_coordinates]
  rfl

theorem boost_phase_coordinate (rate s : ℝ) (x : Coordinate4) :
    opticalPhaseCoordinate (boostFlow rate s x) =
      Real.exp (-rate*s) * opticalPhaseCoordinate x := by
  rw [boost_flow_coordinates]
  dsimp [opticalPhaseCoordinate, boostEven, boostOdd]
  ring

theorem boost_flow_central (rate s t : ℝ) :
    boostFlow rate s (centralNullCurve t) =
      centralNullCurve (Real.exp (-rate*s)*t) := by
  rw [boost_flow_coordinates]
  ext i
  fin_cases i <;>
    simp [centralNullCurve, centralNullDirection, boostEven, boostOdd] <;> ring

theorem boost_matrix_covector (rate s : ℝ) :
    (boostMatrix rate s)ᵀ.mulVec waveCovector =
      Real.exp (-rate*s) • waveCovector := by
  ext i
  fin_cases i <;>
    simp [boostMatrix, boostEven, boostOdd, waveCovector, Matrix.transpose_apply,
      Matrix.mulVec, dotProduct, Fin.sum_univ_four] <;> ring

/-- Exact preservation of the flat metric; no claim of exact plane-wave symmetry. -/
theorem boost_matrix_flat_preserving (rate s : ℝ) :
    (boostMatrix rate s)ᵀ * eta4 * boostMatrix rate s = eta4 := by
  have h := boost_coeff_hyperbolic rate s
  ext i j
  simp only [Matrix.mul_apply, Matrix.transpose_apply, Fin.sum_univ_four]
  fin_cases i <;> fin_cases j <;>
    norm_num [boostMatrix, eta4, Matrix.diagonal_apply, Matrix.cons_val_two,
      Matrix.cons_val_three, Fin.ext_iff] <;> nlinarith [h]

theorem boost_field_rate_zero (x : Coordinate4) : boostField 0 x = 0 := by
  ext i
  fin_cases i <;> simp [boostField]

theorem boost_matrix_rate_zero (s : ℝ) : boostMatrix 0 s = 1 := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    norm_num [boostMatrix, boostEven, boostOdd, Matrix.one_apply]

theorem boost_flow_rate_zero (s : ℝ) (x : Coordinate4) : boostFlow 0 s x = x := by
  simp [boostFlow, boost_matrix_rate_zero]

#print axioms boostField
#print axioms boostGenerator
#print axioms boostEven
#print axioms boostOdd
#print axioms boostMatrix
#print axioms boostFlow
#print axioms boostMatrixAction
#print axioms boost_matrix_action_apply
#print axioms boost_even_add_odd
#print axioms boost_even_sub_odd
#print axioms boost_exponential_product
#print axioms boost_coeff_hyperbolic
#print axioms boost_even_add
#print axioms boost_odd_add
#print axioms boost_even_hasDerivAt
#print axioms boost_odd_hasDerivAt
#print axioms boost_field_smooth
#print axioms boost_field_origin
#print axioms boost_field_central
#print axioms boost_field_future_central
#print axioms boost_field_frequency
#print axioms boost_field_as_linear
#print axioms boost_field_hasFDerivAt
#print axioms boost_field_partial
#print axioms boost_matrix_zero
#print axioms boost_matrix_add
#print axioms boost_matrix_mul_neg
#print axioms boost_matrix_neg_mul
#print axioms boost_matrix_hasDerivAt
#print axioms boost_matrix_hasDerivAt_zero
#print axioms boost_flow_coordinates
#print axioms boost_flow_zero
#print axioms boost_flow_add
#print axioms boost_flow_neg_left
#print axioms boost_flow_neg_right
#print axioms boost_flow_hasDerivAt
#print axioms boost_flow_hasFDerivAt
#print axioms boost_flow_fderiv
#print axioms boost_flow_one
#print axioms boost_flow_two
#print axioms boost_phase_coordinate
#print axioms boost_flow_central
#print axioms boost_matrix_covector
#print axioms boost_matrix_flat_preserving
#print axioms boost_field_rate_zero
#print axioms boost_matrix_rate_zero
#print axioms boost_flow_rate_zero

end
end ChatgptAudit.Boost044
