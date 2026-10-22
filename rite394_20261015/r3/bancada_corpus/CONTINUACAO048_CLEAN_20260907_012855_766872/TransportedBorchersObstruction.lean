import ProductBorchersObstruction
import ProfileFlowTransport

set_option autoImplicit false

namespace ChatgptAudit.Geometry048

open TGLExt ChatgptAudit.Profile026 ChatgptAudit.Transport027

noncomputable section

/-- A product-profile modular flow transported by the concrete GNS unitary027
still admits only the trivial norm-preserving Borchers family. No common period
is assumed. This does not rule out Bisognano-Wichmann for other modular data. -/
theorem profile_borchers_trivial
    (P Q : SiteProfile) (hpos : 0 < profileAffinityLimit P Q)
    (V : ℝ → (TowerHilbert P →L[ℂ] TowerHilbert P))
    (hcont : ∀ v, ContinuousAt (fun a => V a v) 0)
    (hzero : V 0 = 1)
    (hnorm : ∀ a v, ‖V a v‖ = ‖v‖)
    (hborchers : ∀ t a, profileFlowConjugation P Q hpos t (V a) =
      V (Real.exp (-2 * Real.pi * t) * a)) :
    ∀ a, V a = 1 := by
  let e := profileGNSUnitary P Q hpos
  let C := profileFactorConjugation P Q hpos
  let W : ℝ → (TowerHilbert Q →L[ℂ] TowerHilbert Q) := fun a => C.symm (V a)
  have hWcont (v : TowerHilbert Q) : ContinuousAt (fun a => W a v) 0 := by
    change ContinuousAt (fun a => e.symm (V a (e v))) 0
    exact e.symm.continuous.continuousAt.comp (hcont (e v))
  have hWzero : W 0 = 1 := by
    dsimp only [W]
    rw [hzero, map_one]
  have hWnorm (a : ℝ) (v : TowerHilbert Q) : ‖W a v‖ = ‖v‖ := by
    change ‖e.symm (V a (e v))‖ = ‖v‖
    rw [e.symm.norm_map, hnorm, e.norm_map]
  have hWborchers (t a : ℝ) : modularConjugation Q t (W a) =
      W (Real.exp (-2 * Real.pi * t) * a) := by
    apply C.injective
    have h := hborchers t a
    rw [profile_flow_conjugation_eq] at h
    simpa only [W, C, StarAlgEquiv.apply_symm_apply] using h
  have hW := product_borchers_trivial (P := Q) W hWcont hWzero hWnorm hWborchers
  intro a
  have h := congrArg C (hW a)
  simpa only [W, StarAlgEquiv.apply_symm_apply, map_one] using h

#print axioms profile_borchers_trivial

end
end ChatgptAudit.Geometry048
