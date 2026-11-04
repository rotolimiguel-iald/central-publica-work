import TGLExt.EquivariantSection
import Mathlib.Tactic.NoncommRing

set_option autoImplicit false
set_option maxHeartbeats 800000

/-! Finite centralizer criterion and perturbative transport bookkeeping.
No geometric identification or universal physical coefficient is assumed.
The centralizer of a faithful diagonal density is the range of specExpect.
-/
namespace CentralizerRemainderPerturbation
open Matrix TGLExt
noncomputable section
variable {n : Type} [Fintype n] [DecidableEq n]

/-- Commuting with the entire preserved algebra means being scalar on each
spectral block, not merely being block diagonal. -/
theorem commutes_with_preserved_algebra_iff (d : n → ℝ) (Q : Matrix n n ℂ) :
    (∀ X, Commute Q (specExpect d X)) ↔
      ((∀ i j, i ≠ j → Q i j = 0) ∧
       ∀ i j, d i = d j → Q i i = Q j j) := by
  have hs (i j : n) (hd : d i = d j) :
      specExpect d (single i j (1 : ℂ)) = single i j 1 := by
    ext k l
    by_cases hik : i = k
    · subst k
      by_cases hjl : j = l
      · subst l; simp [specExpect_apply, hd]
      · simp [specExpect_apply, hjl]
    · simp [specExpect_apply, hik]
  constructor
  · intro h
    constructor
    · intro i j hij
      have hc := h (single j j 1)
      rw [hs j j rfl] at hc
      have he := congrArg (fun Y : Matrix n n ℂ => Y i j)
        hc.eq
      simpa [Matrix.mul_apply, single_apply, hij, Ne.symm hij] using he
    · intro i j hd
      have hc := h (single i j 1)
      rw [hs i j hd] at hc
      have he := congrArg (fun Y : Matrix n n ℂ => Y i j)
        hc.eq
      simpa [Matrix.mul_apply, single_apply] using he
  · rintro ⟨hoff, hblock⟩ X
    have hdiag : Q = diagonal (fun i => Q i i) := by
      ext i j
      by_cases hij : i = j
      · subst j; simp
      · simp [diagonal_apply_ne _ hij, hoff i j hij]
    rw [hdiag]
    show diagonal (fun i => Q i i) * specExpect d X =
      specExpect d X * diagonal (fun i => Q i i)
    ext i j
    by_cases hd : d i = d j
    · simp [diagonal_mul, mul_diagonal, specExpect_apply, hd, hblock i j hd, mul_comm]
    · simp [diagonal_mul, mul_diagonal, specExpect_apply, hd]

/-- In this full matrix setting the relative commutant is itself contained in
the preserved algebra. This is not an assertion for arbitrary representations. -/
theorem invisible_generator_is_preserved (d : n → ℝ) (Q : Matrix n n ℂ)
    (h : ∀ X, Commute Q (specExpect d X)) : specExpect d Q = Q := by
  have hd := (commutes_with_preserved_algebra_iff d Q).mp h
  ext i j
  by_cases he : d i = d j
  · simp [specExpect_apply, he]
  · have hij : i ≠ j := fun h => he (congrArg d h)
    simp [specExpect_apply, he, hd.1 i j hij]

/-- Commuting with the density alone does not imply centrality in a degenerate
spectral block. The tracial density has every matrix in its centralizer. -/
theorem degenerate_block_counterexample :
    let d : Fin 2 → ℝ := fun _ => 1 / 2
    let Q : Matrix (Fin 2) (Fin 2) ℂ := !![1, 0; 0, 0]
    let X : Matrix (Fin 2) (Fin 2) ℂ := !![0, 1; 1, 0]
    specExpect d Q = Q ∧ specExpect d X = X ∧ ¬Commute Q X := by
  dsimp
  constructor
  · ext i j; simp [specExpect_apply]
  constructor
  · ext i j; simp [specExpect_apply]
  · intro h
    have he := congrArg (fun Y : Matrix (Fin 2) (Fin 2) ℂ => Y 0 1) h.eq
    norm_num [Matrix.mul_apply, Fin.sum_univ_two] at he

section Algebra
variable {A : Type*} [Ring A]

/-- First-order commutator coefficient for R(e)=R0+e R1 and X(e)=X0+e X1.
Taking e as a central scalar yields this coefficient; it is not [R1,X0] alone. -/
theorem transported_first_order_balance (K0 K1 Q0 Q1 X0 X1 : A)
    (h : K1 * X0 - X0 * K1 + (K0 * X1 - X1 * K0) = 0) :
    (K1-Q1)*X0-X0*(K1-Q1) + ((K0-Q0)*X1-X1*(K0-Q0)) =
      -(Q1*X0-X0*Q1 + (Q0*X1-X1*Q0)) := by
  have hi : (K1-Q1)*X0-X0*(K1-Q1) + ((K0-Q0)*X1-X1*(K0-Q0)) =
      (K1*X0-X0*K1+(K0*X1-X1*K0)) -
      (Q1*X0-X0*Q1+(Q0*X1-X1*Q0)) := by noncomm_ring
  rw [hi, h, zero_sub]

/-- Moving a centralizer by a change of representation can move its center
while preserving exact commutation of the transported pair. -/
theorem transported_commutator (u v R X : A) (hvu : v*u=1) :
    (u*R*v)*(u*X*v)-(u*X*v)*(u*R*v) = u*(R*X-X*R)*v := by
  calc
    _ = u*R*(v*u)*X*v - u*X*(v*u)*R*v := by noncomm_ring
    _ = _ := by rw [hvu]; noncomm_ring

end Algebra

/-- The algebraic class alone admits any nonzero amplitude and any positive
perturbative order. This is a finite model, not a relativistic QFT counterexample. -/
theorem arbitrary_order_obstruction (c e : ℂ) (m : ℕ) :
    let R : Matrix (Fin 2) (Fin 2) ℂ := !![0, c*e^m; c*e^m, 0]
    let X : Matrix (Fin 2) (Fin 2) ℂ := !![1, 0; 0, -1]
    (R*X-X*R) 0 1 = -2*c*e^m := by
  dsimp
  simp [Matrix.mul_apply, Fin.sum_univ_two]
  ring

#print axioms commutes_with_preserved_algebra_iff
#print axioms invisible_generator_is_preserved
#print axioms degenerate_block_counterexample
#print axioms transported_first_order_balance
#print axioms transported_commutator
#print axioms arbitrary_order_obstruction
end
end CentralizerRemainderPerturbation
