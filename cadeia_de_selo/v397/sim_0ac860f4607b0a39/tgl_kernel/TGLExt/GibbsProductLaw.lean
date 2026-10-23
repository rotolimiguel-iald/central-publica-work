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
import TGLExt.GibbsGravityControls

set_option autoImplicit false
set_option maxHeartbeats 10000000
namespace ChatgptAudit.Thermal025
open Matrix Filter Topology Set TGLExt ChatgptAudit.Thermal024
noncomputable section
variable {ι κ : Type} [Fintype ι] [Fintype κ]

omit [Fintype ι] [Fintype κ] in
theorem modular_score_product (p : ι → ℝ) (q : κ → ℝ)
    (hp : ∀ i, 0<p i) (hq : ∀ j, 0<q j) (i : ι) (j : κ) :
    modularScore (productWeights p q) (i,j)=modularScore p i+modularScore q j := by
  unfold modularScore productWeights
  rw [Real.log_mul (ne_of_gt (hp i)) (ne_of_gt (hq j))]
  ring

omit [Fintype ι] [Fintype κ] in
theorem gibbs_atom_product (p : ι → ℝ) (q : κ → ℝ)
    (hp : ∀ i, 0<p i) (hq : ∀ j, 0<q j) (s : ℝ) (i : ι) (j : κ) :
    gibbsAtom (productWeights p q) s (i,j)=gibbsAtom p s i*gibbsAtom q s j := by
  unfold gibbsAtom
  rw [modular_score_product p q hp hq]
  have he : -s*(modularScore p i+modularScore q j)= -s*modularScore p i+-s*modularScore q j := by ring
  rw [he,Real.exp_add]
  unfold productWeights
  ring

theorem gibbs_partition_product (p : ι → ℝ) (q : κ → ℝ)
    (hp : ∀ i, 0<p i) (hq : ∀ j, 0<q j) (s : ℝ) :
    gibbsPartition (productWeights p q) s=gibbsPartition p s*gibbsPartition q s := by
  simp only [gibbsPartition,Fintype.sum_prod_type,gibbs_atom_product p q hp hq,
    ←Finset.mul_sum,←Finset.sum_mul]

theorem gibbs_weights_product (p : ι → ℝ) (q : κ → ℝ)
    (hp : ∀ i, 0<p i) (hq : ∀ j, 0<q j) (s : ℝ) :
    gibbsWeights (productWeights p q) s=productWeights (gibbsWeights p s) (gibbsWeights q s) := by
  funext x
  rcases x with ⟨i,j⟩
  change gibbsAtom (productWeights p q) s (i,j)/gibbsPartition (productWeights p q) s=
    (gibbsAtom p s i/gibbsPartition p s)*(gibbsAtom q s j/gibbsPartition q s)
  rw [gibbs_atom_product p q hp hq,gibbs_partition_product p q hp hq]
  simp only [div_eq_mul_inv,_root_.mul_inv_rev]
  ring

theorem product_expectation_add (p : ι → ℝ) (q : κ → ℝ) (f : ι → ℝ) (g : κ → ℝ)
    (hp : ∑ i, p i=1) (hq : ∑ j, q j=1) :
    (∑ x, productWeights p q x*(f x.1+g x.2))=(∑ i, p i*f i)+(∑ j, q j*g j) := by
  simp only [productWeights,Fintype.sum_prod_type]
  have he : ∀ i j, p i*q j*(f i+g j)=(p i*f i)*q j+p i*(q j*g j) := by
    intro i j
    ring
  simp only [he,Finset.sum_add_distrib,←Finset.mul_sum,←Finset.sum_mul,hp,hq,mul_one,one_mul]

variable [Nonempty ι] [Nonempty κ]

theorem gibbs_product_entropy (p : ι → ℝ) (q : κ → ℝ)
    (hp : ∀ i, 0<p i) (hq : ∀ j, 0<q j) (s : ℝ) :
    finiteEntropy (gibbsWeights (productWeights p q) s)=
      finiteEntropy (gibbsWeights p s)+finiteEntropy (gibbsWeights q s) := by
  rw [gibbs_weights_product p q hp hq]
  exact finiteEntropy_product _ _ (gibbs_weights_normalized p hp s) (gibbs_weights_normalized q hq s)

theorem gibbs_mean_product (p : ι → ℝ) (q : κ → ℝ)
    (hp : ∀ i, 0<p i) (hq : ∀ j, 0<q j) (s : ℝ) :
    gibbsMean (productWeights p q) s=gibbsMean p s+gibbsMean q s := by
  unfold gibbsMean
  rw [gibbs_weights_product p q hp hq]
  have he : (fun x : ι×κ => modularScore (productWeights p q) x)=
      (fun x => modularScore p x.1+modularScore q x.2) := by
    funext x
    exact modular_score_product p q hp hq x.1 x.2
  simp_rw [show ∀ x : ι×κ, modularScore (productWeights p q) x=
    modularScore p x.1+modularScore q x.2 from congrFun he]
  exact product_expectation_add _ _ _ _ (gibbs_weights_normalized p hp s) (gibbs_weights_normalized q hq s)

#print axioms modular_score_product
#print axioms gibbs_atom_product
#print axioms gibbs_partition_product
#print axioms gibbs_weights_product
#print axioms product_expectation_add
#print axioms gibbs_product_entropy
#print axioms gibbs_mean_product
end
end ChatgptAudit.Thermal025
