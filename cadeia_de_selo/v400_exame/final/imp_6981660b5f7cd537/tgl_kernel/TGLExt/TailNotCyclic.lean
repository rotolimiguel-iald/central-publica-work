-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_007 (05-06/09/2026), transposta em 06/09/2026
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
import TGLExt.ChainTailClosure
import TGLExt.ChainVolumePositive
import TGLExt.TracialCentralizerExpectation

set_option autoImplicit false
set_option maxHeartbeats 1200000
namespace ChatgptAudit
open TGLExt Matrix
noncomputable section
variable {P : SiteProfile}

theorem tail_prefix_expectation_scalar (N : ℕ)
    (x : TowerHilbert P →L[ℂ] TowerHilbert P) (hx : x ∈ chainTailClosure P (N+1)) :
    towerExpectation P N x = omegaState P x • (1 : TowerHilbert P →L[ℂ] TowerHilbert P) := by
  have hc : ∀ a : Matrix (chainIdx N) (chainIdx N) ℂ, towerPi P a*x=x*towerPi P a := by
    intro a
    have hh := hx
    change x ∈ StarSubalgebra.centralizer ℂ
      ((StarSubalgebra.centralizer ℂ (chainLocalAlgebra P (Set.Ici (N+1)) : Set _) :
        StarSubalgebra ℂ (TowerHilbert P →L[ℂ] TowerHilbert P)) : Set _) at hh
    rw [StarSubalgebra.mem_centralizer_iff] at hh
    exact (hh _ (prefix_mem_tail_commutant N a)).1
  obtain ⟨c,he⟩ := expectation_central_scalar N x (chain_tail_mem_factor _ hx) hc
  have hw := expectation_preserves_state N x
  rw [he,omega_scalar] at hw
  simpa only [hw] using he

theorem tail_mark_factorization (x : TowerHilbert P →L[ℂ] TowerHilbert P)
    (hx : x ∈ chainTailClosure P 1) :
    omegaState P (siteMark P 0*x) = (P.w 0:ℂ)*omegaState P x := by
  have he := expectation_bimodular 0 (Matrix.single (0:Fin 2) 0 (1:ℂ)) 1 x
    (chain_tail_mem_factor _ hx)
  simp only [towerPi_one,mul_one] at he
  change towerExpectation P 0 (siteMark P 0*x) = siteMark P 0*towerExpectation P 0 x at he
  rw [← expectation_preserves_state 0 (siteMark P 0*x),he,tail_prefix_expectation_scalar 0 x hx,
    mul_smul_comm,mul_one]
  change inner ℂ (hOmega P) (omegaState P x • siteMark P 0 (hOmega P)) = _
  rw [inner_smul_right]
  change omegaState P x * omegaState P (siteMark P 0) = _
  rw [siteMark_state,mul_comm]

def tailWitness (P : SiteProfile) : TowerHilbert P :=
  siteMark P 0 (hOmega P) - (P.w 0:ℂ) • hOmega P

theorem tail_witness_orthogonal (x : TowerHilbert P →L[ℂ] TowerHilbert P)
    (hx : x ∈ chainTailClosure P 1) : inner ℂ (tailWitness P) (x (hOmega P)) = 0 := by
  have he : inner ℂ (siteMark P 0 (hOmega P)) (x (hOmega P)) = omegaState P (siteMark P 0*x) := by
    rw [omega_product_inner,siteMark_star]
  rw [tailWitness,inner_sub_left,inner_smul_left,he]
  simp only [Complex.conj_ofReal]
  change omegaState P (siteMark P 0*x) - (P.w 0:ℂ)*omegaState P x = 0
  rw [tail_mark_factorization x hx,sub_self]

theorem tail_witness_inner : inner ℂ (tailWitness P) (tailWitness P) = (P.w 0*(1-P.w 0):ℝ) := by
  have hee : inner ℂ (siteMark P 0 (hOmega P)) (siteMark P 0 (hOmega P)) = (P.w 0:ℂ) := by
    have h := omega_product_inner (P := P) (siteMark P 0) (siteMark P 0)
    rw [siteMark_square,siteMark_star,siteMark_state] at h
    exact h.symm
  have heo : inner ℂ (siteMark P 0 (hOmega P)) (hOmega P) = (P.w 0:ℂ) := by
    have h := omega_product_inner (P := P) (siteMark P 0) 1
    simp only [mul_one,siteMark_star,one_apply_eq_self] at h
    rw [← h,siteMark_state]
  have hoe : inner ℂ (hOmega P) (siteMark P 0 (hOmega P)) = (P.w 0:ℂ) := siteMark_state 0
  simp only [tailWitness,inner_sub_left,inner_sub_right,inner_smul_left,inner_smul_right,
    Complex.conj_ofReal,hee,heo,hoe,hOmega_inner_self]
  push_cast
  ring

theorem tail_witness_norm_sq : ‖tailWitness P‖^2 = P.w 0*(1-P.w 0) := by
  rw [norm_sq_eq_re_inner (𝕜 := ℂ),tail_witness_inner]
  rfl

theorem tail_witness_ne_zero : tailWitness P ≠ 0 := by
  intro h
  have hn := tail_witness_norm_sq (P := P)
  rw [h,norm_zero,zero_pow (by decide : 2 ≠ 0)] at hn
  have hp := mul_pos (P.pos 0) (sub_pos.mpr (P.lt_one 0))
  linarith

theorem tail_not_cyclic :
    ¬ Dense ((fun x : TowerHilbert P →L[ℂ] TowerHilbert P => x (hOmega P)) ''
      (chainTailClosure P 1 : Set (TowerHilbert P →L[ℂ] TowerHilbert P))) := by
  intro hd
  have hclosed : IsClosed {v : TowerHilbert P | inner ℂ (tailWitness P) v = 0} :=
    isClosed_eq (continuous_const.inner continuous_id) continuous_const
  have hsub : ((fun x : TowerHilbert P →L[ℂ] TowerHilbert P => x (hOmega P)) ''
      (chainTailClosure P 1 : Set (TowerHilbert P →L[ℂ] TowerHilbert P))) ⊆
      {v : TowerHilbert P | inner ℂ (tailWitness P) v=0} := by
    rintro _ ⟨x,hx,rfl⟩
    exact tail_witness_orthogonal x hx
  have hz := closure_minimal hsub hclosed (hd (tailWitness P))
  exact tail_witness_ne_zero (inner_self_eq_zero.mp hz)

#print axioms tail_prefix_expectation_scalar
#print axioms tail_mark_factorization
#print axioms tail_witness_orthogonal
#print axioms tail_witness_inner
#print axioms tail_witness_norm_sq
#print axioms tail_witness_ne_zero
#print axioms tail_not_cyclic
end
end ChatgptAudit
