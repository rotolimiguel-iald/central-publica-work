import TGLExt.V350RealGraphCore
import Mathlib.Topology.MetricSpace.Cauchy

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

namespace TGLV350.Regular
open Filter
open scoped Topology
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
variable (D E C : Submodule ℂ H) (S : D →ₗ[ℝ] H) (T : E →ₗ[ℝ] H)
variable (hCD : C ≤ D) (hCE : C ≤ E)

/-- Equal graph-coordinate norms on a core transfer domain membership to a closed map.
No boundedness of S or T and no equality of their values is assumed. -/
theorem graphCore_norm_extension
    (hd : DenseRange (realGraphInclusion D S C hCD))
    (hc : IsClosed (Set.range (fun x : E => ((x : H),T x))))
    (hn : ∀ u : C, ‖S (Submodule.inclusion hCD u)‖ = ‖T (Submodule.inclusion hCE u)‖) :
    ∀ x : D, ∃ y : E, (y : H)=(x : H) ∧ ‖S x‖=‖T y‖ := by
  intro x
  obtain ⟨u,hu,hSu⟩ := realGraphCore_sequence D S C hCD hd x
  have hcs := hSu.cauchySeq
  have hct : CauchySeq (fun n => T (Submodule.inclusion hCE (u n))) := by
    apply Metric.cauchySeq_iff.mpr
    intro ε hε
    obtain ⟨N,hN⟩ := Metric.cauchySeq_iff.mp hcs ε hε
    refine ⟨N,?_⟩
    intro m hm n hn'
    have he := hn (u m-u n)
    simp only [map_sub] at he
    rw [dist_eq_norm, ← he, ← dist_eq_norm]
    exact hN m hm n hn'
  obtain ⟨y,hy⟩ := cauchySeq_tendsto_of_complete hct
  have hpair : Tendsto (fun n => ((u n : H),T (Submodule.inclusion hCE (u n))))
      atTop (𝓝 ((x : H),y)) := hu.prodMk_nhds hy
  have hmem : ((x : H),y) ∈ Set.range (fun w : E => ((w : H),T w)) :=
    hc.mem_of_tendsto hpair (Filter.Eventually.of_forall (fun n =>
      ⟨Submodule.inclusion hCE (u n),rfl⟩))
  obtain ⟨w,hw⟩ := hmem
  refine ⟨w,congrArg Prod.fst hw,?_⟩
  have heq : (fun n => ‖S (Submodule.inclusion hCD (u n))‖) =
      (fun n => ‖T (Submodule.inclusion hCE (u n))‖) := funext (fun n => hn (u n))
  have ht : Tendsto (fun n => ‖S (Submodule.inclusion hCD (u n))‖) atTop (𝓝 ‖y‖) := by
    rw [heq]
    exact hy.norm
  exact (tendsto_nhds_unique hSu.norm ht).trans
    (congrArg norm (congrArg Prod.snd hw)).symm

theorem graphCore_norm_domain_transfer
    (hd : DenseRange (realGraphInclusion D S C hCD))
    (hc : IsClosed (Set.range (fun x : E => ((x : H),T x))))
    (hn : ∀ u : C, ‖S (Submodule.inclusion hCD u)‖ = ‖T (Submodule.inclusion hCE u)‖) :
    D ≤ E := by
  intro x hx
  obtain ⟨y,hy,_⟩ := graphCore_norm_extension D E C S T hCD hCE hd hc hn ⟨x,hx⟩
  change (y : H)=x at hy
  rw [← hy]
  exact y.property

#print axioms graphCore_norm_extension
#print axioms graphCore_norm_domain_transfer
end
end TGLV350.Regular
