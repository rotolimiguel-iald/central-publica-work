import HermitianLocalCoordinates
import GeneralNullCone

set_option autoImplicit false
set_option maxHeartbeats 1800000

namespace ChatgptAudit.Cone039

open Matrix
open scoped ComplexOrder

noncomputable section

/-- A real quadratic reading of the four coordinates of a local matrix.
    The ten coefficients are unrestricted until the cone condition is imposed. -/
def hermitianQuadratic (a b c d e f g h i j : ℝ)
    (A : Matrix (Fin 2) (Fin 2) ℂ) : ℝ :=
  ChatgptAudit.symmetricForm4 a b c d e f g h i j
    (matrixCoordinates A 0) (matrixCoordinates A 1)
    (matrixCoordinates A 2) (matrixCoordinates A 3)

theorem hermitian_quadratic_coordinates (a b c d e f g h i j t x y z : ℝ) :
    hermitianQuadratic a b c d e f g h i j (hermitianMatrix t x y z) =
      ChatgptAudit.symmetricForm4 a b c d e f g h i j t x y z := by
  simp [hermitianQuadratic, coords_of_hermitian]

theorem hermitian_quadratic_identity (a b c d e f g h i j : ℝ) :
    hermitianQuadratic a b c d e f g h i j 1 = a := by
  norm_num [hermitianQuadratic, matrixCoordinates,
    ChatgptAudit.symmetricForm4, Matrix.one_apply]

/-- Nine evaluations on positive outer products fix the nine coefficient ratios.
    This uses only the local matrix cone, without a spacetime metric hypothesis. -/
theorem rank_one_vanishing_coefficients (a b c d e f g h i j : ℝ)
    (hq : ∀ v : Fin 2 → ℂ,
      hermitianQuadratic a b c d e f g h i j (rankOneMatrix v) = 0) :
    b = -a ∧ c = -a ∧ d = -a ∧
      e = 0 ∧ f = 0 ∧ g = 0 ∧ h = 0 ∧ i = 0 ∧ j = 0 := by
  have h1 := hq ![1, 1]
  have h2 := hq ![1, -1]
  have h3 := hq ![1, Complex.I]
  have h4 := hq ![1, -Complex.I]
  have h5 := hq ![1, 0]
  have h6 := hq ![0, 1]
  have h7 := hq ![1 + 2 * Complex.I, 1 - 2 * Complex.I]
  have h8 := hq ![2, 1]
  have h9 := hq ![2, Complex.I]
  norm_num [hermitianQuadratic, matrixCoordinates, rankOneMatrix,
    Matrix.vecMulVec, Complex.star_def, Complex.mul_re, Complex.mul_im,
    ChatgptAudit.symmetricForm4] at h1 h2 h3 h4 h5 h6 h7 h8 h9
  have he : e = 0 := by linarith
  have hf : f = 0 := by linarith
  have hg : g = 0 := by linarith
  have hb : b = -a := by linarith
  have hc : c = -a := by linarith
  have hd : d = -a := by linarith
  have hh : h = 0 := by linarith
  have hi : i = 0 := by linarith
  have hj : j = 0 := by linarith
  exact ⟨hb, hc, hd, he, hf, hg, hh, hi, hj⟩

/-- Vanishing on the local positive outer-product cone selects the determinant
    quadratic form up to its coefficient at the identity. -/
theorem rank_one_quadratic_rigidity (a b c d e f g h i j : ℝ)
    (hq : ∀ v : Fin 2 → ℂ,
      hermitianQuadratic a b c d e f g h i j (rankOneMatrix v) = 0)
    (t x y z : ℝ) :
    hermitianQuadratic a b c d e f g h i j (hermitianMatrix t x y z) =
      a * (t^2 - x^2 - y^2 - z^2) := by
  obtain ⟨hb, hc, hd, he, hf, hg, hh, hi, hj⟩ :=
    rank_one_vanishing_coefficients a b c d e f g h i j hq
  rw [hermitian_quadratic_coordinates]
  simp only [ChatgptAudit.symmetricForm4, hb, hc, hd, he, hf, hg, hh, hi, hj]
  ring

/-- The same conclusion from all positive singular local matrices.
    Zero is allowed, so no separate operator-rank convention is required. -/
theorem positive_singular_quadratic_rigidity (a b c d e f g h i j : ℝ)
    (hq : ∀ A : Matrix (Fin 2) (Fin 2) ℂ,
      A.PosSemidef → Matrix.det A = 0 →
        hermitianQuadratic a b c d e f g h i j A = 0)
    (t x y z : ℝ) :
    hermitianQuadratic a b c d e f g h i j (hermitianMatrix t x y z) =
      a * (t^2 - x^2 - y^2 - z^2) :=
  rank_one_quadratic_rigidity a b c d e f g h i j
    (fun v => hq (rankOneMatrix v) (rank_one_positive v) (rank_one_det v)) t x y z

/-- Positivity at the identity selects the positive overall scale.
    It does not normalize that scale or identify a physical tangent space. -/
theorem positive_singular_rigidity_positive_scale (a b c d e f g h i j : ℝ)
    (hq : ∀ A : Matrix (Fin 2) (Fin 2) ℂ,
      A.PosSemidef → Matrix.det A = 0 →
        hermitianQuadratic a b c d e f g h i j A = 0)
    (hI : 0 < hermitianQuadratic a b c d e f g h i j 1) :
    0 < a ∧ ∀ t x y z : ℝ,
      hermitianQuadratic a b c d e f g h i j (hermitianMatrix t x y z) =
        a * (t^2 - x^2 - y^2 - z^2) := by
  refine ⟨?_, positive_singular_quadratic_rigidity a b c d e f g h i j hq⟩
  simpa only [hermitian_quadratic_identity] using hI

/-- A literal trace-square reading, used to distinguish positivity from cone nullity. -/
def traceSquareReading (A : Matrix (Fin 2) (Fin 2) ℂ) : ℝ :=
  (Matrix.trace (A * A)).re

theorem trace_square_hermitian_coordinates (t x y z : ℝ) :
    traceSquareReading (hermitianMatrix t x y z) =
      2 * (t^2 + x^2 + y^2 + z^2) := by
  norm_num [traceSquareReading, hermitianMatrix, Matrix.trace,
    Matrix.mul_apply, Fin.sum_univ_two, Complex.mul_re, Complex.mul_im]
  ring

theorem trace_square_identity_positive : 0 < traceSquareReading 1 := by
  norm_num [traceSquareReading, Matrix.trace, Fin.sum_univ_two]

theorem trace_square_rank_one_control :
    traceSquareReading (rankOneMatrix (![1, 0] : Fin 2 → ℂ)) = 1 := by
  norm_num [traceSquareReading, rankOneMatrix, Matrix.vecMulVec,
    Matrix.trace, Matrix.mul_apply, Fin.sum_univ_two, Complex.star_def]

/-- A positive quadratic reading of Hermitian coordinates need not vanish
    on positive singular matrices; the explicit projection is a counterexample. -/
theorem trace_square_not_positive_singular_vanishing :
    ¬ (∀ A : Matrix (Fin 2) (Fin 2) ℂ,
      A.PosSemidef → Matrix.det A = 0 → traceSquareReading A = 0) := by
  intro h
  have hz := h (rankOneMatrix (![1, 0] : Fin 2 → ℂ))
    (rank_one_positive _) (rank_one_det _)
  rw [trace_square_rank_one_control] at hz
  norm_num at hz

#print axioms hermitianQuadratic
#print axioms hermitian_quadratic_coordinates
#print axioms hermitian_quadratic_identity
#print axioms rank_one_vanishing_coefficients
#print axioms rank_one_quadratic_rigidity
#print axioms positive_singular_quadratic_rigidity
#print axioms positive_singular_rigidity_positive_scale
#print axioms traceSquareReading
#print axioms trace_square_hermitian_coordinates
#print axioms trace_square_identity_positive
#print axioms trace_square_rank_one_control
#print axioms trace_square_not_positive_singular_vanishing

end

end ChatgptAudit.Cone039
