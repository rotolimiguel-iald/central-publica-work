import RegularMaxwellWaveEquationR1

/-! The algebraic Bianchi and antisymmetry identities for the existing
Cartesian representative of p wedge screen, with explicit index lowering. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
namespace F1Fecho.MaxwellGlobal
open MeasureTheory Filter
open TGLExt.ImportedSQ ChatgptAudit.WignerRapidityMeasure016
open F1Fecho.MaxwellOnShell

def metricSignC (μ : Fin 4) : ℂ := if μ=0 then 1 else -1

theorem metricSignC_square (μ : Fin 4) : metricSignC μ*metricSignC μ=1 := by
  unfold metricSignC
  split_ifs <;> ring

theorem lowerShellMomentum_eq (y : MomentumCoordinates) (μ : Fin 4) :
    (lowerShellMomentum y μ:ℂ)=metricSignC μ*(shellMomentum 0 y μ:ℂ) := by
  simp [lowerShellMomentum,metricFlip_apply,shellEmbedding,metricSignC,apply_ite,Complex.ofReal_neg]

theorem cartesian_antisymmetric_regular (y : MomentumCoordinates) (hy : y.1≠0)
    (j : Fin 2) (μ ν : Fin 4) :
    cartesianStrength y j ν μ= -cartesianStrength y j μ ν := by
  rw [cartesianStrength_inverse_chart y hy j ν μ,cartesianStrength_inverse_chart y hy j μ ν]
  unfold realStrength
  ring

theorem cartesian_bianchi_regular (y : MomentumCoordinates) (hy : y.1≠0)
    (j : Fin 2) (μ ν ρ : Fin 4) :
    shellMomentum 0 y μ*cartesianStrength y j ν ρ+
    shellMomentum 0 y ν*cartesianStrength y j ρ μ+
    shellMomentum 0 y ρ*cartesianStrength y j μ ν=0 := by
  simp only [cartesianStrength_inverse_chart y hy j,realStrength]
  ring

theorem cartesian_lower_bianchi_regular (y : MomentumCoordinates) (hy : y.1≠0)
    (j : Fin 2) (μ ν ρ : Fin 4) :
    (lowerShellMomentum y μ:ℂ)*(metricSignC ν*metricSignC ρ*(cartesianStrength y j ν ρ:ℂ))+
    (lowerShellMomentum y ν:ℂ)*(metricSignC ρ*metricSignC μ*(cartesianStrength y j ρ μ:ℂ))+
    (lowerShellMomentum y ρ:ℂ)*(metricSignC μ*metricSignC ν*(cartesianStrength y j μ ν:ℂ))=0 := by
  rw [lowerShellMomentum_eq,lowerShellMomentum_eq,lowerShellMomentum_eq]
  have hb : (shellMomentum 0 y μ:ℂ)*(cartesianStrength y j ν ρ:ℂ)+
      (shellMomentum 0 y ν:ℂ)*(cartesianStrength y j ρ μ:ℂ)+
      (shellMomentum 0 y ρ:ℂ)*(cartesianStrength y j μ ν:ℂ)=0 := by
    exact_mod_cast cartesian_bianchi_regular y hy j μ ν ρ
  linear_combination metricSignC μ*metricSignC ν*metricSignC ρ*hb

end F1Fecho.MaxwellGlobal
#print axioms F1Fecho.MaxwellGlobal.metricSignC_square
#print axioms F1Fecho.MaxwellGlobal.lowerShellMomentum_eq
#print axioms F1Fecho.MaxwellGlobal.cartesian_antisymmetric_regular
#print axioms F1Fecho.MaxwellGlobal.cartesian_bianchi_regular
#print axioms F1Fecho.MaxwellGlobal.cartesian_lower_bianchi_regular
