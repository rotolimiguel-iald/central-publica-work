import TGLExt.F1Fecho394.MaxwellScreenIntertwinerR2
import TGLExt.TheImportedSecondQuantization
import Mathlib.Topology.ContinuousMap.CompactlySupported
import Mathlib.MeasureTheory.Function.LpSpace.Indicator

/-! A concrete momentum-space test-bivector map into the original H1.
Tests are continuous compactly supported tensor functions in the regular
rapidity chart (support away from the null coordinate axis). The coefficient
is the contraction (1/2) F^{mu nu} test_{mu nu} in the existing real screen basis.
This does not assert that every spacetime Schwartz tensor restricts to this
class; that Fourier restriction and its global support properties are separate. -/
set_option autoImplicit false
set_option maxHeartbeats 1600000
noncomputable section
namespace F1Fecho.MaxwellSmearing
open MeasureTheory Matrix Filter
open ChatgptAudit.WignerRapidityMeasure016 TGLExt.ImportedSQ F1Fecho.MaxwellOnShell
open scoped ENNReal CompactlySupported

abbrev TestTensor := C_c(MomentumCoordinates, Matrix (Fin 4) (Fin 4) ℂ)

def coefficient (f : TestTensor) (y : MomentumCoordinates) : Fib :=
  WithLp.toLp 2 (fun j => (1/2:ℂ)*∑ μ,∑ ν,
    strength (momentum y) (realLift (screen y j)) μ ν * f y μ ν)

theorem coefficient_zero_at (f : TestTensor) (y : MomentumCoordinates) (hf : f y=0) :
    coefficient f y=0 := by
  apply PiLp.ext
  intro j
  simp [coefficient,hf]

theorem coefficient_tsupport (f : TestTensor) : tsupport (coefficient f)⊆tsupport f := by
  apply closure_mono
  intro y hy
  change coefficient f y≠0 at hy
  change f y≠0
  intro hz
  exact hy (coefficient_zero_at f y hz)

theorem coefficient_continuousAt (f : TestTensor) (y : MomentumCoordinates) (hy : y.1≠0) :
    ContinuousAt (coefficient f) y := by
  have hr : transverseMass 0 y.1≠0 := (transverseMass_pos_of_ne_zero 0 y.1 hy).ne'
  have hs1 : ContinuousAt screenOne y := by unfold screenOne; fun_prop
  have hm : Continuous (fun z : MomentumCoordinates => transverseMass 0 z.1) := by
    unfold transverseMass
    fun_prop
  have hs2 : ContinuousAt screenTwo y := by
    unfold screenTwo
    fun_prop (disch := exact hr)
  have hs (j : Fin 2) : ContinuousAt (fun z => screen z j) y := by
    fin_cases j
    · exact hs1
    · exact hs2
  have hp : Continuous momentum := by
    unfold momentum
    exact continuous_pi (fun i => Complex.continuous_ofReal.comp
      ((continuous_apply i).comp ((shellMomentum_continuous 0).comp (rapidityChart_continuous 0))))
  apply (PiLp.continuous_toLp 2 (fun _ : Fin 2 => ℂ)).continuousAt.comp
  apply continuousAt_pi.mpr
  intro j
  have hsj := hs j
  unfold strength realLift
  apply continuousAt_const.mul
  apply tendsto_finsetSum
  intro μ _
  apply tendsto_finsetSum
  intro ν _
  have hpμ : ContinuousAt (fun z => momentum z μ) y := (continuous_apply μ).continuousAt.comp hp.continuousAt
  have hpν : ContinuousAt (fun z => momentum z ν) y := (continuous_apply ν).continuousAt.comp hp.continuousAt
  have hsμ := Complex.continuous_ofReal.continuousAt.comp
    ((continuous_apply μ).continuousAt.comp hsj)
  have hsν := Complex.continuous_ofReal.continuousAt.comp
    ((continuous_apply ν).continuousAt.comp hsj)
  have hf : ContinuousAt (fun z => f z μ ν) y := (continuous_apply ν).continuousAt.comp
    ((continuous_apply μ).continuousAt.comp f.continuous.continuousAt)
  exact ((hpμ.mul hsν).sub (hpν.mul hsμ)).mul hf

theorem coefficient_continuous (f : TestTensor)
    (hreg : ∀ y∈tsupport f,y.1≠0) : Continuous (coefficient f) := by
  apply continuous_of_tsupport
  intro y hy
  exact coefficient_continuousAt f y (hreg y (coefficient_tsupport f hy))

theorem coefficient_compact (f : TestTensor) : HasCompactSupport (coefficient f) :=
  f.hasCompactSupport.of_isClosed_subset (isClosed_tsupport _) (coefficient_tsupport f)

theorem coefficient_memLp (f : TestTensor)
    (hreg : ∀ y∈tsupport f,y.1≠0) : MemLp (coefficient f) 2 momentumMeasure := by
  letI : IsFiniteMeasureOnCompacts momentumMeasure := by unfold momentumMeasure; infer_instance
  exact (coefficient_continuous f hreg).memLp_of_hasCompactSupport (coefficient_compact f)

def smear (f : TestTensor) (hreg : ∀ y∈tsupport f,y.1≠0) : H1 :=
  orbitalL2Inverse 0 ((coefficient_memLp f hreg).toLp (coefficient f))

theorem smear_rapidity_ae (f : TestTensor) (hreg : ∀ y∈tsupport f,y.1≠0) :
    orbitalL2Pullback 0 (smear f hreg)=ᵐ[momentumMeasure] coefficient f := by
  rw [smear,orbitalL2Pullback_inverse]
  exact (coefficient_memLp f hreg).coeFn_toLp

end F1Fecho.MaxwellSmearing
#print axioms F1Fecho.MaxwellSmearing.coefficient_continuous
#print axioms F1Fecho.MaxwellSmearing.coefficient_memLp
#print axioms F1Fecho.MaxwellSmearing.smear
#print axioms F1Fecho.MaxwellSmearing.smear_rapidity_ae
