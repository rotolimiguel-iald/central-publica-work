import Mathlib.Analysis.SpecialFunctions.Trigonometric.Deriv
import Mathlib.Tactic

set_option autoImplicit false
set_option maxHeartbeats 800000
namespace DiamondConformalCurrent
open Finset
noncomputable section

def timeComponent (radius spatialSquared time : ℝ) : ℝ :=
  Real.pi / radius * (radius^2-time^2-spatialSquared)
def spatialComponent (radius time coordinate : ℝ) : ℝ :=
  -2*Real.pi/radius*time*coordinate

theorem time_derivative (radius spatialSquared time : ℝ) :
    HasDerivAt (timeComponent radius spatialSquared)
      (-2*Real.pi/radius*time) time := by
  have h := (((hasDerivAt_const time (radius^2)).sub
    ((hasDerivAt_id time).pow 2)).sub_const spatialSquared).const_mul (Real.pi/radius)
  convert! h using 1
  dsimp [timeComponent]
  ring

theorem spatial_derivative (radius time coordinate : ℝ) :
    HasDerivAt (spatialComponent radius time)
      (-2*Real.pi/radius*time) coordinate := by
  change HasDerivAt (fun y : ℝ => -2*Real.pi/radius*time*y)
    (-2*Real.pi/radius*time) coordinate
  simpa only [mul_one, id_eq] using
    (hasDerivAt_id coordinate).const_mul (-2*Real.pi/radius*time)

/-- Actual divergence in n+1 spacetime dimensions, from component derivatives. -/
theorem diamond_divergence (n : ℕ) (radius spatialSquared time : ℝ)
    (x : Fin n → ℝ) :
    deriv (timeComponent radius spatialSquared) time +
      (∑ i : Fin n, deriv (spatialComponent radius time) (x i)) =
        -2*Real.pi/radius*time*(n+1) := by
  simp only [(time_derivative radius spatialSquared time).deriv,
    (spatial_derivative radius time _).deriv, sum_const, card_univ,
    Fintype.card_fin, nsmul_eq_mul]
  ring

section TensorContraction
variable {I : Type*} [Fintype I]

/-- Symmetry permits contraction with the symmetric gradient. -/
theorem symmetric_contraction (T D : I → I → ℝ)
    (hT : ∀ i j, T i j = T j i) :
    (∑ i, ∑ j, T i j*((D i j+D j i)/2)) = ∑ i, ∑ j, T i j*D i j := by
  have hswap : (∑ i, ∑ j, T i j*D j i) = ∑ i, ∑ j, T i j*D i j := by
    rw [sum_comm]
    apply sum_congr rfl
    intro i _
    apply sum_congr rfl
    intro j _
    rw [hT j i]
  have hsplit : (∑ i, ∑ j, T i j*((D i j+D j i)/2)) =
      ((∑ i, ∑ j, T i j*D i j) + (∑ i, ∑ j, T i j*D j i))/2 := by
    simp only [← mul_div_assoc, mul_add, ← sum_div, sum_add_distrib]
  rw [hsplit, hswap]
  ring

/-- The local divergence identity for a conserved symmetric stress tensor and
a conformal Killing field. dT and D are its first jets at a point; this proves
the contraction, not existence of a renormalized QFT stress tensor. -/
theorem conformal_current_divergence
    (T D eta : I → I → ℝ) (dT : I → I → I → ℝ) (xi : I → ℝ) (c : ℝ)
    (hT : ∀ i j, T i j=T j i)
    (hcons : ∀ j, ∑ i, dT i i j=0)
    (hCKV : ∀ i j, (D i j+D j i)/2=c*eta i j) :
    (∑ i, ∑ j, (dT i i j*xi j+T i j*D i j)) =
      c*(∑ i, ∑ j, T i j*eta i j) := by
  have hzero : (∑ i, ∑ j, dT i i j*xi j)=0 := by
    rw [sum_comm]
    simp only [← sum_mul, hcons, zero_mul, sum_const_zero]
  simp only [sum_add_distrib]
  rw [hzero, zero_add, ← symmetric_contraction T D hT]
  simp only [hCKV, mul_left_comm _ c, ← mul_sum]

end TensorContraction
#print axioms time_derivative
#print axioms spatial_derivative
#print axioms diamond_divergence
#print axioms symmetric_contraction
#print axioms conformal_current_divergence
end
end DiamondConformalCurrent
