import TGLExt.F1Fecho394.ComplexHalfConjugationR1
import TGLExt.F1Fecho394.PhysicalFourierRealityR4
import TGLExt.F1Fecho394.PhysicalCircularRapidityR1
import TGLExt.F1Fecho394.PhysicalLocalizedSubspacesR3

/-! The helicity-swapping antiunitary Theta acts on real physical Maxwell
smears by spacetime inversion. This is an actual test-map identity. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
open MeasureTheory Complex
open scoped ComplexConjugate
namespace F1Fecho.MaxwellLocalization
open TGLExt.ImportedSQ F1Fecho.MaxwellGlobal F1Fecho.OrbitalScreen
open ChatgptAudit.WignerRapidityMeasure016 F1Rede.FiberConjugation

theorem globalCoefficient_invert_real (f:SchwartzTensor) (hf:IsRealTest f)
    (p:MomentumCoordinates) :
    globalCoefficient (physicalFourierCLM (invertTest f)) p=
      fiberJ (globalCoefficient (physicalFourierCLM f) p) := by
  apply PiLp.ext
  intro j
  change (1/2:ℂ)*(∑μ,∑ν,(cartesianStrength p j μ ν:ℂ)*
    physicalFourierCLM (invertTest f) (shellEmbedding p) μ ν)=
      conj ((1/2:ℂ)*(∑μ,∑ν,(cartesianStrength p j μ ν:ℂ)*
        physicalFourierCLM f (shellEmbedding p) μ ν))
  simp only [physicalFourier_invert_real f hf,map_mul,map_sum,
    F1Fecho.ComplexNormalization.half_conj,conj_ofReal]

theorem circularSmear_invert_real (f:SchwartzTensor) (hf:IsRealTest f) :
    circularSmear (invertTest f)=Theta (circularSmear f) := by
  apply Lp.ext
  filter_upwards [circularSmear_ae (invertTest f),circularSmear_ae f,
    Theta_ae (circularSmear f)] with p hp hq ht
  rw [hp,ht,hq,globalCoefficient_invert_real f hf,circularFiber_symm_conjugation]

def inverseRegion (O:Set Spacetime) : Set Spacetime := (fun x:Spacetime=>-x) '' O

theorem inverted_generator (O:Set Spacetime) (v:H1) (hv:v∈supportedGenerators O) :
    Theta v∈supportedGenerators (inverseRegion O) := by
  obtain ⟨f,hr,hs,rfl⟩:=hv
  refine ⟨invertTest f,invertTest_real f hr,?_,circularSmear_invert_real f hr⟩
  rw [invertTest_support]
  exact Set.image_mono hs

def thetaReal : H1→L[ℝ]H1 where
  toFun := Theta
  map_add' := map_add Theta
  map_smul' r v := by
    change Theta ((r:ℂ) • v)=(r:ℂ) • Theta v
    rw [map_smulₛₗ]
    have h : (starRingEnd ℂ) (r:ℂ) = (r:ℂ) := Complex.conj_ofReal r
    rw [h]
  cont := Theta.continuous

theorem localized_inversion (O:Set Spacetime) (v:H1) (hv:v∈localized O) :
    Theta v∈localized (inverseRegion O) := by
  have hs:(Submodule.span ℝ (supportedGenerators O)).map thetaReal.toLinearMap≤
      Submodule.span ℝ (supportedGenerators (inverseRegion O)) := by
    rw [Submodule.map_span]
    apply Submodule.span_le.mpr
    rintro w ⟨x,hx,rfl⟩
    exact Submodule.subset_span (inverted_generator O x hx)
  exact (Submodule.topologicalClosure_mono hs)
    ((Submodule.topologicalClosure_map thetaReal _) (Submodule.mem_map.mpr ⟨v,hv,rfl⟩))

end F1Fecho.MaxwellLocalization
#print axioms F1Fecho.MaxwellLocalization.globalCoefficient_invert_real
#print axioms F1Fecho.MaxwellLocalization.circularSmear_invert_real
#print axioms F1Fecho.MaxwellLocalization.localized_inversion
