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
import TGLExt.RelativeProfilePreparation

set_option autoImplicit false
set_option maxHeartbeats 16000000
namespace ChatgptAudit.Profile026
open Matrix Filter Topology Set TGLExt ChatgptAudit.Thermal024 ChatgptAudit.Thermal025
open scoped ComplexOrder Kronecker
noncomputable section

def siteAffinity (P Q : SiteProfile) (n : ℕ) : ℝ :=
  diagonalAffinity (siteW (P.w n)) (siteW (Q.w n))
def profileAffinity (P Q : SiteProfile) (N : ℕ) : ℝ :=
  diagonalAffinity (towerW P N) (towerW Q N)

theorem site_affinity_positive (P Q : SiteProfile) (n : ℕ) : 0<siteAffinity P Q n :=
  diagonal_affinity_positive _ _ (siteW_pos (P.pos n) (P.lt_one n))
    (siteW_pos (Q.pos n) (Q.lt_one n))

theorem site_affinity_le_one (P Q : SiteProfile) (n : ℕ) : siteAffinity P Q n≤1 :=
  diagonal_affinity_le_one _ _ (fun i => (siteW_pos (P.pos n) (P.lt_one n) i).le)
    (fun i => (siteW_pos (Q.pos n) (Q.lt_one n) i).le) (siteW_sum _) (siteW_sum _)

theorem profile_affinity_positive (P Q : SiteProfile) (N : ℕ) : 0<profileAffinity P Q N :=
  diagonal_affinity_positive _ _ (towerW_pos P N) (towerW_pos Q N)

theorem profile_affinity_le_one (P Q : SiteProfile) (N : ℕ) : profileAffinity P Q N≤1 :=
  diagonal_affinity_le_one _ _ (fun i => (towerW_pos P N i).le)
    (fun i => (towerW_pos Q N i).le) (towerW_sum P N) (towerW_sum Q N)

theorem profile_affinity_succ (P Q : SiteProfile) (N : ℕ) :
    profileAffinity P Q (N+1)=profileAffinity P Q N*siteAffinity P Q (N+1) :=
  diagonal_affinity_product _ _ _ _ (fun i => (towerW_pos P N i).le)
    (fun i => (towerW_pos Q N i).le)

theorem profile_affinity_product (P Q : SiteProfile) (N : ℕ) :
    profileAffinity P Q N=∏ n ∈ Finset.range (N+1), siteAffinity P Q n := by
  induction N with
  | zero => simp [profileAffinity,siteAffinity,towerW]
  | succ N ih => rw [profile_affinity_succ,Finset.prod_range_succ,ih]

theorem relative_trace {ι : Type} [Fintype ι] [DecidableEq ι]
    (p q : ι → ℝ) (hp : ∀ i, 0<p i) (hq : ∀ i, 0≤q i) :
    (∑ i, (p i:ℂ)*(relativeFilter p q) i i)=(diagonalAffinity p q:ℂ) := by
  simp only [relativeFilter,Matrix.diagonal_apply_eq,←Complex.ofReal_mul,
    weighted_sqrt_ratio _ _ (hp _) (hq _),←Complex.ofReal_sum,diagonalAffinity]

theorem profile_filter_step (P Q : SiteProfile) (N : ℕ) :
    relativeFilter (towerW P (N+1)) (towerW Q (N+1))=
      (relativeFilter (towerW P N) (towerW Q N)) ⊗ₖ
        (relativeFilter (siteW (P.w (N+1))) (siteW (Q.w (N+1)))) :=
  relative_filter_product _ _ _ _ (towerW_pos P N) (fun i => (towerW_pos Q N i).le)

theorem profile_trace_step (P Q : SiteProfile) (N : ℕ)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    tState P (N+1) (towerStep a*relativeFilter (towerW P (N+1)) (towerW Q (N+1)))=
      tState P N (a*relativeFilter (towerW P N) (towerW Q N))*(siteAffinity P Q (N+1):ℂ) := by
  rw [profile_filter_step]
  unfold towerStep
  rw [←Matrix.mul_kronecker_mul,one_mul,tState_kron_split,
    relative_trace _ _ (siteW_pos (P.pos _) (P.lt_one _))
      (fun i => (siteW_pos (Q.pos _) (Q.lt_one _) i).le)]
  rfl

theorem profile_trace_push (P Q : SiteProfile) {L N : ℕ} (hLN : L≤N)
    (a : Matrix (chainIdx L) (chainIdx L) ℂ) :
    tState P N (tPush hLN a*relativeFilter (towerW P N) (towerW Q N))=
      tState P L (a*relativeFilter (towerW P L) (towerW Q L))*
        ((profileAffinity P Q N/profileAffinity P Q L:ℝ):ℂ) := by
  induction N, hLN using Nat.le_induction with
  | base =>
    rw [tPush_self,div_self (ne_of_gt (profile_affinity_positive P Q L)),Complex.ofReal_one,mul_one]
  | succ N h ih =>
    rw [tPush_succ h (Nat.le_succ_of_le h),profile_trace_step,ih,profile_affinity_succ]
    push_cast
    ring

theorem profile_filter_square_state (P Q : SiteProfile) (N : ℕ) :
    tState P N (relativeFilter (towerW P N) (towerW Q N)*
      relativeFilter (towerW P N) (towerW Q N))=1 := by
  have h := relative_filter_local_state (towerW P N) (towerW Q N) (towerW_pos P N)
    (fun i => (towerW_pos Q N i).le) 1
  simpa only [relative_filter_self_adjoint,mul_one,tState,Matrix.one_apply_eq,
    ←Complex.ofReal_sum,towerW_sum,Complex.ofReal_one] using h

theorem profile_vectors_overlap (P Q : SiteProfile) {L N : ℕ} (hLN : L≤N) :
    inner ℂ (profileVector P Q L) (profileVector P Q N)=
      ((profileAffinity P Q N/profileAffinity P Q L:ℝ):ℂ) := by
  unfold profileVector
  rw [tower_local_vectors_inner P hLN,tInner,←tPush_star,relative_filter_self_adjoint,
    profile_trace_push,profile_filter_square_state,one_mul]

theorem profile_vectors_distance (P Q : SiteProfile) {L N : ℕ} (hLN : L≤N) :
    ‖profileVector P Q L-profileVector P Q N‖^2=
      2-2*(profileAffinity P Q N/profileAffinity P Q L) := by
  rw [norm_sub_sq (𝕜 := ℂ),profile_vector_norm,profile_vector_norm,profile_vectors_overlap P Q hLN]
  change (1:ℝ)^2-2*(profileAffinity P Q N/profileAffinity P Q L)+1^2=_
  ring

theorem profile_inverse_overlap (P Q : SiteProfile) {L N : ℕ} (hLN : L≤N) :
    inner ℂ (hOmega P)
      (towerPi P (relativeFilter (towerW Q L) (towerW P L)) (profileVector P Q N))=
        ((profileAffinity P Q N/profileAffinity P Q L:ℝ):ℂ) := by
  unfold profileVector
  rw [←towerPi_compat hLN (relativeFilter (towerW Q L) (towerW P L)),
    ←mul_apply_eq_comp,←towerPi_mul]
  change omegaState P (towerPi P _)=_
  rw [omegaState_pi,profile_trace_push,relative_filter_reverse _ _ (towerW_pos Q L) (towerW_pos P L),
    tState_one,one_mul]

#print axioms site_affinity_positive
#print axioms site_affinity_le_one
#print axioms profile_affinity_positive
#print axioms profile_affinity_le_one
#print axioms profile_affinity_succ
#print axioms profile_affinity_product
#print axioms relative_trace
#print axioms profile_filter_step
#print axioms profile_trace_step
#print axioms profile_trace_push
#print axioms profile_filter_square_state
#print axioms profile_vectors_overlap
#print axioms profile_vectors_distance
#print axioms profile_inverse_overlap
end
end ChatgptAudit.Profile026
