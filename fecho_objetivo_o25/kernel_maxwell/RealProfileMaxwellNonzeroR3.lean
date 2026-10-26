import RealProfileMaxwellStressR4
import MaxwellStressPositiveEnergyR1
import RegularMaxwellWaveNonzeroR2
import RegularMaxwellEnergyR2

/-! Non-vacuity of the actual real classical Maxwell stress: an existing
smooth momentum bump gives strictly positive energy density. This does not
construct a local quantum stress, a null-plane charge or a physical source. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
namespace F1Fecho.MaxwellGlobal
open MeasureTheory Filter
open TGLExt.ImportedSQ ChatgptAudit.WignerRapidityMeasure016

theorem exists_strongRegular_positive_stress : ∃h : H1,
    StrongRegularProfile h ∧ 0<(realProfileStress h 0 0 0).re := by
  obtain ⟨f,hf⟩:=exists_nonzero_regularWave
  let h : H1:=momentumSmearCLM f
  refine ⟨h,⟨momentumSmear_regular f,momentumSmear_energySquare f⟩,?_⟩
  apply realWaveProjection_energy_pos_of_component
    (fun μ ν=>lowerProfileWave h μ ν 0)
    (fun μ ν=>lowerProfileWave_antisymmetric h μ ν 0)
  have hp : (lowerProfileWave h 0 1 0).re= -(regularWave f 0 1 0).re := by
    unfold lowerProfileWave
    change (metricSignC 0*metricSignC 1*profileWave (momentumSmearCLM f) 0 1 0).re=_
    rw [profileWave_momentumSmear]
    simp [metricSignC]
  rw [hp]
  exact neg_ne_zero.mpr (ne_of_gt hf)

theorem profileWave_zero (μ ν : Fin 4) (x : Spacetime) :
    profileWave (0:H1) μ ν x=0 := by
  unfold profileWave
  calc
    _ = ∫ _ : MomentumCoordinates,(0:ℂ) ∂orbitalMeasure 0 := by
      apply integral_congr_ae
      filter_upwards [Lp.coeFn_zero Fib 2 (orbitalMeasure 0)] with y hy
      have hz : (0:H1) y=(0:Fib) := hy
      have hj (j : Fin 2) : (0:H1) y j=0 := by
        have hh:=congrArg (fun v : Fib=>v j) hz
        simpa only [PiLp.zero_apply] using hh
      simp only [profileDensity,hj,mul_zero,Finset.sum_const_zero]
    _ = 0 := integral_zero _ _

theorem realProfileStress_zero (μ ν : Fin 4) (x : Spacetime) :
    realProfileStress (0:H1) μ ν x=0 := by
  simp only [realProfileStress,realProfileWave,lowerProfileWave,profileWave_zero,
    mul_zero,map_zero]
  exact F1Fecho.MaxwellStress.stress_zero _ μ ν

end F1Fecho.MaxwellGlobal
#print axioms F1Fecho.MaxwellGlobal.exists_strongRegular_positive_stress
#print axioms F1Fecho.MaxwellGlobal.profileWave_zero
#print axioms F1Fecho.MaxwellGlobal.realProfileStress_zero
