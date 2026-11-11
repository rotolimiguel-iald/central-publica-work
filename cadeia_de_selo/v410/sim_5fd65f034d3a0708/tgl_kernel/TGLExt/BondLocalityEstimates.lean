-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — LOTE 058..062 (09/09/2026), transposta em 10/09/2026 (ENTREGA_062 = elo do lote)
-- Os 77 modulos da sessao de 09/09 da bancada (cadeia de copias integradas 63 -> 72 -> 77 sobre a base v337 lida),
--   1065 teoremas declarados pela bancada. Cinco entregas espontaneas:
--   058: ATLAS GRAVITACIONAL SELECIONADO — continuidade + amostras densas + cortes racionais determinam o registro em U;
--     a leitura geometricLogReading caracteriza a sequencia booleana; a selecao por classe instancia IALDState e os
--     teoremas do Nome; o decodificador devolve classe, g, T e os pesos; Einstein do registro decodificado decorre das
--     leis de area e conservacao do registro original (jets, Levi-Civita, Ricci, Einstein preservados).
--   059: caracter completo reconstroi g/T/Einstein condicionado a area e conservacao; COLAGEM da Lambda unico nas
--     cartas compativeis; naturalidade infinitesimal de Ricci/escalar/Einstein em carta curva; potencial XX somavel
--     auto-adjunto com cauda em norma; exemplo de acoplamento atestado.
--   060: COCICLO UNITARIO INFINITO do potencial XX somavel na acao modular canonica; controle uniforme dos cortes;
--     gerador iV e ODE; grupo beta_t = Ad_u(t) o alpha_t que preserva o fator; transformacao finita de
--     Levi-Civita/Ricci/escalar/Einstein e lei de transformacao de Einstein nas sobreposicoes metricas abertas.
--   061: interacao local somavel com termos NAO comutativos (testemunha explicita); unicidade potencial <-> cociclo;
--     fase central Z^{-it} (gerador i(V - logZ I)); colagem suave selecionada -> Lambda global unico; estado perturbado
--     de Araki [DERIVED + KNOWN, analitico — NAO Lean].
--   062: seletor canonico e Born; reconstrucao do registro pelo seletor; entrelacamento angular; caracter da fase
--     relativa (duas probabilidades de interferencia recuperam a fase); estimativas de localidade de vinculo.
--   Estatuto: [REAL] o compilado; [DERIVED + KNOWN] Araki; [INPUT] R (o registro) e a origem fisica; [OPEN]
--   correspondencia fisica seletor-registro, materia/conservacao/area para os mesmos dados, atlas fisico compativel,
--   alem da classe globalmente limitada, anomalias e UV. Nenhum nome ligado a H3, area fisica ou gate.
-- Auditoria da gerencia (sessao d554e796, 10/09/2026): lote montado da CADEIA de recibos (INTEGRATION_RESULT 77 -> 72
--   -> 63); 77/77 hashes lidos dos bytes contra os recibos; zero proibidos; guarda de colisao; recompilacao INDEPENDENTE
--   77/77 contra o kernel v337, axiomas no trio; a copia integrada da bancada NAO foi usada (so as fontes congeladas).
--   Transposicao: cabecalho + prefixo TGLExt. nos imports locais (+ regra 3).
-- NAO move gate; nao e fisica; NOT_FALSIFIED nunca e CONFIRMED; CONFIRMADA proibido.
-- ---------------------------------------------------------------------
import TGLExt.ChainLocality
import Mathlib.Analysis.Normed.Ring.Basic

set_option autoImplicit false
set_option maxHeartbeats 1000000
namespace ChatgptAudit.BondLocality
open TGLExt
noncomputable section

abbrev BondOperator (P : SiteProfile) := TowerHilbert P →L[ℂ] TowerHilbert P

structure BondInteractionData (P : SiteProfile) where
  term : ℕ → BondOperator P
  selfadjoint : ∀ j, IsSelfAdjoint (term j)
  support : ∀ j, term j ∈ chainLocalAlgebra P ({j, j + 1} : Set ℕ)
  bound : ℝ
  bound_nonnegative : 0 ≤ bound
  norm_bound : ∀ j, ‖term j‖ ≤ bound

def operatorBracket {P : SiteProfile} (A B : BondOperator P) : BondOperator P :=
  A * B - B * A

theorem operator_bracket_norm {P : SiteProfile} (A B : BondOperator P) :
    ‖operatorBracket A B‖ ≤ 2 * ‖A‖ * ‖B‖ := by
  calc
    ‖operatorBracket A B‖ ≤ ‖A * B‖ + ‖B * A‖ := norm_sub_le _ _
    _ ≤ ‖A‖ * ‖B‖ + ‖B‖ * ‖A‖ :=
      add_le_add (norm_mul_le _ _) (norm_mul_le _ _)
    _ = 2 * ‖A‖ * ‖B‖ := by ring

theorem operator_bracket_mem_union {P : SiteProfile} {X Y : Set ℕ}
    {A B : BondOperator P}
    (hA : A ∈ chainLocalAlgebra P X) (hB : B ∈ chainLocalAlgebra P Y) :
    operatorBracket A B ∈ chainLocalAlgebra P (X ∪ Y) := by
  have ha : A ∈ chainLocalAlgebra P (X ∪ Y) :=
    chain_isotony (P := P) Set.subset_union_left hA
  have hb : B ∈ chainLocalAlgebra P (X ∪ Y) :=
    chain_isotony (P := P) Set.subset_union_right hB
  exact (chainLocalAlgebra P (X ∪ Y)).sub_mem
    ((chainLocalAlgebra P (X ∪ Y)).mul_mem ha hb)
    ((chainLocalAlgebra P (X ∪ Y)).mul_mem hb ha)

theorem operator_bracket_eq_zero_of_disjoint {P : SiteProfile} {X Y : Set ℕ}
    {A B : BondOperator P} (hXY : Disjoint X Y)
    (hA : A ∈ chainLocalAlgebra P X) (hB : B ∈ chainLocalAlgebra P Y) :
    operatorBracket A B = 0 := by
  unfold operatorBracket
  rw [chain_locality hXY hA hB, sub_self]

theorem distant_bond_bracket_zero {P : SiteProfile} (D : BondInteractionData P)
    {A : BondOperator P} {R j : ℕ}
    (hA : A ∈ chainLocalAlgebra P (Set.Iic R)) (hj : R < j) :
    operatorBracket (D.term j) A = 0 := by
  apply operator_bracket_eq_zero_of_disjoint (hA := D.support j) (hB := hA)
  apply Set.disjoint_left.mpr
  intro n hn hnr
  simp only [Set.mem_insert_iff, Set.mem_singleton_iff] at hn
  rcases hn with rfl | rfl
  · exact (not_le_of_gt hj) hnr
  · have : R < j + 1 := by omega
    exact (not_le_of_gt this) hnr

theorem bond_bracket_mem_expanded_prefix {P : SiteProfile} (D : BondInteractionData P)
    {A : BondOperator P} {R : ℕ}
    (hA : A ∈ chainLocalAlgebra P (Set.Iic R)) (j : ℕ) :
    operatorBracket (D.term j) A ∈ chainLocalAlgebra P (Set.Iic (R + 1)) := by
  by_cases hj : j ≤ R
  · have hs : ({j, j + 1} : Set ℕ) ⊆ Set.Iic (R + 1) := by
      intro n hn
      simp only [Set.mem_insert_iff, Set.mem_singleton_iff] at hn
      rcases hn with rfl | rfl <;> simp only [Set.mem_Iic] <;> omega
    have ht := chain_isotony (P := P) hs (D.support j)
    have ha := chain_isotony (P := P) (show Set.Iic R ⊆ Set.Iic (R + 1) from
      fun n hn => by simp only [Set.mem_Iic] at *; omega) hA
    exact (chainLocalAlgebra P (Set.Iic (R + 1))).sub_mem
      ((chainLocalAlgebra P (Set.Iic (R + 1))).mul_mem ht ha)
      ((chainLocalAlgebra P (Set.Iic (R + 1))).mul_mem ha ht)
  · rw [distant_bond_bracket_zero D hA (by omega)]
    exact (chainLocalAlgebra P (Set.Iic (R + 1))).zero_mem

def cutoffBracket {P : SiteProfile} (D : BondInteractionData P)
    (N : ℕ) (A : BondOperator P) : BondOperator P :=
  ∑ j ∈ Finset.range N, operatorBracket (D.term j) A

def cutoffHamiltonian {P : SiteProfile} (D : BondInteractionData P)
    (N : ℕ) : BondOperator P :=
  ∑ j ∈ Finset.range N, D.term j

theorem cutoff_hamiltonian_selfadjoint {P : SiteProfile} (D : BondInteractionData P)
    (N : ℕ) : IsSelfAdjoint (cutoffHamiltonian D N) := by
  change star (∑ j ∈ Finset.range N, D.term j) = _
  simp only [star_sum, (D.selfadjoint _).star_eq]
  rfl

theorem cutoff_hamiltonian_mem_prefix {P : SiteProfile} (D : BondInteractionData P)
    (N : ℕ) : cutoffHamiltonian D N ∈ chainLocalAlgebra P (Set.Iic N) := by
  apply (chainLocalAlgebra P (Set.Iic N)).sum_mem
  intro j hj
  have h : j < N := Finset.mem_range.mp hj
  apply chain_isotony (P := P) (J := Set.Iic N) ?_ (D.support j)
  intro n hn
  simp only [Set.mem_insert_iff, Set.mem_singleton_iff] at hn
  rcases hn with rfl | rfl <;> simp only [Set.mem_Iic] <;> omega

theorem cutoff_hamiltonian_bracket {P : SiteProfile} (D : BondInteractionData P)
    (N : ℕ) (A : BondOperator P) :
    operatorBracket (cutoffHamiltonian D N) A = cutoffBracket D N A := by
  simp only [operatorBracket, cutoffHamiltonian, cutoffBracket, Finset.sum_mul,
    Finset.mul_sum, Finset.sum_sub_distrib]

theorem cutoff_bracket_mem_expanded_prefix {P : SiteProfile} (D : BondInteractionData P)
    {A : BondOperator P} {R : ℕ}
    (hA : A ∈ chainLocalAlgebra P (Set.Iic R)) (N : ℕ) :
    cutoffBracket D N A ∈ chainLocalAlgebra P (Set.Iic (R + 1)) := by
  exact (chainLocalAlgebra P (Set.Iic (R + 1))).sum_mem
    (fun j _ => bond_bracket_mem_expanded_prefix D hA j)

theorem cutoff_bracket_stabilizes {P : SiteProfile} (D : BondInteractionData P)
    {A : BondOperator P} {R N : ℕ}
    (hA : A ∈ chainLocalAlgebra P (Set.Iic R)) (hN : R + 1 ≤ N) :
    cutoffBracket D N A = cutoffBracket D (R + 1) A := by
  unfold cutoffBracket
  symm
  apply Finset.sum_subset (Finset.range_mono hN)
  intro j hj hjR
  have : R < j := by
    simp only [Finset.mem_range, not_lt] at hjR
    omega
  exact distant_bond_bracket_zero D hA this

theorem cutoff_bracket_norm {P : SiteProfile} (D : BondInteractionData P)
    (N : ℕ) (A : BondOperator P) :
    ‖cutoffBracket D N A‖ ≤ (N : ℝ) * (2 * D.bound * ‖A‖) := by
  calc
    ‖cutoffBracket D N A‖ ≤ ∑ j ∈ Finset.range N, ‖operatorBracket (D.term j) A‖ :=
      norm_sum_le _ _
    _ ≤ ∑ _j ∈ Finset.range N, 2 * D.bound * ‖A‖ := by
      apply Finset.sum_le_sum
      intro j _
      exact (operator_bracket_norm _ _).trans
        (mul_le_mul_of_nonneg_right
          (mul_le_mul_of_nonneg_left (D.norm_bound j) (by norm_num)) (norm_nonneg _))
    _ = (N : ℝ) * (2 * D.bound * ‖A‖) := by simp

theorem stabilized_bracket_norm {P : SiteProfile} (D : BondInteractionData P)
    {A : BondOperator P} {R N : ℕ}
    (hA : A ∈ chainLocalAlgebra P (Set.Iic R)) (hN : R + 1 ≤ N) :
    ‖cutoffBracket D N A‖ ≤ ((R + 1 : ℕ) : ℝ) * (2 * D.bound * ‖A‖) := by
  rw [cutoff_bracket_stabilizes D hA hN]
  exact cutoff_bracket_norm D _ A

theorem local_bracket_norm {P : SiteProfile} (D : BondInteractionData P)
    {A : BondOperator P} {R : ℕ}
    (hA : A ∈ chainLocalAlgebra P (Set.Iic R)) (N : ℕ) :
    ‖cutoffBracket D N A‖ ≤ ((R + 1 : ℕ) : ℝ) * (2 * D.bound * ‖A‖) := by
  by_cases hN : N ≤ R + 1
  · exact (cutoff_bracket_norm D N A).trans
      (mul_le_mul_of_nonneg_right (by exact_mod_cast hN)
        (mul_nonneg (mul_nonneg (by norm_num) D.bound_nonnegative) (norm_nonneg A)))
  · exact stabilized_bracket_norm D hA (by omega)

def iteratedCutoffBracket {P : SiteProfile} (D : BondInteractionData P)
    (N : ℕ) (A : BondOperator P) : ℕ → BondOperator P
  | 0 => A
  | k + 1 => cutoffBracket D N (iteratedCutoffBracket D N A k)

theorem iterated_bracket_mem_prefix {P : SiteProfile} (D : BondInteractionData P)
    {A : BondOperator P} {R : ℕ}
    (hA : A ∈ chainLocalAlgebra P (Set.Iic R)) (N k : ℕ) :
    iteratedCutoffBracket D N A k ∈ chainLocalAlgebra P (Set.Iic (R + k)) := by
  induction k with
  | zero => simpa [iteratedCutoffBracket] using hA
  | succ k ih =>
      simpa only [iteratedCutoffBracket, Nat.add_assoc] using
        cutoff_bracket_mem_expanded_prefix D ih N

theorem iterated_bracket_cutoff_independent {P : SiteProfile} (D : BondInteractionData P)
    {A : BondOperator P} {R : ℕ}
    (hA : A ∈ chainLocalAlgebra P (Set.Iic R)) (k N M : ℕ)
    (hN : R + k ≤ N) (hM : R + k ≤ M) :
    iteratedCutoffBracket D N A k = iteratedCutoffBracket D M A k := by
  induction k with
  | zero => rfl
  | succ k ih =>
      have hi := ih (by omega) (by omega)
      simp only [iteratedCutoffBracket]
      rw [hi]
      have hs := iterated_bracket_mem_prefix D hA M k
      exact (cutoff_bracket_stabilizes D hs (N := N) (by omega)).trans
        (cutoff_bracket_stabilizes D hs (N := M) (by omega)).symm

def commutatorGrowth (J : ℝ) (R k : ℕ) : ℝ :=
  (2 * J) ^ k * ∏ r ∈ Finset.range k, ((R + r + 1 : ℕ) : ℝ)

theorem commutator_growth_zero (J : ℝ) (R : ℕ) :
    commutatorGrowth J R 0 = 1 := by
  simp [commutatorGrowth]

theorem commutator_growth_succ (J : ℝ) (R k : ℕ) :
    commutatorGrowth J R (k + 1) =
      (2 * J * ((R + k + 1 : ℕ) : ℝ)) * commutatorGrowth J R k := by
  simp only [commutatorGrowth, pow_succ, Finset.prod_range_succ]
  ring

theorem iterated_bracket_uniform_bound {P : SiteProfile} (D : BondInteractionData P)
    {A : BondOperator P} {R : ℕ}
    (hA : A ∈ chainLocalAlgebra P (Set.Iic R)) (N k : ℕ) :
    ‖iteratedCutoffBracket D N A k‖ ≤ commutatorGrowth D.bound R k * ‖A‖ := by
  induction k with
  | zero => simp [iteratedCutoffBracket, commutator_growth_zero]
  | succ k ih =>
      have hs := iterated_bracket_mem_prefix D hA N k
      have hn : 0 ≤ 2 * D.bound * ((R + k + 1 : ℕ) : ℝ) :=
        mul_nonneg (mul_nonneg (by norm_num) D.bound_nonnegative) (Nat.cast_nonneg _)
      calc
        ‖iteratedCutoffBracket D N A (k + 1)‖
          ≤ ((R + k + 1 : ℕ) : ℝ) *
              (2 * D.bound * ‖iteratedCutoffBracket D N A k‖) :=
            local_bracket_norm D hs N
        _ = (2 * D.bound * ((R + k + 1 : ℕ) : ℝ)) *
              ‖iteratedCutoffBracket D N A k‖ := by ring
        _ ≤ (2 * D.bound * ((R + k + 1 : ℕ) : ℝ)) *
              (commutatorGrowth D.bound R k * ‖A‖) :=
            mul_le_mul_of_nonneg_left ih hn
        _ = commutatorGrowth D.bound R (k + 1) * ‖A‖ := by
          rw [commutator_growth_succ]
          ring

#print axioms BondOperator
#print axioms BondInteractionData
#print axioms operatorBracket
#print axioms operator_bracket_norm
#print axioms operator_bracket_mem_union
#print axioms operator_bracket_eq_zero_of_disjoint
#print axioms distant_bond_bracket_zero
#print axioms bond_bracket_mem_expanded_prefix
#print axioms cutoffBracket
#print axioms cutoffHamiltonian
#print axioms cutoff_hamiltonian_selfadjoint
#print axioms cutoff_hamiltonian_mem_prefix
#print axioms cutoff_hamiltonian_bracket
#print axioms cutoff_bracket_mem_expanded_prefix
#print axioms cutoff_bracket_stabilizes
#print axioms cutoff_bracket_norm
#print axioms stabilized_bracket_norm
#print axioms local_bracket_norm
#print axioms iteratedCutoffBracket
#print axioms iterated_bracket_mem_prefix
#print axioms iterated_bracket_cutoff_independent
#print axioms commutatorGrowth
#print axioms commutator_growth_zero
#print axioms commutator_growth_succ
#print axioms iterated_bracket_uniform_bound
end
end ChatgptAudit.BondLocality
