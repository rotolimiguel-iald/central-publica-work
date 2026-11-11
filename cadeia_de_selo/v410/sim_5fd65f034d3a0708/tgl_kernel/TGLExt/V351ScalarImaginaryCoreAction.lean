import TGLExt.V351ScalarImaginaryLeftTransport
import TGLExt.V350BasePolarStrongLimit
import TGLExt.V350ScalarGNSGeneratorTransport

set_option autoImplicit false
set_option maxHeartbeats 6000000
set_option synthInstance.maxHeartbeats 200000

namespace TGLV350.Regular
open TGLExt ChatgptAudit Filter
open scoped Topology
noncomputable section

/-- The regular unitaries act on the existing matrix-unit core element with
the phase of the original tower flow. -/
theorem matrixUnit_regular_core_conjugation (P : SiteProfile) (N : ℕ)
    (i j : chainIdx N) (t : ℝ) :
    regularRightCoreElement P t * localBaseCore P N (Matrix.single i j 1) *
        star (regularRightCoreElement P t) =
      modularPhase t (Real.log (localEigenvalue P N i j)) •
        localBaseCore P N (Matrix.single i j 1) := by
  apply Subtype.ext
  change regularUnitary P t * fibre (towerPi P (Matrix.single i j (1 : ℂ))) *
      star (regularUnitary P t) = _
  rw [regular_covariance, modularConjugation_local, flowLevel_single,
    towerPi_smul, fibre_smul]
  rfl

/-- Reversing the matrix-unit indices converts the proved adjoint action to
the ordinary left generator; the conjugated phase changes with those indices. -/
theorem matrixUnit_imaginaryPower_base_scaling (P : SiteProfile) (N : ℕ)
    (i j : chainIdx N) (t : ℝ) (x : ScalarGNSHilbert P) :
    scalarTomitaImaginaryPower P t
        (scalarGNSRepresentation P (localBaseCore P N (Matrix.single i j 1)) x) =
      modularPhase t (Real.log (localEigenvalue P N i j)) •
        scalarGNSRepresentation P (localBaseCore P N (Matrix.single i j 1))
          (scalarTomitaImaginaryPower P t x) := by
  letI : NormedSpace ℂ (ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P) := inferInstance
  have h := matrixUnit_imaginaryPower_left_scaling P N j i t x
  rw [← matrixUnit_rightCore_star, modularPhase_star_frequency,
    localEigenvalue_reverse_log] at h
  exact h

/-- The original Tomita imaginary powers implement Ad(lambda_t) on every
element of the actual regular core, in its existing scalar GNS representation.
No separate normality, density, or covariance premise is introduced. -/
theorem scalarTomitaImaginaryPower_core_conjugation (P : SiteProfile) (t : ℝ)
    (A : (regularCoreAlgebra P).toStarSubalgebra) (x : ScalarGNSHilbert P) :
    scalarTomitaImaginaryPower P t (scalarGNSRepresentation P A x) =
      scalarGNSRepresentation P
        (regularRightCoreElement P t * A * star (regularRightCoreElement P t))
          (scalarTomitaImaginaryPower P t x) := by
  let U : ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P :=
    (scalarTomitaImaginaryPower P t).toLinearIsometry.toContinuousLinearMap
  let V : ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P :=
    scalarGNSRepresentation P (regularRightCoreElement P t)
  let D : ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P := star V * U
  have hunit : star (regularRightCoreElement P t) * regularRightCoreElement P t = 1 :=
    Subtype.ext (regular_unitary P t).1
  have hunit' : regularRightCoreElement P t * star (regularRightCoreElement P t) = 1 :=
    Subtype.ext (regular_unitary P t).2
  have hVV : star V * V = 1 := by
    have h := congrArg (scalarGNSRepresentation P) hunit
    simpa only [map_mul, map_star, map_one] using h
  have hVV' : V * star V = 1 := by
    have h := congrArg (scalarGNSRepresentation P) hunit'
    simpa only [map_mul, map_star, map_one] using h
  have hmatrix (N : ℕ) (i j : chainIdx N) :
      Commute D (scalarGNSRepresentation P (localBaseCore P N (Matrix.single i j 1))) := by
    let B := scalarGNSRepresentation P (localBaseCore P N (Matrix.single i j 1))
    let c := modularPhase t (Real.log (localEigenvalue P N i j))
    have hU : U * B = (c • B) * U := by
      apply ContinuousLinearMap.ext
      intro z
      exact matrixUnit_imaginaryPower_base_scaling P N i j t z
    have hV : V * B * star V = c • B := by
      have h := congrArg (scalarGNSRepresentation P)
        (matrixUnit_regular_core_conjugation P N i j t)
      simpa only [map_mul, map_star, map_smul] using h
    change (star V * U) * B = B * (star V * U)
    calc
      (star V * U) * B = star V * (U * B) := mul_assoc _ _ _
      _ = star V * ((c • B) * U) := by rw [hU]
      _ = star V * ((V * B * star V) * U) := by rw [hV]
      _ = B * (star V * U) := by simp only [← mul_assoc, hVV, one_mul]
  have hlevel (N : ℕ) (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
      Commute D (scalarGNSRepresentation P (localBaseCore P N a)) := by
    induction a using Matrix.induction_on' with
    | h_zero => simp only [map_zero]; exact Commute.zero_right D
    | h_add a b ha hb =>
        simp only [map_add]
        exact ha.add_right hb
    | h_std_basis i j c =>
        have he : Matrix.single i j c = c • Matrix.single i j (1 : ℂ) := by
          simp only [Matrix.smul_single, smul_eq_mul, mul_one]
        rw [he, map_smul, map_smul]
        apply ContinuousLinearMap.ext
        intro z
        have hz := congrArg (fun F : ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P => F z)
          (hmatrix N i j).eq
        change D (c • scalarGNSRepresentation P
            (localBaseCore P N (Matrix.single i j 1)) z) =
          c • scalarGNSRepresentation P (localBaseCore P N (Matrix.single i j 1)) (D z)
        rw [map_smul]
        exact congrArg (fun v : ScalarGNSHilbert P => c • v) hz
  have hbase (B : (theFactorObject P).toStarSubalgebra) :
      Commute D (scalarGNSRepresentation P (regularCoreEmbedding P B)) := by
    apply Commute.symm
    apply commute_of_strong_tendsto (l := (atTop : Filter ℕ))
      (fun N => scalarGNSRepresentation P (levelCoreApproximation P N B))
    · exact represented_levelExpectation_strong_tendsto P B
    · intro N
      exact (hlevel N (expectationMatrix P N B.val)).symm
  have hregular (s : ℝ) :
      Commute D (scalarGNSRepresentation P (regularRightCoreElement P s)) := by
    have hU : Commute U (scalarGNSRepresentation P (regularRightCoreElement P s)) := by
      apply ContinuousLinearMap.ext
      intro z
      change scalarTomitaImaginaryPower P t
          (scalarGNSRepresentation P (regularRightCoreElement P s) z) =
        scalarGNSRepresentation P (regularRightCoreElement P s)
          (scalarTomitaImaginaryPower P t z)
      have hz := scalarTomitaImaginaryPower_regular_left_commutes P (-s) t z
      simpa only [regularRightCoreElement_star, neg_neg] using hz
    have hcore : Commute (star (regularRightCoreElement P t)) (regularRightCoreElement P s) := by
      apply Subtype.ext
      change star (regularUnitary P t) * regularUnitary P s =
        regularUnitary P s * star (regularUnitary P t)
      rw [regular_star, regular_mul, regular_mul, add_comm]
    have hV : Commute (star V) (scalarGNSRepresentation P (regularRightCoreElement P s)) := by
      dsimp only [V]
      rw [← map_star]
      exact hcore.map (scalarGNSRepresentation P)
    exact hV.mul_left hU
  have hwhole : ∀ B : (regularCoreAlgebra P).toStarSubalgebra,
      Commute D (scalarGNSRepresentation P B) := by
    apply scalarGNS_commutation_from_generators
    intro B hB
    change B.val ∈ regularGenerators P at hB
    rcases hB with ⟨C, hC, he⟩ | ⟨s, he⟩
    · have e : B = regularCoreEmbedding P ⟨C, hC⟩ := Subtype.ext he.symm
      rw [e]
      exact hbase ⟨C, hC⟩
    · have e : B = regularRightCoreElement P s := Subtype.ext he.symm
      rw [e]
      exact hregular s
  have hop : U * scalarGNSRepresentation P A =
      (V * scalarGNSRepresentation P A * star V) * U := by
    have hc := (hwhole A).eq
    change (star V * U) * scalarGNSRepresentation P A =
      scalarGNSRepresentation P A * (star V * U) at hc
    calc
      U * scalarGNSRepresentation P A =
          V * ((star V * U) * scalarGNSRepresentation P A) := by
            simp only [← mul_assoc, hVV', one_mul]
      _ = V * (scalarGNSRepresentation P A * (star V * U)) := by rw [hc]
      _ = (V * scalarGNSRepresentation P A * star V) * U := by simp only [mul_assoc]
  have hx := congrArg (fun F : ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P => F x) hop
  change U (scalarGNSRepresentation P A x) =
    scalarGNSRepresentation P
      (regularRightCoreElement P t * A * star (regularRightCoreElement P t)) (U x)
  rw [map_mul, map_mul, map_star]
  exact hx

#print axioms matrixUnit_regular_core_conjugation
#print axioms matrixUnit_imaginaryPower_base_scaling
#print axioms scalarTomitaImaginaryPower_core_conjugation
end
end TGLV350.Regular
