import TGLExt.F1Fecho394.GaussianL2RemovalR4
import TGLExt.F1Fecho394.GeometricIdentification

/-! The bounded Gaussian acts in the actual rapidity coordinate and converges
strongly on the unchanged H1. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
open MeasureTheory Filter
open scoped Topology
namespace F1Fecho.RapidityGaussian
open TGLExt.ImportedSQ AuditF13v31 ChatgptAudit.WignerRapidityMeasure016
open F1Rede F1Rede.Canonical F1Rede.GeometricIdentification
open F1Fecho.GaussianL2Removal F1Fecho.WedgeLaplace

def regularize (n : ℕ) (f : H1) : H1 :=
  curriedRapidity.symm (GaussianL2Removal.regularize n (curriedRapidity f))

theorem regularize_tendsto (f : H1) : Tendsto (fun n => regularize n f) atTop (𝓝 f) := by
  have h := curriedRapidity.symm.continuous.continuousAt.tendsto.comp
    (GaussianL2Removal.regularize_tendsto (curriedRapidity f))
  simpa only [Function.comp_def,regularize,LinearIsometryEquiv.symm_apply_apply] using h

theorem regularize_rapidity_ae (n : ℕ) (f : H1) :
    toRapidity (regularize n f) =ᵐ[momentumMeasure]
      fun z => lowerGaussian (width n) z.2 • toRapidity f z := by
  have hc : curriedRapidity (regularize n f)=
      GaussianL2Removal.regularize n (curriedRapidity f) :=
    LinearIsometryEquiv.apply_symm_apply _ _
  have hs : ∀ᵐ r ∂(volume : Measure ℝ), ∀ᵐ q ∂(volume : Measure Transverse),
      toRapidity (regularize n f) (q,r)=lowerGaussian (width n) r • toRapidity f (q,r) := by
    have ha := canonicalFub_sections (toRapidity (regularize n f))
    change ∀ᵐ r ∂(volume : Measure ℝ),
      (curriedRapidity (regularize n f) r : Transverse → Fib) =ᵐ[volume] _ at ha
    rw [hc] at ha
    filter_upwards [ha,canonicalFub_sections (toRapidity f),
      GaussianL2Removal.regularize_ae n (curriedRapidity f)] with r hreg hf hr
    rw [hr] at hreg
    filter_upwards [hreg,hf,Lp.coeFn_smul (lowerGaussian (width n) r)
      (curriedRapidity f r)] with q hq hqf hsm
    change (lowerGaussian (width n) r • curriedRapidity f r) q =
      lowerGaussian (width n) r • curriedRapidity f r q at hsm
    change curriedRapidity f r q=toRapidity f (q,r) at hqf
    rw [hsm,hqf] at hq
    exact hq.symm
  have hm : StronglyMeasurable (fun z : Transverse×ℝ =>
      lowerGaussian (width n) z.2 • toRapidity f z) :=
    ((regulator_continuous n).stronglyMeasurable.comp_measurable measurable_snd).smul
      (Lp.stronglyMeasurable (toRapidity f))
  have he := (Lp.stronglyMeasurable (toRapidity (regularize n f))).measurableSet_eq_fun hm
  exact (Measure.ae_prod_iff_ae_ae he).mpr ((Measure.ae_ae_comm he).mpr hs)

end F1Fecho.RapidityGaussian
#print axioms F1Fecho.RapidityGaussian.regularize_tendsto
#print axioms F1Fecho.RapidityGaussian.regularize_rapidity_ae
