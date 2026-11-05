import TGLExt.F1Fecho394.ExponentialLiftR2
import TGLExt.F1Fecho394.CanonicalOutput
import Mathlib.LinearAlgebra.Finsupp.LinearCombination

/-! Positivity of the constructed closed lift on the same Fock space.
The square-root factor is the existing one-particle multiplier WT(c/2),
not a newly assumed positive operator. Self-adjointness and identification
with the algebra-vacuum modular polar factor remain separate obligations. -/
set_option autoImplicit false
set_option maxHeartbeats 1200000
noncomputable section
namespace F1Fecho.ExponentialLiftPositive
open TGLExt.ImportedSQ F1Rede.BosonicFock F1Fecho.Exponential
open F1Fecho.ExponentialLift F1Rede.CanonicalWedge

private theorem graph_pairing (Q : H1 →ₗ.[ℂ] H1) (hQ : IsSelfAdjoint Q)
    (a b c d : H1) (hab : (a,b) ∈ Q.graph) (hcd : (c,d) ∈ Q.graph) :
    inner ℂ b c = inner ℂ a d := by
  obtain ⟨u,hu⟩ := Q.mem_graph_iff'.mp hab
  obtain ⟨v,hv⟩ := Q.mem_graph_iff'.mp hcd
  cases hu
  cases hv
  exact one_particle_pairing Q hQ u v

def halfOperator : H1 →ₗ.[ℂ] H1 := WT (rootParameter/2)

theorem half_graph_exists (f : TW.domain) :
    ∃ h : H1, ((f:H1),h) ∈ halfOperator.graph ∧ (h,TW f) ∈ halfOperator.graph := by
  apply (WT_double_graph_iff (rootParameter/2) (f:H1) (TW f)).mp
  have he : 2*(rootParameter/2)=rootParameter := by ring
  rw [he]
  exact TW.mem_graph f

def halfValue (f : TW.domain) : H1 := Classical.choose (half_graph_exists f)

theorem halfValue_graphs (f : TW.domain) :
    ((f:H1),halfValue f) ∈ halfOperator.graph ∧
      (halfValue f,TW f) ∈ halfOperator.graph := Classical.choose_spec (half_graph_exists f)

theorem halfValue_pairing (f g : TW.domain) :
    inner ℂ (f:H1) (TW g) = inner ℂ (halfValue f) (halfValue g) := by
  exact (graph_pairing halfOperator (WT_selfadjoint _) _ _ _ _
    (halfValue_graphs f).1 (halfValue_graphs g).2).symm

theorem exponential_half_pairing (f g : TW.domain) :
    inner ℂ (exponential f) (exponential (TW g)) =
      inner ℂ (exponential (halfValue f)) (exponential (halfValue g)) := by
  rw [exponential_inner,exponential_inner,halfValue_pairing]

private theorem gram_finite {I : Type*} (a b q : I → F)
    (h : ∀ i j, inner ℂ (a i) (b j) = inner ℂ (q i) (q j)) (c : I →₀ ℂ) :
    inner ℂ (c.sum (fun i z => z • a i)) (c.sum (fun i z => z • b i)) =
      inner ℂ (c.sum (fun i z => z • q i)) (c.sum (fun i z => z • q i)) := by
  simp only [Finsupp.sum_inner,Finsupp.inner_sum,inner_smul_left,inner_smul_right,h]

theorem coreGraph_positive (p : F × F) (hp : p ∈ coreGraph TW) :
    0 ≤ (inner ℂ p.1 p.2).re := by
  obtain ⟨c,rfl⟩ := Finsupp.mem_span_range_iff_exists_finsupp.mp hp
  have hfst : (c.sum (fun i z => z • (exponential (i:H1),exponential (TW i)))).1 =
      c.sum (fun i z => z • exponential (i:H1)) := by
    exact map_finsuppSum (LinearMap.fst ℂ F F) _ _
  have hsnd : (c.sum (fun i z => z • (exponential (i:H1),exponential (TW i)))).2 =
      c.sum (fun i z => z • exponential (TW i)) := by
    exact map_finsuppSum (LinearMap.snd ℂ F F) _ _
  rw [hfst,hsnd,gram_finite (fun i : TW.domain => exponential i)
    (fun i => exponential (TW i)) (fun i => exponential (halfValue i)) exponential_half_pairing]
  exact inner_self_nonneg (𝕜 := ℂ)

theorem closedGraph_positive (p : F × F) (hp : p ∈ closedGraph TW) :
    0 ≤ (inner ℂ p.1 p.2).re := by
  have hc : IsClosed {q : F × F | 0 ≤ (inner ℂ q.1 q.2).re} :=
    isClosed_le continuous_const (Complex.continuous_re.comp (continuous_fst.inner continuous_snd))
  apply closure_minimal (fun q hq => coreGraph_positive q hq) hc
  rw [← Submodule.topologicalClosure_coe]
  exact hp

theorem canonicalLift_positive (x : canonicalLift.domain) :
    0 ≤ (inner ℂ (x:F) (canonicalLift x)).re :=
  closedGraph_positive ((x:F),canonicalLift x) (closedValue_graph TW x)

end F1Fecho.ExponentialLiftPositive
#print axioms F1Fecho.ExponentialLiftPositive.half_graph_exists
#print axioms F1Fecho.ExponentialLiftPositive.halfValue_pairing
#print axioms F1Fecho.ExponentialLiftPositive.exponential_half_pairing
#print axioms F1Fecho.ExponentialLiftPositive.coreGraph_positive
#print axioms F1Fecho.ExponentialLiftPositive.closedGraph_positive
#print axioms F1Fecho.ExponentialLiftPositive.canonicalLift_positive
