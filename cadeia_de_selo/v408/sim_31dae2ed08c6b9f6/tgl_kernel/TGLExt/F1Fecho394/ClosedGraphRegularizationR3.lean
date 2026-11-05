import Mathlib.MeasureTheory.Measure.Lebesgue.Basic
import Mathlib.Analysis.InnerProductSpace.ProdL2
import Mathlib.Analysis.InnerProductSpace.Projection.Submodule
import Mathlib.MeasureTheory.Integral.Bochner.ContinuousLinearMap

/-! Closed real graphs are preserved by integrable real group averages.
A graph equality criterion requires actual regularizers with range in the
smaller domain and strong convergence, rather than mere involutivity. -/
set_option autoImplicit false
set_option maxHeartbeats 1200000
noncomputable section
open MeasureTheory Filter
open scoped Topology
namespace F1Fecho.ClosedGraphRegularization

variable {E:Type} [NormedAddCommGroup E] [InnerProductSpace ℝ E] [CompleteSpace E]

theorem integral_mem (G:Submodule ℝ E) (hG:IsClosed (G:Set E))
    (f:ℝ→E) (hf:Integrable f volume) (hm:∀ᵐ t:ℝ ∂volume,f t∈G) :
    (∫ t:ℝ,f t)∈G := by
  letI : CompleteSpace G:=hG.completeSpace_coe
  apply G.starProjection_eq_self_iff.mp
  rw [←G.starProjection.integral_comp_comm hf]
  apply integral_congr_ae
  filter_upwards [hm] with t ht
  exact G.starProjection_eq_self_iff.mpr ht

variable {H:Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
local instance : InnerProductSpace ℝ H := InnerProductSpace.complexToReal

theorem weighted_orbit_integrable (U:ℝ→H≃ₗᵢ[ℂ]H)
    (hc:∀x,Continuous (fun t=>U t x)) (w:ℝ→ℝ) (hw:Integrable w volume) (x:H) :
    Integrable (fun t=>w t • U t x) volume := by
  apply (hw.norm.mul_const ‖x‖).mono'
    (hw.aestronglyMeasurable.smul (hc x).aestronglyMeasurable)
  apply ae_of_all
  intro t
  rw [norm_smul,(U t).norm_map]

theorem average_preserves_graph (G:Submodule ℝ (WithLp 2 (H×H)))
    (hG:IsClosed (G:Set (WithLp 2 (H×H))))
    (U:ℝ→H≃ₗᵢ[ℂ]H) (hc:∀x,Continuous (fun t=>U t x))
    (hU:∀t x y,WithLp.toLp 2 (x,y)∈G→WithLp.toLp 2 (U t x,U t y)∈G)
    (w:ℝ→ℝ) (hw:Integrable w volume) (x y:H) (hxy:WithLp.toLp 2 (x,y)∈G) :
    WithLp.toLp 2 ((∫t,w t • U t x),(∫t,w t • U t y))∈G := by
  let L: (H×H)≃L[ℝ]WithLp 2 (H×H):=(WithLp.prodContinuousLinearEquiv 2 ℝ H H).symm
  have hx:=weighted_orbit_integrable U hc w hw x
  have hy:=weighted_orbit_integrable U hc w hw y
  have hi:Integrable (fun t=>L (w t • U t x,w t • U t y)) volume :=
    L.toContinuousLinearMap.integrable_comp (hx.prodMk hy)
  have hm:∀ᵐ t:ℝ ∂volume,L (w t • U t x,w t • U t y)∈G := by
    apply ae_of_all
    intro t
    exact G.smul_mem (w t) (hU t x y hxy)
  have he: (∫t:ℝ,L (w t • U t x,w t • U t y))=
      WithLp.toLp 2 ((∫t,w t • U t x),(∫t,w t • U t y)) := by
    rw [L.integral_comp_comm,integral_pair hx hy]
    rfl
  exact he ▸ integral_mem G hG _ hi hm

theorem graph_eq_of_regularizers (S T:Set (H×H)) (hS:IsClosed S)
    (hST:S⊆T)
    (hfun:∀x y z,(x,y)∈T→(x,z)∈T→y=z)
    (A:ℕ→H→H) (ha:∀x,Tendsto (fun n=>A n x) atTop (𝓝 x))
    (hcomm:∀n x y,(x,y)∈T→(A n x,A n y)∈T)
    (hrange:∀n x,∃y,(A n x,y)∈S) : S=T := by
  apply Set.Subset.antisymm hST
  rintro ⟨x,y⟩ hxy
  apply hS.mem_of_tendsto ((ha x).prodMk_nhds (ha y))
  apply Eventually.of_forall
  intro n
  obtain ⟨z,hz⟩:=hrange n x
  have he:=hfun (A n x) z (A n y) (hST hz) (hcomm n x y hxy)
  rwa [he] at hz

end F1Fecho.ClosedGraphRegularization
#print axioms F1Fecho.ClosedGraphRegularization.integral_mem
#print axioms F1Fecho.ClosedGraphRegularization.weighted_orbit_integrable
#print axioms F1Fecho.ClosedGraphRegularization.average_preserves_graph
#print axioms F1Fecho.ClosedGraphRegularization.graph_eq_of_regularizers
