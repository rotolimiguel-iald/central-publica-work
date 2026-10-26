import ProfileWaveFourierPairingR2
import MaxwellCoefficientPairingR2

/-! Exact inner-product pairing of the actual physical Maxwell smearing with
its regular point-wave integral. The 1/2 tensor contraction and angular Fourier
normalization are retained. This is an equality on the SAME H1. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
namespace F1Fecho.MaxwellGlobal
open MeasureTheory Filter TGLExt.ImportedSQ SchwartzMap
open ChatgptAudit.WignerRapidityMeasure016

 theorem profileFourier_pairing_integrable (f : 𝓢(Spacetime,ℂ)) (h : H1)
    (hh : RegularProfile h) (μ ν : Fin 4) :
    Integrable (fun y=>(starRingEnd ℂ) (scalarPhysicalFourier f (shellEmbedding y))*
      profileDensity h μ ν y) (orbitalMeasure 0) := by
  have hi:=(profileWave_pairing_integrable f h hh μ ν).integral_prod_right
  apply hi.congr
  apply ae_of_all
  intro y
  change (∫x,(starRingEnd ℂ) (f x)*wavePhase x y*profileDensity h μ ν y)=_
  rw [integral_mul_const,← scalarPhysicalFourier_conj_integral]

 theorem physicalSmear_inner_wave (f : SchwartzTensor) (h : H1) (hh : RegularProfile h) :
    inner ℂ (physicalSmearCLM f) h=
      (1/2:ℂ)*∑μ : Fin 4,∑ν : Fin 4,
        ∫x,(starRingEnd ℂ) (f x μ ν)*profileWave h μ ν x := by
  have hi (μ ν : Fin 4) := profileFourier_pairing_integrable (componentTest f μ ν) h hh μ ν
  rw [L2.inner_def]
  calc
    _ = ∫y,(1/2:ℂ)*∑μ : Fin 4,∑ν : Fin 4,
        (starRingEnd ℂ) (scalarPhysicalFourier (componentTest f μ ν) (shellEmbedding y))*
          profileDensity h μ ν y ∂orbitalMeasure 0 := by
      apply integral_congr_ae
      filter_upwards [physicalSmear_ae f] with y hy
      rw [hy,globalCoefficient_inner_profile]
      simp only [physicalFourier_component]
    _ = (1/2:ℂ)*∑μ : Fin 4,∑ν : Fin 4,
        ∫y,(starRingEnd ℂ) (scalarPhysicalFourier (componentTest f μ ν) (shellEmbedding y))*
          profileDensity h μ ν y ∂orbitalMeasure 0 := by
      rw [integral_const_mul,integral_finsetSum Finset.univ
        (fun μ _=>integrable_finset_sum _ (fun ν _=>hi μ ν))]
      congr 1
      apply Finset.sum_congr rfl
      intro μ _
      rw [integral_finsetSum Finset.univ (fun ν _=>hi μ ν)]
    _ = _ := by
      simp_rw [← profileWave_fourier_pairing (componentTest f _ _) h hh,
        componentTest_apply]

end F1Fecho.MaxwellGlobal
#print axioms F1Fecho.MaxwellGlobal.profileFourier_pairing_integrable
#print axioms F1Fecho.MaxwellGlobal.physicalSmear_inner_wave
