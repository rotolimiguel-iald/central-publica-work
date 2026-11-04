import TGLExt.V350MatrixUnitPolarCommutation
import TGLExt.ChainPrefix
import Mathlib.Data.Matrix.Basis

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1500000

namespace TGLV350.Regular
open TGLExt ChatgptAudit
noncomputable section

theorem antiunitaryConjugate_add {H : Type} [NormedAddCommGroup H]
    [InnerProductSpace ℂ H] [CompleteSpace H] (U : H ≃ₛₗᵢ[starRingEnd ℂ] H)
    (T V : H →L[ℂ] H) :
    antiunitaryConjugate U (T+V) = antiunitaryConjugate U T + antiunitaryConjugate U V := by
  ext x
  change U (T (U.symm x) + V (U.symm x)) = U (T (U.symm x)) + U (V (U.symm x))
  exact map_add U _ _

theorem antiunitaryConjugate_smul {H : Type} [NormedAddCommGroup H]
    [InnerProductSpace ℂ H] [CompleteSpace H] (U : H ≃ₛₗᵢ[starRingEnd ℂ] H)
    (c : ℂ) (T : H →L[ℂ] H) :
    antiunitaryConjugate U (c • T) = star c • antiunitaryConjugate U T := by
  ext x
  change U (c • T (U.symm x)) = star c • U (T (U.symm x))
  exact map_smulₛₗ U c _

def localBaseCore (P : SiteProfile) (N : ℕ) :
    Matrix (chainIdx N) (chainIdx N) ℂ →ₗ[ℂ] (regularCoreAlgebra P).toStarSubalgebra where
  toFun a := regularCoreEmbedding P ⟨towerPi P a,towerPi_mem_factor a⟩
  map_add' a b := by
    apply Subtype.ext
    change fibre (towerPi P (a+b)) = fibre (towerPi P a) + fibre (towerPi P b)
    rw [towerPi_add,fibre_add]
  map_smul' c a := by
    apply Subtype.ext
    change fibre (towerPi P (c • a)) = c • fibre (towerPi P a)
    rw [towerPi_smul,fibre_smul]

theorem matrix_linear_polar_commutes {H : Type} [NormedAddCommGroup H]
    [InnerProductSpace ℂ H] [CompleteSpace H] {m n : Type*}
    [Fintype m] [Fintype n] [DecidableEq m] [DecidableEq n]
    (U : H ≃ₛₗᵢ[starRingEnd ℂ] H) (F : Matrix m n ℂ →ₗ[ℂ] (H →L[ℂ] H))
    (B : H →L[ℂ] H)
    (hunit : ∀ i j, Commute (antiunitaryConjugate U (F (Matrix.single i j 1))) B)
    (a : Matrix m n ℂ) : Commute (antiunitaryConjugate U (F a)) B := by
  induction a using Matrix.induction_on' with
  | h_zero =>
      rw [map_zero]
      apply ContinuousLinearMap.ext
      intro z
      simp [antiunitaryConjugate_apply]
  | h_add a b ha hb =>
      rw [map_add,antiunitaryConjugate_add]
      exact ha.add_left hb
  | h_std_basis i j c =>
      have he : Matrix.single i j c = c • Matrix.single i j (1 : ℂ) := by
        simp only [Matrix.smul_single,smul_eq_mul,mul_one]
      have hF : F (Matrix.single i j c) = c • F (Matrix.single i j 1) := by
        rw [he]
        exact F.map_smul c _
      rw [hF,antiunitaryConjugate_smul U c]
      have hh := hunit i j
      apply ContinuousLinearMap.ext
      intro z
      have hv := congrArg (fun T : H →L[ℂ] H => T z) hh.eq
      change star c • (antiunitaryConjugate U (F (Matrix.single i j 1))) (B z) =
        B (star c • (antiunitaryConjugate U (F (Matrix.single i j 1))) z)
      rw [map_smul]
      exact congrArg (fun v : H => star c • v) hv

/-- The same polar conjugation now commutes with all represented elements
for every matrix at every finite level, including arbitrary complex coefficients. -/
theorem localBase_polar_commutes (P : SiteProfile) (N : ℕ)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) (B : (regularCoreAlgebra P).toStarSubalgebra) :
    Commute (antiunitaryConjugate (scalarTomitaPolarFactor P)
      (scalarGNSRepresentation P (localBaseCore P N a))) (scalarGNSRepresentation P B) :=
  matrix_linear_polar_commutes (scalarTomitaPolarFactor P)
    ((scalarGNSRepresentation P).toLinearMap.comp (localBaseCore P N))
    (scalarGNSRepresentation P B) (fun i j => matrixUnit_polar_generator_commutes P N i j B) a

#print axioms antiunitaryConjugate_add
#print axioms antiunitaryConjugate_smul
#print axioms localBaseCore
#print axioms matrix_linear_polar_commutes
#print axioms localBase_polar_commutes
end
end TGLV350.Regular
