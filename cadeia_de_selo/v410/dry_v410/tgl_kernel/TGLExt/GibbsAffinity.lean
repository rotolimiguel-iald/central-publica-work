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
import TGLExt.TowerThermalProfile

set_option autoImplicit false
set_option maxHeartbeats 14000000
namespace ChatgptAudit.Thermal025
open Matrix Filter Topology Set TGLExt ChatgptAudit.Thermal024
noncomputable section
variable {ι κ : Type} [Fintype ι] [Fintype κ]

def diagonalAffinity (p q : ι → ℝ) : ℝ := ∑ i, Real.sqrt (p i)*Real.sqrt (q i)
def gibbsAffinity (p : ι → ℝ) (s : ℝ) : ℝ := diagonalAffinity p (gibbsWeights p s)

theorem diagonal_affinity_self (p : ι → ℝ) (hp : ∀ i, 0≤p i) (hs : ∑ i, p i=1) :
    diagonalAffinity p p=1 := by
  simp only [diagonalAffinity,Real.mul_self_sqrt (hp _),hs]

theorem hellinger_sum_identity (p q : ι → ℝ) (hp : ∀ i, 0≤p i) (hq : ∀ i, 0≤q i)
    (hs : ∑ i, p i=1) (ht : ∑ i, q i=1) :
    (∑ i, (Real.sqrt (p i)-Real.sqrt (q i))^2)=2-2*diagonalAffinity p q := by
  have he : ∀ i, (Real.sqrt (p i)-Real.sqrt (q i))^2=
      p i+q i-2*(Real.sqrt (p i)*Real.sqrt (q i)) := by
    intro i
    nlinarith only [Real.sq_sqrt (hp i),Real.sq_sqrt (hq i)]
  simp only [he,Finset.sum_sub_distrib,Finset.sum_add_distrib,←Finset.mul_sum,hs,ht,diagonalAffinity]
  ring

theorem diagonal_affinity_le_one (p q : ι → ℝ) (hp : ∀ i, 0≤p i) (hq : ∀ i, 0≤q i)
    (hs : ∑ i, p i=1) (ht : ∑ i, q i=1) : diagonalAffinity p q≤1 := by
  have hn : 0≤∑ i, (Real.sqrt (p i)-Real.sqrt (q i))^2 := Finset.sum_nonneg (fun i _ => sq_nonneg _)
  rw [hellinger_sum_identity p q hp hq hs ht] at hn
  linarith

theorem diagonal_affinity_eq_one_iff (p q : ι → ℝ) (hp : ∀ i, 0≤p i) (hq : ∀ i, 0≤q i)
    (hs : ∑ i, p i=1) (ht : ∑ i, q i=1) : diagonalAffinity p q=1 ↔ p=q := by
  constructor
  · intro he
    have hz : (∑ i, (Real.sqrt (p i)-Real.sqrt (q i))^2)=0 := by
      rw [hellinger_sum_identity p q hp hq hs ht,he]
      ring
    have hall := (Finset.sum_eq_zero_iff_of_nonneg (fun i _ => sq_nonneg (Real.sqrt (p i)-Real.sqrt (q i)))).mp hz
    funext i
    have hi := hall i (Finset.mem_univ i)
    exact (Real.sqrt_inj (hp i) (hq i)).mp (sub_eq_zero.mp (sq_eq_zero_iff.mp hi))
  · rintro rfl
    exact diagonal_affinity_self p hp hs

theorem diagonal_affinity_product (p r : ι → ℝ) (q z : κ → ℝ)
    (hp : ∀ i, 0≤p i) (hr : ∀ i, 0≤r i) :
    diagonalAffinity (productWeights p q) (productWeights r z)=diagonalAffinity p r*diagonalAffinity q z := by
  simp only [diagonalAffinity,productWeights,Fintype.sum_prod_type,Real.sqrt_mul (hp _),Real.sqrt_mul (hr _)]
  have he : ∀ i j, (Real.sqrt (p i)*Real.sqrt (q j))*(Real.sqrt (r i)*Real.sqrt (z j))=
      (Real.sqrt (p i)*Real.sqrt (r i))*(Real.sqrt (q j)*Real.sqrt (z j)) := by
    intro i j
    ring
  simp only [he,←Finset.mul_sum,←Finset.sum_mul]

omit [Fintype ι] [Fintype κ] in
theorem weighted_sqrt_ratio (p r : ℝ) (hp : 0<p) (hr : 0≤r) :
    p*Real.sqrt (r/p)=Real.sqrt p*Real.sqrt r := by
  rw [Real.sqrt_div hr p,←mul_div_assoc]
  apply (div_eq_iff (ne_of_gt (Real.sqrt_pos.mpr hp))).mpr
  calc
    p*Real.sqrt r=(Real.sqrt p*Real.sqrt p)*Real.sqrt r := by rw [Real.mul_self_sqrt (le_of_lt hp)]
    _=(Real.sqrt p*Real.sqrt r)*Real.sqrt p := by ring

variable [Nonempty ι]

theorem diagonal_affinity_positive (p q : ι → ℝ) (hp : ∀ i, 0<p i) (hq : ∀ i, 0<q i) :
    0<diagonalAffinity p q :=
  Finset.sum_pos (fun i _ => mul_pos (Real.sqrt_pos.mpr (hp i)) (Real.sqrt_pos.mpr (hq i))) Finset.univ_nonempty

theorem gibbs_fixed_iff_tracial (p : ι → ℝ) (hp : ∀ i, 0<p i) (hs : ∑ i, p i=1)
    (s : ℝ) (hS : s≠0) : gibbsWeights p s=p ↔ ∀ i j, p i=p j := by
  constructor
  · intro hf i j
    have hi := gibbs_log_weights p hp s i
    have hj := gibbs_log_weights p hp s j
    rw [hf] at hi hj
    have hz : s*(modularScore p i-modularScore p j)=0 := by
      unfold modularScore at *
      nlinarith only [hi,hj]
    have he := sub_eq_zero.mp ((mul_eq_zero.mp hz).resolve_left hS)
    apply Real.log_injOn_pos (hp i) (hp j)
    unfold modularScore at he
    linarith only [he]
  · intro ht
    exact funext (gibbs_weights_tracial p hs ht s)

theorem gibbs_affinity_positive (p : ι → ℝ) (hp : ∀ i, 0<p i) (s : ℝ) :
    0<gibbsAffinity p s :=
  diagonal_affinity_positive p _ hp (gibbs_weights_positive p hp s)

theorem gibbs_affinity_lt_one (p : ι → ℝ) (hp : ∀ i, 0<p i) (hs : ∑ i, p i=1)
    (s : ℝ) (hS : s≠0) (hn : ∃ i j, p i≠p j) : gibbsAffinity p s<1 := by
  have hle := diagonal_affinity_le_one p (gibbsWeights p s) (fun i => (hp i).le)
    (fun i => (gibbs_weights_positive p hp s i).le) hs (gibbs_weights_normalized p hp s)
  apply lt_of_le_of_ne hle
  intro he
  have hf := (diagonal_affinity_eq_one_iff p (gibbsWeights p s) (fun i => (hp i).le)
    (fun i => (gibbs_weights_positive p hp s i).le) hs (gibbs_weights_normalized p hp s)).mp he
  obtain ⟨i,j,hij⟩ := hn
  exact hij ((gibbs_fixed_iff_tracial p hp hs s hS).mp hf.symm i j)

theorem gibbs_filter_affinity (p : ι → ℝ) (hp : ∀ i, 0<p i) (s : ℝ) :
    (∑ i, p i*Real.sqrt (gibbsWeights p s i/p i))=gibbsAffinity p s := by
  apply Finset.sum_congr rfl
  intro i _
  exact weighted_sqrt_ratio (p i) _ (hp i) (gibbs_weights_positive p hp s i).le

theorem gibbs_affinity_product (p : ι → ℝ) (q : κ → ℝ)
    (hp : ∀ i, 0<p i) (hq : ∀ j, 0<q j) (s : ℝ) :
    gibbsAffinity (productWeights p q) s=gibbsAffinity p s*gibbsAffinity q s := by
  unfold gibbsAffinity
  rw [gibbs_weights_product p q hp hq]
  exact diagonal_affinity_product p _ q _ (fun i => (hp i).le)
    (fun i => (gibbs_weights_positive p hp s i).le)

theorem gibbs_amplitude_product (p : ι → ℝ) (q : κ → ℝ)
    (hp : ∀ i, 0<p i) (hq : ∀ j, 0<q j) (s : ℝ) (i : ι) (j : κ) :
    Real.sqrt (gibbsWeights (productWeights p q) s (i,j)/productWeights p q (i,j))=
      Real.sqrt (gibbsWeights p s i/p i)*Real.sqrt (gibbsWeights q s j/q j) := by
  rw [gibbs_weights_product p q hp hq]
  have he : productWeights (gibbsWeights p s) (gibbsWeights q s) (i,j)/productWeights p q (i,j)=
      (gibbsWeights p s i/p i)*(gibbsWeights q s j/q j) := by
    unfold productWeights
    field_simp [ne_of_gt (hp i),ne_of_gt (hq j)]
  rw [he,Real.sqrt_mul (le_of_lt (div_pos (gibbs_weights_positive p hp s i) (hp i)))]

#print axioms diagonal_affinity_self
#print axioms hellinger_sum_identity
#print axioms diagonal_affinity_le_one
#print axioms diagonal_affinity_eq_one_iff
#print axioms diagonal_affinity_product
#print axioms weighted_sqrt_ratio
#print axioms diagonal_affinity_positive
#print axioms gibbs_fixed_iff_tracial
#print axioms gibbs_affinity_positive
#print axioms gibbs_affinity_lt_one
#print axioms gibbs_filter_affinity
#print axioms gibbs_affinity_product
#print axioms gibbs_amplitude_product
end
end ChatgptAudit.Thermal025
