import TGLExt.LevelExpectationFamily
import Mathlib.Analysis.CStarAlgebra.PositiveLinearMap
import Mathlib.Analysis.CStarAlgebra.ContinuousFunctionalCalculus.Range
import Mathlib.Analysis.SpecialFunctions.ContinuousFunctionalCalculus.Rpow.Basic

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1500000

namespace TGLV350.Regular
open TGLExt ChatgptAudit
noncomputable section

/-- The actual finite-level expectation, restricted to the factor where its
positivity was constructed. This is not a centralizer expectation contract. -/
def levelPositiveMap (P : SiteProfile) (N : ℕ) :
    (theFactorObject P).toStarSubalgebra →ₚ[ℂ] (TowerHilbert P →L[ℂ] TowerHilbert P) where
  toLinearMap := (expectationLinear P N).comp
    (theFactorObject P).toStarSubalgebra.subtype.toLinearMap
  monotone' := by
    intro a b hab
    have hp := expectation_positive N (b.val-a.val)
      ((theFactorObject P).sub_mem b.property a.property) (sub_nonneg.mpr hab)
    change 0 ≤ expectationLinear P N (b.val-a.val) at hp
    rw [map_sub] at hp
    exact sub_nonneg.mp hp

theorem levelPositiveMap_one (P : SiteProfile) (N : ℕ) : levelPositiveMap P N 1 = 1 := by
  change towerExpectation P N 1 = 1
  have hh := expectation_fixes (P := P) N (1 : Matrix (chainIdx N) (chainIdx N) ℂ)
  rwa [towerPi_one] at hh

/-- An explicit bound depending only on f(1), not a separately chosen bound
for each positive map. Four is sufficient for bounded strong transport. -/
theorem positive_unital_four_norm_bound {A B : Type*}
    [CStarAlgebra A] [CStarAlgebra B] [PartialOrder A] [PartialOrder B]
    [StarOrderedRing A] [StarOrderedRing B]
    (f : A →ₚ[ℂ] B) (h1 : f 1 = 1) (x : A) : ‖f x‖ ≤ 4 * ‖x‖ := by
  have hone : ‖(1 : B)‖ ≤ 1 := by
    rcases subsingleton_or_nontrivial B with hs | hn
    · letI := hs
      rw [Subsingleton.elim (1 : B) 0, norm_zero]
      exact zero_le_one
    · letI := hn
      simp
  obtain ⟨y, hypos, hynorm, hy⟩ := CStarAlgebra.exists_sum_four_nonneg x
  have hb (i : Fin 4) : ‖f (y i)‖ ≤ ‖x‖ := by
    have hh := f.norm_apply_le_of_nonneg (y i) (hypos i)
    rw [h1] at hh
    exact (hh.trans (mul_le_of_le_one_left (norm_nonneg _) hone)).trans (hynorm i)
  conv_lhs => rw [hy]
  simp only [map_sum, map_smul]
  apply (norm_sum_le _ _).trans
  simp only [norm_smul, norm_pow, Complex.norm_I, one_pow, one_mul]
  exact (Finset.sum_le_sum (fun i _ => hb i)).trans_eq (by simp)

theorem vonNeumann_norm_closed {H : Type} [NormedAddCommGroup H]
    [InnerProductSpace ℂ H] [CompleteSpace H] (M : VonNeumannAlgebra H) :
    IsClosed (M : Set (H →L[ℂ] H)) := by
  rw [← VonNeumannAlgebra.centralizer_centralizer M]
  exact Set.isClosed_centralizer _

/-- The inherited operator order is the star order: the square root of a
positive element remains in the same norm-closed algebra. -/
theorem vonNeumann_starOrdered {H : Type} [NormedAddCommGroup H]
    [InnerProductSpace ℂ H] [CompleteSpace H] (M : VonNeumannAlgebra H) :
    StarOrderedRing M.toStarSubalgebra := by
  letI : IsClosed (M.toStarSubalgebra : Set (H →L[ℂ] H)) := vonNeumann_norm_closed M
  apply StarOrderedRing.of_nonneg_iff'
  · intro x y h z
    simpa only [add_comm] using add_le_add_left h z
  · intro x
    constructor
    · intro hx
      have hm : CFC.sqrt x.val ∈ M.toStarSubalgebra := by
        rw [CFC.sqrt_eq_real_sqrt x.val (show 0 ≤ x.val from hx)]
        exact cfcₙ_mem (𝕜' := ℂ) Real.sqrt x.property
      refine ⟨⟨CFC.sqrt x.val,hm⟩,Subtype.ext ?_⟩
      change x.val = star (CFC.sqrt x.val) * CFC.sqrt x.val
      rw [(CFC.sqrt_nonneg x.val).isSelfAdjoint.star_eq, CFC.sqrt_mul_sqrt_self x.val hx]
    · rintro ⟨s,hs⟩
      change 0 ≤ x.val
      rw [congrArg Subtype.val hs]
      exact star_mul_self_nonneg s.val

theorem levelExpectation_uniform_norm_bound (P : SiteProfile) (N : ℕ)
    (A : TowerHilbert P →L[ℂ] TowerHilbert P) (hA : A ∈ theFactorObject P) :
    ‖towerExpectation P N A‖ ≤ 4 * ‖A‖ := by
  letI : IsClosed ((theFactorObject P).toStarSubalgebra :
      Set (TowerHilbert P →L[ℂ] TowerHilbert P)) := vonNeumann_norm_closed (theFactorObject P)
  letI : StarOrderedRing (theFactorObject P).toStarSubalgebra :=
    vonNeumann_starOrdered (theFactorObject P)
  exact positive_unital_four_norm_bound (levelPositiveMap P N) (levelPositiveMap_one P N)
    (⟨A,hA⟩ : (theFactorObject P).toStarSubalgebra)

#print axioms levelPositiveMap
#print axioms levelPositiveMap_one
#print axioms positive_unital_four_norm_bound
#print axioms vonNeumann_norm_closed
#print axioms vonNeumann_starOrdered
#print axioms levelExpectation_uniform_norm_bound
end
end TGLV350.Regular
