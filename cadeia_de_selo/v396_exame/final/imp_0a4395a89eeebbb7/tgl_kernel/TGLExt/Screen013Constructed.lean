-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_014 (05-06/09/2026), transposta em 06/09/2026 (COPIA MECANICA de 013 sob namespace Screen013: a versao que COEXISTE com 012 no ROOT — colisao flatNullFrame; CONTADA; o original de 013 fica na bancada)
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
import TGLExt.Screen013NullFrame

set_option autoImplicit false
set_option maxHeartbeats 4000000
namespace ChatgptAudit.Screen013
open Matrix Filter Topology TGLExt
noncomputable section

structure NormalizedScreenAt (g B : Tensor4) (v : Coordinate4) where
  vectors : ScreenVectors
  certificate : NullScreenAt g B v vectors
  gram : screenGram g vectors=-1

theorem normalized_frame_screen_gram (g : Tensor4) (v : Coordinate4)
    (F : NormalizedNullFrame g v) : screenGram g (screenColumns F.frame)=-1 := by
  rw [screen_gram_in_frame,F.gram,null_gram_screen_block]

theorem negative_identity_screen_area : screenArea (-1)=1 := by
  norm_num [screenArea,Matrix.det_fin_two]

def assembleNormalizedScreen (g B : Tensor4) (v : Coordinate4)
    (F : NormalizedNullFrame g v) (hn : (F.frameᵀ*g*B*F.frame) 0 1=0) :
    NormalizedScreenAt g B v where
  vectors := screenColumns F.frame
  certificate := {
    frame := F.frame
    inverse := F.inverse
    metric := -1
    right_inverse := F.right_inverse
    gram := F.gram
    first_column := F.first_column
    columns := rfl
    first_screen_negative := by norm_num
    determinant_positive := by norm_num [Matrix.det_fin_two]
    preserves_null_pairing := hn }
  gram := normalized_frame_screen_gram g v F

def solderedScreenAtPoint (U : Set Coordinate4) (hU : IsOpen U)
    (E D : TensorField4) (Gamma : ConnectionField4) (V : VectorField4)
    (hm : MetricCompatibleOn U (frameMetricField E) Gamma)
    (x : Coordinate4) (hx : x∈U)
    (hED : E x*D x=1) (hDE : D x*E x=1)
    (hg : ∀ a b, DifferentiableAt ℝ (fun y => frameMetricField E y a b) x)
    (hV : ∀ a, DifferentiableAt ℝ (fun y => V y a) x)
    (hv : V x≠0) (hn : ∀ y∈U, tensorQuad (frameMetricField E y) (V y)=0) :
    NormalizedScreenAt (frameMetricField E x) (covariantVectorGradient Gamma V x) (V x) := by
  let F := solderedNullFrame (E x) (D x) hED hDE (V x) hv (hn x hx)
  exact assembleNormalizedScreen _ _ _ F
    (null_field_preserves_frame_pairing U hU (frameMetricField E) Gamma V hm x hx
      (frame_metric_symmetric E x) hg hV hn F.frame F.first_column)

def leviCivitaScreenAtPoint (U : Set Coordinate4) (hU : IsOpen U)
    (E D : TensorField4) (V : VectorField4)
    (hED : ∀ y∈U, E y*D y=1) (hDE : ∀ y∈U, D y*E y=1)
    (hE : SmoothMatrixOn U E) (hV : SmoothVectorOn U V)
    (x : Coordinate4) (hx : x∈U) (hv : V x≠0)
    (hn : ∀ y∈U, tensorQuad (frameMetricField E y) (V y)=0) :
    NormalizedScreenAt (frameMetricField E x)
      (covariantVectorGradient (frameLeviCivita E D) V x) (V x) := by
  let g := frameMetricField E
  let gi := inverseFrameMetricField D
  have hgs : ∀ y∈U, (g y)ᵀ=g y := fun y _ => frame_metric_symmetric E y
  have hm : MetricCompatibleOn U g (frameLeviCivita E D) :=
    levi_civita_field_metric_compatible U hU g gi hgs
      (fun y hy => inverse_frame_metric_left E D y (hED y hy) (hDE y hy))
      (fun y hy => inverse_frame_metric_right E D y (hED y hy) (hDE y hy))
  exact solderedScreenAtPoint U hU E D (frameLeviCivita E D) V hm x hx (hED x hx) (hDE x hx)
    (smooth_matrix_differentiableAt U hU g (frame_metric_smooth U E hE) x hx)
    (smooth_vector_differentiableAt U hU V hV x hx) hv hn

theorem normalized_screen_at_point_area (g B : Tensor4) (v : Coordinate4)
    (S : NormalizedScreenAt g B v) : screenArea (screenGram g S.vectors)=1 := by
  rw [S.gram,negative_identity_screen_area]

theorem levi_civita_null_screen_exists (U : Set Coordinate4) (hU : IsOpen U)
    (E D : TensorField4) (V : VectorField4)
    (hED : ∀ y∈U, E y*D y=1) (hDE : ∀ y∈U, D y*E y=1)
    (hE : SmoothMatrixOn U E) (hV : SmoothVectorOn U V)
    (x : Coordinate4) (hx : x∈U) (hv : V x≠0)
    (hn : ∀ y∈U, tensorQuad (frameMetricField E y) (V y)=0) :
    ∃ S : ScreenVectors, Nonempty (NullScreenAt (frameMetricField E x)
      (covariantVectorGradient (frameLeviCivita E D) V x) (V x) S) ∧
      screenGram (frameMetricField E x) S=-1 ∧ screenArea (screenGram (frameMetricField E x) S)=1 := by
  let S := leviCivitaScreenAtPoint U hU E D V hED hDE hE hV x hx hv hn
  exact ⟨S.vectors,⟨S.certificate⟩,S.gram,normalized_screen_at_point_area _ _ _ S⟩

#print axioms normalized_frame_screen_gram
#print axioms negative_identity_screen_area
#print axioms assembleNormalizedScreen
#print axioms solderedScreenAtPoint
#print axioms leviCivitaScreenAtPoint
#print axioms normalized_screen_at_point_area
#print axioms levi_civita_null_screen_exists
end
end ChatgptAudit.Screen013
