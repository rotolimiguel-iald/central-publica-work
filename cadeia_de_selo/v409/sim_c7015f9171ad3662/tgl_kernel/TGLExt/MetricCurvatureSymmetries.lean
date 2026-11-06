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
import TGLExt.CoordinateCurvature
import TGLExt.MetricFieldConnection

set_option autoImplicit false
set_option maxHeartbeats 1800000
namespace ChatgptAudit
open Matrix
open scoped ContDiff
noncomputable section

def MetricCompatibleOn (U : Set Coordinate4) (g : TensorField4) (Gamma : ConnectionField4) : Prop :=
  ∀ x∈U, ∀ i, covariantTensorJet (g x) (tensorFieldJet g x) (Gamma x) i=0

def lowerCoordinateCurvature (g : TensorField4) (Gamma : ConnectionField4)
    (x : Coordinate4) (a b i j : Fin 4) : ℝ := (g x*coordinateCurvature Gamma x i j) a b

def coordinateRicci (Gamma : ConnectionField4) (x : Coordinate4) : Matrix (Fin 4) (Fin 4) ℝ :=
  fun b j => ∑ a, coordinateCurvature Gamma x a j a b

def coordinateScalarCurvature (gInv : TensorField4) (Gamma : ConnectionField4) (x : Coordinate4) : ℝ :=
  ∑ i, ∑ j, gInv x i j*coordinateRicci Gamma x i j

def geometricEinsteinTensor (g gInv : TensorField4) (Gamma : ConnectionField4) (x : Coordinate4) :
    Matrix (Fin 4) (Fin 4) ℝ :=
  coordinateRicci Gamma x-(coordinateScalarCurvature gInv Gamma x/2) • g x

theorem metric_compatibility_formula (U : Set Coordinate4) (g : TensorField4)
    (Gamma : ConnectionField4) (hm : MetricCompatibleOn U g Gamma)
    (x : Coordinate4) (hx : x∈U) (i : Fin 4) :
    tensorFieldJet g x i=(Gamma x i)ᵀ*g x+g x*Gamma x i := by
  have he := hm x hx i
  rw [covariantTensorJet,sub_sub] at he
  exact sub_eq_zero.mp he

theorem metric_compatibility_derivative (U : Set Coordinate4) (hU : IsOpen U)
    (g : TensorField4) (Gamma : ConnectionField4)
    (hg : SmoothMatrixOn U g) (hG : SmoothConnectionOn U Gamma)
    (hm : MetricCompatibleOn U g Gamma) (x : Coordinate4) (hx : x∈U) (k i : Fin 4) :
    tensorFieldJet (fun y => tensorFieldJet g y i) x k=
      (connectionFirstJet Gamma x k i)ᵀ*g x+(Gamma x i)ᵀ*tensorFieldJet g x k+
        tensorFieldJet g x k*Gamma x i+g x*connectionFirstJet Gamma x k i := by
  have heq : Set.EqOn (fun y => tensorFieldJet g y i)
      (fun y => (Gamma y i)ᵀ*g y+g y*Gamma y i) U := by
    intro y hy
    exact metric_compatibility_formula U g Gamma hm y hy i
  have hdiff (A : TensorField4) (hA : SmoothMatrixOn U A) :
      ∀ a b, DifferentiableAt ℝ (fun y => A y a b) x :=
    smooth_matrix_differentiableAt U hU A hA x hx
  have hT := SmoothMatrixOn.transpose U _ (hG i)
  rw [show tensorFieldJet (fun y => tensorFieldJet g y i) x k =
      tensorFieldJet (fun y => (Gamma y i)ᵀ*g y+g y*Gamma y i) x k from
    congrArg (fun J => J k) (tensorFieldJet_congr_on U hU _ _ heq x hx)]
  rw [tensorFieldJet_add _ _ x (hdiff _ (SmoothMatrixOn.mul U _ _ hT hg))
    (hdiff _ (SmoothMatrixOn.mul U _ _ hg (hG i)))]
  simp only [Pi.add_apply,tensorFieldJet_mul _ _ x (hdiff _ hT) (hdiff _ hg),
    tensorFieldJet_mul _ _ x (hdiff _ hg) (hdiff _ (hG i)),tensorFieldJet_transpose,connectionFirstJet]
  abel

theorem coordinate_curvature_metric_skew (U : Set Coordinate4) (hU : IsOpen U)
    (g : TensorField4) (Gamma : ConnectionField4)
    (hg : SmoothMatrixOn U g) (hG : SmoothConnectionOn U Gamma)
    (hm : MetricCompatibleOn U g Gamma) (x : Coordinate4) (hx : x∈U) (i j : Fin 4) :
    (coordinateCurvature Gamma x i j)ᵀ*g x+g x*coordinateCurvature Gamma x i j=0 := by
  exact curvature_jet_metric_skew (g x) (tensorFieldJet g x)
    (fun a b => tensorFieldJet (fun y => tensorFieldJet g y b) x a)
    (Gamma x) (connectionFirstJet Gamma x)
    (metric_compatibility_formula U g Gamma hm x hx)
    (metric_compatibility_derivative U hU g Gamma hg hG hm x hx)
    (tensorFieldJet_commute U hU g hg x hx) i j

theorem lower_curvature_first_skew (U : Set Coordinate4) (hU : IsOpen U)
    (g : TensorField4) (Gamma : ConnectionField4)
    (hg : SmoothMatrixOn U g) (hG : SmoothConnectionOn U Gamma)
    (hm : MetricCompatibleOn U g Gamma) (x : Coordinate4) (hx : x∈U) (hgs : (g x)ᵀ=g x)
    (a b i j : Fin 4) : lowerCoordinateCurvature g Gamma x a b i j= -lowerCoordinateCurvature g Gamma x b a i j := by
  have he : (g x*coordinateCurvature Gamma x i j)ᵀ= -(g x*coordinateCurvature Gamma x i j) := by
    rw [Matrix.transpose_mul,hgs]
    exact eq_neg_of_add_eq_zero_left (coordinate_curvature_metric_skew U hU g Gamma hg hG hm x hx i j)
  exact congrArg (fun A : Matrix (Fin 4) (Fin 4) ℝ => A b a) he

theorem lower_curvature_last_skew (g : TensorField4) (Gamma : ConnectionField4)
    (x : Coordinate4) (a b i j : Fin 4) :
    lowerCoordinateCurvature g Gamma x a b i j= -lowerCoordinateCurvature g Gamma x a b j i := by
  unfold lowerCoordinateCurvature
  rw [coordinate_curvature_antisymmetric Gamma x i j,Matrix.mul_neg]
  rfl

theorem lower_curvature_first_bianchi (U : Set Coordinate4) (hU : IsOpen U)
    (g : TensorField4) (Gamma : ConnectionField4)
    (ht : ∀ x∈U, ∀ i j l, Gamma x i l j=Gamma x j l i)
    (x : Coordinate4) (hx : x∈U) (a b i j : Fin 4) :
    lowerCoordinateCurvature g Gamma x a b i j+lowerCoordinateCurvature g Gamma x a i j b+
      lowerCoordinateCurvature g Gamma x a j b i=0 := by
  simp only [lowerCoordinateCurvature,Matrix.mul_apply]
  rw [← Finset.sum_add_distrib,← Finset.sum_add_distrib]
  apply Finset.sum_eq_zero
  intro c hc
  rw [← mul_add,← mul_add,coordinate_first_bianchi U hU Gamma ht x hx i j b c,mul_zero]

theorem lower_curvature_pair_symmetry (U : Set Coordinate4) (hU : IsOpen U)
    (g : TensorField4) (Gamma : ConnectionField4)
    (hg : SmoothMatrixOn U g) (hG : SmoothConnectionOn U Gamma)
    (hm : MetricCompatibleOn U g Gamma)
    (ht : ∀ x∈U, ∀ i j l, Gamma x i l j=Gamma x j l i)
    (x : Coordinate4) (hx : x∈U) (hgs : (g x)ᵀ=g x) (a b i j : Fin 4) :
    lowerCoordinateCurvature g Gamma x a b i j=lowerCoordinateCurvature g Gamma x i j a b := by
  exact curvature_pair_symmetry_from_identities (lowerCoordinateCurvature g Gamma x)
    (lower_curvature_first_skew U hU g Gamma hg hG hm x hx hgs)
    (lower_curvature_last_skew g Gamma x)
    (lower_curvature_first_bianchi U hU g Gamma ht x hx) a b i j

theorem ricci_lower_expression (g gInv : TensorField4) (Gamma : ConnectionField4)
    (x : Coordinate4) (hinv : gInv x*g x=1) (b j : Fin 4) :
    coordinateRicci Gamma x b j=∑ a, ∑ c, gInv x a c*lowerCoordinateCurvature g Gamma x c b a j := by
  unfold coordinateRicci
  apply Finset.sum_congr rfl
  intro a ha
  change coordinateCurvature Gamma x a j a b = (gInv x*(g x*coordinateCurvature Gamma x a j)) a b
  rw [← Matrix.mul_assoc,hinv,one_mul]

theorem coordinate_ricci_symmetric (U : Set Coordinate4) (hU : IsOpen U)
    (g gInv : TensorField4) (Gamma : ConnectionField4)
    (hg : SmoothMatrixOn U g) (hG : SmoothConnectionOn U Gamma)
    (hm : MetricCompatibleOn U g Gamma)
    (ht : ∀ x∈U, ∀ i j l, Gamma x i l j=Gamma x j l i)
    (x : Coordinate4) (hx : x∈U) (hgs : (g x)ᵀ=g x) (hinv : gInv x*g x=1) :
    (coordinateRicci Gamma x)ᵀ=coordinateRicci Gamma x := by
  ext b j
  change coordinateRicci Gamma x j b=coordinateRicci Gamma x b j
  rw [ricci_lower_expression g gInv Gamma x hinv j b,ricci_lower_expression g gInv Gamma x hinv b j,
    Finset.sum_comm]
  apply Finset.sum_congr rfl
  intro a ha
  apply Finset.sum_congr rfl
  intro c hc
  have hi : gInv x c a=gInv x a c := congrArg (fun A : Matrix (Fin 4) (Fin 4) ℝ => A a c)
    (inverse_symmetric_of_symmetric (g x) (gInv x) hgs hinv)
  rw [hi,lower_curvature_pair_symmetry U hU g Gamma hg hG hm ht x hx hgs a j c b]

theorem geometric_einstein_symmetric (U : Set Coordinate4) (hU : IsOpen U)
    (g gInv : TensorField4) (Gamma : ConnectionField4)
    (hg : SmoothMatrixOn U g) (hG : SmoothConnectionOn U Gamma)
    (hm : MetricCompatibleOn U g Gamma)
    (ht : ∀ x∈U, ∀ i j l, Gamma x i l j=Gamma x j l i)
    (x : Coordinate4) (hx : x∈U) (hgs : (g x)ᵀ=g x) (hinv : gInv x*g x=1) :
    (geometricEinsteinTensor g gInv Gamma x)ᵀ=geometricEinsteinTensor g gInv Gamma x := by
  simp only [geometricEinsteinTensor,Matrix.transpose_sub,Matrix.transpose_smul,hgs,
    coordinate_ricci_symmetric U hU g gInv Gamma hg hG hm ht x hx hgs hinv]

#print axioms metric_compatibility_formula
#print axioms metric_compatibility_derivative
#print axioms coordinate_curvature_metric_skew
#print axioms lower_curvature_first_skew
#print axioms lower_curvature_last_skew
#print axioms lower_curvature_first_bianchi
#print axioms lower_curvature_pair_symmetry
#print axioms ricci_lower_expression
#print axioms coordinate_ricci_symmetric
#print axioms geometric_einstein_symmetric
end
end ChatgptAudit
