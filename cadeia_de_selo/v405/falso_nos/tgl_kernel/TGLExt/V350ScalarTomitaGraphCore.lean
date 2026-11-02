import TGLExt.V350RealGraphCore
import TGLExt.V350ScalarTomitaSelfAdjoint

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

namespace TGLV350.Regular
open TGLExt Filter
open scoped Topology
noncomputable section
variable (P : SiteProfile)
local instance scalarGraphRealHilbert : InnerProductSpace ℝ (ScalarGNSHilbert P) :=
  InnerProductSpace.complexToReal

theorem scalarTomitaSquareDomain_le :
    (scalarTomitaSquare P).domain ≤ scalarClosedTomitaDomain P :=
  fun _ hx => hx.choose

/-- The already constructed resolvent supplies the weak identity on all of D(S). -/
theorem scalarTomitaSquare_weak_graph_identity (z : ScalarGNSHilbert P) :
    ∃ u : (scalarTomitaSquare P).domain, ∀ x : scalarClosedTomitaDomain P,
      inner ℝ (x : ScalarGNSHilbert P) (u : ScalarGNSHilbert P) +
        inner ℝ (scalarClosedTomita P x)
          (scalarClosedTomita P (Submodule.inclusion (scalarTomitaSquareDomain_le P) u)) =
            inner ℝ (x : ScalarGNSHilbert P) z := by
  obtain ⟨u,hu⟩ := scalarTomitaSquare_resolvent_surjective P z
  refine ⟨u,?_⟩
  intro x
  change (inner ℂ (x : ScalarGNSHilbert P) (u : ScalarGNSHilbert P)).re +
    (inner ℂ (scalarClosedTomita P x)
      (scalarClosedTomita P (scalarTomitaSquareInput P u))).re =
        (inner ℂ (x : ScalarGNSHilbert P) z).re
  have hp := (congrArg Complex.re (scalarTomitaSquare_pairing P u x)).symm.trans
    (inner_re_symm (𝕜 := ℂ) (scalarTomitaSquare P u) (x : ScalarGNSHilbert P))
  calc
    _ = (inner ℂ (x : ScalarGNSHilbert P) (u : ScalarGNSHilbert P)).re +
        (inner ℂ (x : ScalarGNSHilbert P) (scalarTomitaSquare P u)).re :=
      congrArg (fun a : ℝ => (inner ℂ (x : ScalarGNSHilbert P)
        (u : ScalarGNSHilbert P)).re + a) hp
    _ = (inner ℂ (x : ScalarGNSHilbert P)
        ((u : ScalarGNSHilbert P) + scalarTomitaSquare P u)).re :=
      (congrArg Complex.re (inner_add_right (x : ScalarGNSHilbert P)
        (u : ScalarGNSHilbert P) (scalarTomitaSquare P u))).symm
    _ = _ := congrArg (fun v : ScalarGNSHilbert P =>
      (inner ℂ (x : ScalarGNSHilbert P) v).re) hu

/-- D(S†S) is dense in D(S) with its graph norm, not merely dense in H_I. -/
theorem scalarTomitaSquare_graph_core :
    DenseRange (realGraphInclusion (scalarClosedTomitaDomain P)
      (antilinearRealMap (scalarClosedTomitaDomain P) (scalarClosedTomita P))
      (scalarTomitaSquare P).domain (scalarTomitaSquareDomain_le P)) :=
  realGraphInclusion_dense (scalarClosedTomitaDomain P)
    (antilinearRealMap (scalarClosedTomitaDomain P) (scalarClosedTomita P))
    (scalarTomitaSquare P).domain (scalarTomitaSquareDomain_le P)
    (scalarClosedTomita_is_closed (P := P)) (scalarTomitaSquare_weak_graph_identity P)

theorem scalarTomitaSquare_graph_approximation (x : scalarClosedTomitaDomain P) :
    ∃ u : ℕ → (scalarTomitaSquare P).domain,
      Tendsto (fun n => (u n : ScalarGNSHilbert P)) atTop (𝓝 (x : ScalarGNSHilbert P)) ∧
      Tendsto (fun n => scalarClosedTomita P (scalarTomitaSquareInput P (u n)))
        atTop (𝓝 (scalarClosedTomita P x)) :=
  realGraphCore_sequence (scalarClosedTomitaDomain P)
    (antilinearRealMap (scalarClosedTomitaDomain P) (scalarClosedTomita P))
    (scalarTomitaSquare P).domain (scalarTomitaSquareDomain_le P)
    (scalarTomitaSquare_graph_core P) x

#print axioms scalarTomitaSquareDomain_le
#print axioms scalarTomitaSquare_weak_graph_identity
#print axioms scalarTomitaSquare_graph_core
#print axioms scalarTomitaSquare_graph_approximation
end
end TGLV350.Regular
