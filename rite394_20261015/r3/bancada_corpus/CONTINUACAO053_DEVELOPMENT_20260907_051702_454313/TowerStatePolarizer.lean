import HorizonGNSImplementation
import SymplecticPolarizer
import QuantumOrbitArea

set_option autoImplicit false
set_option maxHeartbeats 1600000

namespace ChatgptAudit.Covariant053
open TGLExt ChatgptAudit ChatgptAudit.Density033 ChatgptAudit.Expectation047
  ChatgptAudit.Observable035 ChatgptAudit.Orbit052 ClosedSubmodule
noncomputable section

/-- Real self-adjoint factor vectors separate the real closed state subspace. -/
theorem real_state_pairing_ext (P : SiteProfile) (u v : TowerHilbert P)
    (hu : u ∈ realStateSubspace P) (hv : v ∈ realStateSubspace P)
    (h : ∀ B : TowerHilbert P →L[ℂ] TowerHilbert P,
      B ∈ theFactorObject P → IsSelfAdjoint B →
      (inner ℂ (B (hOmega P)) u).re = (inner ℂ (B (hOmega P)) v).re) :
    u = v := by
  let F : TowerHilbert P →L[ℝ] ℝ := innerSL ℝ (u-v)
  have hs : Submodule.span ℝ (realStateGenerators P) ≤ F.ker := by
    apply Submodule.span_le.mpr
    rintro x ⟨B, hB, hsa, rfl⟩
    change inner ℝ (u-v) (B (hOmega P)) = 0
    rw [real_inner_comm, inner_sub_right,
      ClosedSubmodule.inner_real_eq_re_inner, ClosedSubmodule.inner_real_eq_re_inner,
      h B hB hsa, sub_self]
  have hc : realStateSubspace P ≤ F.ker :=
    Submodule.topologicalClosure_minimal _ hs F.isClosed_ker
  have hz := hc ((realStateSubspace P).sub_mem hu hv)
  change inner ℝ (u-v) (u-v) = 0 at hz
  exact sub_eq_zero.mp (inner_self_eq_zero.mp hz)

/-- The tower uses the previously constructed real compression, without a second operator. -/
def statePolarizer (P : SiteProfile) : TowerHilbert P →L[ℝ] TowerHilbert P :=
  symplecticPolarizer (realStateSubspace P)

theorem state_polarizer_pairing (P : SiteProfile)
    (A B : TowerHilbert P →L[ℂ] TowerHilbert P)
    (hA : A ∈ theFactorObject P) (hAsa : IsSelfAdjoint A)
    (hB : B ∈ theFactorObject P) (hBsa : IsSelfAdjoint B) :
    (inner ℂ (A (hOmega P)) (statePolarizer P (B (hOmega P)))).re =
      (omegaState P (star A * B)).im := by
  rw [omega_product_inner, star_star]
  exact polarizer_duality (realStateSubspace P)
    (real_state_generator_mem P A hA hAsa) (real_state_generator_mem P B hB hBsa)

theorem tower_polarizer_eq_of_pairing (P : SiteProfile)
    (A C : TowerHilbert P →L[ℂ] TowerHilbert P)
    (hA : A ∈ theFactorObject P) (hAsa : IsSelfAdjoint A)
    (hC : C ∈ theFactorObject P) (hCsa : IsSelfAdjoint C)
    (h : ∀ B : TowerHilbert P →L[ℂ] TowerHilbert P,
      B ∈ theFactorObject P → IsSelfAdjoint B →
      (omegaState P (star B * C)).re = (omegaState P (star B * A)).im) :
    statePolarizer P (A (hOmega P)) = C (hOmega P) := by
  apply real_state_pairing_ext P _ _
    (polarizer_mem (realStateSubspace P) _) (real_state_generator_mem P C hC hCsa)
  intro B hB hBsa
  rw [state_polarizer_pairing P B A hB hBsa hA hAsa, ← h B hB hBsa,
    omega_product_inner, star_star]

/-- Testing both self-adjoint parts pays the full complex centralizer condition. -/
theorem state_centralizer_iff_imaginary (P : SiteProfile)
    (A : TowerHilbert P →L[ℂ] TowerHilbert P)
    (hA : A ∈ theFactorObject P) (hAsa : IsSelfAdjoint A) :
    A ∈ omegaCentralizer P ↔
      ∀ B : TowerHilbert P →L[ℂ] TowerHilbert P,
        B ∈ theFactorObject P → IsSelfAdjoint B → (omegaState P (B*A)).im = 0 := by
  constructor
  · intro hc B hB hBsa
    have hz := quantum_centralizer_imaginary_zero P A B hc hAsa hB hBsa
    rw [hAsa.star_eq, hc.2 B hB] at hz
    exact hz
  · intro ht
    refine ⟨hA, ?_⟩
    intro B hB
    have hC : IsSelfAdjoint (B + star B) := by
      change star (B + star B) = B + star B
      simp only [star_add, star_star]
      exact add_comm _ _
    have hF : IsSelfAdjoint (Complex.I • (B - star B)) := by
      change star (Complex.I • (B - star B)) = Complex.I • (B - star B)
      simp only [star_smul, Complex.star_def, Complex.conj_I, star_sub, star_star]
      rw [← neg_sub B (star B), smul_neg, neg_smul, neg_neg]
    have hBm : star B ∈ theFactorObject P := star_mem hB
    have hc := ht (B + star B) ((theFactorObject P).add_mem hB hBm) hC
    have hf := ht (Complex.I • (B - star B))
      ((theFactorObject P).toStarSubalgebra.smul_mem
        ((theFactorObject P).sub_mem hB hBm) Complex.I) hF
    have hconj : omegaState P (star B*A) = star (omegaState P (A*B)) := by
      rw [← omega_state_star, star_mul, hAsa.star_eq]
    simp only [add_mul, omega_state_add, hconj, Complex.add_im,
      Complex.star_def, Complex.conj_im] at hc
    simp only [smul_mul_assoc, sub_mul, omega_state_smul, omegaState_sub, hconj,
      Complex.star_def, Complex.mul_im, Complex.I_re, Complex.I_im,
      Complex.sub_re, Complex.conj_re, zero_mul, one_mul, zero_add] at hf
    apply Complex.ext
    · linarith
    · linarith

/-- The exact radical is the centralizer, including its converse. -/
theorem state_polarizer_zero_iff (P : SiteProfile)
    (A : TowerHilbert P →L[ℂ] TowerHilbert P)
    (hA : A ∈ theFactorObject P) (hAsa : IsSelfAdjoint A) :
    statePolarizer P (A (hOmega P)) = 0 ↔ A ∈ omegaCentralizer P := by
  rw [state_centralizer_iff_imaginary P A hA hAsa]
  constructor
  · intro hz B hB hBsa
    have hp := state_polarizer_pairing P B A hB hBsa hA hAsa
    rw [hz, inner_zero_right, hBsa.star_eq] at hp
    exact hp.symm
  · intro hz
    apply real_state_pairing_ext P _ _
      (polarizer_mem (realStateSubspace P) _) (realStateSubspace P).zero_mem
    intro B hB hBsa
    rw [state_polarizer_pairing P B A hB hBsa hA hAsa, hBsa.star_eq,
      hz B hB hBsa, inner_zero_right]
    rfl

def stateVectorReal (P : SiteProfile) :
    (TowerHilbert P →L[ℂ] TowerHilbert P) →ₗ[ℝ] TowerHilbert P where
  toFun A := A (hOmega P)
  map_add' A B := rfl
  map_smul' c A := rfl

/-- A global real bilinear form on bounded generators, prior to taking the radical quotient. -/
def stateCovariantBilinear (P : SiteProfile) (epsilon : ℝ) :
    (TowerHilbert P →L[ℂ] TowerHilbert P) →ₗ[ℝ]
      (TowerHilbert P →L[ℂ] TowerHilbert P) →ₗ[ℝ] ℝ where
  toFun A := (polarizerFormBilin (realStateSubspace P) epsilon
    (stateVectorReal P A)).comp (stateVectorReal P)
  map_add' A B := by
    ext C
    exact (polarizerFormBilin (realStateSubspace P) epsilon).map_add
      (stateVectorReal P A) (stateVectorReal P B) |> congrArg (fun L => L (stateVectorReal P C))
  map_smul' c A := by
    ext B
    exact (polarizerFormBilin (realStateSubspace P) epsilon).map_smul c
      (stateVectorReal P A) |> congrArg (fun L => L (stateVectorReal P B))

theorem state_covariant_apply (P : SiteProfile) (epsilon : ℝ)
    (A B : TowerHilbert P →L[ℂ] TowerHilbert P) :
    stateCovariantBilinear P epsilon A B =
      (inner ℂ (statePolarizer P (A (hOmega P)))
        (statePolarizer P (B (hOmega P)))).re +
      epsilon * (inner ℂ (statePolarizer P (statePolarizer P (A (hOmega P))))
        (statePolarizer P (statePolarizer P (B (hOmega P))))).re :=
  polarizer_form_re (realStateSubspace P) epsilon _ _

theorem state_covariant_symmetric (P : SiteProfile) (epsilon : ℝ)
    (A B : TowerHilbert P →L[ℂ] TowerHilbert P) :
    stateCovariantBilinear P epsilon A B = stateCovariantBilinear P epsilon B A :=
  polarizer_form_symmetric (realStateSubspace P) epsilon _ _

theorem state_covariant_nonneg (P : SiteProfile) (epsilon : ℝ) (he : 0 ≤ epsilon)
    (A : TowerHilbert P →L[ℂ] TowerHilbert P) :
    0 ≤ stateCovariantBilinear P epsilon A A :=
  polarizer_form_nonneg (realStateSubspace P) epsilon he _

theorem state_covariant_kernel (P : SiteProfile) (epsilon : ℝ) (he : 0 ≤ epsilon)
    (A : TowerHilbert P →L[ℂ] TowerHilbert P)
    (hA : A ∈ theFactorObject P) (hAsa : IsSelfAdjoint A) :
    stateCovariantBilinear P epsilon A A = 0 ↔ A ∈ omegaCentralizer P :=
  (polarizer_form_zero_iff (realStateSubspace P) epsilon he _).trans
    (state_polarizer_zero_iff P A hA hAsa)

theorem state_covariant_positive_iff (P : SiteProfile) (epsilon : ℝ) (he : 0 ≤ epsilon)
    (A : TowerHilbert P →L[ℂ] TowerHilbert P)
    (hA : A ∈ theFactorObject P) (hAsa : IsSelfAdjoint A) :
    0 < stateCovariantBilinear P epsilon A A ↔ A ∉ omegaCentralizer P := by
  have hn := state_covariant_nonneg P epsilon he A
  have hk := state_covariant_kernel P epsilon he A hA hAsa
  constructor
  · intro hp hc
    rw [hk.mpr hc] at hp
    exact (lt_irrefl 0) hp
  · intro hc
    exact lt_of_le_of_ne hn (Ne.symm (mt hk.mp hc))

theorem horizon_gns_real_iff (P : SiteProfile) (h : TowerHorizon P) (x : TowerHilbert P) :
    x ∈ realStateSubspace P ↔ horizonGNSUnitary P h x ∈ realStateSubspace P := by
  constructor
  · exact horizon_gns_real_mem P h x
  · intro hx
    have hr := horizon_gns_real_mem P h.inv (horizonGNSUnitary P h x) hx
    simpa only [← horizon_gns_symm_apply, LinearIsometryEquiv.symm_apply_apply] using hr

theorem state_polarizer_covariant (P : SiteProfile) (h : TowerHorizon P)
    (x : TowerHilbert P) :
    statePolarizer P (horizonGNSUnitary P h x) =
      horizonGNSUnitary P h (statePolarizer P x) :=
  polarizer_covariant (realStateSubspace P) (horizonGNSUnitary P h)
    (horizon_gns_real_iff P h) x

/-- Covariance holds for every specified horizon and every bounded factor generator. -/
theorem state_covariant_factor_invariant (P : SiteProfile) (epsilon : ℝ) (h : TowerHorizon P)
    (A B : TowerHilbert P →L[ℂ] TowerHilbert P)
    (hA : A ∈ theFactorObject P) (hB : B ∈ theFactorObject P) :
    stateCovariantBilinear P epsilon (adT h A) (adT h B) =
      stateCovariantBilinear P epsilon A B := by
  have hf := polarizer_form_covariant (realStateSubspace P) epsilon
    (horizonGNSUnitary P h) (horizon_gns_real_iff P h) (A (hOmega P)) (B (hOmega P))
  rw [horizon_gns_apply_factor P h A hA, horizon_gns_apply_factor P h B hB] at hf
  exact hf

theorem state_covariant_invariant (P : SiteProfile) (epsilon : ℝ) (h : TowerHorizon P)
    (A B : TowerHilbert P →L[ℂ] TowerHilbert P)
    (hA : A ∈ theFactorObject P) (_hAsa : IsSelfAdjoint A)
    (hB : B ∈ theFactorObject P) (_hBsa : IsSelfAdjoint B) :
    stateCovariantBilinear P epsilon (adT h A) (adT h B) =
      stateCovariantBilinear P epsilon A B :=
  state_covariant_factor_invariant P epsilon h A B hA hB

/-- Centralizing additions do not change the form; this pays descent in the first slot. -/
theorem state_covariant_add_centralizer (P : SiteProfile) (epsilon : ℝ)
    (A B C : TowerHilbert P →L[ℂ] TowerHilbert P)
    (hC : C ∈ omegaCentralizer P) (hCsa : IsSelfAdjoint C) :
    stateCovariantBilinear P epsilon (A+C) B = stateCovariantBilinear P epsilon A B := by
  have hz := (state_polarizer_zero_iff P C hC.1 hCsa).mpr hC
  simp only [state_covariant_apply, _root_.add_apply, map_add, hz, add_zero]

theorem state_covariant_add_centralizer_right (P : SiteProfile) (epsilon : ℝ)
    (A B C : TowerHilbert P →L[ℂ] TowerHilbert P)
    (hC : C ∈ omegaCentralizer P) (hCsa : IsSelfAdjoint C) :
    stateCovariantBilinear P epsilon A (B+C) = stateCovariantBilinear P epsilon A B := by
  rw [state_covariant_symmetric P epsilon A (B+C),
    state_covariant_add_centralizer P epsilon B A C hC hCsa,
    state_covariant_symmetric P epsilon B A]

/-- The response is the actual derivative of real state readings under bounded unitary motion. -/
def realStateResponse (P : SiteProfile)
    (A B : TowerHilbert P →L[ℂ] TowerHilbert P) : ℝ :=
  deriv (fun t : ℝ => (omegaState P (unitaryConjugation P A B t)).re) 0

theorem state_reading_real_hasDerivAt (P : SiteProfile)
    (A B : TowerHilbert P →L[ℂ] TowerHilbert P)
    (hA : IsSelfAdjoint A) (hB : IsSelfAdjoint B) :
    HasDerivAt (fun t : ℝ => (omegaState P (unitaryConjugation P A B t)).re)
      (-2 * (omegaState P (B * A)).im) 0 := by
  have hs : omegaState P (A * B) = star (omegaState P (B * A)) := by
    simpa only [star_mul, hA.star_eq, hB.star_eq] using
      omega_state_star P (B * A)
  have hc : (Complex.I * omegaState P (B * A - A * B)).re =
      -2 * (omegaState P (B * A)).im := by
    rw [omegaState_sub, hs]
    simp only [Complex.mul_re, Complex.I_re, Complex.I_im,
      Complex.sub_im, Complex.star_def, Complex.conj_im,
      zero_mul, one_mul, zero_sub]
    ring
  have hd := unitary_expectation_derivative_zero P A B hA
  have hr : HasDerivAt (fun t : ℝ =>
      (omegaState P (unitaryConjugation P A B t)).re)
      (Complex.I * omegaState P (B * A - A * B)).re 0 := by
    convert (Complex.reCLM.hasFDerivAt.comp_hasDerivAt 0 hd) using 1
    all_goals rfl
  rwa [hc] at hr

theorem state_response_formula (P : SiteProfile)
    (A B : TowerHilbert P →L[ℂ] TowerHilbert P)
    (hA : IsSelfAdjoint A) (hB : IsSelfAdjoint B) :
    realStateResponse P A B = -2 * (omegaState P (B*A)).im :=
  (state_reading_real_hasDerivAt P A B hA hB).deriv

theorem state_response_kernel (P : SiteProfile)
    (A : TowerHilbert P →L[ℂ] TowerHilbert P)
    (hA : A ∈ theFactorObject P) (hAsa : IsSelfAdjoint A) :
    (∀ B : TowerHilbert P →L[ℂ] TowerHilbert P,
      B ∈ theFactorObject P → IsSelfAdjoint B → realStateResponse P A B = 0) ↔
      A ∈ omegaCentralizer P := by
  rw [state_centralizer_iff_imaginary P A hA hAsa]
  constructor
  · intro hr B hB hBsa
    have hz := hr B hB hBsa
    rw [state_response_formula P A B hAsa hBsa] at hz
    linarith
  · intro hr B hB hBsa
    rw [state_response_formula P A B hAsa hBsa, hr B hB hBsa, mul_zero]

theorem state_covariant_response_kernel (P : SiteProfile) (epsilon : ℝ) (he : 0 ≤ epsilon)
    (A : TowerHilbert P →L[ℂ] TowerHilbert P)
    (hA : A ∈ theFactorObject P) (hAsa : IsSelfAdjoint A) :
    stateCovariantBilinear P epsilon A A = 0 ↔
      ∀ B : TowerHilbert P →L[ℂ] TowerHilbert P,
        B ∈ theFactorObject P → IsSelfAdjoint B → realStateResponse P A B = 0 :=
  (state_covariant_kernel P epsilon he A hA hAsa).trans
    (state_response_kernel P A hA hAsa).symm

#print axioms real_state_pairing_ext
#print axioms statePolarizer
#print axioms state_polarizer_pairing
#print axioms tower_polarizer_eq_of_pairing
#print axioms state_centralizer_iff_imaginary
#print axioms state_polarizer_zero_iff
#print axioms stateVectorReal
#print axioms stateCovariantBilinear
#print axioms state_covariant_apply
#print axioms state_covariant_symmetric
#print axioms state_covariant_nonneg
#print axioms state_covariant_kernel
#print axioms state_covariant_positive_iff
#print axioms horizon_gns_real_iff
#print axioms state_polarizer_covariant
#print axioms state_covariant_factor_invariant
#print axioms state_covariant_invariant
#print axioms state_covariant_add_centralizer
#print axioms state_covariant_add_centralizer_right
#print axioms realStateResponse
#print axioms state_reading_real_hasDerivAt
#print axioms state_response_formula
#print axioms state_response_kernel
#print axioms state_covariant_response_kernel

end
end ChatgptAudit.Covariant053
