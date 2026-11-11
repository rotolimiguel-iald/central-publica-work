import TGLExt.F1Fecho394.PhysicalSmearLorentzR3
import Mathlib.Topology.Algebra.Support

/-! The compact-test Maxwell region net on the SAME H1 and smearing map.
It is kept distinct from the earlier all-Schwartz-support net. This module
proves isotony and covariance only. Its right-wedge equality and causal
locality require their own consumers; neither is supplied as an input here. -/
set_option autoImplicit false
set_option maxHeartbeats 800000
noncomputable section
namespace F1Fecho.MaxwellLocalization
open F1Fecho.MaxwellGlobal TGLExt.ImportedSQ F1Fecho.OrbitalScreen
open F1Fecho.OrbitalSpatial F1Fecho.SpacetimeLorentz F1Fecho.PhysicalTensorLorentz

def compactSupportedGenerators (O : Set Spacetime) : Set H1 :=
  {v | ∃ f : SchwartzTensor, IsRealTest f ∧
    HasCompactSupport (f : Spacetime → TensorValue) ∧
    tsupport (f : Spacetime → TensorValue) ⊆ O ∧ circularSmear f=v}

def compactLocalized (O : Set Spacetime) : Submodule ℝ H1 :=
  (Submodule.span ℝ (compactSupportedGenerators O)).topologicalClosure

theorem compactLocalized_closed (O : Set Spacetime) :
    IsClosed (compactLocalized O : Set H1) := Submodule.isClosed_topologicalClosure _

theorem compactLocalized_mono {O P : Set Spacetime} (h : O ⊆ P) :
    compactLocalized O ≤ compactLocalized P := by
  apply Submodule.topologicalClosure_mono
  apply Submodule.span_mono
  rintro v ⟨f,hr,hc,hs,hv⟩
  exact ⟨f,hr,hc,hs.trans h,hv⟩

theorem compactLocalized_le_localized (O : Set Spacetime) :
    compactLocalized O ≤ localized O := by
  apply Submodule.topologicalClosure_mono
  apply Submodule.span_mono
  rintro v ⟨f,hr,hc,hs,hv⟩
  exact ⟨f,hr,(subset_tsupport _).trans hs,hv⟩

def testSubtractHomeomorph (a : Spacetime) : Spacetime ≃ₜ Spacetime where
  toFun x := x-a
  invFun x := x+a
  left_inv x := sub_add_cancel x a
  right_inv x := add_sub_cancel_right x a
  continuous_toFun := continuous_id.sub continuous_const
  continuous_invFun := continuous_id.add continuous_const

theorem translateTest_compact (a : Spacetime) (f : SchwartzTensor)
    (hc : HasCompactSupport (f : Spacetime → TensorValue)) :
    HasCompactSupport (translateTest a f : Spacetime → TensorValue) :=
  hc.comp_homeomorph (testSubtractHomeomorph a)

theorem translateTest_tsupport (a : Spacetime) (f : SchwartzTensor) :
    tsupport (translateTest a f : Spacetime → TensorValue) =
      translateRegion a (tsupport (f : Spacetime → TensorValue)) :=
  tsupport_comp_eq_preimage (f : Spacetime → TensorValue) (testSubtractHomeomorph a)

theorem compact_translated_generator (a : Spacetime) (O : Set Spacetime) (v : H1)
    (hv : v ∈ compactSupportedGenerators O) :
    U1 (fun i => a i) v ∈ compactSupportedGenerators (translateRegion a O) := by
  obtain ⟨f,hr,hc,hs,rfl⟩ := hv
  refine ⟨translateTest a f,translateTest_real a f hr,translateTest_compact a f hc,
    ?_,circularSmear_translate a f⟩
  rw [translateTest_tsupport]
  intro x hx
  exact hs hx

theorem compactLocalized_translate (a : Spacetime) (O : Set Spacetime) (v : H1)
    (hv : v ∈ compactLocalized O) :
    U1 (fun i => a i) v ∈ compactLocalized (translateRegion a O) := by
  let T : H1 →L[ℝ] H1 :=
    (U1 (fun i => a i)).toLinearIsometry.toContinuousLinearMap.restrictScalars ℝ
  have hs : (Submodule.span ℝ (compactSupportedGenerators O)).map T.toLinearMap ≤
      Submodule.span ℝ (compactSupportedGenerators (translateRegion a O)) := by
    rw [Submodule.map_span]
    apply Submodule.span_le.mpr
    rintro w ⟨x,hx,rfl⟩
    exact Submodule.subset_span (compact_translated_generator a O x hx)
  exact (Submodule.topologicalClosure_mono hs)
    ((Submodule.topologicalClosure_map T _) (Submodule.mem_map.mpr ⟨v,hv,rfl⟩))

theorem compactLocalized_translate_iff (a : Spacetime) (O : Set Spacetime) (v : H1) :
    v ∈ compactLocalized O ↔ U1 (fun i => a i) v ∈ compactLocalized (translateRegion a O) := by
  constructor
  · exact compactLocalized_translate a O v
  · intro hv
    have h := compactLocalized_translate (-a) (translateRegion a O) (U1 (fun i => a i) v) hv
    rw [translateRegion_inverse] at h
    have hi : U1 (fun i => (-a) i) (U1 (fun i => a i) v)=v := by
      have hh := congrArg (fun u : H1 ≃ₗᵢ[ℂ] H1 => u v)
        (U1_add (fun i => (-a) i) (fun i => a i))
      have hz : (fun i => (-a) i)+(fun i => a i)=(0 : Fin 4 → ℝ) := by funext i; simp
      rw [hz,U1_zero] at hh
      exact hh.symm
    rwa [hi] at h

theorem transform_tsupport (L : TGLExt.LorentzGrp) (f : SchwartzTensor) :
    tsupport (transform L f : Spacetime → TensorValue) ⊆
      action L '' tsupport (f : Spacetime → TensorValue) := by
  apply closure_minimal
  · exact (transform_support L f).trans (Set.image_mono (subset_tsupport _))
  · exact (action L).toHomeomorph.isClosedMap _ isClosed_closure

theorem transform_compact (L : TGLExt.LorentzGrp) (f : SchwartzTensor)
    (hc : HasCompactSupport (f : Spacetime → TensorValue)) :
    HasCompactSupport (transform L f : Spacetime → TensorValue) :=
  (hc.image (action L).continuous).of_isClosed_subset isClosed_closure (transform_tsupport L f)

theorem compact_lorentz_generator (L : generatedLorentz) (O : Set Spacetime) (v : H1)
    (hv : v ∈ compactSupportedGenerators O) :
    helicityUnitary L v ∈ compactSupportedGenerators (lorentzRegion L O) := by
  obtain ⟨f,hr,hc,hs,rfl⟩ := hv
  exact ⟨transform L.val f,transform_real _ f hr,transform_compact _ f hc,
    (transform_tsupport _ f).trans (Set.image_mono hs),circularSmear_lorentz L f⟩

theorem compactLocalized_lorentz (L : generatedLorentz) (O : Set Spacetime) (v : H1)
    (hv : v ∈ compactLocalized O) :
    helicityUnitary L v ∈ compactLocalized (lorentzRegion L O) := by
  let T : H1 →L[ℝ] H1 :=
    (helicityUnitary L).toLinearIsometry.toContinuousLinearMap.restrictScalars ℝ
  have hs : (Submodule.span ℝ (compactSupportedGenerators O)).map T.toLinearMap ≤
      Submodule.span ℝ (compactSupportedGenerators (lorentzRegion L O)) := by
    rw [Submodule.map_span]
    apply Submodule.span_le.mpr
    rintro w ⟨x,hx,rfl⟩
    exact Submodule.subset_span (compact_lorentz_generator L O x hx)
  exact (Submodule.topologicalClosure_mono hs)
    ((Submodule.topologicalClosure_map T _) (Submodule.mem_map.mpr ⟨v,hv,rfl⟩))

theorem compactLocalized_lorentz_iff (L : generatedLorentz) (O : Set Spacetime) (v : H1) :
    v ∈ compactLocalized O ↔ helicityUnitary L v ∈ compactLocalized (lorentzRegion L O) := by
  constructor
  · exact compactLocalized_lorentz L O v
  · intro hv
    have h := compactLocalized_lorentz L⁻¹ (lorentzRegion L O) (helicityUnitary L v) hv
    rw [lorentzRegion_inverse,←helicityUnitary_mul,inv_mul_cancel,helicityUnitary_one] at h
    exact h

end F1Fecho.MaxwellLocalization
#print axioms F1Fecho.MaxwellLocalization.compactLocalized_mono
#print axioms F1Fecho.MaxwellLocalization.compactLocalized_le_localized
#print axioms F1Fecho.MaxwellLocalization.compactLocalized_translate_iff
#print axioms F1Fecho.MaxwellLocalization.compactLocalized_lorentz_iff
