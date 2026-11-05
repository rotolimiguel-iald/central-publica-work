import TGLExt.F1Fecho394.ClosedGraphRegularizationR3
import Mathlib.MeasureTheory.Integral.DominatedConvergence

/-! Strong approximation to the identity by actual group averages.
The same real kernel can be used on a real closed Tomita graph. -/
set_option autoImplicit false
set_option maxHeartbeats 1200000
noncomputable section
open MeasureTheory Filter
open scoped Topology
namespace F1Fecho.GroupAverageApproximation
variable {H:Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

theorem averages_tendsto_identity (U:ℝ→H≃ₗᵢ[ℂ]H)
    (hc:∀x,Continuous (fun t=>U t x)) (h0:∀x,U 0 x=x)
    (w:ℝ→ℝ) (hw:Integrable w volume) (hw1:∫t:ℝ,w t=1)
    (e:ℕ→ℝ) (he:Tendsto e atTop (𝓝 0)) (x:H) :
    Tendsto (fun n=>∫t:ℝ,w t • U (e n*t) x) atTop (𝓝 x) := by
  have hm:∀n,AEStronglyMeasurable (fun t:ℝ=>w t • U (e n*t) x) volume := by
    intro n
    exact hw.aestronglyMeasurable.smul ((hc x).comp (continuous_const.mul continuous_id)).aestronglyMeasurable
  have hb:∀n,∀ᵐ t:ℝ ∂volume,‖w t • U (e n*t) x‖≤‖w t‖*‖x‖ := by
    intro n
    apply ae_of_all
    intro t
    rw [norm_smul,(U _).norm_map]
  have hl:∀ᵐ t:ℝ ∂volume,Tendsto (fun n=>w t • U (e n*t) x) atTop (𝓝 (w t • x)) := by
    apply ae_of_all
    intro t
    have ht:Tendsto (fun n=>e n*t) atTop (𝓝 (0:ℝ)) := by simpa using he.mul_const t
    have hu:=((hc x).continuousAt.tendsto.comp ht).const_smul (w t)
    simpa only [h0,Function.comp_apply] using hu
  have h:=tendsto_integral_of_dominated_convergence (fun t:ℝ=>‖w t‖*‖x‖)
    hm (hw.norm.mul_const ‖x‖) hb hl
  simpa only [integral_smul_const,hw1,one_smul] using h

theorem scaled_average_preserves_graph (G:Submodule ℝ (WithLp 2 (H×H)))
    (hG:IsClosed (G:Set (WithLp 2 (H×H))))
    (U:ℝ→H≃ₗᵢ[ℂ]H) (hc:∀x,Continuous (fun t=>U t x))
    (hU:∀t x y,WithLp.toLp 2 (x,y)∈G→WithLp.toLp 2 (U t x,U t y)∈G)
    (w:ℝ→ℝ) (hw:Integrable w volume) (c:ℝ) (x y:H)
    (hxy:WithLp.toLp 2 (x,y)∈G) :
    WithLp.toLp 2 ((∫t,w t • U (c*t) x),(∫t,w t • U (c*t) y))∈G := by
  exact ClosedGraphRegularization.average_preserves_graph G hG (fun t=>U (c*t))
    (fun x=>(hc x).comp (continuous_const.mul continuous_id))
    (fun t=>hU (c*t)) w hw x y hxy

end F1Fecho.GroupAverageApproximation
#print axioms F1Fecho.GroupAverageApproximation.averages_tendsto_identity
#print axioms F1Fecho.GroupAverageApproximation.scaled_average_preserves_graph
