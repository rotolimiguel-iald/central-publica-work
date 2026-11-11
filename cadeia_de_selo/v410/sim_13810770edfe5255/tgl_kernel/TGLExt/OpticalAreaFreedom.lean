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
import TGLExt.OpticalTidalScreen
import TGLExt.OpticalJacobiArea
import Mathlib.Analysis.Calculus.IteratedDeriv.Lemmas

set_option autoImplicit false
set_option maxHeartbeats 8000000
set_option maxRecDepth 4096

namespace ChatgptAudit.Optical036
open Matrix Filter TGLExt ChatgptAudit ChatgptAudit.Wave029
open scoped Topology
noncomputable section

/-- Transverse Jacobi fields along the existing central null geodesic. -/
def geometricJacobiField (a c : ℝ) (i : Fin 2) (t : ℝ) : Coordinate4 :=
  jacobiOscillator (if i=0 then a else c) t • transverseScreenVector i

def geometricJacobiVelocity (a c : ℝ) (i : Fin 2) (t : ℝ) : Coordinate4 :=
  jacobiOscillatorVelocity (if i=0 then a else c) t • transverseScreenVector i

def geometricJacobiColumns (a c t : ℝ) : ScreenVectors :=
  fun r i => geometricJacobiField a c i t r

/-- The positive metric of the spacelike Jacobi screen; the ambient signature is +---. -/
def geometricJacobiPositiveGram (a c t : ℝ) : ScreenMatrix :=
  -screenGram (frameMetricField (waveSolder a c) (centralNullCurve t))
    (geometricJacobiColumns a c t)

/-- This is the existing geometric area functional, evaluated on Jacobi screen fields. -/
def geometricJacobiArea (a c t : ℝ) : ℝ :=
  inducedArea (frameMetricField (waveSolder a c)) centralNullCurve
    (geometricJacobiColumns a c) t

theorem curvature_action_smul_first (Gamma : ConnectionField4)
    (x u v w : Coordinate4) (q : ℝ) :
    curvatureAction Gamma x (q • u) v w = q • curvatureAction Gamma x u v w := by
  simp only [curvatureAction,Pi.smul_apply,Finset.smul_sum,smul_smul,
    smul_eq_mul,mul_assoc]

/-- The constant screen basis is parallel along the central curve. -/
theorem transverse_basis_parallel (a c t : ℝ) (i : Fin 2) :
    HasDerivAt (fun _ : ℝ => transverseScreenVector i)
      (-((connectionAlong
        (frameLeviCivita (waveSolder a c) (waveInverseSolder a c))
        (centralNullCurve t) centralNullDirection).mulVec (transverseScreenVector i))) t := by
  simpa [connectionAlong,central_curve_connection_zero] using
    hasDerivAt_const t (transverseScreenVector i)

theorem geometric_jacobi_field_derivative (a c : ℝ) (i : Fin 2) (t : ℝ) :
    HasDerivAt (geometricJacobiField a c i) (geometricJacobiVelocity a c i t) t := by
  exact (jacobi_oscillator_hasDerivAt (if i=0 then a else c) t).smul_const
    (transverseScreenVector i)

/-- Since the connection vanishes along the central curve, these are the covariant
Jacobi equations in a parallel screen, with R(W,d)d on the right. -/
theorem geometric_jacobi_velocity_derivative (a c : ℝ) (ha : 0≤a) (hc : 0≤c)
    (i : Fin 2) (t : ℝ) :
    HasDerivAt (geometricJacobiVelocity a c i)
      (-curvatureAction (frameLeviCivita (waveSolder a c) (waveInverseSolder a c))
        (centralNullCurve t) (geometricJacobiField a c i t)
        centralNullDirection centralNullDirection) t := by
  have hcoef : 0 ≤ (if i=0 then a else c) := by
    split_ifs <;> assumption
  have h := (jacobi_oscillator_velocity_hasDerivAt
    (if i=0 then a else c) hcoef t).smul_const (transverseScreenVector i)
  apply h.congr_deriv
  rw [geometricJacobiField,curvature_action_smul_first,optical_tidal_action]
  simp only [smul_smul,← neg_smul]
  congr 1
  ring

theorem geometric_jacobi_field_zero (a c : ℝ) (i : Fin 2) :
    geometricJacobiField a c i 0 = transverseScreenVector i := by
  simp [geometricJacobiField,jacobiOscillator]

theorem geometric_jacobi_velocity_zero (a c : ℝ) (i : Fin 2) :
    geometricJacobiVelocity a c i 0 = 0 := by
  simp [geometricJacobiVelocity,jacobiOscillatorVelocity]

theorem geometric_jacobi_field_null_orthogonal (a c t : ℝ) (i : Fin 2) :
    tensorPair (frameMetricField (waveSolder a c) (centralNullCurve t))
      centralNullDirection (geometricJacobiField a c i t) = 0 := by
  rw [central_curve_metric]
  fin_cases i <;>
    norm_num [geometricJacobiField,tensorPair,centralNullDirection,
      transverseScreenVector,eta4,Matrix.mulVec,dotProduct,Fin.sum_univ_four,
      Matrix.cons_val_two,Matrix.cons_val_three,Matrix.diagonal_apply,Fin.isValue]

theorem geometric_jacobi_gram (a c t : ℝ) :
    screenGram (frameMetricField (waveSolder a c) (centralNullCurve t))
      (geometricJacobiColumns a c t) =
        !![-(jacobiOscillator a t)^2,0;0,-(jacobiOscillator c t)^2] := by
  rw [central_curve_metric]
  ext i j
  fin_cases i <;> fin_cases j <;>
    norm_num [screenGram,geometricJacobiColumns,geometricJacobiField,
      transverseScreenVector,eta4,Matrix.mul_apply,Fin.sum_univ_four,
      Matrix.cons_val_two,Matrix.cons_val_three,Matrix.diagonal_apply,Fin.isValue] <;> ring

theorem geometric_jacobi_positive_gram (a c t : ℝ) :
    geometricJacobiPositiveGram a c t =
      !![(jacobiOscillator a t)^2,0;0,(jacobiOscillator c t)^2] := by
  unfold geometricJacobiPositiveGram
  rw [geometric_jacobi_gram]
  ext i j
  fin_cases i <;> fin_cases j <;> simp

theorem geometric_jacobi_gram_det (a c t : ℝ) :
    (screenGram (frameMetricField (waveSolder a c) (centralNullCurve t))
      (geometricJacobiColumns a c t)).det = (opticalJacobiArea a c t)^2 := by
  rw [geometric_jacobi_gram,Matrix.det_fin_two]
  norm_num [opticalJacobiArea]
  ring

theorem geometric_jacobi_area_abs (a c t : ℝ) :
    geometricJacobiArea a c t = |opticalJacobiArea a c t| := by
  unfold geometricJacobiArea inducedArea screenArea
  rw [geometric_jacobi_gram_det,Real.sqrt_sq_eq_abs]

theorem geometric_jacobi_area_zero (a c : ℝ) :
    geometricJacobiArea a c 0 = 1 := by
  rw [geometric_jacobi_area_abs,optical_jacobi_area_zero,abs_one]

/-- Equality is local, before the initial Jacobi screen degenerates. -/
theorem geometric_jacobi_area_agrees_near_zero (a c : ℝ) (ha : 0≤a) (hc : 0≤c) :
    geometricJacobiArea a c =ᶠ[𝓝 0] opticalJacobiArea a c := by
  filter_upwards [optical_jacobi_area_abs_agrees_near_zero a c ha hc] with t ht
  rw [geometric_jacobi_area_abs]
  exact ht

theorem geometric_jacobi_screen_nondegenerate_near_zero (a c : ℝ)
    (ha : 0≤a) (hc : 0≤c) :
    ∀ᶠ t in 𝓝 0,
      0 < (screenGram (frameMetricField (waveSolder a c) (centralNullCurve t))
        (geometricJacobiColumns a c t)).det ∧ 0 < geometricJacobiArea a c t := by
  filter_upwards [optical_jacobi_area_positive_near_zero a c ha hc] with t ht
  rw [geometric_jacobi_gram_det,geometric_jacobi_area_abs,abs_of_pos ht]
  exact ⟨sq_pos_of_ne_zero (ne_of_gt ht),ht⟩

theorem geometric_jacobi_area_iterated_eq (a c : ℝ) (ha : 0≤a) (hc : 0≤c)
    (n : ℕ) :
    iteratedDeriv n (geometricJacobiArea a c) 0 =
      iteratedDeriv n (opticalJacobiArea a c) 0 :=
  Filter.EventuallyEq.iteratedDeriv_eq n
    (geometric_jacobi_area_agrees_near_zero a c ha hc)

theorem geometric_jacobi_area_initial_first (a c : ℝ) (ha : 0≤a) (hc : 0≤c) :
    iteratedDeriv 1 (geometricJacobiArea a c) 0 = 0 := by
  rw [geometric_jacobi_area_iterated_eq a c ha hc 1,
    optical_jacobi_area_iterated_one_zero a c ha hc]

theorem geometric_jacobi_area_initial_second (a c : ℝ) (ha : 0≤a) (hc : 0≤c) :
    iteratedDeriv 2 (geometricJacobiArea a c) 0 = -(a+c) := by
  rw [geometric_jacobi_area_iterated_eq a c ha hc 2,
    optical_jacobi_area_iterated_two_zero a c ha hc]

theorem geometric_jacobi_area_initial_third (a c : ℝ) (ha : 0≤a) (hc : 0≤c) :
    iteratedDeriv 3 (geometricJacobiArea a c) 0 = 0 := by
  rw [geometric_jacobi_area_iterated_eq a c ha hc 3,
    optical_jacobi_area_iterated_three_zero a c ha hc]

theorem geometric_jacobi_area_initial_fourth (a c : ℝ) (ha : 0≤a) (hc : 0≤c) :
    iteratedDeriv 4 (geometricJacobiArea a c) 0 = a^2+6*a*c+c^2 := by
  rw [geometric_jacobi_area_iterated_eq a c ha hc 4,
    optical_jacobi_area_iterated_four_zero a c ha hc]

theorem geometric_jacobi_area_second_eq_ricci (a c : ℝ) (ha : 0≤a) (hc : 0≤c) :
    iteratedDeriv 2 (geometricJacobiArea a c) 0 =
      -tensorQuad (coordinateRicci
        (frameLeviCivita (waveSolder a c) (waveInverseSolder a c)) 0)
        centralNullDirection := by
  rw [geometric_jacobi_area_initial_second a c ha hc,
    ← optical_tidal_trace_eq_ricci,optical_tidal_trace]

/-- The fourth area jet includes the trace-free tidal response, beyond Ricci focusing. -/
theorem geometric_jacobi_area_fourth_from_tidal (a c : ℝ) (ha : 0≤a) (hc : 0≤c) :
    iteratedDeriv 4 (geometricJacobiArea a c) 0 =
      2*(Matrix.trace (opticalTidalMatrix a c 0))^2 -
        2*opticalTidalTraceFreeNormSq a c 0 := by
  rw [geometric_jacobi_area_initial_fourth a c ha hc,
    optical_tidal_trace,optical_tidal_tracefree_norm_sq]
  ring

theorem geometric_jacobi_area_rs_second (r s : ℝ) (hs : |s|<r/2) :
    iteratedDeriv 2 (geometricJacobiArea (r/2+s) (r/2-s)) 0 = -r := by
  obtain ⟨ha,hc⟩ := optical_rs_positive_coefficients r s hs
  rw [geometric_jacobi_area_iterated_eq _ _ ha.le hc.le 2]
  exact optical_jacobi_area_rs_second r s hs

theorem geometric_jacobi_area_rs_fourth (r s : ℝ) (hs : |s|<r/2) :
    iteratedDeriv 4 (geometricJacobiArea (r/2+s) (r/2-s)) 0 = 2*r^2-4*s^2 := by
  obtain ⟨ha,hc⟩ := optical_rs_positive_coefficients r s hs
  rw [geometric_jacobi_area_iterated_eq _ _ ha.le hc.le 4]
  exact optical_jacobi_area_rs_fourth r s hs

theorem geometric_jacobi_area_rs_quartic_coefficient (r s : ℝ) (hs : |s|<r/2) :
    iteratedDeriv 4 (geometricJacobiArea (r/2+s) (r/2-s)) 0 / 24 =
      r^2/12-s^2/6 := by
  rw [geometric_jacobi_area_rs_fourth r s hs]
  ring

theorem geometric_jacobi_area_same_second_distinct_fourth (r s u : ℝ)
    (hs : |s|<r/2) (hu : |u|<r/2) (hne : s^2≠u^2) :
    iteratedDeriv 2 (geometricJacobiArea (r/2+s) (r/2-s)) 0 =
      iteratedDeriv 2 (geometricJacobiArea (r/2+u) (r/2-u)) 0 ∧
    iteratedDeriv 4 (geometricJacobiArea (r/2+s) (r/2-s)) 0 ≠
      iteratedDeriv 4 (geometricJacobiArea (r/2+u) (r/2-u)) 0 := by
  constructor
  · rw [geometric_jacobi_area_rs_second r s hs,geometric_jacobi_area_rs_second r u hu]
  · rw [geometric_jacobi_area_rs_fourth r s hs,geometric_jacobi_area_rs_fourth r u hu]
    intro he
    exact hne (by linarith)

/-- The actual geometric area germs differ, even when their quadratic coefficients agree. -/
theorem geometric_jacobi_area_not_eventually_eq (r s u : ℝ)
    (hs : |s|<r/2) (hu : |u|<r/2) (hne : s^2≠u^2) :
    ¬geometricJacobiArea (r/2+s) (r/2-s) =ᶠ[𝓝 0]
      geometricJacobiArea (r/2+u) (r/2-u) := by
  intro he
  exact (geometric_jacobi_area_same_second_distinct_fourth r s u hs hu hne).2
    (Filter.EventuallyEq.iteratedDeriv_eq 4 he)

theorem geometric_jacobi_area_nonunique (r s u : ℝ)
    (hs : |s|<r/2) (hu : |u|<r/2) (hne : s^2≠u^2) :
    geometricJacobiArea (r/2+s) (r/2-s) ≠
      geometricJacobiArea (r/2+u) (r/2-u) := by
  intro he
  exact (geometric_jacobi_area_same_second_distinct_fourth r s u hs hu hne).2
    (congrArg (fun f : ℝ → ℝ => iteratedDeriv 4 f 0) he)

#print axioms geometricJacobiField
#print axioms geometricJacobiVelocity
#print axioms geometricJacobiColumns
#print axioms geometricJacobiPositiveGram
#print axioms geometricJacobiArea
#print axioms curvature_action_smul_first
#print axioms transverse_basis_parallel
#print axioms geometric_jacobi_field_derivative
#print axioms geometric_jacobi_velocity_derivative
#print axioms geometric_jacobi_field_zero
#print axioms geometric_jacobi_velocity_zero
#print axioms geometric_jacobi_field_null_orthogonal
#print axioms geometric_jacobi_gram
#print axioms geometric_jacobi_positive_gram
#print axioms geometric_jacobi_gram_det
#print axioms geometric_jacobi_area_abs
#print axioms geometric_jacobi_area_zero
#print axioms geometric_jacobi_area_agrees_near_zero
#print axioms geometric_jacobi_screen_nondegenerate_near_zero
#print axioms geometric_jacobi_area_iterated_eq
#print axioms geometric_jacobi_area_initial_first
#print axioms geometric_jacobi_area_initial_second
#print axioms geometric_jacobi_area_initial_third
#print axioms geometric_jacobi_area_initial_fourth
#print axioms geometric_jacobi_area_second_eq_ricci
#print axioms geometric_jacobi_area_fourth_from_tidal
#print axioms geometric_jacobi_area_rs_second
#print axioms geometric_jacobi_area_rs_fourth
#print axioms geometric_jacobi_area_rs_quartic_coefficient
#print axioms geometric_jacobi_area_same_second_distinct_fourth
#print axioms geometric_jacobi_area_not_eventually_eq
#print axioms geometric_jacobi_area_nonunique

end
end ChatgptAudit.Optical036
