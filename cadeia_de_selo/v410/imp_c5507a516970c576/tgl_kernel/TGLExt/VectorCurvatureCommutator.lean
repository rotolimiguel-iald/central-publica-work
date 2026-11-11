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
import TGLExt.CovariantVectorCalculus

set_option autoImplicit false
set_option maxHeartbeats 2400000
namespace ChatgptAudit
open Matrix Filter Topology
open scoped ContDiff
noncomputable section

theorem covariant_vector_commutator (U : Set Coordinate4) (hU : IsOpen U)
    (Gamma : ConnectionField4) (V : VectorField4)
    (hG : SmoothConnectionOn U Gamma) (hV : SmoothVectorOn U V)
    (x : Coordinate4) (hx : x∈U) (i j : Fin 4) :
    covariantVectorDerivative Gamma (fun y => covariantVectorDerivative Gamma V y j) x i-
      covariantVectorDerivative Gamma (fun y => covariantVectorDerivative Gamma V y i) x j=
      (coordinateCurvature Gamma x i j).mulVec (V x) := by
  have hdiff (W : VectorField4) (hW : SmoothVectorOn U W) :=
    smooth_vector_differentiableAt U hU W hW x hx
  have hdV := hdiff V hV
  have hdGi := smooth_matrix_differentiableAt U hU _ (hG i) x hx
  have hdGj := smooth_matrix_differentiableAt U hU _ (hG j) x hx
  change (vectorPartial (fun y => vectorPartial V y j+(Gamma y j).mulVec (V y)) x i+
      (Gamma x i).mulVec (vectorPartial V x j+(Gamma x j).mulVec (V x)))-
    (vectorPartial (fun y => vectorPartial V y i+(Gamma y i).mulVec (V y)) x j+
      (Gamma x j).mulVec (vectorPartial V x i+(Gamma x i).mulVec (V x)))=_
  rw [vectorPartial_add _ _ x (hdiff _ (vectorPartial_smooth U hU V hV j))
      (hdiff _ (matrix_mulVec_smooth U _ V (hG j) hV)) i,
    vectorPartial_add _ _ x (hdiff _ (vectorPartial_smooth U hU V hV i))
      (hdiff _ (matrix_mulVec_smooth U _ V (hG i) hV)) j,
    vectorPartial_mulVec _ V x hdGj hdV i,vectorPartial_mulVec _ V x hdGi hdV j,
    vectorPartial_commute U hU V hV x hx i j]
  simp only [coordinateCurvature,connectionCurvatureJet,connectionFirstJet,
    Matrix.add_mulVec,Matrix.sub_mulVec,Matrix.mulVec_add,Matrix.mulVec_mulVec]
  abel

theorem mixed_gradient_component (Gamma : ConnectionField4) (V : VectorField4)
    (x : Coordinate4) (i j a : Fin 4) :
    mixedCovariantDerivative Gamma (covariantVectorGradient Gamma V) x i a j=
      covariantVectorDerivative Gamma (fun y => covariantVectorDerivative Gamma V y j) x i a-
        ∑ l, Gamma x i l j*covariantVectorDerivative Gamma V x l a := by
  simp only [mixedCovariantDerivative,Matrix.sub_apply,Matrix.add_apply,Matrix.mul_apply,
    tensorFieldJet,covariantVectorGradient,covariantVectorDerivative,vectorPartial,
    Matrix.mulVec,dotProduct,Pi.add_apply,mul_comm]

theorem mixed_gradient_commutator (U : Set Coordinate4) (hU : IsOpen U)
    (Gamma : ConnectionField4) (V : VectorField4)
    (hG : SmoothConnectionOn U Gamma) (hV : SmoothVectorOn U V)
    (x : Coordinate4) (hx : x∈U)
    (ht : ∀ i j a, Gamma x i a j=Gamma x j a i) (i j a : Fin 4) :
    mixedCovariantDerivative Gamma (covariantVectorGradient Gamma V) x i a j-
      mixedCovariantDerivative Gamma (covariantVectorGradient Gamma V) x j a i=
      (coordinateCurvature Gamma x i j).mulVec (V x) a := by
  rw [mixed_gradient_component,mixed_gradient_component]
  have he : (∑ l, Gamma x i l j*covariantVectorDerivative Gamma V x l a)=
      ∑ l, Gamma x j l i*covariantVectorDerivative Gamma V x l a := by
    apply Finset.sum_congr rfl
    intro l _
    rw [ht i j l]
  rw [he]
  have hc := congrArg (fun v : Coordinate4 => v a)
    (covariant_vector_commutator U hU Gamma V hG hV x hx i j)
  simp only [Pi.sub_apply] at hc
  linarith

theorem covariant_vector_matrix_product (Gamma : ConnectionField4)
    (A : TensorField4) (V : VectorField4) (x : Coordinate4)
    (hA : ∀ a b, DifferentiableAt ℝ (fun y => A y a b) x)
    (hV : ∀ a, DifferentiableAt ℝ (fun y => V y a) x) (i : Fin 4) :
    covariantVectorDerivative Gamma (fun y => (A y).mulVec (V y)) x i=
      (mixedCovariantDerivative Gamma A x i).mulVec (V x)+
        (A x).mulVec (covariantVectorDerivative Gamma V x i) := by
  unfold covariantVectorDerivative
  rw [vectorPartial_mulVec A V x hA hV i]
  simp only [mixedCovariantDerivative,Matrix.add_mulVec,Matrix.sub_mulVec,
    Matrix.mulVec_add,Matrix.mulVec_mulVec]
  abel

theorem mixed_covariant_trace (Gamma : ConnectionField4) (A : TensorField4)
    (x : Coordinate4) (hA : ∀ a b, DifferentiableAt ℝ (fun y => A y a b) x) (i : Fin 4) :
    Matrix.trace (mixedCovariantDerivative Gamma A x i)=
      coordinatePartial (fun y => Matrix.trace (A y)) x i := by
  rw [coordinatePartial_trace A x hA i]
  unfold mixedCovariantDerivative
  rw [Matrix.trace_sub,Matrix.trace_add,Matrix.trace_mul_comm (Gamma x i) (A x)]
  abel

#print axioms covariant_vector_commutator
#print axioms mixed_gradient_component
#print axioms mixed_gradient_commutator
#print axioms covariant_vector_matrix_product
#print axioms mixed_covariant_trace
end
end ChatgptAudit
