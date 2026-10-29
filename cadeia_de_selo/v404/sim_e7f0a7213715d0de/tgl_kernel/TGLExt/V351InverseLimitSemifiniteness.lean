import TGLExt.V351RegularDomainCut
import TGLExt.V351ScalarWeightSemifiniteness

set_option autoImplicit false
set_option maxHeartbeats 1800000

namespace TGLV350.Regular
open TGLExt Filter
open scoped ENNReal Topology
noncomputable section

private theorem hilbert_sqrt_mul_star {H : Type}
    [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (B : H →L[ℂ] H) (hB : 0 ≤ B) :
    hilbertPositiveSqrt B * star (hilbertPositiveSqrt B) = B := by
  change CFC.sqrt B * star (CFC.sqrt B) = B
  rw [(CFC.sqrt_nonneg B).isSelfAdjoint.star_eq,CFC.sqrt_mul_sqrt_self B hB]

/-- A finite-domain estimate uniform in the regulator defining the limit.
The original square-finite domain is used; a is never commuted with a cutoff. -/
theorem scalarInverseLimitWeight_domainCut_bound (P : SiteProfile) (δ : ℝ) (hδ : 0 < δ)
    (a : scalarWeightLeftIdeal P) :
    scalarInverseLimitWeight P (TGLV351.positiveSquare P (a.val * regularDomainCut P δ)) ≤
      ENNReal.ofReal (δ⁻¹) * dualQuadraticIntegral (star a.val.val*a.val.val) (regularVacuum P) := by
  let q := regularDomainCut P δ
  have hq := regularDomainCut_right P δ hδ
  have hqstar : star q.val = q.val := (regularDomainCut_bounds P δ hδ).1.isSelfAdjoint.star_eq
  let c : (regularCoreAlgebra P).toStarSubalgebra := (Real.sqrt (δ⁻¹) : ℂ) • 1
  have hc : c ∈ scalarPolarRightAlgebra P :=
    (scalarPolarRightAlgebra P).smul_mem (scalarPolarRightAlgebra P).one_mem _
  have hcoef : (Real.sqrt (δ⁻¹) : ℂ) * (Real.sqrt (δ⁻¹) : ℂ) = (δ⁻¹ : ℂ) := by
    exact_mod_cast Real.mul_self_sqrt (inv_nonneg.mpr hδ.le)
  have hcc : c.val * star c.val = (δ⁻¹ : ℂ) • 1 := by
    change ((Real.sqrt (δ⁻¹) : ℂ) • 1) * star ((Real.sqrt (δ⁻¹) : ℂ) • 1) = _
    simp only [star_smul,Complex.star_def,Complex.conj_ofReal,star_one,
      smul_mul_assoc,mul_smul_comm,smul_smul,hcoef,one_mul]
  unfold scalarInverseLimitWeight
  apply iSup_le
  intro n
  let ε : ℝ := 1/((n : ℝ)+1)
  have hε : 0 < ε := by dsimp [ε]; positivity
  obtain ⟨hs,hrs⟩ := regularInverseGeneratorCutoff_sqrt_right P ε hε
  let s : (regularCoreAlgebra P).toStarSubalgebra :=
    ⟨hilbertPositiveSqrt (regularInverseGeneratorCutoff P ε),hs⟩
  let b := q*s
  have hb : b ∈ scalarPolarRightAlgebra P := (scalarPolarRightAlgebra P).mul_mem hq hrs
  have hss : s.val * star s.val = regularInverseGeneratorCutoff P ε :=
    hilbert_sqrt_mul_star _ (regularInverseGeneratorCutoff_nonneg P ε hε)
  have hbc : b*star b ≤ c*star c := by
    change (q.val*s.val)*star (q.val*s.val) ≤ c.val*star c.val
    rw [hcc]
    calc
      _ = q.val*(s.val*star s.val)*q.val := by simp only [star_mul,hqstar,mul_assoc]
      _ = q.val*regularInverseGeneratorCutoff P ε*q.val := by rw [hss]
      _ = regularInverseGeneratorCutoff P ε*q.val*q.val := by
        rw [← (regularDomainCut_commutes P ε δ hε hδ).eq]
      _ ≤ _ := regularDomainCut_product_bound P ε δ hε hδ
  have hm := scalarWeight_right_perturbed_mono P b c hb hc hbc a
  calc
    scalarInverseCutoffWeight P ε (TGLV351.positiveSquare P (a.val*q)) =
        dualQuadraticIntegral (star b.val*(star a.val.val*a.val.val)*b.val) (regularVacuum P) := by
      have he : star s.val*(star (a.val.val*q.val)*(a.val.val*q.val))*s.val =
          star (q.val*s.val)*(star a.val.val*a.val.val)*(q.val*s.val) := by
        simp only [star_mul,mul_assoc]
      exact congrArg (fun T : RegularHilbert (TowerHilbert P) →L[ℂ]
        RegularHilbert (TowerHilbert P) => dualQuadraticIntegral T (regularVacuum P)) he
    _ ≤ dualQuadraticIntegral (star c.val*(star a.val.val*a.val.val)*c.val) (regularVacuum P) := hm
    _ = _ := by
      change dualQuadraticIntegral
        (star ((Real.sqrt (δ⁻¹) : ℂ) • 1) * (star a.val.val*a.val.val) *
          ((Real.sqrt (δ⁻¹) : ℂ) • 1)) (regularVacuum P) = _
      simp only [star_smul,Complex.star_def,Complex.conj_ofReal,star_one,
        smul_mul_assoc,mul_smul_comm,smul_smul,hcoef,one_mul,mul_one]
      rw [← Complex.ofReal_inv]
      exact dualQuadraticIntegral_smul_operator (δ⁻¹) (inv_nonneg.mpr hδ.le)
        (star a.val.val*a.val.val) (regularVacuum P)

theorem scalarInverseLimitWeight_domainCut_finite (P : SiteProfile) (δ : ℝ) (hδ : 0 < δ)
    (a : scalarWeightLeftIdeal P) :
    scalarInverseLimitWeight P (TGLV351.positiveSquare P (a.val * regularDomainCut P δ)) < ⊤ :=
  (scalarInverseLimitWeight_domainCut_bound P δ hδ a).trans_lt
    (ENNReal.mul_lt_top ENNReal.ofReal_lt_top a.property)

/-- Usual semifiniteness: square-finite operators are WOT dense in the SAME
core. This is not yet the finite-positive-minorant field of the trace contract. -/
theorem scalarInverseLimitWeight_square_finite_wot_closure (P : SiteProfile) :
    closure {A : RegularHilbert (TowerHilbert P) →WOT[ℂ] RegularHilbert (TowerHilbert P) |
      ∃ h : A.toCLM ∈ regularCoreAlgebra P,
        scalarInverseLimitWeight P (TGLV351.positiveSquare P ⟨A.toCLM,h⟩) < ⊤} =
    {A : RegularHilbert (TowerHilbert P) →WOT[ℂ] RegularHilbert (TowerHilbert P) |
      A.toCLM ∈ regularCoreAlgebra P} := by
  let F := {A : RegularHilbert (TowerHilbert P) →WOT[ℂ] RegularHilbert (TowerHilbert P) |
      ∃ h : A.toCLM ∈ regularCoreAlgebra P,
        scalarInverseLimitWeight P (TGLV351.positiveSquare P ⟨A.toCLM,h⟩) < ⊤}
  change closure F = _
  apply Set.Subset.antisymm
  · exact closure_minimal (fun A hA => hA.choose) (regularCore_wot_closed P)
  · have hinc : {A : RegularHilbert (TowerHilbert P) →WOT[ℂ] RegularHilbert (TowerHilbert P) |
        A.toCLM ∈ regularCoreAlgebra P ∧ HasFiniteScalarSquare P A.toCLM} ⊆ closure F := by
      intro A hA
      let a : scalarWeightLeftIdeal P := ⟨⟨A.toCLM,hA.1⟩,hA.2⟩
      have ht : ∀ v, Tendsto (fun n : ℕ =>
          (a.val.val*(regularDomainCut P (1/((n : ℝ)+1))).val) v) atTop (𝓝 (A.toCLM v)) := by
        intro v
        exact (a.val.val.continuous.tendsto v).comp (regularDomainCut_tendsto_identity P v)
      have hw := strong_tendsto_wot _ A.toCLM ht
      apply mem_closure_of_tendsto hw
      apply Filter.Eventually.of_forall
      intro n
      refine ⟨(regularCoreAlgebra P).mul_mem a.val.property
        (regularDomainCut P (1/((n : ℝ)+1))).property,?_⟩
      exact scalarInverseLimitWeight_domainCut_finite P (1/((n : ℝ)+1)) (by positivity) a
    have hh := closure_mono hinc
    rw [TGLV351.scalarWeight_square_finite_wot_closure,closure_closure] at hh
    exact hh

end
end TGLV350.Regular
