import TGLExt.F1Fecho394.CanonicalOutput
import TGLExt.F1Fecho394.FieldWeylR3
/-! Boost invariance of the ALREADY constructed canonical standard subspace.
The spectral multiplier and conjugation are reused. No global localization net
is invented: this proves the one-wedge flow restriction directly. -/
set_option autoImplicit false
set_option maxHeartbeats 1500000
noncomputable section
open MeasureTheory Filter
namespace F1Fecho.CanonicalWedgeFlow
open TGLExt.ImportedSQ F1Rede.CanonicalWedge F1Rede.Canonical
open F1Rede.FiberConjugation ChatgptAudit.Continuous050 TGLV350.Regular

 theorem phase_reflection (s x : ℝ) : star (characterPhase s (-x)) = characterPhase s x := by
  simp only [characterPhase, Complex.star_def, ← Complex.exp_conj]
  congr 1
  simp

theorem Js_character (s : ℝ) (f : RH) :
    Js (characterMultiplier s f) = characterMultiplier s (Js f) := by
  apply Lp.ext
  have hr := (Measure.measurePreserving_neg (volume : Measure ℝ)).quasiMeasurePreserving.ae
    (characterMultiplier_ae s f)
  filter_upwards [F1Rede.SpectralConjugation.J_ae transverseGeometricJ transverseGeometricJ_involutive
      (characterMultiplier s f), characterMultiplier_ae s (Js f),
    F1Rede.SpectralConjugation.J_ae transverseGeometricJ transverseGeometricJ_involutive f,hr]
    with x hj hc hf hrx
  change (Js (characterMultiplier s f)) x = _ at hj
  change (Js f) x = _ at hf
  rw [hj,hc,hf,hrx,map_smulₛₗ]
  simp only [starRingEnd_apply]
  change star (characterPhase s (-x)) • _ = characterPhase s x • _
  rw [phase_reflection]

theorem Jcandidate_boost (s : ℝ) (f : H1) : Jcandidate (B0 s f) = B0 s (Jcandidate f) := by
  apply Phi.injective
  simp only [Jcandidate_apply, LinearIsometryEquiv.apply_symm_apply,canonicalPartialFourier_boost]
  exact Js_character (2*Real.pi*s) (Phi f)

theorem TW_graph_boost (s : ℝ) (f g : H1) (h : (f,g) ∈ TW.graph) :
    (B0 s f,B0 s g) ∈ TW.graph := by
  apply (TW_multiplier _ _).mpr
  have hh := (TW_multiplier f g).mp h
  simp only [canonicalPartialFourier_boost]
  filter_upwards [characterMultiplier_ae (2*Real.pi*s) (Phi g),
    characterMultiplier_ae (2*Real.pi*s) (Phi f),hh] with x hg hf hfg
  rw [hg,hf,hfg]
  simp only [smul_smul,mul_comm]

theorem boost_mem_KWR (s : ℝ) (f : H1) (hf : f ∈ KWR.toClosedSubmodule) :
    B0 s f ∈ KWR.toClosedSubmodule := by
  obtain ⟨hd,hfix⟩ := (KWR_mem f).mp hf
  have hg := TW_graph_boost s f (TW ⟨f,hd⟩) (TW.mem_graph ⟨f,hd⟩)
  have hd' := LinearPMap.mem_domain_of_mem_graph hg
  have hv : TW ⟨B0 s f,hd'⟩ = B0 s (TW ⟨f,hd⟩) :=
    TW.mem_graph_snd_inj (TW.mem_graph ⟨B0 s f,hd'⟩) hg rfl
  apply (KWR_mem (B0 s f)).mpr
  refine ⟨hd',?_⟩
  change Jcandidate (TW ⟨B0 s f,hd'⟩) = B0 s f
  change Jcandidate (TW ⟨f,hd⟩) = f at hfix
  rw [hv,Jcandidate_boost,hfix]

theorem boost_mem_KWR_iff (s : ℝ) (f : H1) :
    f ∈ KWR.toClosedSubmodule ↔ B0 s f ∈ KWR.toClosedSubmodule := by
  constructor
  · exact boost_mem_KWR s f
  · intro hf
    have h := boost_mem_KWR (-s) (B0 s f) hf
    have hi : B0 (-s) (B0 s f) = f := by
      have hh := congrArg (fun u : H1 ≃ₗᵢ[ℂ] H1 => u f) (B0_add (-s) s)
      change (B0 (-s)) ((B0 s) f) = _
      have hz := hh.symm
      simp only [neg_add_cancel,B0_zero,LinearIsometryEquiv.trans_apply] at hz
      exact hz
    simpa only [hi] using h

def M : VonNeumannAlgebra F1Rede.BosonicFock.F := FieldWeyl.R KWR.toClosedSubmodule.toSubmodule

theorem boostAd_preserves (t : ℝ) (x : F1Rede.BosonicFock.F →L[ℂ] F1Rede.BosonicFock.F) :
    x ∈ M ↔ WeylFlow.boostAd t x ∈ M :=
  FieldWeyl.R_covariance (B0 (-(2*Real.pi*t))) _ _ (boost_mem_KWR_iff (-(2*Real.pi*t))) x

def flow (t : ℝ) : M.toStarSubalgebra ≃⋆ₐ[ℂ] M.toStarSubalgebra :=
  WeylFlow.restrictAutomorphism M (WeylFlow.boostAd t) (boostAd_preserves t)

theorem flow_is_Ad (t : ℝ) (a : M.toStarSubalgebra) :
    ((flow t) a).val = WeylFlow.boostAd t a.val := rfl

theorem flow_zero : flow 0 = StarAlgEquiv.refl := by
  apply StarAlgEquiv.ext
  intro a
  apply Subtype.ext
  change WeylFlow.boostAd 0 a.val = a.val
  rw [WeylFlow.boostAd_zero]
  rfl

theorem flow_add (s t : ℝ) : flow (s+t) = (flow s).trans (flow t) := by
  apply StarAlgEquiv.ext
  intro a
  apply Subtype.ext
  change WeylFlow.boostAd (s+t) a.val = WeylFlow.boostAd t (WeylFlow.boostAd s a.val)
  rw [WeylFlow.boostAd_add]
  rfl

end F1Fecho.CanonicalWedgeFlow
#print axioms F1Fecho.CanonicalWedgeFlow.Jcandidate_boost
#print axioms F1Fecho.CanonicalWedgeFlow.TW_graph_boost
#print axioms F1Fecho.CanonicalWedgeFlow.boost_mem_KWR_iff
#print axioms F1Fecho.CanonicalWedgeFlow.flow
#print axioms F1Fecho.CanonicalWedgeFlow.flow_add
