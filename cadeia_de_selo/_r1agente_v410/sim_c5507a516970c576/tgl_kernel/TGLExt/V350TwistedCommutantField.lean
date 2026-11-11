import TGLExt.V350OperatorFieldFaithfulness
import TGLExt.V350FixedCoreShiftCommutation

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 900000

namespace TGLV350.Regular
open MeasureTheory Filter TGLExt ChatgptAudit
noncomputable section

theorem modularConjugation_preserves_commutant (P : SiteProfile) (t : ℝ)
    (D : TowerHilbert P →L[ℂ] TowerHilbert P) (hD : D ∈ (theFactorObject P).commutant) :
    modularConjugation P t D ∈ (theFactorObject P).commutant := by
  rw [VonNeumannAlgebra.mem_commutant_iff] at hD ⊢
  intro A hA
  have hpre : (modularConjugation P t).symm A ∈ theFactorObject P :=
    (modularConjugation_preserves_factor P t _).mpr (by simpa using hA)
  have he := congrArg (modularConjugation P t) (hD _ hpre)
  simpa only [map_mul, StarAlgEquiv.apply_symm_apply] using he

theorem modularFlow_jointly_continuous (P : SiteProfile) :
    Continuous (fun p : TowerHilbert P × ℝ => modularFlow P p.2 p.1) :=
  continuous_prod_of_continuous_lipschitzWith _ 1
    (fun v => modularFlow_strongly_continuous v)
    (fun t => (modularFlowIsometry P t).lipschitz)

theorem modularConjugation_strongly_continuous (P : SiteProfile)
    (D : TowerHilbert P →L[ℂ] TowerHilbert P) (v : TowerHilbert P) :
    Continuous (fun x : ℝ => modularConjugation P x D v) := by
  have hn : Continuous (fun x : ℝ => modularFlow P (-x) v) :=
    (modularFlow_strongly_continuous v).comp continuous_neg
  have hd : Continuous (fun x : ℝ => D (modularFlow P (-x) v)) := D.continuous.comp hn
  have hp : Continuous (fun x : ℝ => (D (modularFlow P (-x) v), x)) :=
    hd.prodMk continuous_id
  have hc := (modularFlow_jointly_continuous P).comp hp
  simp only [Function.comp_def] at hc
  simpa only [modularConjugation_eq_sandwich, modularFlowCLM_star,
    mul_apply_eq_comp, modularFlowCLM_apply] using hc

/-- The continuous field x ↦ Δ^(ix) D Δ^(-ix), using the same tower flow.
Its bounded lift will lie in the regular commutant when D lies in M'. -/
def twistedCommutantField (P : SiteProfile)
    (D : TowerHilbert P →L[ℂ] TowerHilbert P) :
    StrongIntegral.Family (H := TowerHilbert P) where
  op := fun x => modularConjugation P x D
  continuous_apply := modularConjugation_strongly_continuous P D
  bound := ‖D‖
  bound_nonneg := norm_nonneg D
  norm_bound := fun x => le_of_eq (StarAlgEquiv.norm_map (modularConjugation P x) D)

theorem twistedCommutantField_zero (P : SiteProfile)
    (D : TowerHilbert P →L[ℂ] TowerHilbert P) : (twistedCommutantField P D).op 0 = D := by
  change modularConjugation P 0 D = D
  rw [modularConjugation_eq_sandwich, modularFlowCLM_zero]
  simp only [star_one, one_mul, mul_one]

theorem twistedCommutantField_intertwines (P : SiteProfile)
    (D : TowerHilbert P →L[ℂ] TowerHilbert P) (x t : ℝ) :
    (twistedCommutantField P D).op x * modularFlowCLM P t =
      modularFlowCLM P t * (twistedCommutantField P D).op (x-t) := by
  change modularConjugation P x D * modularFlowCLM P t =
    modularFlowCLM P t * modularConjugation P (x-t) D
  rw [modularConjugation_eq_sandwich, modularConjugation_eq_sandwich,
    modularFlowCLM_star, modularFlowCLM_star]
  calc
    _ = (modularFlowCLM P x * D) * (modularFlowCLM P (-x) * modularFlowCLM P t) := by
      simp only [mul_assoc]
    _ = (modularFlowCLM P x * D) * modularFlowCLM P (t-x) := by
      rw [modularFlowCLM_mul, neg_add_eq_sub]
    _ = ((modularFlowCLM P t * modularFlowCLM P (x-t)) * D) * modularFlowCLM P (-(x-t)) := by
      rw [modularFlowCLM_mul]
      congr 2 <;> congr 1 <;> ring
    _ = _ := by simp only [mul_assoc]

theorem operatorFieldLift_commutes_regular_of_intertwining (P : SiteProfile)
    (F : StrongIntegral.Family (H := TowerHilbert P))
    (hF : ∀ x t : ℝ, F.op x * modularFlowCLM P t = modularFlowCLM P t * F.op (x-t))
    (t : ℝ) :
    operatorFieldLift F * regularUnitary P t = regularUnitary P t * operatorFieldLift F := by
  ext1 f
  apply Lp.ext
  filter_upwards [operatorFieldLift_ae F (regularUnitary P t f),
    fibre_ae (modularFlowCLM P t) (shift t f), shift_ae t f,
    fibre_ae (modularFlowCLM P t) (shift t (operatorFieldLift F f)),
    shift_ae t (operatorFieldLift F f),
    (measurePreserving_sub_right volume t).quasiMeasurePreserving.ae (operatorFieldLift_ae F f)]
    with x h1 h2 h3 h4 h5 h6
  change operatorFieldLift F (regularUnitary P t f) x = regularUnitary P t (operatorFieldLift F f) x
  rw [h1]
  change F.op x (fibre (modularFlowCLM P t) (shift t f) x) =
    fibre (modularFlowCLM P t) (shift t (operatorFieldLift F f)) x
  rw [h2,h3,h4,h5,h6]
  exact congrArg (fun T : TowerHilbert P →L[ℂ] TowerHilbert P => T (f (x-t))) (hF x t)

#print axioms modularConjugation_preserves_commutant
#print axioms modularFlow_jointly_continuous
#print axioms modularConjugation_strongly_continuous
#print axioms twistedCommutantField
#print axioms twistedCommutantField_zero
#print axioms twistedCommutantField_intertwines
#print axioms operatorFieldLift_commutes_regular_of_intertwining
end
end TGLV350.Regular
