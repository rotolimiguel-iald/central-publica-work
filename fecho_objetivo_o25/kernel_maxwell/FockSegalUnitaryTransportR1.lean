import WeakSegalDistributionR3
import WickQuadraticFormR6
import BosonicFockGroupActions

/-! Candidate R50. Unitary transport of the existing Segal and bilocal Wick
operators on their actual exponential domain in the same canonical Fock.
Creation is not asserted to preserve that domain. No coincident-point
restriction, local stress identification or MaxwellCertificate is asserted. -/
set_option Elab.async false
set_option autoImplicit false
set_option maxHeartbeats 400000
set_option synthInstance.maxHeartbeats 500000
noncomputable section

namespace F1Fecho.FockSegalTransport
open TGLExt.ImportedSQ F1Rede.BosonicFock F1Rede.BosonicFockGroupActions
open F1Fecho.Exponential F1Fecho.Annihilation F1Fecho.Creation

theorem synthesize_equivMapDomain (u : H1 ≃ₗᵢ[ℂ] H1) (c : H1 →₀ ℂ) :
    synthesize (Finsupp.equivMapDomain u.toLinearEquiv.toEquiv c) =
      gamma u (synthesize c) := by
  simp only [synthesize, Finsupp.linearCombination_apply, Finsupp.sum_equivMapDomain]
  change (∑ h ∈ c.support, c h • exponential (u h)) =
    gamma u (∑ h ∈ c.support, c h • exponential h)
  simp only [map_sum, map_smul, gamma_exponential]

theorem gamma_mem_exponentialDomain (u : H1 ≃ₗᵢ[ℂ] H1) (x : domain) :
    gamma u x.val ∈ domain := by
  refine ⟨Finsupp.equivMapDomain u.toLinearEquiv.toEquiv (preimage x), ?_⟩
  rw [synthesize_equivMapDomain, preimage_spec]

def domainGamma (u : H1 ≃ₗᵢ[ℂ] H1) : domain →ₗ[ℂ] domain where
  toFun x := ⟨gamma u x.val, gamma_mem_exponentialDomain u x⟩
  map_add' x y := by
    apply Subtype.ext
    exact map_add (gamma u) x.val y.val
  map_smul' c x := by
    apply Subtype.ext
    exact map_smul (gamma u) c x.val

theorem domainGamma_value (u : H1 ≃ₗᵢ[ℂ] H1) (x : domain) :
    (domainGamma u x : F) = gamma u x.val := rfl

theorem domainGamma_symm_apply (u : H1 ≃ₗᵢ[ℂ] H1) (x : domain) :
    domainGamma u.symm (domainGamma u x) = x := by
  apply Subtype.ext
  change gamma u.symm (gamma u x.val) = x.val
  rw [gamma_symm, LinearIsometryEquiv.symm_apply_apply]

theorem weighted_equivMapDomain (u : H1 ≃ₗᵢ[ℂ] H1) (f : H1) (c : H1 →₀ ℂ) :
    weighted (u f) (Finsupp.equivMapDomain u.toLinearEquiv.toEquiv c) =
      gamma u (weighted f c) := by
  simp only [weighted, Finsupp.linearCombination_apply, Finsupp.sum_equivMapDomain]
  change (∑ h ∈ c.support, c h • (inner ℂ (u f) (u h) • exponential (u h))) =
    gamma u (∑ h ∈ c.support, c h • (inner ℂ f h • exponential h))
  simp only [map_sum, map_smul, gamma_exponential, LinearIsometryEquiv.inner_map_map]

theorem annihilation_gamma (u : H1 ≃ₗᵢ[ℂ] H1) (f : H1) (x : domain) :
    annihilation (u f) (domainGamma u x) = gamma u (annihilation f x) := by
  let c := Finsupp.equivMapDomain u.toLinearEquiv.toEquiv (preimage x)
  have hc : synthesize c = (domainGamma u x : F) := by
    change synthesize (Finsupp.equivMapDomain u.toLinearEquiv.toEquiv (preimage x)) =
      gamma u x.val
    rw [synthesize_equivMapDomain, preimage_spec]
  change weighted (u f) (preimage (domainGamma u x)) = gamma u (weighted f (preimage x))
  calc
    _ = weighted (u f) c :=
      weighted_eq_of_synthesize_eq (u f) _ _ ((preimage_spec _).trans hc.symm)
    _ = _ := weighted_equivMapDomain u f (preimage x)

theorem creation_gamma (u : H1 ≃ₗᵢ[ℂ] H1) (f : H1) (x : domain) :
    creation (u f) (domainGamma u x) = gamma u (creation f x) := by
  apply sub_eq_zero.mp
  apply exponential_orthogonal_zero
  intro h
  apply inner_eq_zero_symm.mp
  rw [inner_sub_right]
  apply sub_eq_zero.mpr
  obtain ⟨k, rfl⟩ := u.surjective h
  calc
    inner ℂ (exponential (u k)) (creation (u f) (domainGamma u x)) =
        inner ℂ (u k) (u f) *
          inner ℂ (exponential (u k)) (gamma u x.val) :=
      creation_inner_on_domain (u k) (u f) (domainGamma u x)
    _ = inner ℂ k f * inner ℂ (exponential k) x.val := by
      rw [← gamma_exponential u k, LinearIsometryEquiv.inner_map_map,
        LinearIsometryEquiv.inner_map_map]
    _ = inner ℂ (exponential k) (creation f x) :=
      (creation_inner_on_domain k f x).symm
    _ = inner ℂ (exponential (u k)) (gamma u (creation f x)) := by
      rw [← gamma_exponential u k, LinearIsometryEquiv.inner_map_map]

theorem segal_gamma (u : H1 ≃ₗᵢ[ℂ] H1) (f : H1) (x : domain) :
    segal (u f) (domainGamma u x) = gamma u (segal f x) := by
  change ((Real.sqrt 2)⁻¹ : ℂ) •
      (annihilation (u f) (domainGamma u x) + creation (u f) (domainGamma u x)) =
    gamma u (((Real.sqrt 2)⁻¹ : ℂ) • (annihilation f x + creation f x))
  rw [annihilation_gamma, creation_gamma, map_smul, map_add]

theorem invariant_annihilation_gamma (u : H1 ≃ₗᵢ[ℂ] H1) (f : H1) (x : domain) :
    onInvariantDomain (u f) (domainGamma u x) =
      domainGamma u (onInvariantDomain f x) := by
  apply Subtype.ext
  exact annihilation_gamma u f x

theorem doubleAnnihilate_gamma (u : H1 ≃ₗᵢ[ℂ] H1) (f g : H1) (x : domain) :
    F1Fecho.WickForm.doubleAnnihilate (u f) (u g) (domainGamma u x) =
      gamma u (F1Fecho.WickForm.doubleAnnihilate f g x) := by
  unfold F1Fecho.WickForm.doubleAnnihilate
  rw [invariant_annihilation_gamma, annihilation_gamma]

/-- Bilocal smearing covariance on all finite exponential combinations.
This is not a restriction to coincident spacetime points. -/
theorem wick_quadratic_gamma (u : H1 ≃ₗᵢ[ℂ] H1) (f g : H1) (x y : domain) :
    F1Fecho.WickForm.quadratic (u f) (u g) (domainGamma u x) (domainGamma u y) =
      F1Fecho.WickForm.quadratic f g x y := by
  simp only [F1Fecho.WickForm.quadratic, doubleAnnihilate_gamma,
    annihilation_gamma, domainGamma_value, LinearIsometryEquiv.inner_map_map]

end F1Fecho.FockSegalTransport
#print axioms F1Fecho.FockSegalTransport.synthesize_equivMapDomain
#print axioms F1Fecho.FockSegalTransport.gamma_mem_exponentialDomain
#print axioms F1Fecho.FockSegalTransport.domainGamma_value
#print axioms F1Fecho.FockSegalTransport.domainGamma_symm_apply
#print axioms F1Fecho.FockSegalTransport.weighted_equivMapDomain
#print axioms F1Fecho.FockSegalTransport.annihilation_gamma
#print axioms F1Fecho.FockSegalTransport.creation_gamma
#print axioms F1Fecho.FockSegalTransport.segal_gamma
#print axioms F1Fecho.FockSegalTransport.invariant_annihilation_gamma
#print axioms F1Fecho.FockSegalTransport.doubleAnnihilate_gamma
#print axioms F1Fecho.FockSegalTransport.wick_quadratic_gamma

