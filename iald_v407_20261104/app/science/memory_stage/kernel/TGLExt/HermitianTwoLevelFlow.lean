-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_022 (05-06/09/2026), transposta em 06/09/2026
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
import TGLExt.RelativeEntropyGravityControls

set_option autoImplicit false
set_option maxHeartbeats 7500000
namespace ChatgptAudit.Unitary022
open Matrix Filter Topology Set
noncomputable section

abbrev PairMatrix := Matrix (Fin 2) (Fin 2) ℂ

def axisHamiltonian (a b : ℝ) : PairMatrix := !![(a:ℂ),(b:ℂ);(b:ℂ),(-a:ℂ)]
def pairHamiltonian (a b frequency : ℝ) : PairMatrix := (frequency:ℂ) • axisHamiltonian a b
def pairFlow (a b frequency t : ℝ) : PairMatrix :=
  (Real.cos (frequency*t):ℂ) • 1+
    (-Complex.I*(Real.sin (frequency*t):ℂ)) • axisHamiltonian a b

theorem axis_hermitian (a b : ℝ) : (axisHamiltonian a b)ᴴ=axisHamiltonian a b := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [axisHamiltonian,Matrix.conjTranspose_apply]

theorem axis_square (a b : ℝ) (h : a^2+b^2=1) :
    axisHamiltonian a b*axisHamiltonian a b=1 := by
  have hc : (a:ℂ)*(a:ℂ)+(b:ℂ)*(b:ℂ)=1 := by
    exact_mod_cast (show a*a+b*b=1 by nlinarith [h])
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [axisHamiltonian,Matrix.mul_apply,Fin.sum_univ_two,hc,add_comm] <;> ring

theorem pair_hamiltonian_hermitian (a b frequency : ℝ) :
    (pairHamiltonian a b frequency)ᴴ=pairHamiltonian a b frequency := by
  simp [pairHamiltonian,Matrix.conjTranspose_smul,axis_hermitian]

theorem axis_polynomial_product (A : PairMatrix) (hA : A*A=1) (x y z w : ℂ) :
    (x • (1:PairMatrix)+y • A)*(z • (1:PairMatrix)+w • A)=
      (x*z+y*w) • (1:PairMatrix)+(x*w+y*z) • A := by
  simp only [add_mul,mul_add,smul_mul_assoc,mul_smul_comm,one_mul,mul_one,hA]
  ext i j
  simp only [Matrix.add_apply,Matrix.smul_apply,smul_eq_mul]
  ring

theorem pair_flow_zero (a b frequency : ℝ) : pairFlow a b frequency 0=1 := by
  simp [pairFlow]

theorem pair_flow_group (a b frequency s t : ℝ) (h : a^2+b^2=1) :
    pairFlow a b frequency s*pairFlow a b frequency t=pairFlow a b frequency (s+t) := by
  unfold pairFlow
  rw [axis_polynomial_product _ (axis_square a b h)]
  have hc : (Real.cos (frequency*s):ℂ)*(Real.cos (frequency*t):ℂ)+
      (-Complex.I*(Real.sin (frequency*s):ℂ))*(-Complex.I*(Real.sin (frequency*t):ℂ))=
      (Real.cos (frequency*(s+t)):ℂ) := by
    simp only [mul_add,Real.cos_add,Complex.ofReal_sub,Complex.ofReal_mul]
    linear_combination ((Real.sin (frequency*s):ℂ)*(Real.sin (frequency*t):ℂ))*Complex.I_sq
  have hs : (Real.cos (frequency*s):ℂ)*(-Complex.I*(Real.sin (frequency*t):ℂ))+
      (-Complex.I*(Real.sin (frequency*s):ℂ))*(Real.cos (frequency*t):ℂ)=
      -Complex.I*(Real.sin (frequency*(s+t)):ℂ) := by
    simp only [mul_add,Real.sin_add,Complex.ofReal_add,Complex.ofReal_mul]
    ring
  rw [hc,hs]

theorem pair_flow_adjoint (a b frequency t : ℝ) :
    (pairFlow a b frequency t)ᴴ=pairFlow a b frequency (-t) := by
  unfold pairFlow
  rw [Matrix.conjTranspose_add,Matrix.conjTranspose_smul,Matrix.conjTranspose_smul,
    Matrix.conjTranspose_one,axis_hermitian]
  simp only [Complex.star_def,map_mul,map_neg,Complex.conj_I,Complex.conj_ofReal,mul_neg,
    Real.cos_neg,Real.sin_neg,Complex.ofReal_neg,neg_mul,neg_neg]

theorem pair_flow_adjoint_mul (a b frequency t : ℝ) (h : a^2+b^2=1) :
    (pairFlow a b frequency t)ᴴ*pairFlow a b frequency t=1 := by
  rw [pair_flow_adjoint,pair_flow_group a b frequency (-t) t h,neg_add_cancel,pair_flow_zero]

theorem pair_flow_mul_adjoint (a b frequency t : ℝ) (h : a^2+b^2=1) :
    pairFlow a b frequency t*(pairFlow a b frequency t)ᴴ=1 := by
  rw [pair_flow_adjoint,pair_flow_group a b frequency t (-t) h,add_neg_cancel,pair_flow_zero]

theorem pair_hamiltonian_commutes (a b frequency t : ℝ) :
    pairHamiltonian a b frequency*pairFlow a b frequency t=
      pairFlow a b frequency t*pairHamiltonian a b frequency := by
  simp only [pairHamiltonian,pairFlow,mul_add,add_mul,smul_mul_assoc,mul_smul_comm,
    smul_smul,one_mul,mul_one]
  ext i j
  simp only [Matrix.add_apply,Matrix.smul_apply,smul_eq_mul]
  ring

theorem pair_energy_conserved (a b frequency t : ℝ) (h : a^2+b^2=1) :
    (pairFlow a b frequency t)ᴴ*pairHamiltonian a b frequency*pairFlow a b frequency t=
      pairHamiltonian a b frequency := by
  rw [Matrix.mul_assoc,pair_hamiltonian_commutes,←Matrix.mul_assoc,pair_flow_adjoint_mul a b frequency t h,one_mul]

#print axioms axis_hermitian
#print axioms axis_square
#print axioms pair_hamiltonian_hermitian
#print axioms axis_polynomial_product
#print axioms pair_flow_zero
#print axioms pair_flow_group
#print axioms pair_flow_adjoint
#print axioms pair_flow_adjoint_mul
#print axioms pair_flow_mul_adjoint
#print axioms pair_hamiltonian_commutes
#print axioms pair_energy_conserved
end
end ChatgptAudit.Unitary022
