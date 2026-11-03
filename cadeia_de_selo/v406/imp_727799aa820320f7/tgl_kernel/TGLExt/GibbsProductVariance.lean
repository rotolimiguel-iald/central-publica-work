-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_025 (06/09/2026), transposta em 06/09/2026
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
import TGLExt.GibbsProductLaw

set_option autoImplicit false
set_option maxHeartbeats 12000000
namespace ChatgptAudit.Thermal025
open Matrix Filter Topology Set TGLExt ChatgptAudit.Thermal024
noncomputable section
variable {ι κ : Type} [Fintype ι] [Fintype κ]

theorem modular_mean_product (p : ι → ℝ) (q : κ → ℝ)
    (hp : ∀ i, 0<p i) (hq : ∀ j, 0<q j) (hs : ∑ i, p i=1) (ht : ∑ j, q j=1) :
    modularMean (productWeights p q)=modularMean p+modularMean q := by
  have he : modularScore (productWeights p q)=(fun x => modularScore p x.1+modularScore q x.2) := by
    funext x
    exact modular_score_product p q hp hq x.1 x.2
  unfold modularMean
  rw [he]
  exact product_expectation_add p q _ _ hs ht

theorem product_second_moment (p : ι → ℝ) (q : κ → ℝ) (f : ι → ℝ) (g : κ → ℝ)
    (hp : ∑ i, p i=1) (hq : ∑ j, q j=1) :
    (∑ x, productWeights p q x*(f x.1+g x.2)^2)=
      (∑ i, p i*(f i)^2)+(∑ j, q j*(g j)^2)+2*(∑ i, p i*f i)*(∑ j, q j*g j) := by
  simp only [productWeights,Fintype.sum_prod_type]
  have he : ∀ i j, p i*q j*(f i+g j)^2=
      (p i*(f i)^2)*q j+p i*(q j*(g j)^2)+2*(p i*f i)*(q j*g j) := by
    intro i j
    ring
  simp only [he,Finset.sum_add_distrib,←Finset.mul_sum,←Finset.sum_mul,hp,hq,mul_one,one_mul]

theorem modular_variance_product (p : ι → ℝ) (q : κ → ℝ)
    (hp : ∀ i, 0<p i) (hq : ∀ j, 0<q j) (hs : ∑ i, p i=1) (ht : ∑ j, q j=1) :
    modularVariance (productWeights p q)=modularVariance p+modularVariance q := by
  rw [modular_variance_second_moment _ (product_weights_sum p q hs ht),
    modular_mean_product p q hp hq hs ht,
    modular_variance_second_moment p hs,modular_variance_second_moment q ht]
  have he : modularScore (productWeights p q)=(fun x => modularScore p x.1+modularScore q x.2) := by
    funext x
    exact modular_score_product p q hp hq x.1 x.2
  rw [he,product_second_moment p q _ _ hs ht]
  unfold modularMean
  ring

theorem tower_variance_zero (P : SiteProfile) :
    modularVariance (towerW P 0)=modularVariance (siteW (P.w 0)) := rfl

theorem tower_variance_succ (P : SiteProfile) (N : ℕ) :
    modularVariance (towerW P (N+1))=
      modularVariance (towerW P N)+modularVariance (siteW (P.w (N+1))) := by
  change modularVariance (productWeights (towerW P N) (siteW (P.w (N+1))))=_
  exact modular_variance_product _ _ (towerW_pos P N) (siteW_pos (P.pos _) (P.lt_one _))
    (towerW_sum P N) (siteW_sum _)

theorem tower_variance_sum (P : SiteProfile) (N : ℕ) :
    modularVariance (towerW P N)=∑ n∈Finset.range (N+1), modularVariance (siteW (P.w n)) := by
  induction N with
  | zero =>
    rw [Finset.sum_range_succ,Finset.sum_range_zero,zero_add]
    exact tower_variance_zero P
  | succ N ih => rw [tower_variance_succ,Finset.sum_range_succ,ih]

theorem tower_variance_uniform (P : SiteProfile) (q : ℝ) (hP : ∀ n, P.w n=q) (N : ℕ) :
    modularVariance (towerW P N)=((N:ℝ)+1)*modularVariance (siteW q) := by
  rw [tower_variance_sum]
  simp only [hP,Finset.sum_const,Finset.card_range,nsmul_eq_mul,Nat.cast_add,Nat.cast_one]

#print axioms modular_mean_product
#print axioms product_second_moment
#print axioms modular_variance_product
#print axioms tower_variance_zero
#print axioms tower_variance_succ
#print axioms tower_variance_sum
#print axioms tower_variance_uniform
end
end ChatgptAudit.Thermal025
