import TGLExt.F1Fecho394.PhysicalWedgeGroupInvariantR3
import TGLExt.F1Fecho394.SchwartzCompactDensityR3

/-! Passage from compact real tests to arbitrary real and complex Schwartz
tests inside the closed complex span of the physical right-wedge subspace.
Global totality of Maxwell smearing is an additional, separate obligation. -/
set_option autoImplicit false
set_option maxHeartbeats 1600000
noncomputable section
open Filter
open scoped Topology
namespace F1Fecho.MaxwellLocalization
open TGLExt.ImportedSQ F1Fecho.MaxwellGlobal F1Fecho.OrbitalScreen
open F1Fecho.RegularCoefficient

theorem real_smear_mem_of_compact_support (f:SchwartzTensor) (hr:IsRealTest f)
    (hc:HasCompactSupport (f:Spacetime→TensorValue)) : circularSmear f∈complexWedge := by
  obtain ⟨r,hrb⟩:=hc.isBounded.exists_norm_le
  exact real_smear_mem_of_bounded_support f hr r
    (fun x hx=>hrb x (subset_tsupport (f:Spacetime→TensorValue) hx))

theorem cutoff_real (s:ℝ) (f:SchwartzTensor) (hr:IsRealTest f) :
    IsRealTest (SchwartzCutoff.cutoff s f) := by
  intro x μ ν
  rw [SchwartzCutoff.cutoff_apply]
  change ((SchwartzCutoff.bump (s • x):ℝ) • (f x μ ν)).im=0
  simp [Complex.real_smul,hr x μ ν]

theorem circularSmear_continuous : Continuous circularSmear :=
  circularH1.symm.continuous.comp physicalSmearCLM.continuous

theorem all_real_smears_mem_complexWedge (f:SchwartzTensor) (hr:IsRealTest f) :
    circularSmear f∈complexWedge := by
  apply (Submodule.isClosed_topologicalClosure _).mem_of_tendsto
    (circularSmear_continuous.continuousAt.tendsto.comp (SchwartzCutoff.cutoffSequence_tendsto f))
  apply Eventually.of_forall
  intro n
  exact real_smear_mem_of_compact_support _ (cutoff_real _ f hr)
    (SchwartzCutoff.cutoff_compact _ (by positivity) f)

theorem all_smears_mem_complexWedge (f:SchwartzTensor) : circularSmear f∈complexWedge := by
  have hd:=congrArg circularSmear (real_imag_decomposition f)
  have hadd: circularSmear (realPart f+Complex.I • imagPart f)=
      circularSmear (realPart f)+Complex.I • circularSmear (imagPart f) := by
    simp only [circularSmear,map_add,map_smul]
  rw [hd,hadd]
  exact complexWedge.add_mem (all_real_smears_mem_complexWedge _ (realPart_real f))
    (complexWedge.smul_mem _ (all_real_smears_mem_complexWedge _ (imagPart_real f)))

theorem complexWedge_eq_top_of_global_density
    (hd:DenseRange circularSmear) : complexWedge=⊤ := by
  apply top_unique
  intro v hv
  exact (Submodule.isClosed_topologicalClosure _).closure_subset_iff.mpr
    (by rintro w ⟨f,rfl⟩;exact all_smears_mem_complexWedge f) (hd v)

theorem localized_complex_dense_of_global_density
    (hd:DenseRange circularSmear) :
    (Submodule.span ℂ (localized physicalRightWedge:Set H1)).topologicalClosure=⊤ := by
  have h:(complexWedge:Submodule ℂ H1)≤
      (Submodule.span ℂ (localized physicalRightWedge:Set H1)).topologicalClosure := by
    apply Submodule.topologicalClosure_mono
    apply Submodule.span_le.mpr
    intro ψ hψ
    exact Submodule.subset_span ((Submodule.le_topologicalClosure _) (Submodule.subset_span hψ))
  rw [complexWedge_eq_top_of_global_density hd] at h
  exact top_unique h

end F1Fecho.MaxwellLocalization
#print axioms F1Fecho.MaxwellLocalization.all_real_smears_mem_complexWedge
#print axioms F1Fecho.MaxwellLocalization.all_smears_mem_complexWedge
#print axioms F1Fecho.MaxwellLocalization.localized_complex_dense_of_global_density
