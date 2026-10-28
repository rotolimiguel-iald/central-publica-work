import TGLExt.V350RegularCoreCommutant
import TGLExt.ModularFlowSpectrum

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

namespace TGLV350.Regular
open TGLExt ChatgptAudit Matrix UniformSpace
noncomputable section
variable {P : SiteProfile}

theorem baseCommutant_eq_of_vacuum
    (D E : TowerHilbert P →L[ℂ] TowerHilbert P)
    (hD : D ∈ (theFactorObject P).commutant)
    (hE : E ∈ (theFactorObject P).commutant)
    (h : D (hOmega P) = E (hOmega P)) : D = E := by
  ext1 v
  refine (towerPre_denseRange (P := P)).induction ?_ (isClosed_eq D.continuous E.continuous) v
  rintro _ ⟨a,rfl⟩
  obtain ⟨N,a,rfl⟩ := exists_tof a
  rw [← towerPi_omega]
  have hd := (VonNeumannAlgebra.mem_commutant_iff.mp hD)
    (towerPi P a) (towerPi_mem_factor a)
  have he := (VonNeumannAlgebra.mem_commutant_iff.mp hE)
    (towerPi P a) (towerPi_mem_factor a)
  calc
    D (towerPi P a (hOmega P)) = towerPi P a (D (hOmega P)) :=
      congrArg (fun T : TowerHilbert P →L[ℂ] _ => T (hOmega P)) hd.symm
    _ = towerPi P a (E (hOmega P)) := congrArg (towerPi P a) h
    _ = E (towerPi P a (hOmega P)) :=
      congrArg (fun T : TowerHilbert P →L[ℂ] _ => T (hOmega P)) he

theorem rTowerPi_mem_baseCommutant {N : ℕ}
    (y : Matrix (chainIdx N) (chainIdx N) ℂ) :
    rTowerPi P y ∈ (theFactorObject P).commutant := by
  rw [VonNeumannAlgebra.mem_commutant_iff]
  intro A hA
  exact factor_comm_rTowerPi hA y

theorem rTowerPi_parameter_smul {N : ℕ} (c : ℂ)
    (y : Matrix (chainIdx N) (chainIdx N) ℂ) :
    rTowerPi P (c • y) = c • rTowerPi P y := by
  apply baseCommutant_eq_of_vacuum _ _ (rTowerPi_mem_baseCommutant _)
    ((theFactorObject P).commutant.toStarSubalgebra.smul_mem (rTowerPi_mem_baseCommutant y) c)
  change rTowerPi P (c • y) (hOmega P) = c • rTowerPi P y (hOmega P)
  rw [rTowerPi_omega,rTowerPi_omega,← tof_smul,Completion.coe_smul]

theorem modularConjugation_rTowerPi (t : ℝ) {N : ℕ}
    (y : Matrix (chainIdx N) (chainIdx N) ℂ) :
    modularConjugation P t (rTowerPi P y) = rTowerPi P (flowLevel P t N y) := by
  apply baseCommutant_eq_of_vacuum _ _
    (modularConjugation_preserves_commutant P t _ (rTowerPi_mem_baseCommutant y))
    (rTowerPi_mem_baseCommutant _)
  change modularFlow P t (rTowerPi P y (modularFlow P (-t) (hOmega P))) = _
  rw [modularFlow_fixes_omega,rTowerPi_omega,modularFlow_coe,flowPre_tof,rTowerPi_omega]

theorem rTowerPi_matrixUnit_homogeneous (t : ℝ) (N : ℕ) (i j : chainIdx N) :
    modularConjugation P t (rTowerPi P (Matrix.single i j 1)) =
      modularPhase t (Real.log (localEigenvalue P N i j)) • rTowerPi P (Matrix.single i j 1) := by
  rw [modularConjugation_rTowerPi,flowLevel_single,rTowerPi_parameter_smul]

#print axioms baseCommutant_eq_of_vacuum
#print axioms rTowerPi_mem_baseCommutant
#print axioms rTowerPi_parameter_smul
#print axioms modularConjugation_rTowerPi
#print axioms rTowerPi_matrixUnit_homogeneous
end
end TGLV350.Regular
