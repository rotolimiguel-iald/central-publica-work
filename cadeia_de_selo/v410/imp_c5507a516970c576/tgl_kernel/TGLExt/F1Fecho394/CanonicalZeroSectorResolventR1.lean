import TGLExt.F1Fecho394.CanonicalFockGraphRealizationR3
import TGLExt.F1Fecho394.BoundedPairResolventEquationR2
/-! The actual modular resolvent on the vacuum sector is one half.
The proof uses the constructed bounded graph parameters and their resolvent
equation. It does not assume that the resolvent preserves particle sectors. -/
set_option autoImplicit false
set_option maxHeartbeats 1200000
noncomputable section
open UniformSpace
namespace F1Fecho.CanonicalZeroSector
open TGLExt.ImportedSQ F1Rede.BosonicSectors F1Rede.BosonicFock
open F1Fecho.ExponentialLift F1Fecho.GammaGraph F1Fecho.CanonicalFockPolar

theorem tensor_zero (A : H1 →L[ℂ] H1) (x : TensorHilbert 0) :
    BoundedGamma.tensor A 0 x = x := by
  refine Completion.induction_on x
    (isClosed_eq (BoundedGamma.tensor A 0).continuous continuous_id) ?_
  intro z
  rw [BoundedGamma.tensor_coe]
  rfl

theorem sector_zero (A : H1 →L[ℂ] H1) (x : Sector 0) :
    BoundedGamma.sector A 0 x = x := by
  apply Subtype.ext
  exact tensor_zero A x

theorem GA_zero (x : F) : GA x 0 = x 0 :=
  sector_zero _ _

theorem GB_zero (x : F) : GB x 0 = x 0 :=
  sector_zero _ _

theorem modularR_zero (x : F) :
    modularR x 0 = (1/2 : ℂ) • x 0 := by
  have he := BoundedPairResolvent.equation canonicalLift canonicalLift_selfadjoint
    GA GB GA_selfadjoint GB_selfadjoint graph_parameters GAB_commute
  have h := congrArg (fun L : F →L[ℂ] F => L x 0) he
  change GA (GA (modularR x)) 0 + GB (GB (modularR x)) 0 = GA (GA x) 0 at h
  simp only [GA_zero,GB_zero] at h
  have h2 : (2 : ℂ) • (modularR x) 0 = x 0 := by
    simpa only [two_smul ℂ] using h
  calc
    modularR x 0 = (1/2 : ℂ) • ((2 : ℂ) • (modularR x) 0) := by
      rw [smul_smul]
      norm_num
    _ = (1/2 : ℂ) • x 0 := by rw [h2]

end F1Fecho.CanonicalZeroSector
#print axioms F1Fecho.CanonicalZeroSector.tensor_zero
#print axioms F1Fecho.CanonicalZeroSector.sector_zero
#print axioms F1Fecho.CanonicalZeroSector.GA_zero
#print axioms F1Fecho.CanonicalZeroSector.GB_zero
#print axioms F1Fecho.CanonicalZeroSector.modularR_zero
