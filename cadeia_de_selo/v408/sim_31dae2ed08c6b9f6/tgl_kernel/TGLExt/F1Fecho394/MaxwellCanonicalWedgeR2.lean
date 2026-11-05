import TGLExt.F1Fecho394.MaxwellVectorBalanceR1
import TGLExt.F1Fecho394.CanonicalSectionCriterionR2
import TGLExt.F1Fecho394.RapidityGaussianR1
import TGLExt.F1Fecho394.PhysicalCircularRapidityR1

/-! Genuine wedge-supported real Maxwell tests belong to the already built
canonical KWR. The Gaussian is removed by strong convergence and closedness.
This is one inclusion only: no reverse density, locality or wedge_glue is
asserted by this module. -/
set_option autoImplicit false
set_option maxHeartbeats 2400000
noncomputable section
open MeasureTheory Filter
open scoped FourierTransform Topology
namespace F1Fecho.MaxwellLocalization
open F1Fecho.MaxwellGlobal F1Fecho.OrbitalScreen F1Fecho.MaxwellStrip
open F1Fecho.GaussianL2Removal F1Fecho.CanonicalSectionCriterion
open TGLExt.ImportedSQ AuditF13v31 ChatgptAudit.WignerRapidityMeasure016
open F1Rede.CanonicalWedge F1Rede.FiberConjugation

def regulatedCircular (n : ℕ) (f : SchwartzTensor) : H1 :=
  RapidityGaussian.regularize n (circularSmear f)

theorem regulatedCircular_sections (n : ℕ) (f : SchwartzTensor) :
    ∀ᵐ q ∂(volume : Measure Transverse),
      (fun r : ℝ => toRapidity (regulatedCircular n f) (q,r)) =ᵐ[volume]
        fun r => circularFiber.symm (regularizedVector (width n) q f r) := by
  have hr := Measure.ae_ae_of_ae_prod
    (RapidityGaussian.regularize_rapidity_ae n (circularSmear f))
  have hc := Measure.ae_ae_of_ae_prod (circularSmear_rapidity_ae f)
  have hn : ∀ᵐ q ∂(volume : Measure Transverse),q≠0 := by
    simp only [ae_iff, not_not, Set.setOf_eq_eq_singleton, measure_singleton]
  filter_upwards [hr,hc,hn] with q hqr hqc hq
  filter_upwards [hqr,hqc] with r hrr hcr
  change toRapidity (regulatedCircular n f) (q,r)=_ at hrr
  rw [hrr,hcr,regularizedVector_real (width n) (q,r) hq f,map_smul]

theorem regulatedCircular_section_integrable (n : ℕ) (f : SchwartzTensor)
    (hf : supportedTensorRight f) :
    ∀ᵐ q ∂(volume : Measure Transverse),
      Integrable (fun r : ℝ => toRapidity (regulatedCircular n f) (q,r)) := by
  filter_upwards [regulatedCircular_sections n f] with q hq
  exact (circularFiber.symm.toContinuousLinearEquiv.toContinuousLinearMap.integrable_comp
    (regularizedVector_integrable (width n) (width_pos n) q f hf)).congr hq.symm

theorem regulatedCircular_section_balance (n : ℕ) (f : SchwartzTensor)
    (hf : supportedTensorRight f) (hreal : IsRealTest f) :
    ∀ᵐ q ∂(volume : Measure Transverse), ∀ p : ℝ,
      (Real.exp (2*Real.pi^2*p):ℂ) •
        𝓕 (fun r : ℝ => toRapidity (regulatedCircular n f) (q,r)) p =
      fiberSwappedJ (𝓕 (fun r : ℝ => toRapidity (regulatedCircular n f) (-q,r)) (-p)) := by
  have hs := regulatedCircular_sections n f
  have hn := (Measure.measurePreserving_neg (volume : Measure Transverse)).quasiMeasurePreserving.ae hs
  have hq0 : ∀ᵐ q ∂(volume : Measure Transverse),q≠0 := by
    simp only [ae_iff, not_not, Set.setOf_eq_eq_singleton, measure_singleton]
  filter_upwards [hs,hn,hq0] with q hq hqn hqne
  intro p
  rw [Real.fourier_congr_ae hq p,Real.fourier_congr_ae hqn (-p)]
  have hu (q : Transverse) (p : ℝ) :
      𝓕 (fun r => circularFiber.symm (regularizedVector (width n) q f r)) p =
        circularFiber.symm (𝓕 (regularizedVector (width n) q f) p) :=
    FourierNaturality.fourier_integral_postcomp
      circularFiber.symm.toContinuousLinearEquiv.toContinuousLinearMap _
      (regularizedVector_integrable (width n) (width_pos n) q f hf) p
  rw [hu,hu,←map_smul, maxwell_vector_fourier_balance
    (width n) (width_pos n) q hqne f hf hreal p,circularFiber_symm_conjugation]

theorem regulatedCircular_mem_KWR (n : ℕ) (f : SchwartzTensor)
    (hf : supportedTensorRight f) (hreal : IsRealTest f) :
    regulatedCircular n f ∈ KWR.toClosedSubmodule :=
  mem_KWR_of_section_balance _ (regulatedCircular_section_integrable n f hf)
    (regulatedCircular_section_balance n f hf hreal)

theorem circularSmear_mem_KWR (f : SchwartzTensor)
    (hf : supportedTensorRight f) (hreal : IsRealTest f) :
    circularSmear f ∈ KWR.toClosedSubmodule := by
  apply KWR.toClosedSubmodule.isClosed.mem_of_tendsto
    (RapidityGaussian.regularize_tendsto (circularSmear f))
  exact Filter.Eventually.of_forall (fun n => regulatedCircular_mem_KWR n f hf hreal)

end F1Fecho.MaxwellLocalization
#print axioms F1Fecho.MaxwellLocalization.regulatedCircular_sections
#print axioms F1Fecho.MaxwellLocalization.regulatedCircular_section_balance
#print axioms F1Fecho.MaxwellLocalization.regulatedCircular_mem_KWR
#print axioms F1Fecho.MaxwellLocalization.circularSmear_mem_KWR
