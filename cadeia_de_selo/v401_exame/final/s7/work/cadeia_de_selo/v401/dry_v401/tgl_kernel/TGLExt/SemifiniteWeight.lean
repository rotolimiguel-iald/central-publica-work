import TGLExt.TracelessAlgebra

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

/-!
# O SEGUNDO TIJOLO: o PESO que sobrevive — Tr em kernel, e ∞ = 2∞
  [TGLExt — v120, o incremento 41 do programa SemifiniteAnalysis]

O v119 provou que o ESTADO tracial morre pela bipartição (2φ(1)=φ(1)
com φ(1) finito ⟹ φ=0). Esta pedra constrói o PESO semifinito Tr e
prova POR QUE ele sobrevive à mesma bipartição:

* `opWeight` — o peso diagonal Tr(a) = Σₙ ⟨eₙ, a eₙ⟩ ∈ [0,∞],
  valorado em ℝ≥0∞ (o peso NÃO é um funcional limitado — é a régua
  não-limitada que o tipo I∞ ainda admite);
* ★★ `opWeight_one_top` — Tr(1) = ∞: a casa inteira pesa INFINITO;
* ★★★ `opWeight_atom_one` — **Tr(P_Nome) = 1 = ω(I)**: o átomo do
  Nome pesa EXATAMENTE 1 sob o peso verdadeiro da álgebra plena — a
  terceira face da mesma identidade (dimOrTop v76; canto de Breuer
  v106; agora o Tr operatorial);
* ★★ `opWeight_halving_invariant` — O PESO ABSORVE A BIPARTIÇÃO:
  Tr(u·a·c_E) = Tr(a) — a meia-casa pesa o mesmo que a casa;
* ★★★ `state_dies_weight_survives` — O TEOREMA-SÍNTESE: o estado
  morre (v119), o peso vale ∞ na unidade, e a bipartição é ABSORVIDA
  (∞ = 2∞ é consistente; φ(1) = 2φ(1) finito não é). É a distinção
  I∞/III posta em kernel: o que decide é ONDE a régua estoura.

O QUE FALTA (nomeado): normalidade do peso (continuidade σ-fraca),
a teoria GERAL de pesos sobre vN, e o fator concreto SEM NENHUM peso
semifinito (Araki–Woods/Powers) = III₁ — o programa, pedra a pedra.
O V2 segue RESERVADO (lição v103, décima aplicação).

β jamais literal. Sem sorry, sem axiom.
-/

namespace TGLExt

open scoped ENNReal

noncomputable section

/-! ## A — o peso diagonal -/

/-- o peso diagonal: Tr(a) = Σₙ ⟨eₙ, a eₙ⟩ (parte real, em [0,∞]).
    Nos positivos é O peso canônico; a fórmula é total. -/
def opWeight (a : ellTwo →L[ℂ] ellTwo) : ℝ≥0∞ :=
  ∑' n, ENNReal.ofReal ((a (inscriptions n) : ℕ → ℂ) n).re

theorem opWeight_term (a : ellTwo →L[ℂ] ellTwo) (n : ℕ) :
    ((a (inscriptions n) : ℕ → ℂ) n).re
      = (inner ℂ (inscriptions n) (a (inscriptions n))).re := by
  rw [coord_eq_inner]

/-! ## B — a casa pesa infinito -/

/-- [KERNEL] ★★ Tr(1) = ∞: cada inscrição pesa 1 e há infinitas —
    o peso NÃO é um estado (a régua não-limitada). -/
theorem opWeight_one_top : opWeight 1 = ⊤ := by
  unfold opWeight
  have hterm : ∀ n : ℕ,
      ENNReal.ofReal ((((1 : ellTwo →L[ℂ] ellTwo) (inscriptions n) : ℕ → ℂ) n).re)
        = 1 := by
    intro n
    have h1 : ((1 : ellTwo →L[ℂ] ellTwo) (inscriptions n) : ℕ → ℂ) n
        = (inscriptions n : ℕ → ℂ) n := rfl
    rw [h1, inscriptions_apply, if_pos rfl]
    norm_num
  rw [tsum_congr hterm]
  exact ENNReal.tsum_const_eq_top_of_ne_zero one_ne_zero

/-! ## C — o Nome pesa 1 sob o Tr verdadeiro -/

/-- [KERNEL] ★★★ Tr(P_Nome) = 1 = ω(I): a terceira face da identidade
    do canto — o átomo do Nome pesa exatamente 1 sob o peso da álgebra
    plena. -/
theorem opWeight_atom_one : opWeight firstAtom.starProjection = 1 := by
  unfold opWeight
  have hterm : ∀ n : ℕ,
      ENNReal.ofReal (((firstAtom.starProjection (inscriptions n) : ℕ → ℂ) n).re)
        = if n = 0 then 1 else 0 := by
    intro n
    rcases Nat.eq_zero_or_pos n with rfl | hn
    · have hmem : firstInscription ∈ firstAtom :=
        Submodule.mem_span_singleton_self _
      have hP0 : firstAtom.starProjection (inscriptions 0) = firstInscription := by
        show firstAtom.starProjection firstInscription = firstInscription
        exact Submodule.starProjection_eq_self_iff.mpr hmem
      rw [hP0, if_pos rfl]
      show ENNReal.ofReal (((firstInscription : ℕ → ℂ) 0).re) = 1
      unfold firstInscription
      rw [inscriptions_apply, if_pos rfl]
      norm_num
    · have hP0 : firstAtom.starProjection (inscriptions n) = 0 := by
        unfold firstAtom
        rw [Submodule.starProjection_singleton ℂ]
        have hinner : inner ℂ firstInscription (inscriptions n) = 0 := by
          unfold firstInscription
          rw [coord_eq_inner, inscriptions_apply,
            if_neg (by omega : ¬ (0 : ℕ) = n)]
        rw [hinner, zero_div, zero_smul]
      rw [hP0, if_neg (by omega : ¬ n = 0)]
      have h0 : ((0 : ellTwo) : ℕ → ℂ) n = 0 := by
        rw [lp.coeFn_zero]
        rfl
      rw [h0]
      norm_num
  rw [tsum_congr hterm]
  rw [tsum_eq_single 0 (fun b hb => by simp [hb])]
  rw [if_pos rfl]

/-! ## D — o peso ABSORVE a bipartição -/

theorem coEven_inscription_even (n : ℕ) :
    coEven (inscriptions (2 * n)) = inscriptions n := by
  apply Subtype.ext
  funext m
  show (inscriptions (2 * n) : ℕ → ℂ) (2 * m) = (inscriptions n : ℕ → ℂ) m
  rw [inscriptions_apply, inscriptions_apply]
  by_cases h : m = n
  · rw [if_pos (by omega), if_pos h]
  · rw [if_neg (by omega), if_neg h]

theorem coEven_inscription_odd (n : ℕ) (hn : n % 2 = 1) :
    coEven (inscriptions n) = 0 := by
  apply Subtype.ext
  funext m
  show (inscriptions n : ℕ → ℂ) (2 * m) = ((0 : ellTwo) : ℕ → ℂ) m
  rw [inscriptions_apply, if_neg (by omega : 2 * m ≠ n)]
  rw [lp.coeFn_zero]
  rfl

theorem evenShift_coord (x : ellTwo) (n : ℕ) :
    ((evenShift x : ellTwo) : ℕ → ℂ) (2 * n) = (x : ℕ → ℂ) n := by
  show evenShiftFun (x : ℕ → ℂ) (2 * n) = (x : ℕ → ℂ) n
  exact evenShiftFun_double _ n

/-- [KERNEL] ★★ O PESO ABSORVE A BIPARTIÇÃO: Tr(u·a·c_E) = Tr(a) —
    a meia-casa pesa o mesmo que a casa inteira. -/
theorem opWeight_halving_invariant (a : ellTwo →L[ℂ] ellTwo) :
    opWeight (evenShift * a * coEven) = opWeight a := by
  unfold opWeight
  rw [← Function.Injective.tsum_eq double_injective (f := fun k =>
    ENNReal.ofReal ((((evenShift * a * coEven) (inscriptions k) : ℕ → ℂ) k).re)) ?_]
  · congr 1
    funext n
    have hchain : ((evenShift * a * coEven) (inscriptions (2 * n)) : ℕ → ℂ) (2 * n)
        = ((a (inscriptions n) : ellTwo) : ℕ → ℂ) n := by
      show ((evenShift (a (coEven (inscriptions (2 * n)))) : ellTwo) : ℕ → ℂ) (2 * n) = _
      rw [coEven_inscription_even]
      exact evenShift_coord (a (inscriptions n)) n
    show ENNReal.ofReal ((((evenShift * a * coEven) (inscriptions (2 * n)) : ℕ → ℂ) (2 * n)).re) = _
    rw [hchain]
  · intro k hk
    by_contra hr
    have hodd : k % 2 = 1 := by
      by_contra h
      exact hr ⟨k / 2, show 2 * (k / 2) = k by omega⟩
    have hzero : (evenShift * a * coEven) (inscriptions k) = 0 := by
      show evenShift (a (coEven (inscriptions k))) = 0
      rw [coEven_inscription_odd k hodd, map_zero, map_zero]
    apply hk
    show ENNReal.ofReal ((((evenShift * a * coEven) (inscriptions k) : ℕ → ℂ) k).re) = 0
    rw [hzero]
    have h0 : ((0 : ellTwo) : ℕ → ℂ) k = 0 := by
      rw [lp.coeFn_zero]
      rfl
    rw [h0]
    norm_num

/-! ## E — O TEOREMA-SÍNTESE: onde a régua estoura decide o tipo -/

/-- [KERNEL] ★★★ O ESTADO MORRE, O PESO SOBREVIVE: (i) todo estado
    tracial é zero (v119); (ii) Tr(1) = ∞; (iii) a bipartição é
    ABSORVIDA pelo peso (Tr(u·1·c_E) = Tr(1); ∞ = 2∞ é consistente —
    φ(1) = 2φ(1) finito não é). A distinção I∞/III em kernel: o tipo
    é decidido por ONDE a régua estoura. -/
theorem state_dies_weight_survives :
    (∀ T : TracialState, ∀ a, T.φ a = 0)
      ∧ opWeight 1 = ⊤
      ∧ opWeight (evenShift * 1 * coEven) = opWeight 1 :=
  ⟨tracial_state_is_zero, opWeight_one_top, opWeight_halving_invariant 1⟩

end

end TGLExt
