import RegularPointAnnihilationR1
import CalibratedFockStressDomainBridgeR1
import RegularFockStressContinuityR4

/-! Candidate R51. Local Wick FORM from point annihilators on the existing
regular coherent domain. The bilocal kernel is continuous in its two spacetime
arguments, so its restriction to the diagonal is literal evaluation of this
regular-domain form. It is not multiplication of bounded point fields on H1.
The Maxwell contraction is proved equal to the existing calibrated tensor. -/
set_option Elab.async false
set_option autoImplicit false
set_option maxHeartbeats 400000
set_option synthInstance.maxHeartbeats 500000
noncomputable section
namespace F1Fecho.MaxwellGlobal
open TGLExt TGLExt.ImportedSQ TGLExt.MaxwellBridge
open F1Fecho.NetworkReuse F1Fecho.NetworkModularCore
open F1Fecho.CoherentKernel F1Fecho.MaxwellStress

def normalizedPointEigenvalue (μ ν : Fin 4) (x : Spacetime) (h : RegularLabel) : ℂ :=
  (unitaryFourierFieldAmplitude : ℂ) * lowerProfileWave h.val μ ν x

def pointAnnihilation (μ ν : Fin 4) (x : Spacetime) :
    regularFockDomain →ₗ[ℂ] regularFockDomain :=
  regularDiagonal (normalizedPointEigenvalue μ ν x)

def pointWick (μ ν ρ σ : Fin 4) (x y : Spacetime)
    (ψ χ : regularFockDomain) : ℂ :=
  regularWick (normalizedPointEigenvalue μ ν x) (normalizedPointEigenvalue ρ σ y) ψ χ

theorem pointWick_exponential (μ ν ρ σ : Fin 4) (x y : Spacetime) (h k : RegularLabel) :
    pointWick μ ν ρ σ x y (regularExponential h) (regularExponential k) =
      (unitaryFourierStressScale : ℂ) * Complex.exp (inner ℂ h.val k.val) *
        coherentProfileWave h.val k.val μ ν x * coherentProfileWave h.val k.val ρ σ y := by
  have ha : (unitaryFourierFieldAmplitude : ℂ)^2 = (unitaryFourierStressScale : ℂ) := by
    exact_mod_cast unitaryFourierFieldAmplitude_sq
  have hs : (Real.sqrt 2 : ℂ)^2 = 2 := by
    exact_mod_cast Real.sq_sqrt (by norm_num : (0 : ℝ) ≤ 2)
  have hi : ((Real.sqrt 2 : ℂ)⁻¹)^2 = (1/2 : ℂ) := by
    rw [inv_pow, hs]
    norm_num
  unfold pointWick
  rw [regularWick_exponential]
  simp only [normalizedPointEigenvalue, map_mul, Complex.conj_ofReal]
  calc
    _ = (unitaryFourierFieldAmplitude : ℂ)^2 * (1/2 : ℂ) *
        ((starRingEnd ℂ) (lowerProfileWave h.val μ ν x) + lowerProfileWave k.val μ ν x) *
        ((starRingEnd ℂ) (lowerProfileWave h.val ρ σ y) + lowerProfileWave k.val ρ σ y) *
        Complex.exp (inner ℂ h.val k.val) := by ring
    _ = _ := by rw [ha, ← hi]; unfold coherentProfileWave; ring

theorem pointWick_finiteKernel (μ ν ρ σ : Fin 4) (x y : Spacetime)
    (ψ χ : regularFockDomain) :
    pointWick μ ν ρ σ x y ψ χ =
      finiteKernel (fun h k : RegularLabel =>
        (unitaryFourierStressScale : ℂ) * Complex.exp (inner ℂ h.val k.val) *
          coherentProfileWave h.val k.val μ ν x * coherentProfileWave h.val k.val ρ σ y)
        (regularCoefficients ψ) (regularCoefficients χ) := by
  rw [pointWick, regularWick_finiteKernel]
  simp only [← pointWick, pointWick_exponential]

theorem pointWick_continuous (μ ν ρ σ : Fin 4) (ψ χ : regularFockDomain) :
    Continuous (fun p : Spacetime × Spacetime => pointWick μ ν ρ σ p.1 p.2 ψ χ) := by
  simp only [pointWick_finiteKernel, finiteKernel, Finsupp.sum]
  apply continuous_finset_sum
  intro h _
  apply continuous_finset_sum
  intro k _
  exact continuous_const.mul
    ((continuous_const.mul
      ((coherentProfileWave_continuous h.val k.val h.property.1 k.property.1 μ ν).comp
        continuous_fst)).mul
      ((coherentProfileWave_continuous h.val k.val h.property.1 k.property.1 ρ σ).comp
        continuous_snd))

def contractWick (B : Fin 4 → Fin 4 → Fin 4 → Fin 4 → ℂ) (μ ν : Fin 4) : ℂ :=
  -(∑ α, metricSignC α * B μ α ν α) +
    (1/4 : ℂ) * (if μ = ν then metricSignC μ else 0) *
      (∑ α, ∑ β, metricSignC α * metricSignC β * B α β α β)

theorem contractWick_product (z : ℂ) (G : Fin 4 → Fin 4 → ℂ) (μ ν : Fin 4) :
    contractWick (fun α β γ δ => z * G α β * G γ δ) μ ν =
      z * stress metricSignC G μ ν := by
  have hfirst : (∑ α : Fin 4, metricSignC α * (z * G μ α * G ν α)) =
      z * ∑ α : Fin 4, metricSignC α * G μ α * G ν α := by
    rw [Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro α _
    ring
  have hsecond : (∑ α : Fin 4, ∑ β : Fin 4,
      metricSignC α * metricSignC β * (z * G α β * G α β)) =
      z * ∑ α : Fin 4, ∑ β : Fin 4, metricSignC α * metricSignC β * G α β * G α β := by
    rw [Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro α _
    rw [Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro β _
    ring
  unfold contractWick stress
  rw [hfirst, hsecond]
  ring

theorem finiteKernel_neg_kernel (M : RegularLabel → RegularLabel → ℂ)
    (c d : RegularLabel →₀ ℂ) :
    finiteKernel (fun h k => -M h k) c d = -finiteKernel M c d := by
  simpa only [neg_one_mul] using finiteKernel_mul_kernel (-1) M c d

theorem finiteKernel_sum_kernel {ι : Type*} [Fintype ι]
    (M : ι → RegularLabel → RegularLabel → ℂ) (c d : RegularLabel →₀ ℂ) :
    finiteKernel (fun h k => ∑ i, M i h k) c d = ∑ i, finiteKernel (M i) c d := by
  simpa only [one_mul] using (finiteKernel_weighted_sum M (fun _ => 1) c d).symm

theorem contractWick_finiteKernel
    (M : RegularLabel → RegularLabel → Fin 4 → Fin 4 → Fin 4 → Fin 4 → ℂ)
    (c d : RegularLabel →₀ ℂ) (μ ν : Fin 4) :
    contractWick (fun α β γ δ => finiteKernel (fun h k => M h k α β γ δ) c d) μ ν =
      finiteKernel (fun h k => contractWick (M h k) μ ν) c d := by
  simp only [contractWick, finiteKernel_add_kernel, finiteKernel_neg_kernel,
    finiteKernel_mul_kernel, finiteKernel_sum_kernel]

/-- Coincident restriction and Maxwell contraction of the four-term form.
This definition does not mention pointStressForm or calibratedStress. -/
def localWickStress (ψ χ : regularFockDomain) (μ ν : Fin 4) (x : Spacetime) : ℂ :=
  contractWick (fun α β γ δ => pointWick α β γ δ x x ψ χ) μ ν

theorem localWickStress_eq_unitaryFourierPointStressForm
    (ψ χ : regularFockDomain) (μ ν : Fin 4) (x : Spacetime) :
    localWickStress ψ χ μ ν x = unitaryFourierPointStressForm ψ χ μ ν x := by
  unfold localWickStress
  simp only [pointWick_finiteKernel]
  rw [contractWick_finiteKernel]
  simp only [contractWick_product]
  unfold unitaryFourierPointStressForm pointStressForm coherentProfileStress
  rw [← finiteKernel_mul_kernel]
  congr 1
  funext h k
  ring

theorem localWickStress_eq_calibrated {D : CanonicalNetInput}
    (A : RemainingModularCoreInput D) (ψ : regularFockDomain)
    (x : Fin 4 → ℝ) (μ ν : Fin 4) :
    (localWickStress ψ ψ μ ν (WithLp.toLp 2 x)).re =
      (toStress (regularMaxwellCalibratedForm A)).T ψ.val x μ ν := by
  rw [localWickStress_eq_unitaryFourierPointStressForm,
    calibratedStress_eq_unitaryFourierFock]

theorem normalizedCircularWick_eq_pointSmear (f g : SchwartzTensor)
    (ψ χ : regularFockDomain) :
    F1Fecho.WickForm.quadratic (normalizedCircularSmearCLM f) (normalizedCircularSmearCLM g)
      (regularDomainInput ψ) (regularDomainInput χ) =
    regularWick (normalizedPointSmearEigenvalue f) (normalizedPointSmearEigenvalue g)
      (regularCircular ψ) (regularCircular χ) := by
  rw [normalizedCircularWick_transport, normalizedPointSmear_Wick]

end F1Fecho.MaxwellGlobal
#print axioms F1Fecho.MaxwellGlobal.pointWick_exponential
#print axioms F1Fecho.MaxwellGlobal.pointWick_finiteKernel
#print axioms F1Fecho.MaxwellGlobal.pointWick_continuous
#print axioms F1Fecho.MaxwellGlobal.contractWick_product
#print axioms F1Fecho.MaxwellGlobal.contractWick_finiteKernel
#print axioms F1Fecho.MaxwellGlobal.localWickStress_eq_unitaryFourierPointStressForm
#print axioms F1Fecho.MaxwellGlobal.localWickStress_eq_calibrated
#print axioms F1Fecho.MaxwellGlobal.normalizedCircularWick_eq_pointSmear
