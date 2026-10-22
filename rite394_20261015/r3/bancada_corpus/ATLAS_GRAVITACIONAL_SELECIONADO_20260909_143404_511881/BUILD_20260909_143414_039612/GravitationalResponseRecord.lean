import ProbabilityRecordState
import GeneralSourceResponseReconstruction
import GeneralSourceEinsteinBridge

set_option autoImplicit false
set_option maxHeartbeats 600000
namespace ChatgptAudit.GravitationalRecord
open Matrix Filter Topology Set TGLExt
  ChatgptAudit.AngularTensorCodec ChatgptAudit.ProbabilityRecordState
  ChatgptAudit.GeneralMetric ChatgptAudit.GeneralClausius
  ChatgptAudit.SignedCoverage ChatgptAudit.FiniteResponseRecord
  ChatgptAudit.FullSourceResponse ChatgptAudit.GeneralSourceUnitary
  ChatgptAudit.GeneralSourceEinstein ChatgptAudit.JointUnitary ChatgptAudit.Micro021
open scoped ContDiff
noncomputable section

/-- The record stores probabilities and response coefficients, with explicit regularity.
It does not assert that a physical selection realizes these data. -/
structure GravitationalResponseRecord (U : Set Coordinate4) where
  metric : LorentzProbabilityRecord U
  responses : Coordinate4 → ResponseSamples
  smooth_responses : ∀ i, ContDiffOn ℝ ∞ (fun x => responses x i) U

def recordMetric {U : Set Coordinate4} (R : GravitationalResponseRecord U) : TensorField4 :=
  decodeRecord R.metric.data

def recordSource {U : Set Coordinate4} (R : GravitationalResponseRecord U) : TensorField4 :=
  fun x => decodeSource (recordMetric R x) (metricInverse (recordMetric R) x) (R.responses x)

def recordPreparation {U : Set Coordinate4} (R : GravitationalResponseRecord U)
    (x d : Coordinate4) : DiagonalStateCurve (jointBase calibrationLabelData) :=
  calibrationSourceCurve (recordMetric R) (recordSource R) x d

theorem record_metric_smooth {U : Set Coordinate4} (R : GravitationalResponseRecord U) :
    SmoothMatrixOn U (recordMetric R) :=
  decoded_record_smooth R.metric.data

theorem record_metric_lorentz {U : Set Coordinate4} (R : GravitationalResponseRecord U) :
    ∀ x ∈ U, LorentzByCongruence (recordMetric R x) :=
  R.metric.lorentz

theorem record_metric_symmetric {U : Set Coordinate4} (R : GravitationalResponseRecord U) :
    ∀ x ∈ U, (recordMetric R x)ᵀ=recordMetric R x :=
  fun x hx => lorentz_metric_symmetric _ (record_metric_lorentz R x hx)

theorem response_tensor_smooth {U : Set Coordinate4} (R : GravitationalResponseRecord U) :
    SmoothMatrixOn U (fun x => decodeResponse (normalizedSamples (R.responses x))) := by
  have hs (i : Fin 10) :
      ContDiffOn ℝ ∞ (fun x => normalizedSamples (R.responses x) i) U :=
    (R.smooth_responses i).div_const (-Real.pi)
  intro i j
  fin_cases i <;> fin_cases j
  · exact hs 0
  · exact (((hs 4).sub (hs 0)).sub (hs 1)).div_const 2
  · exact (((hs 5).sub (hs 0)).sub (hs 2)).div_const 2
  · exact (((hs 6).sub (hs 0)).sub (hs 3)).div_const 2
  · exact (((hs 4).sub (hs 0)).sub (hs 1)).div_const 2
  · exact hs 1
  · exact (((hs 7).sub (hs 1)).sub (hs 2)).div_const 2
  · exact (((hs 8).sub (hs 1)).sub (hs 3)).div_const 2
  · exact (((hs 5).sub (hs 0)).sub (hs 2)).div_const 2
  · exact (((hs 7).sub (hs 1)).sub (hs 2)).div_const 2
  · exact hs 2
  · exact (((hs 9).sub (hs 2)).sub (hs 3)).div_const 2
  · exact (((hs 6).sub (hs 0)).sub (hs 3)).div_const 2
  · exact (((hs 8).sub (hs 1)).sub (hs 3)).div_const 2
  · exact (((hs 9).sub (hs 2)).sub (hs 3)).div_const 2
  · exact hs 3

theorem record_source_smooth {U : Set Coordinate4} (R : GravitationalResponseRecord U) :
    SmoothMatrixOn U (recordSource R) :=
  trace_reverse_field_smooth U (recordMetric R) (metricInverse (recordMetric R))
    (fun x => decodeResponse (normalizedSamples (R.responses x)))
    (record_metric_smooth R)
    (constructed_metric_inverse_smooth U (recordMetric R)
      (record_metric_smooth R) (record_metric_lorentz R))
    (response_tensor_smooth R)

theorem record_source_symmetric {U : Set Coordinate4} (R : GravitationalResponseRecord U) :
    ∀ x ∈ U, (recordSource R x)ᵀ=recordSource R x := by
  intro x hx
  exact trace_reverse_symmetric _ _ _ (record_metric_symmetric R x hx)
    (decoded_response_symmetric _)

theorem record_metric_recovered_from_labelled_state {U : Set Coordinate4}
    (R : GravitationalResponseRecord U) :
    decodeTensorField (stateProbabilityField (recordState R.metric.data))=recordMetric R :=
  decode_record_from_state R.metric.data

theorem record_source_recovered_from_preparation {U : Set Coordinate4}
    (R : GravitationalResponseRecord U) (x : Coordinate4) (hx : x∈U) :
    decodeSource (recordMetric R x) (metricInverse (recordMetric R) x)
      (sampleResponse (calibrationSourceResponse (recordMetric R) (recordSource R) x)) =
        recordSource R x :=
  ten_responses_reconstruct_source_field (recordMetric R) (recordSource R) x
    (record_metric_lorentz R x hx) (record_source_symmetric R x hx)

theorem record_preparation_normalized {U : Set Coordinate4}
    (R : GravitationalResponseRecord U) (x d : Coordinate4) (t : ℝ) :
    ∑ k, (recordPreparation R x d).weights t k = 1 :=
  calibration_source_weights_normalized (recordMetric R) (recordSource R) x d t

theorem record_preparation_nonnegative {U : Set Coordinate4}
    (R : GravitationalResponseRecord U) (x d : Coordinate4) (t : ℝ) :
    ∀ k, 0 ≤ (recordPreparation R x d).weights t k :=
  calibration_source_weights_nonnegative (recordMetric R) (recordSource R) x d t

theorem record_preparation_entropy_null {U : Set Coordinate4}
    (R : GravitationalResponseRecord U) (x d : Coordinate4) (hx : x∈U)
    (hn : tensorQuad (recordMetric R x) d=0) :
    Tendsto (fun t => (finiteEntropy ((recordPreparation R x d).weights t) -
      finiteEntropy (jointBase calibrationLabelData))/t^2)
      (𝓝[<] (0 : ℝ)) (𝓝 (-Real.pi * tensorQuad (recordSource R x) d)) :=
  calibration_source_entropy_null_limit (recordMetric R) (recordSource R) x d
    (record_metric_lorentz R x hx) (record_source_symmetric R x hx) hn


/-- The preparation recovers exactly the ten response coefficients stored in this record. -/
theorem record_declared_responses_recovered {U : Set Coordinate4}
    (R : GravitationalResponseRecord U) (x : Coordinate4) (hx : x∈U) :
    sampleResponse (calibrationSourceResponse (recordMetric R) (recordSource R) x)=
      R.responses x := by
  change sampleResponse (calibratedPointResponse (recordMetric R x)
    (metricInverse (recordMetric R) x)
    (decodeSource (recordMetric R x) (metricInverse (recordMetric R) x) (R.responses x)))=_
  exact source_response_samples_roundtrip (recordMetric R x)
    (metricInverse (recordMetric R) x)
    (constructed_metric_inverse_left (recordMetric R) x (record_metric_lorentz R x hx))
    (record_metric_symmetric R x hx) (R.responses x)

/-- Conditional sufficiency: the area law, total conservation and screens are explicit inputs. -/
theorem record_einstein_from_area
    (U : Set Coordinate4) (hU : IsOpen U) (hconn : IsPreconnected U)
    (R : GravitationalResponseRecord U)
    (screens : MetricScreenFamily U (recordMetric R)) (eta : ℝ) (heta : eta ≠ 0)
    (hd : ∀ x ∈ U, ∀ j, tensorFieldDivergence (metricInverse (recordMetric R))
      (leviCivitaField (recordMetric R) (metricInverse (recordMetric R))) (recordSource R) x j=0)
    (harea : ∀ x (hx : x∈U) d (hv : d≠0) (hn : tensorQuad (recordMetric R x) d=0),
      Tendsto (fun t => microscopicAreaError (recordPreparation R x d) eta
        (inducedArea (recordMetric R) (screens x hx d hv hn).curve
          (screens x hx d hv hn).screen.vectors) t/t^2) (𝓝[<] 0) (𝓝 0)) :
    ∃ cosmological : ℝ, ∀ x∈U,
      geometricEinsteinTensor (recordMetric R) (metricInverse (recordMetric R))
        (leviCivitaField (recordMetric R) (metricInverse (recordMetric R))) x +
        cosmological • recordMetric R x = (2*Real.pi/eta) • recordSource R x :=
  general_source_einstein_from_area U hU hconn (recordMetric R) (recordSource R)
    (record_metric_smooth R) (record_source_smooth R)
    (record_metric_lorentz R) (record_source_symmetric R) screens eta heta hd harea

#print axioms GravitationalResponseRecord
#print axioms recordMetric
#print axioms recordSource
#print axioms recordPreparation
#print axioms record_metric_smooth
#print axioms record_metric_lorentz
#print axioms record_metric_symmetric
#print axioms response_tensor_smooth
#print axioms record_source_smooth
#print axioms record_source_symmetric
#print axioms record_metric_recovered_from_labelled_state
#print axioms record_source_recovered_from_preparation
#print axioms record_preparation_normalized
#print axioms record_preparation_nonnegative
#print axioms record_preparation_entropy_null
#print axioms record_declared_responses_recovered
#print axioms record_einstein_from_area
end
end ChatgptAudit.GravitationalRecord
