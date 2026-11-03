import TGLExt.F1Fecho394.GeneralRegularImaginaryPowersR1
import TGLExt.V351RegularGeneratorAffiliation

/-! Affiliation of the concrete positive generator to the generic regular
crossed-product algebra, by commutation of its actual resolvent. Reuses v351
character locality and the constructed group identification. -/
set_option autoImplicit false
set_option maxHeartbeats 2500000
noncomputable section
namespace F1Fecho.RegularPositiveFlow
open TGLV350.Regular TGLExt ChatgptAudit MeasureTheory Filter
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

/-- The actual bounded resolvent belongs to the actual core. -/
theorem regularSpectralResolvent_mem (Q : F1Fecho.RegularCovariantCore.UnitaryFlow H) (M : VonNeumannAlgebra H) :
    regularSpectralResolvent Q ∈ RegularCovariantCore.core Q M := by
  rw [← VonNeumannAlgebra.commutant_commutant (RegularCovariantCore.core Q M),
    VonNeumannAlgebra.mem_commutant_iff]
  intro B hB
  let V := regularSpectralCoordinates Q
  let C := V.symm.conjStarAlgEquiv B
  have hC (x : RegularHilbert (H)) : V (C x) = B (V x) := by
    change V (V.symm (B (V x))) = _
    exact V.apply_symm_apply _
  have hchar : ∀ s : ℝ, characterMultiplier s * C = C * characterMultiplier s := by
    intro s
    let t := s/(2*Real.pi)
    have ht : 2*Real.pi*t = s := by
      dsimp only [t]
      field_simp
    have hv (x : RegularHilbert (H)) :
        V (characterMultiplier s x) = RegularCovariantCore.regularUnitary Q t (V x) := by
      simpa only [ht] using regularSpectralCoordinates_character Q t x
    ext1 x
    apply V.injective
    change V (characterMultiplier s (C x)) = V (C (characterMultiplier s x))
    rw [hv, hC, hC, hv]
    exact congrArg (fun A : RegularHilbert (H) →L[ℂ] RegularHilbert (H) => A (V x))
      ((VonNeumannAlgebra.mem_commutant_iff.mp hB) _ (RegularCovariantCore.regular_mem Q M t))
  let g : ℝ → ℝ := fun ξ => Real.sigmoid (2*Real.pi*ξ)
  have hg : Continuous g := by fun_prop
  have h0 : ∀ ξ, 0 ≤ g ξ := fun ξ => Real.sigmoid_nonneg _
  have h1 : ∀ ξ, g ξ ≤ 1 := fun ξ => Real.sigmoid_le_one _
  let M := realScalarMultiplier (H := H) g hg h0 h1
  have hr : V.symm.conjStarAlgEquiv (regularSpectralResolvent Q) = M := by
    ext1 x
    change V.symm (regularSpectralResolvent Q (V x)) = M x
    change V.symm (V (M (V.symm (V x)))) = M x
    rw [V.symm_apply_apply, V.symm_apply_apply]
  apply V.symm.conjStarAlgEquiv.injective
  change V.symm.conjStarAlgEquiv (B * regularSpectralResolvent Q) =
    V.symm.conjStarAlgEquiv (regularSpectralResolvent Q * B)
  rw [map_mul, map_mul, hr]
  exact (character_commutation_realScalarMultiplier C hchar g hg h0 h1).symm

/-- Affiliation expressed directly as graph commutation for every bounded
operator in N'. Together with the already proved closedness this is the usual
commutant criterion; no new affiliated-form object replaces the operator. -/
theorem regularPositiveGenerator_commutant_graph (Q : F1Fecho.RegularCovariantCore.UnitaryFlow H) (M : VonNeumannAlgebra H)
    (B : RegularHilbert (H) →L[ℂ] RegularHilbert (H))
    (hB : B ∈ (RegularCovariantCore.core Q M).commutant)
    (x y : RegularHilbert (H))
    (hxy : (x,y) ∈ (regularPositiveGenerator Q).graph) :
    (B x,B y) ∈ (regularPositiveGenerator Q).graph := by
  let R := regularSpectralResolvent Q
  have hc : R * B = B * R :=
    (VonNeumannAlgebra.mem_commutant_iff.mp hB) _ (regularSpectralResolvent_mem Q M)
  have he (u : RegularHilbert (H)) : R (B u) = B (R u) :=
    congrArg (fun A : RegularHilbert (H) →L[ℂ] RegularHilbert (H) => A u) hc
  change (x,y) ∈ (resolventGraphOperator R (regularSpectralResolvent_injective Q)).graph at hxy
  rw [resolvent_graph_equation] at hxy
  change (B x,B y) ∈ (resolventGraphOperator R (regularSpectralResolvent_injective Q)).graph
  rw [resolvent_graph_equation]
  change B x - R (B x) = R (B y)
  change x-R x = R y at hxy
  rw [he, he, ← map_sub, hxy]


end F1Fecho.RegularPositiveFlow
#print axioms F1Fecho.RegularPositiveFlow.regularSpectralResolvent_mem
#print axioms F1Fecho.RegularPositiveFlow.regularPositiveGenerator_commutant_graph
