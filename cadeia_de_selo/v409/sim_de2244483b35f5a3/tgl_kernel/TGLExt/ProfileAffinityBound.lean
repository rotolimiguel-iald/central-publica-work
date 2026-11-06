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
import TGLExt.GlobalProfileFaithfulness
import Mathlib.Analysis.PSeries

set_option autoImplicit false
set_option maxHeartbeats 16000000
namespace ChatgptAudit.Profile026
open Matrix Filter Topology Set TGLExt ChatgptAudit.Thermal025
noncomputable section

theorem sqrt_difference_square_bound (p q : ℝ) (hp : 0<p) (hq : 0≤q) :
    (Real.sqrt p-Real.sqrt q)^2≤(p-q)^2/p := by
  have he : (Real.sqrt p-Real.sqrt q)^2*(Real.sqrt p+Real.sqrt q)^2=(p-q)^2 := by
    calc
      _=((Real.sqrt p)^2-(Real.sqrt q)^2)^2 := by ring
      _=_ := by rw [Real.sq_sqrt hp.le,Real.sq_sqrt hq]
  have hb : p≤(Real.sqrt p+Real.sqrt q)^2 := by
    nlinarith [Real.sq_sqrt hp.le,Real.sq_sqrt hq,
      mul_nonneg (Real.sqrt_nonneg p) (Real.sqrt_nonneg q)]
  apply (le_div_iff₀ hp).mpr
  calc
    _≤(Real.sqrt p-Real.sqrt q)^2*(Real.sqrt p+Real.sqrt q)^2 :=
      mul_le_mul_of_nonneg_left hb (sq_nonneg _)
    _=_ := he

theorem binary_affinity_quadratic_bound (p q : ℝ) (hp0 : 0<p) (hp1 : p<1)
    (hq0 : 0<q) (hq1 : q<1) :
    1-diagonalAffinity (siteW p) (siteW q)≤
      (p-q)^2*(1/(2*p)+1/(2*(1-p))) := by
  have h0 := sqrt_difference_square_bound p q hp0 hq0.le
  have h1 := sqrt_difference_square_bound (1-p) (1-q) (by linarith) (by linarith)
  rw [show (1-p-(1-q))^2=(p-q)^2 by ring] at h1
  have hh := hellinger_sum_identity (siteW p) (siteW q)
    (fun i => (siteW_pos hp0 hp1 i).le) (fun i => (siteW_pos hq0 hq1 i).le)
    (siteW_sum p) (siteW_sum q)
  simp only [Fin.sum_univ_two,siteW,Fin.reduceEq,if_true,if_false] at hh
  calc
    1-diagonalAffinity (siteW p) (siteW q)=
      ((Real.sqrt p-Real.sqrt q)^2+(Real.sqrt (1-p)-Real.sqrt (1-q))^2)/2 := by linarith
    _≤((p-q)^2/p+(p-q)^2/(1-p))/2 :=
      div_le_div_of_nonneg_right (add_le_add h0 h1) (by norm_num)
    _=_ := by field_simp

theorem binary_third_affinity_bound (q : ℝ) (hq0 : 0<q) (hq1 : q<1) :
    1-diagonalAffinity (siteW (1/3)) (siteW q)≤(9/4)*(1/3-q)^2 := by
  have hh := binary_affinity_quadratic_bound (1/3) q (by norm_num) (by norm_num) hq0 hq1
  norm_num at hh
  nlinarith only [hh]

theorem profile_weighted_square_summable_positive (P Q : SiteProfile)
    (hs : Summable (fun n => (P.w n-Q.w n)^2*(1/(2*P.w n)+1/(2*(1-P.w n))))) :
    0<profileAffinityLimit P Q := by
  apply affinity_loss_summable_positive_limit P Q
  apply Summable.of_nonneg_of_le (fun n => sub_nonneg.mpr (site_affinity_le_one P Q n)) _ hs
  intro n
  exact binary_affinity_quadratic_bound _ _ (P.pos n) (P.lt_one n) (Q.pos n) (Q.lt_one n)

theorem profile_square_summable_positive (P Q : SiteProfile) (c : ℝ)
    (hb : ∀ n, 1-siteAffinity P Q n≤c*(P.w n-Q.w n)^2)
    (hs : Summable (fun n => (P.w n-Q.w n)^2)) :
    0<profileAffinityLimit P Q := by
  apply affinity_loss_summable_positive_limit P Q
  exact Summable.of_nonneg_of_le (fun n => sub_nonneg.mpr (site_affinity_le_one P Q n))
    hb (hs.mul_left c)

#print axioms sqrt_difference_square_bound
#print axioms binary_affinity_quadratic_bound
#print axioms binary_third_affinity_bound
#print axioms profile_weighted_square_summable_positive
#print axioms profile_square_summable_positive
end
end ChatgptAudit.Profile026
