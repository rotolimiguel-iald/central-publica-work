import TGLExt.GeneralMetricEinstein
import TGLExt.UnitaryClausiusBridge

set_option autoImplicit false
set_option maxHeartbeats 8500000

namespace ChatgptAudit.GeneralClausius
open Matrix Filter Topology Set TGLExt ChatgptAudit.GeneralMetric
  ChatgptAudit.Flow019 ChatgptAudit.Flow020 ChatgptAudit.Unitary022
open scoped ContDiff Matrix.Norms.Elementwise
noncomputable section

def MetricScreenFamily (U : Set Coordinate4) (g : TensorField4) :=
  ∀ p, p ∈ U → ∀ v, v ≠ 0 → tensorQuad (g p) v = 0 →
    EquilibriumScreenData U g (leviCivitaField g (metricInverse g)) p v

def MetricScreenClausius
    {U : Set Coordinate4} {g : TensorField4} {p v : Coordinate4}
    (P : EquilibriumScreenData U g (leviCivitaField g (metricInverse g)) p v)
    (T : TensorField4) (rate eta : ℝ) (hU : IsOpen U) (hg : SmoothMatrixOn U g)
    (hT : ∀ i j, DifferentiableOn ℝ (fun x => T x i j) U) : Prop :=
  Tendsto (fun t => horizonBalancePrimitive rate eta
    (inducedArea g P.curve P.screen.vectors) (constructedHeat P T rate hU hg hT) t / t^2)
    (𝓝[<] 0) (𝓝 0)

theorem metric_screen_clausius_iff_null_balance
    (U : Set Coordinate4) (hU : IsOpen U) (g T : TensorField4)
    (hLor : ∀ x∈U, LorentzByCongruence (g x)) (hg : SmoothMatrixOn U g)
    (hT : ∀ i j, DifferentiableOn ℝ (fun x => T x i j) U)
    (p v : Coordinate4) (hp : p∈U)
    (P : EquilibriumScreenData U g (leviCivitaField g (metricInverse g)) p v)
    (rate eta : ℝ) (hrate : rate ≠ 0) (heta : eta ≠ 0) :
    MetricScreenClausius P T rate eta hU hg hT ↔
      tensorQuad (coordinateRicci (leviCivitaField g (metricInverse g)) p) v =
        (2*Real.pi/eta) * tensorQuad (T p) v := by
  have hG := levi_civita_field_smooth U hU g (metricInverse g) hg
    (constructed_metric_inverse_smooth U g hg hLor)
  have ht := levi_civita_field_torsion_free U hU g (metricInverse g)
    (fun x hx => lorentz_metric_symmetric (g x) (hLor x hx))
  exact constructed_clausius_iff_null_balance P T rate eta hU hg hG hT
    (ht p hp) hrate heta

theorem metric_screen_clausius_independent_of_screen
    (U : Set Coordinate4) (hU : IsOpen U) (g T : TensorField4)
    (hLor : ∀ x∈U, LorentzByCongruence (g x)) (hg : SmoothMatrixOn U g)
    (hT : ∀ i j, DifferentiableOn ℝ (fun x => T x i j) U)
    (p v : Coordinate4) (hp : p∈U)
    (P Q : EquilibriumScreenData U g (leviCivitaField g (metricInverse g)) p v)
    (rate eta : ℝ) (hrate : rate ≠ 0) (heta : eta ≠ 0) :
    MetricScreenClausius P T rate eta hU hg hT ↔
      MetricScreenClausius Q T rate eta hU hg hT :=
  (metric_screen_clausius_iff_null_balance U hU g T hLor hg hT p v hp P rate eta hrate heta).trans
    (metric_screen_clausius_iff_null_balance U hU g T hLor hg hT p v hp Q rate eta hrate heta).symm

theorem metric_einstein_from_screen_clausius
    (U : Set Coordinate4) (hU : IsOpen U) (hconn : IsPreconnected U)
    (g T : TensorField4) (hLor : ∀ x∈U, LorentzByCongruence (g x))
    (hg : SmoothMatrixOn U g)
    (hT : ∀ i j, DifferentiableOn ℝ (fun x => T x i j) U)
    (hsT : ∀ x∈U, (T x)ᵀ = T x)
    (hdT : ∀ x∈U, ∀ j, tensorFieldDivergence (metricInverse g)
      (leviCivitaField g (metricInverse g)) T x j = 0)
    (screens : MetricScreenFamily U g)
    (rate eta : ℝ) (hrate : rate ≠ 0) (heta : eta ≠ 0)
    (hclausius : ∀ p (hp : p∈U) v (hv : v ≠ 0) (hn : tensorQuad (g p) v = 0),
      MetricScreenClausius (screens p hp v hv hn) T rate eta hU hg hT) :
    ∃ cosmological : ℝ, ∀ x∈U,
      geometricEinsteinTensor g (metricInverse g) (leviCivitaField g (metricInverse g)) x +
      cosmological • g x = (2*Real.pi/eta) • T x := by
  apply metric_only_einstein_equation U hU hconn g T (2*Real.pi/eta) hLor hg hT hsT
  · intro p hp v hn
    by_cases hv : v = 0
    · subst v
      simp [tensorQuad]
    · have hb := (metric_screen_clausius_iff_null_balance U hU g T hLor hg hT p v hp
        (screens p hp v hv hn) rate eta hrate heta).mp (hclausius p hp v hv hn)
      rw [tensorQuad_sub_smul, hb, sub_self]
  · exact hdT

theorem metric_unitary_matching_produces_clausius
    {U : Set Coordinate4} {g : TensorField4} {p v : Coordinate4}
    (P : EquilibriumScreenData U g (leviCivitaField g (metricInverse g)) p v)
    (T : TensorField4) (rate eta : ℝ) (hU : IsOpen U) (hg : SmoothMatrixOn U g)
    (hT : ∀ i j, DifferentiableOn ℝ (fun x => T x i j) U)
    (M : UnitaryScreenMatching P T rate eta hU hg hT) :
    MetricScreenClausius P T rate eta hU hg hT :=
  unitary_screen_matching_produces_clausius P T rate eta hU hg hT M

theorem metric_einstein_from_unitary_matching
    (U : Set Coordinate4) (hU : IsOpen U) (hconn : IsPreconnected U)
    (g T : TensorField4) (hLor : ∀ x∈U, LorentzByCongruence (g x))
    (hg : SmoothMatrixOn U g)
    (hT : ∀ i j, DifferentiableOn ℝ (fun x => T x i j) U)
    (hsT : ∀ x∈U, (T x)ᵀ = T x)
    (hdT : ∀ x∈U, ∀ j, tensorFieldDivergence (metricInverse g)
      (leviCivitaField g (metricInverse g)) T x j = 0)
    (screens : MetricScreenFamily U g)
    (rate eta : ℝ) (hrate : rate ≠ 0) (heta : eta ≠ 0)
    (hmatch : ∀ p (hp : p∈U) v (hv : v ≠ 0) (hn : tensorQuad (g p) v = 0),
      Nonempty (UnitaryScreenMatching (screens p hp v hv hn) T rate eta hU hg hT)) :
    ∃ cosmological : ℝ, ∀ x∈U,
      geometricEinsteinTensor g (metricInverse g) (leviCivitaField g (metricInverse g)) x +
      cosmological • g x = (2*Real.pi/eta) • T x := by
  apply metric_einstein_from_screen_clausius U hU hconn g T hLor hg hT hsT hdT
    screens rate eta hrate heta
  intro p hp v hv hn
  obtain ⟨M⟩ := hmatch p hp v hv hn
  exact metric_unitary_matching_produces_clausius (screens p hp v hv hn) T rate eta hU hg hT M

/-- A nonzero source cannot be matched by a zero Einstein tensor through a scalar multiple of eta. -/
def pureTimeTensor : Tensor4 :=
  !![1,0,0,0; 0,0,0,0; 0,0,0,0; 0,0,0,0]

theorem nonzero_pure_time_source_has_no_scalar_metric_balance (coupling : ℝ)
    (hc : coupling ≠ 0) :
    ¬ ∃ cosmological : ℝ,
      (0 : Tensor4) + cosmological • eta4 = coupling • pureTimeTensor := by
  rintro ⟨cosmological, he⟩
  have hspace := congrArg (fun A : Tensor4 => A 1 1) he
  have htime := congrArg (fun A : Tensor4 => A 0 0) he
  norm_num [eta4, pureTimeTensor] at hspace htime
  exact hc (by linarith)

#print axioms MetricScreenFamily
#print axioms MetricScreenClausius
#print axioms metric_screen_clausius_iff_null_balance
#print axioms metric_screen_clausius_independent_of_screen
#print axioms metric_einstein_from_screen_clausius
#print axioms metric_unitary_matching_produces_clausius
#print axioms metric_einstein_from_unitary_matching
#print axioms pureTimeTensor
#print axioms nonzero_pure_time_source_has_no_scalar_metric_balance

end
end ChatgptAudit.GeneralClausius
