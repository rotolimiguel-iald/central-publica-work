-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_009 (05-06/09/2026), transposta em 06/09/2026
-- Lote 007..023: habitante GLOBAL periodico da esperanca do centralizador; cauda nao ciclica;
--   obstrucoes de Borchers e da assinatura; e a camada GEOMETRICA GERAL em carta: tensores,
--   conexao de Levi-Civita, curvatura, Bianchi, Einstein geometrico + conservacao, Raychaudhuri,
--   Clausius local <=> balanco nulo de Ricci, telas/congruencias nulas construidas, area e calor,
--   entropia relativa, dinamica unitaria, covetor de materia. Estatuto [REAL / INPUT / OPEN]:
--   Clausius, a metrica lorentziana, H3 dinamico, assinatura e globalizacao seguem INPUT/OPEN.
-- Auditoria da gerencia (sessao d554e796, 06/09/2026): hashes 100% nas 17 entregas; 17/17
--   auditores da bancada exit 0; recompilacao INDEPENDENTE 116/116 exit 0, todos os axiomas no
--   trio [propext, Classical.choice, Quot.sound]; zero sorry/warning; enunciados lidos.
-- Transposicao MECANICA: este cabecalho + prefixo TGLExt. nos imports; nada mais.
-- NAO move gate; nao e fisica; NOT_FALSIFIED nunca e CONFIRMED; CONFIRMADA proibido.
-- ---------------------------------------------------------------------
import TGLExt.CovariantCurvatureBianchi

set_option autoImplicit false
set_option maxHeartbeats 2400000
namespace ChatgptAudit
open Matrix
open scoped ContDiff
noncomputable section

def ricciDerivativeContraction (gInv : Matrix (Fin 4) (Fin 4) ℝ)
    (Q : Fin 4 → Fin 4 → Fin 4 → Fin 4 → Fin 4 → ℝ) (k b j : Fin 4) : ℝ :=
  ∑ a, ∑ c, gInv a c*Q k c b a j

theorem sum_four_exchange_pairs (f : Fin 4 → Fin 4 → Fin 4 → Fin 4 → ℝ) :
    (∑ i, ∑ j, ∑ k, ∑ l, f i j k l)=∑ k, ∑ l, ∑ i, ∑ j, f i j k l := by
  let F : (Fin 4 × Fin 4) → (Fin 4 × Fin 4) → ℝ := fun p q => f p.1 p.2 q.1 q.2
  have he : (∑ p : Fin 4 × Fin 4, ∑ q : Fin 4 × Fin 4, F p q)=
      ∑ q : Fin 4 × Fin 4, ∑ p : Fin 4 × Fin 4, F p q := Finset.sum_comm
  simpa only [F,Fintype.sum_prod_type] using he

theorem contracted_bianchi_algebra (gInv : Matrix (Fin 4) (Fin 4) ℝ)
    (Q : Fin 4 → Fin 4 → Fin 4 → Fin 4 → Fin 4 → ℝ)
    (hfirst : ∀ k a b i j, Q k a b i j= -Q k b a i j)
    (hlast : ∀ k a b i j, Q k a b i j= -Q k a b j i)
    (hcyclic : ∀ a b i j k, Q i a b j k+Q j a b k i+Q k a b i j=0) (j : Fin 4) :
    2*(∑ i, ∑ k, gInv i k*ricciDerivativeContraction gInv Q i k j)=
      ∑ i, ∑ k, gInv i k*ricciDerivativeContraction gInv Q j k i := by
  have hz : (∑ i, ∑ k, ∑ a, ∑ c, gInv i k*gInv a c*
      (Q i c k a j+Q a c k j i+Q j c k i a))=0 := by
    apply Finset.sum_eq_zero
    intro i hi
    apply Finset.sum_eq_zero
    intro k hk
    apply Finset.sum_eq_zero
    intro a ha
    apply Finset.sum_eq_zero
    intro c hc
    rw [hcyclic c k i a j,mul_zero]
  have ht : (∑ i, ∑ k, ∑ a, ∑ c, gInv i k*gInv a c*Q a c k j i)=
      ∑ i, ∑ k, ∑ a, ∑ c, gInv i k*gInv a c*Q i c k a j := by
    rw [sum_four_exchange_pairs]
    apply Finset.sum_congr rfl
    intro i hi
    apply Finset.sum_congr rfl
    intro k hk
    apply Finset.sum_congr rfl
    intro a ha
    apply Finset.sum_congr rfl
    intro c hc
    rw [hfirst i k c j a,hlast i c k j a,neg_neg]
    ring
  have hn : (∑ i, ∑ k, ∑ a, ∑ c, gInv i k*gInv a c*Q j c k i a)=
      -(∑ i, ∑ k, ∑ a, ∑ c, gInv i k*gInv a c*Q j c k a i) := by
    simp only [← Finset.sum_neg_distrib]
    apply Finset.sum_congr rfl
    intro i hi
    apply Finset.sum_congr rfl
    intro k hk
    apply Finset.sum_congr rfl
    intro a ha
    apply Finset.sum_congr rfl
    intro c hc
    rw [hlast j c k i a,mul_neg]
  simp only [mul_add,Finset.sum_add_distrib] at hz
  rw [ht,hn] at hz
  have hL : (∑ i, ∑ k, gInv i k*ricciDerivativeContraction gInv Q i k j)=
      ∑ i, ∑ k, ∑ a, ∑ c, gInv i k*gInv a c*Q i c k a j := by
    simp only [ricciDerivativeContraction,Finset.mul_sum,← mul_assoc]
  have hR : (∑ i, ∑ k, gInv i k*ricciDerivativeContraction gInv Q j k i)=
      ∑ i, ∑ k, ∑ a, ∑ c, gInv i k*gInv a c*Q j c k a i := by
    simp only [ricciDerivativeContraction,Finset.mul_sum,← mul_assoc]
  rw [hL,hR]
  linarith

theorem coordinate_ricci_smooth (U : Set Coordinate4) (hU : IsOpen U)
    (Gamma : ConnectionField4) (hG : SmoothConnectionOn U Gamma) :
    SmoothMatrixOn U (coordinateRicci Gamma) := by
  have hc : ∀ i j a b, ContDiffOn ℝ ∞ (fun x => coordinateCurvature Gamma x i j a b) U :=
    fun i j => coordinate_curvature_smooth U hU Gamma hG i j
  intro b j
  unfold coordinateRicci
  fun_prop

theorem ricci_derivative_trace (U : Set Coordinate4) (hU : IsOpen U)
    (Gamma : ConnectionField4) (hG : SmoothConnectionOn U Gamma)
    (x : Coordinate4) (hx : x∈U) (k b j : Fin 4) :
    tensorFieldJet (coordinateRicci Gamma) x k b j=
      ∑ a, tensorFieldJet (fun y => coordinateCurvature Gamma y a j) x k a b := by
  change coordinatePartial (fun y => ∑ a, coordinateCurvature Gamma y a j a b) x k = _
  exact coordinatePartial_sum (fun a y => coordinateCurvature Gamma y a j a b) x
    (fun a => smooth_matrix_differentiableAt U hU _ (coordinate_curvature_smooth U hU Gamma hG a j) x hx a b) k

theorem covariant_ricci_contraction (U : Set Coordinate4) (hU : IsOpen U)
    (Gamma : ConnectionField4) (hG : SmoothConnectionOn U Gamma)
    (x : Coordinate4) (hx : x∈U) (k b j : Fin 4) :
    (∑ a, covariantCurvatureDerivative Gamma x k a j a b)=
      covariantTensorJet (coordinateRicci Gamma x) (tensorFieldJet (coordinateRicci Gamma) x) (Gamma x) k b j := by
  have hs : (∑ a, ∑ l, Gamma x k a l*coordinateCurvature Gamma x a j l b)=
      ∑ a, ∑ l, Gamma x k l a*coordinateCurvature Gamma x l j a b := Finset.sum_comm
  have hB : (∑ a, ∑ l, coordinateCurvature Gamma x a j a l*Gamma x k l b)=
      ∑ l, Gamma x k l b*(∑ a, coordinateCurvature Gamma x a j a l) := by
    rw [Finset.sum_comm]
    apply Finset.sum_congr rfl
    intro l hl
    rw [Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro a ha
    ring
  have hC : (∑ a, ∑ l, Gamma x k l j*coordinateCurvature Gamma x a l a b)=
      ∑ l, (∑ a, coordinateCurvature Gamma x a l a b)*Gamma x k l j := by
    rw [Finset.sum_comm]
    apply Finset.sum_congr rfl
    intro l hl
    rw [Finset.sum_mul]
    apply Finset.sum_congr rfl
    intro a ha
    ring
  simp only [covariantCurvatureDerivative,exteriorCovariantCurvatureDerivative,
    Matrix.sub_apply,Matrix.add_apply,Matrix.mul_apply,Matrix.sum_apply,Matrix.smul_apply,smul_eq_mul,
    Finset.sum_add_distrib,Finset.sum_sub_distrib,covariantTensorJet,
    ricci_derivative_trace U hU Gamma hG x hx,Matrix.transpose_apply,coordinateRicci]
  rw [hs,hB,hC]
  ring

theorem lower_covariant_ricci_contraction (U : Set Coordinate4) (hU : IsOpen U)
    (g gInv : TensorField4) (Gamma : ConnectionField4) (hG : SmoothConnectionOn U Gamma)
    (x : Coordinate4) (hx : x∈U) (hinv : gInv x*g x=1) (k b j : Fin 4) :
    covariantTensorJet (coordinateRicci Gamma x) (tensorFieldJet (coordinateRicci Gamma) x) (Gamma x) k b j=
      ricciDerivativeContraction (gInv x) (lowerCovariantCurvatureDerivative g Gamma x) k b j := by
  rw [← covariant_ricci_contraction U hU Gamma hG x hx k b j]
  unfold ricciDerivativeContraction
  apply Finset.sum_congr rfl
  intro a ha
  change covariantCurvatureDerivative Gamma x k a j a b =
    (gInv x*(g x*covariantCurvatureDerivative Gamma x k a j)) a b
  rw [← Matrix.mul_assoc,hinv,one_mul]

#print axioms sum_four_exchange_pairs
#print axioms contracted_bianchi_algebra
#print axioms coordinate_ricci_smooth
#print axioms ricci_derivative_trace
#print axioms covariant_ricci_contraction
#print axioms lower_covariant_ricci_contraction
end
end ChatgptAudit
