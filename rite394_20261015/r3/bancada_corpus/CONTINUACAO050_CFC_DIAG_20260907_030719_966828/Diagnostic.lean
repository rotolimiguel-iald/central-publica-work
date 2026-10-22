import ContinuousModularDomain
import Mathlib.Analysis.InnerProductSpace.StarOrder
import Mathlib.Analysis.CStarAlgebra.ContinuousFunctionalCalculus.Order
import Mathlib.Analysis.SpecialFunctions.ContinuousFunctionalCalculus.Rpow.Basic

open ChatgptAudit.Continuous049
open scoped ComplexOrder
noncomputable section

#synth CompleteSpace SpectralHilbert
#synth CompleteSpace (SpectralHilbert →L[ℂ] SpectralHilbert)
#synth CStarAlgebra (SpectralHilbert →L[ℂ] SpectralHilbert)
#synth StarOrderedRing (SpectralHilbert →L[ℂ] SpectralHilbert)
#synth ContinuousFunctionalCalculus ℝ (SpectralHilbert →L[ℂ] SpectralHilbert) IsSelfAdjoint
#synth IsometricContinuousFunctionalCalculus ℝ (SpectralHilbert →L[ℂ] SpectralHilbert) IsSelfAdjoint
#synth NonUnitalIsometricContinuousFunctionalCalculus ℝ (SpectralHilbert →L[ℂ] SpectralHilbert) IsSelfAdjoint
#synth NonUnitalContinuousFunctionalCalculus ℝ (SpectralHilbert →L[ℂ] SpectralHilbert) IsSelfAdjoint

variable {H : Type*} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
#synth ContinuousFunctionalCalculus ℝ (H →L[ℂ] H) IsSelfAdjoint
#synth NonUnitalContinuousFunctionalCalculus ℝ (H →L[ℂ] H) IsSelfAdjoint
#check @IsSelfAdjoint.instNonUnitalIsometricContinuousFunctionalCalculus
#check @ContinuousFunctionalCalculus.toNonUnital
