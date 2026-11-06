import TGLExt.F1Fecho394.VectorWedge
import TGLExt.F1Fecho394.SpectralConjugation
import TGLExt.F1Fecho394.GeometricFiberConjugation
set_option autoImplicit false
set_option maxHeartbeats 600000
noncomputable section
open MeasureTheory Filter
namespace F1Rede.Wedge
open ChatgptAudit.Continuous049 ChatgptAudit.Continuous050
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
variable (jc : H ≃ₛₗᵢ[starRingEnd ℂ] H) (hJ : Function.Involutive jc)
theorem JA_eq_BJ (c : ℝ) (f : VH H) :
    SpectralConjugation.J jc hJ (A c f) = B c (SpectralConjugation.J jc hJ f) := by
  apply Lp.ext
  have hr := (Measure.measurePreserving_neg (volume : Measure ℝ)).quasiMeasurePreserving.ae (A_ae c f)
  filter_upwards [SpectralConjugation.J_ae jc hJ (A c f), B_ae c (SpectralConjugation.J jc hJ f),
    SpectralConjugation.J_ae jc hJ f,hr] with x hj hb hf ha
  rw [hj,hb,hf,ha,spectral_weight_reflection,map_smulₛₗ]
  simp
theorem JB_eq_AJ (c : ℝ) (f : VH H) :
    SpectralConjugation.J jc hJ (B c f) = A c (SpectralConjugation.J jc hJ f) := by
  have h := JA_eq_BJ jc hJ c (SpectralConjugation.J jc hJ f)
  apply (SpectralConjugation.J jc hJ).injective
  simpa only [SpectralConjugation.J_involutive jc hJ f,
    SpectralConjugation.J_involutive jc hJ (B c f)] using h.symm
end F1Rede.Wedge

namespace F1Rede.CanonicalWedge
open TGLExt.ImportedSQ AuditF13v31 F1Rede.Canonical F1Rede.FiberConjugation
open ChatgptAudit.Continuous049 ChatgptAudit.Continuous050
abbrev RH := RapidityHilbert
abbrev Phi := canonicalPartialFourier
def Js : RH ≃ₛₗᵢ[starRingEnd ℂ] RH := SpectralConjugation.J transverseGeometricJ transverseGeometricJ_involutive
theorem Js_involutive : Function.Involutive Js :=
  SpectralConjugation.J_involutive transverseGeometricJ transverseGeometricJ_involutive
/-- Concrete spectral candidate on canonical H1: xi and q reflection, conjugation and helicity swap.
Its geometric covariance/localization as a physical wedge reflection is NOT asserted here. -/
def Jcandidate : H1 ≃ₛₗᵢ[starRingEnd ℂ] H1 := (Phi.trans Js).trans Phi.symm
theorem Jcandidate_apply (f : H1) : Jcandidate f = Phi.symm (Js (Phi f)) := rfl
theorem Jcandidate_involutive : Function.Involutive Jcandidate := by
  intro f
  simp only [Jcandidate_apply, LinearIsometryEquiv.apply_symm_apply]
  rw [Js_involutive (Phi f), LinearIsometryEquiv.symm_apply_apply]

def pull : (RH →L[ℂ] RH) ≃⋆ₐ[ℂ] (H1 →L[ℂ] H1) := Phi.symm.conjStarAlgEquiv
theorem pull_apply (L : RH →L[ℂ] RH) (f : H1) : pull L f = Phi.symm (L (Phi f)) := rfl
theorem Phi_pull (L : RH →L[ℂ] RH) (f : H1) : Phi (pull L f) = L (Phi f) := by
  rw [pull_apply,LinearIsometryEquiv.apply_symm_apply]
def WA (c : ℝ) : H1 →L[ℂ] H1 := pull (Wedge.A (H := TransverseFiber) c)
def WB (c : ℝ) : H1 →L[ℂ] H1 := pull (Wedge.B (H := TransverseFiber) c)
theorem WA_injective (c : ℝ) : Function.Injective (WA c) := by
  intro f g h
  apply Phi.injective
  apply Wedge.A_injective (H := TransverseFiber) c
  simpa only [WA,Phi_pull] using congrArg Phi h
theorem WA_selfadjoint (c : ℝ) : IsSelfAdjoint (WA c) := by
  change star (pull (Wedge.A (H := TransverseFiber) c)) = pull (Wedge.A (H := TransverseFiber) c)
  exact (map_star pull (Wedge.A (H := TransverseFiber) c)).symm.trans
    (congrArg pull (Wedge.A_selfadjoint (H := TransverseFiber) c).star_eq)
theorem WB_selfadjoint (c : ℝ) : IsSelfAdjoint (WB c) := by
  change star (pull (Wedge.B (H := TransverseFiber) c)) = pull (Wedge.B (H := TransverseFiber) c)
  exact (map_star pull (Wedge.B (H := TransverseFiber) c)).symm.trans
    (congrArg pull (Wedge.B_selfadjoint (H := TransverseFiber) c).star_eq)
theorem WAB_commute (c : ℝ) : WA c * WB c = WB c * WA c := by
  change pull (Wedge.A c) * pull (Wedge.B c) = pull (Wedge.B c) * pull (Wedge.A c)
  rw [← map_mul,← map_mul,Wedge.AB_commute]
theorem WAB_square_sum (c : ℝ) : WA c * WA c + WB c * WB c = 1 := by
  change pull (Wedge.A c) * pull (Wedge.A c) + pull (Wedge.B c) * pull (Wedge.B c) = 1
  calc
    _ = pull (Wedge.A c * Wedge.A c) + pull (Wedge.B c * Wedge.B c) := by
      exact congrArg₂ (fun a b : H1 →L[ℂ] H1 => a + b)
        (pull.map_mul (Wedge.A c) (Wedge.A c)).symm
        (pull.map_mul (Wedge.B c) (Wedge.B c)).symm
    _ = pull (Wedge.A c * Wedge.A c + Wedge.B c * Wedge.B c) := (pull.map_add _ _).symm
    _ = pull 1 := congrArg pull (Wedge.AB_square_sum (H := TransverseFiber) c)
    _ = 1 := pull.map_one
theorem WAB_positive (c : ℝ) (f : H1) : 0 ≤ (inner ℂ (WA c f) (WB c f)).re := by
  change 0 ≤ (inner ℂ (pull (Wedge.A c) f) (pull (Wedge.B c) f)).re
  rw [pull_apply,pull_apply,Phi.symm.inner_map_map]
  exact Wedge.AB_positive c (Phi f)
theorem Jcandidate_WB (c : ℝ) (f : H1) : Jcandidate (WB c f) = WA c (Jcandidate f) := by
  apply Phi.injective
  simp only [Jcandidate_apply,WB,WA,Phi_pull,LinearIsometryEquiv.apply_symm_apply]
  exact Wedge.JB_eq_AJ transverseGeometricJ transverseGeometricJ_involutive c (Phi f)

/-- Parameterized positive self-adjoint multiplier, represented on the unchanged H1. -/
def WT (c : ℝ) : H1 →ₗ.[ℂ] H1 := boundedGraphOperator (WA c) (WB c) (WA_injective c)
theorem WT_selfadjoint (c : ℝ) : IsSelfAdjoint (WT c) :=
  bounded_graph_selfadjoint (WA c) (WB c) (WA_injective c) (WA_selfadjoint c) (WB_selfadjoint c)
    (WAB_commute c) (WAB_square_sum c)
theorem WT_positive (c : ℝ) (f : (WT c).domain) : 0 ≤ (inner ℂ (f:H1) (WT c f)).re :=
  bounded_graph_positive (WA c) (WB c) (WA_injective c) (WAB_positive c) f
theorem WT_dense (c : ℝ) : Dense ((WT c).domain : Set H1) :=
  bounded_graph_domain_dense (WA c) (WB c) (WA_injective c) (WA_selfadjoint c)
theorem WT_graph (c : ℝ) (f g : H1) : (f,g) ∈ (WT c).graph ↔
    (Phi f,Phi g) ∈ (Wedge.T (H := TransverseFiber) c).graph := by
  change (f,g) ∈ (boundedGraphOperator (WA c) (WB c) (WA_injective c)).graph ↔ _
  rw [bounded_graph_equation_iff (WA c) (WB c) (WA_injective c) (WAB_commute c) (WAB_square_sum c)]
  change WB c f = WA c g ↔ (Phi f,Phi g) ∈
    (boundedGraphOperator (Wedge.A (H := TransverseFiber) c) (Wedge.B (H := TransverseFiber) c)
      (Wedge.A_injective (H := TransverseFiber) c)).graph
  rw [bounded_graph_equation_iff (Wedge.A (H := TransverseFiber) c) (Wedge.B c)
    (Wedge.A_injective c) (Wedge.AB_commute c) (Wedge.AB_square_sum c)]
  constructor
  · intro h
    simpa only [WB,WA,Phi_pull] using congrArg Phi h
  · intro h
    apply Phi.injective
    simpa only [WB,WA,Phi_pull] using h

def rootParameter : ℝ := -(2 * Real.pi ^ 2)
def TW : H1 →ₗ.[ℂ] H1 := WT rootParameter
/-- Positive half-modular multiplier exp(2*pi^2*xi), including its full graph/domain. -/
theorem TW_multiplier (f g : H1) : (f,g) ∈ TW.graph ↔
    (Phi g : ℝ → TransverseFiber) =ᵐ[volume]
      fun ξ => (Real.exp (2 * Real.pi ^ 2 * ξ) : ℂ) • Phi f ξ := by
  rw [TW,WT_graph,Wedge.T_graph]
  simp only [rootParameter,neg_neg]
theorem TW_positive (f : TW.domain) : 0 ≤ (inner ℂ (f:H1) (TW f)).re := WT_positive rootParameter f
theorem TW_selfadjoint : IsSelfAdjoint TW := WT_selfadjoint rootParameter

theorem SW_closed : IsClosed (Set.range (fun x : TW.domain => ((x:H1),SW TW Jcandidate x))) :=
  bounded_graph_tomita_closed (WA rootParameter) (WB rootParameter) (WA_injective rootParameter)
    (WAB_commute rootParameter) (WAB_square_sum rootParameter) Jcandidate Jcandidate_involutive
theorem SW_maps (x : TW.domain) : SW TW Jcandidate x ∈ TW.domain :=
  bounded_graph_tomita_maps_domain (WA rootParameter) (WB rootParameter) (WA_injective rootParameter)
    Jcandidate (Jcandidate_WB rootParameter) x
theorem SW_involutive (x : TW.domain) : SW TW Jcandidate ⟨SW TW Jcandidate x, SW_maps x⟩ = (x:H1) :=
  bounded_graph_tomita_involutive (WA rootParameter) (WB rootParameter) (WA_injective rootParameter)
    Jcandidate Jcandidate_involutive (Jcandidate_WB rootParameter) x
/-- A concrete standard real subspace on canonical H1, built as Fix(Jcandidate*TW). -/
def KWR : StandardSubspace H1 := closedAntilinearStandardSubspace TW.domain (SW TW Jcandidate)
  SW_closed SW_maps SW_involutive (WT_dense rootParameter)
theorem KWR_mem (f : H1) : f ∈ KWR.toClosedSubmodule ↔ ∃ hf : f ∈ TW.domain, SW TW Jcandidate ⟨f,hf⟩ = f := Iff.rfl

#print axioms Jcandidate
#print axioms Jcandidate_involutive
#print axioms TW_selfadjoint
#print axioms TW_positive
#print axioms TW_multiplier
#print axioms SW_involutive
#print axioms KWR
end F1Rede.CanonicalWedge