import TGLExt.V351RegularImaginaryPowers
import TGLExt.V350CharacterLocality

set_option autoImplicit false
set_option maxHeartbeats 2500000

namespace TGLV350.Regular
open TGLExt ChatgptAudit MeasureTheory Filter
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

/-- Reuse pointwise pairing locality; no new simple-function approximation. -/
theorem character_commutation_realScalarMultiplier
    (B : RegularHilbert H →L[ℂ] RegularHilbert H)
    (hB : ∀ s : ℝ, characterMultiplier s * B = B * characterMultiplier s)
    (g : ℝ → ℝ) (hg : Continuous g) (h0 : ∀ x, 0 ≤ g x) (h1 : ∀ x, g x ≤ 1) :
    realScalarMultiplier g hg h0 h1 * B = B * realScalarMultiplier g hg h0 h1 := by
  ext1 u
  apply ext_inner_left ℂ
  intro v
  change inner ℂ v (realScalarMultiplier g hg h0 h1 (B u)) =
    inner ℂ v (B (realScalarMultiplier g hg h0 h1 u))
  rw [← ContinuousLinearMap.adjoint_inner_left B (realScalarMultiplier g hg h0 h1 u) v]
  rw [L2.inner_def, L2.inner_def]
  apply integral_congr_ae
  filter_upwards [realScalarMultiplier_ae g hg h0 h1 (B u),
    realScalarMultiplier_ae g hg h0 h1 u,
    character_commutation_local_pairing B hB v u] with x hm1 hm2 hp
  rw [hm1, hm2, inner_smul_right, inner_smul_right, hp]

/-- The actual bounded resolvent belongs to the actual core. -/
theorem regularSpectralResolvent_mem (P : SiteProfile) :
    regularSpectralResolvent P ∈ regularCoreAlgebra P := by
  rw [← VonNeumannAlgebra.commutant_commutant (regularCoreAlgebra P),
    VonNeumannAlgebra.mem_commutant_iff]
  intro B hB
  let V := regularSpectralCoordinates P
  let C := V.symm.conjStarAlgEquiv B
  have hC (x : RegularHilbert (TowerHilbert P)) : V (C x) = B (V x) := by
    change V (V.symm (B (V x))) = _
    exact V.apply_symm_apply _
  have hchar : ∀ s : ℝ, characterMultiplier s * C = C * characterMultiplier s := by
    intro s
    let t := s/(2*Real.pi)
    have ht : 2*Real.pi*t = s := by
      dsimp only [t]
      field_simp
    have hv (x : RegularHilbert (TowerHilbert P)) :
        V (characterMultiplier s x) = regularUnitary P t (V x) := by
      simpa only [ht] using regularSpectralCoordinates_character P t x
    ext1 x
    apply V.injective
    change V (characterMultiplier s (C x)) = V (C (characterMultiplier s x))
    rw [hv, hC, hC, hv]
    exact congrArg (fun A : RegularHilbert (TowerHilbert P) →L[ℂ] RegularHilbert (TowerHilbert P) => A (V x))
      ((VonNeumannAlgebra.mem_commutant_iff.mp hB) _ (regularUnitary_mem P t))
  let g : ℝ → ℝ := fun ξ => Real.sigmoid (2*Real.pi*ξ)
  have hg : Continuous g := by fun_prop
  have h0 : ∀ ξ, 0 ≤ g ξ := fun ξ => Real.sigmoid_nonneg _
  have h1 : ∀ ξ, g ξ ≤ 1 := fun ξ => Real.sigmoid_le_one _
  let M := realScalarMultiplier (H := TowerHilbert P) g hg h0 h1
  have hr : V.symm.conjStarAlgEquiv (regularSpectralResolvent P) = M := by
    ext1 x
    change V.symm (regularSpectralResolvent P (V x)) = M x
    change V.symm (V (M (V.symm (V x)))) = M x
    rw [V.symm_apply_apply, V.symm_apply_apply]
  apply V.symm.conjStarAlgEquiv.injective
  change V.symm.conjStarAlgEquiv (B * regularSpectralResolvent P) =
    V.symm.conjStarAlgEquiv (regularSpectralResolvent P * B)
  rw [map_mul, map_mul, hr]
  exact (character_commutation_realScalarMultiplier C hchar g hg h0 h1).symm

/-- Affiliation expressed directly as graph commutation for every bounded
operator in N'. Together with the already proved closedness this is the usual
commutant criterion; no new affiliated-form object replaces the operator. -/
theorem regularPositiveGenerator_commutant_graph (P : SiteProfile)
    (B : RegularHilbert (TowerHilbert P) →L[ℂ] RegularHilbert (TowerHilbert P))
    (hB : B ∈ (regularCoreAlgebra P).commutant)
    (x y : RegularHilbert (TowerHilbert P))
    (hxy : (x,y) ∈ (regularPositiveGenerator P).graph) :
    (B x,B y) ∈ (regularPositiveGenerator P).graph := by
  let R := regularSpectralResolvent P
  have hc : R * B = B * R :=
    (VonNeumannAlgebra.mem_commutant_iff.mp hB) _ (regularSpectralResolvent_mem P)
  have he (u : RegularHilbert (TowerHilbert P)) : R (B u) = B (R u) :=
    congrArg (fun A : RegularHilbert (TowerHilbert P) →L[ℂ] RegularHilbert (TowerHilbert P) => A u) hc
  change (x,y) ∈ (resolventGraphOperator R (regularSpectralResolvent_injective P)).graph at hxy
  rw [resolvent_graph_equation] at hxy
  change (B x,B y) ∈ (resolventGraphOperator R (regularSpectralResolvent_injective P)).graph
  rw [resolvent_graph_equation]
  change B x - R (B x) = R (B y)
  change x-R x = R y at hxy
  rw [he, he, ← map_sub, hxy]

#print axioms character_commutation_realScalarMultiplier
#print axioms regularSpectralResolvent_mem
#print axioms regularPositiveGenerator_commutant_graph
end
end TGLV350.Regular
