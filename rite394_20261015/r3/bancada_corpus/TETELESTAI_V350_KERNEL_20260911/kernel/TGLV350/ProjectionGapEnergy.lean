import TGLV350.WeightedVariationalEnergy
import TGLV350.ProjectionGapLowerBound

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 200000

namespace TGLV350.Regular
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

theorem projectionGapPart_energy_difference (A B : H →L[ℂ] H) (c : ℝ)
    (hA : star A=A) (hBB : B*star B=A*(1-A)) :
    let e := projectionGapPart A c
    A*e*e=e*B*star B-(c-1) • (e*A*A) := by
  let e := projectionGapPart A c
  have heA : Commute e A := projectionGapPart_commutes A A c (Commute.refl A)
  have hs : e*e=e*(1-c • A) := projectionGapPart_square A c hA
  calc
    A*e*e = A*(e*e) := mul_assoc _ _ _
    _ = e*A*(1-c • A) := by rw [hs,← mul_assoc,heA.eq]
    _ = e*A-c • (e*A*A) := by rw [mul_sub,mul_one,mul_smul_comm]
    _ = e*B*star B-(c-1) • (e*A*A) := by
      rw [mul_assoc e B (star B),hBB]
      simp only [mul_sub,mul_one,← mul_assoc,sub_smul,one_smul]
      abel

theorem projectionGapPart_energy_annihilates (A B : H →L[ℂ] H) (c : ℝ) (η : H)
    (hA : 0 ≤ A) (hinj : Function.Injective A) (hBB : B*star B=A*(1-A))
    (henergy :
      (inner ℂ ((projectionGapPart A c*B*star B) η) η).re ≤
        (c-1)*(inner ℂ ((projectionGapPart A c*A*A) η) η).re) :
    (projectionGapPart A c*A) η=0 := by
  let e := projectionGapPart A c
  let L : H →L[ℂ] H := CFC.sqrt A*e
  have he : star e=e := (IsSelfAdjoint.of_nonneg (projectionGapPart_nonneg A c)).star_eq
  have heA : Commute e A := projectionGapPart_commutes A A c (Commute.refl A)
  have hroot : star L*L=A*e*e := by
    rw [weightedBlock_root_sandwich e A hA,he,heA.eq]
  have hnorm : ‖L η‖^2=(inner ℂ ((A*e*e) η) η).re := by
    rw [← hroot]
    change ‖L η‖^2=(inner ℂ (L.adjoint (L η)) η).re
    rw [ContinuousLinearMap.adjoint_inner_left]
    exact (inner_self_eq_norm_sq (𝕜:=ℂ) _).symm
  have hdiff := projectionGapPart_energy_difference A B c (IsSelfAdjoint.of_nonneg hA).star_eq hBB
  change A*e*e=e*B*star B-(c-1) • (e*A*A) at hdiff
  rw [hdiff] at hnorm
  change ‖L η‖^2=(inner ℂ (((e*B*star B) η)-(c-1) • ((e*A*A) η)) η).re at hnorm
  rw [inner_sub_left,Complex.sub_re] at hnorm
  have hsm : inner ℂ ((c-1) • ((e*A*A) η)) η=(c-1) • inner ℂ ((e*A*A) η) η :=
    inner_smul_left_eq_smul (𝕜:=ℂ) _ _ _
  rw [hsm] at hnorm
  have hs : ‖L η‖^2=0 := by
    have hh : ‖L η‖^2=(inner ℂ ((e*B*star B) η) η).re-
        (c-1)*(inner ℂ ((e*A*A) η) η).re := by simpa using hnorm
    linarith only [hh,henergy,sq_nonneg ‖L η‖]
  have hL : L η=0 := norm_eq_zero.mp (sq_eq_zero_iff.mp hs)
  have hAe : A (e η)=0 := by
    have hh := congrArg (fun v : H => (CFC.sqrt A : H →L[ℂ] H) v) hL
    change (CFC.sqrt A*CFC.sqrt A) (e η)=CFC.sqrt A 0 at hh
    simpa only [CFC.sqrt_mul_sqrt_self A hA,map_zero] using hh
  have heη : e η=0 := hinj (by simpa only [map_zero] using hAe)
  change (e*A) η=0
  rw [heA.eq]
  change A (e η)=0
  rw [heη,map_zero]

#print axioms projectionGapPart_energy_difference
#print axioms projectionGapPart_energy_annihilates
end
end TGLV350.Regular
