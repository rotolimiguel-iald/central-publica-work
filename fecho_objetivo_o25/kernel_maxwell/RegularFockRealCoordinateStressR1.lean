import RegularFockStressContinuityR4
import RegularFockStressTranslationR3
import TGLExt.MaxwellLiteratureBridge
import Mathlib.Analysis.Calculus.LineDeriv.IntegrationByParts
import Mathlib.Analysis.Calculus.ContDiff.Operations
import Mathlib.MeasureTheory.Function.LocallyIntegrable
import Mathlib.Analysis.Complex.Basic
import Mathlib.Tactic

/-! Weak conservation from actual continuous coordinate derivatives, via
mathlib integration by parts. No equation is added to the concrete Maxwell
consumer: it will supply the already proved pointwise divergence. -/
set_option autoImplicit false
set_option maxHeartbeats 1200000
noncomputable section
namespace F1Fecho.RealCompactConservation
open MeasureTheory Measure
variable {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E]
  [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
  (μ : Measure E) [IsAddHaarMeasure μ]

 theorem compact_test_ibp (A D : E→ℝ) (v : E) (hA : Continuous A) (hD : Continuous D)
    (hAD : ∀x,HasLineDerivAt ℝ A (D x) x v) (f : E→ℝ)
    (hf : ContDiff ℝ (⊤ : ℕ∞) f) (hc : HasCompactSupport f) :
    (∫x,A x*(fderiv ℝ f x v) ∂μ)= -(∫x,D x*f x ∂μ) := by
  have hfd : Continuous (fun x=>fderiv ℝ f x v) :=
    (hf.continuous_fderiv (by simp)).clm_apply continuous_const
  apply integral_bilinear_hasLineDerivAt_right_eq_neg_left_of_integrable
    (B:=ContinuousLinearMap.mul ℝ ℝ)
  · exact (hD.mul hf.continuous).integrable_of_hasCompactSupport hc.mul_left
  · exact (hA.mul hfd).integrable_of_hasCompactSupport (hc.fderiv_apply ℝ v).mul_left
  · exact (hA.mul hf.continuous).integrable_of_hasCompactSupport hc.mul_left
  · exact fun x _=>hAD x
  · exact fun x _=>(hf.differentiable (by simp) x).hasFDerivAt.hasLineDerivAt v

 theorem compact_test_integrable (A : E→ℝ) (v : E) (hA : Continuous A)
    (f : E→ℝ) (hf : ContDiff ℝ (⊤ : ℕ∞) f) (hc : HasCompactSupport f) :
    Integrable (fun x=>A x*(fderiv ℝ f x v)) μ := by
  have hfd : Continuous (fun x=>fderiv ℝ f x v) :=
    (hf.continuous_fderiv (by simp)).clm_apply continuous_const
  exact (hA.mul hfd).integrable_of_hasCompactSupport (hc.fderiv_apply ℝ v).mul_left

 theorem weak_conservation {ι : Type*} [Fintype ι] (A D : ι→E→ℝ) (v : ι→E) (s : ι→ℝ)
    (hA : ∀i,Continuous (A i)) (hD : ∀i,Continuous (D i))
    (hAD : ∀i x,HasLineDerivAt ℝ (A i) (D i x) x (v i))
    (hdiv : ∀x,∑i,s i*D i x=0) (f : E→ℝ)
    (hf : ContDiff ℝ (⊤ : ℕ∞) f) (hc : HasCompactSupport f) :
    (∑i,∫x,s i*A i x*(fderiv ℝ f x (v i)) ∂μ)=0 := by
  have hi (i : ι) : Integrable (fun x=>s i*(D i x*f x)) μ :=
    ((hD i).mul hf.continuous).integrable_of_hasCompactSupport hc.mul_left |>.const_mul _
  calc
    _ = -(∑i,∫x,s i*(D i x*f x) ∂μ) := by
      rw [← Finset.sum_neg_distrib]
      apply Finset.sum_congr rfl
      intro i _
      simp only [mul_assoc,integral_const_mul,
        compact_test_ibp μ (A i) (D i) (v i) (hA i) (hD i) (hAD i) f hf hc,mul_neg]
    _ = -(∫x,∑i,s i*(D i x*f x) ∂μ) := by
      rw [integral_finsetSum Finset.univ (fun i _=>hi i)]
    _ = 0 := by
      have he (x : E) : (∑i,s i*(D i x*f x))=0 := by
        simp only [← mul_assoc,← Finset.sum_mul,hdiv x,zero_mul]
      simp only [he,integral_zero,neg_zero]

end F1Fecho.RealCompactConservation

/-! The actual regular Fock stress in the real coordinate and test-function
conventions of MaxwellQuadraticForm. Weak conservation follows from the
proved pointwise derivatives by integration by parts on the actual Pi4
Lebesgue measure. No new conservation assumption is introduced.
The charge identity, modular-energy witness and final Maxwell certificate
remain separate obligations of R8. Production sources are not modified. -/
namespace F1Fecho.MaxwellGlobal
open MeasureTheory TGLExt.ImportedSQ TGLExt.ContratoQGv32
open ChatgptAudit.WignerRapidityMeasure016

 def realCoordinateStress (ψ : regularFockDomain) (x : Fin 4→ℝ)
    (μ ν : Fin 4) : ℝ :=
  (pointStressForm ψ ψ μ ν (WithLp.toLp 2 x)).re

 def realCoordinateStressPartial (ψ : regularFockDomain) (ρ μ ν : Fin 4)
    (x : Fin 4→ℝ) : ℝ :=
  (deriv (fun t : ℝ=>pointStressForm ψ ψ μ ν
    (WithLp.toLp 2 x+t • spacetimeBasis ρ)) 0).re

 theorem realCoordinateStress_continuous (ψ : regularFockDomain) (μ ν : Fin 4) :
    Continuous (fun x=>realCoordinateStress ψ x μ ν) :=
  Complex.continuous_re.comp ((pointStressForm_continuous ψ ψ μ ν).comp
    PiLp.continuous_toLp)

 theorem realCoordinateStressPartial_continuous (ψ : regularFockDomain)
    (ρ μ ν : Fin 4) : Continuous (realCoordinateStressPartial ψ ρ μ ν) :=
  Complex.continuous_re.comp ((pointStressForm_partial_continuous ψ ψ ρ μ ν).comp
    PiLp.continuous_toLp)

 theorem coordinateLine (x : Fin 4→ℝ) (t : ℝ) (ρ : Fin 4) :
    WithLp.toLp 2 (x+t • Pi.single ρ 1)=
      WithLp.toLp 2 x+t • spacetimeBasis ρ := by
  simp [WithLp.toLp_add,WithLp.toLp_smul,PiLp.toLp_single,spacetimeBasis]

 theorem realCoordinateStress_hasLineDerivAt (ψ : regularFockDomain)
    (ρ μ ν : Fin 4) (x : Fin 4→ℝ) :
    HasLineDerivAt ℝ (fun y=>realCoordinateStress ψ y μ ν)
      (realCoordinateStressPartial ψ ρ μ ν x) x (Pi.single ρ 1) := by
  have h := (pointStressForm_line_hasDerivAt ψ ψ ρ μ ν (WithLp.toLp 2 x)).differentiableAt.hasDerivAt
  have hr := Complex.reCLM.hasFDerivAt.comp_hasDerivAt 0 h
  simpa only [HasLineDerivAt,realCoordinateStress,realCoordinateStressPartial,
    coordinateLine,Complex.reCLM_apply,Function.comp_apply] using hr

 theorem metricSignC_eq_ofReal (μ : Fin 4) : metricSignC μ=(metricSignV32 μ:ℂ) := by
  by_cases h : μ=0 <;> simp [metricSignC,metricSignV32,h]

 theorem realCoordinateStress_divergence (ψ : regularFockDomain) (ν : Fin 4)
    (x : Fin 4→ℝ) :
    (∑μ : Fin 4,metricSignV32 μ*realCoordinateStressPartial ψ μ μ ν x)=0 := by
  have h := congrArg Complex.re (pointStressForm_conserved ψ ψ ν (WithLp.toLp 2 x))
  simpa only [Complex.sum_re,metricSignC_eq_ofReal,Complex.mul_re,
    Complex.ofReal_re,Complex.ofReal_im,zero_mul,sub_zero,Complex.zero_re,
    realCoordinateStressPartial] using h

 theorem realCoordinateStress_test_integrable (ψ : regularFockDomain) (ν μ : Fin 4)
    (f : (Fin 4→ℝ)→ℝ) (hf : ContDiff ℝ (⊤ : ℕ∞) f) (hc : HasCompactSupport f) :
    Integrable (fun x=>metricSignV32 μ*realCoordinateStress ψ x μ ν*
      testDerivativeV32 f μ x) := by
  simpa only [mul_assoc,testDerivativeV32] using
    (F1Fecho.RealCompactConservation.compact_test_integrable volume
      (fun x=>realCoordinateStress ψ x μ ν) (Pi.single μ 1)
      (realCoordinateStress_continuous ψ μ ν) f hf hc).const_mul (metricSignV32 μ)

 theorem realCoordinateStress_conserved (ψ : regularFockDomain) (ν : Fin 4)
    (f : (Fin 4→ℝ)→ℝ) (hf : ContDiff ℝ (⊤ : ℕ∞) f) (hc : HasCompactSupport f) :
    (∑μ : Fin 4,∫x : Fin 4→ℝ,metricSignV32 μ*realCoordinateStress ψ x μ ν*
      testDerivativeV32 f μ x)=0 := by
  exact F1Fecho.RealCompactConservation.weak_conservation volume
    (fun μ x=>realCoordinateStress ψ x μ ν)
    (fun μ=>realCoordinateStressPartial ψ μ μ ν) (fun μ=>Pi.single μ 1) metricSignV32
    (fun μ=>realCoordinateStress_continuous ψ μ ν)
    (fun μ=>realCoordinateStressPartial_continuous ψ μ μ ν)
    (fun μ x=>realCoordinateStress_hasLineDerivAt ψ μ μ ν x)
    (realCoordinateStress_divergence ψ ν) f hf hc

 theorem realCoordinateStress_symmetric (ψ : regularFockDomain) (x : Fin 4→ℝ) :
    (realCoordinateStress ψ x).transpose=realCoordinateStress ψ x := by
  ext μ ν
  exact congrArg Complex.re (pointStressForm_symmetric ψ ψ ν μ (WithLp.toLp 2 x))

 theorem realCoordinateStress_vacuum (x : Fin 4→ℝ) :
    realCoordinateStress regularVacuum x=0 := by
  ext μ ν
  simp only [realCoordinateStress,pointStressForm_vacuum,Complex.zero_re,Matrix.zero_apply]

 theorem realCoordinateStress_nontrivial :
    ∃ψ : regularFockDomain,0<realCoordinateStress ψ 0 0 0 := by
  simpa only [realCoordinateStress,WithLp.toLp_zero] using pointStressForm_nontrivial

 theorem realCoordinateStress_translate (a : Fin 4→ℝ) (ψ : regularFockDomain)
    (x : Fin 4→ℝ) :
    realCoordinateStress (regularGamma (U1 a) (strongRegularProfile_U1 a) ψ) x=
      realCoordinateStress ψ (x-a) := by
  ext μ ν
  simp only [realCoordinateStress,pointStressForm_translate,WithLp.toLp_sub]

end F1Fecho.MaxwellGlobal
#print axioms F1Fecho.RealCompactConservation.compact_test_ibp
#print axioms F1Fecho.RealCompactConservation.weak_conservation
#print axioms F1Fecho.MaxwellGlobal.realCoordinateStress_hasLineDerivAt
#print axioms F1Fecho.MaxwellGlobal.realCoordinateStress_test_integrable
#print axioms F1Fecho.MaxwellGlobal.realCoordinateStress_conserved
#print axioms F1Fecho.MaxwellGlobal.realCoordinateStress_symmetric
#print axioms F1Fecho.MaxwellGlobal.realCoordinateStress_vacuum
#print axioms F1Fecho.MaxwellGlobal.realCoordinateStress_nontrivial
#print axioms F1Fecho.MaxwellGlobal.realCoordinateStress_translate
