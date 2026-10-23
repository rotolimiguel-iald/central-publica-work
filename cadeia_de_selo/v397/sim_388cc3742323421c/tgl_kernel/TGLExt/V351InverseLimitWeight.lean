import TGLExt.V351RegulatorWeightOrder
import Mathlib.Data.ENNReal.Operations
import Mathlib.Data.ENNReal.Inv

set_option autoImplicit false
set_option maxHeartbeats 1800000

namespace TGLV350.Regular
open TGLExt Filter
open scoped ENNReal NNReal Topology
noncomputable section

/-- Evaluate the original dual weight after conjugation by the existing root.
The regulator is mathematical; no new physical parameter is introduced. -/
def scalarInverseCutoffWeight (P : SiteProfile) (ε : ℝ) (X : PositiveCoreInput P) : ℝ≥0∞ :=
  dualQuadraticIntegral
    (star (hilbertPositiveSqrt (regularInverseGeneratorCutoff P ε)) * X.val *
      hilbertPositiveSqrt (regularInverseGeneratorCutoff P ε)) (regularVacuum P)

theorem scalarInverseCutoffWeight_zero (P : SiteProfile) (ε : ℝ) :
    scalarInverseCutoffWeight P ε (PositiveCoreInput.zero P) = 0 := by
  simp only [scalarInverseCutoffWeight,PositiveCoreInput.zero,mul_zero,zero_mul,
    dualQuadraticIntegral_zero]

theorem scalarInverseCutoffWeight_add (P : SiteProfile) (ε : ℝ)
    (X Y : PositiveCoreInput P) :
    scalarInverseCutoffWeight P ε (X.add Y) =
      scalarInverseCutoffWeight P ε X + scalarInverseCutoffWeight P ε Y := by
  simp only [scalarInverseCutoffWeight,PositiveCoreInput.add,mul_add,add_mul]
  exact dualQuadraticIntegral_add _ _
    (star_left_conjugate_nonneg X.property.2 _) (star_left_conjugate_nonneg Y.property.2 _) _

theorem scalarInverseCutoffWeight_scale (P : SiteProfile) (ε : ℝ)
    (r : ℝ≥0) (X : PositiveCoreInput P) :
    scalarInverseCutoffWeight P ε (X.scale r) =
      (r : ℝ≥0∞) * scalarInverseCutoffWeight P ε X := by
  simp only [scalarInverseCutoffWeight,PositiveCoreInput.scale,mul_smul_comm,smul_mul_assoc]
  simpa using dualQuadraticIntegral_smul_operator (r : ℝ) r.property _ (regularVacuum P)

theorem scalarInverseCutoffWeight_mono (P : SiteProfile) (ε : ℝ)
    (X Y : PositiveCoreInput P) (hXY : X ≤ Y) :
    scalarInverseCutoffWeight P ε X ≤ scalarInverseCutoffWeight P ε Y :=
  dualQuadraticIntegral_mono _ _
    (star_left_conjugate_le_conjugate (show X.val ≤ Y.val from hXY) _) _

/-- Normality is transported through actual strong limits. No invertibility
of the bounded conjugator or finite integral value is assumed. -/
theorem scalarInverseCutoffWeight_normal (P : SiteProfile) (ε : ℝ)
    {ι : Type*} [Preorder ι] [IsDirectedOrder ι] [Nonempty ι]
    (A : ι → (regularCoreAlgebra P).toStarSubalgebra)
    (S : (regularCoreAlgebra P).toStarSubalgebra)
    (hpos : ∀ i, 0 ≤ A i) (hmono : Monotone A) (hS : IsLUB (Set.range A) S) :
    scalarInverseCutoffWeight P ε
      ⟨S.val,S.property,positive_internal_isLUB_nonneg P A S hpos hS⟩ =
      ⨆ i, scalarInverseCutoffWeight P ε ⟨(A i).val,(A i).property,hpos i⟩ := by
  have hbnd (i : ι) : ‖(A i).val‖ ≤ ‖S.val‖ :=
    CStarAlgebra.norm_le_norm_of_nonneg_of_le (hpos i) (hS.1 (Set.mem_range_self i))
  obtain ⟨D,_,_,hlim,_,hD⟩ := vonNeumann_exists_positive_isLUB (regularCoreAlgebra P)
    A hpos hmono ‖S.val‖ (norm_nonneg _) hbnd
  have hDS : D = S := hD.unique hS
  subst D
  let b := hilbertPositiveSqrt (regularInverseGeneratorCutoff P ε)
  apply dualQuadraticIntegral_of_monotone_strong_limit
    (fun i => star b*(A i).val*b) (star b*S.val*b)
  · exact fun i => star_left_conjugate_nonneg (show 0 ≤ (A i).val from hpos i) b
  · exact fun i j hij => star_left_conjugate_le_conjugate
      (show (A i).val ≤ (A j).val from hmono hij) b
  · intro v
    exact ((star b).continuous.tendsto (S.val (b v))).comp (hlim (b v))

theorem scalarInverseCutoffWeight_antitone (P : SiteProfile)
    (ε η : ℝ) (hε : 0 < ε) (hη : 0 < η) (hεη : ε ≤ η) (X : PositiveCoreInput P) :
    scalarInverseCutoffWeight P η X ≤ scalarInverseCutoffWeight P ε X :=
  scalarWeight_inverseCutoff_antitone P ε η hε hη hεη X

theorem scalarInverseCutoffWeight_sequence_mono (P : SiteProfile) (X : PositiveCoreInput P) :
    Monotone (fun n : ℕ => scalarInverseCutoffWeight P (1/((n : ℝ)+1)) X) := by
  intro n m hnm
  apply scalarInverseCutoffWeight_antitone P
    (1/((m : ℝ)+1)) (1/((n : ℝ)+1)) (by positivity) (by positivity)
  apply one_div_le_one_div_of_le (by positivity : 0 < (n : ℝ)+1)
  have h : (n : ℝ) ≤ (m : ℝ) := by exact_mod_cast hnm
  linarith only [h]

/-- Candidate inverse-generator perturbation, as a monotone supremum of
the actual cutoff weights. This definition alone does not assert a trace. -/
def scalarInverseLimitWeight (P : SiteProfile) (X : PositiveCoreInput P) : ℝ≥0∞ :=
  ⨆ n : ℕ, scalarInverseCutoffWeight P (1/((n : ℝ)+1)) X

theorem scalarInverseLimitWeight_zero (P : SiteProfile) :
    scalarInverseLimitWeight P (PositiveCoreInput.zero P) = 0 := by
  simp only [scalarInverseLimitWeight,scalarInverseCutoffWeight_zero,ciSup_const]

theorem scalarInverseCutoffWeight_le_limit (P : SiteProfile) (n : ℕ) (X : PositiveCoreInput P) :
    scalarInverseCutoffWeight P (1/((n : ℝ)+1)) X ≤ scalarInverseLimitWeight P X :=
  le_iSup (fun m : ℕ => scalarInverseCutoffWeight P (1/((m : ℝ)+1)) X) n

theorem scalarInverseLimitWeight_add (P : SiteProfile) (X Y : PositiveCoreInput P) :
    scalarInverseLimitWeight P (X.add Y) = scalarInverseLimitWeight P X + scalarInverseLimitWeight P Y := by
  simp only [scalarInverseLimitWeight,scalarInverseCutoffWeight_add]
  exact (ENNReal.iSup_add_iSup_of_monotone (scalarInverseCutoffWeight_sequence_mono P X)
    (scalarInverseCutoffWeight_sequence_mono P Y)).symm

theorem scalarInverseLimitWeight_scale (P : SiteProfile) (r : ℝ≥0) (X : PositiveCoreInput P) :
    scalarInverseLimitWeight P (X.scale r) = (r : ℝ≥0∞) * scalarInverseLimitWeight P X := by
  simp only [scalarInverseLimitWeight,scalarInverseCutoffWeight_scale]
  exact (ENNReal.mul_iSup _ _).symm

theorem scalarInverseLimitWeight_mono (P : SiteProfile) (X Y : PositiveCoreInput P) (hXY : X ≤ Y) :
    scalarInverseLimitWeight P X ≤ scalarInverseLimitWeight P Y := by
  apply iSup_le
  intro n
  exact le_iSup_of_le n (scalarInverseCutoffWeight_mono P _ X Y hXY)

theorem scalarInverseLimitWeight_normal (P : SiteProfile)
    {ι : Type*} [Preorder ι] [IsDirectedOrder ι] [Nonempty ι]
    (A : ι → (regularCoreAlgebra P).toStarSubalgebra)
    (S : (regularCoreAlgebra P).toStarSubalgebra)
    (hpos : ∀ i, 0 ≤ A i) (hmono : Monotone A) (hS : IsLUB (Set.range A) S) :
    scalarInverseLimitWeight P
      ⟨S.val,S.property,positive_internal_isLUB_nonneg P A S hpos hS⟩ =
      ⨆ i, scalarInverseLimitWeight P ⟨(A i).val,(A i).property,hpos i⟩ := by
  simp only [scalarInverseLimitWeight,scalarInverseCutoffWeight_normal P _ A S hpos hmono hS]
  exact iSup_comm

end
end TGLV350.Regular
