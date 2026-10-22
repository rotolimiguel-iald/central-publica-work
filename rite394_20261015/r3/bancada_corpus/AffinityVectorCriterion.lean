import AffinityProducts

set_option autoImplicit false
set_option maxHeartbeats 16000000
namespace ChatgptAudit.Profile026
open Filter Topology Set TGLExt
noncomputable section

theorem profile_vectors_cauchy_of_positive (P Q : SiteProfile)
    (hpos : 0<profileAffinityLimit P Q) : CauchySeq (profileVector P Q) := by
  have ht : Tendsto (fun N => 2-2*(profileAffinityLimit P Q/profileAffinity P Q N))
      atTop (𝓝 (0:ℝ)) := by
    convert (tendsto_const_nhds (x := (2:ℝ))).sub
      ((profile_affinity_ratio_tendsto P Q hpos).const_mul 2) using 1
    norm_num
  apply Metric.cauchySeq_iff'.mpr
  intro ε hε
  obtain ⟨L,hL⟩ := eventually_atTop.mp (ht.eventually (gt_mem_nhds (sq_pos_of_pos hε)))
  refine ⟨L,fun N hN => ?_⟩
  have hs := profile_vectors_distance P Q hN
  have hb := div_le_div_of_nonneg_right (profile_affinity_limit_le P Q N)
    (profile_affinity_positive P Q L).le
  have hl := hL L (le_refl L)
  rw [dist_comm,dist_eq_norm]
  nlinarith [norm_nonneg (profileVector P Q L-profileVector P Q N)]

theorem profile_positive_of_vectors_cauchy (P Q : SiteProfile)
    (hc : CauchySeq (profileVector P Q)) : 0<profileAffinityLimit P Q := by
  obtain ⟨L,hL⟩ := Metric.cauchySeq_iff'.mp hc (1:ℝ) zero_lt_one
  have he : ∀ᶠ N in atTop, profileAffinity P Q L/2≤profileAffinity P Q N := by
    filter_upwards [eventually_ge_atTop L] with N hN
    have hd := hL N hN
    rw [dist_comm,dist_eq_norm] at hd
    have hs := profile_vectors_distance P Q hN
    have hr : 1/2<profileAffinity P Q N/profileAffinity P Q L := by
      nlinarith [norm_nonneg (profileVector P Q L-profileVector P Q N)]
    have hb := (lt_div_iff₀ (profile_affinity_positive P Q L)).mp hr
    linarith
  exact lt_of_lt_of_le (half_pos (profile_affinity_positive P Q L))
    (ge_of_tendsto (profile_affinity_tendsto P Q) he)

theorem profile_vectors_cauchy_iff (P Q : SiteProfile) :
    CauchySeq (profileVector P Q) ↔ 0<profileAffinityLimit P Q :=
  ⟨profile_positive_of_vectors_cauchy P Q,profile_vectors_cauchy_of_positive P Q⟩

theorem profile_vectors_limit_iff (P Q : SiteProfile) :
    (∃ v : TowerHilbert P, Tendsto (profileVector P Q) atTop (𝓝 v)) ↔
      0<profileAffinityLimit P Q := by
  constructor
  · rintro ⟨v,hv⟩
    exact profile_positive_of_vectors_cauchy P Q hv.cauchySeq
  · intro hp
    exact cauchySeq_tendsto_of_complete (profile_vectors_cauchy_of_positive P Q hp)

theorem profile_zero_affinity_no_limit (P Q : SiteProfile) (hz : profileAffinityLimit P Q=0)
    (v : TowerHilbert P) : ¬Tendsto (profileVector P Q) atTop (𝓝 v) := by
  intro hv
  have hp := (profile_vectors_limit_iff P Q).mp ⟨v,hv⟩
  rw [hz] at hp
  exact (lt_irrefl 0) hp

theorem profile_summable_has_limit (P Q : SiteProfile)
    (hs : Summable (fun n => 1-siteAffinity P Q n)) :
    ∃ v : TowerHilbert P, Tendsto (profileVector P Q) atTop (𝓝 v) :=
  (profile_vectors_limit_iff P Q).mpr (affinity_loss_summable_positive_limit P Q hs)

#print axioms profile_vectors_cauchy_of_positive
#print axioms profile_positive_of_vectors_cauchy
#print axioms profile_vectors_cauchy_iff
#print axioms profile_vectors_limit_iff
#print axioms profile_zero_affinity_no_limit
#print axioms profile_summable_has_limit
end
end ChatgptAudit.Profile026
