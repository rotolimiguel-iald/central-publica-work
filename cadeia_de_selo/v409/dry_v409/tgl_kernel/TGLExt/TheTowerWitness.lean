import TGLExt.TheTowerConjugation
import TGLExt.TowerDefinite

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

/-!
# A TESTEMUNHA DESCE AO COLIMITE — J existe na torre
  [BANCADA — 26/08/2026 · marco M4, item 4 da dívida · ordem «pague»]

## O passo

A v227 provou que a conjugação **atravessa o degrau**. Isso é exatamente a condição de
compatibilidade que faz uma função descer a um quociente. Esta pedra usa a condição:
primeiro estende a compatibilidade do degrau ao **empurrão inteiro** (indução), depois
**desce `J` ao colimite `TowerPre`** — e prova ali as leis do andar.

## O que se prova

* ★★★ **`towerJ_commutes_with_tPush`** — a conjugação comuta com o empurrão a QUALQUER
  andar acima (indução sobre o degrau);
* ★★★ **`towerJpre`** — **`J` EXISTE NO COLIMITE**: desce ao quociente, bem-definida;
* ★★ `towerJpre_tof` — e vale ponto a ponto: `J[a]_N = [J_N a]_N`;
* ★★★ `towerJpre_involutive` — **`J² = 1` no colimite inteiro**;
* ★★★ `towerJpre_fixes_omega` — **`J Ω = Ω`**: o vácuo do Nome é J-fixo na torre.

## O QUE FALTA (dito, sem véu)
Aditividade e antilinearidade no colimite (as operações usam supremos de andares), a
extensão ao completamento (mecanismo da v225) e as DUAS cláusulas de comutante contra
`theFactorObject`/`commAlg`. Só então o `ModularRealizationCertificate` se habita. Até
lá o razonete lê ABERTO. β jamais entra. Nada move o gate.
-/

namespace TGLExt

open Matrix

variable {P : SiteProfile}

/-- ★★★ **A CONJUGAÇÃO COMUTA COM O EMPURRÃO** a qualquer andar acima. -/
theorem towerJ_commutes_with_tPush (l : ℝ) (hl : 0 < l) :
    ∀ {N M : ℕ} (h : N ≤ M) (a : Matrix (chainIdx N) (chainIdx N) ℂ),
      tPush h (towerJlevel l N a) = towerJlevel l M (tPush h a) := by
  intro N M h a
  induction M, h using Nat.le_induction with
  | base => rw [tPush_self, tPush_self]
  | succ M hNM ih =>
      rw [tPush_succ hNM, tPush_succ hNM, ih, towerJ_commutes_with_step l hl]

/-- ★★★ **J EXISTE NO COLIMITE**: a conjugação desce ao quociente da torre. -/
noncomputable def towerJpre (l : ℝ) (hl : 0 < l) (P : SiteProfile) :
    TowerPre P → TowerPre P :=
  Quotient.map (fun x : TowerPt => (⟨x.1, towerJlevel l x.1 x.2⟩ : TowerPt))
    (by
      rintro x y ⟨K, hx, hy, e⟩
      refine ⟨K, hx, hy, ?_⟩
      show tPush hx (towerJlevel l x.1 x.2) = tPush hy (towerJlevel l y.1 y.2)
      rw [towerJ_commutes_with_tPush l hl, towerJ_commutes_with_tPush l hl, e])

/-- ★★ **PONTO A PONTO**: `J[a]_N = [J_N a]_N`. -/
theorem towerJpre_tof (l : ℝ) (hl : 0 < l) (N : ℕ)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    towerJpre l hl P (tof P N a) = tof P N (towerJlevel l N a) := rfl

/-- ★★★ **A INVOLUÇÃO NO COLIMITE INTEIRO**: `J² = 1` na torre. -/
theorem towerJpre_involutive (l : ℝ) (hl : 0 < l) (x : TowerPre P) :
    towerJpre l hl P (towerJpre l hl P x) = x := by
  obtain ⟨N, a, rfl⟩ := exists_tof x
  rw [towerJpre_tof, towerJpre_tof]
  congr 1
  exact stateJG_involutive (chainRoot l N) (chainRootInv l N) a
    (chainRoot_isHermitian l N) (chainRoot_mul_inv l hl N)

/-- ★★★ **O VÁCUO DO NOME É J-FIXO NA TORRE**: `J Ω = Ω`. -/
theorem towerJpre_fixes_omega (l : ℝ) (hl : 0 < l) :
    towerJpre l hl P (towerOmega P) = towerOmega P := by
  unfold towerOmega
  rw [towerJpre_tof]
  congr 1
  unfold towerJlevel stateJG
  rw [conjTranspose_one, mul_one, chainRoot_mul_inv l hl]

end TGLExt
