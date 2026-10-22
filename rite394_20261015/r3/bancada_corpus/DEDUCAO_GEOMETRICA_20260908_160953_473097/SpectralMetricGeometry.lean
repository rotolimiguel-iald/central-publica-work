import ExistingTowerRealization
set_option autoImplicit false
set_option maxHeartbeats 1800000
namespace ChatgptAudit.Geometry056
open ChatgptAudit.CocycleRealization
noncomputable section

def spectralDistance (t : ℝ) (u v : ℕ → Bool) : ℝ :=
  |geometricLogReading t u-geometricLogReading t v|

theorem spectral_distance_nonnegative (t : ℝ) (u v : ℕ → Bool) :
    0 ≤ spectralDistance t u v := abs_nonneg _

theorem spectral_distance_self (t : ℝ) (u : ℕ → Bool) :
    spectralDistance t u u=0 := by simp [spectralDistance]

theorem spectral_distance_symmetric (t : ℝ) (u v : ℕ → Bool) :
    spectralDistance t u v=spectralDistance t v u := abs_sub_comm _ _

theorem spectral_distance_triangle (t : ℝ) (u v w : ℕ → Bool) :
    spectralDistance t u w  ≤  spectralDistance t u v+spectralDistance t v w :=
  abs_sub_le _ _ _

theorem spectral_distance_zero_iff {t : ℝ} (ht : t≠0) (u v : ℕ → Bool) :
    spectralDistance t u v=0 ↔ u=v := by
  rw [spectralDistance,abs_eq_zero,sub_eq_zero]
  exact (geometric_log_reading_injective ht).eq_iff

theorem spectral_distance_positive {t : ℝ} (ht : t≠0)
    {u v : ℕ → Bool} (h : u≠v) : 0<spectralDistance t u v :=
  lt_of_le_of_ne (spectral_distance_nonnegative t u v)
    (Ne.symm (fun hz => h ((spectral_distance_zero_iff ht u v).mp hz)))

def scaledSpectralDistance (c t : ℝ) (u v : ℕ → Bool) : ℝ :=
  c*spectralDistance t u v

theorem scaled_spectral_distance_triangle {c : ℝ} (hc : 0 ≤ c)
    (t : ℝ) (u v w : ℕ → Bool) :
    scaledSpectralDistance c t u w  ≤ 
      scaledSpectralDistance c t u v+scaledSpectralDistance c t v w := by
  have h := mul_le_mul_of_nonneg_left (spectral_distance_triangle t u v w) hc
  simpa only [scaledSpectralDistance,mul_add] using h

theorem scaled_spectral_distance_zero_iff {c t : ℝ} (hc : 0<c) (ht : t≠0)
    (u v : ℕ → Bool) :
    scaledSpectralDistance c t u v=0 ↔ u=v := by
  rw [scaledSpectralDistance,mul_eq_zero]
  simp only [ne_of_gt hc,false_or,spectral_distance_zero_iff ht]

theorem different_scales_give_different_distances {c d t : ℝ}
    (hcd : c≠d) (ht : t≠0) {u v : ℕ → Bool} (huv : u≠v) :
    scaledSpectralDistance c t u v ≠ scaledSpectralDistance d t u v := by
  intro he
  have hn : spectralDistance t u v≠0 := ne_of_gt (spectral_distance_positive ht huv)
  exact hcd (mul_right_cancel₀ hn he)

def binaryCoordinateTest (c : ℝ) (n : ℕ) (u : ℕ → Bool) : ℝ :=
  if u n then c else 0

theorem coordinate_separates_with_arbitrary_size {u v : ℕ → Bool} (h : u≠v)
    (R : ℝ) :
    ∃ (n : ℕ) (c : ℝ),
      R < |binaryCoordinateTest c n u-binaryCoordinateTest c n v| := by
  have hex : ∃ n, u n≠v n := by
    by_contra hn
    apply h
    funext n
    by_contra hv
    exact hn ⟨n,hv⟩
  obtain ⟨n,hn⟩ := hex
  refine ⟨n,|R|+1,?_⟩
  have hpos : 0 ≤ |R|+1 := by positivity
  have hR := le_abs_self R
  cases hu : u n <;> cases hv : v n
  · exact False.elim (hn (hu.trans hv.symm))
  · simp only [binaryCoordinateTest,hu,hv,Bool.false_eq_true,if_false,if_true,
      zero_sub,abs_neg,abs_of_nonneg hpos]
    linarith
  · simp only [binaryCoordinateTest,hu,hv,Bool.false_eq_true,if_false,if_true,
      sub_zero,abs_of_nonneg hpos]
    linarith
  · exact False.elim (hn (hu.trans hv.symm))

#print axioms spectralDistance
#print axioms spectral_distance_nonnegative
#print axioms spectral_distance_self
#print axioms spectral_distance_symmetric
#print axioms spectral_distance_triangle
#print axioms spectral_distance_zero_iff
#print axioms spectral_distance_positive
#print axioms scaledSpectralDistance
#print axioms scaled_spectral_distance_triangle
#print axioms scaled_spectral_distance_zero_iff
#print axioms different_scales_give_different_distances
#print axioms binaryCoordinateTest
#print axioms coordinate_separates_with_arbitrary_size

end
end ChatgptAudit.Geometry056
