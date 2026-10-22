import ContinuousModularDomain
import Mathlib.Analysis.InnerProductSpace.StarOrder
import Mathlib.Analysis.CStarAlgebra.ContinuousFunctionalCalculus.Order
import Mathlib.Analysis.SpecialFunctions.ContinuousFunctionalCalculus.Rpow.Basic
open ChatgptAudit.Continuous049
open scoped ComplexOrder
noncomputable section
section ModuleOnly
local instance instSpectralOperatorRealModule : Module ℝ (SpectralHilbert →L[ℂ] SpectralHilbert) :=
  Module.restrictScalars ℝ ℂ (SpectralHilbert →L[ℂ] SpectralHilbert)
#synth NonUnitalContinuousFunctionalCalculus ℝ (SpectralHilbert →L[ℂ] SpectralHilbert) IsSelfAdjoint
#synth NonnegSpectrumClass ℝ (SpectralHilbert →L[ℂ] SpectralHilbert)
#check CFC.sqrt (spectralA 0)
#print axioms instSpectralOperatorRealModule
end ModuleOnly
section AlgebraOnly
local instance instSpectralOperatorRealAlgebra : Algebra ℝ (SpectralHilbert →L[ℂ] SpectralHilbert) :=
  Algebra.restrictScalars ℝ ℂ (SpectralHilbert →L[ℂ] SpectralHilbert)
#synth NonUnitalContinuousFunctionalCalculus ℝ (SpectralHilbert →L[ℂ] SpectralHilbert) IsSelfAdjoint
#synth NonnegSpectrumClass ℝ (SpectralHilbert →L[ℂ] SpectralHilbert)
#check CFC.sqrt (spectralA 0)
#print axioms instSpectralOperatorRealAlgebra
end AlgebraOnly
