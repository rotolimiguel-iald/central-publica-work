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
import TGLExt.UnitaryResponseControls

set_option autoImplicit false
set_option maxHeartbeats 7500000
namespace ChatgptAudit.Coherent023
open Matrix Filter Topology Set ChatgptAudit.Unitary022
noncomputable section

abbrev CovectorField4 := Coordinate4 → Coordinate4

def covectorRead (w direction : Coordinate4) : ℝ := w ⬝ᵥ direction

def directionalHamiltonian (a b : ℝ) (w direction : Coordinate4) : PairMatrix :=
  pairHamiltonian a b (covectorRead w direction)

def directionalFlow (a b : ℝ) (w direction : Coordinate4) (t : ℝ) : PairMatrix :=
  pairFlow a b (covectorRead w direction) t

def responseTensor (a b u v : ℝ) (w : Coordinate4) : Tensor4 :=
  unitaryResponse a b 1 u v • Matrix.vecMulVec w w

theorem covector_read_add (w direction other : Coordinate4) :
    covectorRead w (direction+other)=covectorRead w direction+covectorRead w other :=
  dotProduct_add _ _ _

theorem covector_read_smul (w direction : Coordinate4) (c : ℝ) :
    covectorRead w (c • direction)=c*covectorRead w direction := by
  simp [covectorRead,dotProduct_smul,smul_eq_mul]

theorem directional_hamiltonian_add (a b : ℝ) (w direction other : Coordinate4) :
    directionalHamiltonian a b w (direction+other)=
      directionalHamiltonian a b w direction+directionalHamiltonian a b w other := by
  simp [directionalHamiltonian,pairHamiltonian,covector_read_add,add_smul]

theorem pair_flow_reparameterized (a b frequency t : ℝ) :
    pairFlow a b frequency t=pairFlow a b 1 (frequency*t) := by
  simp [pairFlow]

theorem directional_flow_add (a b : ℝ) (h : a^2+b^2=1)
    (w direction other : Coordinate4) (t : ℝ) :
    directionalFlow a b w (direction+other) t=
      directionalFlow a b w direction t*directionalFlow a b w other t := by
  unfold directionalFlow
  rw [pair_flow_reparameterized a b (covectorRead w (direction+other)) t,
    pair_flow_reparameterized a b (covectorRead w direction) t,
    pair_flow_reparameterized a b (covectorRead w other) t,
    pair_flow_group a b 1 _ _ h,covector_read_add,add_mul]

theorem directional_flow_unitary (a b : ℝ) (h : a^2+b^2=1)
    (w direction : Coordinate4) (t : ℝ) :
    (directionalFlow a b w direction t)ᴴ*directionalFlow a b w direction t=1 :=
  pair_flow_adjoint_mul a b (covectorRead w direction) t h

theorem directional_kernel_trivial_flow (a b : ℝ) (w direction : Coordinate4) (t : ℝ)
    (h : covectorRead w direction=0) : directionalFlow a b w direction t=1 := by
  simp [directionalFlow,h,pairFlow]

theorem unitary_response_frequency_square (a b frequency u v : ℝ) :
    unitaryResponse a b frequency u v=frequency^2*unitaryResponse a b 1 u v := by
  unfold unitaryResponse
  ring

theorem outer_tensor_symmetric (w : Coordinate4) : (Matrix.vecMulVec w w)ᵀ=Matrix.vecMulVec w w := by
  ext i j
  simp only [Matrix.transpose_apply,Matrix.vecMulVec,Matrix.of_apply]
  ring

theorem outer_tensor_quad (w direction : Coordinate4) :
    tensorQuad (Matrix.vecMulVec w w) direction=(covectorRead w direction)^2 := by
  simp only [tensorQuad,covectorRead,Matrix.mulVec,dotProduct,Matrix.vecMulVec,Matrix.of_apply,Fin.sum_univ_four]
  ring

theorem response_tensor_symmetric (a b u v : ℝ) (w : Coordinate4) :
    (responseTensor a b u v w)ᵀ=responseTensor a b u v w := by
  rw [responseTensor,Matrix.transpose_smul,outer_tensor_symmetric]

theorem response_tensor_quad (a b u v : ℝ) (w direction : Coordinate4) :
    tensorQuad (responseTensor a b u v w) direction=
      unitaryResponse a b (covectorRead w direction) u v := by
  simp only [responseTensor,tensorQuad,Matrix.smul_mulVec,dotProduct_smul,smul_eq_mul]
  change unitaryResponse a b 1 u v*tensorQuad (Matrix.vecMulVec w w) direction=_
  rw [outer_tensor_quad,unitary_response_frequency_square a b (covectorRead w direction) u v]
  ring

theorem covector_read_change_basis (E : Tensor4) (w direction : Coordinate4) :
    covectorRead (Eᵀ *ᵥ w) direction=covectorRead w (E *ᵥ direction) := by
  simp only [covectorRead,Matrix.mulVec,dotProduct,Matrix.transpose_apply,Fin.sum_univ_four]
  ring

theorem outer_tensor_change_basis (E : Tensor4) (w : Coordinate4) :
    Matrix.vecMulVec (Eᵀ *ᵥ w) (Eᵀ *ᵥ w)=Eᵀ*Matrix.vecMulVec w w*E := by
  apply symmetric_tensor_ext (outer_tensor_symmetric _) (congruence_symmetric E _ (outer_tensor_symmetric w))
  intro direction
  rw [outer_tensor_quad,tensorQuad_congruence,outer_tensor_quad,covector_read_change_basis]

#print axioms covector_read_add
#print axioms covector_read_smul
#print axioms directional_hamiltonian_add
#print axioms pair_flow_reparameterized
#print axioms directional_flow_add
#print axioms directional_flow_unitary
#print axioms directional_kernel_trivial_flow
#print axioms unitary_response_frequency_square
#print axioms outer_tensor_symmetric
#print axioms outer_tensor_quad
#print axioms response_tensor_symmetric
#print axioms response_tensor_quad
#print axioms covector_read_change_basis
#print axioms outer_tensor_change_basis
end
end ChatgptAudit.Coherent023
