import TGLExt.Fundacao
import TGLExt.GeneralMetricClausius
import TGLExt.GravitationalChartGluing
import TGLExt.TopologicalAtlasGluing
import TGLExt.SmoothSelectedAtlasGluing
import TGLExt.HorizonEinsteinReconstruction

/-!
F2.3 — conditional wiring of the finite passage to the curved field law.

The named H3 below is precisely the all-points, all-null-directions area/Clausius
condition required by AreaChart. It is NOT derived from the finite passage.
The arrow from the passage identity to H3 is an explicit input across different
types. Chart records, conservation, topology and smooth transitions are also
explicit inputs. The theorem asserts an implication, not a global solution.
-/

set_option autoImplicit false
set_option maxHeartbeats 1200000

namespace ChatgptAudit.F23CurvedFieldLigand

open Matrix Filter Topology Set TGLExt ChatgptAudit
open ChatgptAudit.GeneralMetric ChatgptAudit.GeneralClausius
open ChatgptAudit.GravitationalRecord ChatgptAudit.ChartGluing
open ChatgptAudit.TopologicalGluing ChatgptAudit.SmoothAtlasGluing
open ChatgptAudit.UnifiedRecorded ChatgptAudit.Micro021

noncomputable section

/-- H3 named at every point and nonzero null direction of every chart. -/
def NamedAtlasH3 {ι : Type} (eta : ℝ) (U : ι → Set Coordinate4)
    (R : ∀ i, GravitationalResponseRecord (U i))
    (screens : ∀ i, MetricScreenFamily (U i) (recordMetric (R i))) : Prop :=
  ∀ i x (hx : x ∈ U i) d (hv : d ≠ 0)
    (hn : tensorQuad (recordMetric (R i) x) d = 0),
    Tendsto (fun t => microscopicAreaError (unifiedPreparation (R i) x d) eta
      (inducedArea (recordMetric (R i))
        (screens i x hx d hv hn).curve
        (screens i x hx d hv hn).screen.vectors) t / t^2)
      (𝓝[<] (0 : ℝ)) (𝓝 0)

/-- Conditional binder: the finite passage feeds the *named* H3 screen law;
    v338 then gives one Einstein coefficient across a smooth selected atlas.
    No physical construction of that bridge or of a global solution is claimed. -/
theorem passage_h3_to_connected_smooth_atlas_einstein
    {n X ι : Type} [Fintype n] [DecidableEq n]
    [TopologicalSpace X] [PreconnectedSpace X]
    {d : n → ℝ} (hd : ∀ i, 0 < d i) (hinj : Function.Injective d)
    {W : Matrix n n ℂ} (hW : Wᴴ * W = 1)
    (hω : ∀ y, (rhoD d * adU W y).trace = (rhoD d * y).trace)
    (G : ℝ) (hG : 0 < G)
    (U : ι → Set Coordinate4) (hopenU : ∀ i, IsOpen (U i))
    (hconnU : ∀ i, IsPreconnected (U i))
    (R : ∀ i, GravitationalResponseRecord (U i))
    (screens : ∀ i, MetricScreenFamily (U i) (recordMetric (R i)))
    (conserved : ∀ i, ∀ x ∈ U i, ∀ j,
      tensorFieldDivergence (metricInverse (recordMetric (R i)))
        (leviCivitaField (recordMetric (R i))
          (metricInverse (recordMetric (R i))))
        (recordSource (R i)) x j = 0)
    (hH3 : (∀ x, adU W (diagExpect x) = diagExpect (adU W x)) →
      NamedAtlasH3 ((4 * G)⁻¹) U R screens)
    (anchor : ι) (S : ι → Set X) (hopenS : ∀ i, IsOpen (S i))
    (hcover : ∀ x, ∃ i, x ∈ S i) (hne : ∀ i, (S i).Nonempty)
    (chart : ∀ i, S i ≃ₜ U i)
    (htransitions : ∀ i j p (_hi : p ∈ S i) (hj : p ∈ S j),
      ∃ D : SmoothRecordTransition U R S chart i j,
        (chart j ⟨p, hj⟩).val ∈ D.source) :
    ∃! a : ℝ, ∀ i x, x ∈ U i →
      recordEinstein (R i) x + a • recordMetric (R i) x =
        (8 * Real.pi * G) • recordSource (R i) x := by
  have hpost : ∀ x, adU W (diagExpect x) = diagExpect (adU W x) :=
    TGLExt.Fundacao.the_post_lives_in_the_passage hd hinj hW hω
  have harea := hH3 hpost
  have hG0 : G ≠ 0 := ne_of_gt hG
  have heta : (4 * G)⁻¹ ≠ 0 := inv_ne_zero (mul_ne_zero (by norm_num) hG0)
  let C : ι → AreaChart ((4 * G)⁻¹) := fun i => {
    domain := U i
    open_domain := hopenU i
    connected_domain := hconnU i
    record := R i
    screens := screens i
    conserved := conserved i
    area := by
      intro x hx v hv hn
      exact harea i x hx v hv hn
  }
  have htransC : ∀ i j p (_hi : p ∈ S i) (hj : p ∈ S j),
      ∃ D : SmoothRecordTransition (fun i => (C i).domain)
        (fun i => (C i).record) S chart i j,
        (chart j ⟨p, hj⟩).val ∈ D.source := by
    intro i j p hi hj
    simpa only [C] using htransitions i j p hi hj
  have hfield := connected_smooth_atlas_einstein ((4 * G)⁻¹) heta C anchor
    S hopenS hcover hne chart htransC
  simpa only [C, ChatgptAudit.entropy_density_einstein_coefficient G hG0] using hfield

#print axioms NamedAtlasH3
#print axioms passage_h3_to_connected_smooth_atlas_einstein

end
end ChatgptAudit.F23CurvedFieldLigand
