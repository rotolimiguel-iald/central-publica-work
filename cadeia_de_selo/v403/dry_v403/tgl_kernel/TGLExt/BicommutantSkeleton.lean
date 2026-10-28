import TGLExt.InvariantProjection

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

/-!
# O ESQUELETO DO BICOMUTANTE E A NORMALIDADE CAUSAL DA RÉGUA
  [TGLExt — v84, o incremento 6 do programa SemifiniteAnalysis]

Duas perguntas do operador, respondidas em kernel:

(1) "A normalidade do τ é causal — a régua não pode ser burlada por
    limites." VIROU TEOREMA: a régua da dimensão é NORMAL sobre cadeias
    crescentes — τ(⨆ Sᵢ) = ⨆ τ(Sᵢ). Nenhum peso nasce no limite: se os
    pesos são uniformemente finitos, a cadeia ESTABILIZA (o crescimento
    do peso acompanha o crescimento do objeto — causalidade da regra).

(2) O caminho ao bicomutante: o esqueleto ALGÉBRICO de von Neumann.

O QUE ESTA PEDRA PROVA [KERNEL]:

* ★★★ `dimension_trace_normal_on_chains` — A NORMALIDADE CAUSAL DA
  RÉGUA: para cadeias crescentes de subespaços, τ(⨆ᵢ Sᵢ) = ⨆ᵢ τ(Sᵢ)
  (pesos limitados ⟹ a cadeia estabiliza num Sᵢ₀ de dimensão máxima;
  pesos ilimitados ⟹ ambos os lados são ⊤);
* ★ `commutant_antitone` — A ⊆ B ⟹ B′ ⊆ A′ (mais operadores a
  respeitar, menos quem comuta);
* ★★ `algebra_in_double_commutant` — A ⊆ A″ (todo conjunto habita o
  próprio bicomutante — a metade algébrica GRATUITA de von Neumann);
* ★★ `triple_commutant_collapse` — A‴ = A′ (o comutante já é ponto fixo:
  a torre para no segundo andar);
* ★ `commutant_unital_multiplicative` — 1 ∈ A′ e A′ é fechado sob
  produto (o comutante é um monoide — o germe da subálgebra);
* ★★ `corner_projection_in_commutant_set` — P_{ker T} ∈ {T}′ como
  pertencimento de CENTRALIZADOR (a linguagem de álgebra, não só a
  equação pontual do v83);
* ★★ `corner_commutes_with_bicommutant` — P_{ker T} comuta com TODO
  elemento de {T}″: o canto respeita a álgebra INTEIRA gerada
  (algebricamente) por T;
* ★★★ `breuer_corner_full_algebraic_frame` — A MOLDURA ALGÉBRICA
  COMPLETA DO CANTO (v80×v82×v83×v84): T auto-adjunto, ker ≠ ⊥ sob gap
  finito, H ∞-dim ⟹ P ∈ {T}′ ∧ (P comuta com {T}″) ∧ 0 < τ(ker) < ∞ ∧
  τ(ker⊥) = ⊤.

HONESTIDADE: o bicomutante aqui é ALGÉBRICO (centralizadores); o teorema
do bicomutante CONTÍNUO de von Neumann (A″ = fecho fraco; P ∈ {T}″ via
cálculo espectral) é exatamente o resíduo nomeado — [KNOWN] na
literatura, programa no kernel. A normalidade provada é sobre cadeias
(σ-completude sequencial); redes gerais seguem o programa. Nada é III₁;
nenhuma flag do fecho se move. β jamais literal. Sem sorry, sem axiom.
-/

namespace TGLExt

open scoped ENNReal

noncomputable section

/- ═══════════ 1. A normalidade causal da régua ═══════════ -/

variable {K : Type} [Field K] {V : Type} [AddCommGroup V] [Module K V]

/-- [KERNEL] ★★★ A NORMALIDADE CAUSAL DA RÉGUA: sobre cadeias
    crescentes, o peso do limite é o limite dos pesos — a regra não pode
    ser burlada por limites (pesos limitados ⟹ a cadeia estabiliza;
    ilimitados ⟹ ambos os lados são ⊤). -/
theorem dimension_trace_normal_on_chains (S : ℕ → Submodule K V)
    (hmono : Monotone S) :
    (semifiniteDimTrace K V).tau (⨆ i, S i)
      = ⨆ i, (semifiniteDimTrace K V).tau (S i) := by
  apply le_antisymm
  · by_cases hsup : (⨆ i, (semifiniteDimTrace K V).tau (S i)) = ⊤
    · rw [hsup]
      exact le_top
    · obtain ⟨N, hN⟩ := ENNReal.exists_nat_gt hsup
      have hfd : ∀ i, FiniteDimensional K (S i) := by
        intro i
        have h1 : (semifiniteDimTrace K V).tau (S i) < ⊤ :=
          lt_of_le_of_lt
            (le_iSup (fun j => (semifiniteDimTrace K V).tau (S j)) i)
            (lt_of_lt_of_le hN le_top)
        exact (dimOrTop_lt_top_iff K).mp h1
      have hbound : ∀ i, Module.finrank K (S i) ≤ N := by
        intro i
        have h1 : (semifiniteDimTrace K V).tau (S i) < (N : ℝ≥0∞) :=
          lt_of_le_of_lt
            (le_iSup (fun j => (semifiniteDimTrace K V).tau (S j)) i) hN
        have h2 : ((Module.finrank K (S i) : ℕ) : ℝ≥0∞) < (N : ℝ≥0∞) := by
          have h3 : dimOrTop K (S i) < (N : ℝ≥0∞) := h1
          rwa [dimOrTop_of_finite K (hfd i)] at h3
        exact_mod_cast le_of_lt h2
      set R : Set ℕ := Set.range (fun i => Module.finrank K (S i)) with hRdef
      have hne : R.Nonempty := ⟨Module.finrank K (S 0), ⟨0, rfl⟩⟩
      have hbdd : BddAbove R := ⟨N, by rintro _ ⟨i, rfl⟩; exact hbound i⟩
      have hmem := Nat.sSup_mem hne hbdd
      obtain ⟨i0, hi0⟩ := hmem
      have hi0' : Module.finrank K (S i0) = sSup R := hi0
      have hstab : (⨆ i, S i) = S i0 := by
        apply le_antisymm
        · apply iSup_le
          intro j
          have h1 : S j ≤ S (max j i0) := hmono (le_max_left _ _)
          have h2 : S i0 = S (max j i0) := by
            haveI := hfd (max j i0)
            refine Submodule.eq_of_le_of_finrank_le (hmono (le_max_right _ _)) ?_
            rw [hi0']
            exact le_csSup hbdd ⟨max j i0, rfl⟩
          rw [← h2] at h1
          exact h1
        · exact le_iSup S i0
      rw [hstab]
      exact le_iSup (fun i => (semifiniteDimTrace K V).tau (S i)) i0
  · exact iSup_le fun i => (semifiniteDimTrace K V).mono (le_iSup S i)

/- ═══════════ 2. O esqueleto algébrico do bicomutante ═══════════ -/

variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

/-- [KERNEL] ★ o comutante é antítono: mais operadores a respeitar,
    menos quem comuta. -/
theorem operator_commutant_antitone (A B : Set (H →L[ℂ] H)) (h : A ⊆ B) :
    B.centralizer ⊆ A.centralizer :=
  Set.centralizer_subset h

/-- [KERNEL] ★★ todo conjunto habita o próprio bicomutante: A ⊆ A″ —
    a metade algébrica gratuita do teorema de von Neumann. -/
theorem operator_algebra_in_double_commutant (A : Set (H →L[ℂ] H)) :
    A ⊆ A.centralizer.centralizer :=
  Set.subset_centralizer_centralizer

/-- [KERNEL] ★★ a torre para no segundo andar: A‴ = A′ (o comutante já
    é ponto fixo da operação ′′). -/
theorem operator_triple_commutant_collapse (A : Set (H →L[ℂ] H)) :
    A.centralizer.centralizer.centralizer = A.centralizer :=
  Set.centralizer_centralizer_centralizer A

/-- [KERNEL] ★ o comutante é um monoide: 1 ∈ A′ e A′ é fechado sob
    produto — o germe da subálgebra. -/
theorem operator_commutant_unital_multiplicative (A : Set (H →L[ℂ] H)) :
    (1 : H →L[ℂ] H) ∈ A.centralizer ∧
      ∀ a b : H →L[ℂ] H, a ∈ A.centralizer → b ∈ A.centralizer →
        a * b ∈ A.centralizer := by
  constructor
  · rw [Set.mem_centralizer_iff]
    intro s _
    rw [mul_one, one_mul]
  · intro a b ha hb
    exact Set.mul_mem_centralizer ha hb

/-- [KERNEL] ★★ o canto pertence ao comutante COMO CONJUNTO: a equação
    pontual do v83 vira pertencimento de centralizador em B(H). -/
theorem corner_projection_in_commutant_set (T : H →L[ℂ] H)
    (hsa : ContinuousLinearMap.adjoint T = T) :
    (T.ker).starProjection ∈ ({T} : Set (H →L[ℂ] H)).centralizer := by
  rw [Set.mem_centralizer_iff]
  intro s hs
  rw [Set.mem_singleton_iff] at hs
  rw [hs]
  ext x
  show T ((T.ker).starProjection x) = (T.ker).starProjection (T x)
  exact (selfadjoint_ker_projection_in_commutant T hsa x).symm

/-- [KERNEL] ★★ o canto respeita a álgebra INTEIRA: P_{ker T} comuta com
    todo elemento do bicomutante algébrico {T}″. -/
theorem corner_commutes_with_bicommutant (T : H →L[ℂ] H)
    (hsa : ContinuousLinearMap.adjoint T = T) :
    ∀ b ∈ ({T} : Set (H →L[ℂ] H)).centralizer.centralizer,
      (T.ker).starProjection * b = b * (T.ker).starProjection := by
  intro b hb
  rw [Set.mem_centralizer_iff] at hb
  exact hb _ (corner_projection_in_commutant_set T hsa)

/-- [KERNEL] ★★★ A MOLDURA ALGÉBRICA COMPLETA DO CANTO
    (v80 × v82 × v83 × v84): T auto-adjunto, kernel não-trivial sob gap
    finito, H ∞-dim ⟹ P ∈ {T}′ ∧ P comuta com {T}″ ∧ 0 < τ(ker) < ∞ ∧
    τ(ker⊥) = ⊤. O que separa isto do canto de Breuer GENUÍNO tem nome:
    P ∈ {T}″ (bicomutante CONTÍNUO / cálculo espectral) — [KNOWN],
    programa. -/
theorem breuer_corner_full_algebraic_frame (hH : ¬FiniteDimensional ℂ H)
    (T : H →L[ℂ] H) (hsa : ContinuousLinearMap.adjoint T = T)
    (gp : Submodule ℂ H) (hker : T.ker ≠ ⊥)
    (hle : T.ker ≤ gp) (hgp : FiniteDimensional ℂ gp) :
    ((T.ker).starProjection ∈ ({T} : Set (H →L[ℂ] H)).centralizer ∧
      ∀ b ∈ ({T} : Set (H →L[ℂ] H)).centralizer.centralizer,
        (T.ker).starProjection * b = b * (T.ker).starProjection) ∧
      ((0 < (semifiniteDimTrace ℂ H).tau T.ker ∧
          (semifiniteDimTrace ℂ H).tau T.ker < ⊤) ∧
        (semifiniteDimTrace ℂ H).tau (T.ker)ᗮ = ⊤) := by
  have hw := breuer_corner_projection_in_commutant hH T hsa gp hker hle hgp
  exact ⟨⟨corner_projection_in_commutant_set T hsa,
          corner_commutes_with_bicommutant T hsa⟩, hw.2⟩

end

end TGLExt
