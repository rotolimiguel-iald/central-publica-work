import TGLExt.F1Fecho394.CanonicalZeroSectorResolventR1
import TGLExt.F1Fecho394.CanonicalFockModularFlowR2
import TGLExt.F1Fecho394.ImaginaryPowerIntertwiningR2
import Mathlib.Analysis.CStarAlgebra.ContinuousLinearMap
/-! The spectral modular flow fixes the actual zero-particle component.
This follows from the measured resolvent relation through continuous calculus
and the dense damped range; no sector-preservation premise is introduced. -/
set_option autoImplicit false
set_option maxHeartbeats 1500000
noncomputable section
namespace F1Fecho.CanonicalZeroSector
open TGLExt.ImportedSQ F1Rede.BosonicSectors F1Rede.BosonicFock
open F1Fecho.CanonicalFockPolar TGLV350.Regular ChatgptAudit

section ScalarOperators
variable {E:Type} [NormedAddCommGroup E] [InnerProductSpace ℂ E] [CompleteSpace E]
lemma half_selfadjoint_generic :
    IsSelfAdjoint (algebraMap ℂ (E→L[ℂ]E) (1/2)) := by
  change star (algebraMap ℂ (E→L[ℂ]E) (1/2))=_
  rw [←algebraMap_star_comm]
  congr 1
  norm_num
lemma half_phase_generic (t:ℝ) :
    resolventPhaseOperator (algebraMap ℂ (E→L[ℂ]E) (1/2)) t=
      algebraMap ℂ (E→L[ℂ]E) (1/4) := by
  unfold resolventPhaseOperator
  rw [cfc_algebraMap]
  congr 1
  norm_num [resolventPhaseFunction,resolventDamping,modularPhase]
end ScalarOperators

def Q0 : F →L[ℂ] Sector 0 := lp.evalCLM ℂ (fun n => Sector n) 2 0
def halfIdentity : Sector 0 →L[ℂ] Sector 0 :=
  algebraMap ℂ (Sector 0 →L[ℂ] Sector 0) (1/2)

theorem Q0_resolvent : Q0.comp modularR = halfIdentity.comp Q0 := by
  ext1 x
  exact modularR_zero x

theorem halfIdentity_selfadjoint : IsSelfAdjoint halfIdentity :=
  half_selfadjoint_generic

theorem halfIdentity_phase (t : ℝ) :
    resolventPhaseOperator halfIdentity t =
      algebraMap ℂ (Sector 0 →L[ℂ] Sector 0) (1/4) := half_phase_generic t

theorem Q0_damping (x : F) :
    (resolventDampingOperator modularR x) 0 = (1/4 : ℂ) • x 0 := by
  change modularR (x-modularR x) 0 = _
  rw [modularR_zero]
  change (1/2 : ℂ) • (x 0-modularR x 0) = _
  rw [modularR_zero,smul_sub,smul_smul]
  module

theorem Q0_phase (t : ℝ) (x : F) :
    (resolventPhaseOperator modularR t x) 0 = (1/4 : ℂ) • x 0 := by
  have h := ContinuousIntertwining.phase_intertwine modularR halfIdentity Q0
    Q0_resolvent (IsSelfAdjoint.of_nonneg modularR_nonneg)
    halfIdentity_selfadjoint t x
  rw [halfIdentity_phase] at h
  exact h

theorem modularFlow_zero_component (t : ℝ) (x : F) :
    (actualModularFlow t x) 0 = x 0 := by
  refine (resolventDampingOperator_denseRange modularR modularR_nonneg
    modularR_le_one modularR_injective modularR_complement_injective).induction
    ?_ (isClosed_eq (Q0.continuous.comp (actualModularFlow t).continuous)
      Q0.continuous) x
  rintro _ ⟨y,rfl⟩
  rw [actualModularFlow_readout,Q0_phase,Q0_damping]

end F1Fecho.CanonicalZeroSector
#print axioms F1Fecho.CanonicalZeroSector.Q0_resolvent
#print axioms F1Fecho.CanonicalZeroSector.halfIdentity_phase
#print axioms F1Fecho.CanonicalZeroSector.Q0_damping
#print axioms F1Fecho.CanonicalZeroSector.Q0_phase
#print axioms F1Fecho.CanonicalZeroSector.modularFlow_zero_component
