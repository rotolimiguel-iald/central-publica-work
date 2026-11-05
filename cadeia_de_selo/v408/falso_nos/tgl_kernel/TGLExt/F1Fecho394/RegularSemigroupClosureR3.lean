import TGLExt.F1Fecho394.RegularCoefficientBoundaryR3
import TGLExt.F1Fecho394.PositiveCoefficientBothR4
import Mathlib.Analysis.InnerProductSpace.Projection.Submodule

/-! A positive-energy one-parameter semigroup on a generating set determines
its entire group on the closed complex span. Only the generators require a
finite energy moment; continuity then supplies every vector in the closure. -/
set_option autoImplicit false
set_option maxHeartbeats 1400000
noncomputable section
open MeasureTheory
open scoped InnerProductSpace
namespace F1Fecho.RegularCoefficient
open TGLExt.ImportedSQ TGLExt.ContratoQGv31 F1Fecho.MaxwellGlobal
open ChatgptAudit.WignerOrbit016 ChatgptAudit.WignerRapidityMeasure016

theorem negative_ray_implies_all_times (a : Fin 4→ℝ)
    (ha : a∈forwardCone)
    (hb : ∀y,orbitPairing a (shellMomentum 0 y)≤2*shellEnergy y)
    (ξ ψ : H1) (hψ : EnergySquareProfile ψ)
    (hz : ∀t:ℝ,t<0→inner ℂ ξ (U1 (t • a) ψ)=0) :
    ∀t:ℝ,inner ℂ ξ (U1 (t • a) ψ)=0 := by
  have hv:=PositiveCoefficientBoundary.vanishes_from_negative_ray (orbitalMeasure 0)
    _ (orbitalEnergy_measurable 0 a) (OrbitalContraction.energy_nonneg a ha)
    _ (L2.integrable_inner (𝕜:=ℂ) ξ ψ)
    (coefficient_first_moment _ (orbitalEnergy_measurable 0 a)
      (OrbitalContraction.energy_nonneg a ha) hb ξ ψ hψ)
    (fun t ht=>by rw [coefficient_eq_inner_V a ha ξ ψ t (by simp),OrbitalContraction.V_boundary]; exact hz t ht)
  intro t
  have ht:=hv t
  rwa [coefficient_eq_inner_V a ha ξ ψ t (by simp),OrbitalContraction.V_boundary] at ht

def complexClosure (G:Set H1) : Submodule ℂ H1 := (Submodule.span ℂ G).topologicalClosure

theorem group_mem_of_semiray (G:Set H1) (a:Fin 4→ℝ) (ha:a∈forwardCone)
    (hb:∀y,orbitPairing a (shellMomentum 0 y)≤2*shellEnergy y)
    (hregular:∀ψ∈G,EnergySquareProfile ψ) (side:Bool)
    (hsemi:∀ψ∈G,∀t:ℝ,(if side then 0<t else t<0)→U1 (t • a) ψ∈complexClosure G)
    (t:ℝ) (v:H1) (hv:v∈complexClosure G) : U1 (t • a) v∈complexClosure G := by
  have hgen : ∀ψ∈G,U1 (t • a) ψ∈complexClosure G := by
    intro ψ hψ
    have hd : U1 (t • a) ψ∈(complexClosure G)ᗮᗮ := by
      apply (Submodule.mem_orthogonal _ _).mpr
      intro ξ hξ
      have hzero : ∀s:ℝ,(if side then 0<s else s<0)→inner ℂ ξ (U1 (s • a) ψ)=0 := by
        intro s hs
        exact Submodule.inner_left_of_mem_orthogonal (hsemi ψ hψ s hs) hξ
      cases side
      · exact negative_ray_implies_all_times a ha hb ξ ψ (hregular ψ hψ) hzero t
      · exact positive_ray_implies_all_times a ha hb ξ ψ (hregular ψ hψ) hzero t
    rw [Submodule.orthogonal_orthogonal_eq_closure] at hd
    simpa only [complexClosure,(Submodule.isClosed_topologicalClosure (Submodule.span ℂ G)).submodule_topologicalClosure_eq] using hd
  let T:H1→L[ℂ]H1:=(U1 (t • a)).toLinearIsometry.toContinuousLinearMap
  have hs:(Submodule.span ℂ G).map T.toLinearMap≤complexClosure G := by
    rw [Submodule.map_span]
    apply Submodule.span_le.mpr
    rintro w ⟨ψ,hψ,rfl⟩
    exact hgen ψ hψ
  have hc:U1 (t • a) v∈(complexClosure G).topologicalClosure :=
    (Submodule.topologicalClosure_mono hs)
      ((Submodule.topologicalClosure_map T _) (Submodule.mem_map.mpr ⟨v,hv,rfl⟩))
  simpa only [complexClosure,(Submodule.isClosed_topologicalClosure (Submodule.span ℂ G)).submodule_topologicalClosure_eq] using hc

end F1Fecho.RegularCoefficient
#print axioms F1Fecho.RegularCoefficient.negative_ray_implies_all_times
#print axioms F1Fecho.RegularCoefficient.group_mem_of_semiray
