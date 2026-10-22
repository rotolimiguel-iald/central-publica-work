import MetricRicciVariation

set_option autoImplicit false
set_option maxHeartbeats 600000
namespace ChatgptAudit.MetricEinsteinVariation
open Matrix Filter Topology Set
  ChatgptAudit.MetricVariation ChatgptAudit.MetricRicci
  ChatgptAudit.CurvedConnection
noncomputable section
open scoped ContDiff

def scalarMetricVariation (g h : TensorField4) (x : Coordinate4) : ℝ :=
  ∑ i : Fin 4, ∑ j : Fin 4,
    (-(g x)⁻¹*h x*(g x)⁻¹) i j *
      coordinateRicci (leviCivitaField g (fun y => (g y)⁻¹)) x i j +
    (g x)⁻¹ i j * ricciVariation (leviCivitaField g (fun y => (g y)⁻¹))
      (metricConnectionVariation g h) x i j

def einsteinMetricVariation (g h : TensorField4) (x : Coordinate4) : Tensor4 :=
  ricciVariation (leviCivitaField g (fun y => (g y)⁻¹))
    (metricConnectionVariation g h) x -
  (scalarMetricVariation g h x / 2) • g x -
  (coordinateScalarCurvature (fun y => (g y)⁻¹)
    (leviCivitaField g (fun y => (g y)⁻¹)) x / 2) • h x

theorem metric_scalar_first_variation
    (U : Set Coordinate4) (hU : IsOpen U) (g h : TensorField4)
    (hg : SmoothMatrixOn U g) (hh : SmoothMatrixOn U h)
    (hi : ∀ x ∈ U, IsUnit (g x)) (x : Coordinate4) (hx : x ∈ U) :
    HasDerivAt (fun t => coordinateScalarCurvature
      (perturbedMetricInverse g h t) (perturbedLeviCivita g h t) x)
      (scalarMetricVariation g h x) 0 := by
  have hinv := matrix_inverse_first_variation (g x) (h x) (hi x hx)
  have hterm (i j : Fin 4) :=
    ((hasDerivAt_pi.mp (hasDerivAt_pi.mp hinv i)) j).mul
      (metric_ricci_first_variation U hU g h hg hh hi x hx i j)
  have hall := HasDerivAt.fun_sum fun i (_ : i ∈ (Finset.univ : Finset (Fin 4))) =>
    HasDerivAt.fun_sum fun j (_ : j ∈ (Finset.univ : Finset (Fin 4))) => hterm i j
  simpa only [coordinateScalarCurvature, perturbedMetricInverse, metricPerturbation,
    scalarMetricVariation, zero_smul, add_zero, perturbed_levi_civita_at_zero,
    neg_mul] using hall

theorem metric_einstein_first_variation_component
    (U : Set Coordinate4) (hU : IsOpen U) (g h : TensorField4)
    (hg : SmoothMatrixOn U g) (hh : SmoothMatrixOn U h)
    (hi : ∀ x ∈ U, IsUnit (g x)) (x : Coordinate4) (hx : x ∈ U) (i j : Fin 4) :
    HasDerivAt (fun t => geometricEinsteinTensor (metricPerturbation g h t)
      (perturbedMetricInverse g h t) (perturbedLeviCivita g h t) x i j)
      (einsteinMetricVariation g h x i j) 0 := by
  have hsc := (metric_scalar_first_variation U hU g h hg hh hi x hx).div_const 2
  have hmetric := (hasDerivAt_pi.mp
    (hasDerivAt_pi.mp (matrix_affine_derivative (g x) (h x)) i)) j
  have H := (metric_ricci_first_variation U hU g h hg hh hi x hx i j).sub
    (hsc.mul hmetric)
  convert! H using 1
  · rfl
  · simp only [einsteinMetricVariation, Matrix.sub_apply, Matrix.smul_apply,
      smul_eq_mul, coordinateScalarCurvature, perturbedMetricInverse, metricPerturbation,
      perturbed_levi_civita_at_zero, zero_smul, add_zero]
    ring

theorem metric_einstein_first_variation
    (U : Set Coordinate4) (hU : IsOpen U) (g h : TensorField4)
    (hg : SmoothMatrixOn U g) (hh : SmoothMatrixOn U h)
    (hi : ∀ x ∈ U, IsUnit (g x)) (x : Coordinate4) (hx : x ∈ U) :
    HasDerivAt (fun t => geometricEinsteinTensor (metricPerturbation g h t)
      (perturbedMetricInverse g h t) (perturbedLeviCivita g h t) x)
      (einsteinMetricVariation g h x) 0 := by
  apply hasDerivAt_pi.mpr
  intro i
  apply hasDerivAt_pi.mpr
  intro j
  exact metric_einstein_first_variation_component U hU g h hg hh hi x hx i j

#print axioms scalarMetricVariation
#print axioms einsteinMetricVariation
#print axioms metric_scalar_first_variation
#print axioms metric_einstein_first_variation_component
#print axioms metric_einstein_first_variation
end
end ChatgptAudit.MetricEinsteinVariation
