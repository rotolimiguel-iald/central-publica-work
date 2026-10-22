import TGLExt.FiniteEinsteinNaturality
import TGLExt.SelectedAtlasGluing

set_option autoImplicit false
set_option maxHeartbeats 1000000
namespace ChatgptAudit.SmoothAtlasGluing
open Matrix Set TGLExt ChatgptAudit.FiniteCoordinates
  ChatgptAudit.FiniteEinsteinNaturality ChatgptAudit.GeneralMetric
  ChatgptAudit.GravitationalRecord ChatgptAudit.ChartGluing
  ChatgptAudit.TopologicalGluing ChatgptAudit.SelectedAtlasGluing
  ChatgptAudit.SelectedAtlas ChatgptAudit.JointCovariance
noncomputable section

/-- A transition from chart j to chart i on actual open subdomains.
All points, not only the distinguished overlap point, agree in the underlying space.
The Einstein transformation is deliberately not a field of this structure. -/
structure SmoothRecordTransition {X ι : Type} [TopologicalSpace X]
    (U : ι → Set Coordinate4) (R : ∀ i, GravitationalResponseRecord (U i))
    (S : ι → Set X) (chart : ∀ i, S i ≃ₜ U i) (i j : ι) where
  source : Set Coordinate4
  target : Set Coordinate4
  change : SmoothCoordinateChange source target
  source_subset : source ⊆ U j
  target_subset : target ⊆ U i
  same_point : ∀ x (hx : x ∈ source),
    ((chart i).symm ⟨change.forward x, target_subset (change.forward_maps hx)⟩).val =
      ((chart j).symm ⟨x, source_subset hx⟩).val
  metric : EqOn (recordMetric (R j)) (pullbackMetric change (recordMetric (R i))) source
  matter : EqOn (recordSource (R j)) (pullbackMetric change (recordSource (R i))) source

theorem transition_same_coordinates {X ι : Type} [TopologicalSpace X]
    (U : ι → Set Coordinate4) (R : ∀ i, GravitationalResponseRecord (U i))
    (S : ι → Set X) (chart : ∀ i, S i ≃ₜ U i) (i j : ι)
    (D : SmoothRecordTransition U R S chart i j)
    (p : X) (hi : p ∈ S i) (hj : p ∈ S j)
    (hp : (chart j ⟨p,hj⟩).val ∈ D.source) :
    D.change.forward (chart j ⟨p,hj⟩) = (chart i ⟨p,hi⟩).val := by
  have he : (chart i).symm
      ⟨D.change.forward (chart j ⟨p,hj⟩), D.target_subset (D.change.forward_maps hp)⟩ =
        (⟨p,hi⟩ : S i) := by
    apply Subtype.ext
    have h := D.same_point (chart j ⟨p,hj⟩) hp
    simpa using h
  have h := congrArg (fun z : S i => (chart i z).val) he
  simpa using h

theorem transition_einstein {X ι : Type} [TopologicalSpace X]
    (U : ι → Set Coordinate4) (R : ∀ i, GravitationalResponseRecord (U i))
    (S : ι → Set X) (chart : ∀ i, S i ≃ₜ U i) (i j : ι)
    (D : SmoothRecordTransition U R S chart i j)
    (x : Coordinate4) (hx : x ∈ D.source) :
    recordEinstein (R j) x = frameMetric (changeJacobian D.change x)
      (recordEinstein (R i) (D.change.forward x)) := by
  have hg : SmoothMatrixOn D.target (recordMetric (R i)) :=
    fun a b => (record_metric_smooth (R i) a b).mono D.target_subset
  have hl : ∀ y ∈ D.target, LorentzByCongruence (recordMetric (R i) y) :=
    fun y hy => record_metric_lorentz (R i) y (D.target_subset hy)
  exact einstein_finite_overlap_transformation D.change (recordMetric (R i))
    (recordMetric (R j)) hg hl D.metric x hx

theorem transition_supplies_tensor_match {X ι : Type} [TopologicalSpace X]
    (U : ι → Set Coordinate4) (R : ∀ i, GravitationalResponseRecord (U i))
    (S : ι → Set X) (chart : ∀ i, S i ≃ₜ U i) (i j : ι)
    (D : SmoothRecordTransition U R S chart i j)
    (p : X) (hi : p ∈ S i) (hj : p ∈ S j)
    (hp : (chart j ⟨p,hj⟩).val ∈ D.source) :
    ∃ F : Tensor4, F.det ≠ 0 ∧
      recordMetric (R j) (chart j ⟨p,hj⟩) =
        frameMetric F (recordMetric (R i) (chart i ⟨p,hi⟩)) ∧
      recordSource (R j) (chart j ⟨p,hj⟩) =
        frameMetric F (recordSource (R i) (chart i ⟨p,hi⟩)) ∧
      recordEinstein (R j) (chart j ⟨p,hj⟩) =
        frameMetric F (recordEinstein (R i) (chart i ⟨p,hi⟩)) := by
  have hcoord := transition_same_coordinates U R S chart i j D p hi hj hp
  refine ⟨changeJacobian D.change (chart j ⟨p,hj⟩),
    change_jacobian_det_ne_zero D.change _ hp, ?_, ?_, ?_⟩
  · have h := D.metric hp
    change recordMetric (R j) (chart j ⟨p,hj⟩) =
      frameMetric (changeJacobian D.change (chart j ⟨p,hj⟩))
        (recordMetric (R i) (D.change.forward (chart j ⟨p,hj⟩))) at h
    rwa [hcoord] at h
  · have h := D.matter hp
    change recordSource (R j) (chart j ⟨p,hj⟩) =
      frameMetric (changeJacobian D.change (chart j ⟨p,hj⟩))
        (recordSource (R i) (D.change.forward (chart j ⟨p,hj⟩))) at h
    rwa [hcoord] at h
  · have h := transition_einstein U R S chart i j D _ hp
    rwa [hcoord] at h

/-- Decoding preserves the same geometric transition because the decoded fields
agree on each chart domain. No new physical laws are imposed on representatives. -/
def decodedTransition {X ι : Type} [TopologicalSpace X]
    (U : ι → Set Coordinate4) [∀ i, Nonempty (U i)]
    (R : ∀ i, GravitationalResponseRecord (U i))
    (S : ι → Set X) (chart : ∀ i, S i ≃ₜ U i) (i j : ι)
    (D : SmoothRecordTransition U R S chart i j) (t : ℝ) (ht : t ≠ 0) :
    SmoothRecordTransition U (fun i => decodedFromCharacter t (R i)) S chart i j where
  source := D.source
  target := D.target
  change := D.change
  source_subset := D.source_subset
  target_subset := D.target_subset
  same_point := D.same_point
  metric := by
    intro x hx
    have hi := character_reconstructs_metric_and_source t ht (R i)
    have hj := character_reconstructs_metric_and_source t ht (R j)
    change EqOn (recordMetric (decodedFromCharacter t (R i))) (recordMetric (R i)) (U i) ∧
      EqOn (recordSource (decodedFromCharacter t (R i))) (recordSource (R i)) (U i) at hi
    change EqOn (recordMetric (decodedFromCharacter t (R j))) (recordMetric (R j)) (U j) ∧
      EqOn (recordSource (decodedFromCharacter t (R j))) (recordSource (R j)) (U j) at hj
    change recordMetric (decodedFromCharacter t (R j)) x =
      (changeJacobian D.change x)ᵀ *
        recordMetric (decodedFromCharacter t (R i)) (D.change.forward x) *
          changeJacobian D.change x
    rw [hj.1 (D.source_subset hx),hi.1 (D.target_subset (D.change.forward_maps hx))]
    exact D.metric hx
  matter := by
    intro x hx
    have hi := character_reconstructs_metric_and_source t ht (R i)
    have hj := character_reconstructs_metric_and_source t ht (R j)
    change EqOn (recordMetric (decodedFromCharacter t (R i))) (recordMetric (R i)) (U i) ∧
      EqOn (recordSource (decodedFromCharacter t (R i))) (recordSource (R i)) (U i) at hi
    change EqOn (recordMetric (decodedFromCharacter t (R j))) (recordMetric (R j)) (U j) ∧
      EqOn (recordSource (decodedFromCharacter t (R j))) (recordSource (R j)) (U j) at hj
    change recordSource (decodedFromCharacter t (R j)) x =
      (changeJacobian D.change x)ᵀ *
        recordSource (decodedFromCharacter t (R i)) (D.change.forward x) *
          changeJacobian D.change x
    rw [hj.2 (D.source_subset hx),hi.2 (D.target_subset (D.change.forward_maps hx))]
    exact D.matter hx

theorem connected_smooth_atlas_einstein {X ι : Type}
    [TopologicalSpace X] [PreconnectedSpace X]
    (eta : ℝ) (heta : eta ≠ 0) (C : ι → AreaChart eta) (anchor : ι)
    (S : ι → Set X) (hopen : ∀ i, IsOpen (S i))
    (hcover : ∀ x, ∃ i, x ∈ S i) (hne : ∀ i, (S i).Nonempty)
    (chart : ∀ i, S i ≃ₜ (C i).domain)
    (htransitions : ∀ i j p (_hi : p ∈ S i) (hj : p ∈ S j),
      ∃ D : SmoothRecordTransition (fun i => (C i).domain)
        (fun i => (C i).record) S chart i j, (chart j ⟨p,hj⟩).val ∈ D.source) :
    ∃! a : ℝ, ∀ i x, x ∈ (C i).domain →
      recordEinstein (C i).record x + a • recordMetric (C i).record x =
        (2*Real.pi/eta) • recordSource (C i).record x := by
  apply connected_chart_cover_einstein eta heta C anchor S hopen hcover hne chart
  intro i j p hi hj
  obtain ⟨D,hD⟩ := htransitions i j p hi hj
  exact transition_supplies_tensor_match _ _ S chart i j D p hi hj hD

theorem selected_connected_smooth_atlas_einstein {X ι : Type}
    [TopologicalSpace X] [PreconnectedSpace X]
    (eta : ℝ) (heta : eta ≠ 0) (C : ι → AreaChart eta)
    [∀ i, Nonempty (C i).domain]
    (t : ℝ) (ht : t ≠ 0) (anchor : ι)
    (S : ι → Set X) (hopen : ∀ i, IsOpen (S i))
    (hcover : ∀ x, ∃ i, x ∈ S i) (hne : ∀ i, (S i).Nonempty)
    (chart : ∀ i, S i ≃ₜ (C i).domain)
    (htransitions : ∀ i j p (_hi : p ∈ S i) (hj : p ∈ S j),
      ∃ D : SmoothRecordTransition (fun i => (C i).domain)
        (fun i => (C i).record) S chart i j, (chart j ⟨p,hj⟩).val ∈ D.source) :
    ∃! a : ℝ, ∀ i x, x ∈ (C i).domain →
      recordEinstein (decodedFromCharacter t (C i).record) x +
        a • recordMetric (decodedFromCharacter t (C i).record) x =
          (2*Real.pi/eta) • recordSource (decodedFromCharacter t (C i).record) x := by
  apply selected_connected_atlas_einstein eta heta C t ht anchor S hopen hcover hne chart
  intro i j p hi hj
  obtain ⟨D,hD⟩ := htransitions i j p hi hj
  exact transition_supplies_tensor_match _ _ S chart i j D p hi hj hD

#print axioms SmoothRecordTransition
#print axioms transition_same_coordinates
#print axioms transition_einstein
#print axioms transition_supplies_tensor_match
#print axioms decodedTransition
#print axioms connected_smooth_atlas_einstein
#print axioms selected_connected_smooth_atlas_einstein
end
end ChatgptAudit.SmoothAtlasGluing
