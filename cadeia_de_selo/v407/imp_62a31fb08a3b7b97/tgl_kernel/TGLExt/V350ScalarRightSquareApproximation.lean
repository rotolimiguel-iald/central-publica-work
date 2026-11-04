import TGLExt.V350SquareResolventSupport
import TGLExt.V350ScalarRightFunctionalStability

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 200000
set_option synthInstance.maxHeartbeats 200000

namespace TGLV350.Regular
open TGLExt Filter
open scoped Topology
noncomputable section

private theorem rightSelfadjointValue (P : SiteProfile)
    (a : scalarPairedRightAlgebra P) (ha : star a = a) : star a.val = a.val := by
  change (star a).val = a.val
  exact congrArg (fun b : scalarPairedRightAlgebra P => b.val) ha

theorem squareResolvent_mem {H : Type} [NormedAddCommGroup H]
    [InnerProductSpace ℂ H] [CompleteSpace H] (N : VonNeumannAlgebra H)
    (A : H →L[ℂ] H) (hA : star A = A) (hmem : A ∈ N) (n : ℕ) :
    squareResolvent A n ∈ N := by
  apply positiveResolvent_mem
  · exact N.toStarSubalgebra.smul_mem (N.toStarSubalgebra.mul_mem hmem hmem)
      (((n : ℝ)+1 : ℝ) : ℂ)
  · apply smul_nonneg (by positivity : 0 ≤ (n : ℝ)+1)
    simpa only [hA] using star_mul_self_nonneg A

theorem squareResolvent_complement_eq {H : Type} [NormedAddCommGroup H]
    [InnerProductSpace ℂ H] [CompleteSpace H]
    (A : H →L[ℂ] H) (hA : star A = A) (n : ℕ) :
    ((n : ℝ)+1) • (A*(squareResolvent A n*A)) = 1-squareResolvent A n := by
  have hp : 0 ≤ ((n : ℝ)+1) • (A*A) := smul_nonneg (by positivity)
    (by simpa only [hA] using star_mul_self_nonneg A)
  have he := positiveResolvent_right_inverse _ hp
  change (1+((n : ℝ)+1) • (A*A))*squareResolvent A n = 1 at he
  rw [add_mul, one_mul, smul_mul_assoc, mul_assoc, (squareResolvent_commutes A hA n).eq] at he
  calc
    _ = (squareResolvent A n + ((n : ℝ)+1) • (A*(squareResolvent A n*A))) -
        squareResolvent A n := by abel
    _ = _ := congrArg (fun T : H →L[ℂ] H => T-squareResolvent A n) he

private theorem commutingDifferenceSquares {B : Type*} [NonUnitalRing B] [Module ℂ B]
    (A D : B) (h : Commute A D) :
    A*D = (1/4 : ℂ) • ((A+D)*(A+D)-(A-D)*(A-D)) := by
  have he : (A+D)*(A+D)-(A-D)*(A-D) = (4 : ℂ) • (A*D) := by
    simp only [mul_add, add_mul, mul_sub, sub_mul, ← h.eq]
    module
  rw [he, smul_smul]
  norm_num

private theorem subalgebraDifferenceSquares {H : Type} [NormedAddCommGroup H]
    [InnerProductSpace ℂ H] [CompleteSpace H]
    (E : NonUnitalStarSubalgebra ℂ (H →L[ℂ] H)) (a d : E) (h : Commute a d) :
    a*d = (1/4 : ℂ) • ((a+d)*(a+d)-(a-d)*(a-d)) := by
  apply Subtype.ext
  exact commutingDifferenceSquares a.val d.val
    (congrArg (fun b : E => b.val) h.eq)

private theorem cutoffSelfadjoint {H : Type} [NormedAddCommGroup H]
    [InnerProductSpace ℂ H] [CompleteSpace H] (D R : H →L[ℂ] H)
    (he : D = 1-R) (hs : star R = R) : star D = D := by
  rw [he, star_sub, star_one, hs]

private theorem commutingCutoff {H : Type} [NormedAddCommGroup H]
    [InnerProductSpace ℂ H] (A D R : H →L[ℂ] H)
    (he : D = 1-R) (h : Commute A R) : Commute A D := by
  change A*D=D*A
  rw [he]
  simp only [mul_sub, sub_mul, mul_one, one_mul, h.eq]

private theorem commutingProductSelfadjoint {H : Type} [NormedAddCommGroup H]
    [InnerProductSpace ℂ H] [CompleteSpace H] (A D : H →L[ℂ] H)
    (ha : star A=A) (hd : star D=D) (h : Commute A D) : star (A*D)=A*D := by
  calc
    _ = star D * star A := ContinuousLinearMap.adjoint_comp A D
    _ = D*A := congrArg₂ (fun X Y : H →L[ℂ] H => X*Y) hd ha
    _ = _ := h.eq.symm

private theorem vectorApproximationTendsto {H B : Type} [NormedAddCommGroup H]
    (j : B → H) (f : ℕ → B) (v : H) (g : ℕ → H)
    (ht : Tendsto g atTop (𝓝 0)) (he : ∀ n, j (f n) = v-g n) :
    Tendsto (fun n => j (f n)) atTop (𝓝 v) := by
  rw [funext he]
  have hd : Tendsto (fun n => v-g n) atTop (𝓝 (v-0)) := tendsto_const_nhds.sub ht
  simpa only [sub_zero] using hd

/-- R_n a is a genuine right pair; R_n itself need not belong to the nonunital algebra. -/
def scalarRightResolventPair (P : SiteProfile) (a : scalarPairedRightAlgebra P)
    (ha : star a = a) (n : ℕ) : scalarPairedRightAlgebra P :=
  scalarSelfadjointRightMultiplier P a ha (squareResolvent a.val n)
    (squareResolvent_mem (scalarGNSCommutant P) a.val (rightSelfadjointValue P a ha)
      (scalarPairedRightAlgebra_mem_commutant P a.val a.property) n)
    (squareResolvent_nonneg a.val (rightSelfadjointValue P a ha) n).isSelfAdjoint.star_eq
    (squareResolvent_commutes a.val (rightSelfadjointValue P a ha) n).symm

/-- Construct the cutoff inside E first, without assuming that E contains the identity. -/
def scalarRightSquareCutoff (P : SiteProfile) (a : scalarPairedRightAlgebra P)
    (ha : star a = a) (n : ℕ) : scalarPairedRightAlgebra P :=
  ((((n : ℝ)+1 : ℝ) : ℂ)) • (a * scalarRightResolventPair P a ha n)

theorem scalarRightSquareCutoff_value (P : SiteProfile) (a : scalarPairedRightAlgebra P)
    (ha : star a = a) (n : ℕ) :
    (scalarRightSquareCutoff P a ha n).val = 1-squareResolvent a.val n :=
  squareResolvent_complement_eq a.val (rightSelfadjointValue P a ha) n

theorem scalarRightSquareCutoff_star (P : SiteProfile) (a : scalarPairedRightAlgebra P)
    (ha : star a = a) (n : ℕ) :
    star (scalarRightSquareCutoff P a ha n) = scalarRightSquareCutoff P a ha n := by
  apply Subtype.ext
  exact cutoffSelfadjoint (scalarRightSquareCutoff P a ha n).val (squareResolvent a.val n)
    (scalarRightSquareCutoff_value P a ha n)
    (squareResolvent_nonneg a.val (rightSelfadjointValue P a ha) n).isSelfAdjoint.star_eq

theorem scalarRightSquareCutoff_commutes (P : SiteProfile) (a : scalarPairedRightAlgebra P)
    (ha : star a = a) (n : ℕ) : Commute a (scalarRightSquareCutoff P a ha n) := by
  apply Subtype.ext
  exact commutingCutoff a.val (scalarRightSquareCutoff P a ha n).val (squareResolvent a.val n)
    (scalarRightSquareCutoff_value P a ha n)
    (squareResolvent_commutes a.val (rightSelfadjointValue P a ha) n)

def scalarRightSquareApproximation (P : SiteProfile) (a : scalarPairedRightAlgebra P)
    (ha : star a = a) (n : ℕ) : scalarPairedRightAlgebra P :=
  a * scalarRightSquareCutoff P a ha n

theorem scalarRightSquareApproximation_star (P : SiteProfile)
    (a : scalarPairedRightAlgebra P) (ha : star a = a) (n : ℕ) :
    star (scalarRightSquareApproximation P a ha n) = scalarRightSquareApproximation P a ha n := by
  apply Subtype.ext
  exact commutingProductSelfadjoint a.val (scalarRightSquareCutoff P a ha n).val
    (rightSelfadjointValue P a ha)
    (rightSelfadjointValue P _ (scalarRightSquareCutoff_star P a ha n))
    (congrArg (fun b : scalarPairedRightAlgebra P => b.val)
      (scalarRightSquareCutoff_commutes P a ha n).eq)

theorem scalarRightSquareApproximation_difference_of_squares (P : SiteProfile)
    (a : scalarPairedRightAlgebra P) (ha : star a = a) (n : ℕ) :
    let d : scalarPairedRightAlgebra P := scalarRightSquareCutoff P a ha n
    scalarRightSquareApproximation P a ha n =
      ((1/4 : ℂ) • ((a+d)*(a+d)-(a-d)*(a-d)) : scalarPairedRightAlgebra P) := by
  refine subalgebraDifferenceSquares (H := ScalarGNSHilbert P) (scalarPairedRightAlgebra P)
    a (scalarRightSquareCutoff P a ha n) ?_
  exact scalarRightSquareCutoff_commutes P a ha n

theorem scalarRightSquareApproximation_vector (P : SiteProfile)
    (a : scalarPairedRightAlgebra P) (ha : star a = a) (n : ℕ) :
    scalarRightPairVector P (scalarRightSquareApproximation P a ha n) =
      scalarRightPairVector P a - squareResolvent a.val n (scalarRightPairVector P a) := by
  exact (congrArg (scalarRightPairVector P) (scalarRightSquareCutoff_commutes P a ha n).eq).trans
    ((scalarRightPairVector_mul P (scalarRightSquareCutoff P a ha n) a).trans
      (congrArg (fun T : ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P =>
        T (scalarRightPairVector P a)) (scalarRightSquareCutoff_value P a ha n)))

theorem scalarRightSquareApproximation_vector_tendsto (P : SiteProfile)
    (a : scalarPairedRightAlgebra P) (ha : star a = a) :
    Tendsto (fun n => scalarRightPairVector P (scalarRightSquareApproximation P a ha n))
      atTop (𝓝 (scalarRightPairVector P a)) := by
  refine vectorApproximationTendsto
    (fun b : scalarPairedRightAlgebra P => scalarRightPairVector P b)
    (scalarRightSquareApproximation P a ha) (scalarRightPairVector P a)
    (fun n => squareResolvent a.val n (scalarRightPairVector P a)) ?_ ?_
  · exact squareResolvent_tendsto_zero_on_rangeClosure a.val (rightSelfadjointValue P a ha)
      (scalarRightPairVector P a) (scalarRightPairVector_mem_range_closure P a)
  · intro n; exact scalarRightSquareApproximation_vector P a ha n

#print axioms squareResolvent_mem
#print axioms squareResolvent_complement_eq
#print axioms scalarRightSquareCutoff_value
#print axioms scalarRightSquareCutoff_star
#print axioms scalarRightSquareCutoff_commutes
#print axioms scalarRightSquareApproximation_star
#print axioms scalarRightSquareApproximation_difference_of_squares
#print axioms scalarRightSquareApproximation_vector
#print axioms scalarRightSquareApproximation_vector_tendsto
end
end TGLV350.Regular
