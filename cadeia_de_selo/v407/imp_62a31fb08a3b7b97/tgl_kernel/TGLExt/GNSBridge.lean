import TGLExt.VariationalInhabitant

set_option autoImplicit false
set_option linter.unusedSectionVars false

/-!
# A ponte GNS: o estado é o primitivo — a representação vem dele
  [TGLExt — v53, a FLEXÃO começa (Degrau 3)]

A derivação do operador (v52) estabeleceu: o habitante é o FUNCIONAL; a
observação é o pareamento; a representação vem do estado. A mathlib
JÁ TEM a construção GNS (`PositiveLinearMap.GNS`, `gnsStarAlgHom`) e o
`StandardSubspace` (com Tomita/KMS declarados como TODO do próprio
arquivo da mathlib). Este arquivo constrói a PONTE:

* ★ **O ESTADO DA FRONTEIRA É UM FUNCIONAL POSITIVO** (`gibbs_nonneg` +
  `gibbs_monotone` + `boundaryState`): `gibbs ρ` com `ρ ⪰ 0` é linear e
  MONÓTONO na ordem de Loewner — o par (léxico, expressão) tipado como
  `Matrix n n ℂ →ₚ[ℂ] ℂ`;
* **A INSTANCIAÇÃO DO GNS: NEGATIVO HONESTO NOMEADO** — o GNS da
  mathlib existe e o funcional está pronto, mas a instanciação sobre
  `Matrix n n ℂ` trava no elaborador (whnf timeout na defeq da pilha de
  instâncias C*/completamento): FALHA NOMEADA
  `gns_matrix_instance_whnf_timeout` — atrito de ENGENHARIA, não de
  matemática. Rotas para a próxima pedra: instância global upstream, ou
  GNS finito sem completamento (PreGNS já é completo em dim finita).

**HONESTIDADE.** O conteúdo REAL desta pedra: o estado da fronteira
como funcional linear positivo TIPADO (`→ₚ[ℂ]` — o habitante no
predual, v52, agora no tipo da mathlib) com positividade e monotonia
[KERNEL]. A composição com o GNS contínuo fica bloqueada e NOMEADA.
O que segue: Tomita/KMS no GNS (o TODO declarado da própria mathlib —
`StandardSubspace`), produto cruzado contínuo, fatores. β JAMAIS
entra: ρ genérico. Sem sorry, sem axiom. Negativo honesto é resultado.
-/

namespace TGLExt

open Matrix
open scoped ComplexOrder MatrixOrder Matrix.Norms.L2Operator

noncomputable section

variable {n : Type} [Fintype n] [DecidableEq n]

/-- A instância-pacote C* das matrizes, montada dos pais escopados
    (`Matrix.Norms.L2Operator`): o GNS da mathlib a exige inteira; os
    campos são EXATAMENTE as instâncias diretas (defeq por construção). -/
scoped instance : NonUnitalCStarAlgebra (Matrix n n ℂ) := fast_instance% { }

/-! ## A — o estado da fronteira é um funcional positivo -/

/-- [KERNEL] ★ POSITIVIDADE: `gibbs ρ x ≥ 0` para `ρ, x ⪰ 0` — o estado
    da fronteira respeita a ordem (rota: `√ρ·x·√ρ ⪰ 0` + ciclo do
    traço + `√ρ·√ρ = ρ`). -/
theorem gibbs_nonneg {ρ x : Matrix n n ℂ} (hρ : ρ.PosSemidef)
    (hx : x.PosSemidef) : 0 ≤ gibbs ρ x := by
  have hΩ : (Omega ρ)ᴴ = Omega ρ := omega_conjTranspose ρ
  have hpsd : (Omega ρ * x * (Omega ρ)ᴴ).PosSemidef :=
    hx.mul_mul_conjTranspose_same (Omega ρ)
  rw [hΩ] at hpsd
  have hnn : (0 : Matrix n n ℂ) ≤ ρ := nonneg_iff_posSemidef.mpr hρ
  have hsq : Omega ρ * Omega ρ = ρ := CFC.sqrt_mul_sqrt_self ρ hnn
  have htr : (Omega ρ * x * Omega ρ).trace = gibbs ρ x := by
    unfold gibbs
    rw [Matrix.trace_mul_cycle, hsq]
  rw [← htr]
  exact hpsd.trace_nonneg

/-- [KERNEL] ★ MONOTONIA: `a ≤ b ⟹ gibbs ρ a ≤ gibbs ρ b` (ordem de
    Loewner) — o funcional da fronteira é ORDENADO: um estado genuíno. -/
theorem gibbs_monotone {ρ : Matrix n n ℂ} (hρ : ρ.PosSemidef)
    {a b : Matrix n n ℂ} (hab : a ≤ b) : gibbs ρ a ≤ gibbs ρ b := by
  have hdiff : (b - a).PosSemidef := le_iff.mp hab
  have hsub : gibbs ρ (b - a) = gibbs ρ b - gibbs ρ a := by
    unfold gibbs
    rw [Matrix.mul_sub, Matrix.trace_sub]
  have h0 := gibbs_nonneg hρ hdiff
  rw [hsub] at h0
  exact sub_nonneg.mp h0

/-! ## B — o funcional tipado e o GNS como termo -/

/-- ★ O ESTADO DA FRONTEIRA como funcional linear positivo
    (`Matrix n n ℂ →ₚ[ℂ] ℂ`) — o habitante no PREDUAL, tipado. -/
noncomputable def boundaryState (ρ : Matrix n n ℂ) (hρ : ρ.PosSemidef) :
    Matrix n n ℂ →ₚ[ℂ] ℂ :=
  { toFun := gibbs ρ
    map_add' := pairing_bilinear_right ρ
    map_smul' := fun c a => by simp [gibbs]
    monotone' := fun a b hab => gibbs_monotone hρ hab }

@[simp] theorem boundaryState_apply (ρ : Matrix n n ℂ) (hρ : ρ.PosSemidef)
    (a : Matrix n n ℂ) : boundaryState ρ hρ a = gibbs ρ a := rfl

/-! ## C — a instanciação do GNS: atrito de engenharia NOMEADO

O GNS da mathlib (`PositiveLinearMap.GNS`, `gnsStarAlgHom`) existe e o
funcional da fronteira está tipado acima — mas a instanciação sobre
`Matrix n n ℂ` TRAVA nesta rev: `whnf timeout` (1M heartbeats, mesmo com
`fast_instance%`) na defeq entre a instância-pacote C* e as diretas,
através da pilha do completamento. FALHA NOMEADA:
`gns_matrix_instance_whnf_timeout` — atrito de ENGENHARIA (arquitetura
de instâncias), não de matemática: o funcional é positivo [KERNEL], a
construção existe [mathlib], a composição está bloqueada no elaborador.
Rotas para a próxima pedra: instância global upstream, ou GNS
reimplementado para o caso finito (sem completamento — o PreGNS já é
completo em dimensão finita). Negativo honesto é resultado. -/

end

end TGLExt
