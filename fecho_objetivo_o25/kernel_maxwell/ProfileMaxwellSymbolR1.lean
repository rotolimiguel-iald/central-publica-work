import ProfileMaxwellWaveR5
import CartesianMaxwellBianchiR2

/-! Explicitly lowered on-shell symbol on the genuine H1 profile domain.
Both Maxwell equations and antisymmetry are inherited from p wedge screen. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
namespace F1Fecho.MaxwellGlobal
open MeasureTheory Filter
open TGLExt.ImportedSQ ChatgptAudit.WignerRapidityMeasure016

def lowerProfileDensity (h : H1) (μ ν : Fin 4) (y : MomentumCoordinates) : ℂ :=
  metricSignC μ*metricSignC ν*profileDensity h μ ν y

theorem profileDensity_antisymmetric_regular (h : H1) (μ ν : Fin 4)
    (y : MomentumCoordinates) (hy : y.1≠0) :
    profileDensity h ν μ y= -profileDensity h μ ν y := by
  simp only [profileDensity,← Finset.sum_neg_distrib]
  apply Finset.sum_congr rfl
  intro j _
  rw [cartesian_antisymmetric_regular y hy j μ ν]
  push_cast
  ring

theorem lowerProfileDensity_antisymmetric_regular (h : H1) (μ ν : Fin 4)
    (y : MomentumCoordinates) (hy : y.1≠0) :
    lowerProfileDensity h ν μ y= -lowerProfileDensity h μ ν y := by
  unfold lowerProfileDensity
  rw [profileDensity_antisymmetric_regular h μ ν y hy]
  ring

theorem lowerProfileDensity_bianchi_regular (h : H1) (μ ν ρ : Fin 4)
    (y : MomentumCoordinates) (hy : y.1≠0) :
    (lowerShellMomentum y μ:ℂ)*lowerProfileDensity h ν ρ y+
    (lowerShellMomentum y ν:ℂ)*lowerProfileDensity h ρ μ y+
    (lowerShellMomentum y ρ:ℂ)*lowerProfileDensity h μ ν y=0 := by
  calc
    _ = ∑ j : Fin 2,h y j*(
        (lowerShellMomentum y μ:ℂ)*(metricSignC ν*metricSignC ρ*(cartesianStrength y j ν ρ:ℂ))+
        (lowerShellMomentum y ν:ℂ)*(metricSignC ρ*metricSignC μ*(cartesianStrength y j ρ μ:ℂ))+
        (lowerShellMomentum y ρ:ℂ)*(metricSignC μ*metricSignC ν*(cartesianStrength y j μ ν:ℂ))) := by
      simp only [lowerProfileDensity,profileDensity,Finset.mul_sum,mul_add,Finset.sum_add_distrib]
      congr 1 <;> congr 1 <;> apply Finset.sum_congr rfl <;> intro j _ <;> ring
    _ = 0 := by simp only [cartesian_lower_bianchi_regular y hy,mul_zero,Finset.sum_const_zero]

theorem lowerProfileDensity_divergence_regular (h : H1) (ν : Fin 4)
    (y : MomentumCoordinates) (hy : y.1≠0) :
    (∑ μ : Fin 4,metricSignC μ*(lowerShellMomentum y μ:ℂ)*lowerProfileDensity h μ ν y)=0 := by
  calc
    _ = metricSignC ν*(∑ μ : Fin 4,(lowerShellMomentum y μ:ℂ)*profileDensity h μ ν y) := by
      rw [Finset.mul_sum]
      apply Finset.sum_congr rfl
      intro μ _
      unfold lowerProfileDensity
      calc
        _ = (metricSignC μ*metricSignC μ)*
            (metricSignC ν*((lowerShellMomentum y μ:ℂ)*profileDensity h μ ν y)) := by ring
        _ = _ := by rw [metricSignC_square,one_mul]
    _ = 0 := by
      have hd : (∑ μ : Fin 4,(lowerShellMomentum y μ:ℂ)*profileDensity h μ ν y)=0 := by
        calc
          _ = ∑ j : Fin 2,h y j*(∑ μ : Fin 4,
                (lowerShellMomentum y μ:ℂ)*(cartesianStrength y j μ ν:ℂ)) := by
            simp only [profileDensity,Finset.mul_sum]
            rw [Finset.sum_comm]
            apply Finset.sum_congr rfl
            intro j _
            apply Finset.sum_congr rfl
            intro μ _
            ring
          _ = 0 := by simp only [lowerShellMomentum,cartesian_divergence_regular y hy,
              mul_zero,Finset.sum_const_zero]
      rw [hd,mul_zero]

end F1Fecho.MaxwellGlobal
#print axioms F1Fecho.MaxwellGlobal.profileDensity_antisymmetric_regular
#print axioms F1Fecho.MaxwellGlobal.lowerProfileDensity_antisymmetric_regular
#print axioms F1Fecho.MaxwellGlobal.lowerProfileDensity_bianchi_regular
#print axioms F1Fecho.MaxwellGlobal.lowerProfileDensity_divergence_regular
