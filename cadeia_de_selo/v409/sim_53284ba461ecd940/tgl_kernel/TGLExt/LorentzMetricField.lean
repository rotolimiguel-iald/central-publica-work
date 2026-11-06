-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_008 (05-06/09/2026), transposta em 06/09/2026
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
import TGLExt.TensorNullCone
import TGLExt.CovariantScalarConservation
import TGLExt.PoincareGroup

set_option autoImplicit false
set_option maxHeartbeats 1800000
namespace ChatgptAudit
open Matrix TGLExt
noncomputable section

def frameMetricField (E : TensorField4) (x : Coordinate4) : Tensor4 :=
  (E x)ᵀ*eta4*E x

def inverseFrameMetricField (D : TensorField4) (x : Coordinate4) : Tensor4 :=
  D x*eta4*(D x)ᵀ

def frameScalar (D A : TensorField4) (x : Coordinate4) : ℝ :=
  ((D x)ᵀ*A x*D x) 0 0

theorem frame_metric_symmetric (E : TensorField4) (x : Coordinate4) :
    (frameMetricField E x)ᵀ=frameMetricField E x :=
  congruence_symmetric (E x) eta4 eta4_symm

theorem inverse_frame_metric_left (E D : TensorField4) (x : Coordinate4)
    (hED : E x*D x=1) (hDE : D x*E x=1) :
    inverseFrameMetricField D x*frameMetricField E x=1 := by
  unfold inverseFrameMetricField frameMetricField
  calc
    (D x*eta4*(D x)ᵀ)*((E x)ᵀ*eta4*E x) =
        D x*eta4*(E x*D x)ᵀ*eta4*E x := by rw [Matrix.transpose_mul]; noncomm_ring
    _ = D x*E x := by rw [hED,Matrix.transpose_one,mul_one,Matrix.mul_assoc (D x),eta4_mul_self,mul_one]
    _ = 1 := hDE

theorem inverse_frame_metric_right (E D : TensorField4) (x : Coordinate4)
    (hED : E x*D x=1) (hDE : D x*E x=1) :
    frameMetricField E x*inverseFrameMetricField D x=1 := by
  unfold inverseFrameMetricField frameMetricField
  calc
    ((E x)ᵀ*eta4*E x)*(D x*eta4*(D x)ᵀ) =
        (E x)ᵀ*eta4*(E x*D x)*eta4*(D x)ᵀ := by noncomm_ring
    _ = (D x*E x)ᵀ := by
      rw [hED,mul_one,Matrix.mul_assoc ((E x)ᵀ),eta4_mul_self,mul_one,Matrix.transpose_mul]
    _ = 1 := by rw [hDE,Matrix.transpose_one]

theorem frame_metric_differentiableOn (U : Set Coordinate4) (E : TensorField4)
    (hE : ∀ i j, DifferentiableOn ℝ (fun x => E x i j) U) (j k : Fin 4) :
    DifferentiableOn ℝ (fun x => frameMetricField E x j k) U := by
  unfold frameMetricField
  simp only [Matrix.mul_apply,Matrix.transpose_apply]
  fun_prop

theorem frame_scalar_differentiableOn (U : Set Coordinate4) (D A : TensorField4)
    (hD : ∀ i j, DifferentiableOn ℝ (fun x => D x i j) U)
    (hA : ∀ i j, DifferentiableOn ℝ (fun x => A x i j) U) :
    DifferentiableOn ℝ (frameScalar D A) U := by
  unfold frameScalar
  simp only [Matrix.mul_apply,Matrix.transpose_apply]
  fun_prop

theorem null_tensor_eq_frame_scalar (E D A : TensorField4) (x : Coordinate4)
    (hED : E x*D x=1) (hDE : D x*E x=1) (hs : (A x)ᵀ=A x)
    (hn : ∀ v, tensorQuad (frameMetricField E x) v=0 → tensorQuad (A x) v=0) :
    A x=frameScalar D A x • frameMetricField E x := by
  have hp : ∀ v, tensorQuad eta4 v=0 → tensorQuad ((D x)ᵀ*A x*D x) v=0 := by
    intro v hv
    rw [tensorQuad_congruence]
    apply hn
    rw [frameMetricField,tensorQuad_congruence,Matrix.mulVec_mulVec,hED,Matrix.one_mulVec]
    exact hv
  have hr := minkowski_tensor_null_rigidity ((D x)ᵀ*A x*D x)
    (congruence_symmetric (D x) (A x) hs) hp
  have ht := congrArg (fun C : Tensor4 => (E x)ᵀ*C*E x) hr
  rw [congruence_undo (D x) (E x) (A x) hDE] at ht
  simpa only [Matrix.mul_smul,Matrix.smul_mul,frameScalar,frameMetricField] using ht

#print axioms frame_metric_symmetric
#print axioms inverse_frame_metric_left
#print axioms inverse_frame_metric_right
#print axioms frame_metric_differentiableOn
#print axioms frame_scalar_differentiableOn
#print axioms null_tensor_eq_frame_scalar
end
end ChatgptAudit
