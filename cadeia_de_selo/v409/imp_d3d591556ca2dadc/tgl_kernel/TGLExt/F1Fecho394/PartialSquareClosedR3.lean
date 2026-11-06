import TGLExt.F1Fecho394.PartialSquareGraphR2
import Mathlib.Topology.Sequences
/-! Closedness of the genuine square of a closed symmetric partial operator.
The proof controls the middle graph coordinate by Cauchy--Schwarz and uses
completeness; ordinary density is not substituted for graph closedness. -/
set_option autoImplicit false
set_option maxHeartbeats 1000000
noncomputable section
open Filter Topology
namespace F1Fecho.PartialSquare
variable {H : Type*} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

def middle (T : H →ₗ.[ℂ] H) : (square T).domain →ₗ[ℂ] H := T.toFun.comp (input T)

theorem middle_norm_sq_le (T : H →ₗ.[ℂ] H) (hs : T.IsFormalAdjoint T)
    (x : (square T).domain) : ‖middle T x‖^2 ≤ ‖(x:H)‖ * ‖square T x‖ := by
  have h := re_inner_le_norm (𝕜 := ℂ) (x:H) (square T x)
  change (inner ℂ (x:H) (square T x)).re ≤ ‖(x:H)‖ * ‖square T x‖ at h
  rw [square_energy T hs x] at h
  exact h

theorem square_graph_iff_two (T : H →ₗ.[ℂ] H) (x y : H) :
    (x,y) ∈ (square T).graph ↔ ∃ z : H, (x,z) ∈ T.graph ∧ (z,y) ∈ T.graph := by
  rw [square_graph_iff]
  constructor
  · rintro ⟨hx,hTx,hxy⟩
    refine ⟨T ⟨x,hx⟩,?_,?_⟩
    · exact (LinearPMap.mem_graph_iff T).mpr ⟨⟨x,hx⟩,rfl,rfl⟩
    · exact (LinearPMap.mem_graph_iff T).mpr ⟨⟨T ⟨x,hx⟩,hTx⟩,rfl,hxy⟩
  · rintro ⟨z,hxz,hzy⟩
    obtain ⟨u,hu,hTu⟩ := (LinearPMap.mem_graph_iff T).mp hxz
    obtain ⟨v,hv,hTv⟩ := (LinearPMap.mem_graph_iff T).mp hzy
    dsimp only [Prod.fst,Prod.snd] at hu hTu hv hTv
    subst x
    have ht : T u = (v:H) := hTu.trans hv.symm
    have hm : T u ∈ T.domain := ht.symm ▸ v.property
    refine ⟨u.property,hm,?_⟩
    have he : (⟨T u,hm⟩ : T.domain) = v := Subtype.ext ht
    rw [he]
    exact hTv

theorem square_formalAdjoint (T : H →ₗ.[ℂ] H) (hs : T.IsFormalAdjoint T) :
    (square T).IsFormalAdjoint (square T) := by
  intro x y
  let u : T.domain := ⟨x,x.property.choose⟩
  let v : T.domain := ⟨y,y.property.choose⟩
  let Tu : T.domain := ⟨T u,x.property.choose_spec⟩
  let Tv : T.domain := ⟨T v,y.property.choose_spec⟩
  change inner ℂ (T Tu) (v:H) = inner ℂ (u:H) (T Tv)
  exact (hs Tu v).trans (hs u Tv)

theorem square_closed (T : H →ₗ.[ℂ] H) (hc : T.IsClosed) (hs : T.IsFormalAdjoint T) :
    (square T).IsClosed := by
  apply IsSeqClosed.isClosed
  intro p q hp hpq
  choose v hv1 hv2 using (fun n => (LinearPMap.mem_graph_iff (square T)).mp (hp n))
  have hx : Tendsto (fun n => (v n:H)) atTop (𝓝 q.1) := by
    simpa only [hv1,Function.comp_def] using (continuous_fst.tendsto q).comp hpq
  have hy : Tendsto (fun n => square T (v n)) atTop (𝓝 q.2) := by
    simpa only [hv2,Function.comp_def] using (continuous_snd.tendsto q).comp hpq
  have hmid : CauchySeq (fun n => middle T (v n)) := by
    apply Metric.cauchySeq_iff.mpr
    intro ε hε
    obtain ⟨Nx,hNx⟩ := Metric.cauchySeq_iff.mp hx.cauchySeq ε hε
    obtain ⟨Ny,hNy⟩ := Metric.cauchySeq_iff.mp hy.cauchySeq ε hε
    refine ⟨max Nx Ny,?_⟩
    intro m hm n hn
    have hxx : ‖(v m:H)-(v n:H)‖ < ε := by
      rw [← dist_eq_norm]
      exact hNx m (le_trans (le_max_left _ _) hm) n (le_trans (le_max_left _ _) hn)
    have hyy : ‖square T (v m)-square T (v n)‖ < ε := by
      rw [← dist_eq_norm]
      exact hNy m (le_trans (le_max_right _ _) hm) n (le_trans (le_max_right _ _) hn)
    have hb := middle_norm_sq_le T hs (v m-v n)
    rw [map_sub,LinearPMap.map_sub] at hb
    change ‖middle T (v m)-middle T (v n)‖^2 ≤
      ‖(v m:H)-(v n:H)‖ * ‖square T (v m)-square T (v n)‖ at hb
    have hprod : ‖(v m:H)-(v n:H)‖ * ‖square T (v m)-square T (v n)‖ < ε*ε := by
      calc
        _ ≤ ε * ‖square T (v m)-square T (v n)‖ := mul_le_mul_of_nonneg_right hxx.le (norm_nonneg _)
        _ < ε*ε := mul_lt_mul_of_pos_left hyy hε
    rw [dist_eq_norm]
    nlinarith [norm_nonneg (middle T (v m)-middle T (v n))]
  obtain ⟨z,hz⟩ := cauchySeq_tendsto_of_complete hmid
  have hfirst : (q.1,z) ∈ T.graph := by
    apply hc.mem_of_tendsto (hx.prodMk_nhds hz)
    apply Filter.Eventually.of_forall
    intro n
    exact (LinearPMap.mem_graph_iff T).mpr ⟨input T (v n),rfl,rfl⟩
  have hsecond : (z,q.2) ∈ T.graph := by
    apply hc.mem_of_tendsto (hz.prodMk_nhds hy)
    apply Filter.Eventually.of_forall
    intro n
    exact (LinearPMap.mem_graph_iff T).mpr
      ⟨⟨middle T (v n),(v n).property.choose_spec⟩,rfl,rfl⟩
  exact (square_graph_iff_two T q.1 q.2).mpr ⟨z,hfirst,hsecond⟩

end F1Fecho.PartialSquare
#print axioms F1Fecho.PartialSquare.middle_norm_sq_le
#print axioms F1Fecho.PartialSquare.square_graph_iff_two
#print axioms F1Fecho.PartialSquare.square_formalAdjoint
#print axioms F1Fecho.PartialSquare.square_closed
