import ProfileMaxwellSymbolR3
import ProfileMaxwellWaveCalculusR2

/-! The complete first Maxwell jet with lowered spacetime indices on the
actual regular H1 domain. Every equation below is consumed from the on-shell
wave integral; no Maxwell equation is a field of an assumed record. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
namespace F1Fecho.MaxwellGlobal
open MeasureTheory Filter
open TGLExt.ImportedSQ ChatgptAudit.WignerRapidityMeasure016

def lowerProfileWave (h : H1) (μ ν : Fin 4) (x : Spacetime) : ℂ :=
  metricSignC μ*metricSignC ν*profileWave h μ ν x

def lowerProfileJet (h : H1) (ρ μ ν : Fin 4) (x : Spacetime) : ℂ :=
  metricSignC μ*metricSignC ν*(∫ y,profileDerivativeIntegrand h μ ν ρ x y ∂orbitalMeasure 0)

def lowerProfileJetIntegrand (h : H1) (ρ μ ν : Fin 4) (x : Spacetime)
    (y : MomentumCoordinates) : ℂ :=
  (-Complex.I*(lowerShellMomentum y ρ:ℂ))*(wavePhase x y*lowerProfileDensity h μ ν y)

theorem lowerProfileWave_integral (h : H1) (μ ν : Fin 4) (x : Spacetime) :
    lowerProfileWave h μ ν x=∫ y,wavePhase x y*lowerProfileDensity h μ ν y ∂orbitalMeasure 0 := by
  unfold lowerProfileWave profileWave
  rw [← integral_const_mul]
  apply integral_congr_ae
  exact Filter.Eventually.of_forall (fun y=>by unfold lowerProfileDensity;ring)

theorem lowerProfileJetIntegrand_eq (h : H1) (ρ μ ν : Fin 4) (x : Spacetime) :
    lowerProfileJetIntegrand h ρ μ ν x=
      fun y=>(metricSignC μ*metricSignC ν)*profileDerivativeIntegrand h μ ν ρ x y := by
  funext y
  unfold lowerProfileJetIntegrand lowerProfileDensity profileDerivativeIntegrand
  ring

theorem lowerProfileJet_integral (h : H1) (ρ μ ν : Fin 4) (x : Spacetime) :
    lowerProfileJet h ρ μ ν x=∫ y,lowerProfileJetIntegrand h ρ μ ν x y ∂orbitalMeasure 0 := by
  rw [lowerProfileJetIntegrand_eq,integral_const_mul]
  rfl

theorem lowerProfileJetIntegrand_integrable (h : H1) (hh : RegularProfile h)
    (ρ μ ν : Fin 4) (x : Spacetime) :
    Integrable (lowerProfileJetIntegrand h ρ μ ν x) (orbitalMeasure 0) := by
  rw [lowerProfileJetIntegrand_eq]
  exact (profileDerivativeIntegrand_integrable h hh μ ν ρ x).const_mul _

theorem lowerProfileWave_line_hasDerivAt (h : H1) (hh : RegularProfile h)
    (ρ μ ν : Fin 4) (x : Spacetime) (t : ℝ) :
    HasDerivAt (fun u : ℝ=>lowerProfileWave h μ ν (x+u • spacetimeBasis ρ))
      (lowerProfileJet h ρ μ ν (x+t • spacetimeBasis ρ)) t :=
  (profileWave_line_hasDerivAt h hh μ ν ρ x t).const_mul (metricSignC μ*metricSignC ν)

theorem lowerProfileWave_antisymmetric (h : H1) (μ ν : Fin 4) (x : Spacetime) :
    lowerProfileWave h ν μ x= -lowerProfileWave h μ ν x := by
  rw [lowerProfileWave_integral,lowerProfileWave_integral,← integral_neg]
  apply integral_congr_ae
  filter_upwards [cartesian_regular_ae] with y hy
  rw [lowerProfileDensity_antisymmetric_regular h μ ν y hy]
  ring

theorem lowerProfileJet_antisymmetric (h : H1) (ρ μ ν : Fin 4) (x : Spacetime) :
    lowerProfileJet h ρ ν μ x= -lowerProfileJet h ρ μ ν x := by
  rw [lowerProfileJet_integral,lowerProfileJet_integral,← integral_neg]
  apply integral_congr_ae
  filter_upwards [cartesian_regular_ae] with y hy
  unfold lowerProfileJetIntegrand
  rw [lowerProfileDensity_antisymmetric_regular h μ ν y hy]
  ring

theorem lowerProfileJet_bianchi (h : H1) (hh : RegularProfile h)
    (ρ μ ν : Fin 4) (x : Spacetime) :
    lowerProfileJet h ρ μ ν x+lowerProfileJet h μ ν ρ x+lowerProfileJet h ν ρ μ x=0 := by
  rw [lowerProfileJet_integral,lowerProfileJet_integral,lowerProfileJet_integral,
    ← integral_add (lowerProfileJetIntegrand_integrable h hh ρ μ ν x)
      (lowerProfileJetIntegrand_integrable h hh μ ν ρ x),
    ← integral_add (show Integrable (fun y=>lowerProfileJetIntegrand h ρ μ ν x y+
      lowerProfileJetIntegrand h μ ν ρ x y) (orbitalMeasure 0) from
      (lowerProfileJetIntegrand_integrable h hh ρ μ ν x).add
        (lowerProfileJetIntegrand_integrable h hh μ ν ρ x))
      (lowerProfileJetIntegrand_integrable h hh ν ρ μ x)]
  calc
    _ = ∫ _ : MomentumCoordinates,(0:ℂ) ∂orbitalMeasure 0 := by
      apply integral_congr_ae
      filter_upwards [cartesian_regular_ae] with y hy
      have hb:=lowerProfileDensity_bianchi_regular h ρ μ ν y hy
      simp only [lowerProfileJetIntegrand]
      linear_combination (-Complex.I*wavePhase x y)*hb
    _ = 0 := integral_zero _ _

theorem lowerProfileJet_divergence (h : H1) (hh : RegularProfile h)
    (ν : Fin 4) (x : Spacetime) :
    (∑ μ : Fin 4,metricSignC μ*lowerProfileJet h μ μ ν x)=0 := by
  simp_rw [lowerProfileJet_integral,← integral_const_mul]
  rw [← integral_finsetSum Finset.univ (fun μ _=>
    (lowerProfileJetIntegrand_integrable h hh μ μ ν x).const_mul (metricSignC μ))]
  calc
    _ = ∫ _ : MomentumCoordinates,(0:ℂ) ∂orbitalMeasure 0 := by
      apply integral_congr_ae
      filter_upwards [cartesian_regular_ae] with y hy
      calc
        _ = (-Complex.I*wavePhase x y)*
            (∑ μ : Fin 4,metricSignC μ*(lowerShellMomentum y μ:ℂ)*lowerProfileDensity h μ ν y) := by
          rw [Finset.mul_sum]
          apply Finset.sum_congr rfl
          intro μ _
          unfold lowerProfileJetIntegrand
          ring
        _ = 0 := by rw [lowerProfileDensity_divergence_regular h ν y hy,mul_zero]
    _ = 0 := integral_zero _ _

end F1Fecho.MaxwellGlobal
#print axioms F1Fecho.MaxwellGlobal.lowerProfileWave_line_hasDerivAt
#print axioms F1Fecho.MaxwellGlobal.lowerProfileWave_antisymmetric
#print axioms F1Fecho.MaxwellGlobal.lowerProfileJet_antisymmetric
#print axioms F1Fecho.MaxwellGlobal.lowerProfileJet_bianchi
#print axioms F1Fecho.MaxwellGlobal.lowerProfileJet_divergence
