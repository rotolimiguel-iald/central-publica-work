-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_013 (05-06/09/2026), transposta em 06/09/2026
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
import TGLExt.GeometricAreaHorizon

set_option autoImplicit false
set_option maxHeartbeats 4000000
namespace ChatgptAudit
open Matrix Filter Topology
noncomputable section

def tensorPair (g : Tensor4) (u v : Coordinate4) : ℝ := u ⬝ᵥ (g *ᵥ v)

theorem tensor_pair_symmetric (g : Tensor4) (hs : gᵀ=g) (u v : Coordinate4) :
    tensorPair g u v=tensorPair g v u := by
  unfold tensorPair
  rw [← hs,Matrix.dotProduct_transpose_mulVec]
  rw [hs]

theorem frame_pair_entry (g F : Tensor4) (i j : Fin 4) :
    (Fᵀ*g*F) i j=tensorPair g (fun a => F a i) (fun a => F a j) := by
  simp only [tensorPair,Matrix.mul_apply,Matrix.transpose_apply,Matrix.mulVec,dotProduct,
    Fin.sum_univ_four]
  ring

theorem mixed_frame_pair_entry (g B F : Tensor4) (i j : Fin 4) :
    (Fᵀ*g*B*F) i j=tensorPair g (fun a => F a i) (B.mulVec (fun a => F a j)) := by
  simp only [tensorPair,Matrix.mul_apply,Matrix.transpose_apply,Matrix.mulVec,dotProduct,
    Fin.sum_univ_four]
  ring

theorem quad_coordinate_derivative (g : TensorField4) (V : VectorField4) (x : Coordinate4)
    (hg : ∀ a b, DifferentiableAt ℝ (fun y => g y a b) x)
    (hV : ∀ a, DifferentiableAt ℝ (fun y => V y a) x) (i : Fin 4) :
    coordinatePartial (fun y => tensorQuad (g y) (V y)) x i =
      tensorPair (g x) (vectorPartial V x i) (V x)+
      tensorPair (tensorFieldJet g x i) (V x) (V x)+
      tensorPair (g x) (V x) (vectorPartial V x i) := by
  have hd (a : Fin 4) : DifferentiableAt ℝ (fun y => ∑ b, g y a b*V y b) x :=
    DifferentiableAt.fun_sum (fun b _ => (hg a b).mul (hV b))
  change coordinatePartial (fun y => ∑ a, V y a*(∑ b, g y a b*V y b)) x i=_
  rw [coordinatePartial_sum (fun a y => V y a*(∑ b, g y a b*V y b)) x (fun a => (hV a).mul (hd a)) i]
  simp only [coordinatePartial_mul (fun y => V y _) (fun y => ∑ b, g y _ b*V y b) x (hV _) (hd _) i]
  simp only [coordinatePartial_sum (fun b y => g y _ b*V y b) x (fun b => (hg _ b).mul (hV b)) i,
    coordinatePartial_mul (fun y => g y _ _) (fun y => V y _) x (hg _ _) (hV _) i]
  simp only [tensorPair,vectorPartial,tensorFieldJet,Matrix.mulVec,dotProduct,
    Fin.sum_univ_four]
  ring

theorem metric_compatible_quad_derivative (U : Set Coordinate4) (g : TensorField4)
    (Gamma : ConnectionField4) (V : VectorField4) (hm : MetricCompatibleOn U g Gamma)
    (x : Coordinate4) (hx : x∈U) (hs : (g x)ᵀ=g x)
    (hg : ∀ a b, DifferentiableAt ℝ (fun y => g y a b) x)
    (hV : ∀ a, DifferentiableAt ℝ (fun y => V y a) x) (i : Fin 4) :
    coordinatePartial (fun y => tensorQuad (g y) (V y)) x i=
      2*tensorPair (g x) (V x) (covariantVectorDerivative Gamma V x i) := by
  rw [quad_coordinate_derivative g V x hg hV i,metric_compatibility_formula U g Gamma hm x hx]
  rw [tensor_pair_symmetric (g x) hs (vectorPartial V x i) (V x)]
  have hs' (a b : Fin 4) : g x b a=g x a b :=
    congrArg (fun A : Tensor4 => A a b) hs
  simp only [tensorPair,covariantVectorDerivative,Pi.add_apply,Matrix.add_apply,
    Matrix.mulVec,dotProduct,Matrix.mul_apply,Matrix.transpose_apply,Fin.sum_univ_four,
    hs' 0 1,hs' 0 2,hs' 0 3,hs' 1 2,hs' 1 3,hs' 2 3]
  ring

theorem null_field_covariant_pairing (U : Set Coordinate4) (hU : IsOpen U)
    (g : TensorField4) (Gamma : ConnectionField4) (V : VectorField4)
    (hm : MetricCompatibleOn U g Gamma) (x : Coordinate4) (hx : x∈U)
    (hs : (g x)ᵀ=g x)
    (hg : ∀ a b, DifferentiableAt ℝ (fun y => g y a b) x)
    (hV : ∀ a, DifferentiableAt ℝ (fun y => V y a) x)
    (hn : ∀ y∈U, tensorQuad (g y) (V y)=0) (i : Fin 4) :
    tensorPair (g x) (V x) (covariantVectorDerivative Gamma V x i)=0 := by
  have he : (fun y => tensorQuad (g y) (V y)) =ᶠ[𝓝 x] (fun _ => (0:ℝ)) := by
    filter_upwards [hU.mem_nhds hx] with y hy
    exact hn y hy
  have hz : coordinatePartial (fun y => tensorQuad (g y) (V y)) x i=0 := by
    unfold coordinatePartial
    rw [he.fderiv_eq]
    simp
  rw [metric_compatible_quad_derivative U g Gamma V hm x hx hs hg hV i] at hz
  linarith

theorem null_field_direction_pairing (U : Set Coordinate4) (hU : IsOpen U)
    (g : TensorField4) (Gamma : ConnectionField4) (V : VectorField4)
    (hm : MetricCompatibleOn U g Gamma) (x : Coordinate4) (hx : x∈U)
    (hs : (g x)ᵀ=g x)
    (hg : ∀ a b, DifferentiableAt ℝ (fun y => g y a b) x)
    (hV : ∀ a, DifferentiableAt ℝ (fun y => V y a) x)
    (hn : ∀ y∈U, tensorQuad (g y) (V y)=0) (w : Coordinate4) :
    tensorPair (g x) (V x) ((covariantVectorGradient Gamma V x).mulVec w)=0 := by
  have hsum : tensorPair (g x) (V x) ((covariantVectorGradient Gamma V x).mulVec w)=
      ∑ i, w i*tensorPair (g x) (V x) (covariantVectorDerivative Gamma V x i) := by
    simp only [tensorPair,covariantVectorGradient,Matrix.mulVec,dotProduct,Fin.sum_univ_four]
    ring
  rw [hsum]
  simp only [null_field_covariant_pairing U hU g Gamma V hm x hx hs hg hV hn,
    mul_zero,Finset.sum_const_zero]

theorem null_field_preserves_frame_pairing (U : Set Coordinate4) (hU : IsOpen U)
    (g : TensorField4) (Gamma : ConnectionField4) (V : VectorField4)
    (hm : MetricCompatibleOn U g Gamma) (x : Coordinate4) (hx : x∈U)
    (hs : (g x)ᵀ=g x)
    (hg : ∀ a b, DifferentiableAt ℝ (fun y => g y a b) x)
    (hV : ∀ a, DifferentiableAt ℝ (fun y => V y a) x)
    (hn : ∀ y∈U, tensorQuad (g y) (V y)=0)
    (F : Tensor4) (hF : ∀ a, F a 0=V x a) :
    (Fᵀ*g x*covariantVectorGradient Gamma V x*F) 0 1=0 := by
  rw [mixed_frame_pair_entry]
  have he : (fun a => F a 0)=V x := funext hF
  rw [he]
  exact null_field_direction_pairing U hU g Gamma V hm x hx hs hg hV hn _

#print axioms tensor_pair_symmetric
#print axioms frame_pair_entry
#print axioms mixed_frame_pair_entry
#print axioms quad_coordinate_derivative
#print axioms metric_compatible_quad_derivative
#print axioms null_field_covariant_pairing
#print axioms null_field_direction_pairing
#print axioms null_field_preserves_frame_pairing
end
end ChatgptAudit
