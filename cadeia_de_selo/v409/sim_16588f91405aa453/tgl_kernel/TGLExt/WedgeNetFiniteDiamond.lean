import TGLExt.WedgeNet

set_option autoImplicit false
set_option maxHeartbeats 1000000

/-!
Scope audit of the existing PRODUCT_TOWER regional witness.
No new net, physical state, dynamics, or gate is defined here.
The geometric region is an ordinary round open Minkowski diamond.
The result applies to the existing wedgeNet, not to every AQFT net.
-/
namespace ChatgptAudit.WedgeNetFiniteDiamond

open TGLExt TGL.SpecificAQFT
noncomputable section

/-- A region with an upper bound on its first spatial coordinate contains no
translated right wedge. -/
theorem no_right_wedge_of_upper_bound (O : Set (Fin 4 → ℝ)) (b : ℝ)
    (h : ∀ x ∈ O, x 1 ≤ b) : ¬ hasRW O := by
  rintro ⟨a, ha⟩
  let m := max (|a 0| + a 1) b + 1
  have hm : |a 0| + a 1 < m := by
    dsimp [m]
    linarith [le_max_left (|a 0| + a 1) b]
  have hb : b < m := by
    dsimp [m]
    linarith [le_max_right (|a 0| + a 1) b]
  have hp := h _ (ha (deep_right_mem a m hm))
  simp only [if_true] at hp
  linarith

/-- The analogous lower-bound obstruction for a left wedge. -/
theorem no_left_wedge_of_lower_bound (O : Set (Fin 4 → ℝ)) (b : ℝ)
    (h : ∀ x ∈ O, b ≤ x 1) : ¬ hasLW O := by
  rintro ⟨a, ha⟩
  let m := max (|a 0| - a 1) (-b) + 1
  have hm : |a 0| - a 1 < m := by
    dsimp [m]
    linarith [le_max_left (|a 0| - a 1) (-b)]
  have hb : -b < m := by
    dsimp [m]
    linarith [le_max_right (|a 0| - a 1) (-b)]
  have hp := h _ (ha (deep_left_mem a m hm))
  simp only [if_true] at hp
  linarith

/-- This is the actual algebra assigned by the existing canonical construction. -/
theorem bounded_region_has_scalar_algebra (O : Set (Fin 4 → ℝ)) (lo hi : ℝ)
    (hlo : ∀ x ∈ O, lo ≤ x 1) (hhi : ∀ x ∈ O, x 1 ≤ hi) :
    wedgeNet O = scalarAlg :=
  wedgeNet_scalar (no_right_wedge_of_upper_bound O hi hhi)
    (no_left_wedge_of_lower_bound O lo hlo)

/-- Round open diamond centred at c, with tip separation 2*r in units c=1. -/
def minkowskiDiamond (c : Fin 4 → ℝ) (r : ℝ) : Set (Fin 4 → ℝ) :=
  {x | |x 0 - c 0| + Real.sqrt
    ((x 1 - c 1)^2 + (x 2 - c 2)^2 + (x 3 - c 3)^2) < r}

theorem diamond_coordinate_bound (c : Fin 4 → ℝ) (r : ℝ)
    (x : Fin 4 → ℝ) (hx : x ∈ minkowskiDiamond c r) :
    c 1 - r ≤ x 1 ∧ x 1 ≤ c 1 + r := by
  let s := (x 1 - c 1)^2 + (x 2 - c 2)^2 + (x 3 - c 3)^2
  have hs : 0 ≤ s := by dsimp [s]; positivity
  have hsqrt := Real.sq_sqrt hs
  have hn := Real.sqrt_nonneg s
  have ha := sq_abs (x 1 - c 1)
  have hcoord : |x 1 - c 1| ≤ Real.sqrt s := by
    nlinarith [sq_nonneg (x 2 - c 2), sq_nonneg (x 3 - c 3),
      abs_nonneg (x 1 - c 1)]
  have hx' : |x 0 - c 0| + Real.sqrt s < r := hx
  have ht := abs_nonneg (x 0 - c 0)
  have hab : |x 1 - c 1| < r := by linarith
  have hp := (abs_lt.mp hab)
  constructor <;> linarith [hp.1, hp.2]

theorem finite_diamond_has_scalar_algebra (c : Fin 4 → ℝ) (r : ℝ) :
    theSpecificAQFTWitness.net (minkowskiDiamond c r) = scalarAlg := by
  change wedgeNet (minkowskiDiamond c r) = scalarAlg
  exact bounded_region_has_scalar_algebra _ (c 1 - r) (c 1 + r)
    (fun x hx => (diamond_coordinate_bound c r x hx).1)
    (fun x hx => (diamond_coordinate_bound c r x hx).2)

/-- On this algebra every bounded candidate remainder commutes, independently
of its origin, couplings, or proposed physical interpretation. No claim about
the domain of an unbounded modular Hamiltonian is hidden in this statement. -/
theorem any_bounded_remainder_is_invisible (c : Fin 4 → ℝ) (r : ℝ)
    (A : WCLM) (hA : A ∈ theSpecificAQFTWitness.net (minkowskiDiamond c r))
    (R : WCLM) : Commute R A := by
  rw [finite_diamond_has_scalar_algebra] at hA
  exact scalarAlg_commutes hA R

/-- The bounded diamond cannot simply be identified with the already constructed
nonabelian wedge algebra: the witness itself supplies a separating example. -/
theorem finite_diamond_is_not_the_wedge (c : Fin 4 → ℝ) (r : ℝ) :
    theSpecificAQFTWitness.net (minkowskiDiamond c r) ≠
      theSpecificAQFTWitness.net rightWedge := by
  intro heq
  obtain ⟨A, hA, B, hB, hAB⟩ := theSpecificAQFTWitness.wedge_nonabelian
  rw [← heq, finite_diamond_has_scalar_algebra] at hA
  exact hAB (scalarAlg_commutes hA B).symm.eq

#print axioms no_right_wedge_of_upper_bound
#print axioms no_left_wedge_of_lower_bound
#print axioms bounded_region_has_scalar_algebra
#print axioms diamond_coordinate_bound
#print axioms finite_diamond_has_scalar_algebra
#print axioms any_bounded_remainder_is_invisible
#print axioms finite_diamond_is_not_the_wedge

end
end ChatgptAudit.WedgeNetFiniteDiamond
