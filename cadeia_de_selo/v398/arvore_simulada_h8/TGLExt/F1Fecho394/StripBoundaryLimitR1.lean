import TGLExt.F1Fecho394.StripUniformLimitR2
/-! Convergence on both real boundary lines determines a bounded analytic
limit throughout the strip. Used with graph-vector convergence, not with an
assumed bound on approximating algebra operators. -/
set_option autoImplicit false
set_option maxHeartbeats 1200000
noncomputable section
open Filter Set
open scoped Topology
namespace F1Fecho.StripBoundaryLimit
open F1Fecho.StripMaximum F1Fecho.StripUniformLimit

theorem of_boundary_uniform (F : ℕ→ℂ→ℂ) (L U : ℝ→ℂ)
    (hd : ∀ n, DiffContOnCl ℂ (F n) strip)
    (hb : ∀ n, ∃ M : ℝ, ∀ z∈closedStrip, ‖F n z‖≤M)
    (hL : TendstoUniformlyOn (fun (n : ℕ) (t : ℝ) => F n t) L atTop univ)
    (hU : TendstoUniformlyOn (fun (n : ℕ) (t : ℝ) => F n ((t:ℂ)+Complex.I)) U atTop univ) :
    ∃ f : ℂ→ℂ, DiffContOnCl ℂ f strip ∧
      (∃ M : ℝ, ∀ z∈closedStrip, ‖f z‖≤M) ∧
      (∀ t : ℝ, f t=L t) ∧ (∀ t : ℝ, f ((t:ℂ)+Complex.I)=U t) := by
  have hc : UniformCauchySeqOn F atTop closedStrip := by
    apply cauchy_of_edges F hd hb
    intro ε hε
    obtain ⟨NL,hNL⟩ := Metric.uniformCauchySeqOn_iff.mp hL.uniformCauchySeqOn ε hε
    obtain ⟨NU,hNU⟩ := Metric.uniformCauchySeqOn_iff.mp hU.uniformCauchySeqOn ε hε
    refine ⟨max NL NU,fun m hm n hn z hz => ?_⟩
    rcases hz with hz|hz
    · have he : (z.re:ℂ)=z := by apply Complex.ext <;> simp [hz]
      have h := hNL m (le_trans (le_max_left _ _) hm) n (le_trans (le_max_left _ _) hn) z.re (mem_univ _)
      simpa only [he,dist_eq_norm] using h.le
    · have he : (z.re:ℂ)+Complex.I=z := by apply Complex.ext <;> simp [hz]
      have h := hNU m (le_trans (le_max_right _ _) hm) n (le_trans (le_max_right _ _) hn) z.re (mem_univ _)
      simpa only [he,dist_eq_norm] using h.le
  obtain ⟨f,ht,hf,hfb⟩ := exists_limit F hd hb hc
  refine ⟨f,hf,hfb,?_,?_⟩
  · intro t
    exact tendsto_nhds_unique (ht.tendsto_at (by simp [closedStrip])) (hL.tendsto_at (mem_univ t))
  · intro t
    exact tendsto_nhds_unique (ht.tendsto_at (by simp [closedStrip])) (hU.tendsto_at (mem_univ t))

end F1Fecho.StripBoundaryLimit
#print axioms F1Fecho.StripBoundaryLimit.of_boundary_uniform
