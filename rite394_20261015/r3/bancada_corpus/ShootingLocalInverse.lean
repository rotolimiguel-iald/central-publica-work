import SmoothFlowControls
import Mathlib.Analysis.Calculus.InverseFunctionTheorem.ContDiff
import Mathlib.Topology.OpenPartialHomeomorph.IsImage

set_option autoImplicit false
set_option maxHeartbeats 5000000
namespace ChatgptAudit.Flow018
open Filter Topology Set
open scoped ContDiff
noncomputable section
variable {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E] [CompleteSpace E]

structure SmoothLocalChart (X : E → E) (D : Set E) (a : E) where
  chart : OpenPartialHomeomorph E E
  map_eq : (chart : E → E)=X
  source_subset : chart.source ⊆ D
  base_mem : a∈chart.source
  inverse_smooth : ContDiffOn ℝ ∞ chart.symm chart.target

def smoothLocalChart (X : E → E) (D : Set E) (hD : IsOpen D)
    (hf : ContDiffOn ℝ ∞ X D) (a : E) (ha : a∈D)
    (hd : HasFDerivAt X (ContinuousLinearMap.id ℝ E) a) : SmoothLocalChart X D a := by
  have hfa : ContDiffAt ℝ ∞ X a := (hf a ha).contDiffAt (hD.mem_nhds ha)
  have hu0 : IsUnit (fderiv ℝ X a) := by
    rw [hd.fderiv]
    exact isUnit_one
  have hunits : ∀ᶠ z in 𝓝 a, IsUnit (fderiv ℝ X z) :=
    (hfa.continuousAt_fderiv (by simp)).eventually (Units.isOpen.mem_nhds hu0)
  let S := interior (D ∩ {z | IsUnit (fderiv ℝ X z)})
  have haS : a∈S := by
    apply mem_interior_iff_mem_nhds.2
    filter_upwards [hD.mem_nhds ha,hunits] with z hz hu
    exact ⟨hz,hu⟩
  let e := hfa.toOpenPartialHomeomorph X (f' := ContinuousLinearEquiv.refl ℝ E) hd (by simp)
  let k := e.restrOpen S isOpen_interior
  have haE : a∈e.source :=
    hfa.mem_toOpenPartialHomeomorph_source (f' := ContinuousLinearEquiv.refl ℝ E) hd (by simp)
  refine {
    chart := k
    map_eq := rfl
    source_subset := ?_
    base_mem := ⟨haE,haS⟩
    inverse_smooth := ?_ }
  · intro z hz
    exact (interior_subset hz.2).1
  · intro y hy
    let z := k.symm y
    have hz : z∈k.source := k.map_target hy
    have hzD : z∈D := (interior_subset hz.2).1
    have hzu : IsUnit (fderiv ℝ X z) := (interior_subset hz.2).2
    obtain ⟨u,hu⟩ := hzu
    let eD : E ≃L[ℝ] E := ContinuousLinearEquiv.ofUnit u
    have hXz : ContDiffAt ℝ ∞ X z := (hf z hzD).contDiffAt (hD.mem_nhds hzD)
    have hdz : HasFDerivAt (k : E → E) (eD : E →L[ℝ] E) z := by
      change HasFDerivAt X (u : E →L[ℝ] E) z
      rw [hu]
      exact (hXz.differentiableAt (by simp)).hasFDerivAt
    exact (k.contDiffAt_symm (f₀' := eD) hy hdz hXz).contDiffWithinAt

#print axioms smoothLocalChart
end
end ChatgptAudit.Flow018
