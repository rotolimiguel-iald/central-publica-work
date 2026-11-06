import TGLExt.V350ScalarRightAverage
import TGLExt.V350ScalarWeightAction

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1500000

namespace TGLV350.Regular
open TGLExt ChatgptAudit MeasureTheory
noncomputable section

def regularRightCoreElement (P : SiteProfile) (t : ℝ) :
    (regularCoreAlgebra P).toStarSubalgebra :=
  ⟨regularUnitary P t,regularUnitary_mem P t⟩

theorem regularRightCoreElement_star (P : SiteProfile) (t : ℝ) :
    star (regularRightCoreElement P t) = regularRightCoreElement P (-t) :=
  Subtype.ext (regular_star P t)

theorem scalarWeight_right_regular_eq (P : SiteProfile)
    (A : (regularCoreAlgebra P).toStarSubalgebra) (t : ℝ) :
    dualQuadraticIntegral (star (A.val * regularUnitary P t) *
      (A.val * regularUnitary P t)) (regularVacuum P) =
    dualQuadraticIntegral (star A.val * A.val) (regularVacuum P) := by
  rw [star_mul]
  simpa only [mul_assoc] using dualQuadraticIntegral_regular_conjugate_vacuum P t
    (star A.val * A.val) ((regularCoreAlgebra P).mul_mem
      ((regularCoreAlgebra P).toStarSubalgebra.star_mem' A.property) A.property)

def scalarRegularRightProduct (P : SiteProfile)
    (t : ℝ) (A : scalarWeightLeftIdeal P) : scalarWeightLeftIdeal P :=
  ⟨A.val * regularRightCoreElement P t,by
    change dualQuadraticIntegral (star (A.val.val * regularUnitary P t) *
      (A.val.val * regularUnitary P t)) (regularVacuum P) < ⊤
    rw [scalarWeight_right_regular_eq]
    exact A.property⟩

/-- Right translation on the outer orbit space. The character acts on the
outer real coordinate, whereas shift acts on the inner regular Hilbert space. -/
def regularRightAmbient (P : SiteProfile) (t : ℝ) :
    RegularHilbert (RegularHilbert (TowerHilbert P)) →L[ℂ]
      RegularHilbert (RegularHilbert (TowerHilbert P)) :=
  characterMultiplier t * fibre (shift t)

theorem characterPhase_comm (s t : ℝ) : characterPhase s t = characterPhase t s := by
  unfold characterPhase
  congr 1
  ring

theorem regularRightAmbient_zero (P : SiteProfile) : regularRightAmbient P 0 = 1 := by
  simp only [regularRightAmbient,characterMultiplier_zero,shift_zero,fibre_one,one_mul]

theorem regularRightAmbient_mul (P : SiteProfile) (s t : ℝ) :
    regularRightAmbient P s * regularRightAmbient P t = regularRightAmbient P (s+t) := by
  unfold regularRightAmbient
  calc
    _ = characterMultiplier s * (fibre (shift s) * characterMultiplier t) *
        fibre (shift t) := by simp only [mul_assoc]
    _ = (characterMultiplier s * characterMultiplier t) *
        (fibre (shift s) * fibre (shift t)) := by
      rw [← characterMultiplier_commutes_fibre]
      simp only [mul_assoc]
    _ = _ := by rw [characterMultiplier_mul,← fibre_mul,shift_mul]

theorem regularRightAmbient_star (P : SiteProfile) (t : ℝ) :
    star (regularRightAmbient P t) = regularRightAmbient P (-t) := by
  simp only [regularRightAmbient,star_mul,← fibre_star,shift_star,characterMultiplier_star]
  exact (characterMultiplier_commutes_fibre _ _).symm

theorem scalarRegularRightOrbit_intertwines (P : SiteProfile)
    (t : ℝ) (A : scalarWeightLeftIdeal P) :
    regularRightAmbient P t (scalarWeightOrbit P A) =
      scalarWeightOrbit P (scalarRegularRightProduct P t A) := by
  apply Lp.ext
  filter_upwards [characterMultiplier_ae t (fibre (shift t) (scalarWeightOrbit P A)),
    fibre_ae (shift t) (scalarWeightOrbit P A),scalarWeightOrbit_ae P A,
    scalarWeightOrbit_ae P (scalarRegularRightProduct P t A)] with s h1 h2 h3 h4
  change characterMultiplier t (fibre (shift t) (scalarWeightOrbit P A)) s = _
  rw [h1,h2,h3,h4]
  change characterPhase t s • shift t ((↑(Real.sqrt dualHaarFactor) : ℂ) •
    dualAmbient s A.val.val (regularVacuum P)) =
    (↑(Real.sqrt dualHaarFactor) : ℂ) •
      dualAmbient s (A.val.val * regularUnitary P t) (regularVacuum P)
  rw [map_smul,scalarOrbit_right_regular,characterPhase_comm t s,smul_comm]

theorem regularRightAmbient_preserves_GNS (P : SiteProfile) (t : ℝ) :
    ∀ v ∈ scalarGNSSubspace P, regularRightAmbient P t v ∈ scalarGNSSubspace P := by
  have h : Set.MapsTo (regularRightAmbient P t)
      ((scalarWeightLinear P).range : Set _) ((scalarWeightLinear P).range : Set _) := by
    rintro v ⟨A,rfl⟩
    exact ⟨scalarRegularRightProduct P t A,(scalarRegularRightOrbit_intertwines P t A).symm⟩
  rw [← scalarWeight_completion_eq P]
  exact h.closure (regularRightAmbient P t).continuous

def regularRightGNS (P : SiteProfile) (t : ℝ) : ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P :=
  (regularRightAmbient P t).restrict (regularRightAmbient_preserves_GNS P t)

theorem regularRightGNS_intertwines (P : SiteProfile) (t : ℝ) (A : scalarWeightLeftIdeal P) :
    regularRightGNS P t (scalarWeightGNSEmbedding P A) =
      scalarWeightGNSEmbedding P (scalarRegularRightProduct P t A) :=
  Subtype.ext (scalarRegularRightOrbit_intertwines P t A)

theorem regularRightGNS_zero (P : SiteProfile) : regularRightGNS P 0 = 1 := by
  ext1 x
  apply Subtype.ext
  exact congrArg (fun T => T x.val) (regularRightAmbient_zero P)

theorem regularRightGNS_mul (P : SiteProfile) (s t : ℝ) :
    regularRightGNS P s * regularRightGNS P t = regularRightGNS P (s+t) := by
  ext1 x
  apply Subtype.ext
  exact congrArg (fun T => T x.val) (regularRightAmbient_mul P s t)

theorem regularRightGNS_star (P : SiteProfile) (t : ℝ) :
    star (regularRightGNS P t) = regularRightGNS P (-t) := by
  ext1 v
  apply ext_inner_left ℂ
  intro w
  rw [ContinuousLinearMap.star_eq_adjoint,ContinuousLinearMap.adjoint_inner_right]
  change inner ℂ (regularRightAmbient P t w.val) v.val =
    inner ℂ w.val (regularRightAmbient P (-t) v.val)
  rw [← regularRightAmbient_star,ContinuousLinearMap.star_eq_adjoint,
    ContinuousLinearMap.adjoint_inner_right]

theorem regularRightGNS_unitary (P : SiteProfile) (t : ℝ) :
    star (regularRightGNS P t) * regularRightGNS P t = 1 ∧
      regularRightGNS P t * star (regularRightGNS P t) = 1 := by
  simp [regularRightGNS_star,regularRightGNS_mul,regularRightGNS_zero]

#print axioms regularRightCoreElement
#print axioms regularRightCoreElement_star
#print axioms scalarWeight_right_regular_eq
#print axioms scalarRegularRightProduct
#print axioms regularRightAmbient
#print axioms characterPhase_comm
#print axioms regularRightAmbient_zero
#print axioms regularRightAmbient_mul
#print axioms regularRightAmbient_star
#print axioms scalarRegularRightOrbit_intertwines
#print axioms regularRightAmbient_preserves_GNS
#print axioms regularRightGNS
#print axioms regularRightGNS_intertwines
#print axioms regularRightGNS_zero
#print axioms regularRightGNS_mul
#print axioms regularRightGNS_star
#print axioms regularRightGNS_unitary
end
end TGLV350.Regular
