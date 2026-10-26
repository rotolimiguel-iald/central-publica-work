import MaxwellScreenEnergyKernelR3
import MaxwellStressJetAlgebraR3
import CartesianMaxwellBianchiR3

/-! The exact null contraction of Maxwell stress and its transverse screen
amplitudes. Algebra only; the null-plane integral is a separate consumer. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
namespace F1Fecho.MaxwellGlobal
open Matrix F1Fecho.MaxwellStress ChatgptAudit.WignerRapidityMeasure016

def shellNullFrequency (y : MomentumCoordinates) : ℝ := shellEnergy y-y.2
def nullPolarization (y : MomentumCoordinates) : Matrix (Fin 2) (Fin 2) ℝ :=
  !![-transverseRatio y 0,transverseRatio y 1;
    -transverseRatio y 1,-transverseRatio y 0]

theorem shellNullFrequency_pos (y : MomentumCoordinates) (hy : y.1≠0) :
    0<shellNullFrequency y := by
  have hr:=transverseMass_pos_of_ne_zero 0 y.1 hy
  have hs:=shellEnergy_sq y
  have hn:=shellEnergy_nonneg y
  unfold shellNullFrequency
  nlinarith [sq_nonneg y.2, transverseMass_sq 0 y.1, sq_pos_of_pos hr]

theorem nullPolarization_orthogonal (y : MomentumCoordinates) (hy : y.1≠0) :
    (nullPolarization y).transpose*nullPolarization y=1 := by
  have h:=transverseRatio_sq_sum y hy
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [nullPolarization,Matrix.mul_apply,Fin.sum_univ_two,Matrix.transpose_apply,
      Matrix.one_apply] <;> nlinarith

theorem null_strength_factor (y : MomentumCoordinates) (a j : Fin 2) :
    -(cartesianStrength y j 0 (show Fin 4 from ⟨a.val+2,by omega⟩))+
      cartesianStrength y j 1 (show Fin 4 from ⟨a.val+2,by omega⟩)=
      shellNullFrequency y*nullPolarization y a j := by
  fin_cases a <;> fin_cases j <;>
    simp [cartesianStrength,shellNullFrequency,nullPolarization] <;> ring

theorem stress_null_contraction (F : Fin 4→Fin 4→ℂ)
    (ha : ∀μ ν,F ν μ= -F μ ν) :
    stress metricSignC F 0 0+stress metricSignC F 0 1+
      stress metricSignC F 1 0+stress metricSignC F 1 1=
      (F 0 2+F 1 2)^2+(F 0 3+F 1 3)^2 := by
  have h00 : F 0 0=0 := by have h:=ha 0 0; linear_combination (1/2:ℂ)*h
  have h11 : F 1 1=0 := by have h:=ha 1 1; linear_combination (1/2:ℂ)*h
  have hs0 : metricSignC (0:Fin 4)=(1:ℂ) := rfl
  have hs1 : metricSignC (1:Fin 4)=(-1:ℂ) := rfl
  have hs2 : metricSignC (2:Fin 4)=(-1:ℂ) := rfl
  have hs3 : metricSignC (3:Fin 4)=(-1:ℂ) := rfl
  simp only [stress,Fin.sum_univ_four,hs0,hs1,hs2,hs3,h00,h11,ha 0 1]
  norm_num
  ring

end F1Fecho.MaxwellGlobal
#print axioms F1Fecho.MaxwellGlobal.shellNullFrequency_pos
#print axioms F1Fecho.MaxwellGlobal.nullPolarization_orthogonal
#print axioms F1Fecho.MaxwellGlobal.null_strength_factor
#print axioms F1Fecho.MaxwellGlobal.stress_null_contraction
