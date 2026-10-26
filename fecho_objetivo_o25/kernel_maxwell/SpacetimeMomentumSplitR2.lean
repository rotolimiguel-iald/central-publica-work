import MaxwellShellGeometryR3
import Mathlib.Analysis.Normed.Module.FiniteDimension

/-! Explicit coordinate equivalence: (p0,p1,p2,p3) to (p0,((p2,p3),p1)).
This is a coordinate change, not a physical Lorentz transformation. -/
set_option autoImplicit false
noncomputable section
namespace F1Fecho.MaxwellGlobal
open Matrix ChatgptAudit.WignerRapidityMeasure016 ChatgptAudit.WignerOrbit016

def splitMomentumLinear : Spacetime ≃ₗ[ℝ] ℝ×MomentumCoordinates where
  toFun p := (p 0,(![p 2,p 3],p 1))
  invFun z := WithLp.toLp 2 ![z.1,z.2.2,z.2.1 0,z.2.1 1]
  left_inv p := by
    apply PiLp.ext
    intro i
    fin_cases i <;> rfl
  right_inv z := by
    apply Prod.ext
    · rfl
    · apply Prod.ext
      · ext i
        fin_cases i <;> rfl
      · rfl
  map_add' p q := by
    apply Prod.ext
    · rfl
    · apply Prod.ext
      · ext i
        fin_cases i <;> rfl
      · rfl
  map_smul' a p := by
    apply Prod.ext
    · rfl
    · apply Prod.ext
      · ext i
        fin_cases i <;> rfl
      · rfl

def splitMomentum : Spacetime ≃L[ℝ] ℝ×MomentumCoordinates :=
  splitMomentumLinear.toContinuousLinearEquiv

theorem splitMomentum_shell (y : MomentumCoordinates) :
    splitMomentum (shellEmbedding y)=(shellEnergy y,y) := by
  rcases y with ⟨q,l⟩
  change (energy (transverseMass 0 q) l,(![q 0,q 1],l))=
    (shellEnergy (q,l),(q,l))
  congr 2
  ext i
  fin_cases i <;> rfl

end F1Fecho.MaxwellGlobal
#print axioms F1Fecho.MaxwellGlobal.splitMomentum_shell
