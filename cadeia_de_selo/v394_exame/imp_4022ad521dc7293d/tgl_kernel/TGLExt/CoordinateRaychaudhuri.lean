-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_010 (05-06/09/2026), transposta em 06/09/2026
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
import TGLExt.VectorCurvatureCommutator

set_option autoImplicit false
set_option maxHeartbeats 3600000
namespace ChatgptAudit
open Matrix Filter Topology
open scoped ContDiff
noncomputable section

theorem sum_three_reverse (f : Fin 4 → Fin 4 → Fin 4 → ℝ) :
    (∑ a, ∑ i, ∑ b, f a i b)=∑ b, ∑ i, ∑ a, f a i b := by
  calc
    _=∑ a, ∑ b, ∑ i, f a i b := by
      apply Finset.sum_congr rfl
      intro a _
      exact Finset.sum_comm
    _=∑ b, ∑ a, ∑ i, f a i b := Finset.sum_comm
    _=∑ b, ∑ i, ∑ a, f a i b := by
      apply Finset.sum_congr rfl
      intro b _
      exact Finset.sum_comm

theorem curvature_vector_contraction (Gamma : ConnectionField4) (x : Coordinate4)
    (v : Coordinate4) (C : Fin 4 → Tensor4)
    (hC : ∀ i j a, C i a j-C j a i=(coordinateCurvature Gamma x i j).mulVec v a) :
    (∑ a, ∑ i, C a a i*v i)-(∑ i, v i*Matrix.trace (C i))=
      tensorQuad (coordinateRicci Gamma x) v := by
  have hs : (∑ i, v i*Matrix.trace (C i))=∑ a, ∑ i, C i a a*v i := by
    simp only [Matrix.trace,Matrix.diag,Finset.mul_sum]
    rw [Finset.sum_comm]
    apply Finset.sum_congr rfl
    intro a _
    apply Finset.sum_congr rfl
    intro i _
    ring
  calc
    _=∑ a, ∑ i, (C a a i-C i a a)*v i := by
      rw [hs,← Finset.sum_sub_distrib]
      apply Finset.sum_congr rfl
      intro a _
      rw [← Finset.sum_sub_distrib]
      apply Finset.sum_congr rfl
      intro i _
      ring
    _=∑ a, ∑ i, (coordinateCurvature Gamma x a i).mulVec v a*v i := by
      simp only [hC]
    _=tensorQuad (coordinateRicci Gamma x) v := by
      simp only [tensorQuad,coordinateRicci,Matrix.mulVec,dotProduct,Finset.sum_mul,Finset.mul_sum]
      rw [sum_three_reverse]
      apply Finset.sum_congr rfl
      intro b _
      apply Finset.sum_congr rfl
      intro i _
      apply Finset.sum_congr rfl
      intro a _
      ring

theorem expansion_of_acceleration (U : Set Coordinate4) (hU : IsOpen U)
    (Gamma : ConnectionField4) (V : VectorField4)
    (hG : SmoothConnectionOn U Gamma) (hV : SmoothVectorOn U V)
    (x : Coordinate4) (hx : x∈U) :
    vectorExpansion Gamma (vectorAcceleration Gamma V) x=
      (∑ a, ∑ i, mixedCovariantDerivative Gamma (covariantVectorGradient Gamma V) x a a i*V x i)+
      Matrix.trace (covariantVectorGradient Gamma V x*covariantVectorGradient Gamma V x) := by
  have hdB := smooth_matrix_differentiableAt U hU _ (covariantVectorGradient_smooth U hU Gamma V hG hV) x hx
  have hdV := smooth_vector_differentiableAt U hU V hV x hx
  change (∑ a, covariantVectorDerivative Gamma
      (fun y => (covariantVectorGradient Gamma V y).mulVec (V y)) x a a)=_
  simp only [covariant_vector_matrix_product Gamma _ V x hdB hdV,Pi.add_apply,Finset.sum_add_distrib]
  congr 1

theorem along_expansion_eq_mixed_trace (U : Set Coordinate4) (hU : IsOpen U)
    (Gamma : ConnectionField4) (V : VectorField4)
    (hG : SmoothConnectionOn U Gamma) (hV : SmoothVectorOn U V)
    (x : Coordinate4) (hx : x∈U) :
    scalarAlong V (vectorExpansion Gamma V) x=
      ∑ i, V x i*Matrix.trace (mixedCovariantDerivative Gamma (covariantVectorGradient Gamma V) x i) := by
  have hdB := smooth_matrix_differentiableAt U hU _ (covariantVectorGradient_smooth U hU Gamma V hG hV) x hx
  unfold scalarAlong vectorExpansion
  simp only [mixed_covariant_trace Gamma _ x hdB]

theorem coordinate_raychaudhuri (U : Set Coordinate4) (hU : IsOpen U)
    (Gamma : ConnectionField4) (V : VectorField4)
    (hG : SmoothConnectionOn U Gamma) (hV : SmoothVectorOn U V)
    (x : Coordinate4) (hx : x∈U) (ht : ∀ i j a, Gamma x i a j=Gamma x j a i) :
    scalarAlong V (vectorExpansion Gamma V) x=
      vectorExpansion Gamma (vectorAcceleration Gamma V) x-
      Matrix.trace (covariantVectorGradient Gamma V x*covariantVectorGradient Gamma V x)-
      tensorQuad (coordinateRicci Gamma x) (V x) := by
  have hc := curvature_vector_contraction Gamma x (V x)
    (mixedCovariantDerivative Gamma (covariantVectorGradient Gamma V) x)
    (mixed_gradient_commutator U hU Gamma V hG hV x hx ht)
  rw [expansion_of_acceleration U hU Gamma V hG hV x hx,
    along_expansion_eq_mixed_trace U hU Gamma V hG hV x hx]
  linarith

theorem vector_expansion_zero_on (U : Set Coordinate4) (hU : IsOpen U)
    (Gamma : ConnectionField4) (V : VectorField4)
    (hz : Set.EqOn V (fun _ => 0) U) (x : Coordinate4) (hx : x∈U) :
    vectorExpansion Gamma V x=0 := by
  have hd (i : Fin 4) : vectorPartial V x i=0 := by
    rw [vectorPartial_congr_on U hU V (fun _ => 0) hz x hx i]
    funext a
    simp [vectorPartial,coordinatePartial]
  simp [vectorExpansion,Matrix.trace,covariantVectorGradient,covariantVectorDerivative,hz hx,hd]

theorem equilibrium_ricci_focusing (U : Set Coordinate4) (hU : IsOpen U)
    (Gamma : ConnectionField4) (V : VectorField4)
    (hG : SmoothConnectionOn U Gamma) (hV : SmoothVectorOn U V)
    (ha : Set.EqOn (vectorAcceleration Gamma V) (fun _ => 0) U)
    (x : Coordinate4) (hx : x∈U) (ht : ∀ i j a, Gamma x i a j=Gamma x j a i)
    (hB : covariantVectorGradient Gamma V x=0) :
    scalarAlong V (vectorExpansion Gamma V) x= -tensorQuad (coordinateRicci Gamma x) (V x) := by
  rw [coordinate_raychaudhuri U hU Gamma V hG hV x hx ht,
    vector_expansion_zero_on U hU Gamma (vectorAcceleration Gamma V) ha x hx,hB]
  simp

#print axioms sum_three_reverse
#print axioms curvature_vector_contraction
#print axioms expansion_of_acceleration
#print axioms along_expansion_eq_mixed_trace
#print axioms coordinate_raychaudhuri
#print axioms vector_expansion_zero_on
#print axioms equilibrium_ricci_focusing
end
end ChatgptAudit
