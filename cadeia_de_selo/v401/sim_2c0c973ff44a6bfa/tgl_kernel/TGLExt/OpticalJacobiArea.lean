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
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Deriv
import Mathlib.Analysis.Calculus.IteratedDeriv.Defs
import Mathlib.Tactic

set_option autoImplicit false

namespace ChatgptAudit.Optical036

open Filter
open scoped Topology ContDiff

noncomputable section

/- The ODE below is an actual differential equation, not a prescribed finite jet.
The product is the oriented transverse determinant. Its absolute value agrees
with it near the initial screen, as proved below. No spacetime identification
or Taylor remainder is assumed by this module. -/

structure ConstantJacobiField (a : ℝ) where
  displacement : ℝ → ℝ
  velocity : ℝ → ℝ
  displacement_derivative : ∀ t, HasDerivAt displacement (velocity t) t
  velocity_derivative : ∀ t, HasDerivAt velocity (-a * displacement t) t
  displacement_zero : displacement 0 = 1
  velocity_zero : velocity 0 = 0

def jacobiFieldOfContDiff (a : ℝ) (f : ℝ → ℝ) (hf : ContDiff ℝ 4 f)
    (hode : ∀ t, deriv (deriv f) t = -a * f t)
    (hzero : f 0 = 1) (hvelocity : deriv f 0 = 0) : ConstantJacobiField a where
  displacement := f
  velocity := deriv f
  displacement_derivative t := (hf.differentiable (by norm_num) t).hasDerivAt
  velocity_derivative t := by
    have hd : Differentiable ℝ (deriv f) := by
      simpa only [iteratedDeriv_one] using
        hf.differentiable_iteratedDeriv 1 (by norm_num)
    exact (hd t).hasDerivAt.congr_deriv (hode t)
  displacement_zero := hzero
  velocity_zero := hvelocity

def jacobiArea {a c : ℝ} (F : ConstantJacobiField a) (G : ConstantJacobiField c)
    (t : ℝ) : ℝ := F.displacement t * G.displacement t

def jacobiAreaFirst {a c : ℝ} (F : ConstantJacobiField a) (G : ConstantJacobiField c)
    (t : ℝ) : ℝ :=
  F.velocity t * G.displacement t + F.displacement t * G.velocity t

def jacobiAreaSecond {a c : ℝ} (F : ConstantJacobiField a) (G : ConstantJacobiField c)
    (t : ℝ) : ℝ :=
  -(a + c) * (F.displacement t * G.displacement t) +
    2 * (F.velocity t * G.velocity t)

def jacobiAreaThird {a c : ℝ} (F : ConstantJacobiField a) (G : ConstantJacobiField c)
    (t : ℝ) : ℝ :=
  -(a + 3 * c) * (F.velocity t * G.displacement t) -
    (3 * a + c) * (F.displacement t * G.velocity t)

def jacobiAreaFourth {a c : ℝ} (F : ConstantJacobiField a) (G : ConstantJacobiField c)
    (t : ℝ) : ℝ :=
  (a ^ 2 + 6 * a * c + c ^ 2) * (F.displacement t * G.displacement t) -
    4 * (a + c) * (F.velocity t * G.velocity t)

theorem jacobi_area_hasDerivAt {a c : ℝ}
    (F : ConstantJacobiField a) (G : ConstantJacobiField c) (t : ℝ) :
    HasDerivAt (jacobiArea F G) (jacobiAreaFirst F G t) t := by
  exact (F.displacement_derivative t).mul (G.displacement_derivative t)

theorem jacobi_area_first_hasDerivAt {a c : ℝ}
    (F : ConstantJacobiField a) (G : ConstantJacobiField c) (t : ℝ) :
    HasDerivAt (jacobiAreaFirst F G) (jacobiAreaSecond F G t) t := by
  have h := ((F.velocity_derivative t).mul (G.displacement_derivative t)).add
    ((F.displacement_derivative t).mul (G.velocity_derivative t))
  exact h.congr_deriv (by dsimp [jacobiAreaSecond]; ring)

theorem jacobi_area_second_hasDerivAt {a c : ℝ}
    (F : ConstantJacobiField a) (G : ConstantJacobiField c) (t : ℝ) :
    HasDerivAt (jacobiAreaSecond F G) (jacobiAreaThird F G t) t := by
  have h := (((F.displacement_derivative t).mul
    (G.displacement_derivative t)).const_mul (-(a + c))).add
      (((F.velocity_derivative t).mul (G.velocity_derivative t)).const_mul 2)
  exact h.congr_deriv (by dsimp [jacobiAreaThird]; ring)

theorem jacobi_area_third_hasDerivAt {a c : ℝ}
    (F : ConstantJacobiField a) (G : ConstantJacobiField c) (t : ℝ) :
    HasDerivAt (jacobiAreaThird F G) (jacobiAreaFourth F G t) t := by
  have h := (((F.velocity_derivative t).mul
    (G.displacement_derivative t)).const_mul (-(a + 3 * c))).sub
      (((F.displacement_derivative t).mul
        (G.velocity_derivative t)).const_mul (3 * a + c))
  exact h.congr_deriv (by dsimp [jacobiAreaFourth]; ring)

theorem jacobi_area_deriv {a c : ℝ}
    (F : ConstantJacobiField a) (G : ConstantJacobiField c) :
    deriv (jacobiArea F G) = jacobiAreaFirst F G := by
  funext t
  exact (jacobi_area_hasDerivAt F G t).deriv

theorem jacobi_area_iterated_two {a c : ℝ}
    (F : ConstantJacobiField a) (G : ConstantJacobiField c) :
    iteratedDeriv 2 (jacobiArea F G) = jacobiAreaSecond F G := by
  rw [show 2 = 1 + 1 from rfl, iteratedDeriv_succ, iteratedDeriv_one,
    jacobi_area_deriv]
  funext t
  exact (jacobi_area_first_hasDerivAt F G t).deriv

theorem jacobi_area_iterated_three {a c : ℝ}
    (F : ConstantJacobiField a) (G : ConstantJacobiField c) :
    iteratedDeriv 3 (jacobiArea F G) = jacobiAreaThird F G := by
  rw [show 3 = 2 + 1 from rfl, iteratedDeriv_succ, jacobi_area_iterated_two]
  funext t
  exact (jacobi_area_second_hasDerivAt F G t).deriv

theorem jacobi_area_iterated_four {a c : ℝ}
    (F : ConstantJacobiField a) (G : ConstantJacobiField c) :
    iteratedDeriv 4 (jacobiArea F G) = jacobiAreaFourth F G := by
  rw [show 4 = 3 + 1 from rfl, iteratedDeriv_succ, jacobi_area_iterated_three]
  funext t
  exact (jacobi_area_third_hasDerivAt F G t).deriv

theorem jacobi_area_zero {a c : ℝ}
    (F : ConstantJacobiField a) (G : ConstantJacobiField c) :
    jacobiArea F G 0 = 1 := by
  simp only [jacobiArea, F.displacement_zero, G.displacement_zero, one_mul]

theorem jacobi_area_iterated_one_zero {a c : ℝ}
    (F : ConstantJacobiField a) (G : ConstantJacobiField c) :
    iteratedDeriv 1 (jacobiArea F G) 0 = 0 := by
  rw [iteratedDeriv_one, jacobi_area_deriv]
  simp only [jacobiAreaFirst, F.velocity_zero, G.velocity_zero, zero_mul, mul_zero,
    add_zero]

theorem jacobi_area_iterated_two_zero {a c : ℝ}
    (F : ConstantJacobiField a) (G : ConstantJacobiField c) :
    iteratedDeriv 2 (jacobiArea F G) 0 = -(a + c) := by
  rw [jacobi_area_iterated_two]
  simp only [jacobiAreaSecond, F.displacement_zero, G.displacement_zero,
    F.velocity_zero, G.velocity_zero, mul_one, mul_zero, add_zero]

theorem jacobi_area_iterated_three_zero {a c : ℝ}
    (F : ConstantJacobiField a) (G : ConstantJacobiField c) :
    iteratedDeriv 3 (jacobiArea F G) 0 = 0 := by
  rw [jacobi_area_iterated_three]
  simp only [jacobiAreaThird, F.velocity_zero, G.velocity_zero, zero_mul, mul_zero,
    sub_zero]

theorem jacobi_area_iterated_four_zero {a c : ℝ}
    (F : ConstantJacobiField a) (G : ConstantJacobiField c) :
    iteratedDeriv 4 (jacobiArea F G) 0 = a ^ 2 + 6 * a * c + c ^ 2 := by
  rw [jacobi_area_iterated_four]
  simp only [jacobiAreaFourth, F.displacement_zero, G.displacement_zero,
    F.velocity_zero, G.velocity_zero, mul_one, mul_zero, sub_zero]

theorem jacobi_area_quartic_coefficient {a c : ℝ}
    (F : ConstantJacobiField a) (G : ConstantJacobiField c) :
    iteratedDeriv 4 (jacobiArea F G) 0 / 24 =
      (a ^ 2 + c ^ 2) / 24 + a * c / 4 := by
  rw [jacobi_area_iterated_four_zero]
  ring

theorem jacobi_area_positive_near_zero {a c : ℝ}
    (F : ConstantJacobiField a) (G : ConstantJacobiField c) :
    ∀ᶠ t in 𝓝 0, 0 < jacobiArea F G t := by
  have hzero : 0 < jacobiArea F G 0 := by rw [jacobi_area_zero]; norm_num
  exact (jacobi_area_hasDerivAt F G 0).continuousAt.eventually (lt_mem_nhds hzero)

theorem jacobi_area_abs_agrees_near_zero {a c : ℝ}
    (F : ConstantJacobiField a) (G : ConstantJacobiField c) :
    (fun t => |jacobiArea F G t|) =ᶠ[𝓝 0] jacobiArea F G := by
  filter_upwards [jacobi_area_positive_near_zero F G] with t ht
  exact abs_of_pos ht

theorem jacobi_area_contDiff_four {a c : ℝ}
    (F : ConstantJacobiField a) (G : ConstantJacobiField c) :
    ContDiff ℝ 4 (jacobiArea F G) := by
  apply contDiff_of_differentiable_iteratedDeriv
  intro m hm
  have hm4 : m ≤ 4 := by exact_mod_cast hm
  interval_cases m
  · rw [iteratedDeriv_zero]
    intro t
    exact (jacobi_area_hasDerivAt F G t).differentiableAt
  · rw [iteratedDeriv_one, jacobi_area_deriv]
    intro t
    exact (jacobi_area_first_hasDerivAt F G t).differentiableAt
  · rw [jacobi_area_iterated_two]
    intro t
    exact (jacobi_area_second_hasDerivAt F G t).differentiableAt
  · rw [jacobi_area_iterated_three]
    intro t
    exact (jacobi_area_third_hasDerivAt F G t).differentiableAt
  · rw [jacobi_area_iterated_four]
    intro t
    exact (((F.displacement_derivative t).differentiableAt.mul
      (G.displacement_derivative t).differentiableAt).const_mul
        (a ^ 2 + 6 * a * c + c ^ 2)).sub
      (((F.velocity_derivative t).differentiableAt.mul
        (G.velocity_derivative t).differentiableAt).const_mul (4 * (a + c)))

def jacobiOscillator (a t : ℝ) : ℝ := Real.cos (Real.sqrt a * t)

def jacobiOscillatorVelocity (a t : ℝ) : ℝ :=
  -Real.sqrt a * Real.sin (Real.sqrt a * t)

theorem jacobi_oscillator_hasDerivAt (a t : ℝ) :
    HasDerivAt (jacobiOscillator a) (jacobiOscillatorVelocity a t) t := by
  have h := ((hasDerivAt_id t).const_mul (Real.sqrt a)).cos
  exact h.congr_deriv (by dsimp [jacobiOscillatorVelocity]; ring)

theorem jacobi_oscillator_velocity_hasDerivAt (a : ℝ) (ha : 0 ≤ a) (t : ℝ) :
    HasDerivAt (jacobiOscillatorVelocity a) (-a * jacobiOscillator a t) t := by
  have h := (((hasDerivAt_id t).const_mul (Real.sqrt a)).sin).const_mul (-Real.sqrt a)
  apply h.congr_deriv
  dsimp [jacobiOscillator]
  calc
    -Real.sqrt a * (Real.cos (Real.sqrt a * t) * (Real.sqrt a * 1)) =
        -(Real.sqrt a ^ 2) * Real.cos (Real.sqrt a * t) := by ring
    _ = -a * Real.cos (Real.sqrt a * t) := by rw [Real.sq_sqrt ha]

def oscillatorJacobiField (a : ℝ) (ha : 0 ≤ a) : ConstantJacobiField a where
  displacement := jacobiOscillator a
  velocity := jacobiOscillatorVelocity a
  displacement_derivative := jacobi_oscillator_hasDerivAt a
  velocity_derivative := jacobi_oscillator_velocity_hasDerivAt a ha
  displacement_zero := by simp [jacobiOscillator]
  velocity_zero := by simp [jacobiOscillatorVelocity]

def opticalJacobiArea (a c t : ℝ) : ℝ :=
  jacobiOscillator a t * jacobiOscillator c t

theorem optical_jacobi_area_is_jacobi (a c : ℝ) (ha : 0 ≤ a) (hc : 0 ≤ c) :
    opticalJacobiArea a c = jacobiArea (oscillatorJacobiField a ha)
      (oscillatorJacobiField c hc) := rfl

theorem optical_jacobi_area_zero (a c : ℝ) : opticalJacobiArea a c 0 = 1 := by
  simp [opticalJacobiArea, jacobiOscillator]

theorem optical_jacobi_area_contDiff (a c : ℝ) : ContDiff ℝ 4 (opticalJacobiArea a c) := by
  exact ((contDiff_const.mul contDiff_id).cos).mul
    ((contDiff_const.mul contDiff_id).cos)

theorem optical_jacobi_area_iterated_one_zero (a c : ℝ) (ha : 0 ≤ a) (hc : 0 ≤ c) :
    iteratedDeriv 1 (opticalJacobiArea a c) 0 = 0 := by
  rw [optical_jacobi_area_is_jacobi a c ha hc]
  exact jacobi_area_iterated_one_zero _ _

theorem optical_jacobi_area_iterated_two_zero (a c : ℝ) (ha : 0 ≤ a) (hc : 0 ≤ c) :
    iteratedDeriv 2 (opticalJacobiArea a c) 0 = -(a + c) := by
  rw [optical_jacobi_area_is_jacobi a c ha hc]
  exact jacobi_area_iterated_two_zero _ _

theorem optical_jacobi_area_iterated_three_zero (a c : ℝ) (ha : 0 ≤ a) (hc : 0 ≤ c) :
    iteratedDeriv 3 (opticalJacobiArea a c) 0 = 0 := by
  rw [optical_jacobi_area_is_jacobi a c ha hc]
  exact jacobi_area_iterated_three_zero _ _

theorem optical_jacobi_area_iterated_four_zero (a c : ℝ) (ha : 0 ≤ a) (hc : 0 ≤ c) :
    iteratedDeriv 4 (opticalJacobiArea a c) 0 = a ^ 2 + 6 * a * c + c ^ 2 := by
  rw [optical_jacobi_area_is_jacobi a c ha hc]
  exact jacobi_area_iterated_four_zero _ _

theorem optical_jacobi_area_quartic_coefficient (a c : ℝ)
    (ha : 0 ≤ a) (hc : 0 ≤ c) :
    iteratedDeriv 4 (opticalJacobiArea a c) 0 / 24 =
      (a ^ 2 + c ^ 2) / 24 + a * c / 4 := by
  rw [optical_jacobi_area_iterated_four_zero a c ha hc]
  ring

theorem optical_jacobi_area_positive_near_zero (a c : ℝ)
    (ha : 0 ≤ a) (hc : 0 ≤ c) :
    ∀ᶠ t in 𝓝 0, 0 < opticalJacobiArea a c t := by
  rw [optical_jacobi_area_is_jacobi a c ha hc]
  exact jacobi_area_positive_near_zero _ _

theorem optical_jacobi_area_abs_agrees_near_zero (a c : ℝ)
    (ha : 0 ≤ a) (hc : 0 ≤ c) :
    (fun t => |opticalJacobiArea a c t|) =ᶠ[𝓝 0] opticalJacobiArea a c := by
  rw [optical_jacobi_area_is_jacobi a c ha hc]
  exact jacobi_area_abs_agrees_near_zero _ _

theorem optical_rs_positive_coefficients (r s : ℝ) (hs : |s| < r / 2) :
    0 < r / 2 + s ∧ 0 < r / 2 - s := by
  obtain ⟨hl, hu⟩ := abs_lt.mp hs
  constructor <;> linarith

theorem optical_jacobi_area_rs_second (r s : ℝ) (hs : |s| < r / 2) :
    iteratedDeriv 2 (opticalJacobiArea (r / 2 + s) (r / 2 - s)) 0 = -r := by
  obtain ⟨ha, hc⟩ := optical_rs_positive_coefficients r s hs
  rw [optical_jacobi_area_iterated_two_zero _ _ ha.le hc.le]
  ring

theorem optical_jacobi_area_rs_fourth (r s : ℝ) (hs : |s| < r / 2) :
    iteratedDeriv 4 (opticalJacobiArea (r / 2 + s) (r / 2 - s)) 0 =
      2 * r ^ 2 - 4 * s ^ 2 := by
  obtain ⟨ha, hc⟩ := optical_rs_positive_coefficients r s hs
  rw [optical_jacobi_area_iterated_four_zero _ _ ha.le hc.le]
  ring

theorem optical_jacobi_area_rs_quartic_coefficient (r s : ℝ) (hs : |s| < r / 2) :
    iteratedDeriv 4 (opticalJacobiArea (r / 2 + s) (r / 2 - s)) 0 / 24 =
      r ^ 2 / 12 - s ^ 2 / 6 := by
  rw [optical_jacobi_area_rs_fourth r s hs]
  ring

theorem optical_jacobi_area_same_second_distinct_fourth (r s u : ℝ)
    (hs : |s| < r / 2) (hu : |u| < r / 2) (hne : s ^ 2 ≠ u ^ 2) :
    iteratedDeriv 2 (opticalJacobiArea (r / 2 + s) (r / 2 - s)) 0 =
      iteratedDeriv 2 (opticalJacobiArea (r / 2 + u) (r / 2 - u)) 0 ∧
    iteratedDeriv 4 (opticalJacobiArea (r / 2 + s) (r / 2 - s)) 0 ≠
      iteratedDeriv 4 (opticalJacobiArea (r / 2 + u) (r / 2 - u)) 0 := by
  constructor
  · rw [optical_jacobi_area_rs_second r s hs, optical_jacobi_area_rs_second r u hu]
  · rw [optical_jacobi_area_rs_fourth r s hs, optical_jacobi_area_rs_fourth r u hu]
    intro heq
    exact hne (by linarith)

theorem optical_jacobi_area_nonunique (r s u : ℝ)
    (hs : |s| < r / 2) (hu : |u| < r / 2) (hne : s ^ 2 ≠ u ^ 2) :
    opticalJacobiArea (r / 2 + s) (r / 2 - s) ≠
      opticalJacobiArea (r / 2 + u) (r / 2 - u) := by
  intro heq
  exact (optical_jacobi_area_same_second_distinct_fourth r s u hs hu hne).2
    (congrArg (fun f : ℝ → ℝ => iteratedDeriv 4 f 0) heq)

end

#print axioms ConstantJacobiField
#print axioms jacobiFieldOfContDiff
#print axioms jacobiArea
#print axioms jacobiAreaFirst
#print axioms jacobiAreaSecond
#print axioms jacobiAreaThird
#print axioms jacobiAreaFourth
#print axioms jacobi_area_hasDerivAt
#print axioms jacobi_area_first_hasDerivAt
#print axioms jacobi_area_second_hasDerivAt
#print axioms jacobi_area_third_hasDerivAt
#print axioms jacobi_area_deriv
#print axioms jacobi_area_iterated_two
#print axioms jacobi_area_iterated_three
#print axioms jacobi_area_iterated_four
#print axioms jacobi_area_zero
#print axioms jacobi_area_iterated_one_zero
#print axioms jacobi_area_iterated_two_zero
#print axioms jacobi_area_iterated_three_zero
#print axioms jacobi_area_iterated_four_zero
#print axioms jacobi_area_quartic_coefficient
#print axioms jacobi_area_positive_near_zero
#print axioms jacobi_area_abs_agrees_near_zero
#print axioms jacobi_area_contDiff_four
#print axioms jacobiOscillator
#print axioms jacobiOscillatorVelocity
#print axioms jacobi_oscillator_hasDerivAt
#print axioms jacobi_oscillator_velocity_hasDerivAt
#print axioms oscillatorJacobiField
#print axioms opticalJacobiArea
#print axioms optical_jacobi_area_is_jacobi
#print axioms optical_jacobi_area_zero
#print axioms optical_jacobi_area_contDiff
#print axioms optical_jacobi_area_iterated_one_zero
#print axioms optical_jacobi_area_iterated_two_zero
#print axioms optical_jacobi_area_iterated_three_zero
#print axioms optical_jacobi_area_iterated_four_zero
#print axioms optical_jacobi_area_quartic_coefficient
#print axioms optical_jacobi_area_positive_near_zero
#print axioms optical_jacobi_area_abs_agrees_near_zero
#print axioms optical_rs_positive_coefficients
#print axioms optical_jacobi_area_rs_second
#print axioms optical_jacobi_area_rs_fourth
#print axioms optical_jacobi_area_rs_quartic_coefficient
#print axioms optical_jacobi_area_same_second_distinct_fourth
#print axioms optical_jacobi_area_nonunique

end ChatgptAudit.Optical036
