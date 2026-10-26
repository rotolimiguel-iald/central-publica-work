import TGLExt.TowerDefinite
import Mathlib.Analysis.InnerProductSpace.Completion

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

/-!
# A PEDRA 84 — TowerHilbert: o completamento H_φ — o ESPAÇO do fator existe
  [TGLExt — v131, Bloco A do PLANO_ULTIMA_FLAG, pedra 2 de 5]

A pedra 83 deu o pré-Hilbert do colimite. Esta pedra toma o COMPLETAMENTO:

* `TowerHilbert P := UniformSpace.Completion (TowerPre P)` — H_φ, com as
  instâncias da mathlib: `NormedAddCommGroup` + `InnerProductSpace ℂ` +
  `CompleteSpace` — UM ESPAÇO DE HILBERT GENUÍNO. O completamento fraco
  deixou de ser não-enunciável: ele está AQUI, como termo;
* `hOmega` — Ω = [1] no completamento; ★ `hOmega_inner_self` — ⟪Ω,Ω⟫ = 1;
  ★ `hOmega_norm` — ‖Ω‖ = 1: o vetor do Nome é unitário em H_φ;
* ★★ `towerPre_denseRange` — a torre é DENSA em H_φ (por construção do
  completamento): todo vetor do espaço do fator é limite de andares finitos.

O QUE RESTA (pedras 85–87): a ação π estendida a B(H_φ), o objeto
M_TGL = (π(torre))'' e a assinatura no limite. β jamais literal.
Sem sorry, sem axiom.
-/

namespace TGLExt

open UniformSpace

noncomputable section

/-- ★★★ H_φ: o espaço de Hilbert do fator — o completamento do colimite
    da torre. As instâncias (normado, produto interno, completo) vêm da
    mathlib: o espaço EXISTE como termo. -/
abbrev TowerHilbert (P : SiteProfile) : Type := Completion (TowerPre P)

variable {P : SiteProfile}

/-- Ω em H_φ: a imagem do vetor do Nome. -/
def hOmega (P : SiteProfile) : TowerHilbert P :=
  (towerOmega P : TowerPre P)

/-- [KERNEL] ★ ⟪Ω,Ω⟫ = 1 em H_φ (o produto interno estende o da torre). -/
theorem hOmega_inner_self :
    inner ℂ (hOmega P) (hOmega P) = (1 : ℂ) := by
  unfold hOmega
  rw [Completion.inner_coe]
  exact towerOmega_inner_self

/-- [KERNEL] ★ ‖Ω‖ = 1: o vetor do Nome é unitário no espaço do fator. -/
theorem hOmega_norm : ‖hOmega P‖ = 1 := by
  have h2 : ‖hOmega P‖ ^ 2 = 1 := by
    rw [norm_sq_eq_re_inner (𝕜 := ℂ) (hOmega P), hOmega_inner_self]
    rfl
  have hnn : 0 ≤ ‖hOmega P‖ := norm_nonneg _
  nlinarith [h2, hnn]

/-- [KERNEL] ★★ A TORRE É DENSA EM H_φ: todo vetor do espaço do fator é
    limite de vetores de andar finito — o completamento é do colimite. -/
theorem towerPre_denseRange :
    DenseRange ((↑) : TowerPre P → TowerHilbert P) :=
  Completion.denseRange_coe

/-- [KERNEL] ★ H_φ é COMPLETO (Hilbert): a instância existe como termo. -/
theorem towerHilbert_complete : CompleteSpace (TowerHilbert P) :=
  inferInstance

end

end TGLExt
