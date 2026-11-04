import TGLExt.F1Fecho394.BoundedWeakAnalyticR6
import TGLExt.F1Fecho394.OrbitalContractionAnalyticR1
import TGLExt.F1Fecho394.BoundedGammaPropertiesR2
/-! Positive energy for the constructed second quantization on the SAME Fock.
The actual orbital contraction is lifted sectorwise. Coefficients on the
total exponential family are analytic; uniform norm bounds extend them to
every vector. No analyticity premise on Fock is assumed. -/
set_option autoImplicit false
set_option maxHeartbeats 1600000
noncomputable section
open Set Filter
open scoped InnerProductSpace Topology
namespace F1Fecho.CanonicalGammaPositive
open TGLExt.ImportedSQ TGLExt.ContratoQGv31 TGL.SpecificAQFT
open F1Rede.BosonicFock F1Fecho.Exponential F1Fecho.OrbitalContraction

def analyticGamma (a : Fin 4 → ℝ) (ha : a ∈ forwardCone) (z : ℂ) : F →L[ℂ] F :=
  BoundedGamma.gamma (V a ha z) (V_norm a ha z)

theorem analyticGamma_norm (a : Fin 4 → ℝ) (ha : a ∈ forwardCone) (z : ℂ) :
    ‖analyticGamma a ha z‖ ≤ 1 := BoundedGamma.gamma_norm_le _ _

theorem analyticGamma_exponential (a : Fin 4 → ℝ) (ha : a ∈ forwardCone)
    (z : ℂ) (f : H1) : analyticGamma a ha z (exponential f) = exponential (V a ha z f) :=
  BoundedGamma.gamma_exponential _ _ f

theorem analyticGamma_boundary (a : Fin 4 → ℝ) (ha : a ∈ forwardCone) (t : ℝ) :
    analyticGamma a ha t = (gamma (U1 (t • a))).toContinuousLinearEquiv.toContinuousLinearMap := by
  apply WeylConstruction.clm_ext_total exponential exponential_total
  intro f
  rw [analyticGamma_exponential,V_boundary]
  exact (gamma_exponential (U1 (t • a)) f).symm

theorem exponential_coefficient (a : Fin 4 → ℝ) (ha : a ∈ forwardCone) (f g : H1) :
    DiffContOnCl ℂ (fun z => inner ℂ (exponential f) (analyticGamma a ha z (exponential g))) upperHalf := by
  have he : (fun z => inner ℂ (exponential f) (analyticGamma a ha z (exponential g))) =
      (fun z => Complex.exp (inner ℂ f (V a ha z g))) := by
    funext z
    rw [analyticGamma_exponential,exponential_inner]
  rw [he]
  exact Complex.differentiable_exp.comp_diffContOnCl (coefficient_analytic a ha f g)

theorem coefficient (a : Fin 4 → ℝ) (ha : a ∈ forwardCone) (x y : F) :
    DiffContOnCl ℂ (fun z => inner ℂ x (analyticGamma a ha z y)) upperHalf := by
  apply BoundedWeakAnalytic.of_total exponential exponential_total (analyticGamma a ha) upperHalf
  · exact isOpen_lt continuous_const Complex.continuous_im
  · intro z _
    exact analyticGamma_norm a ha z
  · exact exponential_coefficient a ha

theorem positive_energy (a : Fin 4 → ℝ) (ha : a ∈ forwardCone) (ψ : F) :
    ∃ G : ℂ → ℂ, DiffContOnCl ℂ G upperHalf ∧
      (∃ M : ℝ, ∀ z : ℂ, 0 ≤ z.im → ‖G z‖ ≤ M) ∧
      (∀ t : ℝ, G t = inner ℂ ψ (gamma (U1 (t • a)) ψ)) := by
  refine ⟨fun z => inner ℂ ψ (analyticGamma a ha z ψ),coefficient a ha ψ ψ,?_,?_⟩
  · refine ⟨‖ψ‖^2,fun z _ => ?_⟩
    calc
      _ ≤ ‖ψ‖*‖analyticGamma a ha z ψ‖ := norm_inner_le_norm _ _
      _ ≤ ‖ψ‖*‖ψ‖ := mul_le_mul_of_nonneg_left
        (((analyticGamma a ha z).le_opNorm ψ).trans
          (by nlinarith [analyticGamma_norm a ha z,norm_nonneg ψ])) (norm_nonneg _)
      _ = _ := (pow_two _).symm
  · intro t
    change inner ℂ ψ (analyticGamma a ha (t:ℂ) ψ) = inner ℂ ψ (gamma (U1 (t • a)) ψ)
    rw [analyticGamma_boundary]
    rfl

/-- Direct inhabitant of the old Γ_positive field; its named one-particle
premise is unnecessary here because the actual orbital multiplier is used. -/
theorem gamma_positive : OneParticlePositiveEnergy →
    ∀ a ∈ forwardCone, ∀ ψ : F, ∃ G : ℂ → ℂ, DiffContOnCl ℂ G upperHalf ∧
      (∃ M : ℝ, ∀ z : ℂ, 0 ≤ z.im → ‖G z‖ ≤ M) ∧
      (∀ t : ℝ, G t = inner ℂ ψ (gamma (U1 (t • a)) ψ)) := by
  intro _ a ha ψ
  exact positive_energy a ha ψ

end F1Fecho.CanonicalGammaPositive
#print axioms F1Fecho.CanonicalGammaPositive.analyticGamma_boundary
#print axioms F1Fecho.CanonicalGammaPositive.exponential_coefficient
#print axioms F1Fecho.CanonicalGammaPositive.coefficient
#print axioms F1Fecho.CanonicalGammaPositive.positive_energy
#print axioms F1Fecho.CanonicalGammaPositive.gamma_positive
