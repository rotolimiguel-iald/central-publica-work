import TGLExt.BoundedPerturbationCocycle

set_option autoImplicit false
set_option maxHeartbeats 900000
namespace ChatgptAudit.SpectatorCancellation
open TGLExt Filter Topology Set ChatgptAudit.UnitaryDuhamel ChatgptAudit.BoundedPerturbation
noncomputable section

local instance operatorRationalAlgebra (P : SiteProfile) :
    NormedAlgebra ℚ (TowerHilbert P →L[ℂ] TowerHilbert P) :=
  NormedAlgebra.restrictScalars ℚ ℂ _

local instance operatorRationalTower (P : SiteProfile) :
    IsScalarTower ℚ ℂ (TowerHilbert P →L[ℂ] TowerHilbert P) :=
  IsScalarTower.restrictScalars ℚ ℂ _

theorem evolution_commuting_sum {P : SiteProfile} (H K : Operator P)
    (hHK : Commute H K) (t : ℝ) :
    evolution (H+K) t = evolution H t * evolution K t := by
  unfold evolution
  rw [smul_add, NormedSpace.exp_add_of_commute
    ((hHK.smul_left (((t : ℂ)*Complex.I))).smul_right (((t : ℂ)*Complex.I)))]

/-- A commuting spectator cancels from the relative evolution exactly. -/
theorem bounded_cocycle_spectator {P : SiteProfile} (H K V : Operator P)
    (hKH : Commute K H) (hKV : Commute K V) (t : ℝ) :
    boundedCocycle (H+K) V t = boundedCocycle H V t := by
  have hKVH : Commute (H+V) K := (hKH.add_right hKV).symm
  have he : evolution (H+K) (-t) = evolution K (-t) * evolution H (-t) := by
    rw [add_comm H K]
    exact evolution_commuting_sum K H hKH (-t)
  calc
    boundedCocycle (H+K) V t =
        (evolution (H+V) t * evolution K t) *
          (evolution K (-t) * evolution H (-t)) := by
      unfold boundedCocycle
      rw [show H+K+V = (H+V)+K by abel,
        evolution_commuting_sum (H+V) K hKVH t, he]
    _ = evolution (H+V) t * (evolution K t * evolution K (-t)) *
        evolution H (-t) := by simp only [mul_assoc]
    _ = boundedCocycle H V t := by
      rw [evolution_mul_neg, mul_one]
      rfl

theorem bounded_cocycle_background_extension {P : SiteProfile} (H G V : Operator P)
    (hGH : Commute (G-H) H) (hGV : Commute (G-H) V) (t : ℝ) :
    boundedCocycle G V t = boundedCocycle H V t := by
  have h := bounded_cocycle_spectator H (G-H) V hGH hGV t
  rw [show H + (G-H) = G by abel] at h
  exact h

/-- Only the spectator part of the background must commute with the old potential. -/
theorem varying_background_duhamel {P : SiteProfile} (H G V W : Operator P)
    (hG : IsSelfAdjoint G) (hV : IsSelfAdjoint V) (hW : IsSelfAdjoint W)
    (hGH : Commute (G-H) H) (hGV : Commute (G-H) V) (t : ℝ) :
    ‖boundedCocycle H V t - boundedCocycle G W t‖ ≤ ‖V-W‖ * |t| := by
  rw [← bounded_cocycle_background_extension H G V hGH hGV t]
  exact bounded_cocycle_perturbation_bound G V W hG hV hW t

theorem varying_background_bound_on_interval {P : SiteProfile} (H G V W : Operator P)
    (hG : IsSelfAdjoint G) (hV : IsSelfAdjoint V) (hW : IsSelfAdjoint W)
    (hGH : Commute (G-H) H) (hGV : Commute (G-H) V) (T t : ℝ) (ht : |t| ≤ T) :
    ‖boundedCocycle H V t - boundedCocycle G W t‖ ≤ ‖V-W‖ * T :=
  (varying_background_duhamel H G V W hG hV hW hGH hGV t).trans
    (mul_le_mul_of_nonneg_left ht (norm_nonneg _))

#print axioms operatorRationalAlgebra
#print axioms operatorRationalTower
#print axioms evolution_commuting_sum
#print axioms bounded_cocycle_spectator
#print axioms bounded_cocycle_background_extension
#print axioms varying_background_duhamel
#print axioms varying_background_bound_on_interval
end
end ChatgptAudit.SpectatorCancellation
