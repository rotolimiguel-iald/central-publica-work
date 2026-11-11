-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_023 (05-06/09/2026), transposta em 06/09/2026
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
import TGLExt.DirectionalUnitaryFamily

set_option autoImplicit false
set_option maxHeartbeats 7500000
namespace ChatgptAudit.Coherent023
open Matrix Filter Topology Set ChatgptAudit.Unitary022
open scoped ContDiff
noncomputable section

def coherentCoupling (a b u v : ℝ) : ℝ := -unitaryResponse a b 1 u v/Real.pi

def covectorStress (g gInv : Tensor4) (w : Coordinate4) (coupling : ℝ) : Tensor4 :=
  coupling • (Matrix.vecMulVec w w-(tensorQuad gInv w/2) • g)

def covectorStressField (g gInv : TensorField4) (w : CovectorField4) (coupling : ℝ) : TensorField4 :=
  fun x => covectorStress (g x) (gInv x) (w x) coupling

theorem response_coupling_identity (a b frequency u v : ℝ) :
    unitaryResponse a b frequency u v= -Real.pi*coherentCoupling a b u v*frequency^2 := by
  rw [unitary_response_frequency_square a b frequency u v]
  unfold coherentCoupling
  field_simp [Real.pi_ne_zero]

theorem coherent_negative_control_coupling_positive : 0<coherentCoupling (-3/5) (4/5) (3/5) (4/5) :=
  negative_control_required_matter_positive

theorem covector_stress_symmetric (g gInv : Tensor4) (w : Coordinate4) (coupling : ℝ)
    (hg : gᵀ=g) : (covectorStress g gInv w coupling)ᵀ=covectorStress g gInv w coupling := by
  simp only [covectorStress,Matrix.transpose_smul,Matrix.transpose_sub,outer_tensor_symmetric,hg]

theorem covector_stress_quad (g gInv : Tensor4) (w direction : Coordinate4) (coupling : ℝ) :
    tensorQuad (covectorStress g gInv w coupling) direction=
      coupling*((covectorRead w direction)^2-(tensorQuad gInv w/2)*tensorQuad g direction) := by
  simp only [covectorStress,tensorQuad,Matrix.smul_mulVec,dotProduct_smul,smul_eq_mul]
  change coupling*tensorQuad (Matrix.vecMulVec w w-(tensorQuad gInv w/2) • g) direction=_
  rw [tensorQuad_sub_smul,outer_tensor_quad]
  rfl

theorem covector_stress_null (g gInv : Tensor4) (w direction : Coordinate4) (coupling : ℝ)
    (hn : tensorQuad g direction=0) :
    tensorQuad (covectorStress g gInv w coupling) direction=coupling*(covectorRead w direction)^2 := by
  rw [covector_stress_quad,hn,mul_zero,sub_zero]

theorem covector_stress_null_nonnegative (g gInv : Tensor4) (w direction : Coordinate4) (coupling : ℝ)
    (hc : 0≤coupling) (hn : tensorQuad g direction=0) :
    0≤tensorQuad (covectorStress g gInv w coupling) direction := by
  rw [covector_stress_null g gInv w direction coupling hn]
  exact mul_nonneg hc (sq_nonneg _)

theorem response_equals_negative_null_stress (a b u v : ℝ) (g gInv : Tensor4)
    (w direction : Coordinate4) (hn : tensorQuad g direction=0) :
    unitaryResponse a b (covectorRead w direction) u v=
      -Real.pi*tensorQuad (covectorStress g gInv w (coherentCoupling a b u v)) direction := by
  rw [covector_stress_null g gInv w direction _ hn,response_coupling_identity]
  ring

theorem covector_stress_field_smooth (U : Set Coordinate4) (g gInv : TensorField4)
    (w : CovectorField4) (coupling : ℝ) (hg : SmoothMatrixOn U g)
    (hgi : SmoothMatrixOn U gInv) (hw : SmoothVectorOn U w) :
    SmoothMatrixOn U (covectorStressField g gInv w coupling) := by
  unfold SmoothMatrixOn at hg hgi ⊢
  unfold SmoothVectorOn at hw
  intro i j
  simp only [covectorStressField,covectorStress,Matrix.smul_apply,Matrix.sub_apply,
    Matrix.vecMulVec,Matrix.of_apply,smul_eq_mul,tensorQuad,Matrix.mulVec,dotProduct]
  fun_prop

theorem covector_stress_zero (g gInv : Tensor4) (coupling : ℝ) :
    covectorStress g gInv 0 coupling=0 := by
  ext i j
  simp [covectorStress,tensorQuad,Matrix.vecMulVec]

#print axioms response_coupling_identity
#print axioms coherent_negative_control_coupling_positive
#print axioms covector_stress_symmetric
#print axioms covector_stress_quad
#print axioms covector_stress_null
#print axioms covector_stress_null_nonnegative
#print axioms response_equals_negative_null_stress
#print axioms covector_stress_field_smooth
#print axioms covector_stress_zero
end
end ChatgptAudit.Coherent023
