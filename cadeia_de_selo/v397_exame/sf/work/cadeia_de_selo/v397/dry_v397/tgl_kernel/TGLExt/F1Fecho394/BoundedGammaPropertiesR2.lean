import TGLExt.F1Fecho394.BoundedBosonicGammaR2
import TGLExt.F1Fecho394.ConcreteWeylContinuityR2
/-! Functorial, adjoint and density properties of the constructed bounded
second quantization on the unchanged canonical Fock. -/
set_option autoImplicit false
set_option maxHeartbeats 1600000
noncomputable section
open scoped InnerProductSpace
namespace F1Fecho.BoundedGamma
open TGLExt.ImportedSQ F1Rede.BosonicFock F1Fecho.Exponential

theorem gamma_commute (A B : H1 →L[ℂ] H1) (hA : ‖A‖ ≤ 1) (hB : ‖B‖ ≤ 1)
    (hc : A * B = B * A) : gamma A hA * gamma B hB = gamma B hB * gamma A hA := by
  apply WeylConstruction.clm_ext_total exponential exponential_total
  intro f
  simp only [ContinuousLinearMap.mul_apply,gamma_exponential]
  exact congrArg exponential (congrArg (fun L : H1 →L[ℂ] H1 => L f) hc)

theorem gamma_selfadjoint (A : H1 →L[ℂ] H1) (hA : ‖A‖ ≤ 1)
    (hs : IsSelfAdjoint A) : IsSelfAdjoint (gamma A hA) := by
  apply ContinuousLinearMap.isSelfAdjoint_iff'.mpr
  apply WeylConstruction.clm_ext_total exponential exponential_total
  intro f
  apply sub_eq_zero.mp
  apply exponential_orthogonal_zero
  intro g
  rw [inner_sub_left,ContinuousLinearMap.adjoint_inner_left,
    gamma_exponential,gamma_exponential,exponential_inner,exponential_inner]
  have hi : inner ℂ (A f) g = inner ℂ f (A g) := hs.isSymmetric f g
  rw [hi,sub_self]

theorem gamma_denseRange (A : H1 →L[ℂ] H1) (hA : ‖A‖ ≤ 1)
    (hd : DenseRange A) : DenseRange (gamma A hA) := by
  let M := (gamma A hA).range.topologicalClosure
  have he (f : H1) : exponential f ∈ M := by
    refine hd.induction_on f ((gamma A hA).range.isClosed_topologicalClosure.preimage
      ConcreteWeyl.exponential_continuous) ?_
    intro g
    apply (gamma A hA).range.le_topologicalClosure
    exact ⟨exponential g,gamma_exponential A hA g⟩
  have hs : Submodule.span ℂ (Set.range exponential) ≤ M := by
    apply Submodule.span_le.mpr
    rintro _ ⟨f,rfl⟩
    exact he f
  have ht := (Submodule.span ℂ (Set.range exponential)).topologicalClosure_minimal hs
    (gamma A hA).range.isClosed_topologicalClosure
  rw [exponential_total] at ht
  have hc : (gamma A hA).range.topologicalClosure = ⊤ := le_antisymm le_top ht
  exact Submodule.dense_iff_topologicalClosure_eq_top.mpr hc

theorem gamma_injective (A : H1 →L[ℂ] H1) (hA : ‖A‖ ≤ 1)
    (hs : IsSelfAdjoint A) (hd : DenseRange A) : Function.Injective (gamma A hA) := by
  apply LinearMap.ker_eq_bot.mp
  have hd' : Dense ((gamma A hA).range : Set F) := gamma_denseRange A hA hd
  have hc := Submodule.dense_iff_topologicalClosure_eq_top.mp hd'
  have ho := Submodule.topologicalClosure_eq_top_iff.mp hc
  rw [ContinuousLinearMap.orthogonal_range,(gamma_selfadjoint A hA hs).adjoint_eq] at ho
  exact ho

end F1Fecho.BoundedGamma
#print axioms F1Fecho.BoundedGamma.gamma_commute
#print axioms F1Fecho.BoundedGamma.gamma_selfadjoint
#print axioms F1Fecho.BoundedGamma.gamma_denseRange
#print axioms F1Fecho.BoundedGamma.gamma_injective
