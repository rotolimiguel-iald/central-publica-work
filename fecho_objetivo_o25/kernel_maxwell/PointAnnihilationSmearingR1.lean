import LocalWickStressIdentificationR1

/-! Candidate R51. Actual Bochner smearing of the point annihilator, on every
state of the existing regular coherent domain. Integrability is discharged
from the old regular-profile Fourier pairing and finite sums. The result is
the old normalized physical annihilation operator, not an assumed Wick link.
No global bounded point field, new representation or point creation operator
is introduced. -/
set_option Elab.async false
set_option autoImplicit false
set_option maxHeartbeats 400000
set_option synthInstance.maxHeartbeats 500000
noncomputable section
namespace F1Fecho.MaxwellGlobal
open MeasureTheory Filter TGLExt.ImportedSQ F1Rede.BosonicFock
open F1Fecho.Exponential F1Fecho.Annihilation

theorem regularDiagonal_add_eigenvalue (v w : RegularLabel → ℂ) :
    regularDiagonal (v + w) = regularDiagonal v + regularDiagonal w := by
  apply regularLinearMap_ext
  intro h
  simp only [regularDiagonal_exponential, LinearMap.add_apply, Pi.add_apply, add_smul]

theorem regularDiagonal_smul_eigenvalue (z : ℂ) (v : RegularLabel → ℂ) :
    regularDiagonal (z • v) = z • regularDiagonal v := by
  apply regularLinearMap_ext
  intro h
  simp only [regularDiagonal_exponential, LinearMap.smul_apply, Pi.smul_apply,
    smul_eq_mul, mul_smul]

def regularEigenvalueLM (ψ : regularFockDomain) :
    (RegularLabel → ℂ) →ₗ[ℂ] regularFockDomain where
  toFun v := regularDiagonal v ψ
  map_add' v w := congrArg (fun L : regularFockDomain →ₗ[ℂ] regularFockDomain => L ψ)
    (regularDiagonal_add_eigenvalue v w)
  map_smul' z v := congrArg (fun L : regularFockDomain →ₗ[ℂ] regularFockDomain => L ψ)
    (regularDiagonal_smul_eigenvalue z v)

theorem regularDiagonal_value_expansion (v : RegularLabel → ℂ) (ψ : regularFockDomain) :
    (regularDiagonal v ψ).val = (regularCoefficients ψ).sum
      (fun h z => z • (v h • exponential h.val)) := by
  have he := regularLinearMap_expansion (regularFockDomain.subtype.comp (regularDiagonal v)) ψ
  simpa only [LinearMap.comp_apply, regularDiagonal_exponential, Submodule.coe_smul,
    regularExponential] using he

theorem regularDiagonal_integrable (v : Spacetime → RegularLabel → ℂ)
    (hv : ∀ h, Integrable (fun x => v x h)) (ψ : regularFockDomain) :
    Integrable (fun x => (regularDiagonal (v x) ψ).val) := by
  simp only [regularDiagonal_value_expansion, Finsupp.sum]
  apply integrable_finset_sum
  intro h _
  exact ((hv h).smul_const (exponential h.val)).smul (regularCoefficients ψ h)

theorem regularDiagonal_integral (v : Spacetime → RegularLabel → ℂ)
    (hv : ∀ h, Integrable (fun x => v x h)) (ψ : regularFockDomain) :
    (regularDiagonal (fun h => ∫ x, v x h) ψ).val =
      ∫ x, (regularDiagonal (v x) ψ).val := by
  simp only [regularDiagonal_value_expansion, Finsupp.sum]
  rw [integral_finsetSum _ (fun h _ =>
    ((hv h).smul_const (exponential h.val)).smul (regularCoefficients ψ h))]
  simp only [integral_smul, integral_smul_const]

theorem scalarTest_profileWave_integrable (f : SchwartzTensor) (h : RegularLabel)
    (μ ν : Fin 4) :
    Integrable (fun x => (starRingEnd ℂ) (f x μ ν) * profileWave h.val μ ν x) := by
  have hi := (profileWave_pairing_integrable (componentTest f μ ν) h.val h.property.1 μ ν).
    integral_prod_left
  apply hi.congr
  apply ae_of_all
  intro x
  change (∫ y, (starRingEnd ℂ) (f x μ ν) * wavePhase x y *
    profileDensity h.val μ ν y ∂ChatgptAudit.WignerRapidityMeasure016.orbitalMeasure 0) = _
  unfold profileWave
  rw [← integral_const_mul]
  apply integral_congr_ae
  exact ae_of_all _ (fun y => by ring)

def pointTestEigenvalue (f : SchwartzTensor) (μ ν : Fin 4) (x : Spacetime)
    (h : RegularLabel) : ℂ :=
  ((starRingEnd ℂ) (f x μ ν) * metricSignC μ * metricSignC ν) *
    normalizedPointEigenvalue μ ν x h

theorem pointTestEigenvalue_eq (f : SchwartzTensor) (μ ν : Fin 4)
    (x : Spacetime) (h : RegularLabel) :
    pointTestEigenvalue f μ ν x h = (unitaryFourierFieldAmplitude : ℂ) *
      ((starRingEnd ℂ) (f x μ ν) * profileWave h.val μ ν x) := by
  unfold pointTestEigenvalue normalizedPointEigenvalue
  calc
    _ = (unitaryFourierFieldAmplitude : ℂ) * ((starRingEnd ℂ) (f x μ ν) *
        (metricSignC μ * metricSignC ν * lowerProfileWave h.val μ ν x)) := by ring
    _ = _ := by rw [raise_lowerProfileWave]

theorem pointTestEigenvalue_integrable (f : SchwartzTensor) (μ ν : Fin 4) (h : RegularLabel) :
    Integrable (fun x => pointTestEigenvalue f μ ν x h) := by
  simp only [pointTestEigenvalue_eq]
  exact (scalarTest_profileWave_integrable f h μ ν).const_mul _

theorem pointTest_diagonal (f : SchwartzTensor) (μ ν : Fin 4) (x : Spacetime)
    (ψ : regularFockDomain) :
    (regularDiagonal (pointTestEigenvalue f μ ν x) ψ).val =
      ((starRingEnd ℂ) (f x μ ν) * metricSignC μ * metricSignC ν) •
        (pointAnnihilation μ ν x ψ).val := by
  change (regularDiagonal
    (((starRingEnd ℂ) (f x μ ν) * metricSignC μ * metricSignC ν) •
      normalizedPointEigenvalue μ ν x) ψ).val = _
  rw [regularDiagonal_smul_eigenvalue]
  rfl

theorem pointAnnihilation_test_integrable (f : SchwartzTensor) (μ ν : Fin 4)
    (ψ : regularFockDomain) :
    Integrable (fun x => ((starRingEnd ℂ) (f x μ ν) * metricSignC μ * metricSignC ν) •
      (pointAnnihilation μ ν x ψ).val) := by
  simp only [← pointTest_diagonal]
  exact regularDiagonal_integrable (pointTestEigenvalue f μ ν)
    (pointTestEigenvalue_integrable f μ ν) ψ

theorem normalizedPointSmearEigenvalue_integrals (f : SchwartzTensor) :
    normalizedPointSmearEigenvalue f = (1/2 : ℂ) •
      ∑ μ : Fin 4, ∑ ν : Fin 4, (fun h : RegularLabel => ∫ x, pointTestEigenvalue f μ ν x h) := by
  funext h
  simp only [normalizedPointSmearEigenvalue, pointSmearEigenvalue, raise_lowerProfileWave,
    Pi.smul_apply, Finset.sum_apply, smul_eq_mul, pointTestEigenvalue_eq, integral_const_mul]
  simp only [← Finset.mul_sum]
  ring

/-- This is the literal normalized physical annihilation, recovered as a
Bochner integral of point annihilation on the same regular-domain state. -/
theorem normalizedPhysical_annihilation_point_integral
    (f : SchwartzTensor) (ψ : regularFockDomain) :
    annihilation (normalizedPhysicalSmearCLM f) (regularDomainInput ψ) =
      (1/2 : ℂ) • ∑ μ : Fin 4, ∑ ν : Fin 4,
        ∫ x, ((starRingEnd ℂ) (f x μ ν) * metricSignC μ * metricSignC ν) •
          (pointAnnihilation μ ν x ψ).val := by
  have he : annihilation (normalizedPhysicalSmearCLM f) (regularDomainInput ψ) =
      (regularEigenvalueLM ψ (normalizedPointSmearEigenvalue f)).val := by
    change _ = (regularDiagonal (normalizedPointSmearEigenvalue f) ψ).val
    simp only [normalizedPointSmearEigenvalue_eq_inner, regularDiagonal_annihilation]
  rw [he, normalizedPointSmearEigenvalue_integrals, map_smul, map_sum]
  simp only [map_sum, Submodule.coe_smul, Submodule.coe_sum]
  congr 1
  apply Finset.sum_congr rfl
  intro μ _
  apply Finset.sum_congr rfl
  intro ν _
  change (regularDiagonal (fun h => ∫ x, pointTestEigenvalue f μ ν x h) ψ).val = _
  rw [regularDiagonal_integral _ (pointTestEigenvalue_integrable f μ ν) ψ]
  simp only [pointTest_diagonal]

end F1Fecho.MaxwellGlobal
#print axioms F1Fecho.MaxwellGlobal.regularDiagonal_add_eigenvalue
#print axioms F1Fecho.MaxwellGlobal.regularDiagonal_smul_eigenvalue
#print axioms F1Fecho.MaxwellGlobal.regularDiagonal_value_expansion
#print axioms F1Fecho.MaxwellGlobal.regularDiagonal_integrable
#print axioms F1Fecho.MaxwellGlobal.regularDiagonal_integral
#print axioms F1Fecho.MaxwellGlobal.scalarTest_profileWave_integrable
#print axioms F1Fecho.MaxwellGlobal.pointTestEigenvalue_eq
#print axioms F1Fecho.MaxwellGlobal.pointTestEigenvalue_integrable
#print axioms F1Fecho.MaxwellGlobal.pointAnnihilation_test_integrable
#print axioms F1Fecho.MaxwellGlobal.normalizedPointSmearEigenvalue_integrals
#print axioms F1Fecho.MaxwellGlobal.normalizedPhysical_annihilation_point_integral
