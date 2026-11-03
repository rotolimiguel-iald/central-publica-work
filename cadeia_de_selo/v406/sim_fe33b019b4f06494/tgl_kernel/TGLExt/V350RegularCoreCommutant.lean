import TGLExt.V350TwistedCommutantField

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 700000

namespace TGLV350.Regular
open TGLExt ChatgptAudit
noncomputable section

/-- Commutation with the two star-closed generating families extends to N.
The adjoint of the prospective commutant element is handled algebraically. -/
theorem mem_regularCommutant_of_generators (P : SiteProfile)
    (T : RegularHilbert (TowerHilbert P) →L[ℂ] RegularHilbert (TowerHilbert P))
    (hM : ∀ A ∈ theFactorObject P, T * fibre A = fibre A * T)
    (hU : ∀ t : ℝ, T * regularUnitary P t = regularUnitary P t * T) :
    T ∈ (regularCoreAlgebra P).commutant := by
  have hN : regularCoreAlgebra P ≤ starCommutantAlgebra {T} := by
    apply regularCore_minimal
    · intro A hA
      change fibre A ∈ StarSubalgebra.centralizer ℂ {T}
      rw [StarSubalgebra.mem_centralizer_iff]
      intro B hB
      have he : B = T := Set.mem_singleton_iff.mp hB
      subst B
      refine ⟨hM A hA, ?_⟩
      have hs := congrArg star (hM (star A) (star_mem hA))
      rw [fibre_star] at hs
      simpa only [star_mul, star_star] using hs.symm
    · intro t
      change regularUnitary P t ∈ StarSubalgebra.centralizer ℂ {T}
      rw [StarSubalgebra.mem_centralizer_iff]
      intro B hB
      have he : B = T := Set.mem_singleton_iff.mp hB
      subst B
      refine ⟨hU t, ?_⟩
      have hs := congrArg star (hU (-t))
      simpa only [star_mul, regular_star, neg_neg] using hs.symm
  rw [VonNeumannAlgebra.mem_commutant_iff]
  intro A hA
  have hm := hN hA
  change A ∈ StarSubalgebra.centralizer ℂ {T} at hm
  rw [StarSubalgebra.mem_centralizer_iff] at hm
  exact (hm T (Set.mem_singleton T)).1.symm

theorem twistedCommutantLift_mem (P : SiteProfile)
    (D : TowerHilbert P →L[ℂ] TowerHilbert P)
    (hD : D ∈ (theFactorObject P).commutant) :
    operatorFieldLift (twistedCommutantField P D) ∈ (regularCoreAlgebra P).commutant := by
  apply mem_regularCommutant_of_generators
  · intro A hA
    apply operatorFieldLift_commutes_fibre
    intro x
    exact ((VonNeumannAlgebra.mem_commutant_iff.mp
      (modularConjugation_preserves_commutant P x D hD)) A hA).symm
  · exact operatorFieldLift_commutes_regular_of_intertwining P _
      (twistedCommutantField_intertwines P D)

/-- A constant fibre in the regular core comes from the original base M.
The test against every D in M' is made with a strongly continuous twisted
field; equality in L² is reflected before evaluation at zero. -/
theorem fibre_mem_regularCore_iff (P : SiteProfile)
    (C : TowerHilbert P →L[ℂ] TowerHilbert P) :
    fibre C ∈ regularCoreAlgebra P ↔ C ∈ theFactorObject P := by
  constructor
  · intro hC
    rw [← VonNeumannAlgebra.commutant_commutant (theFactorObject P),
      VonNeumannAlgebra.mem_commutant_iff]
    intro D hD
    have he := (VonNeumannAlgebra.mem_commutant_iff.mp
      (twistedCommutantLift_mem P D hD)) (fibre C) hC
    have hzero := operatorFieldLift_commutation_reflects
      (twistedCommutantField P D) C he.symm 0
    rwa [twistedCommutantField_zero] at hzero
  · exact amplified_factor_mem P C

#print axioms mem_regularCommutant_of_generators
#print axioms twistedCommutantLift_mem
#print axioms fibre_mem_regularCore_iff
end
end TGLV350.Regular
