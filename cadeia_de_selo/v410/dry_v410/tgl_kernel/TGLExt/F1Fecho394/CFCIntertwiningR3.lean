import TGLExt.F1Fecho394.ContinuousHomIntertwiningR2
import Mathlib.Analysis.CStarAlgebra.ContinuousLinearMap
/-! Continuous functional calculus respects bounded intertwiners between
selfadjoint operators on possibly different Hilbert spaces. -/
set_option autoImplicit false
set_option maxHeartbeats 1600000
noncomputable section
namespace F1Fecho.ContinuousIntertwining
variable {H K:Type*} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
  [NormedAddCommGroup K] [InnerProductSpace ℂ K] [CompleteSpace K]

theorem cfc_intertwine (A:H→L[ℂ]H) (B:K→L[ℂ]K)
    (hA:IsSelfAdjoint A) (hB:IsSelfAdjoint B) (V:H→L[ℂ]K)
    (hV:V.comp A=B.comp V) (f:ℂ→ℂ) (hf:Continuous f) :
    V.comp (cfc f A)=(cfc f B).comp V := by
  let s:Set ℂ:=spectrum ℂ A∪spectrum ℂ B
  letI : CompactSpace s := isCompact_iff_compactSpace.mp
    ((ContinuousFunctionalCalculus.isCompact_spectrum A).union
      (ContinuousFunctionalCalculus.isCompact_spectrum B))
  let iA:C(spectrum ℂ A,s):=⟨fun z=>⟨z,Or.inl z.property⟩,by fun_prop⟩
  let iB:C(spectrum ℂ B,s):=⟨fun z=>⟨z,Or.inr z.property⟩,by fun_prop⟩
  let φ:C(s,ℂ)→⋆ₐ[ℂ](H→L[ℂ]H):=
    (cfcHom hA.isStarNormal).comp (ContinuousMap.compStarAlgHom' ℂ ℂ iA)
  let ψ:C(s,ℂ)→⋆ₐ[ℂ](K→L[ℂ]K):=
    (cfcHom hB.isStarNormal).comp (ContinuousMap.compStarAlgHom' ℂ ℂ iB)
  have hφ:Continuous φ := (cfcHom_continuous hA.isStarNormal).comp iA.continuous_precomp
  have hψ:Continuous ψ := (cfcHom_continuous hB.isStarNormal).comp iB.continuous_precomp
  have ha:φ (.restrict s (.id ℂ))=A := by
    change cfcHom hA.isStarNormal (.restrict (spectrum ℂ A) (.id ℂ))=A
    exact cfcHom_id hA.isStarNormal
  have hb:ψ (.restrict s (.id ℂ))=B := by
    change cfcHom hB.isStarNormal (.restrict (spectrum ℂ B) (.id ℂ))=B
    exact cfcHom_id hB.isStarNormal
  have hmain:=hom_intertwine_selfadjoint φ ψ hφ hψ V (ha.symm ▸ hA) (hb.symm ▸ hB)
    (by rwa [ha,hb]) (.restrict s ⟨f,hf⟩)
  rw [cfc_apply f A hA.isStarNormal hf.continuousOn,
    cfc_apply f B hB.isStarNormal hf.continuousOn]
  exact hmain

end F1Fecho.ContinuousIntertwining
#print axioms F1Fecho.ContinuousIntertwining.cfc_intertwine
