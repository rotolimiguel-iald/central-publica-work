import ChainVolume

set_option autoImplicit false
set_option maxHeartbeats 800000
namespace ChatgptAudit
open TGLExt Matrix
open scoped Kronecker
noncomputable section
variable {P : SiteProfile}

theorem lastSiteMatrix_mul (n : ℕ) (a b : Matrix (Fin 2) (Fin 2) ℂ) :
    lastSiteMatrix n (a*b) = lastSiteMatrix n a * lastSiteMatrix n b := by
  cases n with
  | zero => rfl
  | succ n => simp only [lastSiteMatrix,← mul_kronecker_mul,one_mul]

theorem siteOperator_mul (n : ℕ) (a b : Matrix (Fin 2) (Fin 2) ℂ) :
    siteOperator P n (a*b) = siteOperator P n a * siteOperator P n b := by
  unfold siteOperator
  rw [lastSiteMatrix_mul,towerPi_mul]

theorem siteMark_star (n : ℕ) : star (siteMark P n) = siteMark P n := by
  unfold siteMark
  rw [← siteOperator_star,single_one_conjT]

theorem siteMark_square (n : ℕ) : siteMark P n * siteMark P n = siteMark P n := by
  unfold siteMark
  rw [← siteOperator_mul,Matrix.single_mul_single_same,one_mul]

theorem siteMark_nonnegative (n : ℕ) : 0 ≤ siteMark P n := by
  have h := star_mul_self_nonneg (siteMark P n)
  rwa [siteMark_star,siteMark_square] at h

theorem chainVolume_nonnegative (I : Finset ℕ) : 0 ≤ chainVolumeObject P I := by
  exact Finset.sum_nonneg (fun n _ => siteMark_nonnegative n)

def normalizedVolumeObject (P : SiteProfile) (I : Finset ℕ) : TowerHilbert P →L[ℂ] TowerHilbert P :=
  ∑ n ∈ I, ((P.w n : ℂ)⁻¹) • siteMark P n

theorem normalizedVolume_state (I : Finset ℕ) :
    omegaState P (normalizedVolumeObject P I) = (I.card : ℂ) := by
  rw [normalizedVolumeObject,omega_sum]
  have h : ∀ n, omegaState P ((P.w n : ℂ)⁻¹ • siteMark P n) = 1 := by
    intro n
    change inner ℂ (hOmega P) ((P.w n : ℂ)⁻¹ • (siteMark P n (hOmega P))) = 1
    rw [inner_smul_right]
    change (P.w n : ℂ)⁻¹ * omegaState P (siteMark P n) = 1
    rw [siteMark_state,inv_mul_cancel₀ (Complex.ofReal_ne_zero.mpr (ne_of_gt (P.pos n)))]
  simp only [h,Finset.sum_const,nsmul_eq_mul,mul_one]

#print axioms chainVolume_nonnegative
#print axioms normalizedVolume_state
end
end ChatgptAudit
