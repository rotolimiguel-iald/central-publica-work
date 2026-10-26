import RegularFockPointStressR3

/-! Continuity of the actual point form and of its coordinate derivatives.
Polynomial L1 energy moments provide the common derivative majorant. This
prepares weak conservation; it does not assume distributional conservation. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
namespace F1Fecho.MaxwellGlobal
open MeasureTheory Filter TGLExt.ImportedSQ
open ChatgptAudit.WignerRapidityMeasure016 F1Fecho.CoherentKernel F1Fecho.MaxwellStress

 theorem lowerProfileWave_continuous (h : H1) (hh : RegularProfile h) (μ ν : Fin 4) :
    Continuous (lowerProfileWave h μ ν) :=
  continuous_const.mul (profileWave_continuous h hh μ ν)

 theorem lowerProfileJet_continuous (h : H1) (hh : RegularProfile h) (ρ μ ν : Fin 4) :
    Continuous (lowerProfileJet h ρ μ ν) := by
  apply continuous_const.mul
  apply continuous_of_dominated (bound:=fun y=>shellEnergy y*‖profileDensity h μ ν y‖)
  · exact fun x=>(profileDerivativeIntegrand_integrable h hh μ ν ρ x).aestronglyMeasurable
  · exact fun x=>ae_of_all _ (profileDerivativeIntegrand_bound h μ ν ρ x)
  · simpa only [pow_one] using profileDensity_moment_integrable h hh μ ν 1
  · apply ae_of_all
    intro y
    unfold profileDerivativeIntegrand
    exact continuous_const.mul ((wavePhase_continuous_left y).mul continuous_const)

 theorem coherentProfileWave_continuous (h k : H1) (hh : RegularProfile h)
    (hk : RegularProfile k) (μ ν : Fin 4) :
    Continuous (coherentProfileWave h k μ ν) :=
  continuous_const.mul ((Complex.continuous_conj.comp (lowerProfileWave_continuous h hh μ ν)).add
    (lowerProfileWave_continuous k hk μ ν))

 theorem coherentProfileJet_continuous (h k : H1) (hh : RegularProfile h)
    (hk : RegularProfile k) (ρ μ ν : Fin 4) :
    Continuous (coherentProfileJet h k ρ μ ν) :=
  continuous_const.mul ((Complex.continuous_conj.comp (lowerProfileJet_continuous h hh ρ μ ν)).add
    (lowerProfileJet_continuous k hk ρ μ ν))

 theorem coherentProfileStress_continuous (h k : H1) (hh : RegularProfile h)
    (hk : RegularProfile k) (μ ν : Fin 4) :
    Continuous (coherentProfileStress h k μ ν) := by
  have hw:=coherentProfileWave_continuous h k hh hk
  unfold coherentProfileStress stress
  fun_prop

 theorem coherentProfileStress_partial_continuous (h k : H1) (hh : RegularProfile h)
    (hk : RegularProfile k) (ρ μ ν : Fin 4) :
    Continuous (fun x=>deriv (fun t : ℝ=>coherentProfileStress h k μ ν
      (x+t • spacetimeBasis ρ)) 0) := by
  simp only [(coherentProfileStress_line_hasDerivAt h k hh hk ρ μ ν _).deriv]
  have hw:=coherentProfileWave_continuous h k hh hk
  have hj:=coherentProfileJet_continuous h k hh hk
  unfold stressJet
  fun_prop

 theorem finiteKernel_continuous {ι X : Type*} [TopologicalSpace X]
    (M : ι→ι→X→ℂ) (hM : ∀i j,Continuous (M i j)) (c d : ι→₀ℂ) :
    Continuous (fun x=>finiteKernel (fun i j=>M i j x) c d) := by
  unfold finiteKernel Finsupp.sum
  fun_prop

 theorem pointStressForm_continuous (ψ χ : regularFockDomain) (μ ν : Fin 4) :
    Continuous (pointStressForm ψ χ μ ν) :=
  finiteKernel_continuous _ (fun h k=>coherentProfileStress_continuous h.val k.val
    h.property.1 k.property.1 μ ν) _ _

 theorem pointStressForm_partial_continuous (ψ χ : regularFockDomain) (ρ μ ν : Fin 4) :
    Continuous (fun x=>deriv (fun t : ℝ=>pointStressForm ψ χ μ ν
      (x+t • spacetimeBasis ρ)) 0) := by
  simp only [(pointStressForm_line_hasDerivAt ψ χ ρ μ ν _).deriv]
  exact finiteKernel_continuous _ (fun h k=>coherentProfileStress_partial_continuous h.val k.val
    h.property.1 k.property.1 ρ μ ν) _ _

end F1Fecho.MaxwellGlobal
#print axioms F1Fecho.MaxwellGlobal.lowerProfileJet_continuous
#print axioms F1Fecho.MaxwellGlobal.coherentProfileStress_continuous
#print axioms F1Fecho.MaxwellGlobal.coherentProfileStress_partial_continuous
#print axioms F1Fecho.MaxwellGlobal.pointStressForm_continuous
#print axioms F1Fecho.MaxwellGlobal.pointStressForm_partial_continuous
