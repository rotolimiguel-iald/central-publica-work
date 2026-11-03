import TGLExt.F1Fecho394.RegularScalarGNSStrongContinuityR1
import TGLExt.F1Fecho394.RegularScalarTomitaGraphR1
/-! Density from an actual bounded star-strong approximate identity of finite
square weight. The supplied hypotheses describe the regularizing operators;
no GNS density or closability conclusion is accepted as a field. -/
set_option autoImplicit false
set_option maxHeartbeats 1000000
noncomputable section
namespace F1Fecho.RegularScalarStarDensity
open TGLV350.Regular MeasureTheory Filter F1Fecho.RegularScalarGNS
open F1Fecho.RegularScalarGNSAction F1Fecho.RegularScalarGNSRepresentation
open F1Fecho.RegularScalarTomitaGraph F1Fecho.RegularScalarGNSStrongContinuity
open scoped Topology
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
variable (D : Context H) (b : ℝ → D.algebra.toStarSubalgebra)

def leftRegularization (A : finiteIdeal D) (h : ℝ) : finiteIdeal D :=
  scalarGNSLeftProduct D (star (b h)) A

theorem leftRegularization_mem_starCore
    (hb : ∀ h, 0<h → HasFiniteDualSquare (b h).val)
    (A : finiteIdeal D) (h : ℝ) (hh : 0<h) :
    (leftRegularization D b A h).val ∈ finiteStarCore D := by
  refine ⟨(leftRegularization D b A h).property,?_⟩
  change HasFiniteDualSquare (star (star (b h).val*A.val.val))
  rw [star_mul,star_star]
  exact HasFiniteDualSquare.left_mul _ _ (hb h hh)

theorem embedding_leftRegularization_tendsto
    (hbound : ∀ h, ‖(b h).val‖ ≤ 1)
    (hstrong : ∀ v, Tendsto (fun h : ℝ => star (b h).val v) (𝓝[>] 0) (𝓝 v))
    (A : finiteIdeal D) :
    Tendsto (fun h : ℝ => GNSEmbedding D (leftRegularization D b A h))
      (𝓝[>] 0) (𝓝 (GNSEmbedding D A)) := by
  have hb : ∀ h, ‖(star (b h)).val‖ ≤ 1 := by
    intro h
    change ‖star (b h).val‖ ≤ 1
    rw [norm_star]
    exact hbound h
  have hs : ∀ v, Tendsto (fun h : ℝ => (star (b h)).val v)
      (𝓝[>] 0) (𝓝 ((1 : D.algebra.toStarSubalgebra).val v)) := hstrong
  have ht := scalarGNSRepresentation_tendsto_of_uniformly_bounded D
    (fun h => star (b h)) 1 1 hb hs (GNSEmbedding D A)
  rw [map_one] at ht
  have he : (fun h : ℝ => GNSEmbedding D (leftRegularization D b A h)) =
      (fun h => scalarGNSRepresentation D (star (b h)) (GNSEmbedding D A)) := by
    funext h
    exact (scalarGNSAction_intertwines D (star (b h)) A).symm
  rw [he]
  exact ht

theorem starEmbedding_denseRange
    (hb : ∀ h, 0<h → HasFiniteDualSquare (b h).val)
    (hbound : ∀ h, ‖(b h).val‖ ≤ 1)
    (hstrong : ∀ v, Tendsto (fun h : ℝ => star (b h).val v) (𝓝[>] 0) (𝓝 v)) :
    DenseRange (scalarGNSStarEmbedding D) := by
  have hs : Set.range (GNSEmbedding D) ⊆ closure (Set.range (scalarGNSStarEmbedding D)) := by
    rintro v ⟨A,rfl⟩
    apply isClosed_closure.mem_of_tendsto (embedding_leftRegularization_tendsto D b hbound hstrong A)
    filter_upwards [self_mem_nhdsWithin] with h hh
    apply subset_closure
    exact ⟨⟨(leftRegularization D b A h).val,leftRegularization_mem_starCore D b hb A h hh⟩,rfl⟩
  intro v
  exact (closure_minimal hs isClosed_closure) ((GNSEmbedding_denseRange D) v)

theorem graph_domain_dense
    (hb : ∀ h, 0<h → HasFiniteDualSquare (b h).val)
    (hbound : ∀ h, ‖(b h).val‖ ≤ 1)
    (hstrong : ∀ v, Tendsto (fun h : ℝ => star (b h).val v) (𝓝[>] 0) (𝓝 v)) :
    Dense (Prod.fst '' scalarTomitaGraph D) := by
  apply (starEmbedding_denseRange D b hb hbound hstrong).mono
  rintro x ⟨A,rfl⟩
  exact ⟨(scalarGNSStarEmbedding D A,scalarGNSStarEmbedding D (star A)),⟨A,rfl⟩,rfl⟩
end F1Fecho.RegularScalarStarDensity
#print axioms F1Fecho.RegularScalarStarDensity.leftRegularization
#print axioms F1Fecho.RegularScalarStarDensity.leftRegularization_mem_starCore
#print axioms F1Fecho.RegularScalarStarDensity.embedding_leftRegularization_tendsto
#print axioms F1Fecho.RegularScalarStarDensity.starEmbedding_denseRange
#print axioms F1Fecho.RegularScalarStarDensity.graph_domain_dense
