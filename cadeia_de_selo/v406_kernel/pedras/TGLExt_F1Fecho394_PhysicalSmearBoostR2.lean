import TGLExt.F1Fecho394.PhysicalTensorLorentzR7
import TGLExt.F1Fecho394.MaxwellBoostContractionR1
import TGLExt.F1Fecho394.ScreenHelicityRepresentationR3
import TGLExt.F1Fecho394.CanonicalWedgeUniquenessR5

/-! Actual covariance of physical Maxwell smearing under longitudinal boosts.
This transports real, wedge-supported test tensors to the same H1 and closes
the corresponding real span. Wedge equality still requires complex density;
that density is explicitly conditional in the final consumer below. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
open MeasureTheory
namespace F1Fecho.MaxwellLocalization
open TGLExt TGLExt.ImportedSQ F1Fecho.MaxwellGlobal F1Fecho.OrbitalSpatial
open F1Fecho.OrbitalScreen F1Fecho.SpacetimeLorentz F1Fecho.PhysicalTensorLorentz
open F1Fecho.MaxwellBoostContraction F1Rede.CanonicalWedge
open ChatgptAudit.WignerOrbit016 ChatgptAudit.WignerRapidityMeasure016

theorem inverse_boost_shell_ae (s:ℝ) :
    ∀ᵐp ∂orbitalMeasure 0,(action (theBoost s)).symm (shellEmbedding p)=
      shellEmbedding (coordinateBoost 0 (-s) p) := by
  filter_upwards [shell_boost_ae (-s)] with p hp
  apply PiLp.ext
  intro i
  change (((theBoost s)⁻¹).val.mulVec (shellMomentum 0 p)) i=
    shellMomentum 0 (coordinateBoost 0 (-s) p) i
  rw [theBoost_inv_eq]
  exact congrFun hp.symm i

theorem physicalSmear_boost (s:ℝ) (f:SchwartzTensor) :
    physicalSmearCLM (transform (theBoost s) f)=B0 s (physicalSmearCLM f) := by
  have htr := (coordinateBoost_measurePreserving 0 (-s)).quasiMeasurePreserving.ae
    (physicalSmear_ae f)
  apply Lp.ext
  filter_upwards [physicalSmear_ae (transform (theBoost s) f),
    orbitalScalarBoost_ae 0 s (physicalSmearCLM f),htr,
    inverse_boost_shell_ae s,boost_contraction_ae s] with p h1 h2 h3 hs hc
  change physicalSmearCLM (transform (theBoost s) f) p=
    orbitalScalarBoost 0 s (physicalSmearCLM f) p
  rw [h1,h2,h3]
  apply PiLp.ext
  intro j
  change (1/2:ℂ)*(∑μ,∑ν,(cartesianStrength p j μ ν:ℂ)*
    physicalFourierCLM (transform (theBoost s) f) (shellEmbedding p) μ ν)=
    (1/2:ℂ)*(∑μ,∑ν,(cartesianStrength (coordinateBoost 0 (-s) p) j μ ν:ℂ)*
      physicalFourierCLM f (shellEmbedding (coordinateBoost 0 (-s) p)) μ ν)
  rw [physicalFourier_transform,hs,hc]

theorem circularSmear_boost (s:ℝ) (f:SchwartzTensor) :
    circularSmear (transform (theBoost s) f)=B0 s (circularSmear f) := by
  rw [←helicityUnitary_boost s (circularSmear f),helicityUnitary_apply]
  change circularH1.symm (physicalSmearCLM (transform (theBoost s) f))=
    circularH1.symm (transverseUnitary (generatedBoost s)
      (circularH1 (circularH1.symm (physicalSmearCLM f))))
  rw [circularH1.apply_symm_apply,transverseUnitary_boost,physicalSmear_boost]

theorem boosted_wedge_generator (s:ℝ) (v:H1)
    (hv:v∈supportedGenerators physicalRightWedge) :
    B0 s v∈supportedGenerators physicalRightWedge := by
  obtain ⟨f,hr,hs,rfl⟩:=hv
  exact ⟨transform (theBoost s) f,transform_real _ f hr,
    transform_boost_support s f hs,circularSmear_boost s f⟩

theorem localized_wedge_boost (s:ℝ) (v:H1)
    (hv:v∈localized physicalRightWedge) : B0 s v∈localized physicalRightWedge := by
  let T:H1→L[ℝ]H1:=(B0 s).toLinearIsometry.toContinuousLinearMap.restrictScalars ℝ
  have hs:(Submodule.span ℝ (supportedGenerators physicalRightWedge)).map T.toLinearMap≤
      Submodule.span ℝ (supportedGenerators physicalRightWedge) := by
    rw [Submodule.map_span]
    apply Submodule.span_le.mpr
    rintro w ⟨x,hx,rfl⟩
    exact Submodule.subset_span (boosted_wedge_generator s x hx)
  exact (Submodule.topologicalClosure_mono hs)
    ((Submodule.topologicalClosure_map T _) (Submodule.mem_map.mpr ⟨v,hv,rfl⟩))

theorem localized_wedge_eq_KWR_of_complex_dense
    (hd:(Submodule.span ℂ (localized physicalRightWedge:Set H1)).topologicalClosure=⊤) :
    localized physicalRightWedge=KWR.toClosedSubmodule.toSubmodule :=
  CanonicalWedgeUniqueness.eq_KWR_of_dense_and_boost_invariant _
    (localized_closed _) localized_rightWedge_le_KWR hd localized_wedge_boost

end F1Fecho.MaxwellLocalization
#print axioms F1Fecho.MaxwellLocalization.inverse_boost_shell_ae
#print axioms F1Fecho.MaxwellLocalization.physicalSmear_boost
#print axioms F1Fecho.MaxwellLocalization.circularSmear_boost
#print axioms F1Fecho.MaxwellLocalization.localized_wedge_boost
#print axioms F1Fecho.MaxwellLocalization.localized_wedge_eq_KWR_of_complex_dense
