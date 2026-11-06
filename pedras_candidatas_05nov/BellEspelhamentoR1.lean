import TGLExt.Par
import TGLExt.PsionCanto

set_option autoImplicit false
set_option linter.unusedVariables false
set_option maxHeartbeats 4000000

/-!
# O INPUT DE BELL E O CANAL DE ESPELHAMENTO — pedra candidata R1, 05/11/2026

Derivação nova [DECLARADO pelo Kimi], composta com o canto de Bell já existente.
`bellInputDensity_eq_corner` e `bellInput_PQ` identificam o input e sua coerência;
`bellAfter_zero` e `bellAfter_succ` provam a atenuação `(2uv)^n` por travessia;
`mirror_complete` prova a completeza das Kraus sob `u² + v² = 1`;
`mirror_branch_reconstruct` inverte o ramo seletivo; `bellInput_marginals`
calcula as marginais; `bellAfter_detectors` e `bellAfter_balanced_detectors`
calculam as intensidades nos detectores explícitos; `the_bell_mirror_visibility`
reúne a recursão e a visibilidade.

ESTATUTO: pedra CANDIDATA R1, não selada. É validade algébrica no canto finito,
não teste com a natureza, não dado novo e não movimento do gate. A identificação
`u = sqrt(1 - β)`, `v = sqrt β` fica fora deste módulo: nenhum β literal entra
na prova. A ponte física Bell–Fock/TT e a realização física do canal seguem ABERTAS.
-/

noncomputable section
namespace TGLExt.BellEspelhamento
open Matrix TGL.GravitonShadow TGLExt.PsionCanto
open scoped InnerProductSpace

abbrev BellIndex := Fin 2 × Fin 2
abbrev BellMat := Matrix BellIndex BellIndex ℂ
abbrev BellState := BellIndex → ℂ

/-- O segundo modo de Bell, `Φ⁻ = (e₀₀ − e₁₁)/√2`. -/
def phiMinusVec : BellState := fun p =>
  if p.1 = p.2 then
    (if p.1 = 0 then (((Real.sqrt 2)⁻¹ : ℝ) : ℂ)
     else -(((Real.sqrt 2)⁻¹ : ℝ) : ℂ))
  else 0

/-- `R = |Φ⁻⟩⟨Φ⁻|`. -/
def bellR : BellMat := cornerOf phiMinusVec

/-- `X = |Φ⁺⟩⟨Φ⁻|`. -/
def bellX : BellMat := vecMulVec bellVec (star phiMinusVec)

/-- O complemento do canto de Bell. -/
def bellQ : BellMat := 1 - psionCorner.p

/-- O input de fase do par: `c Φ⁺ − i s Φ⁻`, com `c,s` reais. -/
def bellInputVec (c s : ℝ) : BellState :=
  (c : ℂ) • bellVec + (-(s : ℂ) * Complex.I) • phiMinusVec

/-- A densidade expandida do input, sem exigir normalização nesta definição. -/
def bellInputDensity (c s : ℝ) : BellMat :=
  ((c ^ 2 : ℝ) : ℂ) • psionCorner.p + ((s ^ 2 : ℝ) : ℂ) • bellR
    + (((c * s : ℝ) : ℂ) * Complex.I) • bellX
    - (((c * s : ℝ) : ℂ) * Complex.I) • bellXᴴ

/-- As duas Kraus do espelho na base `P,Q`. -/
def mirror0 (u v : ℝ) : BellMat := (u : ℂ) • psionCorner.p + (v : ℂ) • bellQ
def mirror1 (u v : ℝ) : BellMat := (v : ℂ) • psionCorner.p + (u : ℂ) • bellQ

/-- O canal não-seletivo de duas Kraus. -/
def mirrorChannel (u v : ℝ) (rho : BellMat) : BellMat :=
  mirror0 u v * rho * mirror0 u v + mirror1 u v * rho * mirror1 u v

/-- O input após `n` atenuações da coerência pelo fator `eta = 2uv`. -/
def bellAfter (u v c s : ℝ) (n : ℕ) : BellMat :=
  ((c ^ 2 : ℝ) : ℂ) • psionCorner.p + ((s ^ 2 : ℝ) : ℂ) • bellR
    + ((((2 * u * v) ^ n * c * s : ℝ) : ℂ) * Complex.I) • bellX
    - ((((2 * u * v) ^ n * c * s : ℝ) : ℂ) * Complex.I) • bellXᴴ

lemma bellR_idem : bellR * bellR = bellR := by
  ext p q
  rcases p with ⟨a, b⟩
  rcases q with ⟨c, d⟩
  fin_cases a <;> fin_cases b <;> fin_cases c <;> fin_cases d <;>
    simp [bellR, cornerOf, phiMinusVec, Matrix.mul_apply, Fintype.sum_prod_type,
      Fin.sum_univ_two, vecMulVec_apply, half_of_sqrt_two] <;> norm_num

lemma bellP_bellR : psionCorner.p * bellR = 0 := by
  ext p q
  rcases p with ⟨a, b⟩
  rcases q with ⟨c, d⟩
  fin_cases a <;> fin_cases b <;> fin_cases c <;> fin_cases d <;>
    simp [psionCorner, bellProjector, bellR, cornerOf, phiMinusVec, Matrix.mul_apply,
      Fintype.sum_prod_type, Fin.sum_univ_two, vecMulVec_apply, half_of_sqrt_two] <;> norm_num

lemma bellR_bellP : bellR * psionCorner.p = 0 := by
  ext p q
  rcases p with ⟨a, b⟩
  rcases q with ⟨c, d⟩
  fin_cases a <;> fin_cases b <;> fin_cases c <;> fin_cases d <;>
    simp [psionCorner, bellProjector, bellR, cornerOf, phiMinusVec, Matrix.mul_apply,
      Fintype.sum_prod_type, Fin.sum_univ_two, vecMulVec_apply, half_of_sqrt_two] <;> norm_num

lemma bellP_bellX : psionCorner.p * bellX = bellX := by
  ext p q
  rcases p with ⟨a, b⟩
  rcases q with ⟨c, d⟩
  fin_cases a <;> fin_cases b <;> fin_cases c <;> fin_cases d <;>
    simp [psionCorner, bellProjector, bellX, bellVec, phiMinusVec, Matrix.mul_apply,
      Fintype.sum_prod_type, Fin.sum_univ_two, vecMulVec_apply, half_of_sqrt_two] <;> norm_num

lemma bellX_bellP : bellX * psionCorner.p = 0 := by
  ext p q
  rcases p with ⟨a, b⟩
  rcases q with ⟨c, d⟩
  fin_cases a <;> fin_cases b <;> fin_cases c <;> fin_cases d <;>
    simp [psionCorner, bellProjector, bellX, bellVec, phiMinusVec, Matrix.mul_apply,
      Fintype.sum_prod_type, Fin.sum_univ_two, vecMulVec_apply, half_of_sqrt_two] <;> norm_num

lemma bellX_bellR : bellX * bellR = bellX := by
  ext p q
  rcases p with ⟨a, b⟩
  rcases q with ⟨c, d⟩
  fin_cases a <;> fin_cases b <;> fin_cases c <;> fin_cases d <;>
    simp [bellR, bellX, cornerOf, bellVec, phiMinusVec, Matrix.mul_apply,
      Fintype.sum_prod_type, Fin.sum_univ_two, vecMulVec_apply, half_of_sqrt_two] <;> norm_num

lemma bellQ_idem : bellQ * bellQ = bellQ := by
  simp only [bellQ, mul_sub, sub_mul, one_mul, mul_one, psionCorner.idem]
  abel

lemma bellP_bellQ : psionCorner.p * bellQ = 0 := by
  simp [bellQ, mul_sub, psionCorner.idem]

lemma bellQ_bellP : bellQ * psionCorner.p = 0 := by
  simp [bellQ, sub_mul, psionCorner.idem]

/-- A densidade expandida é literalmente o canto do vetor de input. -/
lemma bellInputDensity_eq_corner (c s : ℝ) :
    bellInputDensity c s = cornerOf (bellInputVec c s) := by
  have h2 : (((Real.sqrt 2 : ℝ) : ℂ)⁻¹) ^ 2 = (2⁻¹ : ℂ) := by
    rw [pow_two, half_of_sqrt_two]
  have hI : Complex.I ^ 2 = -1 := by
    rw [pow_two, Complex.I_mul_I]
  ext p q
  rcases p with ⟨a, b⟩
  rcases q with ⟨c', d⟩
  fin_cases a <;> fin_cases b <;> fin_cases c' <;> fin_cases d <;>
    simp [bellInputDensity, bellInputVec, cornerOf, bellR, bellX, psionCorner,
      bellProjector, bellVec, phiMinusVec, vecMulVec_apply, Matrix.conjTranspose_apply,
      h2, hI, half_of_sqrt_two, Complex.I_mul_I] <;> ring_nf <;> simp [h2, hI] <;> ring

/-- O complemento do canto seleciona exatamente a coerência `i c s X`. -/
lemma bellInput_PQ (c s : ℝ) :
    psionCorner.p * bellInputDensity c s * bellQ
      = (((c * s : ℝ) : ℂ) * Complex.I) • bellX := by
  ext p q
  rcases p with ⟨a, b⟩
  rcases q with ⟨c', d⟩
  fin_cases a <;> fin_cases b <;> fin_cases c' <;> fin_cases d <;>
    simp [bellInputDensity, bellQ, bellR, bellX, psionCorner, bellProjector,
      cornerOf, bellVec, phiMinusVec, Matrix.mul_apply, Fintype.sum_prod_type,
      Fin.sum_univ_two, vecMulVec_apply, Matrix.conjTranspose_apply,
      half_of_sqrt_two, Complex.I_mul_I] <;> ring

lemma bellAfter_zero (u v c s : ℝ) : bellAfter u v c s 0 = bellInputDensity c s := by
  simp [bellAfter, bellInputDensity]

/-- A recursão do canal CPTP: cada travessia multiplica somente a coerência por `2uv`. -/
lemma bellAfter_succ (u v c s : ℝ) (huv : u ^ 2 + v ^ 2 = 1) (n : ℕ) :
    mirrorChannel u v (bellAfter u v c s n) = bellAfter u v c s (n + 1) := by
  have hu2 : u ^ 2 = 1 - v ^ 2 := by linarith
  have hu2C : (u : ℂ) ^ 2 = 1 - (v : ℂ) ^ 2 := by exact_mod_cast hu2
  ext p q
  rcases p with ⟨a, b⟩
  rcases q with ⟨c', d⟩
  fin_cases a <;> fin_cases b <;> fin_cases c' <;> fin_cases d <;>
    simp [mirrorChannel, mirror0, mirror1, bellAfter, bellQ, bellR, bellX,
      psionCorner, bellProjector, cornerOf, bellVec, phiMinusVec, Matrix.mul_apply,
      Fintype.sum_prod_type, Fin.sum_univ_two, vecMulVec_apply,
      Matrix.conjTranspose_apply, half_of_sqrt_two, Complex.I_mul_I, pow_succ, hu2C] <;>
    ring_nf <;> simp [hu2C] <;> ring

/-- Detector de fase `χ = π/2`: `(Φ⁺ − iΦ⁻)/√2`. -/
def detectorPlusVec : BellState := bellVec + (-Complex.I) • phiMinusVec

/-- Detector complementar: `(Φ⁺ + iΦ⁻)/√2`. -/
def detectorMinusVec : BellState := bellVec + Complex.I • phiMinusVec

/-- Os projetores de detecção normalizados. -/
def detectorPlus : BellMat := (2⁻¹ : ℂ) • cornerOf detectorPlusVec
def detectorMinus : BellMat := (2⁻¹ : ℂ) • cornerOf detectorMinusVec

/-- As duas intensidades interferométricas após `n` travessias. -/
lemma bellAfter_detectors (u v c s : ℝ) (hcs : c ^ 2 + s ^ 2 = 1) (n : ℕ) :
    (detectorPlus * bellAfter u v c s n).trace
      = (2⁻¹ : ℂ) * (1 + 2 * (((2 * u * v) ^ n * c * s : ℝ) : ℂ))
    ∧ (detectorMinus * bellAfter u v c s n).trace
      = (2⁻¹ : ℂ) * (1 - 2 * (((2 * u * v) ^ n * c * s : ℝ) : ℂ)) := by
  have hc2 : c ^ 2 = 1 - s ^ 2 := by linarith
  have hc2C : (c : ℂ) ^ 2 = 1 - (s : ℂ) ^ 2 := by exact_mod_cast hc2
  have h2 : (((Real.sqrt 2 : ℝ) : ℂ)⁻¹) ^ 2 = (2⁻¹ : ℂ) := by
    rw [pow_two, half_of_sqrt_two]
  have hI : Complex.I ^ 2 = -1 := by
    rw [pow_two, Complex.I_mul_I]
  constructor
  · simp [detectorPlus, detectorPlusVec, bellAfter, cornerOf, bellR, bellX,
      psionCorner, bellProjector, bellVec, phiMinusVec, Matrix.trace, Matrix.mul_apply,
      Fintype.sum_prod_type, Fin.sum_univ_two, vecMulVec_apply,
      Matrix.conjTranspose_apply, half_of_sqrt_two, Complex.I_mul_I] <;>
      ring_nf <;> simp [h2, hI, hc2C] <;> ring
  · simp [detectorMinus, detectorMinusVec, bellAfter, cornerOf, bellR, bellX,
      psionCorner, bellProjector, bellVec, phiMinusVec, Matrix.trace, Matrix.mul_apply,
      Fintype.sum_prod_type, Fin.sum_univ_two, vecMulVec_apply,
      Matrix.conjTranspose_apply, half_of_sqrt_two, Complex.I_mul_I] <;>
      ring_nf <;> simp [h2, hI, hc2C] <;> ring

/-- A inversa do ramo `M₀`, definida somente quando `u,v ≠ 0`. -/
def mirror0Inv (u v : ℝ) : BellMat :=
  (u : ℂ)⁻¹ • psionCorner.p + (v : ℂ)⁻¹ • bellQ

lemma mirror_complete (u v : ℝ) (huv : u ^ 2 + v ^ 2 = 1) :
    mirror0 u v * mirror0 u v + mirror1 u v * mirror1 u v = 1 := by
  have hu2 : u ^ 2 = 1 - v ^ 2 := by linarith
  have hu2C : (u : ℂ) ^ 2 = 1 - (v : ℂ) ^ 2 := by exact_mod_cast hu2
  ext p q
  rcases p with ⟨a, b⟩
  rcases q with ⟨c', d⟩
  fin_cases a <;> fin_cases b <;> fin_cases c' <;> fin_cases d <;>
    simp [mirror0, mirror1, bellQ, psionCorner, bellProjector, Matrix.mul_apply,
      Fintype.sum_prod_type, Fin.sum_univ_two] <;>
    ring_nf <;> simp [hu2C] <;> ring

lemma mirror0Inv_mul_mirror0 (u v : ℝ) (hu : u ≠ 0) (hv : v ≠ 0) :
    mirror0Inv u v * mirror0 u v = 1 := by
  have huC : (u : ℂ) ≠ 0 := by exact_mod_cast hu
  have hvC : (v : ℂ) ≠ 0 := by exact_mod_cast hv
  ext p q
  rcases p with ⟨a, b⟩
  rcases q with ⟨c', d⟩
  fin_cases a <;> fin_cases b <;> fin_cases c' <;> fin_cases d <;>
    simp [mirror0Inv, mirror0, bellQ, psionCorner, bellProjector, Matrix.mul_apply,
      Fintype.sum_prod_type, Fin.sum_univ_two] <;> field_simp [huC, hvC] <;> ring

lemma mirror0_mul_mirror0Inv (u v : ℝ) (hu : u ≠ 0) (hv : v ≠ 0) :
    mirror0 u v * mirror0Inv u v = 1 := by
  have huC : (u : ℂ) ≠ 0 := by exact_mod_cast hu
  have hvC : (v : ℂ) ≠ 0 := by exact_mod_cast hv
  ext p q
  rcases p with ⟨a, b⟩
  rcases q with ⟨c', d⟩
  fin_cases a <;> fin_cases b <;> fin_cases c' <;> fin_cases d <;>
    simp [mirror0Inv, mirror0, bellQ, psionCorner, bellProjector, Matrix.mul_apply,
      Fintype.sum_prod_type, Fin.sum_univ_two] <;> field_simp [huC, hvC] <;> ring

/-- A inversão é exata no ramo, não no canal não-seletivo inteiro. -/
lemma mirror_branch_reconstruct (u v : ℝ) (hu : u ≠ 0) (hv : v ≠ 0) (rho : BellMat) :
    mirror0Inv u v * (mirror0 u v * rho * mirror0 u v) * mirror0Inv u v = rho := by
  calc
    mirror0Inv u v * (mirror0 u v * rho * mirror0 u v) * mirror0Inv u v
        = (mirror0Inv u v * mirror0 u v) * rho * (mirror0 u v * mirror0Inv u v) := by
          noncomm_ring
    _ = rho := by
      rw [mirror0Inv_mul_mirror0 u v hu hv, mirror0_mul_mirror0Inv u v hu hv,
        one_mul, mul_one]

/-- O traço parcial sobre o primeiro sítio. -/
def ptrFirst (X : BellMat) : Matrix (Fin 2) (Fin 2) ℂ :=
  Matrix.of fun i j => ∑ k, X (k, i) (k, j)

lemma bellInput_marginals (c s : ℝ) (hcs : c ^ 2 + s ^ 2 = 1) :
    ptr (bellInputDensity c s) = (2⁻¹ : ℂ) • 1
    ∧ ptrFirst (bellInputDensity c s) = (2⁻¹ : ℂ) • 1 := by
  have hc2 : c ^ 2 = 1 - s ^ 2 := by linarith
  have hc2C : (c : ℂ) ^ 2 = 1 - (s : ℂ) ^ 2 := by exact_mod_cast hc2
  have h2 : (((Real.sqrt 2 : ℝ) : ℂ)⁻¹) ^ 2 = (2⁻¹ : ℂ) := by
    rw [pow_two, half_of_sqrt_two]
  have hI : Complex.I ^ 2 = -1 := by
    rw [pow_two, Complex.I_mul_I]
  constructor
  · ext i j
    fin_cases i <;> fin_cases j <;>
      simp [bellInputDensity, ptr, bellR, bellX, psionCorner, bellProjector,
        cornerOf, bellVec, phiMinusVec, Fin.sum_univ_two, vecMulVec_apply,
        Matrix.conjTranspose_apply, half_of_sqrt_two, Complex.I_mul_I] <;>
      ring_nf <;> simp [h2, hI, hc2C] <;> ring
  · ext i j
    fin_cases i <;> fin_cases j <;>
      simp [bellInputDensity, ptrFirst, bellR, bellX, psionCorner, bellProjector,
        cornerOf, bellVec, phiMinusVec, Fin.sum_univ_two, vecMulVec_apply,
        Matrix.conjTranspose_apply, half_of_sqrt_two, Complex.I_mul_I] <;>
      ring_nf <;> simp [h2, hI, hc2C] <;> ring

/-- O input sem preparação não tem coerência `P/Q`. -/
lemma bellInput_unprepared_PQ :
    psionCorner.p * bellInputDensity 1 0 * bellQ = 0 := by
  rw [bellInput_PQ]
  simp

/-- A transferência total para `Φ⁻` também não tem coerência `P/Q`. -/
lemma bellInput_full_transfer_PQ :
    psionCorner.p * bellInputDensity 0 1 * bellQ = 0 := by
  rw [bellInput_PQ]
  simp

/-- O preparo balanceado: `I_± = (1 ± (2uv)^n)/2`. -/
lemma bellAfter_balanced_detectors (u v : ℝ) (n : ℕ) :
    (detectorPlus * bellAfter u v (Real.sqrt 2)⁻¹ (Real.sqrt 2)⁻¹ n).trace
      = (2⁻¹ : ℂ) * (1 + (((2 * u * v) ^ n : ℝ) : ℂ))
    ∧ (detectorMinus * bellAfter u v (Real.sqrt 2)⁻¹ (Real.sqrt 2)⁻¹ n).trace
      = (2⁻¹ : ℂ) * (1 - (((2 * u * v) ^ n : ℝ) : ℂ)) := by
  have hcs : ((Real.sqrt 2)⁻¹) ^ 2 + ((Real.sqrt 2)⁻¹) ^ 2 = 1 := by
    norm_num [pow_two, ← mul_inv, Real.mul_self_sqrt (by norm_num : (0 : ℝ) ≤ 2)]
  have hdet := bellAfter_detectors u v (Real.sqrt 2)⁻¹ (Real.sqrt 2)⁻¹ hcs n
  have hprodR : (Real.sqrt 2)⁻¹ * (Real.sqrt 2)⁻¹ = (2⁻¹ : ℝ) := by
    norm_num [← mul_inv, Real.mul_self_sqrt (by norm_num : (0 : ℝ) ≤ 2)]
  simp only [mul_assoc, hprodR] at hdet
  convert hdet using 1 <;> push_cast <;> ring

/-- A síntese da pedra: recursão CPTP e visibilidade interferométrica normalizada. -/
theorem the_bell_mirror_visibility (u v c s : ℝ)
    (huv : u ^ 2 + v ^ 2 = 1) (hcs : c ^ 2 + s ^ 2 = 1) (n : ℕ) :
    mirrorChannel u v (bellAfter u v c s n) = bellAfter u v c s (n + 1)
    ∧ (detectorPlus * bellAfter u v c s n).trace
      = (2⁻¹ : ℂ) * (1 + 2 * (((2 * u * v) ^ n * c * s : ℝ) : ℂ))
    ∧ (detectorMinus * bellAfter u v c s n).trace
      = (2⁻¹ : ℂ) * (1 - 2 * (((2 * u * v) ^ n * c * s : ℝ) : ℂ)) :=
  ⟨bellAfter_succ u v c s huv n, bellAfter_detectors u v c s hcs n⟩

end TGLExt.BellEspelhamento

#print axioms TGLExt.BellEspelhamento.bellInput_unprepared_PQ
#print axioms TGLExt.BellEspelhamento.bellInput_full_transfer_PQ
#print axioms TGLExt.BellEspelhamento.bellAfter_balanced_detectors
#print axioms TGLExt.BellEspelhamento.the_bell_mirror_visibility
#print axioms TGLExt.BellEspelhamento.mirror_complete
#print axioms TGLExt.BellEspelhamento.mirror_branch_reconstruct
#print axioms TGLExt.BellEspelhamento.bellInput_marginals
#print axioms TGLExt.BellEspelhamento.bellAfter_detectors
#print axioms TGLExt.BellEspelhamento.bellInputDensity_eq_corner
#print axioms TGLExt.BellEspelhamento.bellInput_PQ
#print axioms TGLExt.BellEspelhamento.bellAfter_zero
#print axioms TGLExt.BellEspelhamento.bellAfter_succ
#print axioms TGLExt.BellEspelhamento.bellR_idem
#print axioms TGLExt.BellEspelhamento.bellP_bellR
#print axioms TGLExt.BellEspelhamento.bellR_bellP
#print axioms TGLExt.BellEspelhamento.bellP_bellX
#print axioms TGLExt.BellEspelhamento.bellX_bellP
#print axioms TGLExt.BellEspelhamento.bellX_bellR
#print axioms TGLExt.BellEspelhamento.bellQ_idem
#print axioms TGLExt.BellEspelhamento.bellP_bellQ
#print axioms TGLExt.BellEspelhamento.bellQ_bellP
#print axioms TGLExt.BellEspelhamento.mirror0Inv_mul_mirror0
#print axioms TGLExt.BellEspelhamento.mirror0_mul_mirror0Inv
