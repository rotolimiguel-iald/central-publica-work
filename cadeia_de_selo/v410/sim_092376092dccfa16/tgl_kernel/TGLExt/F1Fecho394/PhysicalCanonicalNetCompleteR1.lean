import TGLExt.F1Fecho394.PhysicalSymplecticPairingR7
import TGLExt.F1Fecho394.PhysicalFrameWedgeLocalityR2
import TGLExt.F1Fecho394.PhysicalCompactNetCovarianceR1
import TGLExt.F1Fecho394.PhysicalWedgeSchwartzClosureR3
import TGLExt.LightOneParticleByTerm
import TGLExt.F1Fecho394.GenericSymplecticSpanR2
import TGLExt.F1Fecho394.PhysicalCompactNetGeometryR1
import TGLExt.F1Fecho394.PhysicalCanonicalWedgeEqualityR3
import TGLExt.F1Fecho394.CanonicalFockAssemblyR1

/-! Additive composition of existing candidates. Fixes namespace and coordinate
elaboration only; no locality, standardness, or nonzero premise is added.
This constructs the free Maxwell net in Minkowski spacetime. It does not
construct a device reduction, curved H3, a trace, or a stress-energy charge. -/

/-! Causal commutation of actual compact Maxwell tests with strictly spacelike
topological supports. The finite cover is constructed from opposite physical
wedges; no global locality premise is used. Extension to the entire region
net remains a separate theorem. -/
set_option autoImplicit false
set_option maxHeartbeats 800000
noncomputable section
namespace F1Fecho.MaxwellLocalization
open F1Fecho.MaxwellGlobal F1Fecho.OrbitalScreen F1Fecho.SpacetimeLorentz
open TGL.SpecificAQFT F1Fecho.SpacelikeGeometry TGLExt.ImportedSQ F1Fecho.OrbitalSpatial

theorem physicalFrameRight_open (L : generatedLorentz) (a : Spacetime) :
    IsOpen (physicalFrameRegion L a physicalRightWedge) := by
  change IsOpen {x : Spacetime | |action L.val (x-a) 0| < action L.val (x-a) 1}
  exact isOpen_lt (by fun_prop) (by fun_prop)

theorem physicalFrameLeft_open (L : generatedLorentz) (a : Spacetime) :
    IsOpen (physicalFrameRegion L a physicalLeftWedge) := by
  change IsOpen {x : Spacetime | |action L.val (x-a) 0| < -action L.val (x-a) 1}
  exact isOpen_lt (by fun_prop) (by fun_prop)

theorem physical_frame_test_pair_zero (L : generatedLorentz) (a : Spacetime) :
    TestPairZero physicalTestPairing (physicalFrameRegion L a physicalRightWedge)
      (physicalFrameRegion L a physicalLeftWedge) := by
  intro f g hfr hgr hfs hgs
  exact physical_frame_opposite_symplectic L a (circularSmear f) (circularSmear g)
    ((Submodule.le_topologicalClosure _) (Submodule.subset_span ⟨f,hfr,hfs,rfl⟩))
    ((Submodule.le_topologicalClosure _) (Submodule.subset_span ⟨g,hgr,hgs,rfl⟩))

theorem physical_compact_spacelike_zero (f g : SchwartzTensor)
    (hfr : IsRealTest f) (hgr : IsRealTest g)
    (hfc : HasCompactSupport (f : Spacetime → TensorValue))
    (hgc : HasCompactSupport (g : Spacetime → TensorValue))
    (hsep : ∀ x ∈ tsupport (f : Spacetime → TensorValue),
      ∀ y ∈ tsupport (g : Spacetime → TensorValue),
      minkowskiSq (fun i => x i-y i) < 0) :
    (inner ℂ (circularSmear f) (circularSmear g)).im = 0 := by
  apply compact_pair_zero physicalTestPairing f g hfr hgr hfc hgc
  intro x y
  obtain ⟨L,m,hx,hy⟩ := spacelike_pair_opposite_wedges
    (fun i => x.val i) (fun i => y.val i) (hsep x.val x.property y.val y.property)
  let a : Spacetime := coordinateEquiv.symm m
  refine ⟨physicalFrameRegion L a physicalRightWedge,
    physicalFrameRegion L a physicalLeftWedge,physicalFrameRight_open L a,
    physicalFrameLeft_open L a,?_,?_,physical_frame_test_pair_zero L a⟩
  · exact hx
  · exact hy

end F1Fecho.MaxwellLocalization
#print axioms F1Fecho.MaxwellLocalization.physical_compact_spacelike_zero


/-! Comparison of the compact-test wedge with the original Schwartz-test
wedge. Cutoffs give compact support; a positive spatial shift moves its
closure into the open wedge. Strong continuity removes the shift. The
same smearing map and H1 are used throughout. -/
set_option autoImplicit false
set_option maxHeartbeats 1000000
noncomputable section
open Filter
open scoped Topology
namespace F1Fecho.MaxwellLocalization
open F1Fecho.MaxwellGlobal F1Fecho.SpacetimeLorentz TGLExt.ImportedSQ

def inwardWedgeShift (e : ℝ) : Spacetime := coordinateEquiv.symm (fun i => if i=1 then e else 0)

@[simp] theorem inwardWedgeShift_apply (e : ℝ) (i : Fin 4) :
    inwardWedgeShift e i = if i=1 then e else 0 := rfl

theorem inwardWedgeShift_zero : inwardWedgeShift 0=0 := by
  apply PiLp.ext
  intro i
  simp [inwardWedgeShift_apply]

theorem cutoff_wedge_support (s : ℝ) (f : SchwartzTensor)
    (hs : Function.support (f : Spacetime → TensorValue) ⊆ physicalRightWedge) :
    Function.support (SchwartzCutoff.cutoff s f : Spacetime → TensorValue) ⊆ physicalRightWedge := by
  intro x hx
  apply hs
  intro hz
  exact hx (by rw [SchwartzCutoff.cutoff_apply,hz,smul_zero])

theorem shifted_compact_wedge_tsupport (e : ℝ) (he : 0<e) (f : SchwartzTensor)
    (hs : Function.support (f : Spacetime → TensorValue) ⊆ physicalRightWedge) :
    tsupport (translateTest (inwardWedgeShift e) f : Spacetime → TensorValue) ⊆ physicalRightWedge := by
  have hclosed : IsClosed {x : Spacetime | |x 0| ≤ x 1} := isClosed_le (by fun_prop) (by fun_prop)
  have hts : tsupport (f : Spacetime → TensorValue) ⊆ {x : Spacetime | |x 0| ≤ x 1} :=
    closure_minimal (by
      intro x hx
      have h := hs hx
      change |x 0| < x 1 at h
      exact h.le) hclosed
  rw [translateTest_tsupport]
  intro x hx
  have hb := hts hx
  change |(x-inwardWedgeShift e) 0| ≤ (x-inwardWedgeShift e) 1 at hb
  have hzero : inwardWedgeShift e 0=0 := by simp [inwardWedgeShift_apply]
  have hone : inwardWedgeShift e 1=e := by simp [inwardWedgeShift_apply]
  simp only [PiLp.sub_apply,hzero,hone,sub_zero] at hb
  change |x 0|<x 1
  linarith

theorem shifted_wedge_smear_mem_compact (e : ℝ) (he : 0<e) (f : SchwartzTensor)
    (hr : IsRealTest f)
    (hs : Function.support (f : Spacetime → TensorValue) ⊆ physicalRightWedge) :
    U1 (fun i => inwardWedgeShift e i) (circularSmear f) ∈ compactLocalized physicalRightWedge := by
  have ht := (U1 (fun i => inwardWedgeShift e i)).continuous.continuousAt.tendsto.comp
    (circularSmear_continuous.continuousAt.tendsto.comp (SchwartzCutoff.cutoffSequence_tendsto f))
  apply (compactLocalized_closed physicalRightWedge).mem_of_tendsto ht
  apply Eventually.of_forall
  intro n
  let g := SchwartzCutoff.cutoffSequence f n
  have hgr : IsRealTest g := cutoff_real _ f hr
  have hgc : HasCompactSupport (g : Spacetime → TensorValue) :=
    SchwartzCutoff.cutoff_compact _ (by positivity) f
  have hgs : Function.support (g : Spacetime → TensorValue) ⊆ physicalRightWedge :=
    cutoff_wedge_support _ f hs
  exact (Submodule.le_topologicalClosure _) (Submodule.subset_span
    ⟨translateTest (inwardWedgeShift e) g,translateTest_real _ g hgr,
      translateTest_compact _ g hgc,shifted_compact_wedge_tsupport e he g hgs,
      circularSmear_translate _ g⟩)

theorem wedge_smear_mem_compact (f : SchwartzTensor) (hr : IsRealTest f)
    (hs : Function.support (f : Spacetime → TensorValue) ⊆ physicalRightWedge) :
    circularSmear f ∈ compactLocalized physicalRightWedge := by
  have ha : Tendsto (fun n : ℕ => fun i : Fin 4 => inwardWedgeShift (1/((n:ℝ)+1)) i)
      atTop (𝓝 (0 : Fin 4 → ℝ)) := by
    apply tendsto_pi_nhds.mpr
    intro i
    by_cases hi : i=1
    · simpa [inwardWedgeShift_apply,hi] using (tendsto_one_div_add_atTop_nhds_zero_nat (𝕜 := ℝ))
    · simpa [inwardWedgeShift_apply,hi] using (tendsto_const_nhds : Tendsto (fun _ : ℕ => (0 : ℝ)) atTop (𝓝 0))
  have ht := (TGLExt.LightByTerm.light_translations_strongly_continuous (circularSmear f)).continuousAt.tendsto.comp ha
  rw [U1_zero] at ht
  apply (compactLocalized_closed physicalRightWedge).mem_of_tendsto ht
  exact Eventually.of_forall (fun n => shifted_wedge_smear_mem_compact _ (by positivity) f hr hs)

theorem compactLocalized_rightWedge_eq :
    compactLocalized physicalRightWedge=localized physicalRightWedge := by
  apply le_antisymm (compactLocalized_le_localized _)
  apply Submodule.topologicalClosure_minimal _ _ (compactLocalized_closed _)
  apply Submodule.span_le.mpr
  rintro v ⟨f,hr,hs,rfl⟩
  exact wedge_smear_mem_compact f hr hs

end F1Fecho.MaxwellLocalization
#print axioms F1Fecho.MaxwellLocalization.shifted_compact_wedge_tsupport
#print axioms F1Fecho.MaxwellLocalization.wedge_smear_mem_compact
#print axioms F1Fecho.MaxwellLocalization.compactLocalized_rightWedge_eq


/-! Causal locality for the compact-test net on the same physical Maxwell H1.
All pairs of points in the two regions are strictly spacelike. The previous
all-Schwartz net is not identified with this net by definition. -/
set_option autoImplicit false
set_option maxHeartbeats 800000
noncomputable section
namespace F1Fecho.MaxwellLocalization
open F1Fecho.MaxwellGlobal TGLExt.ImportedSQ TGL.SpecificAQFT

theorem compactLocalized_locality (O P : Set Spacetime)
    (hsep : ∀ x ∈ O, ∀ y ∈ P, minkowskiSq (fun i => x i-y i)<0)
    (u v : H1) (hu : u ∈ compactLocalized O) (hv : v ∈ compactLocalized P) :
    (inner ℂ u v).im=0 := by
  apply GenericSymplecticSpan.closed_spans_zero
    (compactSupportedGenerators O) (compactSupportedGenerators P) ?_ u v hu hv
  rintro x ⟨f,hfr,hfc,hfs,rfl⟩ y ⟨g,hgr,hgc,hgs,rfl⟩
  exact physical_compact_spacelike_zero f g hfr hgr hfc hgc
    (fun x hx y hy => hsep x (hfs hx) y (hgs hy))

end F1Fecho.MaxwellLocalization
#print axioms F1Fecho.MaxwellLocalization.compactLocalized_locality


/-! A concrete global Maxwell LightNetData and its exact nonzero canonical
wedge on the SAME H1. The compact-test net is compared to the prior physical
Schwartz wedge by a theorem, never by renaming. Other Fock, trace and Maxwell
charge certificates are separate obligations and are not fabricated here. -/
set_option autoImplicit false
set_option maxHeartbeats 1200000
noncomputable section
namespace F1Fecho.MaxwellLocalization
open F1Fecho.MaxwellGlobal TGLExt.ImportedSQ TGL.SpecificAQFT
open F1Fecho.NetworkReuse F1Rede.CanonicalWedge

theorem compactPhysicalNet_local (O P : Set (Fin 4 → ℝ)) (hsep : SpacelikeSep O P) :
    ∀ f ∈ compactPhysicalNet O, ∀ g ∈ compactPhysicalNet P, (inner ℂ f g).im=0 := by
  intro f hf g hg
  exact compactLocalized_locality (coordinateRegion O) (coordinateRegion P)
    (fun x hx y hy => hsep (fun i => x i) hx (fun i => y i) hy) f g hf hg

theorem compactPhysicalNet_wedge_glue :
    compactPhysicalNet rightWedge=KWR.toClosedSubmodule.toSubmodule :=
  compactPhysicalNet_rightWedge.trans
    (compactLocalized_rightWedge_eq.trans physical_right_wedge_eq_KWR)

def physicalCanonicalNet : CanonicalNetInput where
  toLightNetData :=
    { helicity := 1
      helicity_light := Or.inl rfl
      K := compactPhysicalNet
      K_mono := compactPhysicalNet_mono
      K_local := compactPhysicalNet_local
      K_translate := compactPhysicalNet_translate
      K_boost := compactPhysicalNet_boost }
  wedge_glue := compactPhysicalNet_wedge_glue

theorem physical_light_net_inhabited : Nonempty TGLExt.QGSolution.LightNetData :=
  ⟨physicalCanonicalNet.toLightNetData⟩

theorem physical_canonical_net_nonzero :
    ∃ v : H1, v ∈ physicalCanonicalNet.K rightWedge ∧ v≠0 :=
  canonical_wedge_nonzero physicalCanonicalNet

theorem physical_canonical_net_zero_refused : physicalCanonicalNet.K rightWedge≠⊥ :=
  zero_wedge_refused physicalCanonicalNet

end F1Fecho.MaxwellLocalization
#print axioms F1Fecho.MaxwellLocalization.compactPhysicalNet_local
#print axioms F1Fecho.MaxwellLocalization.compactPhysicalNet_wedge_glue
#print axioms F1Fecho.MaxwellLocalization.physicalCanonicalNet
#print axioms F1Fecho.MaxwellLocalization.physical_light_net_inhabited
#print axioms F1Fecho.MaxwellLocalization.physical_canonical_net_nonzero
#print axioms F1Fecho.MaxwellLocalization.physical_canonical_net_zero_refused
