import TGLExt.GeometricEinsteinReconstruction

set_option autoImplicit false
set_option maxHeartbeats 2400000

namespace ChatgptAudit.GeneralMetric
open Matrix Filter Topology
open scoped ContDiff
noncomputable section

def metricTraceScalar (gInv A : TensorField4) (x : Coordinate4) : ℝ :=
  Matrix.trace (gInv x * A x) / 4

theorem metric_inverse_unique (g leftInv rightInv : Tensor4)
    (hl : leftInv * g = 1) (hr : g * rightInv = 1) :
    leftInv = rightInv := by
  calc
    leftInv = leftInv * (g * rightInv) := by rw [hr, mul_one]
    _ = (leftInv * g) * rightInv := (mul_assoc _ _ _).symm
    _ = rightInv := by rw [hl, one_mul]

theorem trace_recovers_metric_multiple (g gInv : Tensor4) (c : ℝ)
    (hl : gInv * g = 1) : Matrix.trace (gInv * (c • g)) / 4 = c := by
  rw [Matrix.mul_smul, hl, Matrix.trace_smul]
  norm_num

theorem null_tensor_eq_metric_trace (g gInv A : Tensor4)
    (hl : gInv * g = 1) (hg : LorentzByCongruence g) (hs : Aᵀ = A)
    (hn : ∀ v, tensorQuad g v = 0 → tensorQuad A v = 0) :
    A = (Matrix.trace (gInv * A) / 4) • g := by
  obtain ⟨c, hc⟩ := lorentz_tensor_null_rigidity A g hs hg hn
  rw [hc, trace_recovers_metric_multiple g gInv c hl]

theorem metric_trace_scalar_differentiable
    (U : Set Coordinate4) (gInv A : TensorField4)
    (hgi : ∀ i j, DifferentiableOn ℝ (fun x => gInv x i j) U)
    (hA : ∀ i j, DifferentiableOn ℝ (fun x => A x i j) U) :
    DifferentiableOn ℝ (metricTraceScalar gInv A) U := by
  unfold metricTraceScalar Matrix.trace
  simp only [Matrix.diag, Matrix.mul_apply]
  fun_prop

theorem metric_conserved_null_tensor
    (U : Set Coordinate4) (hU : IsOpen U) (hconn : IsPreconnected U)
    (g gInv A : TensorField4)
    (hgs : ∀ x∈U, (g x)ᵀ = g x)
    (hl : ∀ x∈U, gInv x * g x = 1) (hr : ∀ x∈U, g x * gInv x = 1)
    (hLor : ∀ x∈U, LorentzByCongruence (g x))
    (hg : ∀ i j, DifferentiableOn ℝ (fun x => g x i j) U)
    (hgi : ∀ i j, DifferentiableOn ℝ (fun x => gInv x i j) U)
    (hA : ∀ i j, DifferentiableOn ℝ (fun x => A x i j) U)
    (hs : ∀ x∈U, (A x)ᵀ = A x)
    (hn : ∀ x∈U, ∀ v, tensorQuad (g x) v = 0 → tensorQuad (A x) v = 0)
    (hd : ∀ x∈U, ∀ j,
      tensorFieldDivergence gInv (leviCivitaField g gInv) A x j = 0) :
    ∃ c : ℝ, ∀ x∈U, A x = c • g x := by
  have heq : Set.EqOn A (fun x => metricTraceScalar gInv A x • g x) U := by
    intro x hx
    exact null_tensor_eq_metric_trace (g x) (gInv x) (A x)
      (hl x hx) (hLor x hx) (hs x hx) (hn x hx)
  have hdiv : ∀ x∈U, ∀ j, tensorFieldDivergence gInv (leviCivitaField g gInv)
      (fun x => metricTraceScalar gInv A x • g x) x j = 0 := by
    intro x hx j
    rw [← tensorFieldDivergence_congr_on U hU gInv (leviCivitaField g gInv)
      A (fun x => metricTraceScalar gInv A x • g x) heq x hx]
    exact hd x hx j
  obtain ⟨c, hc⟩ := levi_civita_conserved_scalar_is_constant U hU hconn g gInv
    hgs hl hr (metricTraceScalar gInv A)
    (metric_trace_scalar_differentiable U gInv A hgi hA) hg hdiv
  refine ⟨c, ?_⟩
  intro x hx
  exact (heq hx).trans (congrArg (fun z : ℝ => z • g x) (hc x hx))

theorem metric_conserved_null_balance
    (U : Set Coordinate4) (hU : IsOpen U) (hconn : IsPreconnected U)
    (g gInv G T : TensorField4) (coupling : ℝ)
    (hgs : ∀ x∈U, (g x)ᵀ = g x)
    (hl : ∀ x∈U, gInv x * g x = 1) (hr : ∀ x∈U, g x * gInv x = 1)
    (hLor : ∀ x∈U, LorentzByCongruence (g x))
    (hg : ∀ i j, DifferentiableOn ℝ (fun x => g x i j) U)
    (hgi : ∀ i j, DifferentiableOn ℝ (fun x => gInv x i j) U)
    (hG : ∀ i j, DifferentiableOn ℝ (fun x => G x i j) U)
    (hT : ∀ i j, DifferentiableOn ℝ (fun x => T x i j) U)
    (hsG : ∀ x∈U, (G x)ᵀ = G x) (hsT : ∀ x∈U, (T x)ᵀ = T x)
    (hn : ∀ x∈U, ∀ v, tensorQuad (g x) v = 0 →
      tensorQuad (G x - coupling • T x) v = 0)
    (hdG : ∀ x∈U, ∀ j,
      tensorFieldDivergence gInv (leviCivitaField g gInv) G x j = 0)
    (hdT : ∀ x∈U, ∀ j,
      tensorFieldDivergence gInv (leviCivitaField g gInv) T x j = 0) :
    ∃ cosmological : ℝ, ∀ x∈U, G x + cosmological • g x = coupling • T x := by
  have hA : ∀ i j, DifferentiableOn ℝ (fun x => (G x - coupling • T x) i j) U := by
    intro i j
    exact (hG i j).sub ((hT i j).const_mul coupling)
  have hs : ∀ x∈U, (G x - coupling • T x)ᵀ = G x - coupling • T x := by
    intro x hx
    simp only [Matrix.transpose_sub, Matrix.transpose_smul, hsG x hx, hsT x hx]
  have hd : ∀ x∈U, ∀ j, tensorFieldDivergence gInv (leviCivitaField g gInv)
      (fun x => G x - coupling • T x) x j = 0 := by
    intro x hx j
    have hgAt : ∀ i k, DifferentiableAt ℝ (fun y => G y i k) x :=
      fun i k => (hG i k).differentiableAt (hU.mem_nhds hx)
    have htAt : ∀ i k, DifferentiableAt ℝ (fun y => T y i k) x :=
      fun i k => (hT i k).differentiableAt (hU.mem_nhds hx)
    rw [tensorFieldDivergence_sub _ _ G (fun y => coupling • T y) x hgAt
      (fun i k => (htAt i k).const_mul coupling) j,
      tensorFieldDivergence_const_smul _ _ coupling T x htAt j,
      hdG x hx j, hdT x hx j, mul_zero, sub_zero]
  obtain ⟨c, hc⟩ := metric_conserved_null_tensor U hU hconn g gInv
    (fun x => G x - coupling • T x) hgs hl hr hLor hg hgi hA hs hn hd
  refine ⟨-c, ?_⟩
  intro x hx
  rw [neg_smul, ← hc x hx]
  abel

theorem metric_einstein_equation_from_ricci_null_balance
    (U : Set Coordinate4) (hU : IsOpen U) (hconn : IsPreconnected U)
    (g gInv T : TensorField4) (coupling : ℝ)
    (hgs : ∀ x∈U, (g x)ᵀ = g x)
    (hl : ∀ x∈U, gInv x * g x = 1) (hr : ∀ x∈U, g x * gInv x = 1)
    (hLor : ∀ x∈U, LorentzByCongruence (g x))
    (hg : SmoothMatrixOn U g) (hgi : SmoothMatrixOn U gInv)
    (hT : ∀ i j, DifferentiableOn ℝ (fun x => T x i j) U)
    (hsT : ∀ x∈U, (T x)ᵀ = T x)
    (hn : ∀ x∈U, ∀ v, tensorQuad (g x) v = 0 →
      tensorQuad (coordinateRicci (leviCivitaField g gInv) x - coupling • T x) v = 0)
    (hdT : ∀ x∈U, ∀ j,
      tensorFieldDivergence gInv (leviCivitaField g gInv) T x j = 0) :
    ∃ cosmological : ℝ, ∀ x∈U,
      geometricEinsteinTensor g gInv (leviCivitaField g gInv) x +
      cosmological • g x = coupling • T x := by
  let Gamma := leviCivitaField g gInv
  let G := geometricEinsteinTensor g gInv Gamma
  have hGamma : SmoothConnectionOn U Gamma :=
    levi_civita_field_smooth U hU g gInv hg hgi
  have hm : MetricCompatibleOn U g Gamma :=
    levi_civita_field_metric_compatible U hU g gInv hgs hl hr
  have ht : ∀ x∈U, ∀ i j l, Gamma x i l j = Gamma x j l i :=
    levi_civita_field_torsion_free U hU g gInv hgs
  have hG : ∀ i j, DifferentiableOn ℝ (fun x => G x i j) U :=
    fun i j => (geometric_einstein_smooth U hU g gInv Gamma hg hgi hGamma i j).
      differentiableOn (by simp)
  have hsG : ∀ x∈U, (G x)ᵀ = G x :=
    fun x hx => geometric_einstein_symmetric U hU g gInv Gamma hg hGamma hm ht
      x hx (hgs x hx) (hl x hx)
  have hdG : ∀ x∈U, ∀ j, tensorFieldDivergence gInv Gamma G x j = 0 :=
    fun x hx j => geometric_einstein_conserved U hU g gInv Gamma hg hgi hGamma
      hm hgs ht hl hr x hx j
  have hnG : ∀ x∈U, ∀ v, tensorQuad (g x) v = 0 →
      tensorQuad (G x - coupling • T x) v = 0 := by
    intro x hx v hv
    have he : G x - coupling • T x =
        (coordinateRicci Gamma x - coupling • T x) -
        (coordinateScalarCurvature gInv Gamma x / 2) • g x := by
      change (coordinateRicci Gamma x -
        (coordinateScalarCurvature gInv Gamma x / 2) • g x) - coupling • T x = _
      abel
    rw [he, tensorQuad_sub_smul, hv, mul_zero, sub_zero]
    exact hn x hx v hv
  exact metric_conserved_null_balance U hU hconn g gInv G T coupling hgs hl hr hLor
    (fun i j => (hg i j).differentiableOn (by simp))
    (fun i j => (hgi i j).differentiableOn (by simp)) hG hT hsG hsT hnG hdG hdT

#print axioms metricTraceScalar
#print axioms metric_inverse_unique
#print axioms trace_recovers_metric_multiple
#print axioms null_tensor_eq_metric_trace
#print axioms metric_trace_scalar_differentiable
#print axioms metric_conserved_null_tensor
#print axioms metric_conserved_null_balance
#print axioms metric_einstein_equation_from_ricci_null_balance

end
end ChatgptAudit.GeneralMetric
