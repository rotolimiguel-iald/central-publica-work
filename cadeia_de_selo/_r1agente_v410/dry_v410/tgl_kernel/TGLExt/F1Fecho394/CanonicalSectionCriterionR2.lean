import TGLExt.F1Fecho394.PartialFourierWeightedGraphR2
import TGLExt.F1Fecho394.GeometricIdentification

/-! A sectionwise integral identity implies membership in the previously
constructed canonical standard subspace, on the original H1. Section L1 and
the actual boundary identity are explicit inputs, to be discharged by the
regulated physical Maxwell coefficient. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
open MeasureTheory Filter
open scoped FourierTransform
namespace F1Fecho.CanonicalSectionCriterion
open TGLExt.ImportedSQ AuditF13v31 ChatgptAudit.WignerRapidityMeasure016
open F1Rede F1Rede.Canonical F1Rede.CanonicalWedge F1Rede.GeometricIdentification
open F1Rede.FiberConjugation F1Fecho.PartialFourierRepresentative
local instance : InnerProductSpace ℝ Fib := InnerProductSpace.complexToReal

theorem Jcandidate_section_ae (f : H1) :
    ∀ᵐ q ∂(volume : Measure Transverse),
      (fun r : ℝ => toRapidity (Jcandidate f) (q,r)) =ᵐ[volume]
        fun r => fiberSwappedJ (toRapidity f (-q,r)) :=
  Measure.ae_ae_of_ae_prod (Jcandidate_rapidity_ae f)

theorem mem_KWR_of_section_balance (f : H1)
    (hL1 : ∀ᵐ q ∂(volume : Measure Transverse),
      Integrable (fun r : ℝ => toRapidity f (q,r)))
    (hb : ∀ᵐ q ∂(volume : Measure Transverse), ∀ p : ℝ,
      (Real.exp (2*Real.pi^2*p):ℂ) • 𝓕 (fun r : ℝ => toRapidity f (q,r)) p =
        fiberSwappedJ (𝓕 (fun r : ℝ => toRapidity f (-q,r)) (-p))) :
    f ∈ KWR.toClosedSubmodule := by
  have hn := (Measure.measurePreserving_neg (volume : Measure Transverse)).quasiMeasurePreserving.ae hL1
  have hJ : ∀ᵐ q ∂(volume : Measure Transverse),
      Integrable (fun r : ℝ => toRapidity (Jcandidate f) (q,r)) := by
    filter_upwards [Jcandidate_section_ae f,hn] with q hq hqn
    exact ((FourierConjugation.realMap fiberSwappedJ).integrable_comp hqn).congr hq.symm
  have hbalance : ∀ᵐ q ∂(volume : Measure Transverse), ∀ᵐ p ∂(volume : Measure ℝ),
      𝓕 (fun r : ℝ => toRapidity (Jcandidate f) (q,r)) p =
        (Real.exp (2*Real.pi^2*p):ℂ) • 𝓕 (fun r : ℝ => toRapidity f (q,r)) p := by
    filter_upwards [Jcandidate_section_ae f,hn,hb] with q hq hqn hqb
    filter_upwards [] with p
    rw [Real.fourier_congr_ae hq p,FourierConjugation.fourier_integral fiberSwappedJ _ hqn p]
    exact (hqb p).symm
  have hgraph : (f,Jcandidate f) ∈ TW.graph := by
    apply (TW_multiplier f (Jcandidate f)).mpr
    exact partial_weighted_graph (volume : Measure Transverse) (toRapidity f)
      (toRapidity (Jcandidate f)) hL1 hJ (fun p => (Real.exp (2*Real.pi^2*p):ℂ))
      (by fun_prop) hbalance
  obtain ⟨x,hx⟩ := (TW.mem_graph_iff').mp hgraph
  have hxf : (x:H1)=f := congrArg Prod.fst hx
  have hxg : TW x=Jcandidate f := congrArg Prod.snd hx
  have hdom : f ∈ TW.domain := hxf ▸ x.property
  apply (KWR_mem f).mpr
  refine ⟨hdom,?_⟩
  have he : (⟨f,hdom⟩:TW.domain)=x := Subtype.ext hxf.symm
  change Jcandidate (TW ⟨f,hdom⟩)=f
  rw [he,hxg,Jcandidate_involutive f]

end F1Fecho.CanonicalSectionCriterion
#print axioms F1Fecho.CanonicalSectionCriterion.Jcandidate_section_ae
#print axioms F1Fecho.CanonicalSectionCriterion.mem_KWR_of_section_balance
