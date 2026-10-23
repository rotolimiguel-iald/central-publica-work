import TGLExt.V350HomogeneousRightData
import TGLExt.V350ScalarHomogeneousRightOrbit
import TGLExt.V350ScalarWeightAction

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1500000

namespace TGLV350.Regular
open TGLExt ChatgptAudit MeasureTheory
noncomputable section

def scalarHomogeneousRightProduct {P : SiteProfile} (d : HomogeneousRightData P)
    (A : scalarWeightLeftIdeal P) : scalarWeightLeftIdeal P :=
  ⟨⟨A.val.val * fibre d.left,
    (regularCoreAlgebra P).mul_mem A.val.property (amplified_factor_mem P d.left d.left_mem)⟩,
    scalarWeight_right_homogeneous_finite P d.right d.left d.frequency
      d.right_mem d.homogeneous d.vacuum A⟩

theorem scalarHomogeneousRightOrbit_intertwines {P : SiteProfile}
    (d : HomogeneousRightData P) (A : scalarWeightLeftIdeal P) :
    homogeneousRightAmbient d (scalarWeightOrbit P A) =
      scalarWeightOrbit P (scalarHomogeneousRightProduct d A) := by
  apply Lp.ext
  filter_upwards [fibre_ae (fibre d.right) (shift d.frequency (scalarWeightOrbit P A)),
    shift_ae d.frequency (scalarWeightOrbit P A),
    (measurePreserving_sub_right volume d.frequency).quasiMeasurePreserving.ae
      (scalarWeightOrbit_ae P A),
    scalarWeightOrbit_ae P (scalarHomogeneousRightProduct d A)] with s h1 h2 h3 h4
  change fibre (fibre d.right) (shift d.frequency (scalarWeightOrbit P A)) s = _
  rw [h1,h2,h3,h4]
  change fibre d.right ((↑(Real.sqrt dualHaarFactor) : ℂ) •
    dualAmbient (s-d.frequency) A.val.val (regularVacuum P)) =
    (↑(Real.sqrt dualHaarFactor) : ℂ) •
      dualAmbient s (A.val.val * fibre d.left) (regularVacuum P)
  rw [map_smul,scalarOrbit_right_homogeneous P d.right d.left d.frequency
    d.right_mem d.homogeneous d.vacuum A.val s]

theorem homogeneousRightAmbient_preserves_GNS {P : SiteProfile}
    (d : HomogeneousRightData P) :
    ∀ v ∈ scalarGNSSubspace P, homogeneousRightAmbient d v ∈ scalarGNSSubspace P := by
  have h : Set.MapsTo (homogeneousRightAmbient d)
      ((scalarWeightLinear P).range : Set _) ((scalarWeightLinear P).range : Set _) := by
    rintro v ⟨A,rfl⟩
    exact ⟨scalarHomogeneousRightProduct d A,(scalarHomogeneousRightOrbit_intertwines d A).symm⟩
  rw [← scalarWeight_completion_eq P]
  exact h.closure (homogeneousRightAmbient d).continuous

def homogeneousRightGNS {P : SiteProfile} (d : HomogeneousRightData P) :
    ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P :=
  (homogeneousRightAmbient d).restrict (homogeneousRightAmbient_preserves_GNS d)

theorem homogeneousRightGNS_intertwines {P : SiteProfile}
    (d : HomogeneousRightData P) (A : scalarWeightLeftIdeal P) :
    homogeneousRightGNS d (scalarWeightGNSEmbedding P A) =
      scalarWeightGNSEmbedding P (scalarHomogeneousRightProduct d A) :=
  Subtype.ext (scalarHomogeneousRightOrbit_intertwines d A)

theorem homogeneousRightGNS_adjoint {P : SiteProfile}
    (d e : HomogeneousRightData P) (hR : e.right = star d.right)
    (hc : e.frequency = -d.frequency) :
    star (homogeneousRightGNS d) = homogeneousRightGNS e := by
  ext1 v
  apply ext_inner_left ℂ
  intro w
  rw [ContinuousLinearMap.star_eq_adjoint,ContinuousLinearMap.adjoint_inner_right]
  change inner ℂ (homogeneousRightAmbient d w.val) v.val =
    inner ℂ w.val (homogeneousRightAmbient e v.val)
  rw [← homogeneousRightAmbient_adjoint d e hR hc,ContinuousLinearMap.star_eq_adjoint,
    ContinuousLinearMap.adjoint_inner_right]

/-- A pairing on the full scalar-weight domain in the same GNS Hilbert space.
It is a right-adjoint identity, not yet a global strip-analytic KMS theorem. -/
theorem scalarWeight_right_adjoint_pairing {P : SiteProfile}
    (d e : HomogeneousRightData P) (hR : e.right = star d.right)
    (hc : e.frequency = -d.frequency) (A B : scalarWeightLeftIdeal P) :
    inner ℂ (scalarWeightGNSEmbedding P (scalarHomogeneousRightProduct d A))
      (scalarWeightGNSEmbedding P B) =
    inner ℂ (scalarWeightGNSEmbedding P A)
      (scalarWeightGNSEmbedding P (scalarHomogeneousRightProduct e B)) := by
  have hA := homogeneousRightGNS_intertwines d A
  have hB := homogeneousRightGNS_intertwines e B
  have ha : (homogeneousRightGNS d).adjoint = homogeneousRightGNS e :=
    homogeneousRightGNS_adjoint d e hR hc
  calc
    _ = inner ℂ (homogeneousRightGNS d (scalarWeightGNSEmbedding P A))
        (scalarWeightGNSEmbedding P B) :=
      congrArg (fun v : ScalarGNSHilbert P => inner ℂ v (scalarWeightGNSEmbedding P B)) hA.symm
    _ = inner ℂ (scalarWeightGNSEmbedding P A)
        ((homogeneousRightGNS d).adjoint (scalarWeightGNSEmbedding P B)) :=
      (ContinuousLinearMap.adjoint_inner_right (homogeneousRightGNS d)
        (scalarWeightGNSEmbedding P A) (scalarWeightGNSEmbedding P B)).symm
    _ = inner ℂ (scalarWeightGNSEmbedding P A)
        (homogeneousRightGNS e (scalarWeightGNSEmbedding P B)) :=
      congrArg (fun T : ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P =>
        inner ℂ (scalarWeightGNSEmbedding P A) (T (scalarWeightGNSEmbedding P B))) ha
    _ = _ := congrArg (fun v : ScalarGNSHilbert P =>
      inner ℂ (scalarWeightGNSEmbedding P A) v) hB

theorem matrixUnitRightGNS_adjoint (P : SiteProfile) (N : ℕ) (i j : chainIdx N) :
    star (homogeneousRightGNS (matrixUnitRightData P N i j)) =
      homogeneousRightGNS (matrixUnitTwistedRightData P N i j) :=
  homogeneousRightGNS_adjoint _ _ rfl rfl

theorem matrixUnit_scalarWeight_pairing (P : SiteProfile) (N : ℕ) (i j : chainIdx N)
    (A B : scalarWeightLeftIdeal P) :
    inner ℂ (scalarWeightGNSEmbedding P
      (scalarHomogeneousRightProduct (matrixUnitRightData P N i j) A))
      (scalarWeightGNSEmbedding P B) =
    inner ℂ (scalarWeightGNSEmbedding P A) (scalarWeightGNSEmbedding P
      (scalarHomogeneousRightProduct (matrixUnitTwistedRightData P N i j) B)) :=
  scalarWeight_right_adjoint_pairing _ _ rfl rfl A B

#print axioms scalarHomogeneousRightProduct
#print axioms scalarHomogeneousRightOrbit_intertwines
#print axioms homogeneousRightAmbient_preserves_GNS
#print axioms homogeneousRightGNS
#print axioms homogeneousRightGNS_intertwines
#print axioms homogeneousRightGNS_adjoint
#print axioms scalarWeight_right_adjoint_pairing
#print axioms matrixUnitRightGNS_adjoint
#print axioms matrixUnit_scalarWeight_pairing
end
end TGLV350.Regular
