-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_014 (05-06/09/2026), transposta em 06/09/2026
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
import TGLExt.ScreenTransportODE

set_option autoImplicit false
set_option maxHeartbeats 5000000
namespace ChatgptAudit.Screen014
open Matrix Filter Topology Set
open scoped Matrix.Norms.Elementwise
noncomputable section

def vectorColumn (v : Coordinate4) : Matrix (Fin 4) (Fin 1) ℝ := fun a _ => v a

theorem vector_column_pair (g : Tensor4) (u v : Coordinate4) :
    ((vectorColumn u)ᵀ*g*vectorColumn v) 0 0=tensorPair g u v := by
  simp only [vectorColumn,tensorPair,Matrix.mul_apply,Matrix.transpose_apply,Matrix.mulVec,
    dotProduct,Fin.sum_univ_four]
  ring

theorem pair_curve_derivative (g : ℝ → Tensor4) (u v : ℝ → Coordinate4)
    (dg : Tensor4) (du dv : Coordinate4) (t : ℝ)
    (hg : HasMatrixDerivAt g dg t) (hu : HasDerivAt u du t) (hv : HasDerivAt v dv t) :
    HasDerivAt (fun s => tensorPair (g s) (u s) (v s))
      (tensorPair (g t) du (v t)+tensorPair dg (u t) (v t)+tensorPair (g t) (u t) dv) t := by
  have hcu : HasMatrixDerivAt (fun s => vectorColumn (u s)) (vectorColumn du) t :=
    fun a _ => hasDerivAt_pi.mp hu a
  have hcv : HasMatrixDerivAt (fun s => vectorColumn (v s)) (vectorColumn dv) t :=
    fun a _ => hasDerivAt_pi.mp hv a
  have hd := matrix_curve_deriv_mul _ (fun s => vectorColumn (v s)) _ (vectorColumn dv) t
    (matrix_curve_deriv_mul _ g _ dg t (matrix_curve_deriv_transpose _ _ t hcu) hg) hcv 0 0
  have he : (fun s => ((vectorColumn (u s))ᵀ*g s*vectorColumn (v s)) 0 0)=
      (fun s => tensorPair (g s) (u s) (v s)) := by
    funext s
    exact vector_column_pair _ _ _
  rw [he] at hd
  simpa only [Matrix.add_mul,Matrix.add_apply,vector_column_pair] using hd

theorem generator_pair_cancellation (g L B : Tensor4) (u v : Coordinate4) :
    tensorPair g ((B-L).mulVec u) v+tensorPair (Lᵀ*g+g*L) u v+
      tensorPair g u ((B-L).mulVec v)=tensorPair g (B.mulVec u) v+tensorPair g u (B.mulVec v) := by
  simp only [tensorPair,Matrix.mulVec,dotProduct,Matrix.mul_apply,Matrix.transpose_apply,
    Matrix.add_apply,Matrix.sub_apply,Fin.sum_univ_four]
  ring

theorem frame_column_transport (A F : Tensor4) (curve : ℝ → Tensor4) (t : ℝ)
    (hF : HasMatrixDerivAt curve (A*F) t) (j : Fin 4) :
    HasDerivAt (fun s a => curve s a j) (A.mulVec (fun a => F a j)) t := by
  apply hasDerivAt_pi.2
  intro a
  exact hF a j

theorem transported_null_pair_derivative (U : Set Coordinate4) (hU : IsOpen U)
    (g : TensorField4) (Gamma : ConnectionField4) (V : VectorField4)
    (hm : MetricCompatibleOn U g Gamma) (hgs : ∀ x∈U, (g x)ᵀ=g x)
    (hg : SmoothMatrixOn U g) (hV : SmoothVectorOn U V)
    (hn : ∀ x∈U, tensorQuad (g x) (V x)=0)
    (hgeo : Set.EqOn (vectorAcceleration Gamma V) (fun _ => 0) U)
    (curve : ℝ → Coordinate4) (Z : ℝ → Coordinate4) (t : ℝ)
    (ht : curve t∈U) (hc : HasDerivAt curve (V (curve t)) t)
    (hZ : HasDerivAt Z ((transportGenerator Gamma V (curve t)).mulVec (Z t)) t) :
    HasDerivAt (fun s => tensorPair (g (curve s)) (V (curve s)) (Z s)) 0 t := by
  let x := curve t
  let B := covariantVectorGradient Gamma V x
  let L := connectionAlong Gamma x (V x)
  have hdg := metric_along_curve_derivative U g Gamma hm x (V x) ht
    (smooth_matrix_differentiableAt U hU g hg x ht) curve t hc rfl
  have hdV := velocity_along_flow_derivative Gamma V curve t
    (smooth_vector_differentiableAt U hU V hV x ht) hc
  have hd := pair_curve_derivative (fun s => g (curve s)) (fun s => V (curve s)) Z
    (Lᵀ*g x+g x*L) ((B-L).mulVec (V x)) ((B-L).mulVec (Z t)) t hdg hdV hZ
  have ha : B.mulVec (V x)=0 := hgeo ht
  have hz : tensorPair (g x) (V x) (B.mulVec (Z t))=0 :=
    null_field_direction_pairing U hU g Gamma V hm x ht (hgs x ht)
      (smooth_matrix_differentiableAt U hU g hg x ht)
      (smooth_vector_differentiableAt U hU V hV x ht) hn (Z t)
  have hv : tensorPair (g x) ((B-L).mulVec (V x)) (Z t)+
      tensorPair (Lᵀ*g x+g x*L) (V x) (Z t)+tensorPair (g x) (V x) ((B-L).mulVec (Z t))=0 := by
    rw [generator_pair_cancellation,ha,hz]
    simp [tensorPair]
  rw [hv] at hd
  exact hd

theorem frame_flow_pair_preserved (U : Set Coordinate4) (hU : IsOpen U)
    (g : TensorField4) (Gamma : ConnectionField4) (V : VectorField4)
    (hm : MetricCompatibleOn U g Gamma) (hgs : ∀ y∈U, (g y)ᵀ=g y)
    (hg : SmoothMatrixOn U g) (hV : SmoothVectorOn U V)
    (hn : ∀ y∈U, tensorQuad (g y) (V y)=0)
    (hgeo : Set.EqOn (vectorAcceleration Gamma V) (fun _ => 0) U)
    (x : Coordinate4) (F : Tensor4)
    (P : LocalFrameFlow U V (transportGenerator Gamma V) x F)
    (j : Fin 4) (t : ℝ) (ht : t∈Ioo (-P.radius) P.radius) :
    tensorPair (g (P.curve t)) (V (P.curve t)) (fun a => P.frame t a j)=
      tensorPair (g x) (V x) (fun a => F a j) := by
  let f := fun s => tensorPair (g (P.curve s)) (V (P.curve s)) (fun a => P.frame s a j)
  have hd (s : ℝ) (hs : s∈Ioo (-P.radius) P.radius) : HasDerivAt f 0 s :=
    transported_null_pair_derivative U hU g Gamma V hm hgs hg hV hn hgeo P.curve
      (fun r a => P.frame r a j) s (P.curve_mem s hs) (P.tangent s hs)
      (frame_column_transport _ _ P.frame s (P.transport s hs) j)
  have h0 : (0:ℝ)∈Ioo (-P.radius) P.radius :=
    ⟨neg_neg_of_pos P.radius_positive,P.radius_positive⟩
  have he : f t=f 0 := isOpen_Ioo.is_const_of_deriv_eq_zero isPreconnected_Ioo
    (fun s hs => (hd s hs).differentiableAt.differentiableWithinAt)
    (fun s hs => (hd s hs).deriv) ht h0
  simpa only [f,P.curve_zero,P.frame_zero] using he

#print axioms vector_column_pair
#print axioms pair_curve_derivative
#print axioms generator_pair_cancellation
#print axioms frame_column_transport
#print axioms transported_null_pair_derivative
#print axioms frame_flow_pair_preserved
end
end ChatgptAudit.Screen014
