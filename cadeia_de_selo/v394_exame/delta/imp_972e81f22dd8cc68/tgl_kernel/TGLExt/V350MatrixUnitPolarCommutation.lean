import TGLExt.V350MatrixUnitPolarTransport

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1500000

namespace TGLV350.Regular
open TGLExt ChatgptAudit.Continuous049 ChatgptAudit
noncomputable section

/-- Every constructed homogeneous right multiplier commutes with the full
represented left algebra, by associativity on nν followed by density. -/
theorem homogeneousRightGNS_commutes_left {P : SiteProfile} (d : HomogeneousRightData P)
    (B : (regularCoreAlgebra P).toStarSubalgebra) :
    Commute (homogeneousRightGNS d) (scalarGNSRepresentation P B) := by
  apply ContinuousLinearMap.ext
  intro z
  change homogeneousRightGNS d (scalarGNSRepresentation P B z) =
    scalarGNSRepresentation P B (homogeneousRightGNS d z)
  refine (scalarWeightGNSEmbedding_denseRange P).induction ?_
    (isClosed_eq ((homogeneousRightGNS d).continuous.comp (scalarGNSRepresentation P B).continuous)
      ((scalarGNSRepresentation P B).continuous.comp (homogeneousRightGNS d).continuous)) z
  rintro _ ⟨a,rfl⟩
  have hp : scalarHomogeneousRightProduct d (scalarWeightLeftProduct P B a) =
      scalarWeightLeftProduct P B (scalarHomogeneousRightProduct d a) := by
    apply Subtype.ext
    exact mul_assoc B a.val (homogeneousRightCoreElement d)
  calc
    _ = homogeneousRightGNS d (scalarWeightGNSEmbedding P (scalarWeightLeftProduct P B a)) :=
      congrArg (homogeneousRightGNS d) (scalarWeightGNSAction_intertwines P B a)
    _ = scalarWeightGNSEmbedding P (scalarHomogeneousRightProduct d (scalarWeightLeftProduct P B a)) :=
      homogeneousRightGNS_intertwines d (scalarWeightLeftProduct P B a)
    _ = scalarWeightGNSEmbedding P (scalarWeightLeftProduct P B (scalarHomogeneousRightProduct d a)) :=
      congrArg (scalarWeightGNSEmbedding P) hp
    _ = scalarGNSRepresentation P B (scalarWeightGNSEmbedding P (scalarHomogeneousRightProduct d a)) :=
      (scalarWeightGNSAction_intertwines P B (scalarHomogeneousRightProduct d a)).symm
    _ = _ := congrArg (scalarGNSRepresentation P B) (homogeneousRightGNS_intertwines d a).symm

theorem matrixUnit_polar_conjugate_generator (P : SiteProfile) (N : ℕ) (i j : chainIdx N) :
    antiunitaryConjugate (scalarTomitaPolarFactor P)
      (scalarGNSRepresentation P (homogeneousRightCoreElement (matrixUnitRightData P N i j))) =
    (Real.sqrt (localEigenvalue P N j i) : ℂ) • homogeneousRightGNS (matrixUnitRightData P N j i) := by
  have hh := matrixUnit_polar_conjugate_left P N j i
  rw [← matrixUnit_rightCore_star P N j i] at hh
  exact hh

/-- This covers each local base matrix unit, not yet the entire bicommutant. -/
theorem matrixUnit_polar_generator_commutes (P : SiteProfile) (N : ℕ) (i j : chainIdx N)
    (B : (regularCoreAlgebra P).toStarSubalgebra) :
    Commute (antiunitaryConjugate (scalarTomitaPolarFactor P)
      (scalarGNSRepresentation P (homogeneousRightCoreElement (matrixUnitRightData P N i j))))
        (scalarGNSRepresentation P B) := by
  rw [matrixUnit_polar_conjugate_generator]
  apply ContinuousLinearMap.ext
  intro z
  have hh := congrArg (fun F : ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P => F z)
    (homogeneousRightGNS_commutes_left (matrixUnitRightData P N j i) B).eq
  change (Real.sqrt (localEigenvalue P N j i) : ℂ) •
    homogeneousRightGNS (matrixUnitRightData P N j i) (scalarGNSRepresentation P B z) =
    scalarGNSRepresentation P B ((Real.sqrt (localEigenvalue P N j i) : ℂ) •
      homogeneousRightGNS (matrixUnitRightData P N j i) z)
  rw [map_smul]
  exact congrArg (fun v : ScalarGNSHilbert P => (Real.sqrt (localEigenvalue P N j i) : ℂ) • v) hh

#print axioms homogeneousRightGNS_commutes_left
#print axioms matrixUnit_polar_conjugate_generator
#print axioms matrixUnit_polar_generator_commutes
end
end TGLV350.Regular
