import CharacterPrefixStability

set_option autoImplicit false
set_option maxHeartbeats 800000
namespace ChatgptAudit.FiniteCharacterPrecision
open TGLExt ChatgptAudit.CocycleRealization ChatgptAudit.CharacterPrecision
  ChatgptAudit.SelectedAtlas ChatgptAudit.GravitationalRecord
noncomputable section

/-- A finite expression below the gap to the entire infinite tail. -/
def finiteSiteResolution (t : ℝ) (n : ℕ) : ℝ :=
  geometricContrast t n - 2 * geometricContrast t (n + 1)

/-- A finite minimum, using no infinite sum; the zero-prefix convention uses site zero. -/
def finitePrefixResolution (t : ℝ) : ℕ → ℝ
  | 0 => finiteSiteResolution t 0
  | N + 1 => min (finitePrefixResolution t N) (finiteSiteResolution t N)

theorem finite_site_resolution_positive {t : ℝ} (ht : t ≠ 0) (n : ℕ) :
    0 < finiteSiteResolution t n :=
  sub_pos.mpr (geometric_contrast_strict_succ ht n)

theorem finite_site_resolution_le_gap (t : ℝ) (n : ℕ) :
    finiteSiteResolution t n ≤ siteGap t n := by
  have h := geometric_contrast_tail_le t n
  unfold finiteSiteResolution siteGap
  linarith

theorem finite_prefix_resolution_positive {t : ℝ} (ht : t ≠ 0) (N : ℕ) :
    0 < finitePrefixResolution t N := by
  induction N with
  | zero => exact finite_site_resolution_positive ht 0
  | succ N ih => exact lt_min ih (finite_site_resolution_positive ht N)

theorem finite_prefix_resolution_le_gap (t : ℝ) (N : ℕ) :
    finitePrefixResolution t N ≤ prefixGap t N := by
  induction N with
  | zero => exact finite_site_resolution_le_gap t 0
  | succ N ih => exact min_le_min ih (finite_site_resolution_le_gap t N)

theorem finite_threshold_resolves_prefix (t : ℝ) (u v : ℕ → Bool) (N : ℕ)
    (hclose : |geometricLogReading t u - geometricLogReading t v| < finitePrefixResolution t N) :
    SamePrefix u v N :=
  near_readings_have_same_prefix t u v N
    (lt_of_lt_of_le hclose (finite_prefix_resolution_le_gap t N))

theorem finite_threshold_resolves_noisy_candidates (t z error : ℝ)
    (u v : ℕ → Bool) (N : ℕ)
    (hu : |geometricLogReading t u - z| ≤ error)
    (hv : |geometricLogReading t v - z| ≤ error)
    (hresolution : 2 * error < finitePrefixResolution t N) : SamePrefix u v N :=
  noisy_candidates_have_same_prefix t z error u v N hu hv
    (lt_of_lt_of_le hresolution (finite_prefix_resolution_le_gap t N))

theorem finite_threshold_resolves_record_prefix {U : Set Coordinate4} [Nonempty U]
    (t : ℝ) (R S : GravitationalResponseRecord U) (N : ℕ)
    (hclose : |recordCharacter t R - recordCharacter t S| < finitePrefixResolution t N) :
    SamePrefix (recordBits R) (recordBits S) N :=
  finite_threshold_resolves_prefix t (recordBits R) (recordBits S) N hclose

theorem finite_threshold_resolves_record_cut {U : Set Coordinate4} [Nonempty U]
    (t : ℝ) (R S : GravitationalResponseRecord U) (N n : ℕ) (k : RecordComponent) (q : ℚ)
    (hindex : Encodable.encode (n, k, q) < N)
    (hclose : |recordCharacter t R - recordCharacter t S| < finitePrefixResolution t N) :
    (recordValue R (TopologicalSpace.denseSeq U n) k < (q : ℝ) ↔
      recordValue S (TopologicalSpace.denseSeq U n) k < (q : ℝ)) :=
  near_record_characters_same_rational_cut t R S N n k q hindex
    (lt_of_lt_of_le hclose (finite_prefix_resolution_le_gap t N))

#print axioms finiteSiteResolution
#print axioms finitePrefixResolution
#print axioms finite_site_resolution_positive
#print axioms finite_site_resolution_le_gap
#print axioms finite_prefix_resolution_positive
#print axioms finite_prefix_resolution_le_gap
#print axioms finite_threshold_resolves_prefix
#print axioms finite_threshold_resolves_noisy_candidates
#print axioms finite_threshold_resolves_record_prefix
#print axioms finite_threshold_resolves_record_cut
end
end ChatgptAudit.FiniteCharacterPrecision
