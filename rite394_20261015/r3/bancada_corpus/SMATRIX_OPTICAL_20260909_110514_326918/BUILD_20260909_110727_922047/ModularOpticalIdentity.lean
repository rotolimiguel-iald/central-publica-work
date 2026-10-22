import TGLExt.SMatrix
import TGLExt.UnitaryStateDerivative
import TGLExt.SitePauliObservables

set_option autoImplicit false
set_option maxHeartbeats 1800000

namespace ChatgptAudit.OpticalS

open Matrix TGLExt ChatgptAudit.Observable035
noncomputable section

/-- Exact displacement from identity; no small-parameter expansion. -/
def displacement {R : Type*} [Ring R] (S : R) : R := S - 1

/-- The optical balance in displacement convention. -/
def opticalBalance {R : Type*} [Ring R] [StarRing R] (S : R) : R :=
  displacement S + star (displacement S) + star (displacement S) * displacement S

theorem optical_balance_eq {R : Type*} [Ring R] [StarRing R] (S : R) :
    opticalBalance S = star S * S - 1 := by
  simp only [opticalBalance, displacement, star_sub, star_one]
  noncomm_ring

theorem optical_balance_zero_iff {R : Type*} [Ring R] [StarRing R] (S : R) :
    opticalBalance S = 0 ↔ star S * S = 1 := by
  rw [optical_balance_eq, sub_eq_zero]

theorem unitary_optical_balance {R : Type*} [Ring R] [StarRing R]
    (S : R) (hS : S ∈ unitary R) : opticalBalance S = 0 :=
  (optical_balance_zero_iff S).2 ((Unitary.mem_iff.mp hS).1)

theorem displacement_product {R : Type*} [Ring R] (S V : R) :
    displacement (S * V) =
      displacement S + displacement V + displacement S * displacement V := by
  unfold displacement
  noncomm_ring

/-- Order sensitivity survives in the exact quadratic term. -/
theorem displacement_order_difference {R : Type*} [Ring R] (S V : R) :
    displacement (S * V) - displacement (V * S) =
      displacement S * displacement V - displacement V * displacement S := by
  unfold displacement
  noncomm_ring

/-- Standard convention S = 1 + i T. -/
def transition {R : Type*} [Ring R] [Algebra ℂ R] (S : R) : R :=
  (-Complex.I) • displacement S

theorem transition_reconstructs {R : Type*} [Ring R] [Algebra ℂ R] (S : R) :
    1 + Complex.I • transition S = S := by
  simp [transition, smul_smul, displacement]

theorem transition_star {R : Type*} [Ring R] [StarRing R] [Algebra ℂ R]
    [StarModule ℂ R] (S : R) :
    star (transition S) = Complex.I • star (displacement S) := by
  simp [transition, star_smul]

theorem transition_positive_product {R : Type*} [Ring R] [StarRing R]
    [Algebra ℂ R] [StarModule ℂ R] (S : R) :
    star (transition S) * transition S =
      star (displacement S) * displacement S := by
  rw [transition_star]
  simp only [transition, smul_mul_assoc, mul_smul_comm, smul_smul]
  norm_num

/-- Exact optical identity, retaining the quadratic transition contribution. -/
theorem exact_optical_identity {R : Type*} [Ring R] [StarRing R]
    [Algebra ℂ R] [StarModule ℂ R] (S : R) (hS : S ∈ unitary R) :
    (-Complex.I) • (transition S - star (transition S)) =
      star (transition S) * transition S := by
  rw [transition_positive_product, transition_star]
  have hb := unitary_optical_balance S hS
  change displacement S + star (displacement S) +
    star (displacement S) * displacement S = 0 at hb
  calc
    (-Complex.I) • (transition S - Complex.I • star (displacement S)) =
        -(displacement S + star (displacement S)) := by
      simp only [transition, smul_sub, smul_smul]
      norm_num
      abel
    _ = star (displacement S) * displacement S -
        (displacement S + star (displacement S) +
          star (displacement S) * displacement S) := by abel
    _ = star (displacement S) * displacement S := by rw [hb]; simp

theorem transition_product {R : Type*} [Ring R] [Algebra ℂ R] (S V : R) :
    transition (S * V) =
      transition S + transition V + Complex.I • (transition S * transition V) := by
  simp only [transition, displacement_product, smul_add,
    smul_mul_assoc, mul_smul_comm, smul_smul]
  norm_num

/-- The forward matrix element equals total transition probability in that channel. -/
theorem matrix_optical_channel {n : Type*} [Fintype n] [DecidableEq n]
    (S : Matrix n n ℂ) (hS : S ∈ unitary (Matrix n n ℂ)) (j : n) :
    2 * (transition S j j).im = ∑ k, Complex.normSq (transition S k j) := by
  have hh := congrArg (fun M : Matrix n n ℂ => (M j j).re) (exact_optical_identity S hS)
  simp only [Matrix.smul_apply, smul_eq_mul, Matrix.sub_apply, Matrix.star_eq_conjTranspose,
    Matrix.conjTranspose_apply, Matrix.mul_apply, map_sum] at hh
  simpa [Complex.mul_re, Complex.normSq_apply, pow_two] using hh

/-- Direct instance on the canonical boundary S matrix. -/
theorem boundary_exact_optical (theta : ℝ) :
    (-Complex.I) • (transition (Smat theta) - star (transition (Smat theta))) =
      star (transition (Smat theta)) * transition (Smat theta) :=
  exact_optical_identity (Smat theta) (Smat_mem_unitary theta)

/-- The existing tower orbit may have noncommuting self-adjoint generators. -/
theorem tower_orbit_exact_optical (P : SiteProfile)
    (A C : TowerHilbert P →L[ℂ] TowerHilbert P)
    (hA : IsSelfAdjoint A) (hC : IsSelfAdjoint C) (s t : ℝ) :
    (-Complex.I) •
      (transition (operatorOrbit P A C s t) - star (transition (operatorOrbit P A C s t))) =
      star (transition (operatorOrbit P A C s t)) * transition (operatorOrbit P A C s t) :=
  exact_optical_identity _ (orbit_unitary P A C hA hC s t)

/-- A concrete instance within the existing tower, using its Pauli observables. -/
theorem pauli_orbit_exact_optical (P : SiteProfile) (n : ℕ) (s t : ℝ) :
    let S := operatorOrbit P (sitePauliX P n) (sitePauliY P n) s t
    (-Complex.I) • (transition S - star (transition S)) =
      star (transition S) * transition S :=
  tower_orbit_exact_optical P _ _ (site_pauli_x_selfadjoint P n)
    (site_pauli_y_selfadjoint P n) s t

/-- Direct nonlinear composition law on the existing noncommuting orbit. -/
theorem tower_orbit_transition_product (P : SiteProfile)
    (A C : TowerHilbert P →L[ℂ] TowerHilbert P) (s t : ℝ) :
    transition (operatorOrbit P A C s t) =
      transition (ChatgptAudit.Angular034.boundedPhase P A s) +
      transition (ChatgptAudit.Angular034.boundedPhase P C t) +
      Complex.I • (transition (ChatgptAudit.Angular034.boundedPhase P A s) *
        transition (ChatgptAudit.Angular034.boundedPhase P C t)) :=
  transition_product _ _

/-- The canonical first Taylor polynomial, used as a negative control. -/
def linearBoundary (theta : ℝ) : Matrix (Fin 2) (Fin 2) ℂ :=
  1 + (theta : ℂ) • Grot

theorem linear_boundary_defect (theta : ℝ) :
    (linearBoundary theta)ᴴ * linearBoundary theta =
      (1 + (theta : ℂ)^2) • (1 : Matrix (Fin 2) (Fin 2) ℂ) := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [linearBoundary, Grot, Matrix.mul_apply, Fin.sum_univ_two,
      Matrix.conjTranspose_apply] <;> ring

theorem nonzero_linear_boundary_not_unitary (theta : ℝ) (ht : theta ≠ 0) :
    linearBoundary theta ∉ unitary (Matrix (Fin 2) (Fin 2) ℂ) := by
  intro h
  have he := (Unitary.mem_iff.mp h).1
  change (linearBoundary theta)ᴴ * linearBoundary theta = 1 at he
  rw [linear_boundary_defect] at he
  have hz := congrArg (fun M : Matrix (Fin 2) (Fin 2) ℂ => M 0 0) he
  simp only [Matrix.smul_apply, Matrix.one_apply_eq, smul_eq_mul, mul_one] at hz
  have hs : (theta : ℂ)^2 = 0 := by linear_combination hz
  have hr : theta^2 = 0 := by exact_mod_cast hs
  apply ht
  nlinarith

end

#print axioms displacement
#print axioms opticalBalance
#print axioms optical_balance_eq
#print axioms optical_balance_zero_iff
#print axioms unitary_optical_balance
#print axioms displacement_product
#print axioms displacement_order_difference
#print axioms transition
#print axioms transition_reconstructs
#print axioms transition_star
#print axioms transition_positive_product
#print axioms exact_optical_identity
#print axioms transition_product
#print axioms matrix_optical_channel
#print axioms boundary_exact_optical
#print axioms tower_orbit_exact_optical
#print axioms pauli_orbit_exact_optical
#print axioms tower_orbit_transition_product
#print axioms linearBoundary
#print axioms linear_boundary_defect
#print axioms nonzero_linear_boundary_not_unitary
end ChatgptAudit.OpticalS
