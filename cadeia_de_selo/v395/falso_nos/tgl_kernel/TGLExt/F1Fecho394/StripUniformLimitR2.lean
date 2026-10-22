import TGLExt.F1Fecho394.StripMaximumR2
import Mathlib.Topology.MetricSpace.Cauchy
/-! Boundary Cauchy estimates yield an analytic bounded strip limit. This
is a closure lemma for later use with actual joint algebra/adjoint vectors. -/
set_option autoImplicit false
set_option maxHeartbeats 1000000
noncomputable section
open Filter Set
open scoped Topology
namespace F1Fecho.StripUniformLimit
open F1Fecho.StripMaximum

theorem closure_strip_subset : closure strip ⊆ closedStrip := by
  apply closure_minimal
  · intro z hz; exact ⟨hz.1.le,hz.2.le⟩
  · exact (isClosed_le continuous_const Complex.continuous_im).inter
      (isClosed_le Complex.continuous_im continuous_const)

theorem strip_open : IsOpen strip :=
  (isOpen_lt continuous_const Complex.continuous_im).inter
    (isOpen_lt Complex.continuous_im continuous_const)

theorem cauchy_of_edges (F : ℕ→ℂ→ℂ)
    (hd : ∀ n, DiffContOnCl ℂ (F n) strip)
    (hb : ∀ n, ∃ M : ℝ, ∀ z∈closedStrip, ‖F n z‖≤M)
    (hedge : ∀ ε>0, ∃ N : ℕ, ∀ m≥N, ∀ n≥N,
      ∀ z : ℂ, (z.im=0 ∨ z.im=1) → ‖F m z-F n z‖≤ε) :
    UniformCauchySeqOn F atTop closedStrip := by
  apply Metric.uniformCauchySeqOn_iff.mpr
  intro ε hε
  obtain ⟨N,hN⟩ := hedge (ε/2) (by positivity)
  refine ⟨N,fun m hm n hn z hz => ?_⟩
  have hd' := (hd m).sub (hd n)
  have hb' : ∃ M : ℝ, ∀ z∈closedStrip, ‖F m z-F n z‖≤M := by
    obtain ⟨M,hM⟩ := hb m
    obtain ⟨L,hL⟩ := hb n
    exact ⟨M+L,fun z hz => (norm_sub_le _ _).trans (add_le_add (hM z hz) (hL z hz))⟩
  have he := norm_le_edge_bound (f:=fun z => F m z-F n z) (C:=ε/2)
    (by positivity) hd' hb'
    (fun z hz => hN m hm n hn z (Or.inl hz))
    (fun z hz => hN m hm n hn z (Or.inr hz)) hz
  rw [dist_eq_norm]
  exact he.trans_lt (by linarith)

theorem exists_limit (F : ℕ→ℂ→ℂ)
    (hd : ∀ n, DiffContOnCl ℂ (F n) strip)
    (hb : ∀ n, ∃ M : ℝ, ∀ z∈closedStrip, ‖F n z‖≤M)
    (hc : UniformCauchySeqOn F atTop closedStrip) :
    ∃ f : ℂ→ℂ, TendstoUniformlyOn F f atTop closedStrip ∧
      DiffContOnCl ℂ f strip ∧ (∃ M : ℝ, ∀ z∈closedStrip, ‖f z‖≤M) := by
  classical
  have hex (z : ℂ) (hz : z∈closedStrip) : ∃ a : ℂ, Tendsto (fun n => F n z) atTop (𝓝 a) :=
    cauchySeq_tendsto_of_complete (hc.cauchySeq hz)
  let f : ℂ→ℂ := fun z => if hz : z∈closedStrip then (hex z hz).choose else 0
  have ht : TendstoUniformlyOn F f atTop closedStrip := by
    apply hc.tendstoUniformlyOn_of_tendsto
    intro z hz
    simpa only [f,dif_pos hz] using (hex z hz).choose_spec
  have htc := ht.mono closure_strip_subset
  have hdf : DiffContOnCl ℂ f strip :=
    ⟨(ht.mono (fun z hz => ⟨hz.1.le,hz.2.le⟩)).tendstoLocallyUniformlyOn.differentiableOn
      (Eventually.of_forall fun n => (hd n).differentiableOn) strip_open,
     htc.continuousOn (Filter.Eventually.frequently (Eventually.of_forall fun n => (hd n).continuousOn))⟩
  have he := Metric.tendstoUniformlyOn_iff.mp ht 1 (by norm_num)
  obtain ⟨n,hn⟩ := he.exists
  obtain ⟨M,hM⟩ := hb n
  refine ⟨f,ht,hdf,M+1,fun z hz => ?_⟩
  have hz' := hn z hz
  have hn' : ‖f z-F n z‖<1 := by simpa only [dist_eq_norm] using hz'
  calc
    ‖f z‖ ≤ ‖f z-F n z‖+‖F n z‖ := norm_le_norm_sub_add _ _
    _ ≤ M+1 := by linarith [hM z hz]

end F1Fecho.StripUniformLimit
#print axioms F1Fecho.StripUniformLimit.cauchy_of_edges
#print axioms F1Fecho.StripUniformLimit.exists_limit
