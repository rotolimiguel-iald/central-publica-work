import TGLExt.SemifiniteWeight
import TGLExt.NoFullWitness

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

/-!
# A TESTEMUNHA SATURADA: saturação, não completude — o corte pelo vazamento
  [TGLExt — v131, a sentença de fechamento do operador]

O operador (20/07/2026): "a testemunha não é completa, é saturada no gráviton;
e porque satura, o estado Tetelestai é alcançado, cortando aquilo que
supersaturaria, pelo vazamento."

Esta pedra UNIFICA os dois módulos já provados, sem nada de novo a postular:

* SemifiniteWeight (v120): `Tr(P_Nome) = 1 = ω(I)` — a SATURAÇÃO no átomo único;
* NoFullWitness   (v61): `β > 0` proíbe a testemunha estática plena — o
  VAZAMENTO contínuo que impede a completude/supersaturação.

e acrescenta o elo que a frase do operador nomeia:

* `witness_saturates` — o Nome satura o peso em `1 = ω(I)` (a saturação);
* `house_is_infinite` — `Tr(1) = ∞`: a casa nunca fecha num total finito
  (nunca supersatura);
* ★ `excess_is_infinite` — o EXCESSO (o complemento do Nome) pesa `∞`: é o que
  supersaturaria, CORTADO, deixando o Um em peso 1 — "cortando aquilo que
  supersaturaria";
* `witness_is_single_atom` — a testemunha é UM átomo (o span de uma única
  inscrição), não uma população: "um pontífice engrenante, não uma população";
* ★★★ `saturated_witness_not_complete` — A SENTENÇA: o Nome satura
  (`1 = ω(I)`), o excesso é `∞` (cortado), a casa é `∞` (não fecha) E a
  testemunha plena é proibida pelo vazamento (`β > 0`) ⟹ SATURADA, nunca
  completa, nunca supersaturada; única no átomo.

`full_witness = False` permanece INTOCADO (correto por teorema, v61). O que
esta pedra acrescenta é a face POSITIVA da mesma verdade: `saturated_witness`.
A segunda metade (a identificação gráviton-`=` como resposta geométrica global,
Einstein) NÃO é tocada aqui — segue como a hipótese aberta, julgada fail-closed
pelo gate. β JAMAIS literal. Sem sorry, sem axiom.
-/

namespace TGLExt

open scoped ENNReal

noncomputable section

/-! ## A — a saturação e a casa infinita (reexportadas dos módulos provados) -/

/-- [KERNEL] A SATURAÇÃO: o Nome satura o peso em `1 = ω(I)` (v120). -/
theorem witness_saturates : opWeight firstAtom.starProjection = 1 :=
  opWeight_atom_one

/-- [KERNEL] A CASA NUNCA FECHA: `Tr(1) = ∞` — sem total finito, nunca
    supersatura num fecho completo (v120). -/
theorem house_is_infinite : opWeight (1 : ellTwo →L[ℂ] ellTwo) = ⊤ :=
  opWeight_one_top

/-! ## B — o EXCESSO é infinito: o que supersaturaria, cortado -/

/-- [KERNEL] ★ O EXCESSO É INFINITO: o complemento do Nome pesa `∞`. É a parte
    "sem retorno" que supersaturaria — cortada pela poda, deixando o Um em peso
    1. O termo diagonal é `0` no Nome (n = 0) e `1` fora dele (n ≥ 1); há
    infinitos deles. -/
theorem excess_is_infinite :
    opWeight (1 - firstAtom.starProjection) = ⊤ := by
  unfold opWeight
  have hterm : ∀ n : ℕ,
      ENNReal.ofReal ((((1 - firstAtom.starProjection) (inscriptions n) : ℕ → ℂ) n).re)
        = if n = 0 then 0 else 1 := by
    intro n
    rcases Nat.eq_zero_or_pos n with rfl | hn
    · -- n = 0: (1 - P) e₀ = e₀ - e₀ = 0
      have hP0 : firstAtom.starProjection (inscriptions 0) = firstInscription := by
        show firstAtom.starProjection firstInscription = firstInscription
        exact Submodule.starProjection_eq_self_iff.mpr
          (Submodule.mem_span_singleton_self _)
      have h1 : (1 - firstAtom.starProjection) (inscriptions 0) = 0 := by
        rw [sub_apply, one_apply_eq_self, hP0]
        show firstInscription - firstInscription = 0
        rw [sub_self]
      rw [h1, if_pos rfl]
      have h0 : ((0 : ellTwo) : ℕ → ℂ) 0 = 0 := by
        rw [lp.coeFn_zero]; rfl
      rw [h0]; norm_num
    · -- n ≥ 1: (1 - P) eₙ = eₙ - 0 = eₙ, coordenada n = 1
      have hPn : firstAtom.starProjection (inscriptions n) = 0 := by
        unfold firstAtom
        rw [Submodule.starProjection_singleton ℂ]
        have hinner : inner ℂ firstInscription (inscriptions n) = 0 := by
          unfold firstInscription
          rw [coord_eq_inner, inscriptions_apply,
            if_neg (by omega : ¬ (0 : ℕ) = n)]
        rw [hinner, zero_div, zero_smul]
      have h1 : (1 - firstAtom.starProjection) (inscriptions n) = inscriptions n := by
        rw [sub_apply, one_apply_eq_self, hPn, sub_zero]
      rw [h1, if_neg (by omega : ¬ n = 0)]
      rw [inscriptions_apply, if_pos rfl]
      norm_num
  rw [tsum_congr hterm]
  refine top_le_iff.mp ?_
  calc (⊤ : ℝ≥0∞)
      = ∑' _ : ℕ, (1 : ℝ≥0∞) :=
        (ENNReal.tsum_const_eq_top_of_ne_zero one_ne_zero).symm
    _ ≤ ∑' n : ℕ, (if n = 0 then (0 : ℝ≥0∞) else 1) := by
        have h := ENNReal.tsum_comp_le_tsum_of_injective Nat.succ_injective
          (fun n => if n = 0 then (0 : ℝ≥0∞) else 1)
        simpa using h

/-! ## C — uma única testemunha, não uma população -/

/-- [KERNEL] A TESTEMUNHA É UM ÁTOMO: o subespaço do Nome é o span de UMA
    inscrição — um pontífice, não uma população. -/
theorem witness_is_single_atom : firstAtom = ℂ ∙ firstInscription := rfl

/-! ## D — A SENTENÇA: saturada, não completa; o excesso cortado -/

/-- [KERNEL] ★★★ A TESTEMUNHA É SATURADA, NÃO COMPLETA: o Nome satura o peso em
    `1 = ω(I)`; a casa pesa `∞` (nunca fecha) e o excesso pesa `∞` (cortado,
    "aquilo que supersaturaria"); E a testemunha estática plena é PROIBIDA pelo
    vazamento (`β > 0`, `gap > 0`). Saturação, não completude — o Tetelestai
    alcançado pelo corte. `full_witness = False` permanece correto; esta é a sua
    face positiva. -/
theorem saturated_witness_not_complete :
    opWeight firstAtom.starProjection = 1
      ∧ opWeight (1 : ellTwo →L[ℂ] ellTwo) = ⊤
      ∧ opWeight (1 - firstAtom.starProjection) = ⊤
      ∧ (∀ (β g : ℝ), 0 < β → 0 < g →
          ¬ FullStaticWitness (fun t (x : ℝ) => Real.exp (-(t * β * g)) * x)) :=
  ⟨witness_saturates, house_is_infinite, excess_is_infinite,
   fun _ _ hβ hg => beta_forbids_full_static_witness hβ hg⟩

end

end TGLExt
