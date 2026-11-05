import TGLExt.V351ScalarRightActionLimits
import Mathlib.Analysis.CStarAlgebra.ContinuousFunctionalCalculus.Range

set_option autoImplicit false
set_option maxHeartbeats 2200000
set_option synthInstance.maxHeartbeats 200000

namespace TGLV350.Regular
open TGLExt Filter
open scoped Topology
noncomputable section

/-- The actual polar right identity on the existing full weight domain. -/
def ScalarPolarRight (P : SiteProfile) (b : (regularCoreAlgebra P).toStarSubalgebra) : Prop :=
  ∀ A : scalarWeightLeftIdeal P, ∃ h : A.val*b ∈ scalarWeightLeftIdeal P,
    scalarWeightGNSEmbedding P ⟨A.val*b,h⟩ =
      antiunitaryConjugate (scalarTomitaPolarFactor P)
        (scalarGNSRepresentation P (star b)) (scalarWeightGNSEmbedding P A)

theorem scalarPolarRight_iff_cuts (P : SiteProfile)
    (b : (regularCoreAlgebra P).toStarSubalgebra) :
    ScalarPolarRight P b ↔ ∀ A : scalarWeightLeftIdeal P, ∀ n : ℕ,
      scalarGNSCutMap P (n : ℝ)
        (antiunitaryConjugate (scalarTomitaPolarFactor P)
          (scalarGNSRepresentation P (star b)) (scalarWeightGNSEmbedding P A)) =
        dualOrbitRepresentation (A.val.val*b.val) (scalarCutVacuum P (n : ℝ)) := by
  constructor
  · intro hb A n
    obtain ⟨h,he⟩ := hb A
    rw [← he]
    exact scalarGNSCutMap_weight_embedding P (n : ℝ) ⟨A.val*b,h⟩
  · intro h A
    exact scalarWeightGNSEmbedding_of_cut_actions P (A.val*b) _ (h A)

theorem scalarPolarRight_zero (P : SiteProfile) : ScalarPolarRight P 0 := by
  intro A
  have h : A.val*0 ∈ scalarWeightLeftIdeal P := by simp
  refine ⟨h,?_⟩
  have he : (⟨A.val*0,h⟩ : scalarWeightLeftIdeal P) = 0 := Subtype.ext (mul_zero _)
  rw [he,map_zero,antiunitaryConjugate_apply,star_zero,map_zero]
  simp only [zero_apply,map_zero]

theorem scalarPolarRight_one (P : SiteProfile) : ScalarPolarRight P 1 := by
  intro A
  have h : A.val*1 ∈ scalarWeightLeftIdeal P := by simpa only [mul_one] using A.property
  refine ⟨h,?_⟩
  have he : (⟨A.val*1,h⟩ : scalarWeightLeftIdeal P) = A := Subtype.ext (mul_one _)
  rw [he,antiunitaryConjugate_apply,star_one,map_one]
  simp only [one_apply_eq_self,LinearIsometryEquiv.apply_symm_apply]

theorem scalarPolarRight_add (P : SiteProfile)
    (b c : (regularCoreAlgebra P).toStarSubalgebra)
    (hb : ScalarPolarRight P b) (hc : ScalarPolarRight P c) : ScalarPolarRight P (b+c) := by
  rw [scalarPolarRight_iff_cuts]
  intro A n
  have h1 := (scalarPolarRight_iff_cuts P b).mp hb A n
  have h2 := (scalarPolarRight_iff_cuts P c).mp hc A n
  have hs := congrArg₂ (fun x y => x+y) h1 h2
  have hbc : (b+c).val = b.val+c.val := rfl
  simpa only [antiunitaryConjugate_apply,star_add,map_add,
    hbc,mul_add,add_apply] using hs

theorem scalarPolarRight_smul (P : SiteProfile)
    (b : (regularCoreAlgebra P).toStarSubalgebra) (hb : ScalarPolarRight P b) (c : ℂ) :
    ScalarPolarRight P (c • b) := by
  intro A
  obtain ⟨hAb,heb⟩ := hb A
  have h : A.val*(c • b) ∈ scalarWeightLeftIdeal P := by
    simpa only [mul_smul_comm] using (scalarWeightLeftIdeal P).smul_mem c hAb
  refine ⟨h,?_⟩
  have he : (⟨A.val*(c • b),h⟩ : scalarWeightLeftIdeal P) =
      c • (⟨A.val*b,hAb⟩ : scalarWeightLeftIdeal P) := Subtype.ext (mul_smul_comm _ _ _)
  rw [he,map_smul,heb]
  simp only [antiunitaryConjugate_apply,star_smul,map_smul,
    smul_apply,LinearIsometryEquiv.map_smulₛₗ,starRingEnd_apply,star_star]

theorem scalarPolarRight_mul (P : SiteProfile)
    (b c : (regularCoreAlgebra P).toStarSubalgebra)
    (hb : ScalarPolarRight P b) (hc : ScalarPolarRight P c) : ScalarPolarRight P (b*c) := by
  intro A
  obtain ⟨hAb,heb⟩ := hb A
  obtain ⟨hAbc,hec⟩ := hc ⟨A.val*b,hAb⟩
  have h : A.val*(b*c) ∈ scalarWeightLeftIdeal P := by
    simpa only [mul_assoc] using hAbc
  refine ⟨h,?_⟩
  have he : (⟨A.val*(b*c),h⟩ : scalarWeightLeftIdeal P) =
      ⟨(A.val*b)*c,hAbc⟩ := Subtype.ext (mul_assoc _ _ _).symm
  rw [he,hec,heb]
  simp only [antiunitaryConjugate_apply,star_mul,map_mul,mul_apply_eq_comp,
    LinearIsometryEquiv.symm_apply_apply]

/-- The two-sided star condition is explicit; it is not silently inferred
from a right-boundedness condition on b alone. -/
def scalarPolarRightAlgebra (P : SiteProfile) :
    StarSubalgebra ℂ (regularCoreAlgebra P).toStarSubalgebra where
  carrier := {b | ScalarPolarRight P b ∧ ScalarPolarRight P (star b)}
  zero_mem' := by simpa only [Set.mem_setOf_eq,star_zero] using And.intro (scalarPolarRight_zero P) (scalarPolarRight_zero P)
  one_mem' := by simpa only [Set.mem_setOf_eq,star_one] using And.intro (scalarPolarRight_one P) (scalarPolarRight_one P)
  add_mem' := by
    intro b c hb hc
    exact ⟨scalarPolarRight_add P b c hb.1 hc.1,
      by simpa only [star_add] using scalarPolarRight_add P (star b) (star c) hb.2 hc.2⟩
  mul_mem' := by
    intro b c hb hc
    exact ⟨scalarPolarRight_mul P b c hb.1 hc.1,
      by simpa only [star_mul] using scalarPolarRight_mul P (star c) (star b) hc.2 hb.2⟩
  algebraMap_mem' c := by
    have h := scalarPolarRight_smul P 1 (scalarPolarRight_one P) c
    have hs := scalarPolarRight_smul P 1 (scalarPolarRight_one P) (star c)
    simpa only [Set.mem_setOf_eq,Algebra.algebraMap_eq_smul_one,star_smul,star_one] using And.intro h hs
  star_mem' := by
    intro b hb
    exact ⟨hb.2,by simpa only [star_star] using hb.1⟩

/-- Closedness uses bounded cut identities, not a false finite-minorant
characterization of the nontracial weight. -/
theorem scalarPolarRight_isClosed (P : SiteProfile) :
    IsClosed {b : (regularCoreAlgebra P).toStarSubalgebra | ScalarPolarRight P b} := by
  have hπ : Continuous (scalarGNSRepresentation P) := by
    have hb (b : (regularCoreAlgebra P).toStarSubalgebra) :
        ‖scalarGNSRepresentation P b‖ ≤ 1*‖b‖ := by
      rw [one_mul]
      apply ContinuousLinearMap.opNorm_le_bound _ (norm_nonneg b)
      intro v
      change ‖scalarGNSAmbientAction P b v.val‖ ≤ ‖b.val‖*‖v.val‖
      exact (ContinuousLinearMap.le_opNorm _ _).trans
        (mul_le_mul_of_nonneg_right (scalarGNSAmbientAction_norm_le P b) (norm_nonneg v.val))
    have hLip : LipschitzWith 1 (scalarGNSRepresentation P) := by
      apply LipschitzWith.of_dist_le_mul
      intro b c
      simpa only [dist_eq_norm, ← map_sub, NNReal.coe_one] using hb (b-c)
    exact hLip.continuous
  have hdual : Continuous (dualOrbitRepresentation (H := TowerHilbert P)) := by
    have hb (b : RegularHilbert (TowerHilbert P) →L[ℂ] RegularHilbert (TowerHilbert P)) :
        ‖dualOrbitRepresentation b‖ ≤ 1*‖b‖ := by
      rw [one_mul]
      change ‖operatorFieldLift (dualIntegralFamily b)‖ ≤ (dualIntegralFamily b).bound
      exact operatorFieldLift_norm_le (dualIntegralFamily b)
    exact ((dualOrbitRepresentation (H := TowerHilbert P)).toLinearMap.mkContinuous 1 hb).continuous
  have he : {b : (regularCoreAlgebra P).toStarSubalgebra | ScalarPolarRight P b} =
      ⋂ A : scalarWeightLeftIdeal P, ⋂ n : ℕ,
      {b | scalarGNSCutMap P (n : ℝ)
        (antiunitaryConjugate (scalarTomitaPolarFactor P)
          (scalarGNSRepresentation P (star b)) (scalarWeightGNSEmbedding P A)) =
        dualOrbitRepresentation (A.val.val*b.val) (scalarCutVacuum P (n : ℝ))} := by
    ext b
    simp only [Set.mem_setOf_eq,Set.mem_iInter,scalarPolarRight_iff_cuts]
  rw [he]
  apply isClosed_iInter
  intro A
  apply isClosed_iInter
  intro n
  apply isClosed_eq
  · simp only [antiunitaryConjugate_apply]
    exact (scalarGNSCutMap P (n : ℝ)).continuous.comp
      ((scalarTomitaPolarFactor P).continuous.comp
        ((hπ.comp continuous_star).clm_apply continuous_const))
  · exact (hdual.comp (continuous_const.mul continuous_subtype_val)).clm_apply continuous_const

theorem scalarPolarRightAlgebra_isClosed (P : SiteProfile) :
    IsClosed (scalarPolarRightAlgebra P : Set (regularCoreAlgebra P).toStarSubalgebra) :=
  (scalarPolarRight_isClosed P).inter ((scalarPolarRight_isClosed P).preimage continuous_star)

theorem scalarPolarRightAlgebra_regular_mem (P : SiteProfile) (t : ℝ) :
    regularRightCoreElement P t ∈ scalarPolarRightAlgebra P := by
  have h (s : ℝ) : ScalarPolarRight P (regularRightCoreElement P s) := by
    intro A
    exact ⟨(scalarRegularRightProduct P s A).property,scalarRightAction_regular P s A⟩
  exact ⟨h t,by simpa only [regularRightCoreElement_star] using h (-t)⟩

/-- Consume the ambient CFC, using a norm-closed image of the actual
right-identity algebra. No CFC or completeness of the core subtype is assumed. -/
theorem scalarRightAction_cfc (P : SiteProfile)
    (b : (regularCoreAlgebra P).toStarSubalgebra)
    (hb : b ∈ scalarPolarRightAlgebra P) (f : ℂ → ℂ) :
    ∃ hf : cfc f b.val ∈ regularCoreAlgebra P,
      (⟨cfc f b.val,hf⟩ : (regularCoreAlgebra P).toStarSubalgebra) ∈
        scalarPolarRightAlgebra P := by
  let E := (scalarPolarRightAlgebra P).map (regularCoreAlgebra P).toStarSubalgebra.subtype
  have hN : IsClosed (regularCoreAlgebra P : Set (RegularHilbert (TowerHilbert P) →L[ℂ]
      RegularHilbert (TowerHilbert P))) := by
    rw [← VonNeumannAlgebra.centralizer_centralizer (regularCoreAlgebra P)]
    exact Set.isClosed_centralizer _
  have hE : IsClosed (E : Set (RegularHilbert (TowerHilbert P) →L[ℂ]
      RegularHilbert (TowerHilbert P))) :=
    hN.isClosedMap_subtype_val _ (scalarPolarRightAlgebra_isClosed P)
  letI := hE
  have hbE : b.val ∈ E := ⟨b,hb,rfl⟩
  have hc : cfc f b.val ∈ E := cfc_mem (𝕜' := ℂ) f hbE
  obtain ⟨d,hd,he⟩ := hc
  have hm : cfc f b.val ∈ regularCoreAlgebra P := he ▸ d.property
  refine ⟨hm,?_⟩
  have heq : d = (⟨cfc f b.val,hm⟩ : (regularCoreAlgebra P).toStarSubalgebra) := Subtype.ext he
  exact heq ▸ hd

#print axioms ScalarPolarRight
#print axioms scalarPolarRight_iff_cuts
#print axioms scalarPolarRight_zero
#print axioms scalarPolarRight_one
#print axioms scalarPolarRight_add
#print axioms scalarPolarRight_smul
#print axioms scalarPolarRight_mul
#print axioms scalarPolarRightAlgebra
#print axioms scalarPolarRight_isClosed
#print axioms scalarPolarRightAlgebra_isClosed
#print axioms scalarPolarRightAlgebra_regular_mem
#print axioms scalarRightAction_cfc
end
end TGLV350.Regular
