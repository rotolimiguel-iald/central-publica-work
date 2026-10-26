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
import TGLExt.ProfileOverlapFactorization

set_option autoImplicit false
set_option maxHeartbeats 16000000
namespace ChatgptAudit.Profile026
open Filter Topology Set TGLExt
noncomputable section

def profileAffinityLimit (P Q : SiteProfile) : ℝ := ⨅ N, profileAffinity P Q N
def affinityLossSum (P Q : SiteProfile) (N : ℕ) : ℝ :=
  ∑ n ∈ Finset.range (N+1), (1-siteAffinity P Q n)

theorem profile_affinity_antitone (P Q : SiteProfile) : Antitone (profileAffinity P Q) := by
  apply antitone_nat_of_succ_le
  intro N
  rw [profile_affinity_succ]
  exact mul_le_of_le_one_right (profile_affinity_positive P Q N).le (site_affinity_le_one P Q (N+1))

theorem profile_affinity_bddBelow (P Q : SiteProfile) : BddBelow (range (profileAffinity P Q)) :=
  ⟨0,by rintro _ ⟨N,rfl⟩; exact (profile_affinity_positive P Q N).le⟩

theorem profile_affinity_limit_nonnegative (P Q : SiteProfile) : 0≤profileAffinityLimit P Q :=
  le_ciInf (fun N => (profile_affinity_positive P Q N).le)

theorem profile_affinity_limit_le (P Q : SiteProfile) (N : ℕ) :
    profileAffinityLimit P Q≤profileAffinity P Q N :=
  ciInf_le (profile_affinity_bddBelow P Q) N

theorem profile_affinity_tendsto (P Q : SiteProfile) :
    Tendsto (profileAffinity P Q) atTop (𝓝 (profileAffinityLimit P Q)) :=
  tendsto_atTop_ciInf (profile_affinity_antitone P Q) (profile_affinity_bddBelow P Q)

theorem profile_affinity_ratio_tendsto (P Q : SiteProfile)
    (hpos : 0<profileAffinityLimit P Q) :
    Tendsto (fun N => profileAffinityLimit P Q/profileAffinity P Q N) atTop (𝓝 1) := by
  have ht := (tendsto_const_nhds (x := profileAffinityLimit P Q)).div
    (profile_affinity_tendsto P Q) (ne_of_gt hpos)
  rw [div_self (ne_of_gt hpos)] at ht
  convert ht using 1
  rfl

theorem affinity_loss_sum_succ (P Q : SiteProfile) (N : ℕ) :
    affinityLossSum P Q (N+1)=affinityLossSum P Q N+(1-siteAffinity P Q (N+1)) := by
  exact Finset.sum_range_succ _ _

theorem affinity_tail_loss_bound (P Q : SiteProfile) {L N : ℕ} (hLN : L≤N) :
    profileAffinity P Q L-profileAffinity P Q N≤
      profileAffinity P Q L*(affinityLossSum P Q N-affinityLossSum P Q L) := by
  induction N, hLN using Nat.le_induction with
  | base => simp
  | succ N h ih =>
    have hm := mul_le_mul_of_nonneg_right (profile_affinity_antitone P Q h)
      (sub_nonneg.mpr (site_affinity_le_one P Q (N+1)))
    rw [profile_affinity_succ,affinity_loss_sum_succ]
    nlinarith only [ih,hm]

theorem affinity_loss_summable_positive_limit (P Q : SiteProfile)
    (hs : Summable (fun n => 1-siteAffinity P Q n)) :
    0<profileAffinityLimit P Q := by
  have ht : Tendsto (affinityLossSum P Q) atTop (𝓝 (∑' n, (1-siteAffinity P Q n))) := by
    exact hs.hasSum.tendsto_sum_nat.comp (tendsto_add_atTop_nat 1)
  have hc := ht.cauchySeq
  obtain ⟨L,hL⟩ := Metric.cauchySeq_iff'.mp hc (1/2:ℝ) (by norm_num)
  have he : ∀ᶠ N in atTop, profileAffinity P Q L/2≤profileAffinity P Q N := by
    filter_upwards [eventually_ge_atTop L] with N hN
    have hd := hL N hN
    rw [Real.dist_eq] at hd
    have hl : affinityLossSum P Q N-affinityLossSum P Q L<1/2 :=
      lt_of_le_of_lt (le_abs_self _) hd
    have hb := affinity_tail_loss_bound P Q hN
    have hp := profile_affinity_positive P Q L
    nlinarith [mul_pos hp (show 0<1/2-(affinityLossSum P Q N-affinityLossSum P Q L) by linarith)]
  have hb := ge_of_tendsto (profile_affinity_tendsto P Q) he
  exact lt_of_lt_of_le (half_pos (profile_affinity_positive P Q L)) hb

#print axioms profile_affinity_antitone
#print axioms profile_affinity_bddBelow
#print axioms profile_affinity_limit_nonnegative
#print axioms profile_affinity_limit_le
#print axioms profile_affinity_tendsto
#print axioms profile_affinity_ratio_tendsto
#print axioms affinity_loss_sum_succ
#print axioms affinity_tail_loss_bound
#print axioms affinity_loss_summable_positive_limit
end
end ChatgptAudit.Profile026
