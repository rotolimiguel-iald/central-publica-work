import OpticalTidalScreen
import Mathlib.LinearAlgebra.Matrix.Trace

set_option autoImplicit false
set_option maxHeartbeats 800000
namespace ChatgptAudit.Optical036
open Matrix
noncomputable section

def screenTraceFree (K : Matrix (Fin 2) (Fin 2) ℝ) : Matrix (Fin 2) (Fin 2) ℝ :=
  K - (Matrix.trace K / 2) • 1

def screenAnisotropy (K : Matrix (Fin 2) (Fin 2) ℝ) : ℝ :=
  Matrix.trace ((screenTraceFree K).transpose * screenTraceFree K)

theorem orthogonal_trace_conjugation (K Q : Matrix (Fin 2) (Fin 2) ℝ)
    (hR : Q * Q.transpose = 1) :
    Matrix.trace (Q.transpose * K * Q) = Matrix.trace K := by
  calc
    Matrix.trace (Q.transpose * K * Q) =
        Matrix.trace (Q * (Q.transpose * K)) := Matrix.trace_mul_comm _ _
    _ = Matrix.trace ((Q * Q.transpose) * K) := by rw [Matrix.mul_assoc]
    _ = Matrix.trace K := by rw [hR, one_mul]

theorem screen_tracefree_conjugation (K Q : Matrix (Fin 2) (Fin 2) ℝ)
    (hL : Q.transpose * Q = 1) (hR : Q * Q.transpose = 1) :
    screenTraceFree (Q.transpose * K * Q) =
      Q.transpose * screenTraceFree K * Q := by
  rw [screenTraceFree, orthogonal_trace_conjugation K Q hR]
  simp [screenTraceFree, mul_sub, sub_mul, hL]

theorem screen_anisotropy_conjugation (K Q : Matrix (Fin 2) (Fin 2) ℝ)
    (hL : Q.transpose * Q = 1) (hR : Q * Q.transpose = 1) :
    screenAnisotropy (Q.transpose * K * Q) = screenAnisotropy K := by
  unfold screenAnisotropy
  rw [screen_tracefree_conjugation K Q hL hR]
  have hm :
      (Q.transpose * screenTraceFree K * Q).transpose *
          (Q.transpose * screenTraceFree K * Q) =
        Q.transpose * ((screenTraceFree K).transpose * screenTraceFree K) * Q := by
    simp only [Matrix.transpose_mul, Matrix.transpose_transpose]
    calc
      (Q.transpose * ((screenTraceFree K).transpose * Q)) *
          (Q.transpose * screenTraceFree K * Q) =
        Q.transpose * (screenTraceFree K).transpose * (Q * Q.transpose) *
          screenTraceFree K * Q := by noncomm_ring
      _ = Q.transpose * ((screenTraceFree K).transpose * screenTraceFree K) * Q := by
        rw [hR]
        simp only [mul_one, Matrix.mul_assoc]
  rw [hm, orthogonal_trace_conjugation _ Q hR]

theorem screen_anisotropy_diagonal (a c : ℝ) :
    screenAnisotropy (Matrix.diagonal ![a,c]) = (a-c)^2/2 := by
  norm_num [screenAnisotropy, screenTraceFree, Matrix.trace, Matrix.diag,
    Fin.sum_univ_two, Matrix.mul_apply, Matrix.transpose_apply, Matrix.diagonal_apply]
  ring

theorem screen_anisotropy_matched (r s : ℝ) :
    screenAnisotropy (Matrix.diagonal ![r/2+s,r/2-s]) = 2*s^2 := by
  rw [screen_anisotropy_diagonal]
  ring

theorem optical_tidal_anisotropy_basis (a c t : ℝ)
    (Q : Matrix (Fin 2) (Fin 2) ℝ)
    (hL : Q.transpose * Q = 1) (hR : Q * Q.transpose = 1) :
    screenAnisotropy (Q.transpose * opticalTidalMatrix a c (centralNullCurve t) * Q) =
      (a-c)^2/2 := by
  rw [screen_anisotropy_conjugation _ Q hL hR]
  change opticalTidalTraceFreeNormSq a c (centralNullCurve t) = _
  exact optical_tidal_tracefree_norm_sq a c (centralNullCurve t)

theorem optical_tidal_no_orthogonal_match (r s u t : ℝ) (hne : s^2 ≠ u^2)
    (Q : Matrix (Fin 2) (Fin 2) ℝ)
    (hL : Q.transpose * Q = 1) (hR : Q * Q.transpose = 1) :
    Q.transpose * opticalTidalMatrix (r/2+s) (r/2-s) (centralNullCurve t) * Q ≠
      opticalTidalMatrix (r/2+u) (r/2-u) (centralNullCurve t) := by
  intro heq
  have hh := congrArg screenAnisotropy heq
  rw [optical_tidal_anisotropy_basis _ _ t Q hL hR] at hh
  change ((r/2+s)-(r/2-s))^2/2 =
    opticalTidalTraceFreeNormSq (r/2+u) (r/2-u) (centralNullCurve t) at hh
  rw [optical_tidal_tracefree_norm_sq] at hh
  apply hne
  nlinarith

#print axioms optical_tidal_anisotropy_basis
#print axioms optical_tidal_no_orthogonal_match

#print axioms screenTraceFree
#print axioms screenAnisotropy
#print axioms orthogonal_trace_conjugation
#print axioms screen_tracefree_conjugation
#print axioms screen_anisotropy_conjugation
#print axioms screen_anisotropy_diagonal
#print axioms screen_anisotropy_matched
end
end ChatgptAudit.Optical036
