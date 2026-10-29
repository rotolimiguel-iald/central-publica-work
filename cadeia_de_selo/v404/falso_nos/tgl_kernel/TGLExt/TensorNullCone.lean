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
import TGLExt.GeneralNullCone
import TGLExt.EmergenceTriad

set_option autoImplicit false
set_option maxHeartbeats 1800000
namespace ChatgptAudit
open Matrix TGLExt
noncomputable section

abbrev SpacetimeVector := Fin 4 → ℝ
abbrev Tensor4 := Matrix (Fin 4) (Fin 4) ℝ

def tensorQuad (A : Tensor4) (v : SpacetimeVector) : ℝ := v ⬝ᵥ (A *ᵥ v)

theorem tensorQuad_single (A : Tensor4) (i : Fin 4) :
    tensorQuad A (Pi.single i 1) = A i i := by
  simp [tensorQuad,Matrix.mulVec,dotProduct,Pi.single_apply]

theorem tensorQuad_single_add (A : Tensor4) (i j : Fin 4) :
    tensorQuad A (Pi.single i 1+Pi.single j 1) = A i i+A i j+A j i+A j j := by
  simp only [tensorQuad,Matrix.mulVec_add,dotProduct_add,add_dotProduct]
  simp [Matrix.mulVec,dotProduct,Pi.single_apply]
  ring

theorem symmetric_tensor_ext {A B : Tensor4} (hA : Aᵀ=A) (hB : Bᵀ=B)
    (hq : ∀ v, tensorQuad A v=tensorQuad B v) : A=B := by
  ext i j
  have hi := hq (Pi.single i 1)
  have hj := hq (Pi.single j 1)
  have hij := hq (Pi.single i 1+Pi.single j 1)
  rw [tensorQuad_single,tensorQuad_single] at hi hj
  rw [tensorQuad_single_add,tensorQuad_single_add] at hij
  have ha : A j i=A i j := congrArg (fun C : Tensor4 => C i j) hA
  have hb : B j i=B i j := congrArg (fun C : Tensor4 => C i j) hB
  linarith

theorem tensorQuad_congruence (E A : Tensor4) (v : SpacetimeVector) :
    tensorQuad (Eᵀ*A*E) v=tensorQuad A (E*ᵥv) := by
  unfold tensorQuad
  rw [← Matrix.mulVec_mulVec,← Matrix.mulVec_mulVec,dotProduct_mulVec,
    ← Matrix.mulVec_transpose,Matrix.transpose_transpose]

theorem tensorQuad_eta (t x y z : ℝ) :
    tensorQuad eta4 ![t,x,y,z]=t^2-x^2-y^2-z^2 := by
  simp [tensorQuad,eta4,Matrix.mulVec,dotProduct,Fin.sum_univ_four]
  ring

theorem tensorQuad_components (A : Tensor4) (hA : Aᵀ=A) (t x y z : ℝ) :
    tensorQuad A ![t,x,y,z] = symmetricForm4
      (A 0 0) (A 1 1) (A 2 2) (A 3 3) (A 0 1) (A 0 2) (A 0 3) (A 1 2) (A 1 3) (A 2 3)
      t x y z := by
  have hs (i j : Fin 4) : A j i=A i j := congrArg (fun C : Tensor4 => C i j) hA
  simp [tensorQuad,Matrix.mulVec,dotProduct,Fin.sum_univ_four,symmetricForm4,
    hs 0 1,hs 0 2,hs 0 3,hs 1 2,hs 1 3,hs 2 3]
  ring

theorem minkowski_tensor_null_rigidity (A : Tensor4) (hA : Aᵀ=A)
    (hc : ∀ v, tensorQuad eta4 v=0 → tensorQuad A v=0) : A=(A 0 0) • eta4 := by
  have h := general_null_cone_rigidity (A 0 0) (A 1 1) (A 2 2) (A 3 3)
    (A 0 1) (A 0 2) (A 0 3) (A 1 2) (A 1 3) (A 2 3) (by
      intro t x y z he
      rw [← tensorQuad_components A hA]
      apply hc
      rw [tensorQuad_eta]
      linarith)
  apply symmetric_tensor_ext hA (by simp [eta4,Matrix.diagonal_transpose])
  intro v
  have hv : v=![v 0,v 1,v 2,v 3] := by ext i; fin_cases i <;> rfl
  rw [hv,tensorQuad_components A hA,h]
  have hs : tensorQuad ((A 0 0) • eta4) ![v 0,v 1,v 2,v 3] =
      (A 0 0)*tensorQuad eta4 ![v 0,v 1,v 2,v 3] := by
    simp [tensorQuad,Matrix.smul_mulVec,dotProduct_smul,smul_eq_mul]
  rw [hs,tensorQuad_eta]

theorem congruence_symmetric (D A : Tensor4) (hA : Aᵀ=A) : (Dᵀ*A*D)ᵀ=Dᵀ*A*D := by
  simp only [Matrix.transpose_mul,Matrix.transpose_transpose,hA,Matrix.mul_assoc]

theorem congruence_undo (D E A : Tensor4) (hDE : D*E=1) : Eᵀ*(Dᵀ*A*D)*E=A := by
  calc
    Eᵀ*(Dᵀ*A*D)*E=(D*E)ᵀ*A*(D*E) := by rw [Matrix.transpose_mul]; noncomm_ring
    _ = A := by rw [hDE,Matrix.transpose_one,one_mul,mul_one]

theorem lorentz_tensor_null_rigidity (A g : Tensor4) (hA : Aᵀ=A)
    (hg : LorentzByCongruence g)
    (hc : ∀ v, tensorQuad g v=0 → tensorQuad A v=0) : ∃ c : ℝ, A=c • g := by
  obtain ⟨E,hE,hg⟩ := hg
  let D := E⁻¹
  have hDE : D*E=1 := Matrix.nonsing_inv_mul E hE
  have hED : E*D=1 := Matrix.mul_nonsing_inv E hE
  have hp : ∀ v, tensorQuad eta4 v=0 → tensorQuad (Dᵀ*A*D) v=0 := by
    intro v hv
    rw [tensorQuad_congruence]
    apply hc
    rw [hg,tensorQuad_congruence,Matrix.mulVec_mulVec,hED,Matrix.one_mulVec]
    exact hv
  have hr := minkowski_tensor_null_rigidity (Dᵀ*A*D) (congruence_symmetric D A hA) hp
  refine ⟨(Dᵀ*A*D) 0 0,?_⟩
  have ht := congrArg (fun C : Tensor4 => Eᵀ*C*E) hr
  rw [congruence_undo D E A hDE] at ht
  simpa only [Matrix.mul_smul,Matrix.smul_mul,hg] using ht

#print axioms tensorQuad_single
#print axioms tensorQuad_single_add
#print axioms symmetric_tensor_ext
#print axioms tensorQuad_congruence
#print axioms tensorQuad_eta
#print axioms tensorQuad_components
#print axioms minkowski_tensor_null_rigidity
#print axioms congruence_symmetric
#print axioms congruence_undo
#print axioms lorentz_tensor_null_rigidity
end
end ChatgptAudit
