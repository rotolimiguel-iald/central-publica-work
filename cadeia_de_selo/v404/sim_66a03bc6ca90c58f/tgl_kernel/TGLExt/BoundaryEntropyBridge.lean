-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_011 (05-06/09/2026), transposta em 06/09/2026
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
import TGLExt.TowerEntropyScaling
import TGLExt.SchmidtCutPurification

set_option autoImplicit false
set_option maxHeartbeats 2200000
namespace ChatgptAudit
open Matrix TGLExt
open scoped Kronecker ComplexOrder
noncomputable section

def towerCutDensity (P : SiteProfile) (N : ℕ) :
    Matrix (chainIdx N × chainIdx N) (chainIdx N × chainIdx N) ℂ :=
  pureCutDensity (towerW P N)

def reducedDiagonalEntropy {ι : Type} [Fintype ι]
    (rho : Matrix (ι × ι) (ι × ι) ℂ) : ℝ :=
  finiteEntropy (fun i => (partialTraceRight rho i i).re)

theorem tower_cut_density_properties (P : SiteProfile) (N : ℕ) :
    (towerCutDensity P N).PosSemidef ∧
    Matrix.trace (towerCutDensity P N)=1 ∧
    towerCutDensity P N*towerCutDensity P N=towerCutDensity P N := by
  exact ⟨pure_cut_positive _, pure_cut_trace_one _ (fun i => (towerW_pos P N i).le) (towerW_sum P N),
    pure_cut_idempotent _ (fun i => (towerW_pos P N i).le) (towerW_sum P N)⟩

theorem tower_cut_marginals (P : SiteProfile) (N : ℕ) :
    partialTraceRight (towerCutDensity P N)=Matrix.diagonal (fun i => (towerW P N i:ℂ)) ∧
    partialTraceLeft (towerCutDensity P N)=Matrix.diagonal (fun i => (towerW P N i:ℂ)) :=
  ⟨pure_cut_right_reduction _ (fun i => (towerW_pos P N i).le),
    pure_cut_left_reduction _ (fun i => (towerW_pos P N i).le)⟩

theorem tower_cut_expectation (P : SiteProfile) (N : ℕ)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    Matrix.trace (towerCutDensity P N*(a ⊗ₖ (1:Matrix (chainIdx N) (chainIdx N) ℂ)))=
      tState P N a :=
  pure_cut_left_expectation _ (fun i => (towerW_pos P N i).le) a

theorem tower_cut_prefix_coherence (P : SiteProfile) (N : ℕ)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    Matrix.trace (towerCutDensity P (N+1)*
      (towerStep a ⊗ₖ (1:Matrix (chainIdx (N+1)) (chainIdx (N+1)) ℂ)))=
    Matrix.trace (towerCutDensity P N*(a ⊗ₖ (1:Matrix (chainIdx N) (chainIdx N) ℂ))) := by
  rw [tower_cut_expectation,tower_cut_expectation,tState_towerStep]

theorem tower_cut_reduced_entropy (P : SiteProfile) (N : ℕ) :
    reducedDiagonalEntropy (towerCutDensity P N)=towerEntropy P N := by
  unfold reducedDiagonalEntropy
  rw [(tower_cut_marginals P N).1]
  simp only [Matrix.diagonal_apply_eq,Complex.ofReal_re]
  rfl

theorem tower_cut_entropy_sum (P : SiteProfile) (N : ℕ) :
    reducedDiagonalEntropy (towerCutDensity P N)=
      ∑ n∈Finset.range (N+1), Real.binEntropy (P.w n) := by
  rw [tower_cut_reduced_entropy,tower_entropy_sum]

theorem tower_cut_modular_entropy (P : SiteProfile) (N : ℕ) :
    Matrix.trace (towerCutDensity P N*
      (diagonalModularGenerator (towerW P N) ⊗ₖ (1:Matrix (chainIdx N) (chainIdx N) ℂ)))=
        (reducedDiagonalEntropy (towerCutDensity P N):ℂ) := by
  rw [tower_cut_expectation,tower_cut_reduced_entropy]
  exact (tower_entropy_modular_expectation P N).symm

theorem tower_cut_left_faithful (P : SiteProfile) (N : ℕ)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ)
    (hz : Matrix.trace (towerCutDensity P N*
      ((aᴴ*a) ⊗ₖ (1:Matrix (chainIdx N) (chainIdx N) ℂ)))=0) : a=0 := by
  rw [tower_cut_expectation] at hz
  exact tInner_self_definite P N hz

theorem chain_indices_distinct (N : ℕ) : ∃ i j : chainIdx N, i≠j := by
  induction N with
  | zero => exact ⟨(0:Fin 2), (1:Fin 2), by decide⟩
  | succ N ih =>
    obtain ⟨i,j,hij⟩ := ih
    exact ⟨(i,(0:Fin 2)),(j,(0:Fin 2)), fun h => hij (congrArg Prod.fst h)⟩

theorem tower_cut_full_not_faithful (P : SiteProfile) (N : ℕ) :
    ∃ a : Matrix (chainIdx N × chainIdx N) (chainIdx N × chainIdx N) ℂ,
      a≠0 ∧ Matrix.trace (towerCutDensity P N*(aᴴ*a))=0 := by
  obtain ⟨i,j,hij⟩ := chain_indices_distinct N
  obtain ⟨hne,hzero⟩ := pure_cut_annihilated_projection (towerW P N) i j hij
  refine ⟨Matrix.single (i,j) (i,j) 1,hne,?_⟩
  simpa only [towerCutDensity,Matrix.conjTranspose_single,star_one,Matrix.single_mul_single_same,one_mul] using hzero

theorem tower_cut_chosen_area (P : SiteProfile) (p : ℝ) (hp : ∀ n, P.w n=p)
    (areaUnit : ℝ) (ha : areaUnit≠0) (N : ℕ) :
    reducedDiagonalEntropy (towerCutDensity P N)=
      (Real.binEntropy p/areaUnit)*countArea areaUnit N := by
  rw [tower_cut_reduced_entropy]
  exact entropy_as_chosen_count_area P p hp areaUnit ha N

#print axioms tower_cut_density_properties
#print axioms tower_cut_marginals
#print axioms tower_cut_expectation
#print axioms tower_cut_prefix_coherence
#print axioms tower_cut_reduced_entropy
#print axioms tower_cut_entropy_sum
#print axioms tower_cut_modular_entropy
#print axioms tower_cut_left_faithful
#print axioms chain_indices_distinct
#print axioms tower_cut_full_not_faithful
#print axioms tower_cut_chosen_area
end
end ChatgptAudit
