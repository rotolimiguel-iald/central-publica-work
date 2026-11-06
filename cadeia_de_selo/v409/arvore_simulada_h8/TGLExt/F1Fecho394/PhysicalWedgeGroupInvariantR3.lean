import TGLExt.F1Fecho394.RegularSemigroupClosureR3
import TGLExt.F1Fecho394.PhysicalWedgeNullGeometryR3

/-! Actual group invariance of the closed complex span of wedge-localized
Maxwell tests. The real localized space itself is not claimed invariant under
outward translations. The two null groups together supply spatial shifts. -/
set_option autoImplicit false
set_option maxHeartbeats 1600000
noncomputable section
open scoped InnerProductSpace
namespace F1Fecho.MaxwellLocalization
open TGLExt.ImportedSQ F1Fecho.MaxwellGlobal F1Fecho.RegularCoefficient

def complexWedge : Submodule ℂ H1 := complexClosure (supportedGenerators physicalRightWedge)

theorem generator_regular (ψ:H1) (hψ:ψ∈supportedGenerators physicalRightWedge) :
    EnergySquareProfile ψ := by
  obtain ⟨f,hr,hs,rfl⟩:=hψ
  exact circularSmear_energySquare f

theorem complexWedge_nullPlus (t:ℝ) (v:H1) (hv:v∈complexWedge) :
    U1 (t • nullPlus) v∈complexWedge := by
  apply group_mem_of_semiray _ nullPlus nullPlus_future nullPlus_energy_bound generator_regular true
    (fun ψ hψ s hs=>?_) t v hv
  exact (Submodule.le_topologicalClosure _) (Submodule.subset_span (nullPlus_generator s hs.le ψ hψ))

theorem complexWedge_nullMinus (t:ℝ) (v:H1) (hv:v∈complexWedge) :
    U1 (t • nullMinus) v∈complexWedge := by
  apply group_mem_of_semiray _ nullMinus nullMinus_future nullMinus_energy_bound generator_regular false
    (fun ψ hψ s hs=>?_) t v hv
  exact (Submodule.le_topologicalClosure _) (Submodule.subset_span (nullMinus_generator s hs.le ψ hψ))

def spatialDirection : Fin 4→ℝ := ![0,1,0,0]

theorem spatial_split (t:ℝ) : t • spatialDirection=(t/2) • nullPlus+(-t/2) • nullMinus := by
  funext i
  fin_cases i <;> simp [spatialDirection,nullPlus,nullMinus] <;> ring

theorem complexWedge_spatial (t:ℝ) (v:H1) (hv:v∈complexWedge) :
    U1 (t • spatialDirection) v∈complexWedge := by
  rw [spatial_split,U1_add]
  exact complexWedge_nullPlus (t/2) _ (complexWedge_nullMinus (-t/2) v hv)

theorem real_smear_mem_of_bounded_support (f:SchwartzTensor) (hr:IsRealTest f)
    (r:ℝ) (hs:∀x,x∈Function.support (f:Spacetime→TensorValue)→‖x‖≤r) :
    circularSmear f∈complexWedge := by
  let t:ℝ:=2*r+1
  let a:Spacetime:=WithLp.toLp 2 (t • spatialDirection)
  have hsupport:Function.support (translateTest a f:Spacetime→TensorValue)⊆physicalRightWedge := by
    intro x hx
    have hb:=hs (x-a) hx
    have h0: |(x-a) 0|≤r := (PiLp.norm_apply_le (x-a) 0).trans hb
    have h1: |(x-a) 1|≤r := (PiLp.norm_apply_le (x-a) 1).trans hb
    change |x 0|<x 1
    have h0a:|x 0|≤r := by simpa [a,spatialDirection] using h0
    have h1a:|x 1-t|≤r := by simpa [a,spatialDirection] using h1
    have h1':= (abs_le.mp h1a).1
    dsimp [t] at h1'
    linarith
  have hg:circularSmear (translateTest a f)∈complexWedge :=
    (Submodule.le_topologicalClosure _) (Submodule.subset_span
      ⟨translateTest a f,translateTest_real a f hr,hsupport,rfl⟩)
  have hback:=complexWedge_spatial (-t) _ hg
  rw [circularSmear_translate] at hback
  have ha:(fun i=>a i)=t • spatialDirection := rfl
  rw [ha] at hback
  have hi:U1 ((-t) • spatialDirection) (U1 (t • spatialDirection) (circularSmear f))=circularSmear f := by
    have hh:=congrArg (fun u:H1≃ₗᵢ[ℂ]H1=>u (circularSmear f))
      (U1_add ((-t) • spatialDirection) (t • spatialDirection))
    have hz:(-t) • spatialDirection+t • spatialDirection=0 := by rw [←add_smul];simp
    rw [hz,U1_zero] at hh
    exact hh.symm
  rwa [hi] at hback

end F1Fecho.MaxwellLocalization
#print axioms F1Fecho.MaxwellLocalization.complexWedge_nullPlus
#print axioms F1Fecho.MaxwellLocalization.complexWedge_nullMinus
#print axioms F1Fecho.MaxwellLocalization.complexWedge_spatial
#print axioms F1Fecho.MaxwellLocalization.real_smear_mem_of_bounded_support
