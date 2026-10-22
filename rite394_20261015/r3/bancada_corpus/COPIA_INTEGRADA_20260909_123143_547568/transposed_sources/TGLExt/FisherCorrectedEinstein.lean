import TGLExt.GeneralMetricClausius

set_option autoImplicit false
set_option maxHeartbeats 8500000

namespace ChatgptAudit.FisherEinstein
open Matrix Filter Topology Set TGLExt ChatgptAudit.GeneralMetric
  ChatgptAudit.GeneralClausius ChatgptAudit.Flow019 ChatgptAudit.Flow020 ChatgptAudit.Micro021
open scoped ContDiff Matrix.Norms.Elementwise
noncomputable section

def informationStress (g F : TensorField4) : TensorField4 :=
  fun x => F x - (Matrix.trace (metricInverse g x * F x) / 2) • g x

def correctedStress (g T F : TensorField4) : TensorField4 :=
  fun x => T x + (1 / (2*Real.pi)) • informationStress g F x

theorem tensor_quad_add (A B : Tensor4) (v : Coordinate4) :
    tensorQuad (A+B) v = tensorQuad A v + tensorQuad B v := by
  simp only [tensorQuad, Matrix.add_mulVec, dotProduct_add]

theorem tensor_quad_smul (A : Tensor4) (c : ℝ) (v : Coordinate4) :
    tensorQuad (c • A) v = c * tensorQuad A v := by
  simp only [tensorQuad, Matrix.smul_mulVec, dotProduct_smul, smul_eq_mul]

theorem information_stress_null_contraction (g F : TensorField4) (x v : Coordinate4)
    (hn : tensorQuad (g x) v = 0) :
    tensorQuad (informationStress g F x) v = tensorQuad (F x) v := by
  rw [informationStress, tensorQuad_sub_smul, hn, mul_zero, sub_zero]

theorem corrected_stress_null_contraction (g T F : TensorField4) (x v : Coordinate4)
    (hn : tensorQuad (g x) v = 0) :
    tensorQuad (correctedStress g T F x) v =
      tensorQuad (T x) v + tensorQuad (F x) v / (2*Real.pi) := by
  rw [correctedStress, tensor_quad_add, tensor_quad_smul,
    information_stress_null_contraction g F x v hn]
  ring

theorem information_stress_symmetric (g F : TensorField4) (x : Coordinate4)
    (hg : (g x)ᵀ = g x) (hF : (F x)ᵀ = F x) :
    (informationStress g F x)ᵀ = informationStress g F x := by
  simp only [informationStress, Matrix.transpose_sub, Matrix.transpose_smul, hg, hF]

theorem corrected_stress_symmetric (g T F : TensorField4) (x : Coordinate4)
    (hg : (g x)ᵀ = g x) (hT : (T x)ᵀ = T x) (hF : (F x)ᵀ = F x) :
    (correctedStress g T F x)ᵀ = correctedStress g T F x := by
  simp only [correctedStress, Matrix.transpose_add, Matrix.transpose_smul, hT,
    information_stress_symmetric g F x hg hF]

theorem information_stress_smooth (U : Set Coordinate4) (g F : TensorField4)
    (hg : SmoothMatrixOn U g) (hF : SmoothMatrixOn U F)
    (hLor : ∀ x∈U, LorentzByCongruence (g x)) :
    SmoothMatrixOn U (informationStress g F) := by
  have hprod := SmoothMatrixOn.mul U (metricInverse g) F
    (constructed_metric_inverse_smooth U g hg hLor) hF
  have htrace : ContDiffOn ℝ ∞ (fun x => Matrix.trace (metricInverse g x * F x) / 2) U := by
    have hsum : ContDiffOn ℝ ∞
        (fun x => ∑ i : Fin 4, (metricInverse g x * F x) i i) U := by
      apply ContDiffOn.sum
      intro i _
      exact hprod i i
    exact hsum.div_const 2
  intro i j
  exact (hF i j).sub (htrace.mul (hg i j))

theorem corrected_stress_differentiable (U : Set Coordinate4) (g T F : TensorField4)
    (hg : SmoothMatrixOn U g) (hF : SmoothMatrixOn U F)
    (hLor : ∀ x∈U, LorentzByCongruence (g x))
    (hT : ∀ i j, DifferentiableOn ℝ (fun x => T x i j) U) :
    ∀ i j, DifferentiableOn ℝ (fun x => correctedStress g T F x i j) U := by
  intro i j
  exact (hT i j).add
    (((information_stress_smooth U g F hg hF hLor i j).differentiableOn (by simp)).const_mul (1/(2*Real.pi)))

theorem metric_einstein_from_information_balance
    (U : Set Coordinate4) (hU : IsOpen U) (hconn : IsPreconnected U)
    (g T F : TensorField4)
    (hg : SmoothMatrixOn U g) (hF : SmoothMatrixOn U F)
    (hLor : ∀ x∈U, LorentzByCongruence (g x))
    (hT : ∀ i j, DifferentiableOn ℝ (fun x => T x i j) U)
    (hsT : ∀ x∈U, (T x)ᵀ = T x) (hsF : ∀ x∈U, (F x)ᵀ = F x)
    (eta : ℝ) (heta : eta ≠ 0)
    (hd : ∀ x∈U, ∀ j, tensorFieldDivergence (metricInverse g)
      (leviCivitaField g (metricInverse g)) (correctedStress g T F) x j = 0)
    (hb : ∀ x∈U, ∀ v, tensorQuad (g x) v = 0 →
      eta * tensorQuad (coordinateRicci (leviCivitaField g (metricInverse g)) x) v =
        2*Real.pi*tensorQuad (T x) v + tensorQuad (F x) v) :
    ∃ cosmological : ℝ, ∀ x∈U,
      geometricEinsteinTensor g (metricInverse g) (leviCivitaField g (metricInverse g)) x +
        cosmological • g x = (2*Real.pi/eta) • correctedStress g T F x := by
  apply metric_only_einstein_equation U hU hconn g (correctedStress g T F)
    (2*Real.pi/eta) hLor hg (corrected_stress_differentiable U g T F hg hF hLor hT)
    (fun x hx => corrected_stress_symmetric g T F x
      (lorentz_metric_symmetric (g x) (hLor x hx)) (hsT x hx) (hsF x hx))
  · intro x hx v hn
    rw [tensorQuad_sub_smul, corrected_stress_null_contraction g T F x v hn]
    have he := hb x hx v hn
    apply (mul_left_cancel₀ heta)
    field_simp [heta, Real.pi_ne_zero]
    nlinarith only [he]
  · exact hd

theorem metric_einstein_from_microscopic_information
    {ι : Type} [Fintype ι]
    (U : Set Coordinate4) (hU : IsOpen U) (hconn : IsPreconnected U)
    (g T F : TensorField4) (prob : Coordinate4 → ι → ℝ)
    (hg : SmoothMatrixOn U g) (hF : SmoothMatrixOn U F)
    (hLor : ∀ x∈U, LorentzByCongruence (g x))
    (hT : ∀ i j, DifferentiableOn ℝ (fun x => T x i j) U)
    (hsT : ∀ x∈U, (T x)ᵀ = T x) (hsF : ∀ x∈U, (F x)ᵀ = F x)
    (hpos : ∀ x∈U, ∀ i, 0 < prob x i)
    (screens : MetricScreenFamily U g)
    (curves : ∀ x (_hx : x∈U) v (_hv : v ≠ 0) (_hn : tensorQuad (g x) v = 0),
      DiagonalStateCurve (prob x))
    (hFisher : ∀ x (hx : x∈U) v (hv : v ≠ 0) (hn : tensorQuad (g x) v = 0),
      diagonalFisher (prob x) ((curves x hx v hv hn).tangent 0) = tensorQuad (F x) v)
    (rate eta : ℝ) (hrate : rate ≠ 0) (heta : eta ≠ 0)
    (hheat : ∀ x (hx : x∈U) v (hv : v ≠ 0) (hn : tensorQuad (g x) v = 0),
      Tendsto (fun t => microscopicHeatError (curves x hx v hv hn) rate
        (constructedHeat (screens x hx v hv hn) T rate hU hg hT) t / t^2)
        (𝓝[<] 0) (𝓝 0))
    (harea : ∀ x (hx : x∈U) v (hv : v ≠ 0) (hn : tensorQuad (g x) v = 0),
      Tendsto (fun t => microscopicAreaError (curves x hx v hv hn) eta
        (inducedArea g (screens x hx v hv hn).curve (screens x hx v hv hn).screen.vectors) t / t^2)
        (𝓝[<] 0) (𝓝 0))
    (hd : ∀ x∈U, ∀ j, tensorFieldDivergence (metricInverse g)
      (leviCivitaField g (metricInverse g)) (correctedStress g T F) x j = 0) :
    ∃ cosmological : ℝ, ∀ x∈U,
      geometricEinsteinTensor g (metricInverse g) (leviCivitaField g (metricInverse g)) x +
        cosmological • g x = (2*Real.pi/eta) • correctedStress g T F x := by
  apply metric_einstein_from_information_balance U hU hconn g T F hg hF hLor hT hsT hsF eta heta hd
  intro x hx v hn
  by_cases hv : v = 0
  · subst v
    simp [tensorQuad]
  · have hG := levi_civita_field_smooth U hU g (metricInverse g) hg
      (constructed_metric_inverse_smooth U g hg hLor)
    have ht := levi_civita_field_torsion_free U hU g (metricInverse g)
      (fun y hy => lorentz_metric_symmetric (g y) (hLor y hy))
    have he := geometric_microscopic_compatibility (curves x hx v hv hn) U hU g
      (leviCivitaField g (metricInverse g)) T hg hG hT x v
      (screens x hx v hv hn) (ht x hx) (hpos x hx) rate eta hrate
      (hheat x hx v hv hn) (harea x hx v hv hn)
    simpa only [hFisher x hx v hv hn] using he

theorem zero_information_recovers_original_source (g T : TensorField4) :
    correctedStress g T (fun _ => 0) = T := by
  funext x
  simp [correctedStress, informationStress]

#print axioms informationStress
#print axioms correctedStress
#print axioms tensor_quad_add
#print axioms tensor_quad_smul
#print axioms information_stress_null_contraction
#print axioms corrected_stress_null_contraction
#print axioms information_stress_symmetric
#print axioms corrected_stress_symmetric
#print axioms information_stress_smooth
#print axioms corrected_stress_differentiable
#print axioms metric_einstein_from_information_balance
#print axioms metric_einstein_from_microscopic_information
#print axioms zero_information_recovers_original_source

end
end ChatgptAudit.FisherEinstein
