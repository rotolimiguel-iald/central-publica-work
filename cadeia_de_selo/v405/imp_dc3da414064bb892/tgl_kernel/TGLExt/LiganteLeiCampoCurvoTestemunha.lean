import TGLExt.LiganteLeiCampoCurvo
import TGLExt.ConstructedClausiusControls
import TGLExt.EquilibriumScreenIntegration
import TGLExt.PoincareGroup

set_option autoImplicit false
set_option maxHeartbeats 1200000


/-! ===================== AUDITORIA F2.3 — S7/S8 (cetico c1, 08/10/2026) =====================
S7: testemunha plana (Minkowski, fonte nula, uma carta, X = Coordinate4): as hipoteses da
    F2.3 sao CONJUNTAMENTE satisfaziveis, para todo G > 0.
S8: contramodelo: mesma geometria plana, fonte CONSTANTE com T(k,k) = 1 numa direcao nula:
    todas as hipoteses da F2.3 menos hH3 valem; H3 falha; e a conclusao falha.
    Logo hH3 e carga real (nao e redundante).
NADA disto e pedra; vive so no sandbox do auditor. -/

namespace AuditF23Flat
open Matrix Filter Topology Set TGLExt ChatgptAudit
open ChatgptAudit.GeneralMetric ChatgptAudit.GeneralClausius
open ChatgptAudit.GravitationalRecord ChatgptAudit.ChartGluing
open ChatgptAudit.TopologicalGluing ChatgptAudit.SmoothAtlasGluing
open ChatgptAudit.UnifiedRecorded ChatgptAudit.Micro021
open ChatgptAudit.F23CurvedFieldLigand
open ChatgptAudit.Flow019 ChatgptAudit.Flow020
open ChatgptAudit.AngularTensorCodec ChatgptAudit.FiniteCoordinates
open ChatgptAudit.FiniteResponseRecord ChatgptAudit.FullSourceResponse ChatgptAudit.SignedCoverage

noncomputable section

/-- S5 (copia local): o H3 nomeado equivale ao balanco nulo de Ricci. -/
theorem s5_local {ι : Type} (eta : ℝ)
    (U : ι → Set Coordinate4) (hopenU : ∀ i, IsOpen (U i))
    (R : ∀ i, GravitationalResponseRecord (U i))
    (screens : ∀ i, MetricScreenFamily (U i) (recordMetric (R i))) :
    NamedAtlasH3 eta U R screens ↔
      ∀ i x (hx : x ∈ U i) d (hv : d ≠ 0) (hn : tensorQuad (recordMetric (R i) x) d = 0),
        eta * tensorQuad (coordinateRicci (leviCivitaField (recordMetric (R i))
          (metricInverse (recordMetric (R i)))) x) d =
        2 * Real.pi * tensorQuad (recordSource (R i) x) d := by
  unfold NamedAtlasH3
  apply forall_congr'; intro i
  apply forall_congr'; intro x
  apply forall_congr'; intro hx
  apply forall_congr'; intro d
  apply forall_congr'; intro hv
  apply forall_congr'; intro hn
  rw [unified_area_matching_iff (R i) x d eta _]
  have hLor := record_metric_lorentz (R i)
  have hg := record_metric_smooth (R i)
  have hgi := constructed_metric_inverse_smooth (U i) (recordMetric (R i)) hg hLor
  have hGc := levi_civita_field_smooth (U i) (hopenU i) _ _ hg hgi
  have ht := levi_civita_field_torsion_free (U i) (hopenU i) (recordMetric (R i))
    (metricInverse (recordMetric (R i))) (record_metric_symmetric (R i)) x hx
  exact ChatgptAudit.GeneralSourceEinstein.general_source_area_matching_iff_ricci
    (screens i x hx d hv hn) (recordSource (R i)) eta (hopenU i) hg hGc ht (hLor x hx)
    (record_source_symmetric (R i) x hx) hn

theorem flat_metric_lorentz :
    ∀ x ∈ (univ : Set Coordinate4), LorentzByCongruence (frameMetricField flatSolder x) :=
  fun _ _ => ⟨1, by simp, rfl⟩

def flatMetricRecord : LorentzProbabilityRecord (univ : Set Coordinate4) :=
  encodeLorentzRecord univ (frameMetricField flatSolder)
    (frame_metric_smooth univ flatSolder flat_solder_smooth) flat_metric_lorentz

/-- registro plano com amostras de resposta CONSTANTES `s` -/
def flatRecordS (s : ResponseSamples) : GravitationalResponseRecord (univ : Set Coordinate4) where
  metric := flatMetricRecord
  responses := fun _ => s
  smooth_responses := fun _ => contDiffOn_const

theorem flat_record_metric (s : ResponseSamples) :
    recordMetric (flatRecordS s) = frameMetricField flatSolder :=
  decode_encoded_record univ (frameMetricField flatSolder)
    (frame_metric_smooth univ flatSolder flat_solder_smooth)

theorem eta4_inv_self : eta4⁻¹ = eta4 :=
  Matrix.inv_eq_left_inv eta4_mul_self

theorem flat_metric_inverse :
    metricInverse (frameMetricField flatSolder) = inverseFrameMetricField flatSolder := by
  funext x
  simp only [metricInverse, frameMetricField, inverseFrameMetricField, flatSolder,
    Matrix.transpose_one, Matrix.one_mul, Matrix.mul_one]
  exact eta4_inv_self

theorem flat_record_connection (s : ResponseSamples) :
    leviCivitaField (recordMetric (flatRecordS s)) (metricInverse (recordMetric (flatRecordS s)))
      = frameLeviCivita flatSolder flatSolder := by
  rw [flat_record_metric, flat_metric_inverse]
  rfl

theorem flat_ricci_rec (s : ResponseSamples) (x : Coordinate4) :
    coordinateRicci (leviCivitaField (recordMetric (flatRecordS s))
      (metricInverse (recordMetric (flatRecordS s)))) x = 0 := by
  rw [flat_record_connection]
  exact flat_ricci_zero x

def flatScreensS (s : ResponseSamples) :
    MetricScreenFamily (univ : Set Coordinate4) (recordMetric (flatRecordS s)) := by
  rw [flat_record_metric]
  intro p hp v hv hn
  rw [flat_metric_inverse]
  exact localEquilibriumScreen univ isOpen_univ flatSolder flatSolder flat_solder_inverse
    flat_solder_inverse flat_solder_smooth flat_solder_smooth p v hp hv hn

theorem flat_record_source (s : ResponseSamples) :
    recordSource (flatRecordS s) = fun _ =>
      traceReverse (frameMetricField flatSolder 0) (inverseFrameMetricField flatSolder 0)
        (decodeResponse (normalizedSamples s)) := by
  funext x
  show decodeSource (recordMetric (flatRecordS s) x)
    (metricInverse (recordMetric (flatRecordS s)) x) s = _
  rw [flat_record_metric, flat_metric_inverse]
  rfl

theorem flat_conserved (s : ResponseSamples) : ∀ x ∈ (univ : Set Coordinate4), ∀ j,
    tensorFieldDivergence (metricInverse (recordMetric (flatRecordS s)))
      (leviCivitaField (recordMetric (flatRecordS s)) (metricInverse (recordMetric (flatRecordS s))))
      (recordSource (flatRecordS s)) x j = 0 := by
  intro x _ j
  rw [flat_record_connection, flat_connection_zero, flat_record_source]
  simp [tensorFieldDivergence, tensorJetDivergence, covariantTensorJet, tensorFieldJet,
    coordinatePartial]

def flatChart : (univ : Set Coordinate4) ≃ₜ (univ : Set Coordinate4) :=
  (Homeomorph.Set.univ Coordinate4).trans (Homeomorph.Set.univ Coordinate4).symm

def idChange : SmoothCoordinateChange (univ : Set Coordinate4) (univ : Set Coordinate4) where
  forward := fun y => y
  inverse := fun y => y
  source_open := isOpen_univ
  target_open := isOpen_univ
  forward_maps := fun _ _ => mem_univ _
  inverse_maps := fun _ _ => mem_univ _
  left_inverse := fun _ _ => rfl
  right_inverse := fun _ _ => rfl
  forward_smooth := fun a => (contDiff_apply ℝ ℝ a).contDiffOn
  inverse_smooth := fun a => (contDiff_apply ℝ ℝ a).contDiffOn

def flatTransition (s : ResponseSamples) :
    SmoothRecordTransition (fun _ : Unit => (univ : Set Coordinate4)) (fun _ => flatRecordS s)
      (fun _ : Unit => (univ : Set Coordinate4)) (fun _ => flatChart) () () where
  source := univ
  target := univ
  change := idChange
  source_subset := subset_refl _
  target_subset := subset_refl _
  same_point := by intro x hx; rfl
  metric := by
    intro x _
    show recordMetric (flatRecordS s) x =
      (changeJacobian idChange x)ᵀ * recordMetric (flatRecordS s) x * changeJacobian idChange x
    rw [show changeJacobian idChange x = 1 from coordinate_jacobian_identity x]
    simp
  matter := by
    intro x _
    show recordSource (flatRecordS s) x =
      (changeJacobian idChange x)ᵀ * recordSource (flatRecordS s) x * changeJacobian idChange x
    rw [show changeJacobian idChange x = 1 from coordinate_jacobian_identity x]
    simp

theorem flat_transitions (s : ResponseSamples) :
    ∀ i j p (_hi : p ∈ (fun _ : Unit => (univ : Set Coordinate4)) i)
      (hj : p ∈ (fun _ : Unit => (univ : Set Coordinate4)) j),
      ∃ D : SmoothRecordTransition (fun _ : Unit => (univ : Set Coordinate4))
        (fun _ => flatRecordS s) (fun _ : Unit => (univ : Set Coordinate4))
        (fun _ => flatChart) i j,
        ((fun _ : Unit => flatChart) j ⟨p, hj⟩).val ∈ D.source := by
  rintro ⟨⟩ ⟨⟩ p _ hj
  exact ⟨flatTransition s, mem_univ _⟩

/-- vacuo: amostras nulas dao fonte nula -/
theorem vacuum_source (x : Coordinate4) : recordSource (flatRecordS 0) x = 0 := by
  rw [flat_record_source]
  have h0 : decodeResponse (normalizedSamples (0 : ResponseSamples)) = 0 := by
    ext a b
    fin_cases a <;> fin_cases b <;> simp [decodeResponse, normalizedSamples]
  simp [h0, traceReverse]

theorem vacuum_h3 (eta : ℝ) :
    NamedAtlasH3 eta (fun _ : Unit => (univ : Set Coordinate4)) (fun _ => flatRecordS 0)
      (fun _ => flatScreensS 0) := by
  rw [s5_local eta (fun _ : Unit => (univ : Set Coordinate4)) (fun _ => isOpen_univ)]
  intro i x hx d hv hn
  try dsimp only
  rw [flat_ricci_rec, vacuum_source]
  simp [tensorQuad]

/-- S7: TESTEMUNHA — as hipoteses da F2.3 sao conjuntamente satisfaziveis (vacuo plano). -/
theorem s7_f23_hypotheses_jointly_satisfiable (G : ℝ) (hG : 0 < G) :
    ∃! a : ℝ, ∀ i x, x ∈ (fun _ : Unit => (univ : Set Coordinate4)) i →
      recordEinstein ((fun _ : Unit => flatRecordS 0) i) x +
        a • recordMetric ((fun _ : Unit => flatRecordS 0) i) x =
        (8 * Real.pi * G) • recordSource ((fun _ : Unit => flatRecordS 0) i) x :=
  passage_h3_to_connected_smooth_atlas_einstein (X := Coordinate4) (ι := Unit)
    (n := Fin 1) (d := fun _ => (1:ℝ))
    (fun _ => one_pos) (fun a b _ => Subsingleton.elim a b) (W := 1) (by simp)
    (fun y => by simp [adU]) G hG (fun _ => (univ : Set Coordinate4)) (fun _ => isOpen_univ)
    (fun _ => isPreconnected_univ) (fun _ => flatRecordS 0) (fun _ => flatScreensS 0)
    (fun _ => flat_conserved 0) (fun _ => vacuum_h3 _)
    () (fun _ => (univ : Set Coordinate4)) (fun _ => isOpen_univ)
    (fun x => ⟨(), mem_univ x⟩) (fun _ => univ_nonempty) (fun _ => flatChart) (flat_transitions 0)

/-- amostras que decodificam no tensor de tempo puro diag(1,0,0,0) -/
def sP : ResponseSamples := fun i => if i = 0 ∨ i = 4 ∨ i = 5 ∨ i = 6 then -Real.pi else 0

theorem sP_decoded : decodeResponse (normalizedSamples sP) = pureTimeTensor := by
  ext a b
  fin_cases a <;> fin_cases b <;> simp [decodeResponse, normalizedSamples, sP, pureTimeTensor]

theorem tq_add (A B : Tensor4) (k : Coordinate4) :
    tensorQuad (A + B) k = tensorQuad A k + tensorQuad B k := by
  simp [tensorQuad, Matrix.add_mulVec, dotProduct_add]

theorem tq_smul (c : ℝ) (A : Tensor4) (k : Coordinate4) :
    tensorQuad (c • A) k = c * tensorQuad A k := by
  simp [tensorQuad, Matrix.smul_mulVec, dotProduct_smul]

theorem hcd_ne : horizonControlDirection ≠ 0 := by
  intro h
  have := congrFun h 0
  simp [horizonControlDirection] at this

theorem flat_g0 : frameMetricField flatSolder 0 = eta4 := by
  simp [frameMetricField, flatSolder]

theorem flat_gi0 : inverseFrameMetricField flatSolder 0 = eta4 := by
  simp [inverseFrameMetricField, flatSolder]

theorem trace_eta4_pure : Matrix.trace (eta4 * pureTimeTensor) = 1 := by
  have h : eta4 * pureTimeTensor = pureTimeTensor := by
    ext a b
    fin_cases a <;> fin_cases b <;>
      simp [eta4, pureTimeTensor, Matrix.diagonal_mul]
  rw [h]
  simp [Matrix.trace, pureTimeTensor, Fin.sum_univ_four]

theorem tq_eta4_hcd : tensorQuad eta4 horizonControlDirection = 0 := by
  rw [← flat_g0]
  exact flat_control_null

theorem tq_pure_hcd : tensorQuad pureTimeTensor horizonControlDirection = 1 := by
  simp [tensorQuad, pureTimeTensor, horizonControlDirection, Matrix.mulVec, dotProduct,
    Fin.sum_univ_four]

theorem sP_null_value :
    tensorQuad (recordSource (flatRecordS sP) 0) horizonControlDirection = 1 := by
  rw [flat_record_source]
  try dsimp only
  rw [sP_decoded, flat_g0, flat_gi0]
  unfold traceReverse
  rw [tensorQuad_sub_smul, tq_pure_hcd, tq_eta4_hcd, trace_eta4_pure]
  norm_num

theorem flat_einstein_zero (s : ResponseSamples) (x : Coordinate4) :
    recordEinstein (flatRecordS s) x = 0 := by
  unfold recordEinstein geometricEinsteinTensor
  rw [flat_record_connection]
  simp [coordinateScalarCurvature, flat_ricci_zero]

/-- S8: CONTRAMODELO — todas as hipoteses menos hH3 valem (conservacao abaixo; atlas, cartas,
    transicoes e telas sao as de S7 com o mesmo `flatRecordS`), H3 falha e a conclusao falha. -/
theorem s8_h3_is_load_bearing (G : ℝ) (hG : 0 < G) :
    (∀ x ∈ (univ : Set Coordinate4), ∀ j,
      tensorFieldDivergence (metricInverse (recordMetric (flatRecordS sP)))
        (leviCivitaField (recordMetric (flatRecordS sP))
          (metricInverse (recordMetric (flatRecordS sP))))
        (recordSource (flatRecordS sP)) x j = 0) ∧
    ¬ NamedAtlasH3 ((4 * G)⁻¹) (fun _ : Unit => (univ : Set Coordinate4))
        (fun _ => flatRecordS sP) (fun _ => flatScreensS sP) ∧
    ¬ (∃! a : ℝ, ∀ i x, x ∈ (fun _ : Unit => (univ : Set Coordinate4)) i →
        recordEinstein ((fun _ : Unit => flatRecordS sP) i) x +
          a • recordMetric ((fun _ : Unit => flatRecordS sP) i) x =
          (8 * Real.pi * G) • recordSource ((fun _ : Unit => flatRecordS sP) i) x) := by
  refine ⟨flat_conserved sP, ?_, ?_⟩
  · intro h
    have hb := (s5_local ((4 * G)⁻¹) (fun _ : Unit => (univ : Set Coordinate4))
      (fun _ => isOpen_univ) _ _).mp h () 0 (mem_univ _) horizonControlDirection hcd_ne
      (by try dsimp only
          rw [flat_record_metric]; exact flat_control_null)
    try dsimp only at hb
    rw [flat_ricci_rec, sP_null_value] at hb
    simp [tensorQuad] at hb
  · rintro ⟨a, ha, _⟩
    have h := ha () 0 (mem_univ _)
    try dsimp only at h
    have hq := congrArg (fun A : Tensor4 => tensorQuad A horizonControlDirection) h
    try dsimp only at hq
    rw [tq_add, tq_smul, tq_smul, flat_einstein_zero, flat_record_metric, flat_control_null,
      sP_null_value] at hq
    simp [tensorQuad] at hq
    have hpos : 0 < 8 * Real.pi * G := by positivity
    linarith

#print axioms s5_local
#print axioms flatScreensS
#print axioms vacuum_h3
#print axioms s7_f23_hypotheses_jointly_satisfiable
#print axioms sP_decoded
#print axioms s8_h3_is_load_bearing

end
end AuditF23Flat
