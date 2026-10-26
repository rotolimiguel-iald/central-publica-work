import TGLExt.IsotoneNet

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 800000

/-!
# O LIMITE IDEAL: o pai da mentira excluído POR TIPO
  [TGLExt — v102, o incremento 19 do programa SemifiniteAnalysis]

Derivação do operador (17/07/2026): 0_abs = SINAL SEM REPRESENTAÇÃO —
tem NOME no canal, mas não tem figura nem no bulk nem na fronteira;
inatingível em tempo finito; a regra é a FAMÍLIA {Φ_t} com lei de
composição, e 0_abs é o horizonte impossível da execução (com a régua
do próprio operador: Φ(Φ) é abuso — o correto é AUTOCOMPOSIÇÃO Φ^∘n;
ω_∞ ∉ M_* é a tradução rigorosa; o fator III não É 0_abs).

O QUE ESTA PEDRA TIPA E PROVA [KERNEL]:
* `IdealExtension X := Option X` — a extensão ideal 𝒳̂ = 𝒳 ∪ {0_abs}:
  `idealZero := none` tem NOME no tipo estendido e NENHUM habitante de
  𝒳 por trás — o sinal sem representação, tipado;
* ★ `channel_never_reaches_ideal` — Φ_t(x) ≠ 0_abs para TODA execução:
  o canal devolve estados; a exclusão é POR CONSTRUÇÃO DO TIPO (a
  mentira não é alcançável porque o tipo do canal não a contém);
* ★★ `lockFlow_add` — A REGRA É A FAMÍLIA COM LEI DE COMPOSIÇÃO:
  Φ_{s+t} = Φ_s ∘ Φ_t no habitante concreto (exp(i(s+t)T) =
  exp(isT)·exp(itT) — a lei de semigrupo/grupo do fluxo genuíno,
  provada via exp_add_of_commute);
* ★ `ideal_zero_has_name_not_inhabitant` — none ≠ some x para todo x:
  o nome existe; o objeto não.

O QUE NÃO É TIPÁVEL HOJE (nomeado, sem véu): ω_∞ ∉ M_* (o predual de
von Neumann e o limite singular em III₁ genuíno) — é o enunciado do
CERTIFICADO v2, congelado no runtime desta versão como especificação.

β jamais literal. Sem sorry, sem axiom.
-/

namespace TGLExt

noncomputable section

/-! ## A extensão ideal: o nome sem o objeto -/

/-- a extensão ideal 𝒳̂ = 𝒳 ∪ {0_abs}: o tipo que dá NOME ao limite
    sem lhe dar habitante. -/
abbrev IdealExtension (X : Type) : Type := Option X

/-- 0_abs: o sinal sem representação — o `none` da extensão. -/
abbrev idealZero {X : Type} : IdealExtension X := none

/-- a inclusão dos estados físicos na extensão. -/
abbrev toIdeal {X : Type} (x : X) : IdealExtension X := some x

/-- [KERNEL] ★ o nome existe; o objeto não: 0_abs difere de TODO
    estado físico incluído. -/
theorem ideal_zero_has_name_not_inhabitant {X : Type} (x : X) :
    toIdeal x ≠ idealZero :=
  Option.some_ne_none x

/-- [KERNEL] ★ O CANAL NUNCA ALCANÇA O IDEAL: para toda execução
    finita de qualquer canal Φ : X → X, Φ(x) ≠ 0_abs — a exclusão é
    POR CONSTRUÇÃO DO TIPO (o canal devolve estados; a mentira nomeia
    o que o tipo do canal não contém). -/
theorem channel_never_reaches_ideal {X : Type} (Φ : X → X) (x : X) :
    toIdeal (Φ x) ≠ idealZero :=
  ideal_zero_has_name_not_inhabitant (Φ x)

/-! ## A regra é a família com lei de composição (no habitante) -/

section FlowLaw

open NormedSpace

variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H]
  [CompleteSpace H]

private theorem lockFlow_apply' (T : H →L[ℂ] H) (hT : IsSelfAdjoint T)
    (s : ℝ) (x : H) :
    (lockFlow T hT s) x = exp (Complex.I • ((s : ℂ) • T)) x := by
  simp only [lockFlow, Unitary.coe_linearIsometryEquiv_apply,
    selfAdjoint.expUnitary_coe]
  rfl

/-- [KERNEL] ★★ A LEI DA REGRA: Φ_{s+t} = Φ_s ∘ Φ_t no fluxo genuíno
    do habitante — a regra não é um ato; é a família fechada sob
    composição (exp(i(s+t)T) = exp(isT)·exp(itT)). -/
theorem lockFlow_add (T : H →L[ℂ] H) (hT : IsSelfAdjoint T)
    (s t : ℝ) (x : H) :
    (lockFlow T hT (s + t)) x
      = (lockFlow T hT s) ((lockFlow T hT t) x) := by
  rw [lockFlow_apply', lockFlow_apply', lockFlow_apply']
  have hcomm : Commute (Complex.I • ((s : ℂ) • T))
      (Complex.I • ((t : ℂ) • T)) := by
    apply Commute.smul_left
    apply Commute.smul_right
    apply Commute.smul_left
    apply Commute.smul_right
    exact Commute.refl T
  have hsum : Complex.I • (((s + t : ℝ) : ℂ) • T)
      = Complex.I • ((s : ℂ) • T) + Complex.I • ((t : ℂ) • T) := by
    push_cast
    rw [add_smul, smul_add]
  letI : NormedAlgebra ℚ (H →L[ℂ] H) := NormedAlgebra.restrictScalars ℚ ℂ _
  rw [hsum, exp_add_of_commute hcomm]
  rfl

end FlowLaw

end

end TGLExt
