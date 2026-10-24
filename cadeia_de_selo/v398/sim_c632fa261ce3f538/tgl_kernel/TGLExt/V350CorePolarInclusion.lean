import TGLExt.V350ScalarGNSGeneratorTransport
import TGLExt.V350BasePolarStrongLimit
import TGLExt.V350ScalarRegularPolarCommutation

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1500000

namespace TGLV350.Regular
open TGLExt
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

theorem antiunitaryConjugate_involutive (U : H ≃ₛₗᵢ[starRingEnd ℂ] H)
    (hU : Function.Involutive U) : Function.Involutive (antiunitaryConjugate U) := by
  have hs : ∀ x : H, U.symm x = U x := by
    intro x
    apply U.injective
    rw [U.apply_symm_apply,hU]
  intro T
  ext1 x
  simp only [antiunitaryConjugate_apply,hs]
  exact (hU (T (U (U x)))).trans (congrArg T (hU x))

theorem antiunitaryConjugate_commutation_flip (U : H ≃ₛₗᵢ[starRingEnd ℂ] H)
    (hU : Function.Involutive U) (A B : H →L[ℂ] H)
    (h : Commute (antiunitaryConjugate U A) B) :
    Commute (antiunitaryConjugate U B) A := by
  have he := congrArg (antiunitaryConjugate U) h.eq
  rw [antiunitaryConjugate_mul,antiunitaryConjugate_mul,
    antiunitaryConjugate_involutive U hU A] at he
  exact he.symm

theorem scalarTomitaPolar_commutes_generators (P : SiteProfile)
    (B : (regularCoreAlgebra P).toStarSubalgebra) :
    ∀ A ∈ scalarCoreGenerators P,
      Commute (antiunitaryConjugate (scalarTomitaPolarFactor P)
        (scalarGNSRepresentation P B)) (scalarGNSRepresentation P A) := by
  intro A hA
  apply antiunitaryConjugate_commutation_flip (scalarTomitaPolarFactor P)
    (scalarTomitaPolarFactor_involutive P)
  rcases hA with ⟨x,hx,he⟩ | ⟨t,he⟩
  · have hAx : A = regularCoreEmbedding P ⟨x,hx⟩ := Subtype.ext he.symm
    rw [hAx]
    exact base_polar_commutes P ⟨x,hx⟩ B
  · have hAt : A = regularRightCoreElement P t := Subtype.ext he.symm
    rw [hAt]
    exact scalarTomitaPolar_regular_generator_commutes P t B

/-- The actual polar J conjugates EVERY core element into the commutant,
in the same scalar-weight GNS Hilbert space. Reverse inclusion is not asserted. -/
theorem scalarTomitaPolar_core_commutes (P : SiteProfile)
    (A B : (regularCoreAlgebra P).toStarSubalgebra) :
    Commute (antiunitaryConjugate (scalarTomitaPolarFactor P)
      (scalarGNSRepresentation P A)) (scalarGNSRepresentation P B) :=
  scalarGNS_commutation_from_generators P _ (scalarTomitaPolar_commutes_generators P A) B

theorem scalarTomitaPolar_core_commutant_mem (P : SiteProfile)
    (A : (regularCoreAlgebra P).toStarSubalgebra) :
    antiunitaryConjugate (scalarTomitaPolarFactor P) (scalarGNSRepresentation P A) ∈
      StarSubalgebra.centralizer ℂ (Set.range (scalarGNSRepresentation P)) := by
  rw [StarSubalgebra.mem_centralizer_iff]
  rintro _ ⟨B,rfl⟩
  constructor
  · exact (scalarTomitaPolar_core_commutes P A B).eq.symm
  · rw [← map_star]
    exact (scalarTomitaPolar_core_commutes P A (star B)).eq.symm

#print axioms antiunitaryConjugate_involutive
#print axioms antiunitaryConjugate_commutation_flip
#print axioms scalarTomitaPolar_commutes_generators
#print axioms scalarTomitaPolar_core_commutes
#print axioms scalarTomitaPolar_core_commutant_mem
end
end TGLV350.Regular
