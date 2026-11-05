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
import TGLExt.PeriodicBorchersObstruction
import TGLExt.ModularFlowSpectrum
import TGLExt.ExpectationProjection

set_option autoImplicit false
set_option maxHeartbeats 1200000
namespace ChatgptAudit
open TGLExt Filter Topology
noncomputable section
variable {P : SiteProfile}

theorem eigenvector_diagonal_modular_invariant (t : ℝ)
    (x : TowerHilbert P →L[ℂ] TowerHilbert P) (N : ℕ) (i j : chainIdx N) :
    inner ℂ (localEigenvector P N i j) (modularConjugation P t x (localEigenvector P N i j)) =
      inner ℂ (localEigenvector P N i j) (x (localEigenvector P N i j)) := by
  change inner ℂ (localEigenvector P N i j)
    (modularFlow P t (x (modularFlow P (-t) (localEigenvector P N i j)))) = _
  rw [flow_inner_transport,modularFlow_eigenvector,map_smul,inner_smul_left,inner_smul_right,
    ← mul_assoc,Complex.conj_mul',modularPhase_norm,Complex.ofReal_one,one_pow,one_mul]

theorem isometry_fixed_of_diagonal
    (V : TowerHilbert P →L[ℂ] TowerHilbert P) (v : TowerHilbert P)
    (hn : ‖V v‖=‖v‖) (hi : inner ℂ v (V v)=inner ℂ v v) : V v=v := by
  have he := norm_sub_sq (𝕜 := ℂ) v (V v)
  rw [hn,hi,← norm_sq_eq_re_inner (𝕜 := ℂ)] at he
  have hz : ‖v-V v‖=0 := by nlinarith [norm_nonneg (v-V v)]
  exact (sub_eq_zero.mp (norm_eq_zero.mp hz)).symm

theorem product_borchers_fixes_eigenvector
    (V : ℝ → (TowerHilbert P →L[ℂ] TowerHilbert P))
    (hcont : ∀ v, ContinuousAt (fun a => V a v) 0) (hzero : V 0=1)
    (hnorm : ∀ a v, ‖V a v‖=‖v‖)
    (hborchers : ∀ t a, modularConjugation P t (V a)=V (Real.exp (-2*Real.pi*t)*a))
    (a : ℝ) (N : ℕ) (i j : chainIdx N) :
    V a (localEigenvector P N i j)=localEigenvector P N i j := by
  let v := localEigenvector P N i j
  have hf : ContinuousAt (fun a => inner ℂ v (V a v)) 0 := continuousAt_const.inner (hcont v)
  have hinv (b : ℝ) : inner ℂ v (V (Real.exp (-2*Real.pi)*b) v)=inner ℂ v (V b v) := by
    have h := eigenvector_diagonal_modular_invariant (P := P) 1 (V b) N i j
    rw [hborchers,mul_one] at h
    exact h
  have hc : Real.exp (-2*Real.pi)<1 := Real.exp_lt_one_iff.mpr (by nlinarith [Real.pi_pos])
  have hh := contraction_invariant_continuous_constant (fun a => inner ℂ v (V a v)) hf
    (le_of_lt (Real.exp_pos _)) hc hinv a
  rw [hzero,one_apply_eq_self] at hh
  exact isometry_fixed_of_diagonal (V a) v (hnorm a v) hh

theorem product_borchers_trivial
    (V : ℝ → (TowerHilbert P →L[ℂ] TowerHilbert P))
    (hcont : ∀ v, ContinuousAt (fun a => V a v) 0) (hzero : V 0=1)
    (hnorm : ∀ a v, ‖V a v‖=‖v‖)
    (hborchers : ∀ t a, modularConjugation P t (V a)=V (Real.exp (-2*Real.pi*t)*a)) :
    ∀ a, V a=1 := by
  intro a
  have hspan : ∀ v ∈ Submodule.span ℂ (localEigenvectors P), V a v=v := by
    intro v hv
    induction hv using Submodule.span_induction with
    | mem v hv =>
      obtain ⟨N,i,j,rfl⟩ := hv
      exact product_borchers_fixes_eigenvector V hcont hzero hnorm hborchers a N i j
    | zero => exact map_zero _
    | add v w hv hw he hf => rw [map_add,he,hf]
    | smul c v hv he => rw [map_smul,he]
  ext v
  exact closure_minimal hspan (isClosed_eq (V a).continuous continuous_id)
    (localEigenvectors_total (P := P) v)

#print axioms eigenvector_diagonal_modular_invariant
#print axioms isometry_fixed_of_diagonal
#print axioms product_borchers_fixes_eigenvector
#print axioms product_borchers_trivial
end
end ChatgptAudit
