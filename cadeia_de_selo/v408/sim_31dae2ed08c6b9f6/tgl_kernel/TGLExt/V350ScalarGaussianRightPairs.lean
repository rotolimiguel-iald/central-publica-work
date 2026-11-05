import TGLExt.V350ScalarPairedRightAlgebra
import TGLExt.V350ScalarGaussianGNSMap
import TGLExt.V350ScalarTomitaAdjoint

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1500000

namespace TGLV350.Regular
open TGLExt MeasureTheory
noncomputable section

private theorem gaussianSandwichAdjoint {H E : Type*}
    [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    [NormedAddCommGroup E] [InnerProductSpace ℂ E] [CompleteSpace E]
    (C : H →L[ℂ] E) (B : E →L[ℂ] E) :
    (C.adjoint.comp (B.comp C)).adjoint = C.adjoint.comp (B.adjoint.comp C) := by
  rw [ContinuousLinearMap.adjoint_comp,ContinuousLinearMap.adjoint_comp,
    ContinuousLinearMap.adjoint_adjoint]
  exact ContinuousLinearMap.comp_assoc _ _ _

/-- The original Gaussian intertwiner acts on the FULL scalar weight ideal. -/
theorem scalarGaussianGNSMap_weightEmbedding (P : SiteProfile) (a : scalarWeightLeftIdeal P) :
    scalarGaussianGNSMap P (scalarWeightGNSEmbedding P a) =
      dualOrbitRepresentation a.val.val (scalarGaussianVacuum P) := by
  apply Lp.ext
  filter_upwards [realScalarMultiplier_ae gaussianProfile gaussianProfile_continuous
    (fun s => (gaussianProfile_pos s).le) gaussianProfile_le_one (scalarWeightOrbit P a),
    scalarWeightOrbit_ae P a,scalarGaussianVacuum_ae P,
    operatorFieldLift_ae (dualIntegralFamily a.val.val) (scalarGaussianVacuum P)]
    with s h1 h2 h3 h4
  change realScalarMultiplier gaussianProfile gaussianProfile_continuous
    (fun s => (gaussianProfile_pos s).le) gaussianProfile_le_one (scalarWeightOrbit P a) s =
      operatorFieldLift (dualIntegralFamily a.val.val) (scalarGaussianVacuum P) s
  rw [h1,h2,h4,h3]
  change (gaussianProfile s : ℂ) •
      ((Real.sqrt dualHaarFactor : ℂ) • dualAmbient s a.val.val (regularVacuum P)) =
    dualAmbient s a.val.val ((gaussianProfile s : ℂ) •
      ((Real.sqrt dualHaarFactor : ℂ) • regularVacuum P))
  rw [map_smul,map_smul]

theorem scalarGaussianAdjoint_intertwines (P : SiteProfile)
    (a : (regularCoreAlgebra P).toStarSubalgebra)
    (v : RegularHilbert (RegularHilbert (TowerHilbert P))) :
    (scalarGaussianGNSMap P).adjoint (dualOrbitRepresentation a.val v) =
      scalarGNSRepresentation P a ((scalarGaussianGNSMap P).adjoint v) := by
  apply ext_inner_left ℂ
  intro x
  calc
    _ = inner ℂ (scalarGaussianGNSMap P x) (dualOrbitRepresentation a.val v) :=
      (scalarGaussianGNSMap P).adjoint_inner_right x _
    _ = inner ℂ (dualOrbitRepresentation (star a).val (scalarGaussianGNSMap P x)) v := by
      have hs : dualOrbitRepresentation (star a).val = (dualOrbitRepresentation a.val).adjoint :=
        map_star dualOrbitRepresentation a.val
      exact ((dualOrbitRepresentation a.val).adjoint_inner_left _ _).symm.trans
        (congrArg (fun B : RegularHilbert (RegularHilbert (TowerHilbert P)) →L[ℂ]
          RegularHilbert (RegularHilbert (TowerHilbert P)) =>
          inner ℂ (B (scalarGaussianGNSMap P x)) v) hs.symm)
    _ = inner ℂ (scalarGaussianGNSMap P (scalarGNSRepresentation P (star a) x)) v :=
      congrArg (fun z => inner ℂ z v) (scalarGaussianGNSMap_intertwines P (star a) x).symm
    _ = inner ℂ (scalarGNSRepresentation P (star a) x) ((scalarGaussianGNSMap P).adjoint v) :=
      ((scalarGaussianGNSMap P).adjoint_inner_right _ _).symm
    _ = _ := by
      have hs : scalarGNSRepresentation P (star a) = (scalarGNSRepresentation P a).adjoint :=
        map_star (scalarGNSRepresentation P) a
      exact (congrArg (fun B : ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P =>
        inner ℂ (B x) ((scalarGaussianGNSMap P).adjoint v)) hs).trans
        ((scalarGNSRepresentation P a).adjoint_inner_left _ _)

def scalarGaussianRightOperator (P : SiteProfile)
    (B : RegularHilbert (RegularHilbert (TowerHilbert P)) →L[ℂ]
      RegularHilbert (RegularHilbert (TowerHilbert P))) :
    ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P :=
  (scalarGaussianGNSMap P).adjoint.comp (B.comp (scalarGaussianGNSMap P))

theorem scalarGaussianRightOperator_adjoint (P : SiteProfile)
    (B : RegularHilbert (RegularHilbert (TowerHilbert P)) →L[ℂ]
      RegularHilbert (RegularHilbert (TowerHilbert P))) :
    star (scalarGaussianRightOperator P B) = scalarGaussianRightOperator P (star B) := by
  exact gaussianSandwichAdjoint (scalarGaussianGNSMap P) B

theorem scalarGaussianRightOperator_right (P : SiteProfile)
    (B : RegularHilbert (RegularHilbert (TowerHilbert P)) →L[ℂ]
      RegularHilbert (RegularHilbert (TowerHilbert P)))
    (hB : B ∈ (dualOrbitVonNeumann (regularCoreAlgebra P)).commutant)
    (a : scalarWeightLeftIdeal P) :
    scalarGaussianRightOperator P B (scalarWeightGNSEmbedding P a) =
      scalarGNSRepresentation P a.val
        ((scalarGaussianGNSMap P).adjoint (B (scalarGaussianVacuum P))) := by
  have hm : dualOrbitRepresentation a.val.val ∈ dualOrbitVonNeumann (regularCoreAlgebra P) :=
    (mem_dualOrbitVonNeumann_iff (regularCoreAlgebra P)
      (dualOrbitRepresentation a.val.val)).mpr ⟨a.val.val,a.val.property,rfl⟩
  have hc : dualOrbitRepresentation a.val.val * B = B * dualOrbitRepresentation a.val.val :=
    (VonNeumannAlgebra.mem_commutant_iff.mp hB) (dualOrbitRepresentation a.val.val) hm
  change (scalarGaussianGNSMap P).adjoint
    (B (scalarGaussianGNSMap P (scalarWeightGNSEmbedding P a))) = _
  calc
    _ = (scalarGaussianGNSMap P).adjoint
        (B (dualOrbitRepresentation a.val.val (scalarGaussianVacuum P))) :=
      congrArg (fun z => (scalarGaussianGNSMap P).adjoint (B z))
        (scalarGaussianGNSMap_weightEmbedding P a)
    _ = (scalarGaussianGNSMap P).adjoint
        (dualOrbitRepresentation a.val.val (B (scalarGaussianVacuum P))) :=
      congrArg (fun z => (scalarGaussianGNSMap P).adjoint z)
        (congrArg (fun T : RegularHilbert (RegularHilbert (TowerHilbert P)) →L[ℂ]
          RegularHilbert (RegularHilbert (TowerHilbert P)) => T (scalarGaussianVacuum P)) hc.symm)
    _ = _ := scalarGaussianAdjoint_intertwines P a.val _

/-- Genuine bounded right pairs in the SAME scalar GNS realization.
The auxiliary state only supplies vectors; the adjoint relation uses original F. -/
def scalarGaussianRightAdjointPair (P : SiteProfile)
    (B : RegularHilbert (RegularHilbert (TowerHilbert P)) →L[ℂ]
      RegularHilbert (RegularHilbert (TowerHilbert P)))
    (hB : B ∈ (dualOrbitVonNeumann (regularCoreAlgebra P)).commutant) :
    ScalarRightAdjointPair P (scalarGaussianRightOperator P B) where
  vector := (scalarGaussianGNSMap P).adjoint (B (scalarGaussianVacuum P))
  adjointVector := (scalarGaussianGNSMap P).adjoint (star B (scalarGaussianVacuum P))
  right := scalarGaussianRightOperator_right P B hB
  adjoint := by
    intro a
    rw [scalarGaussianRightOperator_adjoint]
    exact scalarGaussianRightOperator_right P (star B)
      ((dualOrbitVonNeumann (regularCoreAlgebra P)).commutant.toStarSubalgebra.star_mem' hB) a

#print axioms scalarGaussianGNSMap_weightEmbedding
#print axioms scalarGaussianAdjoint_intertwines
#print axioms scalarGaussianRightOperator
#print axioms scalarGaussianRightOperator_adjoint
#print axioms scalarGaussianRightOperator_right
#print axioms scalarGaussianRightAdjointPair
end
end TGLV350.Regular
