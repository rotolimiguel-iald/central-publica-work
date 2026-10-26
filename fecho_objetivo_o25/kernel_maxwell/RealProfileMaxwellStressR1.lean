import ProfileMaxwellLowerWaveR1
import MaxwellStressEnergyR2

/-! An actual real classical Maxwell wave and its conserved stress from a
regular profile of the SAME H1. The factor sqrt(2) records the Segal coherent
normalization. Pairing this point wave with the operator-valued distribution,
boost tensor covariance and the null-plane charge remain separate consumers. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
namespace F1Fecho.MaxwellGlobal
open MeasureTheory Filter
open TGLExt.ImportedSQ ChatgptAudit.WignerRapidityMeasure016
open F1Fecho.MaxwellStress

def realWaveProjection : ℂ→L[ℝ]ℂ :=
  Real.sqrt 2 • (Complex.ofRealCLM.comp Complex.reCLM)

theorem realWaveProjection_apply (z : ℂ) :
    realWaveProjection z=((Real.sqrt 2*z.re:ℝ):ℂ) := by
  simp [realWaveProjection,Complex.real_smul]

theorem realWaveProjection_sign (μ : Fin 4) (z : ℂ) :
    realWaveProjection (metricSignC μ*z)=metricSignC μ*realWaveProjection z := by
  unfold metricSignC
  split_ifs <;> simp

def realProfileWave (h : H1) (μ ν : Fin 4) (x : Spacetime) : ℂ :=
  realWaveProjection (lowerProfileWave h μ ν x)

def realProfileJet (h : H1) (ρ μ ν : Fin 4) (x : Spacetime) : ℂ :=
  realWaveProjection (lowerProfileJet h ρ μ ν x)

theorem realProfileWave_line_hasDerivAt (h : H1) (hh : RegularProfile h)
    (ρ μ ν : Fin 4) (x : Spacetime) (t : ℝ) :
    HasDerivAt (fun u : ℝ=>realProfileWave h μ ν (x+u • spacetimeBasis ρ))
      (realProfileJet h ρ μ ν (x+t • spacetimeBasis ρ)) t :=
  realWaveProjection.hasFDerivAt.comp_hasDerivAt t
    (lowerProfileWave_line_hasDerivAt h hh ρ μ ν x t)

theorem realProfileWave_antisymmetric (h : H1) (μ ν : Fin 4) (x : Spacetime) :
    realProfileWave h ν μ x= -realProfileWave h μ ν x := by
  simp only [realProfileWave,lowerProfileWave_antisymmetric,map_neg]

theorem realProfileJet_antisymmetric (h : H1) (ρ μ ν : Fin 4) (x : Spacetime) :
    realProfileJet h ρ ν μ x= -realProfileJet h ρ μ ν x := by
  simp only [realProfileJet,lowerProfileJet_antisymmetric,map_neg]

theorem realProfileJet_bianchi (h : H1) (hh : RegularProfile h)
    (ρ μ ν : Fin 4) (x : Spacetime) :
    realProfileJet h ρ μ ν x+realProfileJet h μ ν ρ x+realProfileJet h ν ρ μ x=0 := by
  simp only [realProfileJet,← map_add,lowerProfileJet_bianchi h hh,map_zero]

theorem realProfileJet_divergence (h : H1) (hh : RegularProfile h)
    (ν : Fin 4) (x : Spacetime) :
    (∑ μ : Fin 4,metricSignC μ*realProfileJet h μ μ ν x)=0 := by
  simp only [realProfileJet,← realWaveProjection_sign,← map_sum,
    lowerProfileJet_divergence h hh,map_zero]

def realProfileStress (h : H1) (μ ν : Fin 4) (x : Spacetime) : ℂ :=
  stress metricSignC (fun α β=>realProfileWave h α β x) μ ν

theorem realProfileStress_line_hasDerivAt (h : H1) (hh : RegularProfile h)
    (ρ μ ν : Fin 4) (x : Spacetime) :
    HasDerivAt (fun t : ℝ=>realProfileStress h μ ν (x+t • spacetimeBasis ρ))
      (stressJet metricSignC (fun α β=>realProfileWave h α β x)
        (fun ρ α β=>realProfileJet h ρ α β x) ρ μ ν) 0 := by
  have hd (α β : Fin 4) := realProfileWave_line_hasDerivAt h hh ρ α β x 0
  have hr:=stress_hasDerivAt metricSignC
    (fun t α β=>realProfileWave h α β (x+t • spacetimeBasis ρ))
    (fun α β=>realProfileJet h ρ α β x) 0
    (fun α β=>by simpa only [zero_smul,add_zero] using hd α β) μ ν
  simpa only [realProfileStress,stressJet,zero_smul,add_zero] using hr

theorem realProfileStress_conserved (h : H1) (hh : RegularProfile h)
    (ν : Fin 4) (x : Spacetime) :
    (∑ μ : Fin 4,metricSignC μ*
      deriv (fun t : ℝ=>realProfileStress h μ ν (x+t • spacetimeBasis μ)) 0)=0 := by
  simp only [(realProfileStress_line_hasDerivAt h hh _ _ _ x).deriv]
  exact stressJet_conserved metricSignC metricSignC_square
    (fun α β=>realProfileWave h α β x) (fun ρ α β=>realProfileJet h ρ α β x)
    (fun μ ν=>realProfileWave_antisymmetric h μ ν x)
    (fun ρ μ ν=>realProfileJet_antisymmetric h ρ μ ν x)
    (fun ρ μ ν=>realProfileJet_bianchi h hh ρ μ ν x)
    (fun ν=>realProfileJet_divergence h hh ν x) ν

theorem realProfileStress_real (h : H1) (μ ν : Fin 4) (x : Spacetime) :
    star (realProfileStress h μ ν x)=realProfileStress h μ ν x := by
  simp only [realProfileStress,realProfileWave,realWaveProjection_apply]
  have hs : metricSignC=(fun μ=>((if μ=0 then 1 else -1:ℝ):ℂ)) := by
    funext μ
    by_cases h : μ=0 <;> simp [metricSignC,h]
  rw [hs]
  exact stress_real _ _ μ ν

theorem realProfileStress_symmetric (h : H1) (μ ν : Fin 4) (x : Spacetime) :
    realProfileStress h μ ν x=realProfileStress h ν μ x := stress_symmetric _ _ μ ν

theorem realProfileStress_energy_nonneg (h : H1) (x : Spacetime) :
    0≤(realProfileStress h 0 0 x).re := by
  let R : Fin 4→Fin 4→ℝ := fun μ ν=>Real.sqrt 2*(lowerProfileWave h μ ν x).re
  have ha : ∀μ ν,R ν μ= -R μ ν := by
    intro μ ν
    simp only [R,lowerProfileWave_antisymmetric,Complex.neg_re,mul_neg]
  exact stress_classical_energy_nonneg R ha

end F1Fecho.MaxwellGlobal
#print axioms F1Fecho.MaxwellGlobal.realProfileWave_line_hasDerivAt
#print axioms F1Fecho.MaxwellGlobal.realProfileJet_bianchi
#print axioms F1Fecho.MaxwellGlobal.realProfileJet_divergence
#print axioms F1Fecho.MaxwellGlobal.realProfileStress_line_hasDerivAt
#print axioms F1Fecho.MaxwellGlobal.realProfileStress_conserved
#print axioms F1Fecho.MaxwellGlobal.realProfileStress_real
#print axioms F1Fecho.MaxwellGlobal.realProfileStress_symmetric
#print axioms F1Fecho.MaxwellGlobal.realProfileStress_energy_nonneg
