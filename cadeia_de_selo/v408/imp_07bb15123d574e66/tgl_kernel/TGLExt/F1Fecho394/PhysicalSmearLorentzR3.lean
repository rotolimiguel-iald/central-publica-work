import TGLExt.F1Fecho394.MaxwellLorentzContractionR5
import TGLExt.F1Fecho394.PhysicalTensorLorentzR7
import TGLExt.F1Fecho394.ScreenHelicityRepresentationR3

/-! Physical covariance of the real-test Maxwell net under the constructed
Lorentz screen representation. This gives covariance on arbitrary regions;
causal commutation and standard-wedge equality are not assumed. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
open MeasureTheory Matrix
namespace F1Fecho.MaxwellLocalization
open TGLExt TGLExt.ImportedSQ F1Fecho.MaxwellGlobal F1Fecho.OrbitalSpatial
open F1Fecho.OrbitalScreen F1Fecho.SpacetimeLorentz F1Fecho.PhysicalTensorLorentz
open F1Fecho.MaxwellLorentzContraction
open ChatgptAudit.WignerOrbit016 ChatgptAudit.WignerRapidityMeasure016

theorem inverse_lorentz_shell_ae (L:generatedLorentz) :
    ∀ᵐp ∂orbitalMeasure 0,(action L.val).symm (shellEmbedding p)=
      shellEmbedding (shellAction L⁻¹.val p) := by
  filter_upwards [(shellAction_lift L⁻¹).2] with p hp
  apply PiLp.ext
  intro i
  exact congrFun hp.symm i

theorem physicalSmear_lorentz (L:generatedLorentz) (f:SchwartzTensor) :
    physicalSmearCLM (transform L.val f)=transverseUnitary L (physicalSmearCLM f) := by
  have htr:=(shellAction_lift L⁻¹).1.quasiMeasurePreserving.ae (physicalSmear_ae f)
  apply Lp.ext
  filter_upwards [physicalSmear_ae (transform L.val f),
    transverseAction_ae L (physicalSmearCLM f),htr,
    inverse_lorentz_shell_ae L,contraction_lorentz_ae L] with p h1 h2 h3 hs hc
  change physicalSmearCLM (transform L.val f) p=transverseAction L (physicalSmearCLM f) p
  rw [h1,h2,h3]
  apply PiLp.ext
  intro j
  change (1/2:ℂ)*(∑μ,∑ν,(cartesianStrength p j μ ν:ℂ)*
      physicalFourierCLM (transform L.val f) (shellEmbedding p) μ ν)=
    ∑i:Fin 2,transportMatrix L p j i *
      ((1/2:ℂ)*(∑μ,∑ν,(cartesianStrength (shellAction L⁻¹.val p) i μ ν:ℂ)*
        physicalFourierCLM f (shellEmbedding (shellAction L⁻¹.val p)) μ ν))
  rw [physicalFourier_transform,hs]
  have hcs:=hc j (physicalFourierCLM f (shellEmbedding (shellAction L⁻¹.val p)))
  change (∑μ,∑ν,(cartesianStrength p j μ ν:ℂ)*
    F1Fecho.CovariantTensor.pull (L.val⁻¹.val.map Complex.ofReal)
      (physicalFourierCLM f (shellEmbedding (shellAction L⁻¹.val p))) μ ν)=_ at hcs
  rw [hcs,Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro i hi
  ring

theorem circularSmear_lorentz (L:generatedLorentz) (f:SchwartzTensor) :
    circularSmear (transform L.val f)=helicityUnitary L (circularSmear f) := by
  rw [helicityUnitary_apply]
  change circularH1.symm (physicalSmearCLM (transform L.val f))=
    circularH1.symm (transverseUnitary L (circularH1 (circularH1.symm (physicalSmearCLM f))))
  rw [circularH1.apply_symm_apply,physicalSmear_lorentz]

def lorentzRegion (L:generatedLorentz) (O:Set Spacetime) : Set Spacetime := action L.val '' O

theorem lorentz_generator (L:generatedLorentz) (O:Set Spacetime) (v:H1)
    (hv:v∈supportedGenerators O) : helicityUnitary L v∈supportedGenerators (lorentzRegion L O) := by
  obtain ⟨f,hr,hs,rfl⟩:=hv
  exact ⟨transform L.val f,transform_real _ f hr,
    (transform_support _ f).trans (Set.image_mono hs),circularSmear_lorentz L f⟩

theorem localized_lorentz (L:generatedLorentz) (O:Set Spacetime) (v:H1)
    (hv:v∈localized O) : helicityUnitary L v∈localized (lorentzRegion L O) := by
  let T:H1→L[ℝ]H1:=(helicityUnitary L).toLinearIsometry.toContinuousLinearMap.restrictScalars ℝ
  have hs:(Submodule.span ℝ (supportedGenerators O)).map T.toLinearMap≤
      Submodule.span ℝ (supportedGenerators (lorentzRegion L O)) := by
    rw [Submodule.map_span]
    apply Submodule.span_le.mpr
    rintro w ⟨x,hx,rfl⟩
    exact Submodule.subset_span (lorentz_generator L O x hx)
  exact (Submodule.topologicalClosure_mono hs)
    ((Submodule.topologicalClosure_map T _) (Submodule.mem_map.mpr ⟨v,hv,rfl⟩))

theorem lorentzRegion_inverse (L:generatedLorentz) (O:Set Spacetime) :
    lorentzRegion L⁻¹ (lorentzRegion L O)=O := by
  change (action L.val).symm '' ((action L.val) '' O)=O
  exact (action L.val).toEquiv.symm_image_image O

theorem localized_lorentz_iff (L:generatedLorentz) (O:Set Spacetime) (v:H1) :
    v∈localized O ↔ helicityUnitary L v∈localized (lorentzRegion L O) := by
  constructor
  · exact localized_lorentz L O v
  · intro hv
    have h:=localized_lorentz L⁻¹ (lorentzRegion L O) (helicityUnitary L v) hv
    rw [lorentzRegion_inverse,←helicityUnitary_mul,inv_mul_cancel,helicityUnitary_one] at h
    exact h

end F1Fecho.MaxwellLocalization
#print axioms F1Fecho.MaxwellLocalization.physicalSmear_lorentz
#print axioms F1Fecho.MaxwellLocalization.circularSmear_lorentz
#print axioms F1Fecho.MaxwellLocalization.localized_lorentz_iff
