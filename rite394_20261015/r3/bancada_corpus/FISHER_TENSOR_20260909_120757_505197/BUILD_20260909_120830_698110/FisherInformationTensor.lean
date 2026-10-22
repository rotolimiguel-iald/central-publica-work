import TGLExt.ScalarStressConservation
import TGLExt.MicroscopicClausiusBridge

set_option autoImplicit false
set_option maxHeartbeats 8000000
namespace ChatgptAudit.FisherField
open Matrix Filter Topology Set ChatgptAudit.Coherent023 ChatgptAudit.Micro021
open scoped ContDiff
noncomputable section
variable {ι : Type} [Fintype ι]

/-- Information tensor; no Lorentzian metric is asserted. -/
def fisherTensorAt (p : ι → ℝ) (dp : ι → Coordinate4) : Tensor4 :=
  ∑ i, (p i)⁻¹ • Matrix.vecMulVec (dp i) (dp i)

/-- Actual coordinate differential of the probability field. -/
def probabilityDifferential (P : Coordinate4 → ι → ℝ) (x : Coordinate4) (i : ι) : Coordinate4 :=
  potentialCovector (fun y => P y i) x

def directionalVariation (P : Coordinate4 → ι → ℝ) (x v : Coordinate4) : ι → ℝ :=
  fun i => covectorRead (probabilityDifferential P x i) v

def fisherTensorField (P : Coordinate4 → ι → ℝ) : TensorField4 :=
  fun x => fisherTensorAt (P x) (probabilityDifferential P x)

theorem fisher_tensor_entries (p : ι → ℝ) (dp : ι → Coordinate4) (a b : Fin 4) :
    fisherTensorAt p dp a b = ∑ i, dp i a * dp i b / p i := by
  simp only [fisherTensorAt, Matrix.sum_apply, Matrix.smul_apply, Matrix.vecMulVec,
    Matrix.of_apply, smul_eq_mul]
  apply Finset.sum_congr rfl
  intro i _
  ring

theorem fisher_tensor_symmetric (p : ι → ℝ) (dp : ι → Coordinate4) :
    (fisherTensorAt p dp)ᵀ = fisherTensorAt p dp := by
  simp only [fisherTensorAt, Matrix.transpose_sum, Matrix.transpose_smul, outer_tensor_symmetric]

theorem fisher_tensor_directional (p : ι → ℝ) (dp : ι → Coordinate4) (v : Coordinate4) :
    tensorQuad (fisherTensorAt p dp) v =
      diagonalFisher p (fun i => covectorRead (dp i) v) := by
  simp only [fisherTensorAt, tensorQuad, Matrix.sum_mulVec, dotProduct_sum,
    Matrix.smul_mulVec, dotProduct_smul, smul_eq_mul]
  change (∑ i, (p i)⁻¹ * tensorQuad (Matrix.vecMulVec (dp i) (dp i)) v) = _
  simp only [outer_tensor_quad, diagonalFisher]
  apply Finset.sum_congr rfl
  intro i _
  ring

theorem fisher_tensor_nonnegative (p : ι → ℝ) (dp : ι → Coordinate4)
    (hp : ∀ i, 0 < p i) (v : Coordinate4) :
    0 ≤ tensorQuad (fisherTensorAt p dp) v := by
  rw [fisher_tensor_directional]
  exact diagonal_fisher_nonneg _ _ hp

theorem fisher_tensor_null_iff (p : ι → ℝ) (dp : ι → Coordinate4)
    (hp : ∀ i, 0 < p i) (v : Coordinate4) :
    tensorQuad (fisherTensorAt p dp) v = 0 ↔
      (fun i => covectorRead (dp i) v) = 0 := by
  rw [fisher_tensor_directional]
  exact diagonal_fisher_zero_iff _ _ hp

theorem fisher_tensor_positive_iff (p : ι → ℝ) (dp : ι → Coordinate4)
    (hp : ∀ i, 0 < p i) (v : Coordinate4) :
    0 < tensorQuad (fisherTensorAt p dp) v ↔
      (fun i => covectorRead (dp i) v) ≠ 0 := by
  rw [fisher_tensor_directional]
  exact diagonal_fisher_pos_iff _ _ hp

theorem fisher_field_entries (P : Coordinate4 → ι → ℝ) (x : Coordinate4) (a b : Fin 4) :
    fisherTensorField P x a b =
      ∑ i, coordinatePartial (fun y => P y i) x a *
        coordinatePartial (fun y => P y i) x b / P x i :=
  fisher_tensor_entries _ _ a b

theorem fisher_field_symmetric (P : Coordinate4 → ι → ℝ) (x : Coordinate4) :
    (fisherTensorField P x)ᵀ = fisherTensorField P x :=
  fisher_tensor_symmetric _ _

theorem fisher_field_directional (P : Coordinate4 → ι → ℝ) (x v : Coordinate4) :
    tensorQuad (fisherTensorField P x) v =
      diagonalFisher (P x) (directionalVariation P x v) :=
  fisher_tensor_directional _ _ v

theorem fisher_field_nonnegative (P : Coordinate4 → ι → ℝ) (x : Coordinate4)
    (hp : ∀ i, 0 < P x i) (v : Coordinate4) :
    0 ≤ tensorQuad (fisherTensorField P x) v :=
  fisher_tensor_nonnegative _ _ hp v

theorem directional_variation_fderiv (P : Coordinate4 → ι → ℝ)
    (x v : Coordinate4) (i : ι) :
    directionalVariation P x v i = fderiv ℝ (fun y => P y i) x v := by
  rw [← scalarAlong_eq_fderiv (fun _ => v) (fun y => P y i) x]
  simp only [directionalVariation, probabilityDifferential, potentialCovector,
    covectorRead, dotProduct, scalarAlong]
  apply Finset.sum_congr rfl
  intro a _
  ring

theorem fisher_field_smooth (U : Set Coordinate4) (hU : IsOpen U)
    (P : Coordinate4 → ι → ℝ) (hP : ∀ i, ContDiffOn ℝ ∞ (fun x => P x i) U)
    (hp : ∀ x ∈ U, ∀ i, 0 < P x i) :
    SmoothMatrixOn U (fisherTensorField P) := by
  intro a b
  simp only [fisher_field_entries]
  apply ContDiffOn.sum
  intro i _
  exact ((coordinatePartial_smooth U hU _ (hP i) a).mul
    (coordinatePartial_smooth U hU _ (hP i) b)).div (hP i)
      (fun x hx => ne_of_gt (hp x hx i))

theorem probability_line_derivative (x v : Coordinate4) (t : ℝ) :
    HasDerivAt (fun s : ℝ => x + s • v) v t := by
  simpa using ((hasDerivAt_id t).smul_const v).const_add x

theorem probability_line_eventually (U : Set Coordinate4) (hU : IsOpen U)
    (x v : Coordinate4) (hx : x ∈ U) :
    ∀ᶠ t in 𝓝 (0 : ℝ), x + t • v ∈ U := by
  have hc := (probability_line_derivative x v 0).continuousAt
  exact hc.eventually (hU.mem_nhds (by simpa using hx))

theorem probability_weights_derivative (U : Set Coordinate4) (hU : IsOpen U)
    (P : Coordinate4 → ι → ℝ) (hP : ∀ i, ContDiffOn ℝ ∞ (fun x => P x i) U)
    (x v : Coordinate4) (t : ℝ) (ht : x + t • v ∈ U) (i : ι) :
    HasDerivAt (fun s => P (x + s • v) i) (directionalVariation P (x + t • v) v i) t := by
  rw [directional_variation_fderiv]
  exact ((hP i).differentiableOn (by simp)).differentiableAt
    (hU.mem_nhds ht) |>.hasFDerivAt.comp_hasDerivAt t (probability_line_derivative x v t)

theorem directional_variation_continuous (U : Set Coordinate4) (hU : IsOpen U)
    (P : Coordinate4 → ι → ℝ) (hP : ∀ i, ContDiffOn ℝ ∞ (fun x => P x i) U)
    (x v : Coordinate4) (hx : x ∈ U) (i : ι) :
    ContinuousAt (fun t : ℝ => directionalVariation P (x + t • v) v i) 0 := by
  have hd : ContDiffOn ℝ ∞ (fun y => directionalVariation P y v i) U := by
    simp only [directionalVariation, probabilityDifferential, potentialCovector,
      covectorRead, dotProduct]
    apply ContDiffOn.sum
    intro a _
    exact (coordinatePartial_smooth U hU _ (hP i) a).mul contDiffOn_const
  have hc := (hd.continuousOn.continuousAt (hU.mem_nhds hx)).comp
    (probability_line_derivative x v 0).continuousAt
  simpa using hc

/-- Affine spacetime sampling of P; no modular-flow identification. -/
def probabilityFieldCurve (U : Set Coordinate4) (hU : IsOpen U)
    (P : Coordinate4 → ι → ℝ) (hP : ∀ i, ContDiffOn ℝ ∞ (fun x => P x i) U)
    (htrace : ∀ y, ∑ i, P y i = 1) (x v : Coordinate4) (hx : x ∈ U) :
    DiagonalStateCurve (P x) where
  weights := fun t => P (x + t • v)
  tangent := fun t => directionalVariation P (x + t • v) v
  at_zero := by intro i; simp
  trace_one := fun t => htrace _
  derivative_zero := by
    intro i
    simpa using probability_weights_derivative U hU P hP x v 0 (by simpa using hx) i
  derivative_past := by
    filter_upwards [(probability_line_eventually U hU x v hx).filter_mono nhdsWithin_le_nhds]
      with t ht
    exact probability_weights_derivative U hU P hP x v t ht
  tangent_continuous := directional_variation_continuous U hU P hP x v hx

theorem probability_field_curve_tangent (U : Set Coordinate4) (hU : IsOpen U)
    (P : Coordinate4 → ι → ℝ) (hP : ∀ i, ContDiffOn ℝ ∞ (fun x => P x i) U)
    (htrace : ∀ y, ∑ i, P y i = 1) (x v : Coordinate4) (hx : x ∈ U) :
    (probabilityFieldCurve U hU P hP htrace x v hx).tangent 0 =
      directionalVariation P x v := by
  simp [probabilityFieldCurve]

theorem probability_field_curve_fisher (U : Set Coordinate4) (hU : IsOpen U)
    (P : Coordinate4 → ι → ℝ) (hP : ∀ i, ContDiffOn ℝ ∞ (fun x => P x i) U)
    (htrace : ∀ y, ∑ i, P y i = 1) (x v : Coordinate4) (hx : x ∈ U) :
    diagonalFisher (P x) ((probabilityFieldCurve U hU P hP htrace x v hx).tangent 0) =
      tensorQuad (fisherTensorField P x) v := by
  rw [probability_field_curve_tangent, fisher_field_directional]


#print axioms fisherTensorAt
#print axioms probabilityDifferential
#print axioms directionalVariation
#print axioms fisherTensorField
#print axioms fisher_tensor_entries
#print axioms fisher_tensor_symmetric
#print axioms fisher_tensor_directional
#print axioms fisher_tensor_nonnegative
#print axioms fisher_tensor_null_iff
#print axioms fisher_tensor_positive_iff
#print axioms fisher_field_entries
#print axioms fisher_field_symmetric
#print axioms fisher_field_directional
#print axioms fisher_field_nonnegative
#print axioms directional_variation_fderiv
#print axioms fisher_field_smooth
#print axioms probability_line_derivative
#print axioms probability_line_eventually
#print axioms probability_weights_derivative
#print axioms directional_variation_continuous
#print axioms probabilityFieldCurve
#print axioms probability_field_curve_tangent
#print axioms probability_field_curve_fisher
end
end ChatgptAudit.FisherField
