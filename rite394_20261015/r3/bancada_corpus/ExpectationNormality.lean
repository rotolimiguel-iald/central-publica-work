import ExpectationContinuity
import GeneralExpectationPositive
import MonotoneOperatorLimit

set_option autoImplicit false
set_option maxHeartbeats 1600000

namespace ChatgptAudit.Expectation047

open TGLExt Filter ChatgptAudit.Aperiodic046
open scoped Topology ComplexOrder

noncomputable section

/-- A fixed commutation relation survives a strong limit along any nontrivial filter. -/
theorem strong_net_limit_commutes (P : SiteProfile)
    {ι : Type*} (l : Filter ι) [l.NeBot]
    (A : ι → TowerHilbert P →L[ℂ] TowerHilbert P)
    (B Y : TowerHilbert P →L[ℂ] TowerHilbert P)
    (hlim : ∀ v, Tendsto (fun i => A i v) l (𝓝 (B v)))
    (hcomm : ∀ i, Y * A i = A i * Y) :
    Y * B = B * Y := by
  ext v
  change Y (B v) = B (Y v)
  have he : (fun i => Y (A i v)) = (fun i => A i (Y v)) := by
    funext i
    simpa only [mul_apply_eq_comp] using
      congrArg (fun T : TowerHilbert P →L[ℂ] TowerHilbert P => T v) (hcomm i)
  have hl := (Y.continuous.tendsto (B v)).comp (hlim v)
  change Tendsto (fun i => Y (A i v)) l (𝓝 (Y (B v))) at hl
  rw [he] at hl
  exact tendsto_nhds_unique hl (hlim (Y v))

/-- The bicommutant defining M is strongly closed for arbitrary nets. -/
theorem factor_mem_of_net_strong_limit (P : SiteProfile)
    {ι : Type*} (l : Filter ι) [l.NeBot]
    (A : ι → TowerHilbert P →L[ℂ] TowerHilbert P)
    (B : TowerHilbert P →L[ℂ] TowerHilbert P)
    (hmem : ∀ i, A i ∈ theFactorObject P)
    (hlim : ∀ v, Tendsto (fun i => A i v) l (𝓝 (B v))) :
    B ∈ theFactorObject P := by
  change B ∈ StarSubalgebra.centralizer ℂ
    ((StarSubalgebra.centralizer ℂ (towerImage P) :
      StarSubalgebra ℂ (TowerHilbert P →L[ℂ] TowerHilbert P)) : Set _)
  rw [StarSubalgebra.mem_centralizer_iff]
  intro Y hY
  have hc (i : ι) : Y * A i = A i * Y ∧ star Y * A i = A i * star Y := by
    have hi := hmem i
    change A i ∈ StarSubalgebra.centralizer ℂ
      ((StarSubalgebra.centralizer ℂ (towerImage P) :
        StarSubalgebra ℂ (TowerHilbert P →L[ℂ] TowerHilbert P)) : Set _) at hi
    rw [StarSubalgebra.mem_centralizer_iff] at hi
    exact hi Y hY
  exact ⟨strong_net_limit_commutes P l A B Y hlim (fun i => (hc i).1),
    strong_net_limit_commutes P l A B (star Y) hlim (fun i => (hc i).2)⟩

/-- Linearity and positivity imply monotonicity on the actual factor domain. -/
theorem expectation_order_preserving (P : SiteProfile) (I : ExpectationInput P)
    (A B : TowerHilbert P →L[ℂ] TowerHilbert P)
    (hA : A ∈ theFactorObject P) (hB : B ∈ theFactorObject P) (hAB : A ≤ B) :
    I.E A ≤ I.E B := by
  have h := general_expectation_nonnegative P I (B - A)
    ((theFactorObject P).sub_mem hB hA) (sub_nonneg.mpr hAB)
  rw [expectation_sub P I B A hB hA] at h
  exact sub_nonneg.mp h

/-- The supremum is constructed in M, and E preserves it for every bounded positive directed net. -/
theorem factor_monotone_supremum_and_expectation (P : SiteProfile) (I : ExpectationInput P)
    {ι : Type*} [Preorder ι] [IsDirectedOrder ι] [Nonempty ι]
    (A : ι → TowerHilbert P →L[ℂ] TowerHilbert P)
    (hmem : ∀ i, A i ∈ theFactorObject P)
    (hpos : ∀ i, 0 ≤ A i) (hmono : Monotone A)
    (C : ℝ) (hC : 0 ≤ C) (hbound : ∀ i, ‖A i‖ ≤ C) :
    ∃ B : TowerHilbert P →L[ℂ] TowerHilbert P,
      B ∈ theFactorObject P ∧ 0 ≤ B ∧ ‖B‖ ≤ C ∧
      IsLUB (Set.range A) B ∧
      IsLUB (Set.range (fun i => I.E (A i))) (I.E B) ∧
      (∀ v, Tendsto (fun i => A i v) atTop (𝓝 (B v))) ∧
      (∀ v, Tendsto (fun i => I.E (A i) v) atTop (𝓝 (I.E B v))) := by
  obtain ⟨B, hBpos, hBbound, hlim, hsup⟩ :=
    monotone_operator_limit A hpos hmono C hC hbound
  have hBmem := factor_mem_of_net_strong_limit P atTop A B hmem hlim
  have hElim := expectation_strong_tendsto_of_omega P I atTop A B
    hmem hBmem C hC hbound (hlim (hOmega P))
  have hEmono : Monotone (fun i => I.E (A i)) := by
    intro i j hij
    exact expectation_order_preserving P I (A i) (A j) (hmem i) (hmem j) (hmono hij)
  exact ⟨B, hBmem, hBpos, hBbound, hsup,
    monotone_strong_limit_isLUB (fun i => I.E (A i)) hEmono (I.E B) hElim,
    hlim, hElim⟩

/-- An order bound suffices: positivity converts it into a uniform norm bound. -/
theorem expectation_preserves_order_bounded_nets (P : SiteProfile) (I : ExpectationInput P)
    {ι : Type*} [Preorder ι] [IsDirectedOrder ι] [Nonempty ι]
    (A : ι → TowerHilbert P →L[ℂ] TowerHilbert P)
    (hmem : ∀ i, A i ∈ theFactorObject P)
    (hpos : ∀ i, 0 ≤ A i) (hmono : Monotone A)
    (D : TowerHilbert P →L[ℂ] TowerHilbert P) (hbound : ∀ i, A i ≤ D) :
    ∃ B : TowerHilbert P →L[ℂ] TowerHilbert P,
      B ∈ theFactorObject P ∧ IsLUB (Set.range A) B ∧
      IsLUB (Set.range (fun i => I.E (A i))) (I.E B) := by
  have hn (i : ι) : ‖A i‖ ≤ ‖D‖ :=
    CStarAlgebra.norm_le_norm_of_nonneg_of_le (hpos i) (hbound i)
  obtain ⟨B, hBmem, _, _, hsup, hEsup, _, _⟩ :=
    factor_monotone_supremum_and_expectation P I A hmem hpos hmono ‖D‖ (norm_nonneg D) hn
  exact ⟨B, hBmem, hsup, hEsup⟩

/-- Normality in the order sense: every positive increasing directed supremum is preserved. -/
theorem general_expectation_normal_order (P : SiteProfile) (I : ExpectationInput P)
    {ι : Type*} [Preorder ι] [IsDirectedOrder ι] [Nonempty ι]
    (A : ι → TowerHilbert P →L[ℂ] TowerHilbert P)
    (hmem : ∀ i, A i ∈ theFactorObject P)
    (hpos : ∀ i, 0 ≤ A i) (hmono : Monotone A)
    (B : TowerHilbert P →L[ℂ] TowerHilbert P) (hB : IsLUB (Set.range A) B) :
    B ∈ theFactorObject P ∧ IsLUB (Set.range (fun i => I.E (A i))) (I.E B) := by
  obtain ⟨D, hDmem, hDsup, hEDsup⟩ :=
    expectation_preserves_order_bounded_nets P I A hmem hpos hmono B
      (fun i => hB.1 (Set.mem_range_self i))
  have he : D = B := hDsup.unique hB
  subst D
  exact ⟨hDmem, hEDsup⟩

/-- The aperiodic expectation constructed in046 is normal in this full directed-order sense. -/
theorem aperiodic_expectation_normal_order (P : SiteProfile)
    {ι : Type*} [Preorder ι] [IsDirectedOrder ι] [Nonempty ι]
    (A : ι → TowerHilbert P →L[ℂ] TowerHilbert P)
    (hmem : ∀ i, A i ∈ theFactorObject P)
    (hpos : ∀ i, 0 ≤ A i) (hmono : Monotone A)
    (B : TowerHilbert P →L[ℂ] TowerHilbert P) (hB : IsLUB (Set.range A) B) :
    B ∈ theFactorObject P ∧
      IsLUB (Set.range (fun i => aperiodicExpectation P (A i))) (aperiodicExpectation P B) := by
  exact general_expectation_normal_order P (aperiodicExpectationInput P) A hmem hpos hmono B hB

#print axioms strong_net_limit_commutes
#print axioms factor_mem_of_net_strong_limit
#print axioms expectation_order_preserving
#print axioms factor_monotone_supremum_and_expectation
#print axioms expectation_preserves_order_bounded_nets
#print axioms general_expectation_normal_order
#print axioms aperiodic_expectation_normal_order

end

end ChatgptAudit.Expectation047
