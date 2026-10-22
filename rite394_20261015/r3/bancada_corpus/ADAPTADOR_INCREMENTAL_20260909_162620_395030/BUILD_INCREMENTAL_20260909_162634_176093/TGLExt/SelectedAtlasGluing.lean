import TGLExt.TopologicalAtlasGluing
import TGLExt.SelectedGravitationalAtlas

set_option autoImplicit false
set_option maxHeartbeats 600000
namespace ChatgptAudit.SelectedAtlasGluing
open Set TGLExt ChatgptAudit.ChartGluing ChatgptAudit.TopologicalGluing
  ChatgptAudit.SelectedAtlas ChatgptAudit.GravitationalRecord
  ChatgptAudit.JointCovariance
noncomputable section

def decodedFromCharacter {U : Set Coordinate4} [Nonempty U] (t : ℝ)
    (R : GravitationalResponseRecord U) : GravitationalResponseRecord U :=
  reconstructedRecord (⟨classCharacter t (classOfRecord R),
    ⟨classOfRecord R, rfl⟩⟩ : CharacterImage U t)

theorem selected_equation_iff {U : Set Coordinate4} [Nonempty U]
    (hU : IsOpen U) (t : ℝ) (ht : t ≠ 0) (R : GravitationalResponseRecord U)
    (a k : ℝ) (x : Coordinate4) (hx : x ∈ U) :
    (recordEinstein (decodedFromCharacter t R) x +
      a • recordMetric (decodedFromCharacter t R) x =
      k • recordSource (decodedFromCharacter t R) x) ↔
    (recordEinstein R x + a • recordMetric R x = k • recordSource R x) := by
  have hf := character_reconstructs_metric_and_source t ht R
  change EqOn (recordMetric (decodedFromCharacter t R)) (recordMetric R) U ∧
    EqOn (recordSource (decodedFromCharacter t R)) (recordSource R) U at hf
  have he := geometric_einstein_congr_on hU _ _ hf.1
  change EqOn (recordEinstein (decodedFromCharacter t R)) (recordEinstein R) U at he
  rw [he hx, hf.1 hx, hf.2 hx]

/-- The exact character of each chart reconstructs the same global equations.
The area/conservation laws are required only on the original records. -/
theorem selected_connected_atlas_einstein {X ι : Type}
    [TopologicalSpace X] [PreconnectedSpace X]
    (eta : ℝ) (heta : eta ≠ 0) (C : ι → AreaChart eta)
    [∀ i, Nonempty (C i).domain]
    (t : ℝ) (ht : t ≠ 0) (anchor : ι)
    (S : ι → Set X) (hopen : ∀ i, IsOpen (S i))
    (hcover : ∀ x, ∃ i, x ∈ S i) (hne : ∀ i, (S i).Nonempty)
    (chart : ∀ i, S i ≃ₜ (C i).domain)
    (hmatch : ∀ i j p (hi : p ∈ S i) (hj : p ∈ S j), ∃ F : Tensor4,
      F.det ≠ 0 ∧
      recordMetric (C j).record (chart j ⟨p, hj⟩) =
        frameMetric F (recordMetric (C i).record (chart i ⟨p, hi⟩)) ∧
      recordSource (C j).record (chart j ⟨p, hj⟩) =
        frameMetric F (recordSource (C i).record (chart i ⟨p, hi⟩)) ∧
      recordEinstein (C j).record (chart j ⟨p, hj⟩) =
        frameMetric F (recordEinstein (C i).record (chart i ⟨p, hi⟩))) :
    ∃! a : ℝ, ∀ i x, x ∈ (C i).domain →
      recordEinstein (decodedFromCharacter t (C i).record) x +
        a • recordMetric (decodedFromCharacter t (C i).record) x =
        (2*Real.pi/eta) • recordSource (decodedFromCharacter t (C i).record) x := by
  obtain ⟨a, ha, hu⟩ := connected_chart_cover_einstein eta heta C anchor
    S hopen hcover hne chart hmatch
  have he (b : ℝ) :
      (∀ i x, x ∈ (C i).domain →
        recordEinstein (decodedFromCharacter t (C i).record) x +
          b • recordMetric (decodedFromCharacter t (C i).record) x =
          (2*Real.pi/eta) • recordSource (decodedFromCharacter t (C i).record) x) ↔
      (∀ i x, x ∈ (C i).domain →
        recordEinstein (C i).record x + b • recordMetric (C i).record x =
          (2*Real.pi/eta) • recordSource (C i).record x) := by
    constructor <;> intro hb i x hx
    · exact (selected_equation_iff (C i).open_domain t ht (C i).record
        b (2*Real.pi/eta) x hx).mp (hb i x hx)
    · exact (selected_equation_iff (C i).open_domain t ht (C i).record
        b (2*Real.pi/eta) x hx).mpr (hb i x hx)
  exact ⟨a, (he a).mpr ha, fun b hb => hu b ((he b).mp hb)⟩

#print axioms decodedFromCharacter
#print axioms selected_equation_iff
#print axioms selected_connected_atlas_einstein
end
end ChatgptAudit.SelectedAtlasGluing
