-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_026 (06/09/2026), transposta em 06/09/2026
-- Lote 024..026: a perturbacao de GIBBS realizada no mesmo Hilbert da torre (estado fiel,
--   normalizado, distinto da orbita modular; resposta quadratica; calor/fonte por normalizacao);
--   o LIMITE TERMICO: para perfil constante nao tracial a preparacao NAO tem limite em norma
--   (nao-Cauchy) e o acoplamento da torre e ilimitado; corte com escala escolhida; AFINIDADE:
--   criterio exato (Cauchy <=> afinidade-limite > 0), estado global no Hilbert original, fiel e
--   ciclico; perfil gradual (muda em infinitos sitios, ainda fiel). Estatuto [REAL / INPUT / OPEN]:
--   selecao fisica, area, H3 dinamico, dimensao/assinatura, globalizacao e a classificacao geral
--   dos estados normais (disjuncao) seguem INPUT/OPEN — a bancada NAO promoveu nao-Cauchy a teorema
--   geral de disjuncao nem importou Kakutani.
-- Auditoria da gerencia (sessao d554e796, 06/09/2026): hashes 100%; manifestos 202/206/220;
--   3/3 auditores da bancada exit 0; recompilacao INDEPENDENTE 22/22, axiomas no trio; guarda de
--   colisao estatica no ROOT; enunciados lidos. Transposicao MECANICA (cabecalho + prefixo TGLExt.).
-- NAO move gate; nao e fisica; NOT_FALSIFIED nunca e CONFIRMED; CONFIRMADA proibido.
-- ---------------------------------------------------------------------
import TGLExt.AffinityProducts

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
