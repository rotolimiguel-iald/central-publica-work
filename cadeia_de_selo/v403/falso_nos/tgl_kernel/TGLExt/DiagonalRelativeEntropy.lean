-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_021 (05-06/09/2026), transposta em 06/09/2026
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
import TGLExt.ConstructedClausiusControls

set_option autoImplicit false
set_option maxHeartbeats 4000000
namespace ChatgptAudit.Micro021
open Matrix Filter Topology Set
noncomputable section
variable {ι : Type} [Fintype ι]

def diagonalRelativeEntropy (r p : ι → ℝ) : ℝ :=
  ∑ i, r i*(Real.log (r i)-Real.log (p i))

def modularIncrement (p r : ι → ℝ) : ℝ :=
  ∑ i, (r i-p i)*(-Real.log (p i))

def diagonalFisher (p q : ι → ℝ) : ℝ := ∑ i, q i^2/p i

theorem relative_entropy_identity (r p : ι → ℝ) :
    diagonalRelativeEntropy r p=modularIncrement p r-(finiteEntropy r-finiteEntropy p) := by
  unfold diagonalRelativeEntropy modularIncrement finiteEntropy entropyAtom
  simp only [←Finset.sum_sub_distrib]
  apply Finset.sum_congr rfl
  intro i _
  ring

theorem relative_entropy_self (p : ι → ℝ) : diagonalRelativeEntropy p p=0 := by
  simp [diagonalRelativeEntropy]

theorem modular_increment_self (p : ι → ℝ) : modularIncrement p p=0 := by
  simp [modularIncrement]

theorem diagonal_fisher_nonneg (p q : ι → ℝ) (hp : ∀ i, 0<p i) :
    0≤diagonalFisher p q := by
  apply Finset.sum_nonneg
  intro i _
  exact div_nonneg (sq_nonneg _) (le_of_lt (hp i))

theorem diagonal_fisher_zero_iff (p q : ι → ℝ) (hp : ∀ i, 0<p i) :
    diagonalFisher p q=0 ↔ q=0 := by
  constructor
  · intro h
    funext i
    by_contra hn
    have hi : 0<q i^2/p i := div_pos (sq_pos_of_ne_zero hn) (hp i)
    have hs : q i^2/p i≤diagonalFisher p q :=
      Finset.single_le_sum (fun j _ => div_nonneg (sq_nonneg _) (le_of_lt (hp j))) (Finset.mem_univ i)
    rw [h] at hs
    linarith
  · intro h
    simp [h,diagonalFisher]

theorem diagonal_fisher_pos_iff (p q : ι → ℝ) (hp : ∀ i, 0<p i) :
    0<diagonalFisher p q ↔ q≠0 := by
  constructor
  · intro hf hq
    have hz := (diagonal_fisher_zero_iff p q hp).mpr hq
    linarith
  · intro hq
    have hf := diagonal_fisher_nonneg p q hp
    have hn := (diagonal_fisher_zero_iff p q hp).not.mpr hq
    rcases lt_or_eq_of_le hf with h|h
    · exact h
    · exact False.elim (hn h.symm)

#print axioms relative_entropy_identity
#print axioms relative_entropy_self
#print axioms modular_increment_self
#print axioms diagonal_fisher_nonneg
#print axioms diagonal_fisher_zero_iff
#print axioms diagonal_fisher_pos_iff
end
end ChatgptAudit.Micro021
