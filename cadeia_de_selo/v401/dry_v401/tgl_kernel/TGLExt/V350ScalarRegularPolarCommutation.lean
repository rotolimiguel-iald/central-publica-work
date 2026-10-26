import TGLExt.V350ScalarRegularRightPolar

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1500000

namespace TGLV350.Regular
open TGLExt ChatgptAudit.Continuous049
noncomputable section

/-- Associativity on the full scalar-weight ideal, followed by density,
proves commutation with EVERY represented left algebra element. -/
theorem regularRightGNS_commutes_left (P : SiteProfile) (t : ℝ)
    (B : (regularCoreAlgebra P).toStarSubalgebra) :
    Commute (regularRightGNS P t) (scalarGNSRepresentation P B) := by
  apply ContinuousLinearMap.ext
  intro z
  change regularRightGNS P t (scalarGNSRepresentation P B z) =
    scalarGNSRepresentation P B (regularRightGNS P t z)
  refine (scalarWeightGNSEmbedding_denseRange P).induction ?_
    (isClosed_eq ((regularRightGNS P t).continuous.comp (scalarGNSRepresentation P B).continuous)
      ((scalarGNSRepresentation P B).continuous.comp (regularRightGNS P t).continuous)) z
  rintro _ ⟨a,rfl⟩
  have hp : scalarRegularRightProduct P t (scalarWeightLeftProduct P B a) =
      scalarWeightLeftProduct P B (scalarRegularRightProduct P t a) := by
    apply Subtype.ext
    exact mul_assoc B a.val (regularRightCoreElement P t)
  calc
    _ = regularRightGNS P t (scalarWeightGNSEmbedding P (scalarWeightLeftProduct P B a)) :=
      congrArg (regularRightGNS P t) (scalarWeightGNSAction_intertwines P B a)
    _ = scalarWeightGNSEmbedding P (scalarRegularRightProduct P t (scalarWeightLeftProduct P B a)) :=
      regularRightGNS_intertwines P t (scalarWeightLeftProduct P B a)
    _ = scalarWeightGNSEmbedding P (scalarWeightLeftProduct P B (scalarRegularRightProduct P t a)) :=
      congrArg (scalarWeightGNSEmbedding P) hp
    _ = scalarGNSRepresentation P B (scalarWeightGNSEmbedding P (scalarRegularRightProduct P t a)) :=
      (scalarWeightGNSAction_intertwines P B (scalarRegularRightProduct P t a)).symm
    _ = _ := congrArg (scalarGNSRepresentation P B) (regularRightGNS_intertwines P t a).symm

theorem scalarTomitaPolar_conjugate_regular_left (P : SiteProfile) (t : ℝ) :
    antiunitaryConjugate (scalarTomitaPolarFactor P)
      (scalarGNSRepresentation P (star (regularRightCoreElement P t))) =
        regularRightGNS P t := by
  apply ContinuousLinearMap.ext
  intro x
  have h := scalarTomitaPolarFactor_regular_left P t ((scalarTomitaPolarFactor P).symm x)
  simpa only [antiunitaryConjugate_apply,LinearIsometryEquiv.apply_symm_apply] using h

/-- A generator identity for the actual polar factor of the weight's S.
This is not an equality of the whole represented algebra and its commutant. -/
theorem scalarTomitaPolar_regular_generator (P : SiteProfile) (t : ℝ) :
    antiunitaryConjugate (scalarTomitaPolarFactor P)
      (scalarGNSRepresentation P (regularRightCoreElement P t)) =
        regularRightGNS P (-t) := by
  have h := scalarTomitaPolar_conjugate_regular_left P (-t)
  simpa only [regularRightCoreElement_star,neg_neg] using h

theorem scalarTomitaPolar_regular_generator_commutes (P : SiteProfile) (t : ℝ)
    (B : (regularCoreAlgebra P).toStarSubalgebra) :
    Commute (antiunitaryConjugate (scalarTomitaPolarFactor P)
      (scalarGNSRepresentation P (regularRightCoreElement P t)))
        (scalarGNSRepresentation P B) := by
  rw [scalarTomitaPolar_regular_generator]
  exact regularRightGNS_commutes_left P (-t) B

#print axioms regularRightGNS_commutes_left
#print axioms scalarTomitaPolar_conjugate_regular_left
#print axioms scalarTomitaPolar_regular_generator
#print axioms scalarTomitaPolar_regular_generator_commutes
end
end TGLV350.Regular
