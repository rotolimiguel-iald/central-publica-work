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
import TGLExt.MetricCurvatureSymmetries

set_option autoImplicit false
set_option maxHeartbeats 2400000
namespace ChatgptAudit
open Matrix
noncomputable section

def covariantCurvatureDerivative (Gamma : ConnectionField4) (x : Coordinate4) (k i j : Fin 4) :
    Matrix (Fin 4) (Fin 4) ℝ :=
  exteriorCovariantCurvatureDerivative Gamma x k i j-
    ∑ l, Gamma x k l i • coordinateCurvature Gamma x l j-
    ∑ l, Gamma x k l j • coordinateCurvature Gamma x i l

def lowerCovariantCurvatureDerivative (g : TensorField4) (Gamma : ConnectionField4)
    (x : Coordinate4) (k a b i j : Fin 4) : ℝ :=
  (g x*covariantCurvatureDerivative Gamma x k i j) a b

theorem tensorFieldJet_neg (A : TensorField4) (x : Coordinate4) (i : Fin 4) :
    tensorFieldJet (fun y => -A y) x i= -tensorFieldJet A x i := by
  ext j k
  simp [tensorFieldJet,coordinatePartial,fderiv_fun_neg]

theorem covariant_tensor_skew (U : Set Coordinate4) (hU : IsOpen U)
    (A : TensorField4) (Gamma : ConnectionField4) (hA : ∀ x∈U, (A x)ᵀ= -A x)
    (x : Coordinate4) (hx : x∈U) (i : Fin 4) :
    (covariantTensorJet (A x) (tensorFieldJet A x) (Gamma x) i)ᵀ=
      -covariantTensorJet (A x) (tensorFieldJet A x) (Gamma x) i := by
  have heq : Set.EqOn (fun y => (A y)ᵀ) (fun y => -A y) U := by
    intro y hy
    exact hA y hy
  have hj : (tensorFieldJet A x i)ᵀ= -tensorFieldJet A x i := by
    rw [← tensorFieldJet_transpose]
    have he := congrArg (fun J => J i) (tensorFieldJet_congr_on U hU _ _ heq x hx)
    exact he.trans (tensorFieldJet_neg A x i)
  simp only [covariantTensorJet,Matrix.transpose_sub,Matrix.transpose_mul,Matrix.transpose_transpose,
    hj,hA x hx,Matrix.neg_mul,Matrix.mul_neg]
  abel

theorem coordinate_second_bianchi (U : Set Coordinate4) (hU : IsOpen U)
    (Gamma : ConnectionField4) (hG : SmoothConnectionOn U Gamma)
    (ht : ∀ x∈U, ∀ i j l, Gamma x i l j=Gamma x j l i)
    (x : Coordinate4) (hx : x∈U) (i j k : Fin 4) :
    covariantCurvatureDerivative Gamma x i j k+covariantCurvatureDerivative Gamma x j k i+
      covariantCurvatureDerivative Gamma x k i j=0 := by
  have hp (l : Fin 4) : Gamma x i l j • coordinateCurvature Gamma x l k+
      Gamma x i l k • coordinateCurvature Gamma x j l+
      Gamma x j l k • coordinateCurvature Gamma x l i+
      Gamma x j l i • coordinateCurvature Gamma x k l+
      Gamma x k l i • coordinateCurvature Gamma x l j+
      Gamma x k l j • coordinateCurvature Gamma x i l=0 := by
    rw [ht x hx i j l,ht x hx i k l,ht x hx j k l,
      coordinate_curvature_antisymmetric Gamma x k l,
      coordinate_curvature_antisymmetric Gamma x l j,
      coordinate_curvature_antisymmetric Gamma x i l]
    simp only [smul_neg]
    abel
  have he : covariantCurvatureDerivative Gamma x i j k+covariantCurvatureDerivative Gamma x j k i+
      covariantCurvatureDerivative Gamma x k i j =
      (exteriorCovariantCurvatureDerivative Gamma x i j k+exteriorCovariantCurvatureDerivative Gamma x j k i+
        exteriorCovariantCurvatureDerivative Gamma x k i j)-
      ∑ l, (Gamma x i l j • coordinateCurvature Gamma x l k+
        Gamma x i l k • coordinateCurvature Gamma x j l+
        Gamma x j l k • coordinateCurvature Gamma x l i+
        Gamma x j l i • coordinateCurvature Gamma x k l+
        Gamma x k l i • coordinateCurvature Gamma x l j+
        Gamma x k l j • coordinateCurvature Gamma x i l) := by
    simp only [covariantCurvatureDerivative,Finset.sum_add_distrib]
    abel
  rw [he,coordinate_exterior_bianchi U hU Gamma hG x hx]
  simp only [hp,Finset.sum_const_zero,sub_zero]

theorem lower_second_bianchi (U : Set Coordinate4) (hU : IsOpen U)
    (g : TensorField4) (Gamma : ConnectionField4) (hG : SmoothConnectionOn U Gamma)
    (ht : ∀ x∈U, ∀ i j l, Gamma x i l j=Gamma x j l i)
    (x : Coordinate4) (hx : x∈U) (a b i j k : Fin 4) :
    lowerCovariantCurvatureDerivative g Gamma x i a b j k+
    lowerCovariantCurvatureDerivative g Gamma x j a b k i+
    lowerCovariantCurvatureDerivative g Gamma x k a b i j=0 := by
  have he := congrArg (fun A : Matrix (Fin 4) (Fin 4) ℝ => (g x*A) a b)
    (coordinate_second_bianchi U hU Gamma hG ht x hx i j k)
  simpa only [Matrix.mul_add,Matrix.add_apply,mul_zero,Matrix.zero_apply,lowerCovariantCurvatureDerivative] using he

theorem lower_exterior_derivative_formula (U : Set Coordinate4) (hU : IsOpen U)
    (g : TensorField4) (Gamma : ConnectionField4)
    (hg : SmoothMatrixOn U g) (hG : SmoothConnectionOn U Gamma)
    (hm : MetricCompatibleOn U g Gamma) (x : Coordinate4) (hx : x∈U) (k i j : Fin 4) :
    covariantTensorJet (g x*coordinateCurvature Gamma x i j)
      (tensorFieldJet (fun y => g y*coordinateCurvature Gamma y i j) x) (Gamma x) k =
        g x*exteriorCovariantCurvatureDerivative Gamma x k i j := by
  rw [covariantTensorJet,tensorFieldJet_mul _ _ x
    (smooth_matrix_differentiableAt U hU g hg x hx)
    (smooth_matrix_differentiableAt U hU _ (coordinate_curvature_smooth U hU Gamma hG i j) x hx),
    metric_compatibility_formula U g Gamma hm x hx k]
  unfold exteriorCovariantCurvatureDerivative
  noncomm_ring

theorem lower_covariant_derivative_formula (U : Set Coordinate4) (hU : IsOpen U)
    (g : TensorField4) (Gamma : ConnectionField4)
    (hg : SmoothMatrixOn U g) (hG : SmoothConnectionOn U Gamma)
    (hm : MetricCompatibleOn U g Gamma) (x : Coordinate4) (hx : x∈U) (k i j : Fin 4) :
    g x*covariantCurvatureDerivative Gamma x k i j =
      covariantTensorJet (g x*coordinateCurvature Gamma x i j)
        (tensorFieldJet (fun y => g y*coordinateCurvature Gamma y i j) x) (Gamma x) k-
      ∑ l, Gamma x k l i • (g x*coordinateCurvature Gamma x l j)-
      ∑ l, Gamma x k l j • (g x*coordinateCurvature Gamma x i l) := by
  rw [lower_exterior_derivative_formula U hU g Gamma hg hG hm x hx]
  simp only [covariantCurvatureDerivative,Matrix.mul_sub,Matrix.mul_sum,Matrix.mul_smul]

theorem lower_covariant_first_skew (U : Set Coordinate4) (hU : IsOpen U)
    (g : TensorField4) (Gamma : ConnectionField4)
    (hg : SmoothMatrixOn U g) (hG : SmoothConnectionOn U Gamma)
    (hm : MetricCompatibleOn U g Gamma) (hgs : ∀ x∈U, (g x)ᵀ=g x)
    (x : Coordinate4) (hx : x∈U) (k a b i j : Fin 4) :
    lowerCovariantCurvatureDerivative g Gamma x k a b i j=
      -lowerCovariantCurvatureDerivative g Gamma x k b a i j := by
  have hs (i j : Fin 4) : ∀ y∈U, (g y*coordinateCurvature Gamma y i j)ᵀ=
      -(g y*coordinateCurvature Gamma y i j) := by
    intro y hy
    rw [Matrix.transpose_mul,hgs y hy]
    exact eq_neg_of_add_eq_zero_left (coordinate_curvature_metric_skew U hU g Gamma hg hG hm y hy i j)
  have he : (g x*covariantCurvatureDerivative Gamma x k i j)ᵀ=
      -(g x*covariantCurvatureDerivative Gamma x k i j) := by
    rw [lower_covariant_derivative_formula U hU g Gamma hg hG hm x hx k i j]
    simp only [Matrix.transpose_sub,Matrix.transpose_sum,Matrix.transpose_smul,
      covariant_tensor_skew U hU _ Gamma (hs i j) x hx k,hs _ _ x hx,smul_neg,
      Finset.sum_neg_distrib]
    abel
  exact congrArg (fun A : Matrix (Fin 4) (Fin 4) ℝ => A b a) he

theorem exterior_derivative_last_skew (Gamma : ConnectionField4) (x : Coordinate4) (k i j : Fin 4) :
    exteriorCovariantCurvatureDerivative Gamma x k i j=
      -exteriorCovariantCurvatureDerivative Gamma x k j i := by
  have heq : (fun y => coordinateCurvature Gamma y i j)=(fun y => -coordinateCurvature Gamma y j i) := by
    funext y
    exact coordinate_curvature_antisymmetric Gamma y i j
  have hd : tensorFieldJet (fun y => coordinateCurvature Gamma y i j) x k=
      -tensorFieldJet (fun y => coordinateCurvature Gamma y j i) x k := by
    rw [heq,tensorFieldJet_neg]
  simp only [exteriorCovariantCurvatureDerivative,hd,coordinate_curvature_antisymmetric Gamma x i j,
    Matrix.mul_neg,Matrix.neg_mul]
  abel

theorem covariant_derivative_last_skew (Gamma : ConnectionField4) (x : Coordinate4) (k i j : Fin 4) :
    covariantCurvatureDerivative Gamma x k i j= -covariantCurvatureDerivative Gamma x k j i := by
  have h1 : (∑ l, Gamma x k l i • coordinateCurvature Gamma x l j)=
      -(∑ l, Gamma x k l i • coordinateCurvature Gamma x j l) := by
    rw [← Finset.sum_neg_distrib]
    apply Finset.sum_congr rfl
    intro l hl
    rw [coordinate_curvature_antisymmetric Gamma x l j,smul_neg]
  have h2 : (∑ l, Gamma x k l j • coordinateCurvature Gamma x i l)=
      -(∑ l, Gamma x k l j • coordinateCurvature Gamma x l i) := by
    rw [← Finset.sum_neg_distrib]
    apply Finset.sum_congr rfl
    intro l hl
    rw [coordinate_curvature_antisymmetric Gamma x i l,smul_neg]
  rw [covariantCurvatureDerivative,covariantCurvatureDerivative,exterior_derivative_last_skew Gamma x k i j,h1,h2]
  abel

theorem lower_covariant_last_skew (g : TensorField4) (Gamma : ConnectionField4)
    (x : Coordinate4) (k a b i j : Fin 4) :
    lowerCovariantCurvatureDerivative g Gamma x k a b i j=
      -lowerCovariantCurvatureDerivative g Gamma x k a b j i := by
  unfold lowerCovariantCurvatureDerivative
  rw [covariant_derivative_last_skew Gamma x k i j,Matrix.mul_neg]
  rfl

#print axioms tensorFieldJet_neg
#print axioms covariant_tensor_skew
#print axioms coordinate_second_bianchi
#print axioms lower_second_bianchi
#print axioms lower_exterior_derivative_formula
#print axioms lower_covariant_derivative_formula
#print axioms lower_covariant_first_skew
#print axioms exterior_derivative_last_skew
#print axioms covariant_derivative_last_skew
#print axioms lower_covariant_last_skew
end
end ChatgptAudit
