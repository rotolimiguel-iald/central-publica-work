import TGLExt.V350RealGraphCore
import TGLExt.V350PartialOperatorSquare

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

namespace TGLV350.Regular
open Filter
open scoped Topology
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
local instance squareGraphRealHilbert : InnerProductSpace ℝ H := InnerProductSpace.complexToReal
variable (B A : H →ₗ.[ℂ] H) (he : partialOperatorSquare B = A)
include he

theorem partialSquare_domain_le : A.domain ≤ B.domain := by
  intro x hx
  have hx' : x ∈ (partialOperatorSquare B).domain := by rw [he]; exact hx
  exact ((partialOperatorSquare_domain_iff B x).mp hx').choose

/-- The square pairing holds against the whole domain of B. -/
theorem partialSquare_pairing_all (hs : B.IsFormalAdjoint B)
    (u : A.domain) (x : B.domain) :
    inner ℂ (x : H) (A u) = inner ℂ (B x)
      (B (Submodule.inclusion (partialSquare_domain_le B A he) u)) := by
  have hg : ((u : H),A u) ∈ (partialOperatorSquare B).graph := by
    rw [he]
    exact LinearPMap.mem_graph A u
  obtain ⟨y,hy1,hy2⟩ := (partialOperatorSquare_graph_iff B (u : H) (A u)).mp hg
  obtain ⟨v,hv,hBv⟩ := (LinearPMap.mem_graph_iff B).mp hy1
  obtain ⟨w,hw,hBw⟩ := (LinearPMap.mem_graph_iff B).mp hy2
  dsimp only [Prod.fst,Prod.snd] at hv hBv hw hBw
  have hi : Submodule.inclusion (partialSquare_domain_le B A he) u = v :=
    Subtype.ext hv.symm
  have hvalue : B (Submodule.inclusion (partialSquare_domain_le B A he) u) = y :=
    (congrArg B hi).trans hBv
  calc
    _ = inner ℂ (x : H) (B w) := congrArg (fun z : H => inner ℂ (x : H) z) hBw.symm
    _ = inner ℂ (B x) (w : H) := (hs x w).symm
    _ = _ := congrArg (fun z : H => inner ℂ (B x) z) (hw.trans hvalue.symm)

/-- A resolvent for B² gives graph-core density of D(B²) in D(B). -/
theorem partialSquare_graph_core (hs : B.IsFormalAdjoint B)
    (hc : IsClosed (Set.range (fun x : B.domain => ((x : H),B x))))
    (hr : ∀ z : H, ∃ u : A.domain, (u : H)+A u=z) :
    DenseRange (realGraphInclusion B.domain (B.toFun.restrictScalars ℝ)
      A.domain (partialSquare_domain_le B A he)) := by
  apply realGraphInclusion_dense B.domain (B.toFun.restrictScalars ℝ)
    A.domain (partialSquare_domain_le B A he) hc
  intro z
  obtain ⟨u,hu⟩ := hr z
  refine ⟨u,?_⟩
  intro x
  change (inner ℂ (x : H) (u : H)).re +
    (inner ℂ (B x) (B (Submodule.inclusion (partialSquare_domain_le B A he) u))).re =
      (inner ℂ (x : H) z).re
  have hp := congrArg Complex.re (partialSquare_pairing_all B A he hs u x)
  calc
    _ = (inner ℂ (x : H) (u : H)).re + (inner ℂ (x : H) (A u)).re :=
      congrArg (fun a : ℝ => (inner ℂ (x : H) (u : H)).re+a) hp.symm
    _ = (inner ℂ (x : H) ((u : H)+A u)).re :=
      (congrArg Complex.re (inner_add_right (x : H) (u : H) (A u))).symm
    _ = _ := congrArg (fun v : H => (inner ℂ (x : H) v).re) hu

#print axioms partialSquare_domain_le
#print axioms partialSquare_pairing_all
#print axioms partialSquare_graph_core
end
end TGLV350.Regular
