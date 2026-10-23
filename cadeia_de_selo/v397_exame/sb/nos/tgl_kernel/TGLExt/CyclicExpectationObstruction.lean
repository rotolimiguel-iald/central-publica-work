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
import TGLExt.TracialCentralizerExpectation

set_option autoImplicit false
namespace ChatgptAudit
open TGLExt
noncomputable section
variable {P : SiteProfile}

structure SubalgebraExpectationInput (P : SiteProfile)
    (N : StarSubalgebra ℂ (TowerHilbert P →L[ℂ] TowerHilbert P)) where
  E : (TowerHilbert P →L[ℂ] TowerHilbert P) → (TowerHilbert P →L[ℂ] TowerHilbert P)
  into : ∀ x ∈ theFactorObject P, E x ∈ N
  fixes : ∀ x ∈ N, E x=x
  ortho : ∀ x ∈ theFactorObject P, ∀ b ∈ N, omegaState P (star b*(x-E x))=0

theorem cyclic_expectation_forces_identity
    (N : StarSubalgebra ℂ (TowerHilbert P →L[ℂ] TowerHilbert P))
    (hNM : ∀ x ∈ N, x ∈ theFactorObject P) (F : SubalgebraExpectationInput P N)
    (hcyclic : Dense ((fun x : TowerHilbert P →L[ℂ] TowerHilbert P => x (hOmega P)) '' (N : Set _)))
    (x : TowerHilbert P →L[ℂ] TowerHilbert P) (hx : x ∈ theFactorObject P) : F.E x=x := by
  let d := (x-F.E x) (hOmega P)
  have hclosed : IsClosed {v : TowerHilbert P | inner ℂ v d=0} :=
    isClosed_eq (continuous_id.inner continuous_const) continuous_const
  have hsub : ((fun b : TowerHilbert P →L[ℂ] TowerHilbert P => b (hOmega P)) '' (N : Set _)) ⊆
      {v : TowerHilbert P | inner ℂ v d=0} := by
    rintro _ ⟨b,hb,rfl⟩
    have h := F.ortho x hx b hb
    rw [omega_product_inner,star_star] at h
    exact h
  have hz := inner_self_eq_zero.mp (closure_minimal hsub hclosed (hcyclic d))
  symm
  apply factor_eq_of_omega hx (hNM _ (F.into x hx))
  exact sub_eq_zero.mp hz

theorem cyclic_expectation_forces_full_algebra
    (N : StarSubalgebra ℂ (TowerHilbert P →L[ℂ] TowerHilbert P))
    (hNM : ∀ x ∈ N, x ∈ theFactorObject P) (F : SubalgebraExpectationInput P N)
    (hcyclic : Dense ((fun x : TowerHilbert P →L[ℂ] TowerHilbert P => x (hOmega P)) '' (N : Set _))) :
    ∀ x, x ∈ N ↔ x ∈ theFactorObject P := by
  intro x
  refine ⟨hNM x,fun hx => ?_⟩
  rw [← cyclic_expectation_forces_identity N hNM F hcyclic x hx]
  exact F.into x hx

theorem proper_expected_subalgebra_not_cyclic
    (N : StarSubalgebra ℂ (TowerHilbert P →L[ℂ] TowerHilbert P))
    (hNM : ∀ x ∈ N, x ∈ theFactorObject P) (F : SubalgebraExpectationInput P N)
    (hproper : ∃ x ∈ theFactorObject P, x ∉ N) :
    ¬ Dense ((fun x : TowerHilbert P →L[ℂ] TowerHilbert P => x (hOmega P)) '' (N : Set _)) := by
  intro hc
  obtain ⟨x,hx,hn⟩ := hproper
  exact hn ((cyclic_expectation_forces_full_algebra N hNM F hc x).mpr hx)

#print axioms cyclic_expectation_forces_identity
#print axioms cyclic_expectation_forces_full_algebra
#print axioms proper_expected_subalgebra_not_cyclic
end
end ChatgptAudit
