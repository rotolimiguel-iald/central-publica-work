import TGLExt.F1Fecho394.WeylNetWiringR1
import TGLExt.F1Fecho394.BosonicFockGroupActions
import TGLExt.FlagNetV31
import TGLExt.QGSolutionComplete
/-!
The existing concrete boost on bosonic Fock restricts to an automorphism of the
generated wedge algebra when the named Weyl covariance input is supplied.
The restricted group and its implementation are constructed here. This does
not prove that this group is the vacuum modular group: that requires the
remaining Tomita/KMS realization. No concrete Weyl family or LightNetData
inhabitant is claimed here.
-/
set_option autoImplicit false
set_option maxHeartbeats 1200000
noncomputable section
namespace F1Fecho.WeylFlow
open F1Fecho.WeylNet TGLExt.ImportedSQ F1Rede.BosonicFock
open TGL.SpecificAQFT TGLExt.ContratoQGv31 TGLExt.QGSolution

variable {E : Type} [NormedAddCommGroup E] [InnerProductSpace ℂ E] [CompleteSpace E]

def restrictAutomorphism (M : VonNeumannAlgebra E)
    (e : (E →L[ℂ] E) ≃⋆ₐ[ℂ] (E →L[ℂ] E))
    (he : ∀ x, x ∈ M ↔ e x ∈ M) : M.toStarSubalgebra ≃⋆ₐ[ℂ] M.toStarSubalgebra where
  toFun x := ⟨e x, (he x).mp x.property⟩
  invFun x := ⟨e.symm x, (he (e.symm x)).mpr (by simpa using x.property)⟩
  left_inv x := Subtype.ext (e.symm_apply_apply x)
  right_inv x := Subtype.ext (e.apply_symm_apply x)
  map_mul' x y := Subtype.ext (map_mul e x.val y.val)
  map_add' x y := Subtype.ext (map_add e x.val y.val)
  map_smul' r x := Subtype.ext (map_smul e r x.val)
  map_star' x := Subtype.ext (map_star e x.val)

theorem restrictAutomorphism_apply (M : VonNeumannAlgebra E)
    (e : (E →L[ℂ] E) ≃⋆ₐ[ℂ] (E →L[ℂ] E))
    (he : ∀ x, x ∈ M ↔ e x ∈ M) (x : M.toStarSubalgebra) :
    ((restrictAutomorphism M e he) x).val = e x := rfl

def boostAd (t : ℝ) : (F →L[ℂ] F) ≃⋆ₐ[ℂ] (F →L[ℂ] F) :=
  (gamma (B0 (-(2 * Real.pi * t)))).conjStarAlgEquiv

theorem boostAd_zero : boostAd 0 = StarAlgEquiv.refl := by
  simp only [boostAd, mul_zero, neg_zero, B0_zero, gamma_refl,
    LinearIsometryEquiv.conjStarAlgEquiv_refl]

theorem boostAd_add (s t : ℝ) : boostAd (s+t) = (boostAd s).trans (boostAd t) := by
  unfold boostAd
  rw [show -(2 * Real.pi * (s+t)) = -(2 * Real.pi * t) + -(2 * Real.pi * s) by ring,
    B0_add, gamma_trans, LinearIsometryEquiv.conjStarAlgEquiv_trans]

variable (W : H1 → (F →L[ℂ] F))
  (hstar : ∀ f, star (W f) = W (-f))
  (hcov : ∀ (u : H1 ≃ₗᵢ[ℂ] H1) f,
    (gamma u).conjStarAlgEquiv (W f) = W (u f))
  (L : LightNetData)

include hstar hcov in
theorem boostAd_preserves_wedge (t : ℝ) (x : F →L[ℂ] F) :
    x ∈ R W (L.K rightWedge) ↔ boostAd t x ∈ R W (L.K rightWedge) := by
  have hk : ∀ f : H1, f ∈ L.K rightWedge ↔
      B0 (-(2 * Real.pi * t)) f ∈ L.K rightWedge := by
    intro f
    have hh := L.K_boost (-(2 * Real.pi * t)) rightWedge f
    rw [FlagNet.boost_image_rightWedge] at hh
    exact hh
  exact R_cov W hstar (B0 (-(2 * Real.pi * t))) (boostAd t)
    (hcov (B0 (-(2 * Real.pi * t)))) (L.K rightWedge) (L.K rightWedge) hk x

def wedgeFlow (t : ℝ) : (R W (L.K rightWedge)).toStarSubalgebra ≃⋆ₐ[ℂ]
    (R W (L.K rightWedge)).toStarSubalgebra :=
  restrictAutomorphism (R W (L.K rightWedge)) (boostAd t)
    (boostAd_preserves_wedge W hstar hcov L t)

theorem wedgeFlow_is_Ad (t : ℝ) (x : (R W (L.K rightWedge)).toStarSubalgebra) :
    ((wedgeFlow W hstar hcov L t) x).val =
      (gamma (B0 (-(2*Real.pi*t)))).conjStarAlgEquiv x.val := rfl

theorem wedgeFlow_zero : wedgeFlow W hstar hcov L 0 = StarAlgEquiv.refl := by
  apply StarAlgEquiv.ext
  intro x
  apply Subtype.ext
  change boostAd 0 x.val = x.val
  rw [boostAd_zero]
  rfl

theorem wedgeFlow_add (s t : ℝ) : wedgeFlow W hstar hcov L (s+t) =
    (wedgeFlow W hstar hcov L s).trans (wedgeFlow W hstar hcov L t) := by
  apply StarAlgEquiv.ext
  intro x
  apply Subtype.ext
  change boostAd (s+t) x.val = boostAd t (boostAd s x.val)
  rw [boostAd_add]
  rfl

end F1Fecho.WeylFlow

open Lean in
run_cmd do
  let env ← Elab.Command.liftCoreM getEnv
  for (n, ci) in env.constants.map₂.toList do
    if (`F1Fecho.WeylFlow).isPrefixOf n then
      let axs ← collectAxioms n
      IO.println ("LOCAL_DECL\t" ++ n.toString ++ "\t" ++ String.intercalate "," (axs.toList.map Name.toString))
      unless axs.all (fun a => a == `propext || a == `Classical.choice || a == `Quot.sound) do
        throwError "AXIOM_AUDIT_REFUSED: {n}"
      match ci with
      | .axiomInfo _ => throwError "LOCAL_AXIOM_REFUSED: {n}"
      | _ => pure ()
