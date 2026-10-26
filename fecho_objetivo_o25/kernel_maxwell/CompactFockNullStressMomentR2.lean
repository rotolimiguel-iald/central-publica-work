import CoherentNullStressMomentR2
import UnitaryFourierFockStressR1

/-! Finite coherent extension of the proved mixed null moment.
All coefficient supports and tensor values are those of regularFockDomain.
Termwise integrability is proved before commuting the sums with the integral.
The diagonal gives the actual VF boost energy on the AxisCompact coefficient
core. This does not yet provide its translation-invariant certificate domain,
the contract's product-coordinate charge adapter or a nonzero modular witness. -/
set_option autoImplicit false
set_option maxHeartbeats 2200000
noncomputable section

namespace F1Fecho.CoherentKernel
open MeasureTheory
variable {ι α : Type*} [MeasurableSpace α] {μ : Measure α}

theorem finiteKernel_add_kernel (M N : ι → ι → ℂ) (c d : ι →₀ ℂ) :
    finiteKernel (fun i j => M i j + N i j) c d = finiteKernel M c d + finiteKernel N c d := by
  simp only [finiteKernel, Finsupp.sum, mul_add, Finset.sum_add_distrib]

theorem finiteKernel_const_mul_kernel (M : ι → ι → ℂ) (c d : ι →₀ ℂ) (z : ℂ) :
    finiteKernel (fun i j => z * M i j) c d = z * finiteKernel M c d := by
  simp only [finiteKernel, Finsupp.sum, Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro i _
  apply Finset.sum_congr rfl
  intro j _
  ring

theorem finiteKernel_integrable_on_support (M : ι → ι → α → ℂ) (c d : ι →₀ ℂ)
    (hM : ∀ i ∈ c.support, ∀ j ∈ d.support, Integrable (M i j) μ) :
    Integrable (fun x => finiteKernel (fun i j => M i j x) c d) μ := by
  unfold finiteKernel Finsupp.sum
  exact integrable_finsetSum _ (fun i hi => integrable_finsetSum _
    (fun j hj => (hM i hi j hj).const_mul ((starRingEnd ℂ) (c i) * d j)))

theorem integral_finiteKernel_on_support (M : ι → ι → α → ℂ) (c d : ι →₀ ℂ)
    (hM : ∀ i ∈ c.support, ∀ j ∈ d.support, Integrable (M i j) μ) :
    (∫ x, finiteKernel (fun i j => M i j x) c d ∂μ) =
      finiteKernel (fun i j => ∫ x, M i j x ∂μ) c d := by
  unfold finiteKernel Finsupp.sum
  rw [integral_finsetSum _ (fun i hi => integrable_finsetSum _
    (fun j hj => (hM i hi j hj).const_mul ((starRingEnd ℂ) (c i) * d j)))]
  apply Finset.sum_congr rfl
  intro i hi
  rw [integral_finsetSum _
    (fun j hj => (hM i hi j hj).const_mul ((starRingEnd ℂ) (c i) * d j))]
  simp only [integral_const_mul]

end F1Fecho.CoherentKernel

namespace F1Fecho.MaxwellGlobal
open MeasureTheory TGLExt.ImportedSQ TGLExt.ContratoQGv31
open F1Fecho.CoherentKernel F1Rede.BosonicFockGroupActions

def unitaryFourierFockNullStress (ψ χ : regularFockDomain) (x : NullFourierSpace) : ℂ :=
  unitaryFourierPointStressForm ψ χ 0 0 (nullPlanePoint (x 0) (nullFourierScreen x)) +
  unitaryFourierPointStressForm ψ χ 0 1 (nullPlanePoint (x 0) (nullFourierScreen x)) +
  unitaryFourierPointStressForm ψ χ 1 0 (nullPlanePoint (x 0) (nullFourierScreen x)) +
  unitaryFourierPointStressForm ψ χ 1 1 (nullPlanePoint (x 0) (nullFourierScreen x))

theorem unitaryFourierPointStressForm_eq_finiteKernel (ψ χ : regularFockDomain)
    (μ ν : Fin 4) (x : Spacetime) :
    unitaryFourierPointStressForm ψ χ μ ν x =
      finiteKernel (fun h k : RegularLabel => unitaryFourierCoherentStress h.val k.val μ ν x)
        (regularCoefficients ψ) (regularCoefficients χ) := by
  exact (finiteKernel_const_mul_kernel
    (fun h k : RegularLabel => coherentProfileStress h.val k.val μ ν x)
    (regularCoefficients ψ) (regularCoefficients χ) (unitaryFourierStressScale : ℂ)).symm

theorem unitaryFourierFockNullStress_eq_finiteKernel (ψ χ : regularFockDomain)
    (x : NullFourierSpace) :
    unitaryFourierFockNullStress ψ χ x =
      finiteKernel (fun h k : RegularLabel => unitaryFourierCoherentNullStress h.val k.val x)
        (regularCoefficients ψ) (regularCoefficients χ) := by
  simp only [unitaryFourierFockNullStress, unitaryFourierPointStressForm_eq_finiteKernel,
    unitaryFourierCoherentNullStress, finiteKernel_add_kernel]

theorem axisCompact_fockNullStress_moment_integrable (ψ χ : regularFockDomain)
    (hψ : AxisCompactFock ψ) (hχ : AxisCompactFock χ) :
    Integrable (fun x : NullFourierSpace => (x 0 : ℂ) * unitaryFourierFockNullStress ψ χ x) := by
  have hi := finiteKernel_integrable_on_support
    (fun h k : RegularLabel => fun x : NullFourierSpace =>
      (x 0 : ℂ) * unitaryFourierCoherentNullStress h.val k.val x)
    (regularCoefficients ψ) (regularCoefficients χ)
    (fun h hh k hk => axisCompact_coherentNullStress_moment_integrable h.val k.val
      (hψ h hh) (hχ k hk))
  simpa only [unitaryFourierFockNullStress_eq_finiteKernel,
    finiteKernel_const_mul_kernel] using hi

theorem axisCompact_fockNullStress_moment (ψ χ : regularFockDomain)
    (hψ : AxisCompactFock ψ) (hχ : AxisCompactFock χ) :
    (∫ x : NullFourierSpace, (x 0 : ℂ) * unitaryFourierFockNullStress ψ χ x) =
      -Complex.I * regularFockBoostPair ψ χ := by
  calc
    _ = ∫ x : NullFourierSpace, finiteKernel
        (fun h k : RegularLabel => (x 0 : ℂ) * unitaryFourierCoherentNullStress h.val k.val x)
        (regularCoefficients ψ) (regularCoefficients χ) := by
      apply integral_congr_ae
      filter_upwards [] with x
      rw [unitaryFourierFockNullStress_eq_finiteKernel, finiteKernel_const_mul_kernel]
    _ = finiteKernel (fun h k : RegularLabel =>
        ∫ x : NullFourierSpace, (x 0 : ℂ) * unitaryFourierCoherentNullStress h.val k.val x)
        (regularCoefficients ψ) (regularCoefficients χ) :=
      integral_finiteKernel_on_support _ _ _ (fun h hh k hk =>
        axisCompact_coherentNullStress_moment_integrable h.val k.val (hψ h hh) (hχ k hk))
    _ = finiteKernel (fun h k : RegularLabel => -Complex.I * coherentBoostPair h.val k.val)
        (regularCoefficients ψ) (regularCoefficients χ) := by
      unfold finiteKernel Finsupp.sum
      apply Finset.sum_congr rfl
      intro h hh
      apply Finset.sum_congr rfl
      intro k hk
      rw [axisCompact_coherentNullStress_moment h.val k.val (hψ h hh) (hχ k hk)]
    _ = _ := finiteKernel_const_mul_kernel _ _ _ _

theorem axisCompact_fockNullStress_real_moment_integrable (ψ : regularFockDomain)
    (hψ : AxisCompactFock ψ) :
    Integrable (fun x : NullFourierSpace => x 0 * (unitaryFourierFockNullStress ψ ψ x).re) := by
  have hi := (axisCompact_fockNullStress_moment_integrable ψ ψ hψ hψ).re
  simpa only [RCLike.re_eq_complex_re, Complex.mul_re, Complex.ofReal_re,
    Complex.ofReal_im, zero_mul, sub_zero] using hi

theorem axisCompact_fockNullStress_real_moment (ψ : regularFockDomain)
    (hψ : AxisCompactFock ψ) :
    (∫ x : NullFourierSpace, x 0 * (unitaryFourierFockNullStress ψ ψ x).re) =
      (regularFockBoostPair ψ ψ).im := by
  have hr := integral_re (axisCompact_fockNullStress_moment_integrable ψ ψ hψ hψ)
  simp only [RCLike.re_eq_complex_re, Complex.mul_re, Complex.ofReal_re,
    Complex.ofReal_im, zero_mul, sub_zero] at hr
  rw [hr, axisCompact_fockNullStress_moment ψ ψ hψ hψ]
  simp [Complex.mul_re]

/-- The actual finite coherent VF energy equals the real normalized tensor moment. -/
theorem axisCompact_fock_hasBoostEnergy_null_moment (ψ : regularFockDomain)
    (hψ : AxisCompactFock ψ) :
    HasBoostEnergy VF ψ.val
      (∫ x : NullFourierSpace, x 0 * (unitaryFourierFockNullStress ψ ψ x).re) := by
  rw [axisCompact_fockNullStress_real_moment ψ hψ]
  exact axisCompact_regularFock_hasBoostEnergy ψ hψ

end F1Fecho.MaxwellGlobal

#print axioms F1Fecho.CoherentKernel.finiteKernel_add_kernel
#print axioms F1Fecho.CoherentKernel.finiteKernel_const_mul_kernel
#print axioms F1Fecho.CoherentKernel.finiteKernel_integrable_on_support
#print axioms F1Fecho.CoherentKernel.integral_finiteKernel_on_support
#print axioms F1Fecho.MaxwellGlobal.unitaryFourierPointStressForm_eq_finiteKernel
#print axioms F1Fecho.MaxwellGlobal.unitaryFourierFockNullStress_eq_finiteKernel
#print axioms F1Fecho.MaxwellGlobal.axisCompact_fockNullStress_moment_integrable
#print axioms F1Fecho.MaxwellGlobal.axisCompact_fockNullStress_moment
#print axioms F1Fecho.MaxwellGlobal.axisCompact_fockNullStress_real_moment_integrable
#print axioms F1Fecho.MaxwellGlobal.axisCompact_fockNullStress_real_moment
#print axioms F1Fecho.MaxwellGlobal.axisCompact_fock_hasBoostEnergy_null_moment
